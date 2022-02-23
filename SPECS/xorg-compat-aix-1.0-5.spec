Summary: X.Org X11 AIX compatibility layer
Name: xorg-compat-aix
Version: 1.0
Release: 5
License: MIT/X11
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

Source0: x11.pc
Source1: xproto.pc
Source2: xext.pc
Source3: xextproto.pc
Source4: randrproto.pc
Source5: fixesproto.pc
#Source6: xfixes.pc surtout ne pas le mettre avec gtk2
Source7: glproto.pc
%ifos aix6.1
Source8: xrender.pc
%endif
Source9: renderproto.pc

BuildRequires: pkg-config
Requires: pkg-config

%description
This RPM package provides a pkg-config compatibility layer for X11 on AIX.


%prep


%build
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig

cp %{SOURCE0} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
#cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
%ifos aix6.1
cp %{SOURCE8} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig
%endif
cp %{SOURCE9} ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig

chmod 0644 ${RPM_BUILD_ROOT}%{_prefix}/lib/pkgconfig/*


%install


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_prefix}/lib/pkgconfig/*.pc


%changelog
* Thu Mar 15 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.0-5
- Xrender rpm is necessary for Aix5.1

* Fri Mar 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.0-4
- Introduce somes .pc files.  Note that xfixes.pc must not be installed

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.0-3
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 1.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.0-1
- Port on platform Aix5.3
