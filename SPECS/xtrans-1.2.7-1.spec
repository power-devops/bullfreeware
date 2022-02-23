Name:          xtrans
Version:       1.2.7
Release:       1
Summary:       X protocol translation tools for X.Org
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.7/src/proto/%{name}-%{version}.tar.bz2
License:       MIT
Provides:      xorg-xtrans
Obsoletes:     xorg-xtrans
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X protocol translation tools for X.Org

%package devel
Summary:       X protocol translation tools for X.Org
Group:         Development/Libraries
Provides:      xorg-xtrans-devel
Obsoletes:     xorg-xtrans-devel

%description devel
X protocol translation tools for X.Org

This package contains static libraries and header files need for development.


%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig
mv ${RPM_BUILD_ROOT}/%{_datadir}/pkgconfig/xtrans.pc ${RPM_BUILD_ROOT}/%{_libdir}/pkgconfig
(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%dir %{_includedir}/X11/Xtrans
%{_includedir}/X11/Xtrans/*.c
%{_includedir}/X11/Xtrans/*.h
%{_libdir}/pkgconfig/xtrans.pc
%{_datadir}/aclocal/xtrans.m4
%dir %{_datadir}/doc/xtrans
%{_datadir}/doc/xtrans/xtrans.*
%doc AUTHORS COPYING ChangeLog README


%changelog
* Fri Apr 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.7-1
- Initial port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.6
- Inital port on Aix 5.3

