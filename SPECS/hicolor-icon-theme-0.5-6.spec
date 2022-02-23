%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Name: 		hicolor-icon-theme
Version: 	0.5
Release: 	6
Group: 		System Environment/Libraries
Summary: 	The hicolor icon theme
License: 	GPL
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Source:         %{name}-%{version}.tar.bz2

Patch0:		hicolor-icon-theme-0.5-aix.patch
Patch1:		hicolor-icon-theme-0.5-autotools.patch


%description

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/hicolor-icon-theme-0.5-aix.patch
$PATCH -p2 -s < %{_sourcedir}/hicolor-icon-theme-0.5-autotools.patch


%build

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
%{_datadir}/icons/hicolor
/usr/share/*
%changelog
*  Tue Nov 21 2006  BULL
 - Release  6
 - gnome 2.16.1

*  Thu Nov 17 2005  BULL
 - Release  5
*  Wed Aug 10 2005  BULL
 - Release  4
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Wed May 25 2005  BULL
 - Release  3

*  Tue Nov 24 2004  BULL
 - Release  2
