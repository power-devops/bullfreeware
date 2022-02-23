%define _prefix /opt/freeware


Summary:	D-Bus GLib Bindings
Name:		dbus-glib
Version:        0.71	
Release:	1
License:	AFL v2.0 or GPL v2
Group:		Libraries
Source0:	http://dbus.freedesktop.org/releases/dbus-glib-%{version}.tar.bz2
URL:		http://dbus.freedesktop.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libxml2-devel			>= 2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-root


%description
D-Bus GLib Bindings

%package devel
Summary:	D-Bus GLib Bindings for devel
Group:		Development/Libraries

%description devel
GLib Bindings for devel

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/dbus-glib-0.71-aix.patch
$PATCH -p2 -s < %{_sourcedir}/dbus-glib-0.71-autotools.patch


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
for dir in bin lib
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%{_bindir}/*
/usr/bin/*
%{_libdir}/*.a
/usr/lib/*.a

%files devel
%defattr(-,root,system)
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%changelog
*  Mon Nov 20 2006  BULL
 - Release  1
 - gnome 2.16.1

