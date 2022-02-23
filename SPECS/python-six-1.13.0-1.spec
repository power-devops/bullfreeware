%define name python-six
%define srcname six
%define version 1.13.0
%define release 1

# Beware, test suite use pip to download some script.
# Hard to automatise on both 32 and 64 bits.
%bcond_without dotests

# It is a script. We put .py and .pyc only on sitelib.
%define is_python %(test -e /opt/freeware/bin/python2.7_32 && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib   %(/opt/freeware/bin/python2.7_32 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%endif

%define _libdir64 %{_prefix}/lib64

%global with_python3 1
%if %{with_python3}
%define python3_sitelib   %(/opt/freeware/bin/python3_32 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%define python3_minor_version %(/opt/freeware/bin/python3 -c "import sys; print(sys.version.split('.')[1])")
%endif

%global build_wheel 0
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname


Summary:    Python 2 and 3 compatibility utilities
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    MIT
Group:      Development/Languages
BuildArch:  noarch

URL:        http://pypi.python.org/pypi/six/
Source0:    https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.tar.gz

Source1000: %{name}-%{version}-%{release}.build.log

Requires: python
BuildRequires: python, python-devel
BuildRequires: python-setuptools

# For documentation
BuildRequires: python-sphinx

%if %{with dotests}
# For tests
BuildRequires:  python-pytest
# Workaround: py is needed by pytest but requires was forgotten
BuildRequires:  python-py
# BuildRequires:  tkinter
%endif

%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif


%description
Six is a Python 2 and 3 compatibility library.  It provides utility functions
for smoothing over the differences between Python versions with the goal of
writing Python code that is compatible on both Python versions.

Python 2 version.

Six supports every Python version since 2.6.

Online documentation is at https://pythonhosted.org/six/

%if %{with_python3}
%package -n python3-%{srcname}
Summary:    Python 2 and 3 compatibility utilities
Provides:  python3-%{srcname}
Requires:       python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
# For tests
# BuildRequires:  python3-pytest

# BuildRequires:  python3-tkinter

%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif

%description -n python3-%{srcname}

Six is a Python 2 and 3 compatibility library.  It provides utility functions
for smoothing over the differences between Python versions with the goal of
writing Python code that is compatible on both Python versions.

Python 3 version.

Six supports every Python version since 2.6.

Online documentation is at https://pythonhosted.org/six/
%endif


%prep
%setup -q -n %{srcname}-%{version}

# Remove six.egg-info contents
rm -rf ./six.egg-info

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%if %{with python3}
# Duplicate source for python2 and python3
rm -rf   /tmp/%{name}-%{version}-python2
cp -pr . /tmp/%{name}-%{version}-python2
rm -fr *
mv       /tmp/%{name}-%{version}-python2 python2
cp -pr python2 python3
%endif


%build

cd python2
cd 64bit

# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7_64 setup.py build
# %endif
cd ../32bit
# %if 0%{?build_wheel}
# %py2_build_wheel
# %else
/opt/freeware/bin/python2.7_32 setup.py build
# %endif
# documentation (as text file) made on 32bit.
# Need sphinx
cd documentation
# make text
cd ../..

%if %{with_python3}
cd ../python3/64bit
/opt/freeware/bin/python3_64 setup.py build
cd ../32bit
/opt/freeware/bin/python3_32 setup.py build
cd documentation
# make text
cd ../..
%endif


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd python2
cd 64bit

# # Do not need to install on 64 bits

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else

# /opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %endif
# %if 0%{?build_wheel}
# %py3_install_wheel %{python3_wheelname}
# %else
# %py3_install
# %endif
  
# py.test-2 -rfsxX test_six.py
# py.test-3 -rfsxX test_six.py

# Move lib to lib64
# mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit

# %if 0%{?build_wheel}
# %py2_install_wheel %{python2_wheelname}
# %else

/opt/freeware/bin/python2.7_32  setup.py install --skip-build --root ${RPM_BUILD_ROOT}

%if %{with_python3}
cd ../../python3/32bit
/opt/freeware/bin/python3_32  setup.py install --skip-build --root ${RPM_BUILD_ROOT}
%endif

%check
%if %{with dotests}
cd python2/32bit
(python2.7_32 /opt/freeware/bin/py.test -rfsxX test_six.py || true)
cd ../64bit
(python2.7_64 /opt/freeware/bin/py.test -rfsxX test_six.py || true)
%if %{with_python3}
cd ../../python3/32bit
(
  # Create virtualenv with right packages.
  python3_32 -m venv six_env
  . ./six_env/bin/activate
  pip3 install pytest
  python3_32 -m pytest -rfsxX test_six.py || true
  deactivate
)
cd ../64bit
(
  python3_64 -m venv six_env
  . ./six_env/bin/activate
  pip3 install pytest
  python3_64 -m pytest -rfsxX test_six.py || true
  deactivate
)
%endif
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{srcname}
%defattr(-,root,system,-)
# %license LICENSE
%doc python2/32bit/CHANGES python2/32bit/LICENSE python2/32bit/README.rst
# %doc python2/32bit/documentation/_build/text/index.txt
%{python_sitelib}/%{srcname}-*.egg-info/
%{python_sitelib}/%{srcname}.py*
# %{python_sitelib64}/%{srcname}-*.egg-info/
# %{python_sitelib64}/%{srcname}.py*

%if %{with_python3}
%files -n python3-%{srcname}
%defattr(-,root,system,-)
%doc python3/32bit/LICENSE python3/32bit/CHANGES python3/32bit/README.rst 
# %doc python3/32bit/documentation/_build/text/index.txt
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/__pycache__/%{srcname}.*
# %{python3_sitelib64}/%{srcname}-*.egg-info/
# %{python3_sitelib64}/%{srcname}.py*
# %{python3_sitelib64}/__pycache__/%{srcname}.*
%endif


%changelog
* Mon Jan 13 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.13.0-1
- New version 1.13.0
- Provide python3 package

* Fri Apr 28 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.10.0-1
- Update to version 1.10.0

* Thu Jul 04 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 1.3.0-1
- first version for AIX V6.1 and higher

