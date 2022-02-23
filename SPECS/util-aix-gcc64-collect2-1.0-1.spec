# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# The collect2 built is taken for gcc version 10.3.0, based
# on BullFreeware specfile.
%define gcc_version 10.3.0

Name: util-aix-gcc64-collect2
Version: 1.0
Release: 1
Group: Development/Tools
Summary: 64bit version of collect2
License: GPL

# For now, collect2 made with gcc 7.1 seems to work
# fine in 7.2. If anything goes wrong, another RPMs
# should be made for 7.2.
Source1: collect2-%{gcc_version}-64-aix71
Source100: %{name}-%{version}-%{release}.build.log

%description
64bit-built version of collect2 taken from GCC version %{gcc_version}.
It aims to bypass a limitation of 32bit-built collect2.
To use it, add to gcc calls "-B/opt/freeware/libexec/gcc64/".

%prep
# Nothing to do.

%build
# Nothing to do.

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_libexecdir}/gcc64/
install -m755 %{SOURCE1} ${RPM_BUILD_ROOT}/%{_libexecdir}/gcc64/collect2

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Nothing to do.

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_libexecdir}/gcc64/*


%changelog
* Mon Sep 20 2021 Clement Chigot <clement.chigot@atos.net> - 1.0-1
- Initial version
