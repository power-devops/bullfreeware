Summary: Utilities for manipulating .desktop files
Name: desktop-file-utils
Version: 0.20
Release: 1
URL: http://www.freedesktop.org/software/desktop-file-utils
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Tools
BuildRoot: /var/tmp/%{name}-%{version}-root

BuildRequires: glib2-devel >= 2.0.0
#BuildRequires: emacs
BuildRequires: popt

Obsoletes: desktop-file-validator

%description
.desktop files are used to describe an application for inclusion in
GNOME or KDE menus.  This package contains desktop-file-validate which
checks whether a .desktop file complies with the specification at
http://www.freedesktop.org/standards/, and desktop-file-install 
which installs a desktop file to the standard directory, optionally 
fixing it up in the process.

%prep
%setup -q

%build

./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/* .
 cd -
)

# We don't want the vfs module yet
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/libmenu*
/bin/rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gnome-vfs-2.0/modules/menu-modules.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
#%{_datadir}/emacs/site-lisp/
%{_bindir}/*
/usr/bin/*

%changelog
* Tue Sep 11 2012 Gerard Visiedo <gerard.visiedo@bull.net>  - 0.20-1
- Initial port on Aix6.1
