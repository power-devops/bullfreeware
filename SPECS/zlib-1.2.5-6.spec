Summary:	The zlib compression and decompression library
Name:		zlib
Version:	1.2.5
Release:	6
Group:		System Environment/Libraries
Source0:	http://www.zlib.net/%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-aix.patch
URL:		http://www.gzip.org/zlib/
License:	zlib
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

The library is available as 32-bit and 64-bit.

%define libdir64 /opt/freeware/lib64

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
%setup -q
%patch0


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

export CFLAGS="-qmaxmem=16384 -O3"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
./configure \
    --prefix=%{_prefix} \
    --static

make %{?_smp_mflags}

/usr/vac/bin/CreateExportList -X64 %{name}.exp libz.a
${CC} -qmkshrobj libz.a -o libz.so.1 -bE:%{name}.exp
rm -f %{name}.exp libz.a

mkdir -p 64
cp libz.so.1 64/

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
./configure \
    --prefix=%{_prefix} \
    --static

make %{?_smp_mflags}

/usr/vac/bin/CreateExportList -X32 %{name}.exp libz.a
${CC} -qmkshrobj libz.a -o libz.so.1 -bE:%{name}.exp
rm -f %{name}.exp libz.a

${AR} -rv libz.a libz.so.1

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q libz.a 64/libz.so.1

# add AIX Toolbox compatibility member for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp libz.so.1 shr.o
/usr/bin/strip -X32 -e shr.o
${AR} -q libz.a ./shr.o


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

mkdir -p ${RPM_BUILD_ROOT}%{libdir64}
echo "on est sous `pwd`"

cp  64/libz.so.1 ${RPM_BUILD_ROOT}%{libdir64}
cd ${RPM_BUILD_ROOT}%{libdir64}
ln -sf libz.so.1 libz.so
cd -
cp libz.so.1 ${RPM_BUILD_ROOT}%{_libdir}
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
%doc README ChangeLog FAQ
%{_libdir}/*.a
%{_libdir}/*.so*
%{libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%doc README doc/algorithm.txt minigzip.c example.c
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/*
%{_mandir}/man3/*
/usr/include/*


%changelog
* Wed Jul 24 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-6
-  Confusion between libraries 32 et 64bit

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
