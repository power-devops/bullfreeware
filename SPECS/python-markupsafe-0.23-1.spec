%define name python-markupsafe
%define srcname MarkupSafe
%define version 0.23
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

# Configure tests for gcc first, so default is GCC if installed on the machine
# To force gcc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}


%global with_python3 0

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Implements a XML/HTML/XHTML Markup safe string for Python

Group: Development/Languages
License: BSD
URL: http://pypi.python.org/pypi/MarkupSafe
Source0: http://pypi.python.org/packages/source/M/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: python-devel python-setuptools

# %if 0%{?with_python3}
# BuildRequires: python3-devel python3-setuptools
# %endif # if with_python3


%description
A library for safe markup escaping.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


# %if 0%{?with_python3}
# %package -n python3-markupsafe
# Summary: Implements a XML/HTML/XHTML Markup safe string for Python 3
# Group: Development/Languages
# %{?python_provide:%python_provide python3-markupsafe}

# %description -n python3-markupsafe
# A library for safe markup escaping.
# %endif #if with_python3

%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# A python3 build/install is not yet supported

%build
# %py2_build

# %if 0%{?with_python3}
# %py3_build
# %endif # with_python3

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

export CC32=" ${CC__}  ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"


# First build the 64-bit version
cd 64bit
export CC="${CC64} "
export OBJECT_MODE=64
/opt/freeware/bin/python2.7_64 setup.py build


# Build the 32-bit version
cd ../32bit
export CC="${CC32} "
export OBJECT_MODE=32
/opt/freeware/bin/python2.7 setup.py build


# A python3 build/install is not yet supported
%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# %py2_install
# C code errantly gets installed
# rm $RPM_BUILD_ROOT/%{python2_sitearch}/markupsafe/*.c

# %if 0%{?with_python3}
# %py3_install
# %endif # with_python3
# C code errantly gets installed
# rm $RPM_BUILD_ROOT/%{python3_sitearch}/markupsafe/*.c


cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# C source file  _speedups.c is installed by error
rm $RPM_BUILD_ROOT/%{python_sitelib64}/markupsafe/*.c

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 setup.py test || true)
fi


cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# C source file  _speedups.c is installed by error
rm $RPM_BUILD_ROOT/%{python_sitelib}/markupsafe/*.c

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 setup.py test || true)
fi



# A python3 build/install is not yet supported
# and RPM 3.0.5 does not accept %check

# %check

# %{__python2} setup.py test

# %if 0%{?with_python3}
# %{__python3} setup.py test
# %endif # with_python3


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files -n python-markupsafe
# %license LICENSE
%doc 32bit/AUTHORS 32bit/LICENSE 32bit/PKG-INFO 32bit/README.rst
%{python_sitelib}/*
%{python_sitelib64}/*

# %if 0%{?with_python3}
# %files -n python3-markupsafe
# %doc AUTHORS LICENSE README.rst
# %{python3_sitearch}/*
# %endif # with_python3


%changelog
* Thu Apr 20 2017 Michael Wilson <michael.a.wilson@atos.net> - 0.23-1
- Update to version 0.23 (version 1.0 dispo, but not on Fedora, nor download)

* Thu Jul 1 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 0.18-1
- first version for AIX V6.1 and higher

