# Version with/without AIX X11
%{!?aixX11:%define AIXX11 0}
%{?aixX11:%define AIXX11 1}

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

%define fontconfig_version 2.8.0
%define freetype_version 2.4.2
%define pixman_version 0.30.0 
%define libpng_version 1.6
%define _libdir64 %{_libdir}64

Summary:	A vector graphics library
Name:		cairo
Version:	1.15.2
Release:	1%{RELEASE_SUFFIX}
URL:		http://cairographics.org
Source:		http://cairographics.org/releases/%{name}-%{version}.tar.xz
Patch0:         cairo-1.15.2-aix-bigendian.patch
Patch1:         cairo-1.15.2-aix-typeof.patch
License:	LGPL/MPL
Group:		System Environment/Libraries
BuildRoot:	/var/tmp/%{name}-%{version}-root

BuildRequires: pkgconfig
BuildRequires: libXrender-devel
#BuildRequires: libxcb-devel
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: freetype2-devel >= %{freetype_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: libffi-devel
BuildRequires: gettext-devel
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: libX11-devel
BuildRequires: libXext-devel

Requires: libX11
Requires: libXext
%endif
Requires: libXrender
#Requires: libxcbx
Requires: libpng >= %{libpng_version}
Requires: pixman >= %{pixman_version}
Requires: freetype2 >= %{freetype_version}
Requires: fontconfig >= %{fontconfig_version}
Requires: zlib
Requires: glib2
Requires: libffi

%description 
Cairo is a vector graphics library designed to provide high-quality
display and print output. Currently supported output targets include
the X Window System, OpenGL (via glitz), in-memory image buffers, and
image files (PDF, PostScript, and SVG).  Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available (e.g. through the X Render
Extension or OpenGL).

The library is available as 32-bit and 64-bit.
%if %{AIXX11} == 1
This package requires AIX X11.
%else
This package requires Bull Freeware X11.
%endif


%package devel
Summary: Cairo developmental libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libXrender-devel
Requires: libpng-devel
#Requires: libxcb-devel
Requires: freetype2-devel >= %{freetype_version}
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: zlib-devel
Requires: glib2-devel
%if %{AIXX11} == 0
Requires: libX11-devel
%endif

%description devel
Developmental libraries and header files required for developing or
compiling software which links to the cairo graphics library, which is
an open source vector graphics library.

%prep
echo "AIXX11=%{AIXX11}"
echo "DO_TESTS=%{DO_TESTS}"
%setup -q
%patch0 -p 1 -b .aix
%patch1 -p 1 -b .aix

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS="-lXrender"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/usr/vac/bin/xlc_r"
export CC64="$CC32 -q64"
export CFLAGS="-D_NO_PROTO -g"
export CXXFLAGS="-g"

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --disable-gtk-doc \
    --enable-shared --disable-static \
    --enable-xlib=yes \
    --enable-xlib-xrender=yes \
    --enable-png=yes \
    --enable-ps=yes \
    --enable-pdf=yes \
    --enable-svg=yes \
    --enable-xcb=no \
    --enable-xcb-shm=no \
    --disable-silent-rules

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi
cd ..


# now build the 32-bit version
cd 32bit
export CC=$CC32
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --disable-gtk-doc \
    --enable-shared --disable-static \
    --enable-xlib=yes \
    --enable-xlib-xrender=yes \
    --enable-png=yes \
    --enable-ps=yes \
    --enable-pdf=yes \
    --enable-svg=yes \
    --enable-xcb=no \
    --enable-xcb-shm=no \
    --disable-silent-rules

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

%define LINKS lib/libcairo*.a
%define LINKS_DEVEL include/cairo lib/libcairo*.la

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# Extract the 64 bit object from the lib
LIBS="libcairo
libcairo-gobject
libcairo-script-interpreter"
cd ${RPM_BUILD_ROOT}%{_libdir64}
for LIB in $LIBS; do
    /usr/bin/ar -X64 xv ${LIB}.a ${LIB}.so.2
done
cd -

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects and extract the 32 bit shared object
cd ${RPM_BUILD_ROOT}%{_libdir}
for LIB in $LIBS; do
    /usr/bin/ar -q -X64 ${LIB}.a ${RPM_BUILD_ROOT}%{_libdir64}/${LIB}.so.2
    /usr/bin/ar -X32 xv ${LIB}.a ${LIB}.so.2
done
cd ${RPM_BUILD_ROOT}%{_libdir}

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir usr/include
LINKS="`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 lib/libcairo*.a lib/libcairo*.la`
include/cairo"
for LINK in $LINKS; do
    if [ ! -e /usr/$LINK ] || [ x`ls -l /usr/$LINK | grep -v "/opt/freeware/$LINK"` == "x" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    else
	echo "Warning: /usr/$LINK already exists and is not a link to /opt/freeware/$LINK"
    fi
done

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/BIBLIOGRAPHY 32bit/BUGS 32bit/COPYING 32bit/COPYING-LGPL-2.1 32bit/COPYING-MPL-1.1 32bit/NEWS 32bit/README
%{_libdir}/libcairo*.a
%{_libdir64}/*.so*
%{_libdir}/*.so*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_libdir}/libcairo*.la
%{_libdir}/pkgconfig/cairo*.pc
%{_includedir}/cairo/cairo*.h
%{_datadir}/gtk-doc/html/cairo/*
/usr/lib/*.la
/usr/include/cairo


%changelog
* Wed Apr 13 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.15.2-1
- Update to version 1.15.2

* Mon Oct 07 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.12.2-3
- Rebuild due to libX11 issue

* Fri Mar 29 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.12.2-2
- Rebuild to libXrender.a issue

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.12.2-1
- Update to version 1.12.2

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
