%define name python-packaging
%define pypi_name packaging
%define version 16.8
%define release 1

%global pypi_name packaging

# %global build_wheel 1
# %global with_python3 1

# %global python2_wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl
# %global python3_wheelname %python2_wheelname

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
Summary:        Core utilities for Python packages

Group:          Development/Libraries
License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:      %{_prefix}


BuildRequires:  python-setuptools
BuildRequires:  python-devel
BuildRequires:  python-pytest
BuildRequires:  python-pyparsing
BuildRequires:  python-sphinx

# BuildRequires:  python-pretend
BuildRequires:  python-six

# Build Python 3 subpackage only for Fedora
# %if 0%{?with_python3}
# BuildRequires:  python%{python3_pkgversion}-setuptools
# BuildRequires:  python%{python3_pkgversion}-devel
# BuildRequires:  python%{python3_pkgversion}-pytest
# BuildRequires:  python%{python3_pkgversion}-pretend
# BuildRequires:  python%{python3_pkgversion}-pyparsing
# BuildRequires:  python%{python3_pkgversion}-six
# BuildRequires:  python%{python3_pkgversion}-sphinx
# %endif

# %if 0%{?build_wheel}
# BuildRequires:  python2-pip
# BuildRequires:  python-wheel
# %if 0%{?with_python3}
# BuildRequires:  python%{python3_pkgversion}-pip
# BuildRequires:  python%{python3_pkgversion}-wheel
# %endif
# %endif


%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-pyparsing
Requires:       python-six

%description -n python-%{pypi_name}
A Python 2 package providing core utilities for Python packages like utilities
for dealing with versions, specifiers, markers etc.


# A python3 build/install is not yet supported

# %if 0%{?with_python3}
# %package -n python%{python3_pkgversion}-%{pypi_name}
# Summary:        %{summary}
# Group:          Development/Libraries
# %{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
#  
# Requires:       python%{python3_pkgversion}-pyparsing
# Requires:       python%{python3_pkgversion}-six
# %description -n python%{python3_pkgversion}-%{pypi_name}
# python3-packaging provides core utilities for Python packages like utilities for
# dealing with versions, specifiers, markers etc.
# %endif


%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
Group:          Documentation

%description -n python-%{pypi_name}-doc
Documentation for python-packaging


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * .coveragerc
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

cd 64bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7_64  setup.py build
# %endif

# %if 0%{?with_python3}
# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6_64  setup.py build
# %endif
# %endif

cd ../32bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7  setup.py build
# %endif

# %if 0%{?with_python3}
# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6  setup.py build
# %endif
# %endif


# generate html docs
# %if 0%{?with_python3}
# sphinx-build-3 docs html
# %else
sphinx-build docs html
# %endif

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/



%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
 ( /opt/freeware/bin/python2.7_64  -m pytest tests/ || true)
fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


# %if 0%{?with_python3}
# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif
# %endif


cd ../32bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
 ( /opt/freeware/bin/python2.7  -m pytest tests/ || true)
fi


# %if 0%{?with_python3}
# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif
# %endif


# %check
# %if 0%{?fedora}
# %{__python2} -m pytest tests/
# %{__python3} -m pytest tests/
# %else
# # Disable non-working tests in Epel7
# %{__python2} -m pytest --ignore=tests/test_requirements.py tests/
# %endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{pypi_name}
%doc 32bit/LICENSE 32bit/LICENSE.APACHE 32bit/LICENSE.BSD
%doc 32bit/README.rst 32bit/CHANGELOG.rst 32bit/CONTRIBUTING.rst
%{python_sitelib}/%{pypi_name}/
%{python_sitelib}/%{pypi_name}-*-info/
%{python_sitelib64}/%{pypi_name}/
%{python_sitelib64}/%{pypi_name}-*-info/

# %if 0%{?with_python3}
# %files -n python%{python3_pkgversion}-%{pypi_name}
# %license 32bit/LICENSE 32bit/LICENSE.APACHE 32bit/LICENSE.BSD
# %doc 32bit/README.rst 32bit/CHANGELOG.rst 32bit/CONTRIBUTING.rst
# %{python3_sitelib}/%{pypi_name}/
# %{python3_sitelib}/%{pypi_name}-*-info/
# %{python3_sitelib64}/%{pypi_name}/
# %{python3_sitelib64}/%{pypi_name}-*-info/
# %endif

%files -n python-%{pypi_name}-doc
%doc 32bit/html
%doc 32bit/LICENSE 32bit/LICENSE.APACHE 32bit/LICENSE.BSD

%changelog
* Tue Jan 16 2018 Michael Wilson <michael.a.wilson@atos.net> - 16.8-1
- Initial version for AIX

