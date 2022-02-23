# This package is built for Python 2 and not valid on Python 3 before 3.4

%define name python-enum34
%define srcname enum34
%define modname enum
%define version 1.0.4
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



Name:           %{name}
Version:        %{version}
Release:        %{release}
Group:          Development/Libraries
Summary:        Backport of Python 3.4 Enum
License:        BSD

URL:            https://pypi.python.org/pypi/enum34
Source0:        https://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-devel python-setuptools

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log


%description
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.


%prep
%setup -q -n %{srcname}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

# First build the 64-bit version
cd 64bit
/opt/freeware/bin/python2.7_64 setup.py build

# Build the 32-bit version
cd ../32bit
/opt/freeware/bin/python2.7 setup.py build


%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Docs will be delivered in doc directory
rm -rf %{buildroot}%{python_sitelib}/enum/LICENSE
rm -rf %{buildroot}%{python_sitelib}/enum/README
rm -rf %{buildroot}%{python_sitelib}/enum/doc

# %check
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 enum/test_enum.py || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Docs will be delivered in doc directory
rm -rf %{buildroot}%{python_sitelib}/enum/LICENSE
rm -rf %{buildroot}%{python_sitelib}/enum/README
rm -rf %{buildroot}%{python_sitelib}/enum/doc

# Currently there are no tests
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 enum/test_enum.py || true)
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc 32bit/PKG-INFO 32bit/enum/LICENSE 32bit/enum/README 32bit/enum/doc/enum.rst
%{python_sitelib}/%{modname}
%{python_sitelib}/%{srcname}-*-py2.7.egg-info
%{python_sitelib64}/%{modname}
%{python_sitelib64}/%{srcname}-*-py2.7.egg-info


%changelog
* Fri May 12 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.0.4-1
- Initial version

