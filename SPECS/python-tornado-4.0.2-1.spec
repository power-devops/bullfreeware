%define name python-tornado
%define srcname tornado
%define version 4.0.2
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

Summary: Scalable, non-blocking web server and tools
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/t//%{srcname}/%{srcname}-%{version}.tar.gz
License: ASL 2.0
URL: http://www.tornadoweb.org
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides: python2-boto = %{version}-%{release}
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-nose 
BuildRequires: python-mock
BuildRequires: python-httpretty
BuildArch:     noarch
Requires: python >= 2.4

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%package doc
Summary:        Examples for python-tornado
Group:          Documentation
Requires:       python-tornado = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.

%prep
%setup -q -n %{srcname}-%{version}
sed -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py

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
PATH=$PATH:%{buildroot}%{python_sitearch64}/%{srcname}
python_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

cd ../32bit
PATH=$PATH:%{buildroot}%{python_sitearch}/%{srcname}
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}

#%check
#PYTHONPATH=%{python_sitearch} \
#    python -m tornado.test.runtests --verbose

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/README.rst 32bit/PKG-INFO
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}-%{version}-*.egg-info
%{python_sitelib64}/%{srcname}/
%{python_sitelib64}/%{srcname}-%{version}-*.egg-info

%files doc
%doc 32bit/demos


%changelog
* Fri Nov 21 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 4.0.2-1
- First version for AIX V6.1 and higher
