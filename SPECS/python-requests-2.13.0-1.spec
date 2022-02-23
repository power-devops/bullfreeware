%define name python-requests
%define srcname requests
%define version 2.13.0
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}


# Needs care because default command python may be linked to 32 or 64 bit python
# and compiler/loader options are not the same, e.g. -maix32/-maix64
# Also, although
#     /usr/bin/python_64 eventually links to /opt/freeware/bin/python2.7_64
#     /usr/bin/python_32 links to inexistant /opt/freeware/bin/python2_32
# So, use /opt/freeware/bin/python2.7 and /opt/freeware/bin/python2.7_64

%define is_python %(test -e /opt/freeware/bin/python2.7 && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(/opt/freeware/bin/python2.7 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /opt/freeware/bin/python2.7_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(/opt/freeware/bin/python2.7_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif


%global with_python3 0


%global urllib3_unbundled_version 1.20

Name:        %{name}
Version:     %{version}
Release:     %{release}
Summary:     HTTP library, written in Python, for human beings

License:     ASL 2.0
Group:       Development/Libraries
URL:         https://pypi.python.org/pypi/requests
Source0:     https://github.com/kennethreitz/requests/archive/v%{version}/requests-v%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}


# This patch requires an AIX adaptation when ca-certificates RPM is modified

# Use the system CA certificates supplied by package ca-certificates.
Patch0:         python-requests-2.13.0-remove-bundle-cert.patch

# Tell setuptools about what version of urllib3 we're unbundling
# - https://github.com/kennethreitz/requests/issues/2816
# Patch2:         python-requests-urllib3-at-%{urllib3_unbundled_version}.patch

# Use 127.0.0.1 not localhost for socket.bind() in the Server test
# class, to fix tests in Koji's no-network environment
# This probably isn't really upstreamable, because I guess localhost
# could technically be IPv6 or something, and our no-network env is
# a pretty odd one so this is a niche requirement.
# Patch3:         requests-2.12.4-tests_nonet.patch

BuildArch:      noarch

%description
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

Provides:       python-%{srcname} = %{version}-%{release}

BuildRequires:  python-devel
# BuildRequires:  python-chardet
# BuildRequires:  python-urllib3 == %{urllib3_unbundled_version}
# For tests
BuildRequires:  python-pytest
BuildRequires:  python-pytest-cov
BuildRequires:  python-pytest-httpbin
BuildRequires:  python-pytest-mock


Requires:       ca-certificates
# Requires:       python-chardet
# Requires:       python-urllib3 == %{urllib3_unbundled_version}

# RFC 5891 version of the protocol is often referred to as "IDNA2008"
# and can produce different results from the earlier RFC 3490 2003 standard.
# The python-idna library is a suitable replacement for the
# encodings.idna module included in the Python standard library, but
# which currently only supports the older 2003 specification
# See module python2.7/encodings/idna.py
# Requires:       python-idna


# %if 0%{?_with_python3}
# %package -n python3-requests
# Summary: HTTP library, written in Python, for human beings
# 
# Provides:       python3-%{srcname} = %{version}-%{release}
# 
# BuildRequires:  python3-devel
# BuildRequires:  python3-chardet
# BuildRequires:  python3-urllib3 == %{urllib3_unbundled_version}
# # For tests
# BuildRequires:  python3-pytest
# BuildRequires:  python3-pytest-cov
# BuildRequires:  python3-pytest-httpbin
# BuildRequires:  python3-pytest-mock
# 
# Requires:       python3-chardet
# Requires:       python3-urllib3 == %{urllib3_unbundled_version}
# Requires:       python3-idna
# 
# %description -n python3-requests
# Most existing Python modules for sending HTTP requests are extremely verbose and
# cumbersome. Python’s built-in urllib2 module provides most of the HTTP
# capabilities you should need, but the API is thoroughly broken. This library is
# designed to make HTTP requests easy for developers.
# %endif

%prep
%setup -q -n requests-%{version}

echo "dotests=%{dotests}"

%patch0 -p1
# %patch1 -p1
# %patch2 -p1
# %patch3 -p1

# Continue to bundle CA certificates until the ca-certificates RPM is completed
# Remove the included certificate bundle
rm -rf requests/cacert.pem

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * ./.[cgt]*
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# %if 0%{?_with_python3}
# rm -rf %{py3dir}
# cp -a . %{py3dir}
# %endif # with_python3


# A python3 build/install is not yet supported

# Fedora unbundles chardet and urllib3, but previous Bull version does not
# Continue to bundle them until proof that separate RPMs are required

%build

cd 64bit
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64  setup.py build

cd ../32bit
export OBJECT_MODE=32
/opt/freeware/bin/python2.7  setup.py build


# %if 0%{?_with_python3}
# %{__python3} setup.py build
# 
# Unbundle chardet and urllib3.  We replace these with symlinks to system libs.
# rm -rf build/lib/requests/packages/chardet
# rm -rf build/lib/requests/packages/urllib3
# rm -rf build/lib/requests/packages/idna
# 
# %endif
# 
# %{__python} setup.py build
# 
# Unbundle chardet and urllib3.  We replace these with symlinks to system libs.
# rm -rf build/lib/requests/packages/chardet
# rm -rf build/lib/requests/packages/urllib3
# rm -rf build/lib/requests/packages/idna


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Continue to bundle chardet and urllib3
# ln -s ../../chardet %{buildroot}/%{python_sitelib}/requests/packages/chardet
# ln -s ../../urllib3 %{buildroot}/%{python_sitelib}/requests/packages/urllib3
# ln -s ../../idna %{buildroot}/%{python_sitelib}/requests/packages/idna

# %check
if [ "%{dotests}" == 1 ]
then
  (PYTHONPATH=%{buildroot}/%{python_sitelib} py.test || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Continue to bundle chardet and urllib3
# ln -s ../../chardet %{buildroot}/%{python_sitelib}/requests/packages/chardet
# ln -s ../../urllib3 %{buildroot}/%{python_sitelib}/requests/packages/urllib3
# ln -s ../../idna %{buildroot}/%{python_sitelib}/requests/packages/idna

# %check
if [ "%{dotests}" == 1 ]
then
  (PYTHONPATH=%{buildroot}/%{python_sitelib} py.test || true)
fi


# %if 0%{?_with_python3}
# pushd %{py3dir}
# %{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
# ln -s ../../chardet %{buildroot}/%{python3_sitelib}/requests/packages/chardet
# ln -s ../../urllib3 %{buildroot}/%{python3_sitelib}/requests/packages/urllib3
# ln -s ../../idna %{buildroot}/%{python3_sitelib}/requests/packages/idna
# popd
# %endif


# %check
# 
# PYTHONPATH=./ py.test
# %if 0%{?_with_python3}
# pushd %{py3dir}
# PYTHONPATH=./ py.test-%{python3_pkgversion}
# popd
# %endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-requests
%defattr(-,root,system,-)
%{!?_licensedir:%global license %%doc}
%license 32bit/LICENSE
# %doc 32bit/LICENSE
%doc 32bit/NOTICE 32bit/README.rst 32bit/HISTORY.rst
%{python_sitelib}/*.egg-info
%dir %{python_sitelib}/requests
%{python_sitelib}/requests/*
%{python_sitelib64}/*.egg-info
%dir %{python_sitelib64}/requests
%{python_sitelib64}/requests/*

# %if 0%{?_with_python3}
# %files -n python%{python3_pkgversion}-requests
# %{!?_licensedir:%global license %%doc}
# %license LICENSE
# %doc NOTICE README.rst HISTORY.rst
# %{python3_sitelib}/*.egg-info
# %{python3_sitelib}/requests/
# %endif

%changelog
* Wed May 02 2017 Michael Wilson <michael.a.wilson@atos.net> - 2.13.0-1
- Update to version 2.13.0

* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.3-1
- first version for AIX V6.1 and higher

