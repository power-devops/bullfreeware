Name: renderproto
Summary: X.Org X11 Protocol renderproto
Group: Development/System
Version: 0.11.1
License: MIT
URL: http://www.x.org
Release: 1
Source0: http://xorg.freedesktop.org/releases/individual/proto/renderproto-%{version}.tar.bz2
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

Provides: renderproto
 
%description
Description: %{summary}
 
%prep
%setup -q -n renderproto-%{version}
 
%build
export RM="/usr/bin/rm -f"
./configure \
    --prefix=%{_prefix} \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost}

make %{?_smp_mflags}
 
%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install
 
%find_lang xorg-x11-proto-renderproto || echo -n >> xorg-x11-proto-renderproto.lang
 
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}-%{version}
for f in `ls ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}`; do
    if [ -f ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/$f ]; then
        mv ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}/$f ${RPM_BUILD_ROOT}/%{_prefix}/share/doc/%{name}-%{version}
    fi
done
 
%clean
rm -rf ${RPM_BUILD_ROOT}
 
%files -f xorg-x11-proto-renderproto.lang
%defattr(-,root,system,-)
%{_prefix}/lib/pkgconfig/renderproto.pc
%{_prefix}/include/X11/extensions/renderproto.h
%{_prefix}/include/X11/extensions/render.h
%doc %{_prefix}/share/doc/renderproto
 
 
%changelog
* Thu Apr 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 0.11.1-1
- Update to version 0.11.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 0.9.3-4
- Initial port on Aix6.1

* Mon Sep 26 2011 Patricia Cugny <patricia.cugny@bull.net> 0.9.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Jun 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> 0.9.3
- initial import
