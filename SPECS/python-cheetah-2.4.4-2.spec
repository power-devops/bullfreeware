%define name python-cheetah
%define srcname Cheetah
%define version 2.4.4
%define release 2

%define is_python %(test -e /usr/bin/python && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /usr/bin/python_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Summary: Template engine and code generator
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/C/Cheetah/%{srcname}-%{version}.tar.gz
Patch0:  cheetah-2.4.4-dont-run-tests-twice.patch
Patch1:  cheetah-optional-deps.patch
Url: http://cheetahtemplate.org
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
Requires: python >= 2.4

%description
Cheetah is an open source template engine and code generation tool,
written in Python. It can be used standalone or combined with other
tools and frameworks. Web development is its principal use, but
Cheetah is very flexible and is also being used to generate C++ code,
Java, SQL, form emails and even Python code.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1

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

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

#%check
#export PATH="%{buildroot}/%{_bindir}:$PATH"
#export PYTHONPATH="%{buildroot}/%{python_sitelib}"
#%{buildroot}/%{_bindir}/cheetah test

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/README.markdown 32bit/LICENSE 32bit/PKG-INFO 32bit/TODO
/usr/bin/*
%{_bindir}/*
%{python_sitelib}/*
%{python_sitelib64}/*

%changelog
* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.4-1
- Add some patches

* Thu Jun 25 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 2.4.4-1
- first version for AIX V6.1 and higher
