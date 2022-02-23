# rpm -ba --define 'aixX11 1' gtk2-2.24.30-1.spec ...
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

#Used for debugging:
%define with_64bits 1
%define with_configure 1

%define _libdir64 %{_libdir}64

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

%define base_version 2.24.30
# Binary compatibility. See: configure.ac: m4_define([gtk_binary_version], [2.10.0])
%define bin_version 2.10.0
%define patch_version 2.20.1

Summary: The GIMP ToolKit (GTK+), a library for creating GUIs for X
Name: gtk2
Version: %{base_version}
Release: 1%{RELEASE_SUFFIX}
License: LGPLv2+
Group: System Environment/Libraries
Source0: http://download.gnome.org/sources/gtk+/2.24/gtk+-%{version}.tar.xz
Source1: http://download.gnome.org/sources/gtk+/2.24/gtk+-%{version}.sha256sum
Source2: gtk2-%{version}-update-gtk-immodules

# https://bugzilla.gnome.org/show_bug.cgi?id=583273
Patch2: %{name}-%{patch_version}-icon-padding.patch

# https://bugzilla.gnome.org/show_bug.cgi?id=599617
Patch4: %{name}-%{patch_version}-fresh-tooltips.patch
#4 out of 8 hunks FAILED -- saving rejects to file gtk/gtktooltip.c.rej
#1 out of 1 hunk FAILED -- saving rejects to file gtk/gtkwidget.c.rej

# https://bugzilla.gnome.org/show_bug.cgi?id=599618
Patch8: %{name}-%{patch_version}-tooltip-positioning.patch
#1 out of 3 hunks FAILED -- saving rejects to file gtk/gtktooltip.c.rej

# http://bugzilla.redhat.com/show_bug.cgi?id=529364
Patch11: %{name}-%{patch_version}-remove-connecting-reason.patch
#2 out of 2 hunks FAILED -- saving rejects to file modules/printbackends/cups/gtkprintbackendcups.c.rej

# https://bugzilla.gnome.org/show_bug.cgi?id=611313
Patch15: %{name}-%{patch_version}-window-dragging.patch
#1 out of 1 hunk FAILED -- saving rejects to file gtk/gtktoolbar.c.rej

Patch17: %{name}-%{version}-aix-xvfb.patch
Patch18: %{name}-%{version}-aix-defaultvalue.patch


#BuildRequires: make, patch
## VSD BuildRequires: gcc >= 4.2.3-2
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: fontconfig-devel >= 2.8.0-1
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
## VSD BuildRequires: gettext >= 0.10.40-6
## VSD BuildRequires: gettext-progs >= 0.17-2
BuildRequires: libXrender-devel >= 0.9.5-1
BuildRequires: gdk-pixbuf-devel
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: libX11-devel

Requires: libX11
%endif
Requires: gdk-pixbuf

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
echo "AIXX11=%{AIXX11}"
echo "DO_TESTS=%{DO_TESTS}"
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
%setup -q -n gtk+-%{version}
%patch2 -p1 -b .icon-padding
#%patch4 -p1 -b .fresh-tooltips
#%patch8 -p1 -b .tooltip-positioning
#%patch11 -p1 -b .remove-connecting-reason
#%patch15 -p1 -b .window-dragging
#%patch16 -p1 -b .png
%patch17 -p1 -b .xvfb
%patch18 -p1 -b .defaultvalue

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/

%build
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export CONFIG_SHELL=/bin/sh
export CONFIG_ENV_ARGS=/bin/sh
export RM="/usr/bin/rm -f"
export GREP="/opt/freeware/bin/grep"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -B -X32_64"
export CC32="/usr/vac/bin/xlc_r -D_LARGE_FILES"
export CC64="$CC32 -q64"
export CXX32="/usr/vacpp/bin/xlC_r -D_LARGE_FILES"
export CXX64="$CC32 -q64"

