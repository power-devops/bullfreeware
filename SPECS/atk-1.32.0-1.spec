Summary: Interfaces for accessibility support
Name: 	 atk
Version: 1.32.0
Release: 1
License: LGPLv2+
Group: 	 System Environment/Libraries
Source0: http://download.gnome.org/sources/%{name}/1.32/%{name}-%{version}.tar.gz
URL: 	 http://developer.gnome.org/doc/API/2.0/gtk/gtk-building.html
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: glib2-devel >= 2.0.0
BuildRequires: gettext, pkg-config
Requires: glib2 >= 2.0.0
Requires: gettext

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.



%package devel
Summary: Files necessary to develop applications using ATK
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= 2.0.0
Requires: pkg-config

%description devel
The atk-devel package includes the static libraries, header files, and
developer docs for the atk package.

Install atk-devel if you want to develop programs which will use ATK.

%prep
%setup -q


%build
CFLAGS="-I/opt/freeware/include/"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib"  \
./configure --enable-shared --disable-static --disable-gtk-doc \
    --prefix=%{_prefix}
    
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

cd ${RPM_BUILD_ROOT}
mkdir -p usr/lib
cd usr/lib
ln -sf ../..%{_prefix}/lib/* .


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc README AUTHORS COPYING NEWS
%{_libdir}/libatk*.a
/usr/lib/libatk*.a
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-,root,system)
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_includedir}/atk-1.0/atk/*.h
%{_datadir}/gtk-doc/html/atk/*
/usr/lib/*.la


%changelog
* Mon Nov 08 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.32
- Update to version 1.32.0
