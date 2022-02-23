%define name python-appdirs
%define modname appdirs
%define version 1.4.3
%define release 1

%global modname appdirs
# %global build_wheel 1
# 
# %global python2_wheelname %{modname}-%{version}-py2.py3-none-any.whl
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


Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       Python 2 module for determining platform-specific directories

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/ActiveState/appdirs
Source0:       https://files.pythonhosted.org/packages/source/a/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:      %{_prefix}

%{?python_provide:%python_provide python-%{modname}}
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# %if 0%{?build_wheel}
# BuildRequires:  python-pip
# BuildRequires:  python-wheel
# %endif

%description -n python-%{modname}
A small Python 2 module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".


# A python3 build/install is not yet supported

# %package -n python3-%{modname}
# Summary:       Python 3 module for determining platform-specific directoriess
# %{?python_provide:%python_provide python3-%{modname}}
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# %if 0%{?build_wheel}
# BuildRequires:  python3-pip
# BuildRequires:  python3-wheel
# %endif
# 
# %description -n python3-%{modname}
# A small Python 3 module for determining appropriate " + " platform-specific
# directories, e.g. a "user data dir".


%prep
%setup -q -n %{modname}-%{version}
rm -rf %{modname}.egg-info

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

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6_64  setup.py build
# %endif

cd ../32bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7  setup.py build
# %endif

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# /opt/freeware/bin/python3.6  setup.py build
# %endif



%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python_sitelib}/%{modname}.py

# %check
if [ "%{dotests}" == 1 ]
then
 /opt/freeware/bin/python2.7_64  setup.py test
fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif
# 
# sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python3_sitelib}/%{modname}.py


cd ../32bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif

sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python_sitelib}/%{modname}.py

# %check
if [ "%{dotests}" == 1 ]
then
 /opt/freeware/bin/python2.7  setup.py test
fi


# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# /opt/freeware/bin/python3.6 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif
# 
# sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python3_sitelib}/%{modname}.py




# %check
# %{__python2} setup.py test
# %{__python3} setup.py test


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{modname}
%doc 32bit/LICENSE.txt
%doc 32bit/README.rst 32bit/CHANGES.rst
%{python_sitelib}/%{modname}*
%{python_sitelib64}/%{modname}*

# %files -n python3-%{modname}
# %doc 32bit/LICENSE.txt
# %doc 32bit/README.rst 32bit/CHANGES.rst
# %{python3_sitelib}/%{modname}*
# %{python3_sitelib}/__pycache__/%{modname}.*
# %{python3_sitelib64}/%{modname}*
# %{python3_sitelib64}/__pycache__/%{modname}.*

%changelog
* Tue Jan 16 2018 Michael Wilson <michael.a.wilson@atos.net> - 1.4.3-2
- Initial version for AIX

