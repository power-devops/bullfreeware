Summary:	The zlib compression and decompression library
Name:		zlib
Version:	1.2.5
Release:	1
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
mv libz.so.1 shr.o
/usr/bin/strip -X32 -e shr.o
${AR} -q libz.a ./shr.o


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
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
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc README doc/algorithm.txt minigzip.c example.c
%{_includedir}/*
%{_mandir}/man3/*
/usr/include/*


%changelog
* Thu Jul 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.2.5
- Initial port on Aix 5.3
