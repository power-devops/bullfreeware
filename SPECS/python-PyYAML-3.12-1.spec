%define name python-PyYAML
%define srcname PyYAML
%define version 3.12
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# Configure tests for gcc first, so default is GCC if installed on the machine
# To force gcc : --define 'gcc_compiler=x'
# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}

# Needs care because default command python may be linked to 32 or 64 bit python
# Also, although
#     /usr/bin/python_64 eventually links to /opt/freeware/bin/python2.7_64
#     /usr/bin/python_32 links to inexistant /opt/freeware/bin/python2_32
# So, use /opt/freeware/bin/python2.7 and /opt/freeware/bin/python2.7_64

%define is_python %(test -e /usr/bin/python && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")
%endif

%define _libdir64 %{_prefix}/lib64

%define is_python_64 %(test -e /usr/bin/python_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

Summary: YAML parser and emitter for Python
Name: %{name}
Version: %{version}
Release: %{release}
Source0:  http://pyyaml.org/download/pyyaml/%{srcname}-%{version}.tar.gz
Url: http://pyyaml.org
License: MIT
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: python >= 2.4
BuildRequires: python-devel >= 2.4
# setuptools may have already been installed using command pip
# BuildRequires: python-setuptools
BuildRequires: libyaml-devel

Provides:       python-yaml = %{version}-%{release}
Provides:       python-yaml%{?_isa} = %{version}-%{release}


%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  PyYAML is a YAML parser and
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
%setup -q -n %{srcname}-%{version}
chmod a-x examples/yaml-highlight/yaml_hl.py

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build

# Display build environment and currently installed RPM packages
/usr/bin/env
rpm -qa

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"


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
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


cd 64bit

export CC="${CC64} "
export OBJECT_MODE=64
# export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -lyaml"

#python_64 setup.py --with-libyaml build_ext
/opt/freeware/bin/python2.7_64 setup.py --with-libyaml build

cd ../32bit

export CC="${CC32} "
export OBJECT_MODE=32
# export LDFLAGS="-L/opt/freeware/lib -lyaml"

#python setup.py --with-libyaml build_ext
/opt/freeware/bin/python2.7 setup.py --with-libyaml build

%install

export AR="/usr/bin/ar -X32_64"

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 setup.py test || true)
fi


cd ../32bit
/opt/freeware/bin/python2.7 setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}


#%check
#python_32 setup.py test
if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 setup.py test || true)
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/CHANGES 32bit/PKG-INFO  32bit/README  32bit/examples 
%{python_sitelib}/*
%{python_sitelib64}/_yaml.so

%changelog
* Tue Mar 28 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.12-1
- Update to version 3.12

* Mon Feb 02 2015 Gerard Visiedo <gerard.visiedo@bull.net> - 3.11-2
- Rebuilt with "build" onsted of "build√_ext" compile option

* Thu Oct 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 3.11-1
- first version for AIX V6.1 and higher
