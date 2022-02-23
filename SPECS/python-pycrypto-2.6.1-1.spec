%define name python-pycrypto
%define srcname pycrypto
%define version 2.6.1
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


Summary: Cryptographic modules for Python
Name: %{name}
Version: %{version}
Release: %{release}
# Mostly Public Domain apart from parts of HMAC.py & setup.py, which are Python
License:  Public Domain and Python
Group: Development/Libraries
URL: http://www.pycrypto.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

# Source0: %{srcname}-%{version}.tar.gz
Source0:        http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

# Patch0: %{srcname}-%{version}-aix.patch
Patch0:         pycrypto-2.6-aix.patch
Patch1:         python-crypto-2.4-optflags.patch
Patch2:         python-crypto-2.4-fix-pubkey-size-divisions.patch
Patch3:         pycrypto-2.6.1-CVE-2013-7459.patch
Patch4:         pycrypto-2.6.1-unbundle-libtomcrypt.patch


BuildRequires:  coreutils
# BuildRequires:  findutils
BuildRequires:  python, python-devel
BuildRequires:  gmp-devel >= 4.1
BuildRequires:  gmp
# BuildRequires:  libtomcrypt-devel >= 1.16
BuildRequires:  python-tools

Provides:       pycrypto = %{version}-%{release}
%{?python_provide:%python_provide python-pycrypto}

%description
PyCrypto is a collection of both secure hash functions (such as MD5 and SHA), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.).

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
%setup -q -n %{srcname}-%{version}

echo "dotests=%{dotests}
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"

%patch0 -p1 -b .aix

# Use distribution compiler flags rather than upstream's
# These are perhaps Fedora specific
# %patch1 -p1

# Fix divisions within benchmarking suite:
%patch2 -p1

# AES.new with invalid parameter crashes python
# https://github.com/dlitz/pycrypto/issues/176
# CVE-2013-7459
%patch3 -p1

# Unbundle libtomcrypt
# This may not be appropriate for AIX - TBC
# rm -rf src/libtom
# %patch4

# setup.py doesn't run 2to3 on pct-speedtest.py
# This may be required, linked to python2/3 diffs ? - TBC
# cp pct-speedtest.py pct-speedtest3.py
# 2to3 -wn pct-speedtest3.py



# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# Autoconf and RPL_MALLOC
export ac_cv_func_malloc_0_nonnull=yes

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

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


# May require -fno-strict-aliasing  - TBC
# %global optflags %{optflags} -fno-strict-aliasing
# A python3 build is not yet supported
# %py2_build
# %py3_build


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


%install

# Probably not needed
export AR="/usr/bin/ar -X32_64"

# A python3 build/install is not yet supported
# %py2_install
# %py3_install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
/opt/freeware/bin/python2.7_64 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7_64 setup.py test || true)
fi

cd ../32bit
/opt/freeware/bin/python2.7 setup.py install --skip-build --root ${RPM_BUILD_ROOT}

# Tests and a python3 build are not yet supported
# and RPM 3.0.5 does not accept %check
# %check
# %{__python2} setup.py test
# %{__python3} setup.py test

# Benchmark tests - TBC
#PYTHONPATH=%{buildroot}%{python2_sitearch} %{__python2} pct-speedtest.py
#PYTHONPATH=%{buildroot}%{python3_sitearch} %{__python3} pct-speedtest3.py

if [ "%{dotests}" == 1 ]
then
  (/opt/freeware/bin/python2.7 setup.py test || true)
fi




%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
# RPM 3.0.5 does not accept %license
# %license COPYRIGHT LEGAL/
%doc 32bit/ACKS 32bit/COPYRIGHT 32bit/ChangeLog 32bit/LEGAL/ 32bit/PKG-INFO 32bit/README 32bit/TODO 32bit/Doc/
%doc 32bit/Doc 
%{python_sitelib}/*
%{python_sitelib64}/*

%changelog
* Fri Feb 03 2017 Michael Wilson <michael.a.wilson@atos.net> - 2.6.1-1
- New version 2.6.1 and Fedora inspired changes

* Fri Feb 03 2017 Michael Wilson <michael.a.wilson@atos.net> - 2.6-2
- Corrections for compiler options and build GCC/XLC

* Thu Jul 17 2013 Tristan Delhalle <Tristan.Delhalle@ext.bull.net> - 2.6-1
- first version for AIX V6.1 and higher
