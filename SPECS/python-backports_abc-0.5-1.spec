%define name python-backports_abc
%define srcname backports_abc
%define version 0.5
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

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A backport of recent additions to the collections.abc module

Group:          Development/Languages
License:        Python
URL:            https://pypi.python.org/pypi/backports_abc
Source0:        https://files.pythonhosted.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
# BuildRequires:  python-devel python%{python3_pkgversion}-devel
BuildRequires:  python-setuptools
# BuildRequires:  python-setuptools python%{python3_pkgversion}-setuptools

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log


%description
A backport of recent additions to the collections.abc module.


# %package -n python%{python3_pkgversion}-%{srcname}
# Summary:        A backport of recent additions to the collections.abc module
# %{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
# 
# %description -n python%{python3_pkgversion}-%{srcname}
# A backport of recent additions to the collections.abc module.


%prep
%setup -n %{srcname}-%{version}

echo "dotests=%{dotests}"

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build

# %py2_build
# %py3_build

# First build the 64-bit version
cd 64bit
/opt/freeware/bin/python2.7_64 setup.py build

# Build the 32-bit version
cd ../32bit
/opt/freeware/bin/python2.7 setup.py build


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# %py2_install
# %py3_install

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 tests.py || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 tests.py || true)
fi



# A python3 build/install is not yet supported
# and RPM 3.0.5 does not accept %check
# %check
# %{__python2} setup.py test
# %{__python3} setup.py test


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-backports_abc
# %license LICENSE
%doc 32bit/LICENSE 32bit/CHANGES.rst 32bit/README.rst
%{python_sitelib}/*
%{python_sitelib64}/*

# %files -n python%{python3_pkgversion}-%{srcname}
# %license LICENSE
# %doc CHANGES.rst README.rst
# %{python3_sitelib}/%{srcname}.py
# %{python3_sitelib}/%{srcname}*.egg-info/
# %{python3_sitelib}/__pycache__/*


%changelog
* Thu Apr 20 2017 Michael Wilson <michael.a.wilson@atos.net> - 0.5-1
- Initial version

