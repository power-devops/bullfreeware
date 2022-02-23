# rpm -ba --define 'dotests 0' libpng-1.5.26-1.spec > libpng-1.5.26-1.spec.res11 2>&1
%{!?dotests:%define DO_TESTS 1}

Summary:	The zlib compression and decompression library
Name:		zlib
Version:	1.2.11
Release:	1
Group:		System Environment/Libraries
Source0:	http://www.zlib.net/%{name}-%{version}.tar.xz
Patch0:		%{name}-%{version}-aix-mandir.patch
Patch1:		%{name}-%{version}-aix-O3.patch
URL:		http://www.gzip.org/zlib/
License:	zlib
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Source1000:	%{name}-%{version}-%{release}.build.log

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

The library is available as 32-bit and 64-bit.

%define _libdir64 %{_prefix}/lib64

%package devel
Summary:	Header files and libraries for Zlib development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
export PATH="/opt/freeware/bin:$PATH"
%setup -q
%patch0
%patch1

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS="-qmaxmem=16384 -O3"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64

export CC="/usr/vac/bin/xlc -q64"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

/usr/vac/bin/CreateExportList -X64 %{name}.exp libz.a
${CC} -qmkshrobj libz.a -o libz.so.1 -bE:%{name}.exp
rm -f %{name}.exp libz.a
${AR} -rv -X64 libz.a libz.so.1


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

export CC="/usr/vac/bin/xlc -q32"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

/usr/vac/bin/CreateExportList -X32 %{name}.exp libz.a
${CC} -qmkshrobj libz.a -o libz.so.1 -bE:%{name}.exp
rm -f %{name}.exp libz.a
${AR} -rv -X32 libz.a libz.so.1


# add AIX Toolbox compatibility member for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp libz.so.1 shr.o
/usr/bin/strip -X32 -e shr.o
${AR} -q libz.a ./shr.o


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..


# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
cd                  ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libz.a	libz.so.1
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libz.a		${RPM_BUILD_ROOT}%{_libdir64}/libz.so.1
cd -

# Add a sym link from 64bit to 32bit libz.a
cd ${RPM_BUILD_ROOT}%{_libdir64}
rm libz.a
ln -s %{_libdir}/libz.a .
cd -

cp 64bit/libz.so.1 ${RPM_BUILD_ROOT}%{_libdir64}
cd ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf libz.so.1 libz.so
cd -

cp 32bit/libz.so.1 ${RPM_BUILD_ROOT}%{_libdir}
cd ${RPM_BUILD_ROOT}%{_libdir}
ln -sf libz.so.1 libz.so

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib lib64
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
%defattr(-,root,system,-)
%doc 32bit/README 32bit/ChangeLog 32bit/FAQ
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%doc 32bit/README 32bit/doc/algorithm.txt 32bit/test/minigzip.c 32bit/test/example.c
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/*
%{_mandir}/man3/*
/usr/include/*


%changelog
* Wed Apr 11 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.2.11-1
- New version 1.2.11
- Add sym link of 32bit libz.a to 64bit libz.a

* Mon May 09 2016 Tony Reix <tony.reix@bull.net> - 1.2.8-3
- Looks like .so files are useful... at least by openssl tests

* Wed Apr 27 2016 Tony Reix <tony.reix@bull.net> - 1.2.8-2
- Fix issues in .spec file (no more deliver .so files)
- Change 32-64 bits management

* Fri Sep 11 2015 Tony Reix <tony.reix@bull.net> - 1.2.8-1
- New version 1.2.8

* Wed Jul 24 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-6
- Confusion between libraries 32 et 64bit

* Tue Jul 16 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-5
- Add librairies .so 

* Wed Jun 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-4
- Add zlib.pc into devel package

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-3
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 1.2.5-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jul 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.2.5
- Initial port on Aix 5.3
