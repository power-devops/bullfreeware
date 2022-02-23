Summary: A screen manager that supports multiple logins on one terminal
Name: screen
Version: 4.4.0
Release: 2
License: GPL2
Group: Applications/System
URL: http://www.gnu.org/software/screen
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: texinfo, info
Requires: /sbin/install-info, info

#
# The one and only true source
#
# Source0: ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
Source0: ftp://ftp.gnu.org/gnu/screen/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/screen/%{name}-%{version}.tar.gz.sig

Patch0:   %{name}-4.4.0.socket-accept.patch
Patch1:   %{name}-4.4.0.Makefile.in-GIT_DEV.patch
Patch2:   %{name}-4.4.0.loadaverage-kernelinfo.patch


%description
The screen utility allows you to have multiple logins on just one
terminal. Screen is useful for users who telnet into a machine or are
connected via a dumb terminal, but want to use more than just one
login.

Install the screen package if you need a screen manager that can
support multiple logins on one terminal.


%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
export CC=gcc

./configure \
    --prefix=%{_prefix} \
    --disable-pam \
    --enable-locale \
    --enable-telnet \
    --enable-colors256 \
    --enable-rxvt_osc \
    --with-sys-screenrc=/etc/screenrc

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

# doc is now in: /opt/freeware/share/info
%define _infodir /opt/freeware/share/info
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}/etc
cp etc/etcscreenrc ${RPM_BUILD_ROOT}/etc/screenrc
chmod 0644 ${RPM_BUILD_ROOT}/etc/*

mkdir -p ${RPM_BUILD_ROOT}/etc/skel
cp etc/screenrc ${RPM_BUILD_ROOT}/etc/skel/.screenrc
chmod 0644 ${RPM_BUILD_ROOT}/etc/skel/.screenrc

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%post
/sbin/install-info %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."

if [ -d /tmp/screens ]; then
    chmod 777 /tmp/screens
fi


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
# man is now in: /opt/freeware/share/man
%define _mandir /opt/freeware/share/man

%defattr(-,root,system)
%doc NEWS README doc/FAQ doc/README.DOTSCREEN
%attr(4755,root,system) %{_bindir}/%{name}-%{version}
%{_bindir}/screen
%{_mandir}/man1/screen.*
%{_infodir}/screen.info*
%{_datadir}/screen
%config(noreplace) /etc/screenrc
%config(noreplace) /etc/skel/.screenrc
/usr/bin/*


%changelog
* Wed Sep 21 2016 Tony Reix <tony.reix@atos.nete> - 4.4.0-2
- Group 2 patches in one and add #ifdef _AIX

* Tue Sep 20 2016 Tony Reix <tony.reix@atos.nete> - 4.4.0-1
- Initial port on AIX 6.1 and higher.
- Fix issue with /dev/kmem always opened.

* Fri Mar 14 2008 Michael Perzl <michael@perzl.org> - 4.0.3-1
- first version for AIX V5.1 and higher
