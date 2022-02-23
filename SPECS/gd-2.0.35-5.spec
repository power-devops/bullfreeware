Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.0.35
Release:       6
Group:         System Environment/Libraries
License:       BSD-style
URL:           http://www.libgd.org/Main_Page
Source0:       http://www.libgd.org/releases/%{name}-%{version}.tar.bz2
Patch0:  	%{name}-%{version}-aixconfig.patch

BuildRoot:     /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: freetype2-devel >= 2.3.5, fontconfig-devel >= 2.5.0
BuildRequires: libjpeg-devel, libpng-devel, zlib-devel, pkg-config
#BuildRequires: libXpm-devel >= 3.5.7
Requires: freetype2 >= 2.3.5, fontconfig >= 2.5.0
Requires: libjpeg, libpng, zlib
#Requires: libXpm >= 3.5.7

%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.

The library is available as 32-bit and 64-bit.


%package progs
Summary:        Utility programs that use libgd
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images. If you install
these, you must also install gd.


%package devel
Summary:  The development libraries and header files for gd
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config, libjpeg-devel, freetype2-devel >= 2.3.5
Requires: libpng-devel, zlib-devel, fontconfig-devel >= 2.5.0
#Requires: libXpm-devel >= 3.5.7

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.

%prep
%setup -q
%patch0 -p1 -b .aixconfig

%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-static --enable-shared
make

cp .libs/libgd.so.2 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libgd.a ./libgd.so.2


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

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
%defattr(-,root,system,-)
%doc COPYING README-JPEG.TXT index.html entities.html
%{_libdir}/*.a
/usr/lib/*.a


%files progs
%defattr(-,root,system,-)
%{_bindir}/bdftogd
%{_bindir}/gd2copypal
%{_bindir}/gd2togif
%{_bindir}/gd2topng
%{_bindir}/gdcmpgif
%{_bindir}/gdparttopng
%{_bindir}/gdtopng
%{_bindir}/giftogd2
%{_bindir}/pngtogd
%{_bindir}/pngtogd2
%{_bindir}/webpng
/usr/bin/bdftogd
/usr/bin/gd2copypal
/usr/bin/gd2togif
/usr/bin/gd2topng
/usr/bin/gdcmpgif
/usr/bin/gdparttopng
/usr/bin/gdtopng
/usr/bin/giftogd2
/usr/bin/pngtogd
/usr/bin/pngtogd2
/usr/bin/webpng


%files devel
%defattr(-,root,system,-)
%doc index.html
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.la
/usr/bin/gdlib-config
/usr/include/*
/usr/lib/*.la


%changelog
* Thu May 03 2012 Gerard Visiedo <gerard.visiedo àbull.net> - 2.0.35-6
- Build on Aix6.1

* Tue Apr 27 2010 Michael Perzl <michael@perzl.org> - 2.0.35-5
- recompiled thread-safe with cc_r

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 2.0.35-4
- some minor spec file fixes

* Sat Mar 29 2008 Michael Perzl <michael@perzl.org> - 2.0.35-3
- changed to FreeType version 2

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 2.0.35-2
- included both 32-bit and 64-bit shared objects

* Fri Sep 28 2007 Michael Perzl <michael@perzl.org> - 2.0.35-1
- first version for AIX V5.1 and higher
