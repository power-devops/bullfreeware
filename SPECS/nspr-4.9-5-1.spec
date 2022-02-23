Summary:        Netscape Portable Runtime
Name:           nspr
Version:        4.9.5
Release:        1
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://www.mozilla.org/projects/nspr/
Group:          System Environment/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
# Sources available at ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/
Source0:        %{name}-%{version}.tar.gz
Patch0:		%{name}-4.9-aixconf.patch

%description
NSPR provides platform independence for non-GUI operating system 
facilities. These facilities include threads, thread synchronization, 
normal file and network I/O, interval timing and calendar time, basic 
memory management (malloc and free) and shared library linking.

The library is available as 32-bit and 64-bit.

%package devel
Summary:        Development libraries for the Netscape Portable Runtime
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Header files for doing development with the Netscape Portable Runtime.

The library is available as 32-bit and 64-bit.

%prep
%setup -q
%patch0 -p1 -b .aixconf

%build
# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64" 
export OBJECT_MODE=64

./mozilla/nsprpub/configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir}64 \
    --includedir=%{_includedir}/nspr4 \
    --enable-64bit \
    --disable-debug
gmake %{?_smp_mflags}

cp config/nspr-config config/nspr-config_64

# build 64-bit shared objects for AIX
(
  cd dist/lib
  for file in libnspr4 libplc4 libplds4
  do
       /usr/bin/rm -f ${file}.so
      /usr/vac/bin/CreateExportList -X64 ${file}.exp ${file}.a
  done

${CC} -qmkshrobj libnspr4.a -o libnspr4.so -bE:libnspr4.exp -bmaxdata:0x80000000 -lpthreads -lodm -lcfg
${CC} -qmkshrobj libplc4.a -o libplc4.so -bE:libplc4.exp -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads
${CC} -qmkshrobj libplds4.a -o libplds4.so -bE:libplds4.exp -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads

for file in libnspr4 libplc4 libplds4
do
 	cp ${file}.so ../..
       /usr/bin/rm -f ${file}.exp
done

)

gmake distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r" 
export OBJECT_MODE=32

./mozilla/nsprpub/configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir}/nspr4 \
    --disable-debug
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}

cp config/nspr-config_64 ${RPM_BUILD_ROOT}%{_bindir}
cp config/nspr-config ${RPM_BUILD_ROOT}%{_bindir}

chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_64
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export CC="/usr/vac/bin/xlc_r" 
export OBJECT_MODE=32

# create 32-bit AIX shared library
(
  cd  ${RPM_BUILD_ROOT}%{_libdir}
  for file in libnspr4 libplc4 libplds4
  do
       /usr/bin/rm -f ${file}.so
      /usr/vac/bin/CreateExportList -X32 ${file}.exp ${file}.a
  done

  ${CC} -qmkshrobj libnspr4.a -o libnspr4.so -bE:libnspr4.exp -bmaxdata:0x80000000 -lpthreads -lodm -lcfg
  ${CC} -qmkshrobj libplc4.a -o libplc4.so -bE:libplc4.exp -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads
  ${CC} -qmkshrobj libplds4.a -o libplds4.so -bE:libplds4.exp -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads

  for file in libnspr4 libplc4 libplds4
  do
	/usr/bin/rm -f ${file}.a
 	${AR} -rv ${file}.a ${file}.so
  	/usr/bin/rm -f ${file}.exp
  done
)

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64
for file in libnspr4 libplc4 libplds4
do
	cp  ${file}.so ${RPM_BUILD_ROOT}%{_libdir}64
done

# add the 64-bit shared objects to the shared libraries already containing
# the 32-bit shared objects
for file in libnspr4 libplc4 libplds4
do
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${file}.so
done


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir}64/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_bindir}/nspr-config*
%{_includedir}/*
%{_datadir}/aclocal/*
/usr/bin/nspr-config*
/usr/include/*


%changelog
* Fri Feb 22 2013 Gerard Visiedo <gerard.visiedo@bul.net> 4.9.5-1
- update to 4.9.5 version

* Mon Mar 26 2012 Patricia Cugny <patricia.cugny@bull.net> 4.9-1
- update to 4.9

* Wed Feb 18 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.7.3
- Initial port for AIX

