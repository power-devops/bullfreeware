%bcond_without dotests

%define name python3-setuptools
%define meta_name setuptools
%define version 59.2.0
%define release 1
%define desc Setuptools is a collection of enhancements to the Python distutils that allow \
you to more easily build and distribute Python packages, especially ones that \
have dependencies on other packages. \
\
This package also contains the runtime components of setuptools, necessary to \
execute the software that requires pkg_resources.py.

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Easily build and distribute Python 3 packages

Group:          Applications/System
License:        MIT and (BSD or ASL 2.0)
URL:            https://pypi.python.org/pypi/%{meta_name}
Source0:        https://files.pythonhosted.org/packages/source/s/%{meta_name}/%{meta_name}-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
# May have to create Python lib/pythonV.vv/site-packages directory
#Patch0: create-site-packages.patch

BuildArch:      noarch

%python_meta_requires

BuildRequires:  python(abi) >= 3.9
BuildRequires:  python3-devel
BuildRequires:  tar, sed

%if %{with dotests}
# # Test. Done with pip for us because these packages are not available.
# BuildRequires: pip
# BuildRequires: pytest
# BuildRequires: mock
# BuildRequires: pytest-fixture-config
# BuildRequires: pytest-virtualenv
# BuildRequires: wheel
%endif # with_dotests

# # Provides bundled.
# Provides: python-packaging = 16.8
# Provides: python-pyparsing = 2.2.1
# Provides: python-six = 1.10.0

%description
%desc

%python_module
%python_module_desc

%prep
export PATH="/opt/freeware/bin:/usr/bin"

# Does not work with AIX tar
%define __tar /opt/freeware/bin/tar

%setup -q -n %{meta_name}-%{version}

# We can't remove .egg-info (but it doesn't matter, since it'll be rebuilt):
#  The problem is that to properly execute setuptools' setup.py,
#   it is needed for setuptools to be loaded as a Distribution
#   (with egg-info or .dist-info dir), it's not sufficient
#   to just have them on PYTHONPATH
#  Running "setup.py install" without having setuptools installed
#   as a distribution gives warnings such as
#    ... distutils/dist.py:267: UserWarning: Unknown distribution option: 'entry_points'
#   and doesn't create "easy_install" and .egg-info directory
# Note: this is only a problem if bootstrapping wheel or building on RHEL,
#  otherwise setuptools are installed as dependency into buildroot

# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled .exe files
rm -f setuptools/*.exe

# These tests require internet connection
# Pass randomly with our proxy...
rm setuptools/tests/test_integration.py 

# Remove erroneous execute permissions
chmod -x README.rst


%build
export PATH="/opt/freeware/bin:/usr/bin"
%{__python} bootstrap.py
%{__python} setup.py build


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export PATH="/opt/freeware/bin:/usr/bin"

%{__python} setup.py install --skip-build --root ${RPM_BUILD_ROOT}

find %{buildroot}%{python_sitelib} -name '*.exe' | xargs rm -f

%check
export PATH="/opt/freeware/bin:/usr/bin"
%if %{with dotests}
%{__python} -m ensurepip --default-pip

# Create virtualenv with right packages.
%{__python} -m venv setupTest
. ./setupTest/bin/activate
pip3 install pytest mock pytest-fixture-config pytest-virtualenv wheel coverage jaraco.envs jaraco.path

sed -i 's|\-\-flake8||g' pytest.ini
sed -i 's|\-\-cov||g' pytest.ini


# From FEDORA
( PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(pwd) ./setupTest/bin/pytest \
    --ignore=pavement.py \
    --deselect=setuptools/tests/test_setuptools.py::TestDepends::testRequire \
    || true)

deactivate
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc LICENSE
%doc docs/* CHANGES.rst README.rst
%{python_sitelib}/pkg_resources/
%{python_sitelib}/setuptools*/
%{python_sitelib}/_distutils_hack/


%changelog
* Tue Nov 23 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 59.2.0-1
- New version 59.2.0
- Add metapackage

* Tue Mar 02 2021 Étienne Guesnet <etienne.guesnet@atos.net> 54.0.0-1
- New version 54.0.0
- No more easy-install binaries
- Add _distutils_hack

* Wed Aug 12 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 49.3.1-1
- New version 49.3.1-1

* Thu Jan 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 45.0.0-1
- New version 45.0.0-1
- Merge with Fedora specfile
- Now use Python3
- Test suite is now executed

* Thu Apr 11 2019 Michael Wilson <michael.a.wilson@atos.net> - 40.8.0-1
- Update to version 40.8.0 for Python 2.7 only

* Wed Apr 12 2017 Michael Wilson <michael.a.wilson@atos.net> - 34.3.2-1
- Update to version 34.3.2-1 for Python 2.7 only
- Remove package python-setuptools-devel

* Fri Nov 07 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.8-2
- Add paquage setuptools-devel

* Mon Aug 12 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.9.8-1
- update and fix provides

* Wed Jul 17 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.9.5-1
- update distribute 0.6.45 with setuptools 0.9.5

* Wed May 1 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.6.45-1
- updated to version 0.6.45

* Thu Nov 17 2011 Michael Perzl <michael@perzl.org> - 0.6.24-1
- updated to version 0.6.24

* Mon Jan 17 2011 Michael Perzl <michael@perzl.org> - 0.6.14-1
- first version for AIX V5.1 and higher
