%define name python-pyserial
%define srcname pyserial
%define version 2.7
%define release 1

%define is_python %(test -e /usr/bin/python && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /usr/bin/python_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Summary: Python serial port access library
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{srcname}-%{version}.tar.gz
Url:     https://pypi.python.org/pypi/pyserial
License: Python
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4

Requires: python >= 2.4

%description
This module encapsulates the access for the serial port. It provides backends
for standard Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automaticaly selects
the appropriate backend.

%prep
%setup -q -n %{srcname}-%{version}

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
cd 64bit
export OBJECT_MODE=64
python_64 setup.py build

cd ../32bit
export OBJECT_MODE=32
python setup.py build

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
/usr/bin/*
%{_bindir}/*
%doc 32bit/LICENSE.txt 32bit/CHANGES.txt 32bit/README.txt 32bit/examples
%{python_sitelib}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.7-1
- first version for AIX V6.1 and higher
