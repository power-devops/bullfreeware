%define name python-futures
%define srcname futures
%define modname concurrent
%define version 3.1.1
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


Summary:       Backport of the concurrent.futures package from Python 3.2
Name:          %{name}
Version:       %{version}
Release:       %{release}
License:       Python
Group:         Development/Libraries
URL:           https://pypi.python.org/pypi/futures
Source0:       https://files.pythonhosted.org/packages/source/f/futures/futures-%{version}.tar.gz
BuildRequires: python-devel
BuildArch:     noarch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log


%description
The concurrent.futures module provides a high-level interface for
asynchronously executing callables.

Provides:  python-futures = %{version}-%{release}
Obsoletes: python-futures < %{version}-%{release}


%prep
%setup -q -n %{srcname}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

 # First build the 64-bit version
cd 64bit
/opt/freeware/bin/python2.7_64 setup.py build

# Build the 32-bit version
cd ../32bit
/opt/freeware/bin/python2.7 setup.py build


%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# %check
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 setup.py test || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Currently there are no tests
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 setup.py test || true)
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files -n python-futures
# %license LICENSE
%doc 32bit/LICENSE
%doc 32bit/CHANGES
%{python_sitelib}/%{modname}
%{python_sitelib}/%{srcname}-*.egg-info
%{python_sitelib64}/%{modname}
%{python_sitelib64}/%{srcname}-*.egg-info


%changelog
* Mon May 22 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.1.1-1
- Initial version

