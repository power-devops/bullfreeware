%define glib2_version 2.21.3
%define pango_version 1.20
%define atk_version 1.13.0
%define cairo_version 1.6.0
%define libtiff_version 3.6.0

%define base_version 2.18.9
%define bin_version 2.10.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk2
Version: 2.18.9
Release: 3
License: LGPLv2+
Group: System Environment/Libraries
Source: http://download.gnome.org/sources/gtk+/2.18/gtk+-%{version}.tar.gz
Source2: update-gdk-pixbuf-loaders
Source3: update-gtk-immodules
Patch0: gtk+-%{version}-aix.patch
URL: http://www.gtk.org
BuildRoot: /var/tmp/%{name}-%{version}-root

BuildRequires: make
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gettext-devel >= 0.17
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel >= 3.8.2
BuildRequires: libtiff-devel >= 3.6.0
BuildRequires: jasper-devel


# Conflicts with packages containing theme engines
# built against the 2.4.0 ABI
Conflicts: gtk2-engines < 2.7.4-7
Conflicts: libgnomeui < 2.15.1cvs20060505-2

Provides: gail = %{version}-%{release}
Obsoletes: gail < 2.13.0-1


# We need to prereq these so we can run gtk-query-immodules-2.0
Requires: atk >= %{atk_version}
Requires: cairo >= %{cairo_version}
Requires: fontconfig >= 2.5.0
Requires: glib2 >= %{glib2_version}
Requires: pango >= %{pango_version}
Requires: gettext >= 0.17
Requires: libjpeg
Requires: libpng
# and these for gdk-pixbuf-query-loaders
Requires: libtiff >= %{libtiff_version}
Requires: jasper

%define _libdir64 %{_prefix}/lib64

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.


%package immodules
Summary: Input methods for GTK+
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description immodules
The gtk2-immodules package contains standalone input methods that are shipped
as part of GTK+.


%package immodule-xim
Summary: XIM support for GTK+
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description immodule-xim
The gtk2-immodule-xim package contains XIM support for GTK+.


%package devel
Summary: Development files for GTK+
Group: Development/Libraries
Requires: gtk2 = %{version}-%{release}
Requires: pango-devel >= %{pango_version}
Requires: atk-devel >= %{atk_version}
Requires: glib2-devel >= %{glib2_version}
Requires: cairo-devel >= %{cairo_version}
Requires: libpng-devel
Requires: pkg-config

Provides: gail-devel = %{version}-%{release}
Obsoletes: gail-devel < 2.13.0-1

%description devel
This package contains the libraries amd header files that are needed
for writing applications with the GTK+ widget toolkit. If you plan
to develop applications with GTK+, consider installing the gtk2-devel-docs
package.


%package devel-docs
Summary: Developer documentation for GTK+
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel-docs
This package contains developer documentation for the GTK+ widget toolkit.


%prep
%setup -q -n gtk+-%{version}
%patch0
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc_r -q64"
export PATH=/opt/freeware/bin:$PATH
export CFLAGS="-g -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L/opt/freeware/lib64"

LDFLAGS="-L/opt/freeware/lib64" \
LIBPATH="%{_prefix}/lib64:%{_libdir}:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-largefile

LDFLAGS="-L/opt/freeware/lib64" \
LIBPATH="%{_prefix}/lib64:%{_libdir}:/usr/lib64:/usr/lib" \
make

# avoid "busy" error messages...
slibclean

# now build the 32-bit version
cd ../32bit

export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"
export PATH=/opt/freeware/bin:$PATH
export CFLAGS="-g -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L/opt/freeware/lib"

LDFLAGS="-L/opt/freeware/lib" \
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-largefile

LDFLAGS="-L/opt/freeware/lib" \
LIBPATH="%{_libdir}:/usr/lib" \
make

# avoid "busy" error messages...
slibclean


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH

cd 64bit
export OBJECT_MODE=64
LDFLAGS="-L/opt/freeware/lib64" \
LIBPATH="%{_prefix}/lib64:%{_libdir}:/usr/lib64:/usr/lib" \
 make DESTDIR=${RPM_BUILD_ROOT} install

for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

cd ../32bit
export OBJECT_MODE=32
LDFLAGS="-L/opt/freeware/lib" \
LIBPATH="%{_libdir}:/usr/lib" \
  make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Make cleaned-up versions of tutorials, examples, and faq for installation
mkdir -p tmpdocs
cp -pr docs/tutorial/html tmpdocs/tutorial
cp -pr docs/faq/html tmpdocs/faq

