%define name python-singledispatch
%define srcname singledispatch
%define version 3.4.0.3
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


Name:        %{name}
Version:     %{version}
Release:     %{release}
Summary:     This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3

License:     MIT
Group:       Development/Languages
URL:         https://pypi.python.org/pypi/singledispatch/
BuildArch:   noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}

Source0:     https://pypi.python.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

%description
PEP 443 proposed to expose a mechanism in the functools standard library
module in Python 3.4 that provides a simple form of generic programming 
known as single-dispatch generic functions.

Python 2 version.

This library is a backport of this functionality to Python 2.6 - 3.3.

Online documentation is at http://docs.python.org/3/library/functools.html#functools.single dispatch

Provides:       python-%{srcname} = %{version}-%{release}

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six

Requires:       python-six


# python3 packaging stuff
# %if 0%{?with_python3}
# %package -n python3-%{srcname}
# Summary:        This library brings functools.singledispatch from Python 3.4 to Python 2.6-3.3
# Provides:       python3-%{srcname} = %{version}-%{release}
# 
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# BuildRequires:  python3-six
# 
# Requires:       python3-six
# %endif

# %if 0%{?with_python3}
# %description -n python3-%{srcname}
# PEP 443 proposed to expose a mechanism in the functools standard library
# module in Python 3.4 that provides a simple form of generic programming 
# known as single-dispatch generic functions.
# 
# This library is a backport of this functionality to Python 2.6 - 3.3.
# %endif

%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"


# remove /usr/bin/env python from scripts
sed -i '1d' singledispatch.py
sed -i '1d' singledispatch_helpers.py

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build

cd 64bit

/opt/freeware/bin/python2.7_64 setup.py build

# %if 0%{?with_python3}
# %{__python3} setup.py build
# %endif


cd ../32bit

/opt/freeware/bin/python2.7 setup.py build

# %if 0%{?with_python3}
# %{__python3} setup.py build
# %endif


%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root %{buildroot}

# %if 0%{?with_python3}
# %{__python3} setup.py install --skip-build --root %{buildroot}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 setup.py test || true)
fi

# %if 0%{?with_python3}
# %{__python3} setup.py test
# %endif


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit

/opt/freeware/bin/python2.7 setup.py install --skip-build --root %{buildroot}

# %if 0%{?with_python3}
# %{__python3} setup.py install --skip-build --root %{buildroot}
# %endif

# %check
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 setup.py test || true)
fi

# %if 0%{?with_python3}
# %{__python3} setup.py test
# %endif



%files -n python-%{srcname}
%doc 32bit/README.rst
%{python_sitelib}/%{srcname}-%{version}-py?.?.egg-info
%{python_sitelib}/%{srcname}.py*
%{python_sitelib}/%{srcname}_helpers.py*
%{python_sitelib64}/%{srcname}-%{version}-py?.?.egg-info
%{python_sitelib64}/%{srcname}.py*
%{python_sitelib64}/%{srcname}_helpers.py*

# %if 0%{?with_python3}
# %files -n python3-%{srcname}
# %doc 32bit/README.rst
# %{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info
# %{python3_sitelib}/%{srcname}.py*
# %{python3_sitelib}/%{srcname}_helpers.py*
# %{python3_sitelib}/__pycache__/*
# %endif

%changelog
* Tue May 02 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.4.0.3-1
- Initial version for AIX

