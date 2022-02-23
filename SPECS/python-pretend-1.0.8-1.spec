%define name python-pretend
%define srcname pretend
%define version 1.0.8
%define release 1

%global srcname pretend

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


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A library for stubbing in Python


Group:          Development/Libraries
License:        BSD
URL:            https://github.com/alex/pretend
Source0:        https://pypi.python.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:      %{_prefix}


BuildRequires:  python-devel
BuildRequires:  python-setuptools
# %if %{with python3}
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# %endif


%{?python_provide:%python_provide python2-%{srcname}}


%description -n python-pretend
Pretend is a library to make stubbing with Python easier.


# %if %{with python3}
# %package -n python3-pretend
# Summary:        A library for stubbing in Python
# Group:          Development/Libraries
# License:        BSD
# %{?python_provide:%python_provide python3-%{srcname}}
# 
# %description -n python3-pretend
# Pretend is a library to make stubbing with Python easier.
# %endif


%prep
%setup -q -n %{srcname}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr * .coveragerc
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

cd 64bit

/opt/freeware/bin/python2.7_64  setup.py build

# %if %{with python3}
# /opt/freeware/bin/python3.6_64  setup.py build
# %endif

cd ../32bit

/opt/freeware/bin/python2.7  setup.py build

# %if %{with python3}
# /opt/freeware/bin/python3.6  setup.py build
# %endif



%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit

/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %check
if [ "%{dotests}" == 1 ]
then
 echo No tests defined
fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


# %if %{with python3}
# /opt/freeware/bin/python3.6_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif


cd ../32bit

/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %check
if [ "%{dotests}" == 1 ]
then
 echo No tests defined
fi


# %if %{with python3}
# /opt/freeware/bin/python3.6 setup.py install --skip-build --root ${RPM_BUILD_ROOT}
# %endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-pretend
%doc 32bit/PKG-INFO 32bit/README.rst
%doc 32bit/LICENSE.rst
%{python_sitelib}/pretend.py*
%{python_sitelib}/pretend-%{version}-py2.?.egg-info
%{python_sitelib64}/pretend.py*
%{python_sitelib64}/pretend-%{version}-py2.?.egg-info

# %if %{with python3}
# %files -n python3-pretend
# %doc 32bit/PKG-INFO 32bit/README.rst
# %doc 32bit/LICENSE.rst
# %{python3_sitelib}/pretend.py
# %{python3_sitelib}/__pycache__/pretend.cpython-3?*
# %{python3_sitelib}/pretend-%{version}-py3.?.egg-info
# %{python3_sitelib64}/__pycache__/pretend.cpython-3?*
# %{python3_sitelib64}/pretend-%{version}-py3.?.egg-info
# %endif


%changelog
* Tue Jan 16 2018 Michael Wilson <michael.a.wilson@atos.net> - 1.0.8-1
- Initial version for AIX

