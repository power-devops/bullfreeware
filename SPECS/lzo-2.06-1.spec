Summary: A real-time data compression library.
Name: lzo
Version: 2.06
Release: 2
Group: System Environment/Libraries
License: GPL
Source0: http://www.oberhumer.com/opensource/%{name}/download/%{name}-%{version}.tar.gz
URL: http://www.oberhumer.com/opensource/%{name}/
BuildRoot: %{_tmppath}/%{name}-%{version}-root

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
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

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
* Wed Jun 21 2013 Gerard Viseido <gerard.viseido@bull.net> - 2.06-2
- Initial port on Aix6.1

* Tue Aug 23 2011 Michael Perzl <michael@perzl.org> - 2.06-1
- updated to version 2.06

* Sat Apr 23 2011 Michael Perzl <michael@perzl.org> - 2.05-1
- updated to version 2.05

* Mon Nov 08 2010 Michael Perzl <michael@perzl.org> - 2.04-1
- updated to version 2.04

* Fri May 16 2008 Michael Perzl <michael@perzl.org> - 2.03-1
- updated to version 2.03

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 2.02-3
- corrected some SPEC file errors

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 2.02-2
- included both 32-bit and 64-bit shared objects

* Tue Jan 03 2006 Michael Perzl <michael@perzl.org> - 2.02-1
- first version for AIX V5.1 and higher
