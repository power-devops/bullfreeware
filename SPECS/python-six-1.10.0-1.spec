%define name python-six
%define srcname six
%define version 1.10.0
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
%global build_wheel 0

%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname



Summary:    Python 2 and 3 compatibility utilities
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    MIT
Group:      Development/Languages
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}
BuildArch:  noarch

URL:        http://pypi.python.org/pypi/six/
Source0:    https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: python, python-devel
BuildRequires: python-setuptools
# BuildRequires: python-sphinx
# Requires: python

# For tests
BuildRequires:  python-pytest
BuildRequires:  tkinter

# %if 0%{?build_wheel}
# BuildRequires:  python-pip
# BuildRequires:  python-wheel
# %endif


%description
Six is a Python 2 and 3 compatibility library.  It provides utility functions
for smoothing over the differences between Python versions with the goal of
writing Python code that is compatible on both Python versions.

Python 2 version.

Six supports every Python version since 2.6.

Online documentation is at https://pythonhosted.org/six/


# %package -n python3-%{srcname}
# Summary:    Python 2 and 3 compatibility utilities
# 
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# For tests
# BuildRequires:  python3-pytest
# BuildRequires:  python3-tkinter
# 
# %if 0%{?build_wheel}
# BuildRequires:  python3-pip
# BuildRequires:  python3-wheel
# %endif
# 
# %description -n python3-%{srcname}
# 
# Six is a Python 2 and 3 compatibility library.  It provides utility functions
# for smoothing over the differences between Python versions with the goal of
# writing Python code that is compatible on both Python versions.
# 
# Python 3 version.
# 
# Six supports every Python version since 2.6.
# 
# Online documentation is at https://pythonhosted.org/six/



%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"

# Remove six.egg-info contents
rm -rf ./six.egg-info

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build

cd 64bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7_64 setup.py build
# %endif

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# %py3_build
# %endif


cd ../32bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7 setup.py build
# %endif

# %if 0%{?build_wheel}
# %py3_build_wheel
# %else
# %py3_build
# %endif


# cd documentation
# make text


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else

/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %endif
# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# %py3_install
# %endif

if [ "%{dotests}" == 1 ]
then
  (py.test-2.7 -rfsxX test_six.py || true)
fi

# py.test-2 -rfsxX test_six.py
# py.test-3 -rfsxX test_six.py

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


cd ../32bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else

/opt/freeware/bin/python2.7  setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %endif
# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# %py3_install
# %endif

if [ "%{dotests}" == 1 ]
then
  (py.test-2.7 -rfsxX test_six.py || true)
fi



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files -n python-%{srcname}
%defattr(-,root,system,-)
# %license LICENSE
%doc 32bit/CHANGES 32bit/LICENSE 32bit/README 
%doc 32bit/documentation/index.rst
%{python_sitelib}/%{srcname}-*.egg-info/
%{python_sitelib}/%{srcname}.py*
%{python_sitelib64}/%{srcname}-*.egg-info/
%{python_sitelib64}/%{srcname}.py*


# %files -n python3-%{srcname}
# %license LICENSE
# %doc 32bit/README 32bit/documentation/index.rst
# %{python3_sitelib}/%{srcname}-*.egg-info/
# %{python3_sitelib}/%{srcname}.py
# %{python3_sitelib}/__pycache__/%{srcname}.*
# %{python3_sitelib64}/%{srcname}-*.egg-info/
# %{python3_sitelib64}/%{srcname}.py*
# %{python3_sitelib64}/__pycache__/%{srcname}.*


%changelog
* Fri Apr 28 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.10.0-1
- Update to version 1.10.0

* Thu Jul 04 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 1.3.0-1
- first version for AIX V6.1 and higher

