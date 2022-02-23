%bcond_without dotests

Summary: pkg-config files for AIX X11 libraries
Name: aix-x11-pc
Version: 1.0
Release: 2
License: GNU GPL
Url: 	 http://www.bullfreeware.com
Source0: x11.pc
Source1: xau.pc
Source2: xext.pc
Group:   Development/Libraries

Source100: %{name}-%{version}-%{release}.build.log

Conflicts: libX11-devel
Conflicts: libXau-devel
Conflicts: libXext-devel

%description 
This package containes pkg-config definitions for some of the X11 libraries
shipped with AIX : libX11, libXau and libXext.

%pre
if ! (lslpp -w /usr/lib/libX11.a > /dev/null); then
    echo "X11.base.lib LPP fileset must be installed first."
fi
if ! (lslpp -w /usr/lib/libXau.a > /dev/null); then
    echo "X11.adt.lib LPP fileset must be installed first."
fi


%check
%if %{with dotests}
# No test.
%endif


%install
mkdir -p ${RPM_BUILD_ROOT}/opt/freeware/lib/pkgconfig
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} ${RPM_BUILD_ROOT}/opt/freeware/lib/pkgconfig/

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Nov 30 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 1.0-2
- Rebuild on RPMv4

* Thu Jul 07 2016 Matthieu Sarter <matthieu.sarter@atos.net> - 1.0-1
- first release
