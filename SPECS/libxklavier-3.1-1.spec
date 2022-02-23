%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Name: 		libxklavier
Version: 	3.1
Release: 	1
Group: 		Development/Libraries
Summary: 	libXklavier library
License: 	LGPL
URL: 		http://gswitchit.sourceforge.net/
BuildRequires: doxygen
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Source:         http:///%{name}-%{version}.tar.bz2

Patch0:		libxklavier-3.1-aix.patch
Patch1:		libxklavier-3.1-autotools.patch


%description
This library allows you simplify XKB-related development.

%package devel
Summary: Libraries, includes, etc to develop libxklavier applications
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Libraries, include files, etc you can use to develop libxklavier applications.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/libxklavier-3.1-aix.patch
$PATCH -p2 -s < %{_sourcedir}/libxklavier-3.1-autotools.patch


%build
./configure --prefix=%{_prefix}
make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
%{_make} INSTALL_PATH=%{buildroot}%{_prefix} install-dtd
PATH=%{_bindir}:$PATH DATADIR=%{buildroot}%{_datadir}/xml/ \
SYSCONFDIR=%{buildroot}%{_sysconfdir}/xml/ ./buildDocBookCatalog

# Make the links
cd %{buildroot}
for dir in bin lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr (-,root,system)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB 
%{_libdir}/lib*.a
/usr/lib/lib*.a
%{_datadir}/libxklavier
/usr/share/*

%files devel
%defattr (-,root,system)
%doc doc/html/*.html doc/html/*.png doc/html/*.css
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*a
%{_includedir}/*
/usr/include/*
%changelog
*  Wed Nov 22 2006  BULL
 - Release  1
 - New version  version: 3.1
 - gnome 2.16.1

*  Thu Jul 20 2006  BULL
 - Release  6
 - built with ORBit 2.14

*  Thu Jul 10 2006  BULL
 - Release  5
 - New version  version: 2.2

*  Tue Feb 07 2006  BULL
 - Release  5
 - fix: undef X11 symbols

*  Wed Nov 16 2005  BULL
 - Release  4
*  Wed Aug 10 2005  BULL
 - Release  3
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 2.0

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 1.04

