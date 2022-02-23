%bcond_without dotests
%bcond_with doc

%define name python3-pip
%define meta_name pip
%define version 21.3.1
%define release 1
%define desc pip is a package management system used to install and manage software packages \
written in Python. Many packages can be found in the Python Package Index (PyPI).

Summary: Tool for installing and managing Python packages.
Name: %{name}
Version: %{version}
Release: %{release}
# Full URL is
# https://files.pythonhosted.org/packages/da/f6/c83229dcc3635cdeb51874184241a9508ada15d8baa337a41093fab58011/pip-%%{version}.tar.gz
# Not possible to deal with automatically.
Source0: pip-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

# to get tests:
# git clone https://github.com/pypa/pip && cd pip
# VERSION=   # define the version you want
# git checkout $VERSION && tar -czvf ../pip-$VERSION-tests.tar.gz tests/
%if %{with dotests}
#Source1:        pip-%{version}-tests.tar.gz
%endif

License: MIT
Group: Development/Libraries

BuildArch: noarch
Url: https://pypi.python.org/pypi/pip/

BuildRequires: sed tar
BuildRequires: python(abi) >= 3.9
BuildRequires: python3-setuptools >= 50.0.0

%python_meta_requires

%description
%desc

%python_module
%python_module_desc


# Not yet tested!
%if %{with doc}
%package doc
Summary:        A documentation for a tool for installing and managing Python packages

BuildRequires:  python3-sphinx

%description doc
A documentation for a tool for installing and managing Python packages
%endif


%prep
%define __tar %{_bindir}/tar
%setup -q -n %{meta_name}-%{version}
%if %{with dotests}
#%__tar -xf %{SOURCE1}
%endif


%build
%{__python} setup.py build

%if %{with doc}
export PYTHONPATH=./src/
# from tox.ini
sphinx-build-3 -b html docs/html docs/build/html
sphinx-build-3 -b man  docs/man  docs/build/man  -c docs/html
rm docs/build/html/.buildinfo
%endif

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export PATH="/opt/freeware/bin:/usr/bin"

%{__python} setup.py install --skip-build --root ${RPM_BUILD_ROOT}


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

cd ../python3
mkdir _bin
export PATH="$PWD/_bin:$PATH"

export PYTHONPATH="%{buildroot}%{python3_sitelib}:/opt/freeware/lib/python3/site-packages/"
ln -sf %{buildroot}%{_bindir}/pip3 _bin/pip3
(python3_64 -m pytest -m 'not network' -k "$(echo $pytest_k)" || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc LICENSE.txt PKG-INFO README.rst 
%{python_sitelib}/*
%{_bindir}/pip*

%if %{with doc}
%files doc
%defattr(-,root,system,-)
%doc  LICENSE.txt
%doc  README.rst
%doc  docs/build/html
%endif


%changelog
* Tue Nov 23 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 21.3.1-1
- New version 21.3.1
- Add metapackage
- Remove all mention of python2

* Thu Jan 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 19.3.1
- New version 19.3.1
- Port on Python 3
- Detail trouble with test

* Tue May 21 2019 Tony Reix <tony.reix@atos.net> - 10.0.1-1
- Port on BullFreeware

* Wed Jun 13 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 10.0.1-1
- Updated to 10.0.1

* Wed Feb 22 2017 Sangamesh Mallayya <smallayy@in.ibm.com> 9.0.1-1
- Initial port to AIX.
