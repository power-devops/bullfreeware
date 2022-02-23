Summary: Library for manipulating GIF format image files
Name: giflib
Version: 4.1.6
Release: 1
License: MIT
URL: http://www.sf.net/projects/giflib/
Source0: http://dl.sf.net/giflib/%{name}-%{version}.tar.bz2
Source1: http://dl.sf.net/giflib/SHA1SUMS.asc
Patch0:  %{name}-%{version}-aixconfig.patch
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: sed

Obsoletes: libungif <= %{version}-%{release}
Provides: libungif <= %{version}-%{release}

%description
The giflib package contains a shared library of functions for
loading and saving GIF format image files.  It is API and ABI compatible
with libungif, the library which supported uncompressed GIFs while the
Unisys LZW patent was in effect.

Install the giflib package if you need to write programs that use GIF files.
You should also install the giflib-utils package if you need some simple
utilities to manipulate GIFs.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development tools for programs which will use the libungif library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libungif-devel <= %{version}-%{release}
Obsoletes: libungif-devel <= %{version}-%{release}

%description devel
This package contains the static libraries, header files and
documentation necessary for development of programs that will use the
giflib library to load and save GIF format image files.

You should install this package if you need to develop programs which
will use giflib library functions.  You'll also need to install the
giflib package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%package utils
Summary: Programs for manipulating GIF format image files
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}
Obsoletes: libungif-progs <= %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating
GIF format image files.

Install this package if you need to manipulate GIF format image files.
You'll also need to install the giflib package.


%prep
%setup -q
%patch0 -p1 -b .aixconfig
/opt/freeware/bin/sed -i 's/\r//' doc/lzgif.txt


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make 

cp lib/.libs/libgif.so.4 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q lib/.libs/libgif.a ./libgif.so.4


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
make DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/lib || :
  mkdir -p usr/include || :
  mkdir -p usr/bin || :
  cd usr/lib
  ln -sf ../..%{_libdir}/* .
  cd ../include
  ln -sf ../..%{_includedir}/* .
  cd ../bin
  ln -sf ../..%{_bindir}/* .
)


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc COPYING README UNCOMPRESSED_GIF NEWS ONEWS
%doc ChangeLog TODO BUGS AUTHORS
%{_libdir}/lib*.a
/usr/lib/lib*.a


%files devel
%defattr(-,root,system)
%doc doc/* util/giffiltr.c util/gifspnge.c
%{_libdir}/lib*.la
%{_includedir}/*.h
/usr/lib/lib*.la
/usr/include/*.h


%files utils
%defattr(-,root,system)
%{_bindir}/*
/usr/bin/*


%changelog
* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 4.1.6-1
- Initial port on Aix6.1
