%define name python-libcloud
%define srcname libcloud
%define module_name apache-libcloud
%define egg_name apache_libcloud
%define version 2.0.0
%define release 1

# No tests by default. With tests: rpm -ba --define 'dotests 1' *.spec
%{!?dotests: %define dotests 0}

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
Summary:        A Python library to address multiple cloud provider APIs

Group:          Development/Languages
License:        ASL 2.0
URL:            http://libcloud.apache.org/
Source0:        http://www-us.apache.org/dist/libcloud/%{module_name}/%{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

%description
libcloud is a client library for interacting with many of \
the popular cloud server providers.  It was created to make \
it easy for developers to build products that work between \
any of the services that it supports.
Python 2 version.

BuildRequires:  python-devel
BuildRequires:  python-setuptools
Provides:       python-%{srcname}


# A python3 build/install is not yet supported

# %if 0%{?with_python3}

# %package -n python3-%{srcname}
# Summary:        A Python library to address multiple cloud provider APIs
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# Provides:       python3-%{srcname}
#
# %description
# libcloud is a client library for interacting with many of \
# the popular cloud server providers.  It was created to make \
# it easy for developers to build products that work between \
# any of the services that it supports.
# Python 3 version.
# %endif # with_python3

%prep
%setup -n %{module_name}-%{version}

echo "dotests=%{dotests}"


# Delete shebang lines in the demos
sed -i '1d' demos/gce_demo.py demos/compute_demo.py

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{module_name}-%{version}-32bit
cp -pr . /tmp/%{module_name}-%{version}-32bit
rm -fr * ./.pylintrc
mv       /tmp/%{module_name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build

# %py2_build
# %py3_build

cd 64bit
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64  setup.py build

# Fix permissions for demos
chmod -x demos/gce_demo.py demos/compute_demo.py

cd ../32bit
export OBJECT_MODE=32
/opt/freeware/bin/python2.7  setup.py build

# Fix permissions for demos
chmod -x demos/gce_demo.py demos/compute_demo.py

# %if 0%{?with_python3}
# cd 64bit
# export OBJECT_MODE=64
# /opt/freeware/bin/python3.5_64  setup.py build
#
# Fix permissions for demos
# chmod -x demos/gce_demo.py demos/compute_demo.py
#
# cd ../32bit
# export OBJECT_MODE=32
# /opt/freeware/bin/python3.5  setup.py build
#
# Fix permissions for demos
# chmod -x demos/gce_demo.py demos/compute_demo.py
#
# %endif # with_python3


%install

# %py2_install
# %py3_install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# The test suite is not packaged.
# It is not executed because it requires valid cloud credentials
rm -r $RPM_BUILD_ROOT%{python_sitelib}/%{srcname}/test


# %check
if [ "%{dotests}" == 1 ]
then
 (/opt/freeware/bin/python2.7_64 -m tornado.test.runtests --verbose || true)
fi


# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# The test suite is not packaged.
# It is not executed because it requires valid cloud credentials
rm -r $RPM_BUILD_ROOT%{python_sitelib}/%{srcname}/test


if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 -m tornado.test.runtests --verbose || true)
fi



# rm -r $RPM_BUILD_ROOT%{python3_sitelib}/%{srcname}/test
# rm -r $RPM_BUILD_ROOT%{python3_sitelib64}/%{srcname}/test


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n python-%{srcname}
%doc 32bit/README.rst 32bit/demos/
%doc 32bit/LICENSE
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{egg_name}-*.egg-info
%{python_sitelib64}/%{srcname}/
%{python_sitelib64}/%{egg_name}-*.egg-info

# %files -n python3-%{srcname}
# %doc 32bit/README.rst 32bit/demos/
# %doc 32bit/LICENSE
# %{python3_sitelib}/%{srcname}/
# %{python3_sitelib}/%{egg_name}-*.egg-info
# %{python3_sitelib64}/%{srcname}/
# %{python3_sitelib64}/%{egg_name}-*.egg-info

%changelog
* Mon Jul 10 2017 Michael Wilson <michael.a.wilson@atos.net> - 2.0.0-1
- Initial version

