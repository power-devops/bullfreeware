Name:          inputproto
Epoch:         1
Version:       2.2
Release:       1
Summary:       X11 prototype headers for input devices
Group:         Development/Libraries
URL:           http://www.x.org
Source:        ftp://ftp.x.org/pub/individual/proto/inputproto-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
X11 prototype headers for input devices.

%package devel
Summary:       X11 prototype headers for input devices
Group:         Development/Libraries

%description devel
X11 prototype headers for input devices.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

#(
#  cd ${RPM_BUILD_ROOT}
#  mkdir -p usr/include/X11/extensions
#  cd usr/include/X11/extensions
#  ln -sf ../../../..%{_prefix}/include/X11/extensions/* .
#)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files devel
%defattr(-,root,system)
%doc ChangeLog COPYING INSTALL README
%{_includedir}/X11/extensions/*.h
#/usr/include/X11/extensions/*.h
%{_libdir}/pkgconfig/inputproto.pc
#%dir %{_datadir}/doc/inputproto
#%{_datadir}/doc/inputproto/*.txt

%changelog
* Mon Apr 08 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.2-1
- Initial port on Aix6.1

* Fri Sep 02 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.0.1-1
- Initial port on Aix5.3

