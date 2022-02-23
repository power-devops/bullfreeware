# ATTENTION !!!
# These versions must be taken from the output of a first build (or from a build on Linux/x86_64) !!!
%define libgpgme_version 11
%define libgpgme_fullversion 11.24.1
%define libgpgmepp_version 6
%define libgpgmepp_fullversion 6.12.1
# The full version is significant as each new version of libgpgme adds symbols

%define _smp_mflags -j4

%global gnupg2_min_ver 2.2.24
%global libgpg_error_min_ver 1.36

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# By default, Python 2 is no longer built, unless it it installed already
# To build Python 2 : rpmbuild -ba --with python2 *.spec
%bcond_with python2

# RPM macro set to /usr/bin/bzip2 and the symlink has been removed
%define __bzip2 /opt/freeware/bin/bzip2


# Needs care because default command python may be linked to 32 or 64 bit python
# and compiler/loader options are not the same, e.g. -maix32/-maix64
# Also there is only 1 python in /usr/bin, usually 64 bit version :
#
# /usr/bin/python now links to /opt/freeware/bin/python
#                                                -> python2
#                                                -> python2_64
# And :
#
#     /opt/freeware/bin/python_64 -> python2_64 -> python2.7_64
#     /opt/freeware/bin/python_32 -> python2_32  -> python2.7_32
#
# So, use /opt/freeware/bin/python2.7_32 and /opt/freeware/bin/python2.7_64

# Also, this package builds Python3 bindings and Python3 is installed
# This will lead to confusion over which is the Primary Python version, e.g.
# symlink /opt/freeware/bin/python may/will point to Python3 AND 64 bit version
#
#      use /opt/freeware/bin/python3.8_32 and /opt/freeware/bin/python3.8_64

