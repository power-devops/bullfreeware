Summary: A real-time data compression library.
Name: lzo
Version: 2.05
Release: 1
Group: System Environment/Libraries
License: GPL
Source0: http://www.oberhumer.com/opensource/%{name}/download/%{name}-%{version}.tar.gz
URL: http://www.oberhumer.com/opensource/%{name}/
BuildRoot: /var/tmp/%{name}-%{version}-root

%description
LZO is a portable lossless data compression library written in ANSI C.
It implements a number of algorithms with the following features:
- Decompression is simple and *very* fast.
- Requires no memory for decompression.
- Compression is pretty fast.
- Requires 64 kB of memory for compression.
- Allows you to dial up extra compression at a speed cost in the
  compressor. The speed of the decompressor is not reduced.
- Includes compression levels for generating pre-compressed data which
  achieve a quite competitive compression ratio.
- There is also a compression level which needs only 8 kB for
  compression.
- Supports overlapping compression and in-place decompression.
- Algorithm is thread safe.
- Algorithm is lossless.


%package devel
Summary: Development files for the lzo compression library.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
LZO is a portable lossless data compression library written in ANSI C.
It implements a number of algorithms with many features.

Install the package if you need to build programs that will use the lzo
compression library.


%prep
%setup -q


%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
export CFLAGS="-O2"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make %{?_smp_mflags}

cp src/.libs/liblzo2.so.2 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/liblzo2.a ./liblzo2.so.2


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

cd ${RPM_BUILD_ROOT}
mkdir -p usr/include
mkdir -p usr/lib

cd usr/lib
ln -sf ../..%{_libdir}/* .
cd ../..

cd usr/include
ln -sf ../..%{_includedir}/* .
cd ../..


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS BUGS NEWS README THANKS doc/LZO.FAQ
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc doc/LZO.TXT doc/LZOAPI.TXT
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%changelog
* Tue Jun 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.05
- Initial port on Aix5.3
