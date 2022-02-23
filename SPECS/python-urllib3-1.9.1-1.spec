%define name python-urllib3
%define srcname urllib3
%define version 1.9.1
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

Summary: Python HTTP library with thread-safe connection pooling and file post
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/u/%{srcname}/%{srcname}-%{version}.tar.gz
Url:     http://urllib3.readthedocs.org
License: MIT
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
#BuildRequires: python-setuptools
BuildArch:     noarch

%description
Python HTTP module with connection pooling and file POST abilities.

%prep
%setup -q -n %{srcname}-%{version}
### rm -rf urllib3/packages

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
#nosetests

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES.rst 32bit/README.rst 32bit/CONTRIBUTORS.txt
%{python_sitelib}/*

%changelog
* Thu Nov 20 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.9.1-1
- first version for AIX V6.1 and higher