for dir in examples/* ; do
    if [ -d ${dir} ] ; then
        mkdir -p tmpdocs/${dir}
        for file in ${dir}/* ; do
            cp ${file} tmpdocs/${dir}
            chmod 0644 tmpdocs/${dir}/*
        done
    fi
done

for dir in ${RPM_BUILD_ROOT}%{_libdir64} \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/engines \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/immodules \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/loaders \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/printbackends \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/modules \
           ; do
    cd ${dir}
    for f in *.a ; do
        /usr/bin/ar -X64 -x ${f}
    done
done

for dir in ${RPM_BUILD_ROOT}%{_libdir} \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/engines \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/immodules \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/loaders \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/printbackends \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/modules \
           ; do
    cd ${dir}
    for f in *.a ; do
        /usr/bin/ar -X32 -x ${f}
	dir_64=$(echo ${dir} | sed "s;lib;lib64;")
	f_so=$(/usr/bin/ar -X32 -tv ${f}| awk '{print $8}')
	/usr/bin/ar -X32_64 -q ${f} ${dir_64}/${f_so}
    done
done

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgailutil.a            ${RPM_BUILD_ROOT}%{_libdir64}/libgailutil.so.18
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgdk-x11-2.0.a         ${RPM_BUILD_ROOT}%{_libdir64}/libgdk-x11-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgdk_pixbuf-2.0.a      ${RPM_BUILD_ROOT}%{_libdir64}/libgdk_pixbuf-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgdk_pixbuf_xlib-2.0.a ${RPM_BUILD_ROOT}%{_libdir64}/libgdk_pixbuf_xlib-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgtk-x11-2.0.a         ${RPM_BUILD_ROOT}%{_libdir64}/libgtk-x11-2.0.so.0

# Install wrappers for the binaries
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}/update-gdk-pixbuf-loaders
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_bindir}/update-gtk-immodules
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

# make symlinks
(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%post
[ ! -d /etc/gtk-2.0 ] && mkdir /etc/gtk-2.0
/opt/freeware/bin/update-gdk-pixbuf-loaders
/opt/freeware/bin/update-gtk-immodules


%post immodules
/opt/freeware/bin/update-gtk-immodules


%post immodule-xim
/opt/freeware/bin/update-gtk-immodules


%postun
if [ $1 -gt 0 ]; then
    /opt/freeware/bin/update-gdk-pixbuf-loaders
    /opt/freeware/bin/gtk-query-immodules-2.0_64
fi
[ -d /etc/gtk-2.0 ] && rm -rf /etc/gtk-2.0


%postun immodules
/opt/freeware/bin/update-gtk-immodules


%postun immodule-xim
/opt/freeware/bin/update-gtk-immodules


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)

%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS 32bit/README
%{_bindir}/gdk-pixbuf-query-loaders*
%{_bindir}/gtk-demo*
%{_bindir}/gtk-query-immodules-2.0*
%{_bindir}/gtk-update-icon-cache*
%{_bindir}/update-gdk-pixbuf-loaders
%{_bindir}/update-gtk-immodules

%{_libdir}/lib*.a
%{_libdir}/lib*.so*
%{_libdir64}/lib*.so*

%dir %{_libdir}/gtk-2.0
%dir %{_libdir64}/gtk-2.0
%dir %{_libdir}/gtk-2.0/%{bin_version}
%dir %{_libdir64}/gtk-2.0/%{bin_version}
%dir %{_libdir}/gtk-2.0/%{bin_version}/immodules
%dir %{_libdir64}/gtk-2.0/%{bin_version}/immodules
%{_libdir}/gtk-2.0/%{bin_version}/engines
%{_libdir64}/gtk-2.0/%{bin_version}/engines
%{_libdir}/gtk-2.0/%{bin_version}/loaders
%{_libdir64}/gtk-2.0/%{bin_version}/loaders
%{_libdir}/gtk-2.0/%{bin_version}/printbackends
%{_libdir64}/gtk-2.0/%{bin_version}/printbackends
%{_libdir}/gtk-2.0/modules
%{_libdir64}/gtk-2.0/modules

%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_datadir}/themes/Raleigh

%{_datadir}/locale/*/*/*

/usr/bin/gdk-pixbuf-query-loaders*
/usr/bin/gtk-demo*
/usr/bin/gtk-query-immodules-2.0*
/usr/bin/gtk-update-icon-cache*
/usr/bin/update-gdk-pixbuf-loaders
/usr/bin/update-gtk-immodules

/usr/lib/lib*.a


%files immodules
%defattr(-,root,system)
%config(noreplace) /etc/gtk-2.0/im-multipress.conf
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-am-et.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ipa.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-multipress.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-thai.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-viqr.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-viqr.so


%files immodule-xim
%defattr(-,root,system)
%{_libdir}/gtk-2.0/%{bin_version}/immodules/im-xim.so
%{_libdir64}/gtk-2.0/%{bin_version}/immodules/im-xim.so


%files devel
%defattr(-,root,system)
%{_bindir}/gdk-pixbuf-csource*
%{_bindir}/gtk-builder-convert*
%{_includedir}/*
%{_libdir}/lib*.la
%{_libdir64}/lib*.la
%{_libdir}/gtk-2.0/include
%{_libdir64}/gtk-2.0/include
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*

%{_datadir}/aclocal/*
%{_datadir}/gtk-2.0

/usr/bin/gdk-pixbuf-csource*
/usr/bin/gtk-builder-convert*
/usr/include/*


%files devel-docs
%defattr(-,root,system)
%doc 32bit/tmpdocs/tutorial
%doc 32bit/tmpdocs/faq
%doc 32bit/tmpdocs/examples
%{_datadir}/gtk-doc/html/*
# oops, man pages went missing
# %{_mandir}/man1/*


%changelog
* Thu Nov 24 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.18.9-3
- Add .so 64bit binary into 32bit .a library archive

* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.18.9-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Sep 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.18.9-1
- Initial port on Aix5.3

