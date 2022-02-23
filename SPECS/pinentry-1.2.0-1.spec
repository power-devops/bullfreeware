# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

# NO gtk !
%bcond_with gtk

Name:    pinentry
Version: 1.2.0
Release: 1
Summary: Collection of simple PIN or passphrase entry dialogs

Group:   Applications/System
License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

Source100: %{name}-%{version}-%{release}.build.log

Patch1:  %{name}-1.1.1-aix.patch
%if %{with gtk}
Patch12:  %{name}-1.1.1-aix-gtk.patch
Patch2:  %{name}-1.1.1-gdkkeysyms.h.patch
%endif
Patch13:  %{name}-1.1.1-aix-Makefile.in.patch

BuildRequires: libgpg-error, libgpg-error-devel
BuildRequires: libassuan, libassuan-devel
%if %{with gtk}
BuildRequires: glib2-devel >= 2.34.3-1
BuildRequires: gtk2-devel >= 2.20.1-2
BuildRequires: pango-devel >= 1.24.5-1
BuildRequires: gdk-pixbuf-devel
%endif

BuildRequires: libiconv >= 1.14-3

Requires: libiconv >= 1.14-3

#Requires: /sbin/install-info, info

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.


%if %{with gtk}
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
%endif


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch1
%if %{with gtk}
%patch12
%patch2
%endif
%patch13


%build
#export CC="/opt/IBM/xlc/13.1.3/bin/xlc -D_LINUX_SOURCE_COMPAT"
export CC="gcc -maix32 -D_LINUX_SOURCE_COMPAT"
export OBJECT_MODE=32

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
#export LDFLAGS="$LDFLAGS -lcurses -lgtk-x11-2.0"
export LDFLAGS="$LDFLAGS -lcurses "

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --disable-pinentry-curses \
    --disable-fallback-curses \
    --disable-rpath \
    --disable-dependency-tracking \
    --without-libcap \
    --disable-pinentry-fltk \
    --disable-pinentry-gnome3 \
%if %{with gtk}
    --enable-pinentry-gtk2 \
%else
    --disable-pinentry-gtk2 \
%endif
    --disable-pinentry-qt5 \
    --disable-pinentry-emacs \
    --enable-pinentry-tty \
    --enable-libsecret

${CC} ${CFLAGS} -c getopt_long.c
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

%if %{with gtk}
# for backwards compatibility
ln -s pinentry-gtk-2 ${RPM_BUILD_ROOT}%{_bindir}/pinentry-gtk
%endif

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

echo "There are NO tests"


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
%{_bindir}/pinentry-tty
%{_infodir}/pinentry.info*

%if %{with gtk}
%files gtk
%defattr(-,root,system,-)
%{_bindir}/pinentry-gtk
%{_bindir}/pinentry-gtk-2
%endif



%changelog
* Sat Aug 28 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.2.0-1
- Update to 1.2.0

* Wed Jun 02 2021 Tony Reix <tony.reix@atos.net> - 1.1.1-1
- Port to AIX 6.1
- Do not build package gtk by default
- Do not deliver pinentry-curses, which does not work correctly
- Remove /usr stuff from %files
- Deliver pinentry-tty by default

* Fri Nov 17 2017 Tony Reix <tony.reix@atos.net> - 1.0.0-1
- Port to AIX 6.1

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 1.0.0-1
- updated to version 1.0.0

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 0.9.7-1
- updated to version 0.9.7

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 0.8.4-1
- updated to version 0.8.4

* Thu Sep 09 2010 Michael Perzl <michael@perzl.org> - 0.8.0-1
- first version for AIX V5.1 and higher
