# Beware, test suite use pip to download some script.
# Hard to automatise on both 32 and 64 bits.
%bcond_without dotests

# No doc by default
%bcond_with doc

%define name python3-six
%define meta_name six
%define version 1.16.0
%define release 1
%define desc Six is a Python 2 and 3 compatibility library.  It provides utility functions \
for smoothing over the differences between Python versions with the goal of \
writing Python code that is compatible on both Python versions.

%define _libdir64 %{_prefix}/lib64

%global build_wheel 0

Summary:    Python 2 and 3 compatibility utilities
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    MIT
Group:      Development/Languages
BuildArch:  noarch

URL:        http://pypi.python.org/pypi/six/
Source0:    https://files.pythonhosted.org/packages/source/s/six/six-%{version}.tar.gz

Source1000: %{name}-%{version}-%{release}.build.log

%python_meta_requires

BuildRequires: tar
BuildRequires: python(abi) >= 3.9, python3-devel
BuildRequires: python3-setuptools

%if %{with doc}
# For documentation
BuildRequires: python-sphinx
%endif

# For tests; done with pip
# BuildRequires:  python-pytest
# BuildRequires:  tkinter

%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif


%description
%desc

%python_module
%python_module_desc


%prep
%define __tar %{_bindir}/tar
%setup -q -n %{meta_name}-%{version}

# Remove six.egg-info contents
#rm -rf ./six.egg-info


%build
%{__python} setup.py build
%if %{with doc}
cd documentation
make text
%endif


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root ${RPM_BUILD_ROOT}


%check
%if %{with dotests}
(
  # Create virtualenv with right packages.
  %{__python} -m venv six_env
  . ./six_env/bin/activate
  pip install pytest py
  %{__python} -m pytest -rfsxX test_six.py || true
  deactivate
)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc LICENSE CHANGES README.rst
%if %{with doc} 
%doc python3/32bit/documentation/_build/text/index.txt
%endif
%{python_sitelib}/%{meta_name}-*.egg-info/
%{python_sitelib}/%{meta_name}.py
%{python_sitelib}/__pycache__/%{meta_name}.*


%changelog
* Wed Nov 24 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 1.16.0-1
- New version 1.16.0-1
- Remove all python2 and 32 bits support
- Add metapackage

* Mon Jan 13 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.13.0-1
- New version 1.13.0
- Provide python3 package

* Fri Apr 28 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.10.0-1
- Update to version 1.10.0

* Thu Jul 04 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 1.3.0-1
- first version for AIX V6.1 and higher

