%bcond_without dotests

Name: renderproto
Summary: X.Org X11 Protocol renderproto
Group: Development/System
Version: 0.11.1
License: MIT
URL: http://www.x.org
Release: 2
Source0: http://xorg.freedesktop.org/releases/individual/proto/renderproto-%{version}.tar.bz2
Source100: %{name}-%{version}-%{release}.build.log

%description
Description: %{summary}
 
%prep
%setup -q -n renderproto-%{version}
 
%build
export RM="/usr/bin/rm -f"
./configure \
    --prefix=%{_prefix} \

make %{?_smp_mflags}
 
%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install
 
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}-%{version}
for f in `ls ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}`; do
    if [ -f ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/$f ]; then
        mv ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}/$f ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}-%{version}
    fi
done

%check
%if %{with dotests}
# No tests ?
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
 
%files
%defattr(-,root,system,-)
%{_libdir}/pkgconfig/renderproto.pc
%{_includedir}/X11/extensions/renderproto.h
%{_includedir}/X11/extensions/render.h
%doc %{_datadir}/doc/renderproto
 
 
%changelog
* Tue Nov 30 2021 Etienne Guesnet <etienne.guesnet@atos.net> 0.11.1-2
- Rebuild on RPMv4

* Thu Apr 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 0.11.1-1
- Update to version 0.11.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 0.9.3-4
- Initial port on Aix6.1

* Mon Sep 26 2011 Patricia Cugny <patricia.cugny@bull.net> 0.9.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Jun 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> 0.9.3
- initial import
