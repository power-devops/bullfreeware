Name:          fixesproto
Version:       5.0
Release:       1
Summary:       X11 prototype headers for libXfixes
Group:         Development/Libraries
URL:           http://www.x.org
Source:        http://www.x.org/releases/X11R7.7/src/proto/%{name}-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X11 prototype headers for libXfixes.

%package devel
Summary:       Miscellaneous X11 prototype headers
Group:         Development/Libraries

%description devel
X11 prototype headers for libXfixes.


%prep
%setup -q

%build
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

#(
#  cd ${RPM_BUILD_ROOT}
#  mkdir -p usr/include/X11/extensions
#  cd usr/include/X11/extensions
#  ln -sf ../../../..%{_prefix}/include/X11/extensions/* .
#
#)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,system)
%{_includedir}/X11/extensions/xfixes*.h
#/usr/include/X11/extensions/*.h
%{_libdir}/pkgconfig/fixesproto.pc
%{_datadir}/doc/fixesproto/fixesproto.txt


%changelog
* Mon Apr 08 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 5.0-1
- Inital port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 4.1.2
- Inital port on Aix 5.3
