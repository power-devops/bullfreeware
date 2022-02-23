# ATTENTION !!!
# These versions must be taken from the output of a first build (or from a build on Linux/x86_64) !!!
%define libgpgme_version 11
%define libgpgmepp_version 6
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

# RPM macro set to /usr/bin/bzip2 and the symlink has been removed
%define __bzip2 /opt/freeware/bin/bzip2

%define _libdir64 %{_prefix}/lib64

Name:           gpgme
Version: 1.16.0
Release: 2
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
Patch5:      gpgme-1.16.0-configure.patch

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

Provides:   gpgme-pp = %{version}-%{release}
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


%package -n python%{python_version}-gpg
Summary:    %{name} bindings for Python 3
Group:      Development/Libraries

BuildRequires:  python3-devel
Requires:       python%{python_version}(abi) = %{python_version}
Requires:       %{name} = %{version}-%{release}

%description -n python%{python_version}-gpg
%{name} bindings for Python 3.

%package -n python3-gpg
Summary:    %{name} bindings for Python 3
Group:      Development/Libraries

Requires:   python%{python_version}-gpg = %{version}-%{release}
Requires:   python(abi) = %{python_version}

%description -n python3-gpg
%{name} bindings for Python 3.


%prep
%autosetup -p1

# From Fedora 33 - is it needed on AIX ?
# The build machinery does not support Python 3.9+ yet
# https://github.com/gpg/gpgme/pull/4

# Hack for absence of getopt.h on AIX - getopt(), etc are in unistd.h
# Use compat-getopt-devel for getopt.h      cp /usr/include/unistd.h ./getopt.h

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

# Required by swig with Python 3.8 when building 'gpg._gpgme' extension
ulimit -d unlimited

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
set -x 
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
export ENABLE="cpp,python"
export PYTHON=%{__python}
else  # 32bit
export CFLAGS="$CFLAGS -D_LARGE_FILES"
export CC="${CC32}   $CFLAGS"
export CXX="${CXX32} $CFLAGS"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib:/opt/freeware/src/packages/BUILD/%{name}-%{version}/${OBJECT_MODE}bit/src/.libs"
# No python build for 32 bits
export ENABLE="cpp"
unset PYTHON
fi


export PYTHON=%{__python}
export PYTHONS=$PYTHON

./configure LDFLAGS="$LDFLAGS" \
            PYTHON="${PYTHON}" \
            CC="${CC}" \
            CXX="${CXX}" \
            -v \
            --prefix=%{_prefix} \
            --infodir=%{_infodir} \
            --disable-static \
            --disable-silent-rules \
            --enable-languages="$ENABLE"

TRACE="--trace VERBOSE=1"
TRACE=""
gmake $TRACE %{?_smp_mflags}

cd ..
}

# First build the 64-bit version
build_gpgme 64

build_gpgme 32


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
dump -X${OBJECT_MODE} -Hv $BUILD/%{name}-%{version}/${OBJECT_MODE}bit/lang/python/python*-gpg/lib.aix-*/gpg/_gpgme*.so | grep -q libgpgme.so.%{libgpgme_version}
(gmake check || true)
cd ..

export OBJECT_MODE=32
export CFLAGS="$CFLAGS -D_LARGE_FILES"
cd ${OBJECT_MODE}bit
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


%files -n python3-gpg
%defattr(-,root,system)

%files -n python%{python_version}-gpg
%defattr(-,root,system)
# %doc 32bit/lang/python/README
%{python_sitearch64}/gpg-*.egg-info
%{python_sitearch64}/gpg/


%changelog
* Mon Nov 29 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 1.16.0-2
- Remove support of python2
- Remove 32 bits support of python3
- Add python metapackage

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

