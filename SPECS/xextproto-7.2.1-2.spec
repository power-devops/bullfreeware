Name:          xextproto
Version:       7.2.1
Release:       1
Summary:       X11 prototype headers for libXext
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.6/src/proto/%{name}-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X11 prototype headers for libXext.

%package devel
Summary:       X11 prototype headers for libXext
Group:         Development/Libraries

%description devel
X11 prototype headers for libXext

%prep
%setup -q

%build
CC="/usr/vac/bin/xlc"
./configure --prefix=%{_prefix}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/include/X11/extensions
  cd usr/include/X11/extensions
  ln -sf ../../../..%{_prefix}/include/X11/extensions/* .
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%{_includedir}/X11/extensions/*.h
%{_libdir}/pkgconfig/xextproto.pc
%dir %{_datadir}/doc/xextproto
%{_datadir}/doc/xextproto/*


%changelog
* Tue Feb 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.2.1-1
- Update to version 7.2.1

* Tue Feb 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.1.2-2
- Inital port on Aix 6.1

