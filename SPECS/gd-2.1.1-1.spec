Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.1.1
Release:       1
Group:         System Environment/Libraries
License:       BSD-style
URL:           http://libgd.github.io/
Source0:       https://github.com/libgd/libgd/archive/%{name}-%{version}.tar.gz

BuildRoot:     /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: freetype2-devel >= 2.3.5, fontconfig-devel >= 2.5.0
BuildRequires: libjpeg-devel, libpng-devel, zlib-devel, pkg-config
BuildRequires: libtiff-devel
#BuildRequires: libXpm-devel >= 3.5.7
Requires: freetype2 >= 2.3.5, fontconfig >= 2.5.0
Requires: libjpeg, libpng, zlib, libtiff
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
Requires: libtiff-devel
#Requires: libXpm-devel >= 3.5.7

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.

# %{name}-%{version}.tar.gz file contains a libgd-%{name}-%{version} folder
# so %setup cannot be used, a custom prep is required to add a mv
%prep
cd $RPM_BUILD_DIR
rm -rf %{name}-%{version} libgd-%{name}-%{version}
/bin/gzip -dc $RPM_SOURCE_DIR/%{name}-%{version}.tar.gz | tar -xf -
STATUS=$?
if [ $STATUS -ne 0 ]; then
  exit $STATUS
fi
mv $RPM_BUILD_DIR/libgd-%{name}-%{version} $RPM_BUILD_DIR/%{name}-%{version}
cd %{name}-%{version}
[ `/bin/id -u` = '0' ] && /bin/chown -Rhf root .
[ `/bin/id -u` = '0' ] && /bin/chgrp -Rhf system .
/bin/chmod -Rf a+rX,g-w,o-w .

%build
cd %{name}-%{version}
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./bootstrap.sh
./configure \
  --prefix=/opt/freeware \
  --with-tiff=/opt/freeware \
  --with-xpm=no \
  --enable-shared \
  --enable-static
make

cp src/.libs/libgd.so.3 .
make clean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r -O3"
./configure \
  --prefix=/opt/freeware \
  --with-tiff=/opt/freeware \
  --with-xpm=no \
  --enable-shared \
  --enable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libgd.a ./libgd.so.3


%install
cd %{name}-%{version}
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
%doc %{name}-%{version}/src/COPYING %{name}-%{version}/README %{name}-%{version}/src/entities.html
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
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.la
/usr/bin/gdlib-config
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Feb 25 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.1.1-1
- Updated to version 2.1.1

* Thu May 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.0.35-6
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
