%define name python-argparse
%define srcname argparse
%define version 1.2.1
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

Summary: HTTP library, written in Python, for human beings
Name: %{name}
Version: %{version}
Release: %{release}
Source0: https://code.google.com/p/argparse/downloads/list/%{srcname}-%{version}.tar.gz
Url:     http://code.google.com/p/argparse
License: Python
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-setuptools
BuildArch:     noarch

%description

The argparse module is an optparse-inspired command line parser that
improves on optparse by:
 * handling both optional and positional arguments
 * supporting parsers that dispatch to sub-parsers
 * producing more informative usage messages
 * supporting actions that consume any number of command-line args
 * allowing types and actions to be specified with simple callables
    instead of hacking class attributes like STORE_ACTIONS or CHECK_METHODS

as well as including a number of other more minor improvements on the
optparse API.


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

#%check
#cd test
#PYTHONPATH=../ python test_argparse.py

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE.txt 32bit/NEWS.txt 32bit/README.txt 32bit/doc/*
%{python_sitelib}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.1-1
- first version for AIX V6.1 and higher
