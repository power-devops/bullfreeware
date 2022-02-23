# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name: util-aix-ld
Version: 1.0
Release: 1
Group: Development/Tools
Summary: Utilities made to workaround some behaviors of AIX linker
License: Public Domain

Source0: %{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

# Make sure OpenSource version are here.
Requires: grep gawk sed

%description
Utilities made to workaround some behaviors of AIX linker.

%prep
%setup -q

%build
# Nothing to do.

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
install -m755 scripts/* ${RPM_BUILD_ROOT}/%{_bindir}

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd testsuite
make check


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_bindir}/*


%changelog
* Tue Aug 24 2021 Clement Chigot <clement.chigot@atos.net> - 1.0-1
- Initial version
