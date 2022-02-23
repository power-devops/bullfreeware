%define name python-jsonpointer
%define srcname jsonpointer
%define github_name python-json-pointer
%define commit c1ec3dfd171b242e23b3fe078a99f0e23fb0c6ea
%define version 1.0.c1ec3df
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

Summary:  Resolve JSON Pointers in Python
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{github_name}-%{version}.tar.gz
Url: https://github.com/stefankoegl/%{github_name}
License: BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildArch: noarch
BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
Requires: python >= 2.4

%description
Library to resolve JSON Pointers according to RFC 6901.

%prep
%setup -q -n %{github_name}-%{commit}

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

#%check
#python test.py

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/README.md 32bit/COPYING
%{python_sitelib}/*

%changelog
* Fri Nov 07 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.c1ec3df-1
- first version for AIX V6.1 and higher
