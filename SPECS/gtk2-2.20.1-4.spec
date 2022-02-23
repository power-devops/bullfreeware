# Note that this is NOT a relocatable package

#
# we MUST move 'xfixes.pc' out of the way as otherwise there will be
# -DHAVE_FIXES=1 defined and there is no /usr/include/X11/extensions/Xfixes.h
# before AIX 6.1 and then the compilation will stop:
#
# mv /opt/freeware/lib/pkgconfig/xfixes.pc /opt/freeware/lib/pkgconfig/xfixes.pc-SAVE
#

%define glib2_base_version 2.24.2
%define glib2_version %{glib2_base_version}-1
%define pango_base_version 1.24.5
%define pango_version %{pango_base_version}-1
%define atk_base_version 1.30.0
%define atk_version %{atk_base_version}-1
%define cairo_base_version 1.8.10
%define cairo_version %{cairo_base_version}-1
%define libpng_version 1.2.46-1
%define libtiff_version 3.9.4-2

%define base_version 2.20.1
%define bin_version 2.10.0

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk2
Version: %{base_version}
Release: 4
License: LGPLv2+
Group: System Environment/Libraries
Source0: http://download.gnome.org/sources/gtk+/2.20/gtk+-%{version}.tar.bz2
Source1: http://download.gnome.org/sources/gtk+/2.20/gtk+-%{version}.sha256sum
Source2: update-gdk-pixbuf-loaders
Source3: update-gtk-immodules

# https://bugzilla.gnome.org/show_bug.cgi?id=583273
Patch2: %{name}-%{version}-icon-padding.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599617
Patch4: %{name}-%{version}-fresh-tooltips.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=599618
Patch8: %{name}-%{version}-tooltip-positioning.patch
# http://bugzilla.redhat.com/show_bug.cgi?id=529364
Patch11: %{name}-%{version}-remove-connecting-reason.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=611313
Patch15: %{name}-%{version}-window-dragging.patch
Patch16: %{name}-%{version}-png.patch

BuildRequires: make, patch
## VSD BuildRequires: gcc >= 4.2.3-2
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: fontconfig-devel >= 2.8.0-1
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
## VSD BuildRequires: gettext >= 0.10.40-6
## VSD BuildRequires: gettext-progs >= 0.17-2
BuildRequires: libXrender-devel >= 0.9.5-1
BuildRequires: libjpeg-devel >= 6b-7
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: libtiff-devel >= %{libtiff_version}
BuildRequires: jasper-devel >= 1.900.1-2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# Conflicts with packages containing theme engines
# built against the 2.4.0 ABI
Conflicts: gtk2-engines < 2.7.4-7
Conflicts: libgnomeui < 2.15.1cvs20060505-2

Provides: gail = %{version}-%{release}
Obsoletes: gail < 2.13.0-1

URL: http://www.gtk.org

# We need to prereq these so we can run gtk-query-immodules-2.0
PreReq:   atk >= %{atk_version}
PreReq:   cairo >= %{cairo_version}
PreReq:   fontconfig >= 2.8.0-1
PreReq:   glib2 >= %{glib2_version}
#PreReq:   libgcc >= 4.2.3-2
PreReq:   pango >= %{pango_version}
PreReq:   gettext >= 0.10.40-6
PreReq:   libXrender >= 0.9.5-1
PreReq:   libjpeg >= 6b-7
PreReq:   libpng >= %{libpng_version}
# and these for gdk-pixbuf-query-loaders
PreReq:   libtiff >= %{libtiff_version}
PreReq:   jasper >= 1.900.1-2

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
Requires: libpng-devel >= 1.2.46-1
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
export PATH=/opt/freeware/bin:$PATH
%setup -q -n gtk+-%{version}
%patch2 -p1 -b .icon-padding
%patch4 -p1 -b .fresh-tooltips
%patch8 -p1 -b .tooltip-positioning
%patch11 -p1 -b .remove-connecting-reason
%patch15 -p1 -b .window-dragging
%patch16 -p1 -b .png
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export PATH=/opt/freeware/bin:$PATH
export RM="/usr/bin/rm -f"