# A revoir : -g vs -O2 | I/usr/include/glib-2.0 | -I/usr/include/cairo | -I/usr/include/pango-1.0 
export CFLAGS="-g -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -D_LARGE_FILES \
	-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE \
	-DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include/glib-2.0 \
	-I/opt/freeware/lib/glib-2.0/include -I/usr/include/cairo \
	-I/opt/freeware/include/atk-1.0/atk -I/opt/freeware/include/freetype2 \
	-I/usr/include/pango-1.0 -I/opt/freeware/include/gio-unix-2.0"

export CXXFLAGS="-g -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -D_LARGE_FILES \
	-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE \
	-DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include/glib-2.0 \
	-I/opt/freeware/lib/glib-2.0/include -I/usr/include/cairo \
	-I/opt/freeware/include/atk-1.0/atk -I/opt/freeware/include/freetype2 \
	-I/usr/include/pango-1.0 -I/opt/freeware/include/gio-unix-2.0"


%if %{with_64bits} == 1
# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64

## VSD export CC="gcc -maix64 -D_LARGE_FILES"
export CC=$CC64
export CXX=$CXX64

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

%if %{with_configure}
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-silent-rules \
    --disable-cups
%endif

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi
# avoid "busy" error messages...
slibclean
cd ..
%endif


# now build the 32-bit version
cd 32bit
export OBJECT_MODE=32

## VSD export CC="gcc -maix32 -D_LARGE_FILES"
export CC=$CC32
export CXX=$CXX32

export LDFLAGS="-L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

%if %{with_configure}
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc \
    --enable-shared --disable-static \
    --disable-silent-rules \
    --disable-cups
%endif

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi
# avoid "busy" error messages...
slibclean
cd ..

%install
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

%if %{with_64bits} == 1
cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done
cd ..
%endif

cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/gtk-demo* ${RPM_BUILD_ROOT}%{_bindir}/gtk-query* ${RPM_BUILD_ROOT}%{_bindir}/gtk-update* || :

# Make cleaned-up versions of tutorials, examples, and faq for installation
cd 32bit
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
cd ..

for dir in ${RPM_BUILD_ROOT}%{_libdir} \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/engines \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/immodules \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/%{bin_version}/printbackends \
           ${RPM_BUILD_ROOT}%{_libdir}/gtk-2.0/modules \
           ; do
    cd ${dir}
    for f in *.a ; do
        ar -X32 -x ${f}
    done
done

%if %{with_64bits} == 1
for dir in ${RPM_BUILD_ROOT}%{_libdir64} \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/engines \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/immodules \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/%{bin_version}/printbackends \
           ${RPM_BUILD_ROOT}%{_libdir64}/gtk-2.0/modules \
           ; do
    cd ${dir}
    for f in *.a ; do
        ar -X64 -x ${f}
    done
done

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
for LIB in libgailutil libgdk-x11-2.0 libgtk-x11-2.0; do
    SO=0
    if [ "$LIB" == "libgailutil" ]; then
        SO=18
    fi
    /usr/bin/ar -X64 -xv ${RPM_BUILD_ROOT}%{_libdir64}/${LIB}.a ${LIB}.so.$SO
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/${LIB}.a ${LIB}.so.$SO
done
%endif

# Install wrappers for the binaries
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}/update-gtk-immodules
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
/opt/freeware/bin/update-gtk-immodules


%post immodules
/opt/freeware/bin/update-gtk-immodules


%post immodule-xim
/opt/freeware/bin/update-gtk-immodules


%postun
if [ $1 -gt 0 ]; then
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
%{_bindir}/gtk-demo*
%{_bindir}/gtk-query-immodules-2.0*
%{_bindir}/gtk-update-icon-cache*
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
%{_libdir}/gtk-2.0/%{bin_version}/printbackends
%{_libdir64}/gtk-2.0/%{bin_version}/printbackends
%{_libdir}/gtk-2.0/modules
%{_libdir64}/gtk-2.0/modules

%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_datadir}/themes/Raleigh

%{_datadir}/locale/*/*/*

/usr/bin/gtk-demo*
/usr/bin/gtk-query-immodules-2.0*
/usr/bin/gtk-update-icon-cache*
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
* Thu Jun 9 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.24.30-1
- Updated to version 2.24.30

* Thu Apr 07 2016 Tony Reix <tony.reix@bull.net> - 2.24.28
- First port of version 2.24.28

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
