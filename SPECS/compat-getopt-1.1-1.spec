%bcond_without dotests

Name:           compat-getopt
Version:        1.1
Release:        1
Summary:        Provide getopt_long() from glibc and getopt() from AIX.
License:        BSD
Group:          Development/Libraries/C and C++
Source0:        %{name}-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64


%description
It provides the getopt() and getopt_long() routine.

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Headers of getopt().
Requires:       %{name}

%description devel
It provides the getopt() and getopt_long() routine.

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
* Fri Oct 23 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 1.1-1
- Add "extern C" for C++

* Fri Mar 27 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0-2
- Add require for -devel to base.

* Thu Jan 09 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.0-1
- First version from getopt_long
