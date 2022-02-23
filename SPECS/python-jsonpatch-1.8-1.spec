%define name python-jsonpatch
%define srcname jsonpatch
%define version 1.8
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

Summary: Applying JSON Patches in Python
Name: %{name}
Version: %{version}
Release: %{release}
Source0: https://pypi.python.org/packages/source/j/%{srcname}/%{srcname}-%{version}.tar.gz
Url: https://github.com/stefankoegl/python-json-patch
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildArch:     noarch
BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires:  python-setuptools
BuildRequires:  python-jsonpointer
Requires:       python-jsonpointer
Requires: python >= 2.4

%description
Library to apply JSON Patches according to RFC 6902 - Python 2 build

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

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/PKG-INFO 32bit/README.md
%{python_sitelib}/*
#### %{python_sitelib64}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.8-1
- first version for AIX V6.1 and higher
