# From Perzl

# 1 means : ln -s  already done
%define links 1

Name:    pinentry
Version: 1.0.0
Release: 1
Summary: Collection of simple PIN or passphrase entry dialogs

Group:   Applications/System
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

Patch0:  %{name}-%{version}-aix.patch
Patch1:  %{name}-%{version}-gdkkeysyms.h.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: glib2-devel >= 2.34.3-1
BuildRequires: gtk2-devel >= 2.20.1-2
BuildRequires: pango-devel >= 1.24.5-1
BuildRequires: gdk-pixbuf-devel
BuildRequires: libiconv >= 1.14-3

Requires: libiconv >= 1.14-3

Requires: /sbin/install-info, info

%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%endif

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.


%package gtk
Summary: Passphrase/PIN entry dialog based on GTK+
Group:   Applications/System
Requires: %{name} = %{version}-%{release}
Requires: glib2 >= 2.34.3-1
Requires: gtk2 >= 2.20.1-2
Requires: pango >= 1.24.5-1
Requires: libiconv >= 1.14-3

%description gtk
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GTK GUI based version of the PIN entry dialog.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch0
# Not Useful %patch1


%build
export CC="/opt/IBM/xlc/13.1.3/bin/xlc -D_LINUX_SOURCE_COMPAT"
export CC="gcc -maix32 -D_LINUX_SOURCE_COMPAT"

# GDK/GTK/GIO include files have an issue...
if [  %{link} -eq 1 ]; then
	ln -s /opt/freeware/include/gtk-2.0/gdk               /opt/freeware/include/gdk
	ln -s /opt/freeware/include/gtk-2.0/gtk               /opt/freeware/include/gtk
	ln -s /opt/freeware/include/glib-2.0/gio              /opt/freeware/include/gio     
	ln -s /opt/freeware/include/glib-2.0/glib-object.h    /opt/freeware/include/glib-object.h
	ln -s /opt/freeware/include/glib-2.0/gobject          /opt/freeware/include/gobject
	ln -s /opt/freeware/include/glib-2.0/glib.h           /opt/freeware/include/glib.h
	ln -s /opt/freeware/include/glib-2.0/glib             /opt/freeware/include/glib
	ln -s /opt/freeware/lib/glib-2.0/include/glibconfig.h /opt/freeware/include/glibconfig.h
	ln -s /opt/freeware/include/glib-2.0/gmodule.h        /opt/freeware/include/gmodule.h
	ln -s /opt/freeware/include/cairo/cairo.h             /opt/freeware/include/cairo.h
	ln -s /opt/freeware/include/cairo/cairo-version.h     /opt/freeware/include/cairo-version.h
	ln -s /opt/freeware/include/cairo/cairo-features.h    /opt/freeware/include/cairo-features.h
	ln -s /opt/freeware/include/cairo/cairo-deprecated.h  /opt/freeware/include/cairo-deprecated.h
	ln -s /opt/freeware/include/pango-1.0/pango           /opt/freeware/include/pango
	ln -s /opt/freeware/lib/gtk-2.0/include/gdkconfig.h   /opt/freeware/include/gdkconfig.h
	ln -s /opt/freeware/include/gdk-pixbuf-2.0/gdk-pixbuf /opt/freeware/include/gdk-pixbuf 
	ln -s /opt/freeware/include/atk-1.0/atk               /opt/freeware/include/atk
fi



export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib/threads:/usr/vac/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS="$LDFLAGS -lcurses -lgtk-x11-2.0"

./configure \
    --prefix=%{_prefix} \
   --infodir=%{_infodir} \
    --enable-pinentry-curses \
    --enable-fallback-curses \
    --enable-pinentry-gtk2 \
    --disable-pinentry-qt \
    --disable-pinentry-qt5

${CC} ${CFLAGS} -c getopt_long.c
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# for backwards compatibility
ln -s pinentry-gtk-2 ${RPM_BUILD_ROOT}%{_bindir}/pinentry-gtk

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%post
if [ -f %{_infodir}/%{name}.info* ]; then
    /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir ||:
fi


%preun
if [ $1 -eq 0 -a -f %{_infodir}/%{name}.info* ] ; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir ||:
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%{_bindir}/pinentry
%{_bindir}/pinentry-curses
%{_infodir}/pinentry.info*
/usr/bin/pinentry
/usr/bin/pinentry-curses


%files gtk
%defattr(-,root,system,-)
%{_bindir}/pinentry-gtk
%{_bindir}/pinentry-gtk-2
/usr/bin/pinentry-gtk
/usr/bin/pinentry-gtk-2


%changelog
* Fri Nov 17 2017 Tony Reix <tony.reix@atos.net> - 1.0.0-1
- Port on AIX 6.1

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 1.0.0-1
- updated to version 1.0.0

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 0.9.7-1
- updated to version 0.9.7

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 0.8.4-1
- updated to version 0.8.4

* Thu Sep 09 2010 Michael Perzl <michael@perzl.org> - 0.8.0-1
- first version for AIX V5.1 and higher
