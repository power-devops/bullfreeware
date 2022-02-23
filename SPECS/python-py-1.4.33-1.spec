%define name python-py
%define srcname py
%define version 1.4.33
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


%global pytest_version_lb 2.9.0
%global pytest_version_ub 2.10

%global srcname py

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   Library with cross-python path, ini-parsing, io, code, log facilities
License:   MIT and Public Domain
#          main package: MIT, except: doc/style.css: Public Domain
Group:     Development/Libraries
URL:       http://pylib.readthedocs.io/en/stable/
Source0:   https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

Source10:  %{name}-%{version}-%{release}.build.log

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:     %{_prefix}

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools

BuildRequires:  python-sphinx
BuildRequires:  python-pytest
# BuildRequires:  python-pytest >= %{pytest_version_lb}, python-pytest < %{pytest_version_ub}
# BuildRequires:  python3-pytest
# BuildRequires:  python3-pytest >= %{pytest_version_lb}, python3-pytest < %{pytest_version_ub}

# needed by the testsuite
BuildRequires:  subversion

%description
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects


Provides:    python-py
Provides:    bundled(python-apipkg) = 1.3.dev


# %package -n python3-py
# Summary:   Library with cross-python path, ini-parsing, io, code, log facilities
# Requires:  python3-setuptools
# Provides:  python3-py
# Provides:  bundled(python3-apipkg) = 1.3.dev
# 
# %description -n python3-py
# The py lib is a Python development support library featuring the
# following tools and modules:
# 
#   * py.path: uniform local and svn path objects
#   * py.apipkg: explicit API control and lazy-importing
#   * py.iniconfig: easy parsing of .ini files
#   * py.code: dynamic code generation and introspection
#   * py.path: uniform local and svn path objects


%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"

# remove shebangs and fix permissions
find . -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * .coveragerc
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# %if 0%{?_with_python3}
# rm -rf %{py3dir}
# cp -a . %{py3dir}
# %endif # with_python3



# A python3 build/install is not yet supported

%build

cd 64bit
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64  setup.py build

cd ../32bit
export OBJECT_MODE=32
/opt/freeware/bin/python2.7  setup.py build

make -C doc html PYTHONPATH=$(pwd)


# %py3_build
# %if 0%{?with_docs}
# make -C doc html PYTHONPATH=$(pwd)
# %endif # with_docs


# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# remove hidden file
rm -rf doc/_build/html/.buildinfo

# %check
if [ "%{dotests}" == 1 ]
then

 (PYTHONPATH=%{buildroot}%{python_sitelib} \
  LC_ALL="en_US.UTF-8" \
  py.test-2.7 -r s -k"-TestWCSvnCommandPath" testing    || true)
fi

# %py3_install
# remove hidden file
# rm -rf doc/_build/html/.buildinfo


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# remove hidden file
rm -rf doc/_build/html/.buildinfo



# %check
if [ "%{dotests}" == 1 ]
then

 (PYTHONPATH=%{buildroot}%{python_sitelib} \
  LC_ALL="en_US.UTF-8" \
  py.test-2.7 -r s -k"-TestWCSvnCommandPath" testing    || true)
fi


# %py3_install
# remove hidden file
# rm -rf doc/_build/html/.buildinfo
# 
# if [ "%{dotests}" == 1 ]
# then
# 
#  (PYTHONPATH=%{buildroot}%{python3_sitelib} \
#   LC_ALL="en_US.UTF-8" \
#   py.test-%{python3_version} -r s -k"-TestWCSvnCommandPath" testing
#            || true)
# fi


#%clean
#[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-py
%defattr(-,root,system,-)
%doc 32bit/CHANGELOG 32bit/README.rst
# %license python2/LICENSE
%doc 32bit/LICENSE
%doc 32bit/doc/_build/html
%{python_sitelib}/*
%{python_sitelib64}/*


# %files -n python3-py
# %doc python3/CHANGELOG
# %doc python3/README.rst
# %license python2/LICENSE
# %if 0%{?with_docs}
# %doc python3/doc/_build/html
# %endif # with_docs
# %{python3_sitelib}/*


%changelog
* Thu May 11 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.4.33-1
- Update to version 1.4.33

* Thu Jul 17 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 1.4.15-1
- first version for AIX V6.1 and higher

