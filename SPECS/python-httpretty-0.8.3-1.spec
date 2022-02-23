%define name python-httpretty
%define srcname httpretty
%define version 0.8.3
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
Source0: https://pypi.python.org/packages/source/h/%{srcname}/%{srcname}-%{version}.tar.gz
Url:     http://falcao.it/HTTPretty
License: MIT
Group: UNKNOWN
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires:  python-setuptools
BuildArch:      noarch

Requires: python >= 2.4
#Requires:       python-urllib3

%description
Once upon a time a python developer wanted to use a RESTful API, everything was
fine but until the day he needed to test the code that hits the RESTful API:
what if the API server is down? What if its content has changed?

Don't worry, HTTPretty is here for you.

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
python_64 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/README.md 32bit/PKG-INFO 32bit/README.rst 32bit/COPYING
%{python_sitelib}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 0.8.3-1
- first version for AIX V6.1 and higher
