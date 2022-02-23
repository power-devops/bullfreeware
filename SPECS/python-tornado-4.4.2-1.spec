%define name python-tornado
%define srcname tornado
%define version 4.4.2
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# Configure tests for gcc first, so default is GCC if installed on the machine
# To force gcc : --define 'gcc_compiler=x'
# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}


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
Summary:        Scalable, non-blocking web server and tools

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.tornadoweb.org
Source0:        https://files.pythonhosted.org/packages/source/t/tornado/tornado-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

# Patch to use system CA certs instead of certifi
# Patch1:  python-tornado-cert.patch

# Patch to run tests in BuildRoot
# https://github.com/tornadoweb/tornado/pull/1781
Patch2:  python-tornado-options_test.patch

# Patch to fix tests for Python 3.6
# https://github.com/tornadoweb/tornado/commit/a391e126e7f277244c691f5057d4cdb97c1ba2e7
# Patch3:  update-warning-config-to-fix-tests-on-python-3.6-nightly.patch

BuildRequires:  python-devel
BuildRequires:  python-backports_abc
BuildRequires:  python-singledispatch
# %if 0%{?with_python3}
# BuildRequires:  python3-setuptools
# BuildRequires:  python3-devel
# %endif

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


Requires:       python-pycurl
Requires:       python-backports_abc
Requires:       python-singledispatch


%package doc
Summary:        Examples for python-tornado
Group:          Documentation
Obsoletes:      python-%{srcname}-doc < 4.2.1-3
Provides:       python-%{srcname}-doc = %{version}-%{release}

%description doc
Tornado is an open source version of the scalable, non-blocking web
server and and tools. This package contains some example applications.


# A python3 build/install is not yet supported

# %if 0%{?with_python3}
# %package -n python3-%{srcname}
# Summary:        Scalable, non-blocking web server and tools
# %{?python_provide:%python_provide python3-%{srcname}}
# Requires:       python3-pycurl
# 
# %description -n python3-%{srcname}
# Tornado is an open source version of the scalable, non-blocking web
# server and tools.
# 
# The framework is distinct from most mainstream web server frameworks
# (and certainly most Python frameworks) because it is non-blocking and
# reasonably fast. Because it is non-blocking and uses epoll, it can
# handle thousands of simultaneous standing connections, which means it is
# ideal for real-time web services.
# %endif # with_python3


%prep 
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"

# %patch1 -p1 -b .cert
%patch2 -p1 -b .test
# %patch3 -p1
# Filter interpreter string - typically   #!/usr/bin/env python
sed -i.orig -e '/^#!\//, 1d' *py tornado/*.py tornado/*/*.py


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

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export CC__="/opt/freeware/bin/gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export CC__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


cd 64bit
export CC="${CC64} "
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64  setup.py build

cd ../32bit
export CC="${CC32} "
export OBJECT_MODE=32
/opt/freeware/bin/python2.7  setup.py build


# %if 0%{?with_python3}
# cd 64bit
# export OBJECT_MODE=64
# /opt/freeware/bin/python3.5_64  setup.py build
# 
# cd ../32bit
# export OBJECT_MODE=32
# /opt/freeware/bin/python3.5  setup.py build
# 
# %endif # with_python3



# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}


# %check
if [ "%{dotests}" == 1 ]
then
 (/opt/freeware/bin/python2.7_64 -m tornado.test.runtests --verbose || true)
fi


# Move lib to lib64  - Already lib64 ???
# mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 -m tornado.test.runtests --verbose || true)
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}




%files -n python-%{srcname}
%defattr(-,root,system,-)
%doc 32bit/README.rst
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}-%{version}-*.egg-info
%{python_sitelib64}/%{srcname}/
%{python_sitelib64}/%{srcname}-%{version}-*.egg-info

%files doc
%doc 32bit/demos

# %if 0%{?with_python3}
# %files -n python3-%{srcname}
# %defattr(-,root,system,-)
# %doc 32bit/README.rst
# %{python3_sitelib}/%{srcname}/
# %{python3_sitelib}/%{srcname}-%{version}-*.egg-info
# %{python3_sitelib64}/%{srcname}/
# %{python3_sitelib64}/%{srcname}-%{version}-*.egg-info
# %endif


%changelog
* Mon May 22 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.4.2-1
- Update to version 4.4.2

* Fri Nov 21 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 4.0.2-1
- First version for AIX V6.1 and higher

