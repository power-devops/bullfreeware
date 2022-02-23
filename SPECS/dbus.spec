%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define		req_ver_glib_devel		2.2.0
%define		req_ver_qt_devel		3.1.0


Summary:	D-BUS message bus
Name:		dbus
Version:        0.94	
Release:	1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-%{version}.tar.bz2
URL:		http://dbus.freedesktop.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libxml2-devel			>= 2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-root


%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.

%package devel
Summary:	Header files for D-BUS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for D-BUS.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/dbus-0.94-aix.patch
$PATCH -p2 -s < %{_sourcedir}/dbus-0.94-autotools.patch


%build
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix}
G_CHARSET_ALIAS=%{_libdir}/charset.alias make


%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
PATH=%{_bindir}:$PATH make DESTDIR=%{buildroot} install-strip

# make links
cd %{buildroot}
for dir in bin lib include
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README doc/TODO
%{_bindir}/*
/usr/bin/*
%{_libdir}/*.a
/usr/lib/*.a
%dir %{_libdir}/dbus-*
%dir %{_sysconfdir}/dbus-1
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/dbus-1/*.conf
%dir %{_sysconfdir}/dbus-1/system.d
%dir %{_localstatedir}/run/dbus
%{_mandir}/man1/dbus*.1*

%files devel
%defattr(-,root,system)
%{_libdir}/*.la
%{_libdir}/dbus-*/include
%{_libdir}/pkgconfig/*
%{_includedir}/dbus*/dbus/*
/usr/include/*
%changelog
*  Mon Nov 20 2006  BULL
 - Release  1
 - New version  version: 0.94
 - gnome 2.16.1

*  Tue Jul 25 2006  BULL
 - Release  2

*  Fri Nov 04 2005  BULL
 - Release  1
 - New version  version: 0.50

