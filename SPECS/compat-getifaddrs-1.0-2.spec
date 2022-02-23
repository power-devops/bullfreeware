%bcond_without dotests

# TODO know bugs
# If you have multiple IP adress on the same interface,
# only the first IPv4 and the first IPv6 will be found.

Name:           compat-getifaddrs
Version:        1.0
Release:        2
Summary:        Provide getifaddrs().
License:        LGPLv3+
Group:          Development/Libraries/C and C++
Source0:        %{name}-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64


%description
It provides the getifaddrs() routine.

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Headers of getifaddrs().
Requires:       %{name}

%description devel
It provides the getifaddrs() routine.

This package contains headers.


%prep
%setup -q


%build

gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir64}
mkdir -p ${RPM_BUILD_ROOT}/%{_includedir}

cp lib%{name}.a ${RPM_BUILD_ROOT}/%{_libdir}
(
  cd ${RPM_BUILD_ROOT}/%{_libdir64}
  ln -s ../lib/lib%{name}.a .
)
cp *.h ${RPM_BUILD_ROOT}/%{_includedir}


%check
%if %{with dotests}
# You must compare results manually...
gmake check
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir64}/*.a

%files devel
%defattr(-,root,system)
%{_includedir}/*.h


%changelog
* Wed Jul 08 2020 �~Itienne Guesnet <etienne.guesnet.external@atos.net> - 1-2
- Mistakes in licence

* Mon Mar 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0-1
- First version of getifaddrs
