# Python 2.7 version only, Python 3.5 may be added in future release

%define name python-setuptools
%define srcname setuptools
%define version 34.3.2
%define release 1

%global build_wheel 0
%global with_python3 0

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

# Configure tests for gcc first, so default is GCC if installed on the machine
# To force gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}

#%global __python2 %__python
#%global python2_sitelib %python_sitelib

%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%global python2_record %{python2_sitelib}/%{srcname}-%{version}.dist-info/RECORD
#%if 0%{?with_python3}
#%global python3_wheelname %python2_wheelname
#%global python3_record %{python3_sitelib}/%{srcname}-%{version}.dist-info/RECORD
#%endif
%endif

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Easily build and distribute Python packages

Group:          Applications/System
License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/s/%{srcname}/%{srcname}-%{version}.zip

# Add --executable option to easy_install command to make it work for
# entry_points (from Fedora 26 34.2)
#Patch0: add-executable-option.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-packaging
BuildRequires:  python-appdirs
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
%if 0%{?with_check}
BuildRequires:  python-pytest
BuildRequires:  python-mock
BuildRequires:  python-backports-unittest_mock
%endif # with_check

#%if 0%{?with_python3}
#BuildRequires:  python3-devel
#BuildRequires:  python3-packaging
#BuildRequires:  python3-appdirs
#%if 0%{?with_check}
#BuildRequires:  python3-pytest
#BuildRequires:  python3-mock
#%endif # with_check
#%if 0%{?build_wheel}
#BuildRequires:  python3-pip
#BuildRequires:  python3-wheel
#%endif # build_wheel
#%endif # with_python3

Obsoletes: python-setuptools-devel

# Following may not be necessary, just keep the Obsoletes
Provides: distribute
Provides: python-distribute = %{version}-%{release}
Obsoletes: python-distribute < 0.6.36-2

Requires: python-packaging >= 16.8
Requires: python-six >= 1.6.0
Requires: python-appdirs >= 1.4.0


%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.


%if 0%{?with_python3}
%package -n python3-setuptools
Summary:        Easily build and distribute Python 3 packages
Requires: python3-packaging >= 16.8
Requires: python3-six >= 1.6.0
Requires: python3-appdirs >= 1.4.0
Group:          Applications/System
%{?python_provide:%python_provide python3-setuptools}


%description -n python3-setuptools
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%endif # with_python3

%prep
rm -rf ./setuptools-%{version}
mkdir setuptools-34.3.2
%setup -q -D -T -n %{srcname}-%{version}

# The rpm 3.0.5 command does not recognize .zip source files
cd ..
/usr/bin/unzip -qq /opt/freeware/src/packages/SOURCES/%{srcname}-%{version}.zip
cd ./%{srcname}-%{version}

# No need to build 32 and 64 bit versions, this is noarch only

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
find setuptools -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled .exe files
rm -f setuptools/*.exe
# These tests require internet connection
#rm setuptools/tests/test_integration.py 

#%patch0 -p1

%build

%if 0%{?build_wheel}
%py2_build_wheel
%else
/opt/freeware/bin/python2.7 setup.py build
%endif

#%if 0%{?with_python3}
#%if 0%{?build_wheel}
#%py3_build_wheel
#%else
#%py3_build
#%endif
#%endif # with_python3

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
#%if 0%{?with_python3}
#%if 0%{?build_wheel}
#%py3_install_wheel %{python3_wheelname}
#
#sed -i '/\/usr\/bin\/easy_install,/d' %{buildroot}%{python3_record}
#%else
#%py3_install
#%endif
#
#rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests
#%if 0%{?build_wheel}
#sed -i '/^setuptools\/tests\//d' %{buildroot}%{python3_record}
#%endif
#
#find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
#%endif # with_python3

%if 0%{?build_wheel}
%py2_install_wheel %{python2_wheelname}
%else
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
%endif

#rm -rf %{buildroot}%{python2_sitelib}/setuptools/tests
%if 0%{?build_wheel}
sed -i '/^setuptools\/tests\//d' %{buildroot}%{python2_record}
%endif

find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f

# Don't ship these
# Following is Open Source rm command
#rm -r docs/{Makefile,conf.py,_*}

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


#%if 0%{?with_check}
#%check

#python setup.py test
#LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test

# Not currently able to run tests
#PYTHONPATH=$(pwd) py.test

#%if 0%{?with_python3}
#LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test-%{python3_version}
#%endif # with_python3
#%endif # with_check


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
# %license LICENSE
%doc LICENSE
%doc docs/* CHANGES.rst README.rst
%{python2_sitelib}/*
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*
/usr/bin/*

#%if 0%{?with_python3}
#%files -n python3-setuptools
#%license LICENSE CHANGES.rst README.rst
#%doc docs/*
#%{python3_sitelib}/easy_install.py
#%{python3_sitelib}/pkg_resources/
#%{python3_sitelib}/setuptools*/
#%{python3_sitelib}/__pycache__/*
#%{_bindir}/easy_install-3.*
#%endif # with_python3

%changelog
* Wed Apr 12 2017 Michael Wilson <michael.a.wilson@atos.net> - 34.3.2-1
- Update to version 34.3.2-1 for Python 2.7 only
- Remove package python-setuptools-devel

* Fri Nov 07 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.8-2
- Add paquage setuptools-devel

* Thu Aug 12 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.9.8-1
- update and fix provides

* Thu Jul 17 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.9.5-1
- update distribute 0.6.45 with setuptools 0.9.5

* Thu May 1 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.6.45-1
- updated to version 0.6.45

* Thu Nov 17 2011 Michael Perzl <michael@perzl.org> - 0.6.24-1
- updated to version 0.6.24

* Mon Jan 17 2011 Michael Perzl <michael@perzl.org> - 0.6.14-1
- first version for AIX V5.1 and higher
