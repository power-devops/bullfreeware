%bcond_without dotests
%bcond_with doc
%bcond_without python2
%bcond_without python3

%define name python-pip
%define srcname pip
%define version 19.3.1
%define release 1

%define is_python %(test -e /opt/freeware/bin/python2_64 && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python2_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
%endif

%define is_python3 %(test -e /opt/freeware/bin/python3_64 && echo 1 || echo 0)
%if %{is_python3}
%define python3_sitelib %(python3_64 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%endif

%if %{with python2}
%if %{is_python}
# Fine
%else
echo "Python2 required. Install it on standard location,"
echo "or use rmpmbuidl with flag '--without python2'."
%endif
%endif

%if %{with python3}
%if %{is_python3}
# Fine
%else
echo "Python3 required. Install it on standard location,"
echo "or use rmpmbuidl with flag '--without python3'."
%endif
%endif

Summary: Tool for installing and managing Python packages.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{srcname}-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

# to get tests:
# git clone https://github.com/pypa/pip && cd pip
# VERSION=   # define the version you want
# git checkout $VERSION && tar -czvf ../pip-$VERSION-tests.tar.gz tests/
%if %{with dotests}
Source1:        pip-%{version}-tests.tar.gz
%endif

License: MIT
Group: Development/Libraries

BuildArch: noarch
Url: https://pypi.python.org/pypi/pip/

BuildRequires: sed

%if %{with python2}
BuildRequires: python, python-devel
BuildRequires: python-setuptools >= 0.9.8-2
Requires: python
Requires: python-setuptools >= 0.9.8-2
%endif

%description
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index (PyPI).


%if %{with python3}
%package -n python3-%{srcname}
Summary:        A tool for installing and managing Python3 packages
BuildRequires: python3, python3-devel
BuildRequires: python3-setuptools >= 0.9.8-2
Requires: python3
Requires: python3-setuptools >= 0.9.8-2

%description -n python3-%{srcname}
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index (PyPI).
%endif


# Not yet tested!
%if %{with doc}
%package doc
Summary:        A documentation for a tool for installing and managing Python packages

BuildRequires:  python3-sphinx

%description doc
A documentation for a tool for installing and managing Python packages
%endif


%prep
%setup -q -n %{srcname}-%{version}
%if %{with dotests}
tar -xf %{SOURCE1}
%endif

mkdir ../python2
mv * ../python2
mv ../python2 .
mkdir python3
cp -r python2/* python3/

%build
cd python2
%if %{with python2}
python2_64 setup.py build
%endif

cd ../python3
%if %{with python3}
python3_64 setup.py build
%endif

%if %{with doc}
export PYTHONPATH=./src/
# from tox.ini
sphinx-build-3 -b html docs/html docs/build/html
sphinx-build-3 -b man  docs/man  docs/build/man  -c docs/html
rm docs/build/html/.buildinfo

# # OLD
# # Building docs.
# cd docs
# gmake
%endif

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export PATH="/opt/freeware/bin:/usr/bin"

cd python3
%if %{with python3}
python3_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
%endif

# Python2 has priority on python3
cd ../python2
%if %{with python2}
python2_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
%endif

sed -i 's|#!/opt/freeware/bin/python3_64|#! /usr/bin/env python3|' $RPM_BUILD_ROOT/%{_bindir}/*
sed -i 's|#!/opt/freeware/bin/python2_64|#! /usr/bin/env python2|' $RPM_BUILD_ROOT/%{_bindir}/*

# # Useless, it is scripts!
# (
#   cd ${RPM_BUILD_ROOT}%{_bindir}
#   for f in *
#   do
#     mv ${f} ${f}_64
#   done
# )


%check
# Up to now, we cannot run easily test from specfile.
# Tests need the following modules:
# mock pytest pretend freezegun scripttest virtualenv pyyaml
# py pluggy attrs packaging attr wcwidth
# We do not provide them. So, we install it throught pip itself.
# However, the this interacts with test and causes mass fails for functional tests.
# Unittest are less affected, and 8 of them fail on ~1000.
#
# To test, install the listed packages in a virtual env here called VIRT_PIP.
#
# Copy the tests from pip-test. To get tests:
# git clone https://github.com/pypa/pip && cd pip
# VERSION=   # define the version you want
# git checkout $VERSION && tar -czvf ../pip-$VERSION-tests.tar.gz tests/
#
# Copy or link the VIRT_PIP/lib/python3/site-packages/virtualenv_support to
# tests/data/common_wheels.
#
# Modify tests/conftest.py to use directly python and not virtual python created by pip.
# This will cause some fail, but setup of functional test does not work without this trick.
# line 242
# - subprocess.check_call([venv.bin / 'python', 'setup.py', '-q', 'develop'],
# + subprocess.check_call(['python3', 'setup.py', '-q', 'develop'],
# remove tests/functional/test_yaml.py and tests/functional/test_no_color.py.
# They cause crash of test suite.
# Now, you can the test with right path and pythonpath, see command bellow.

%if %{with dotests}
# From Fedora
# bash completion tests only work from installed package
# needs unaltered sys.path and we cannot do that in %%check
#     test_pep517_and_build_options
#     test_config_file_venv_option
# TODO investigate failures
#     test_uninstall_non_local_distutils
pytest_k='not completion and
          not test_pep517_and_build_options and
          not test_config_file_venv_option and
          not test_uninstall_non_local_distutils'

cd python2
%if %{with python2}
mkdir _bin
export PATH="$PWD/_bin:$PATH"

# Add pip env.
export PYTHONPATH=%{buildroot}%{python_sitelib}
ln -sf %{buildroot}%{_bindir}/pip2 _bin/pip2
(python2_64 -m pytest -m 'not network' -k "$(echo $pytest_k)" || true)
%endif

cd ../python3
%if %{with python3}
mkdir _bin
export PATH="$PWD/_bin:$PATH"

export PYTHONPATH="%{buildroot}%{python3_sitelib}:/opt/freeware/lib/python3/site-packages/"
ln -sf %{buildroot}%{_bindir}/pip3 _bin/pip3
(python3_64 -m pytest -m 'not network' -k "$(echo $pytest_k)" || true)
%endif
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%if %{with python2}
%files
%defattr(-,root,system,-)
%doc python2/LICENSE.txt python2/PKG-INFO python2/README.rst 
%{python_sitelib}/*
%{_bindir}/pip
%{_bindir}/pip2*
%endif


%if %{with python3}
%files -n python3-%{srcname}
%defattr(-,root,system,-)
%doc python3/LICENSE.txt python3/PKG-INFO python3/README.rst 
%{python3_sitelib}/*
%{_bindir}/pip3*
%endif


%if %{with doc}
%files doc
%defattr(-,root,system,-)
%doc  python2/LICENSE.txt
%doc  python2/README.rst
%doc  python2/docs/build/html
%endif


%changelog
* Thu Jan 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net>
- New version 19.3.1
- Port on Python 3
- Detail trouble with test

* Tue May 21 2019 Tony Reix <tony.reix@atos.net> - 10.0.1-1
- Port on BullFreeware

* Wed Jun 13 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 10.0.1-1
- Updated to 10.0.1

* Wed Feb 22 2017 Sangamesh Mallayya <smallayy@in.ibm.com> 9.0.1-1
- Initial port to AIX.
