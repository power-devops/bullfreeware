%define fontconfig_version 2.8.0
%define freetype_version 2.4.2

Summary:	A vector graphics library
Name:		cairo
Version:	1.8.8
Release:	4
URL:		http://cairographics.org
Source:		http://cairographics.org/releases/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-pkgconfig.patch
License:	LGPL/MPL
Group:		System Environment/Libraries
BuildRoot:	/var/tmp/%{name}-%{version}-root

BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: freetype2-devel >= %{freetype_version}
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: pixman-devel
BuildRequires: zlib-devel
Requires: fontconfig >= %{fontconfig_version}
Requires: freetype2 >= %{freetype_version}
Requires: libpng
Requires: libxml2
Requires: pixman
Requires: zlib

%description 
Cairo is a vector graphics library designed to provide high-quality
display and print output. Currently supported output targets include
the X Window System, OpenGL (via glitz), in-memory image buffers, and
image files (PDF, PostScript, and SVG).  Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available (e.g. through the X Render
Extension or OpenGL).

The library is available as 32-bit and 64-bit.


%package devel
Summary: Cairo developmental libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: freetype2-devel >= %{freetype_version}
Requires: libpng-devel
Requires: libxml2-devel
Requires: zlib-devel

%description devel
Developmental libraries and header files required for developing or
compiling software which links to the cairo graphics library, which is
an open source vector graphics library.

%prep
%setup -q
%patch0 -p1 -b .pkgconfig

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export LDFLAGS="-lXrender"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --disable-gtk-doc \
    --enable-shared --disable-static \
    --enable-xlib=yes \
    --enable-xlib-xrender=yes \
    --enable-png=yes \
    --enable-ps=yes \
    --enable-pdf=yes \
    --enable-svg=yes
make

cp ./src/.libs/libcairo.so.2 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --disable-gtk-doc \
    --enable-shared --disable-static \
    --enable-xlib=yes \
    --enable-xlib-xrender=yes \
    --enable-png=yes \
    --enable-ps=yes \
    --enable-pdf=yes \
    --enable-svg=yes 
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
make DESTDIR=$RPM_BUILD_ROOT install

# Due to an inexpected rebuild of the librairy, we force to copy into the
# BUIL_ROOT directory, the library whith the objects with 32 and 64 bit.
#
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm  ./src/.libs/lib%{name}.a
/usr/bin/ar -X32_64 -q ./src/.libs/lib%{name}.a ./src/.libs/lib%{name}.so.2 ./lib%{name}.so.2
cp ./src/.libs/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a

(
  cd $RPM_BUILD_ROOT
  for dir in include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system,-)
%doc AUTHORS BIBLIOGRAPHY BUGS COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1 NEWS README
%{_libdir}/libcairo.a
/usr/lib/libcairo.a


%files devel
%defattr(-,root,system,-)
%{_libdir}/libcairo.la
%{_libdir}/pkgconfig/cairo*.pc
%{_includedir}/cairo/cairo*.h
/usr/include/cairo/cairo*.h
%{_datadir}/gtk-doc/html/cairo/*
/usr/lib/*.la
/usr/include/*


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.8.8-4
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.8.8-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.8.8-2
- Add 64-bit libraries

* Tue Nov 30 2010 Jean Noel Cordenenr <jean-noel.cordenner@bull.net> 1.8.8-1
- updated to version 1.8.8

*  Fri Nov 17 2006  BULL
 - Release  1
 - New version  version: 1.2.4
 - gnome 2.16.1

*  Mon Sep 18 2006  BULL
 - Release  5
 - support 64 bits

*  Wed Jul 26 2006  BULL
 - Release  1
 - New version  version: 1.0.2

*  Mon Feb 13 2006  BULL
 - Release 4
 - Prototype gtk 64 bit - build with type CARD32 = unsigned int
*  Fri Dec 23 2005  BULL
 - Release 3
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  2

*  Fri Nov 04 2005  BULL
 - Release  1
 - New version  version: 1.0.0
