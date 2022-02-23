Summary: A library of functions for manipulating PNG image format files
Name: libpng
Version: 1.5.4
Release: 4
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/
Source0: ftp://ftp.simplesystems.org/pub/png/src/%{name}-%{version}.tar.bz2
Source1: libpng.so.3-aix32
Source2: libpng.so.3-aix64
Source3: libpng12.so.0-aix32
Source4: libpng12.so.0-aix64
Source5: libpng14.so.14-aix32
Source6: libpng14.so.14-aix64

Buildroot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: zlib-devel
Requires: zlib

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} zlib-devel pkg-config

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make 

cp .libs/libpng15.so.15 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make 


%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng15.a ./libpng15.so.15

# Add the older v1.2.xx shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} libpng.so.3
/usr/bin/strip -X32 -e libpng.so.3
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng.so.3

cp %{SOURCE2} libpng.so.3
/usr/bin/strip -X64 -e libpng.so.3
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng.so.3

# # copy the old libpng12.a library for compatibility reasons
# cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/
# chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/*.a

# Add the older v1.2.x shared members for compatibility with older apps
cp %{SOURCE3} libpng12.so.0
/usr/bin/strip -X32 -e libpng12.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng12.so.0

cp %{SOURCE4} libpng12.so.0
/usr/bin/strip -X64 -e libpng12.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng12.so.0

# Add the older v1.4.x shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE5} libpng14.so.14
/usr/bin/strip -X32 -e libpng14.so.14
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng14.so.14

cp %{SOURCE6} libpng14.so.14
/usr/bin/strip -X64 -e libpng14.so.14
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng14.so.14

# add compatibility symlink for "libpng14.a"
(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  %{__ln_s} libpng.a libpng12.a 
  %{__ln_s} libpng.a libpng14.a
)

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
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
%doc *.txt example.c README TODO CHANGES LICENSE 
%{_libdir}/*.a
%{_mandir}/man5/*
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
/usr/bin/*
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-3
- Initial port on Aix6.1

* Wed Nov 23 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-2
- Add omitted symbolic link libpng12.a

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.5.4-1
- Update to version 1.5.4-1

* Wed Nov 30 2010 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.2.44-1
 - Update to version 1.2.44

*  Wed Oct 18 2006  BULL
 - Release  5

*  Mon Sep 18 2006  BULL
 - Release  4
 - support 64 bits

*  Fri Jan 06 2006  BULL
 - Release  3
 - added compatmember= shr.o

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit

*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.2.8