%define is_python2 %(test -e /opt/freeware/bin/python2.7_32 && echo 1 || echo 0)
%if %{is_python2}
%define python_sitelib %(/opt/freeware/bin/python2.7_32 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
BuildRequires:  python, python-devel
%endif


%define is_python2_64 %(test -e /opt/freeware/bin/python2.7_64 && echo 1 || echo 0)
%if %{is_python2_64}
%define python_sitelib64 %(/opt/freeware/bin/python2.7_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

# And similar for python3 may be required

# Test for Python 3.8, also python3 may point to 64 bit version

%define is_python3 %(test -e /opt/freeware/bin/python3.8_32 && echo 1 || echo 0)
%if %{is_python3}
%define python3_sitelib %(/opt/freeware/bin/python3.8_32 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%endif

%define is_python3_64 %(test -e /opt/freeware/bin/python3.8_64 && echo 1 || echo 0)
%if %{is_python3_64}
%define python3_sitelib64 %(/opt/freeware/bin/python3.8_64 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%endif

%define _libdir64 %{_prefix}/lib64

Name:           gpgme
Version: 1.16.0
Release: 1
Summary:        GnuPG Made Easy - high level crypto API
Group:          System Environment/Libraries

License:        LGPLv2+
URL:            https://gnupg.org/related_software/gpgme/
Source0:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Source1:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-%{version}.tar.bz2.sig
Source2:        gpgme-multilib.h

Source10: %{name}-%{version}-%{release}.build.log

Patch1:      gpgme-remove-library-for-linking.patch
Patch2:      gpgme-1.3.2-largefile.patch
Patch3:      gpgme-bad-test-ax_python_devel.patch
Patch4:      gpgme-No-local-exec-model-v2.patch

# It seems impossible to configure for 32 bit Pythons without changing symlinks
Patch5:      gpgme-1.14.0-32bit-pythons.patch

BuildRequires:  gcc
BuildRequires:  gnupg2 >= %{gnupg2_min_ver}
# Only need gnupg2-smime to build gpgsm, but it was never built/available on AIX
# BuildRequires:  gnupg2-smime
BuildRequires:  libgpg-error-devel >= %{libgpg_error_min_ver}
BuildRequires:  libassuan-devel >= 2.4.2

BuildRequires:  sed
BuildRequires:  bzip2 >= 1.0.8
# Replace W/A copy of unistd.h to getopt.h - getopt_long() is not called ?
BuildRequires:  compat-getopt-devel

# For python
BuildRequires:  swig
# No more python2
# As Python 2 is installed the configure/build tries to build the binding, need
#	BuildRequires:  python-devel >= 2.7.17-3

Requires:  gnupg2 >= %{gnupg2_min_ver}


%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

The library is available as 32-bit and 64-bit.

%if %{with gcc_compiler}
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary:   Development headers and libraries for gpgme
Group:     Development/Libraries
# BuildArch: ppc

Requires:  %{name} = %{version}-%{release}
Requires:  libgpg-error-devel >= %{libgpg_error_min_ver}

%description devel
Development headers and libraries for gpgme.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%package -n %{name}pp
Summary:    C++ bindings/wrapper for GPGME
Group:      Development/Libraries

Provides:   gpgme-pp = {version}-%{release}
Requires:   %{name} = %{version}-%{release}

%description -n %{name}pp
C++ bindings/wrapper for GPGME.


%package -n %{name}pp-devel
Summary:    Development libraries and header files for %{name}-pp
Group:      Development/Libraries

Provides:   gpgme-pp-devel = %{version}-%{release}
Requires:   %{name}pp = %{version}-%{release}
Requires:   %{name}-devel

# For automatic provides
# BuildRequires:  cmake

%description -n %{name}pp-devel
Development libraries and header files for %{name}-pp


# %package -n q%{name}
# Summary:    Qt API bindings/wrapper for GPGME
# Group:      Development/Libraries
# 
# Requires:   %{name}pp = %{version}-%{release}
# BuildRequires:  pkgconfig(Qt5Core)
# BuildRequires:  pkgconfig(Qt5Test)
# 
# %description -n q%{name}
# Qt API bindings/wrapper for GPGME.


# %package -n q%{name}-devel
# Summary:    Development libraries and header files for %{name}
# Group:      Development/Libraries
# 
# Requires:   q%{name} = %{version}-%{release}
# Requires:   %{name}pp-devel%{?_isa}

# For automatic provides
# BuildRequires:  cmake

# %description -n q%{name}-devel
# Development libraries and header files for %{name}.


# Python 2 error in python2.7/_sysconfigdata.py & python2.7/config/Makefile
#   calling /usr/bin/gcc due to CC/CXX set to /usr/bin/gcc in spec file
# W/A by creating symlink /usr/bin/gcc not required if python >= 2.7.17-3
#
# But Python 2 binding will be removed next/this version

%if %{with python2}
%package -n python2-gpg
Summary:    %{name} bindings for Python 2
Group:      Development/Libraries

Provides:   python2-gpg
# BuildRequires:  python2-devel  How could this work before  - there was/is none
BuildRequires:  python-devel >= 2.7.17-3
Requires:       %{name} = %{version}-%{release}

%description -n python2-gpg
%{name} bindings for Python 2.
%endif


%package -n python3-gpg
Summary:    %{name} bindings for Python 3
Group:      Development/Libraries

Provides:   python3-gpg
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}

%description -n python3-gpg
%{name} bindings for Python 3.


%prep

# Have to apply patch5 to 32bit only
# %%autosetup -p1

%setup -q

%patch1 -p1 -b .removelib
%patch2 -p1 -b .largefile
%patch3 -p1 -b .badtest
%patch4 -p1 -b .No-local-exec-model-v2

# From Fedora 33 - is it needed on AIX ?
# The build machinery does not support Python 3.9+ yet
# https://github.com/gpg/gpgme/pull/4
# Pb no macro python3_version -  sed -i 's/3.8/%{python3_version}/g' configure

# Hack for absence of getopt.h on AIX - getopt(), etc are in unistd.h
# Use compat-getopt-devel for getopt.h      cp /usr/include/unistd.h ./getopt.h

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%if %{is_python2}
cd 32bit
%patch5 -p1 -b .32bit-pythons
%endif


%build

# Required by swig with Python 3.8 when building 'gpg._gpgme' extension
ulimit -d unlimited

export PYTHON2_VERSION="2.7"
export PYTHON3_VERSION=`python3 --version | awk '{print $2}' | awk -F. '{print $1 "." $2}'`

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{with gcc_compiler}

# binutils not installed, must use AIX nm - export NM="/opt/freeware/bin/nm"
export NM="/usr/bin/nm -X32_64"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export CXX__="/usr/vacpp/bin/xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif   # gcc_compiler

type $CC__
type $CXX__

export CC32="  ${CC__}  ${FLAG32}"
export CXX32=" ${CXX__} ${FLAG32}"
export CC64="  ${CC__}  ${FLAG64}"
export CXX64=" ${CXX__} ${FLAG64}"

# -pthread is required for multi-threading (tests thread1)
# tls-model is required for Python tests
CFLAGS="-ftls-model=global-dynamic -pthread"

build_gpgme ()
{
export OBJECT_MODE=$1
cd ${OBJECT_MODE}bit
export LIBS=" -lm "

# PATH: /opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs
#   is required for running the Python tests.
# Otherwise, gpgme must be installed in order to be able to run the Python tests.

# Hack for pb in Python _sysconfigdata.py with line :
# LINKFORSHARED: '-Wl,-bE:Modules/python.exp -lld'

if [ ${OBJECT_MODE} -eq 64 ]
then
export CFLAGS
export CC="${CC64}   $CFLAGS"
export CXX="${CXX64} $CFLAGS"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib:/opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs"
else  # 32bit
export CFLAGS="$CFLAGS -D_LARGE_FILES"
export CC="${CC32}   $CFLAGS"
export CXX="${CXX32} $CFLAGS"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib:/opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs"
fi

# Issue Python 2 in  _sysconfigdata.py calling ld_so_aix /usr/bin/gcc
# But needed for configure  !?
mkdir Modules
ln -s /opt/freeware/lib64/python${PYTHON2_VERSION}/config/python.exp Modules/python.exp

%if %{with python2}
export PYTHON="/opt/freeware/bin/python${PYTHON2_VERSION}_64"
export PYTHONS="/opt/freeware/bin/python${PYTHON2_VERSION}_64 /opt/freeware/bin/python${PYTHON3_VERSION}_64"
%else
export PYTHON="/opt/freeware/bin/python${PYTHON3_VERSION}_64"
export PYTHONS="/opt/freeware/bin/python${PYTHON3_VERSION}_64"
%endif

./configure LDFLAGS="$LDFLAGS" \
            PYTHON="${PYTHON}" \
            PYTHONS="${PYTHONS}" \
            CC="${CC}" \
            CXX="${CXX}" \
            -v \
            --prefix=%{_prefix} \
             --infodir=%{_infodir} \
            --disable-static \
            --disable-silent-rules \
            --enable-languages=cpp,python

TRACE="--trace VERBOSE=1"
TRACE=""
gmake $TRACE %{?_smp_mflags}

cd ..
}

# First build the 64-bit version
build_gpgme 64

# Build the 32-bit version
# Be sure Python 32bit is called!
for p in `find 32bit -name "*.py"`
do
   /opt/freeware/bin/sed -i -e "s|#!/usr/bin/env python3|#!/usr/bin/env python3_32|" \
                            -e "s|#!/usr/bin/env python|#!/usr/bin/env python3_32|"     $p
done

build_gpgme 32

# There is a bug somewhere, probalbly in the configure, that generates:
#   python2_32 and python3_32
# instead of:
#   python2.7_32 and python3.N_32  (N=8 for now...)
# in files:
#   lang/python/Makefile
#   lang/python/Makefile.in
#      PYTHON = /opt/freeware/bin/python2_32
#      PYTHONS = /opt/freeware/bin/python2_32 /opt/freeware/bin/python3_32
# and only in 32bit.
# This generates an issue when running the lang/python tests,
# since directories are named:
#   lang/python/python2_32-gpg
#   lang/python/python3_32-gpg
# instead of:
#   lang/python/python2.7-gpg
#   lang/python/python3.8-gpg
# and thus Python tests are not run
for m in 32bit/lang/python/Makefile 32bit/lang/python/Makefile.in
do
   /opt/freeware/bin/sed -i -e "s/python2_32/python${PYTHON2_VERSION}_32/g" -e "s/python3_32/python${PYTHON3_VERSION}_32/g" $m
done


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Required here too now for "swigging python"
ulimit -d unlimited

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib:/opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs"

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"

# Move libs (and Python 2) files from lib to lib64
# Python 3 files appear to be already in lib64 (default python3 is 64 bit)
mv  ${RPM_BUILD_ROOT}/%{_libdir}/*  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
export OBJECT_MODE=32
# Defining again LDFLAGS with the libpath is required so that 32bit Python tests can find libgpgme.a
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib:/opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs"

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"

# Create lib64 symlinks
rm                        ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.a
ln -s ../lib/libgpgme.a   ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.a
rm                        ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.a
ln -s ../lib/libgpgmepp.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.a

cd ..

# Add 64bit .so to 32bit in lib*.a
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.a     64bit/src/.libs/libgpgme.so.%{libgpgme_version}
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.a   64bit/lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version}

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info-1
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info-2

rm -fv ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -fv ${RPM_BUILD_ROOT}%{_libdir}/lib*.la


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

ulimit -d unlimited

# v1.15.1: there are 26 + 3 + 9 + 0 + 3 tests + the 56 Python tests
#   grep "tests passed"  gpgme-1.15.1-2.spec.res_...
#   grep "tests run"     gpgme-1.15.1-2.spec.res_...  : Python tests

CFLAGS="-ftls-model=global-dynamic -pthread"

export OBJECT_MODE=64
export CFLAGS
cd ${OBJECT_MODE}bit
# Check PATH for: libgpgme.a(libgpgme.so.11)
dump -X${OBJECT_MODE} -Hv $BUILD/%{name}-%{version}/${OBJECT_MODE}bit/lang/python/python*-gpg/lib.aix-*/gpg/_gpgme.so
  (gmake check || true)

cd ..

export OBJECT_MODE=32
export CFLAGS="$CFLAGS -D_LARGE_FILES"
cd ${OBJECT_MODE}bit
# Check PATH for: libgpgme.a(libgpgme.so.11)
dump -X${OBJECT_MODE} -Hv $BUILD/%{name}-%{version}/${OBJECT_MODE}bit/lang/python/python*-gpg/lib.aix-*/gpg/_gpgme.so
# Fix the issue with python*-gpg directory names
for f in `find . -name "*-gpg" | grep -v "temp.aix"`
do
        f2=`echo $f | sed -e"s/_32//g"`
        echo $f " --> " $f2
	mv $f $f2
	d=`dirname $f`
	b=`basename $f`
	b2=`basename $f2`
	(
	  cd $d
	  ln -sf $b2 $b
	)
done
for f in `find . -name "*-gpg" | grep "temp.aix"`
do
        f2=`echo $f | sed -e"s/_32//g"`
        echo $f " --> " $f2
	mv $f $f2
	d=`dirname $f`
	b=`basename $f`
	b2=`basename $f2`
	(
	  cd $d
	  ln -sf $b2 $b
	)
done
export PYTHON2_VERSION="2.7"
export PYTHON3_VERSION=`python3 --version | awk '{print $2}' | awk -F. '{print $1 "." $2}'`
for m in lang/python/tests/Makefile
do
   /opt/freeware/bin/sed -i -e "s/python${PYTHON2_VERSION}/python${PYTHON2_VERSION}_32/g" -e "s/python${PYTHON3_VERSION}/python${PYTHON3_VERSION}_32/g" $m
done
  (gmake check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/COPYING*
%doc 32bit/AUTHORS 32bit/NEWS 32bit/README*
%{_bindir}/%{name}-json
%{_libdir}/lib%{name}.a
%{_libdir64}/lib%{name}.a


%files devel
%defattr(-,root,system)
%{_bindir}/%{name}-config
%{_bindir}/%{name}-tool
%{_includedir}/%{name}.h
%{_datadir}/aclocal/%{name}.m4
%{_infodir}/%{name}.info*


%files -n %{name}pp
%defattr(-,root,system)
%doc 32bit/lang/cpp/README
%{_libdir}/lib%{name}pp.a*
%{_libdir64}/lib%{name}pp.a*


%files -n %{name}pp-devel
%defattr(-,root,system)
%{_includedir}/%{name}++/
%{_libdir}/cmake/Gpgmepp/
%{_libdir64}/cmake/Gpgmepp/


# %files -n q%{name}
# %defattr(-,root,system)
# %doc 32bit/lang/qt/README


# %files -n q%{name}-devel
# %defattr(-,root,system)
# %{_includedir}/q%{name}/
# %{_includedir}/QGpgME/
# %{_libdir}/libq%{name}.so
# %{_libdir}/cmake/QGpgme/
# %{_libdir64}/libq%{name}.so
# %{_libdir64}/cmake/QGpgme/


%if %{with python2}
%files -n python2-gpg
%defattr(-,root,system)
%doc 32bit/lang/python/README
%{python_sitelib}/gpg-*.egg-info
%{python_sitelib}/gpg/
%{python_sitelib64}/gpg-*.egg-info
%{python_sitelib64}/gpg/
%endif


%files -n python3-gpg
%defattr(-,root,system)
# %doc 32bit/lang/python/README
%{python3_sitelib}/gpg-*.egg-info
%{python3_sitelib}/gpg/
%{python3_sitelib64}/gpg-*.egg-info
%{python3_sitelib64}/gpg/


%changelog
* Wed Jul 21 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16.0-1
- Update to 1.16.0

* Thu Jun 24 2021 Tony Reix <tony.reix@atos.com> - 1.15.1-3
- BullFreeware Compatibility Improvements

* Tue Jun 15 2021 Tony Reix <tony.reix@atos.com> - 1.15.1-2
- Add -pthread and use a new libgpg-error asking for -pthread

* Mon Jun 14 2021 Tony Reix <tony.reix@atos.com> - 1.15.1-1
- Updated to version 1.15.1
- Add: ulimit -d unlimited  for swig & Python 3.8 in %build

* Fri Oct 16 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.14.0-1
- Updated to version 1.14.0
- Python 2 binding no longer built/provided by default
- Replace W/A copy of unistd.h to getopt.h by BuildRequires: compat-getopt-devel

* Tue Oct 06 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.11.1-3
- Rebuild on laurel2 and RPM version 4
- W/A Python 2 pb in python2.7/_sysconfigdata.py & python2.7/config/Makefile
-   calling /usr/bin/gcc due to CC/CXX set to /usr/bin/gcc in spec file
- Patch added to force 32 bit python2/python3 in 32bit build

* Wed Dec 05 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.11.1-2
- Correction for TLS __thread type as AIX has no local-exec model
-    for thread-local storage (src/debug.c)

* Mon Oct 01 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.11.1-1
- Initial version 1.11.1

