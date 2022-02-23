Name:          xproto
Version:       7.0.20
Release:       3
Summary:       The X.org xproto header
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.6/src/proto/%{name}-%{version}.tar.gz
License:       MIT
Provides:      xorg-proto
Obsoletes:     xorg-proto

BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
The X.org xproto header

%package devel
Summary:       The X.org xproto header
Group:         Development/Libraries

%description devel
The X.org xproto header

%prep
%setup -q

%build
export RM="/usr/bin/rm -f"
./configure --prefix=%{_prefix}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/include/X11
  cd usr/include/X11
  ln -sf ../../..%{_prefix}/include/X11/* .

)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%{_includedir}/X11/*.h
/usr/include/X11/*.h
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/doc/
%{_datadir}/doc/*/*


%changelog
* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-3
- Initial port on Aix6.1

* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 7.0.20
- Inital port on Aix 5.3

