%{!?dotests: %define dotests 1}
%{!?default_bits: %define default_bits 64}

Summary:        Netscape Portable Runtime
Name:           nspr
Version:        4.13
Release:        1
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://www.mozilla.org/projects/nspr/
Group:          System Environment/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
# Sources available at http://ftp.mozilla.org/pub/mozilla.org/nspr/releases/
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-%{release}.build.log

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

mkdir 32bit
cp -rp nspr 32bit
cp -rp 32bit 64bit


%build

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds

build_nspr() {
    export AR="/usr/bin/ar -X${OBJECT_MODE}"
    LIBDIR=%{_libdir}
    ENABLE_64=--disable-64bit
    if [ "${OBJECT_MODE}" == "64" ]; then
        LIBDIR=%{_libdir}64
        ENABLE_64=--enable-64bit        
    fi
    cd ${OBJECT_MODE}bit/nspr
    echo `date +%Y%m%d_%H%M%S`" : Starting ${OBJECT_MODE}bit build"
    export CC="/usr/vac/bin/xlc_r -q${OBJECT_MODE}"
    ./configure \
        --prefix=%{_prefix} \
        --libdir=${LIBDIR} \
        --includedir=%{_includedir}/nspr4 \
        ${ENABLE_64} --disable-debug

    gmake %{?_smp_mflags}

    # build shared objects for AIX
    (
        cd dist/lib
        for file in libnspr4 libplc4 libplds4
        do
            /usr/bin/rm -f ${file}.so
            /usr/vac/bin/CreateExportList -X${OBJECT_MODE} ${file}.exp ${file}.a
        done

        ${CC} -qmkshrobj libnspr4.a -o libnspr4.so -bE:libnspr4.exp                                                        -bmaxdata:0x80000000 -lodm -lcfg -lpthreads
        ${CC} -qmkshrobj libplc4.a  -o libplc4.so  -bE:libplc4.exp  -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads
        ${CC} -qmkshrobj libplds4.a -o libplds4.so -bE:libplds4.exp -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib -bmaxdata:0x80000000 -L. -lnspr4 -lpthreads
    )
    echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit build completed"
    
    if [ "%{dotests}" == "1" ]; then
        echo `date +%Y%m%d_%H%M%S`" : Starting ${OBJECT_MODE}bit tests"
        cd pr/tests
        make
        (./runtests.sh || true )
        cd -
        echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit tests completed"
    fi
    cd ../..
}

export OBJECT_MODE=64
build_nspr

export OBJECT_MODE=32
build_nspr

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit/nspr
gmake install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
mv ${RPM_BUILD_ROOT}%{_bindir}/nspr-config ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_64


cd 32bit/nspr
gmake install DESTDIR=${RPM_BUILD_ROOT}
cd ../..
mv ${RPM_BUILD_ROOT}%{_bindir}/nspr-config ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_32

chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_64
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/nspr-config_32

DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi
ln -sf nspr-config_${DEFAULT_BITS} ${RPM_BUILD_ROOT}%{_bindir}/nspr-config

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar"

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64

# add the shared objects to the libraries already containing
for file in libnspr4 libplc4 libplds4
do
	${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${RPM_BUILD_ROOT}%{_libdir}64/${file}.so
	${AR} -q -X32 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a ${RPM_BUILD_ROOT}%{_libdir}/${file}.so
done


# add the 64-bit objects to the libraries already containing
# the 32-bit objects
for file in libnspr4 libplc4 libplds4
do
    mkdir $file
    cd $file
	${AR} -x -X64 ${RPM_BUILD_ROOT}%{_libdir}64/${file}.a
    ${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${file}.a *.o
done


(
  cd ${RPM_BUILD_ROOT}%{_libdir}64

  for file in libnspr4 libplc4 libplds4
  do
    ln -sf %{_libdir}/${file}.a .
  done
)

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
%{_libdir}64/*.a
%{_libdir}64/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_bindir}/nspr-config*
%{_includedir}/*
%{_datadir}/aclocal/*
/usr/bin/nspr-config*
/usr/include/*


%changelog
* Fri Oct 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 4.13-1
- Update to version 4.13

* Fri Jun 30 2016 Tony Reix <tony.reix@bull.net> 4.12-1
- Update to 4.12 version
- Add symlink from lib to lib64 for .a files
- No tests are available

* Fri Feb 22 2013 Gerard Visiedo <gerard.visiedo@bul.net> 4.9.5-1
- update to 4.9.5 version

* Mon Mar 26 2012 Patricia Cugny <patricia.cugny@bull.net> 4.9-1
- update to 4.9

* Wed Feb 18 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.7.3
- Initial port for AIX

