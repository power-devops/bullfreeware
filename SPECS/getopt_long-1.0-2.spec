Name:           getopt_long
Version:        1.0
Release:        2
Summary:        Provide getopt_long()) from glibc
License:        Artistic or GPL
Group:          Development/Libraries/C and C++
Source0:        %{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%define _libdir64 %{_prefix}/lib64


%description
It provides the getopt_long() routine like the Linux glibc does.

The library is available as 32-bit and 64-bit.


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
cp %{name}.h ${RPM_BUILD_ROOT}/%{_includedir}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/*.a
%{_libdir64}/*.a
%{_includedir}/*.h


%changelog
* Thu May 23 2019 Tony Reix <tony.reix@atos.net> - 1.0-2
- Fix ../lib... symlink

* Tue Sep 04 2018 Tony Reix <tony.reix@atos.net> - 1.0-1
- First version

* Tue Sep 04 2018 Tony Reix <tony.reix@atos.net> - 1.0-1
- First version

* Tue Sep 04 2018 Tony Reix <tony.reix@atos.net> - 1.0-1
- First version

