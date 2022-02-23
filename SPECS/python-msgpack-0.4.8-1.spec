%define name python-msgpack
%define srcname msgpack
%define version 0.4.8
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

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
Summary:        A Python MessagePack (de)serializer
Group:          Applications/System

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/msgpack-python/
Source0:        https://files.pythonhosted.org/packages/source/m/%{srcname}-python/%{srcname}-python-%{version}.tar.gz

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
# BuildRequires:  python3-devel
# BuildRequires:  python3-setuptools
# BuildRequires:  python3-pytest

%description
MessagePack is a fast, compact binary serialization format, suitable
for data similar to JSON.
This package provides CPython bindings for reading and writing
MessagePack data.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


# %package -n python3-%{srcname}
# Summary:        A Python MessagePack (de)serializer
# Group:          Applications/System
# Provides:       python3-%{srcname}
# 
# %description -n python3-%{srcname}
# MessagePack is a fast, compact binary serialization format, suitable
# for data similar to JSON.
# This package provides CPython bindings for reading and writing
# MessagePack data.
# This is a Python python3 (de)serializer for MessagePack.


%prep
# %autosetup not recognized by RPM 3.0.5
# May be it sets BuildRoot - %{buildroot}
#%autosetup -n %{srcname}-python-%{version}

%setup -n %{srcname}-python-%{version}

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# A python3 build/install is not yet supported

%build

# setup environment for 32-bit and 64-bit builds

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
# export LDFLAGS="-L./.libs -L/opt/freeware/lib"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/fr
eeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
# export LDFLAGS="-L./.libs -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"

/opt/freeware/bin/python2.7_64 setup.py build

# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"

/opt/freeware/bin/python2.7 setup.py build


# %py3_build

# A python3 build/install is not yet supported

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
export OBJECT_MODE=64

/opt/freeware/bin/python2.7_64 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}


# %check is not recogized by RPM 3.0.5
#%check

# py.test and py.test-%{python_version} are delivered in python-pytest
# py.test-3 and py.test-%{python3_version} are delivered in python3-pytest

if [ "%{dotests}" == 1 ]
then
  export PYTHONPATH=$(pwd)
  (py.test -v test || true)
fi


# Move lib to lib64
# mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
export OBJECT_MODE=32

/opt/freeware/bin/python2.7 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

# Currently there are no tests
if [ "%{dotests}" == 1 ]
then
  export PYTHONPATH=$(pwd)
  (py.test -v test || true)
fi


# %py3_install



%files -n python-%{srcname}
%doc 32bit/README.rst
# %license is not recogized by RPM 3.0.5
# %license COPYING
%doc 32bit/COPYING
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info
%{python_sitelib64}/%{srcname}/
%{python_sitelib64}/%{srcname}*.egg-info


# %files -n python3-%{srcname}
# %doc README.rst
# %license is not recogized by RPM 3.0.5
# %license COPYING
# %doc COPYING
# %{python3_sitelib}/%{srcname}/
# %{python3_sitelib}/%{srcname}*.egg-info
# %{python3_sitelib64}/%{srcname}/
# %{python3_sitelib64}/%{srcname}*.egg-info
# %{python3_sitearch}/%{srcname}*.egg-info


%changelog
* Fri May 19 2017 Michael Wilson <michael.a.wilson@atos.com> - 0.4.8-1
- Initial version 0.4.8

