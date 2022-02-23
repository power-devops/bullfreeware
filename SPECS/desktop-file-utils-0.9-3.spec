%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define pkgconfig_version @pkgconfig_version@

Summary:	Utilities for manipulating .desktop files
Name:		desktop-file-utils
Version:	0.9
Release:	3
License:	GPL
Group:		Development/Tools
Source: %{name}-%{version}.tar.bz2

Patch0:		desktop-file-utils-0.9-aix.patch
Patch1:		desktop-file-utils-0.9-autotools.patch

URL: http://www.freedesktop.org/software/desktop-file-utils
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: glib2-devel >= 2.0.0
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

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/desktop-file-utils-0.9-aix.patch
$PATCH -p2 -s < %{_sourcedir}/desktop-file-utils-0.9-autotools.patch


%build

%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# We don't want the vfs module yet
#/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/libmenu*
#/bin/rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gnome-vfs-2.0/modules/menu-modules.conf

%files
%defattr(-,root,system)
%{_bindir}/*
/usr/bin/*
%{_libdir}/*
/usr/lib/*
%{_sysconfdir}/*
#%{_datadir}/emacs/site-lisp/

%changelog
*  Wed Nov 16 2005  BULL
 - Release  3
*  Wed May 25 2005  BULL
 - Release  2

*  Tue Jan 25 2005  BULL
 - Release  1
 - add new package for gnome 2.8.1
 - add new package for gnome 2.8.1
 - add new package for gnome 2.8.1

