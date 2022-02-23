%define name python-yaml
%define srcname PyYAML
%define version 3.11
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

Summary: Python package implementing YAML parser and emitter
Name: %{name}
Version: %{version}
Release: %{release}
Source0:  http://pyyaml.org/download/pyyaml/%{srcname}-%{version}.tar.gz
Url: http://pyyaml.org/wiki/PyYAML
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-setuptools
BuildRequires: libyaml-devel

Provides:       python-yaml = %{version}-%{release}


%description
PyYAML is a YAML parser and emitter for the Python programming language.

YAML is a data serialization format designed for human readability
and interaction with scripting languages.

%prep
%setup -q -n %{srcname}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
cd 64bit
export OBJECT_MODE=64
python_64 setup.py --with-libyaml build_ext

cd ../32bit
export OBJECT_MODE=32
python setup.py --with-libyaml build_ext

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
python_64 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
python setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

#%check
#python setup.py test

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/CHANGES 32bit/PKG-INFO  32bit/README  32bit/examples 
%{python_sitelib}/*
%{python_sitelib64}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 3.11-1
- first version for AIX V6.1 and higher