export CFLAGS="-g -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -D_LARGE_FILES \
	-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE \
	-DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include/glib-2.0 \
	-I/opt/freeware/lib/glib-2.0/include -I/usr/include/cairo \
	-I/-I/opt/freeware/include/atk-1.0/atk -I/opt/freeware/include/freetype2 \
	-I/usr/include/pango-1.0 -I/opt/freeware/include/gio-unix-2.0"

export CXXFLAGS="-g -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -D_LARGE_FILES \
	-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE \
	-DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include/glib-2.0 \
	-I/opt/freeware/lib/glib-2.0/include -I/usr/include/cairo \
	-I/-I/opt/freeware/include/atk-1.0/atk -I/opt/freeware/include/freetype2 \
	-I/usr/include/pango-1.0 -I/opt/freeware/include/gio-unix-2.0"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
## VSD export CC="gcc -maix64 -D_LARGE_FILES"
export CC="/usr/vac/bin/xlc_r -q64  -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-silent-rules \
    --disable-cups

gmake %{?_smp_mflags}

# avoid "busy" error messages...
slibclean

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
## VSD export CC="gcc -maix32 -D_LARGE_FILES"
export CC="/usr/vac/bin/xlc_r -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-silent-rules \
    --disable-cups

gmake %{?_smp_mflags}

# avoid "busy" error messages...
slibclean


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

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

for dir in ${RPM_BUILD_ROOT}%{_libdir} \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/engines \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/immodules \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/loaders \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/printbackends \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/modules \
           ; do
    cd ${dir}
    for f in *.a ; do
        ar -X32 -x ${f}
    done
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
        ar -X64 -x ${f}
    done
done

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

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
/opt/freeware/bin/update-gdk-pixbuf-loaders
/opt/freeware/bin/update-gtk-immodules


%post immodules
/opt/freeware/bin/update-gtk-immodules


%post immodule-xim
/opt/freeware/bin/update-gtk-immodules


%postun
if [ $1 -gt 0 ]; then
    /opt/freeware/bin/update-gdk-pixbuf-loaders
    /opt/freeware/bin/update-gtk-immodules
fi


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

%dir /etc/gtk-2.0

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
/usr/lib/lib*.so*
/usr/lib64/lib*.so*


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
/usr/lib/lib*.la
/usr/lib64/lib*.la


%files devel-docs
%defattr(-,root,system)
%doc 32bit/tmpdocs/tutorial
%doc 32bit/tmpdocs/faq
%doc 32bit/tmpdocs/examples
%{_datadir}/gtk-doc/html/*
# oops, man pages went missing
# %{_mandir}/man1/*


%changelog
* Mon Oct 07 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 2.20.1-4
- Rebuild due to libX11 issue

* Tue May 14 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.20.1-3
- Initial port on Aix6.1

* Mon Feb 04 2013 Michael Perzl <michael@perzl.org> - 2.20.1-2
- fixed more 'PreReqs' for update-gdk-pixbuf-loaders and update-gtk-immodules

* Thu Jan 31 2013 Michael Perzl <michael@perzl.org> - 2.20.1-1
- updated to version 2.20.1

* Wed Jan 30 2013 Michael Perzl <michael@perzl.org> - 2.18.9-3
- fixed the non-working scripts which are not working in 64-bit mode:
  update-gdk-pixbuf-loaders and update-gtk-immodules
- updated dependencies to current levels

* Thu Dec 16 2010 Michael Perzl <michael@perzl.org> - 2.18.9-2
- removed dependency on gettext >= 0.17

* Mon Mar 29 2010 Michael Perzl <michael@perzl.org> - 2.18.9-1
- updated to version 2.18.9

* Thu Feb 18 2010 Michael Perzl <michael@perzl.org> - 2.18.7-1
- updated to version 2.18.7

* Wed Jan 13 2010 Michael Perzl <michael@perzl.org> - 2.18.6-1
- updated to version 2.18.6

* Tue Dec 15 2009 Michael Perzl <michael@perzl.org> - 2.18.5-1
- updated to version 2.18.5

* Mon Nov 23 2009 Michael Perzl <michael@perzl.org> - 2.18.3-1
- updated to version 2.18.3

* Fri Nov 20 2009 Michael Perzl <michael@perzl.org> - 2.16.6-1
- updated to version 2.16.6

* Wed Aug 26 2009 Michael Perzl <michael@perzl.org> - 2.16.4-1
- first version for AIX V5.1 and higher
