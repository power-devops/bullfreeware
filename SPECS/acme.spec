%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary:	ACME the Versatile Keyboard daemon
Name:           acme
Version:        2.4.0
Release:        1

Group:          System Environment/Daemons 
License:      	GPL
URL:            http://www.hadess.net/misc-code.php3
Source:         %{name}-%{version}.tar.bz2

Patch0:		acme-2.4.0-aix.patch
Patch1:		acme-2.4.0-autotools.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Requires:	libgnomeui >= 2.0.0
Requires:	libglade2 >= 2.0.0
BuildRequires:  libgnomeui-devel >= 2.0.0
BuildRequires:  libglade2-devel >= 2.0.0
BuildRequires:	gob2

%description
ACME is a small GNOME tool to make use of the multimedia buttons present on
most laptops and internet keyboards: Volume, Brightness, Power, Eject, My Home,
Search, E-Mail, Sleep, Screensaver, Finance and Help buttons.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/acme-2.4.0-aix.patch
$PATCH -p2 -s < %{_sourcedir}/acme-2.4.0-autotools.patch


%build
./configure --prefix=%{_prefix}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# Make the links
cd %{buildroot}
for dir in bin
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%post
export GCONF_CONFIG_SOURCE=`%{_bindir}/gconftool-2 --get-default-source`
%{_bindir}/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/acme.schemas > /dev/null

%files
%defattr(644,root,system,755)
%attr(755,root,system) %{_bindir}/*
%doc AUTHORS COPYING NEWS README
%{_datadir}/acme/*
%{_datadir}/control-center-2.0/capplets/*
%{_datadir}/locale/*/LC_MESSAGES/acme.mo
%{_sysconfdir}/gconf/schemas/acme.schemas

%attr(755,root,system) /usr/bin/*
