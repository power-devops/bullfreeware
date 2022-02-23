%define name python-backports-ssl_match_hostname
%define srcname backports.ssl_match_hostname
%define version 3.4.0.2
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

Summary: A simple, lightweight interface to Amazon Web Services
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://pypi.python.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:  %{name}-namespace.patch

License: Python
URL: https://bitbucket.org/brandon/backports.ssl_match_hostname
Group: Development/Languages
BuildRoot: %{_tmppath}/%{srcname}-%{version}-%{release}-buildroot
Provides: python2-boto = %{version}-%{release}
Prefix: %{_prefix}

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
BuildRequires: python-setuptools 
Requires: python-backports
BuildArch:     noarch

%description
The Secure Sockets layer is only actually secure if you check the hostname in
the certificate returned by the server to which you are connecting, and verify
that it matches to hostname that you are trying to reach.

But the matching logic, defined in RFC2818, can be a bit tricky to implement on
your own. So the ssl package in the Standard Library of Python 3.2 now includes
a match_hostname() function for performing this check instead of requiring
every application to implement the check separately.

This backport brings match_hostname() to users of earlier versions of Python.
The actual code inside comes verbatim from Python 3.2.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1

mv src/backports/ssl_match_hostname/README.txt ./
mv src/backports/ssl_match_hostname/LICENSE.txt ./

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
rm -f %{buildroot}%{python_sitelib}/backports/__init__.py*

cd ../32bit
python setup.py install --skip-build --root ${RPM_BUILD_ROOT}
rm -f %{buildroot}%{python_sitelib}/backports/__init__.py*

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/README.rst 32bit/LICENSE.txt 
%{python_sitelib}/backports/ssl_match_hostname
%{python_sitelib}/backports.ssl_match_hostname-%{version}-*-nspkg.pth
%{python_sitelib}/backports.ssl_match_hostname-%{version}-*.egg-info

%changelog
* Tue Nov 04 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 4.3.0.2-1
- first version for AIX V6.1 and higher
