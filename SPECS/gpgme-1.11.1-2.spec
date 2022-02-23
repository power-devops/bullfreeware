%define libgpgme_version 11
%define libgpgme_fullversion 11.17.0
%define libgpgmepp_version 6
%define libgpgmepp_fullversion 6.3.0
# The full version is significant as each new version of libgpgme adds symbols

%define name gpgme
%define srcname gpgme
%define version 1.11.1
%define release 2

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

# Also, this package builds Python3 bindings and Python3 is installed
# This will lead to confusion over which is the Primary Python version, e.g.
# symlink /opt/freeware/bin/python may/will point to Python3 AND 64 bit version
#
# So, use /opt/freeware/bin/python3.5_32 and /opt/freeware/bin/python3.5_64
#      or /opt/freeware/bin/python3.6_32 and /opt/freeware/bin/python3.6_64

%define is_python %(test -e /opt/freeware/bin/python2.7 && echo 1 || echo 0)
%if %{is_python}
%define python_sitelib %(/opt/freeware/bin/python2.7 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif


%define is_python_64 %(test -e /opt/freeware/bin/python2.7_64 && echo 1 || echo 0)
%if %{is_python_64}
%define python_sitelib64 %(/opt/freeware/bin/python2.7_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

# And similar for python3 may be required

# Test for Python 3.5 and 3.6, also python3 may point to 64 bit version

%define is_python3 %(test -e /opt/freeware/bin/python3.5_32 && echo 1 || echo 0)
%if %{is_python3}
%define python3_sitelib %(/opt/freeware/bin/python3.5_32 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%else

%define is_python3 %(test -e /opt/freeware/bin/python3.6_32 && echo 1 || echo 0)
%if %{is_python3}
%define python3_sitelib %(/opt/freeware/bin/python3.6_32 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%endif

%endif



%define is_python3_64 %(test -e /opt/freeware/bin/python3.5_64 && echo 1 || echo 0)
%if %{is_python3_64}
%define python3_sitelib64 %(/opt/freeware/bin/python3.5_64 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%else

%define is_python3_64 %(test -e /opt/freeware/bin/python3.6_64 && echo 1 || echo 0)
%if %{is_python3_64}
%define python3_sitelib64 %(/opt/freeware/bin/python3.6_64 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%endif

%endif




%define _libdir64 %{_prefix}/lib64


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        GnuPG Made Easy - high level crypto API
Group:          System Environment/Libraries
BuildArch:      ppc

License:        LGPLv2+
URL:            https://gnupg.org/related_software/gpgme/
Source0:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-1.11.1.tar.bz2
Source1:        https://gnupg.org/ftp/gcrypt/gpgme/gpgme-1.11.1.tar.bz2.sig
Source2:        gpgme-multilib.h

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

Patch1:      gpgme-remove-library-for-linking.patch
Patch2:      gpgme-1.3.2-largefile.patch
Patch3:      gpgme-bad-test-ax_python_devel.patch
Patch4:      gpgme-No-local-exec-model.patch

BuildRequires:  gcc
BuildRequires:  gnupg2 >= 2.1.13
BuildRequires:  gnupg2-smime
BuildRequires:  libgpg-error-devel >= 1.24
BuildRequires:  libassuan-devel >= 2.4.2

# For python
# BuildRequires:  swig

Requires:  gnupg2 >= 2.1.13


%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary:   Development headers and libraries for gpgme
Group:     Development/Libraries
BuildArch: ppc

Requires:  %{name} = %{version}-%{release}
Requires:  libgpg-error-devel >= 1.24


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



%package -n python2-gpg
Summary:    %{name} bindings for Python 2
Group:      Development/Libraries

Provides:   python2-gpg
BuildRequires:  python2-devel
Requires:       %{name} = %{version}-%{release}

%description -n python2-gpg
%{name} bindings for Python 2.



%package -n python3-gpg
Summary:    %{name} bindings for Python 3
Group:      Development/Libraries

Provides:   python3-gpg
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}

%description -n python3-gpg
%{name} bindings for Python 3.





%prep
# %autosetup not recognized by RPM 3.0.5

%setup -q

%patch1 -p1 -b .removelib
%patch2 -p1 -b .largefile
%patch3 -p1 -b .badtest
%patch4 -p1 -b .No-local-exec-model


echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif


# Hack for absence of getopt.h on AIX - getopt(), etc are in unistd.h
cp /usr/include/unistd.h ./getopt.h

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

/usr/bin/env | /usr/bin/sort

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/opt/freeware/bin/nm"
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

%endif

type $CC__
type $CXX__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"
export CXX32=" ${CXX__}  ${FLAG32} -D_LARGE_FILES"
export CXX64=" ${CXX__}  ${FLAG64} -D_LARGE_FILES"


# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64}   $GLOBAL_CC_OPTIONS"
export LIBS=" -lm "
export LDFLAGS=" -L/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

# Hack for pb in Python _sysconfigdata.py with line :
# LINKFORSHARED: '-Wl,-bE:Modules/python.exp -lld'
mkdir Modules
ln -s /opt/freeware/lib64/python2.7/config/python.exp Modules/python.exp

# Have to use the 64 bit version of python2.7, 32 bit is often the default
# export PYTHON=python_64
# export PYTHONS='/opt/freeware/bin/python2_64 /opt/freeware/bin/python3_64'

#            --enable-languages=cpp,qt,python

#./autogen.sh

# Link for python3 is to 64 bit version, but python2 is to 32 bit version
ln -sf python2.7_64 /opt/freeware/bin/python2

./configure LDFLAGS=" -L/opt/freeware/lib64:/opt/freeware/lib:/usr/lib" \
             -v --prefix=%{_prefix} \
             --infodir=%{_infodir} \
            --disable-static \
            --disable-silent-rules \
            --enable-languages=cpp,python

gmake %{?_smp_mflags}

# Restore correct link for python2 to 32 bit version
ln -sf python2.7 /opt/freeware/bin/python2



# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32}   $GLOBAL_CC_OPTIONS"
export LIBS=" -lm "
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib:/usr/lib"

# Hack for pb in Python _sysconfigdata.py with line :
# LINKFORSHARED: '-Wl,-bE:Modules/python.exp -lld'
mkdir Modules
ln -s /opt/freeware/lib/python2.7/config/python.exp Modules/python.exp

# Have to use the 32 bit version of python2.7, the default may be 64 bit
# export PYTHON=python_32
# export PYTHONS='/opt/freeware/bin/python2.7 /opt/freeware/bin/python3_32'

#            --enable-languages=cpp,qt,python

#./autogen.sh

# Link for python3 is to 64 bit version, but python2 is to 32 bit version
%if %{is_python3}
ln -sf python3_32 /opt/freeware/bin/python3
%endif

./configure PYTHON_VERSION=2.7_32 LDFLAGS=" -Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib:/usr/lib" \
             -v --prefix=%{_prefix} \
             --infodir=%{_infodir} \
            --disable-static \
            --disable-silent-rules \
            --enable-languages=cpp,python

gmake %{?_smp_mflags}

# Restore correct link for python3 to 64 bit version
%if %{is_python3}
ln -sf python3_64 /opt/freeware/bin/python3
%endif




# Archive 64 bit shared object in 32 bit shared library

# slibclean
${AR} -q src/.libs/libgpgme.a ../64bit/src/.libs/libgpgme.so.%{libgpgme_version}
${AR} -q lang/cpp/src/.libs/libgpgmepp.a ../64bit/lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version}

# slibclean

# strip -e -X32_64     src/.libs/libgpgme.so.%{libgpgme_version} ../64bit/src/.libs/libgpgme.so.%{libgpgme_version}
# strip -e -X32_64     lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version} ../64bit/lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version}





%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"


# %check is not recogized by RPM 3.0.5
#%check


# Currently there are 26 tests
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi

# rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

# Move libs and Python 2 files from lib to lib64
# Python 3 files appear to be already in lib64 (default python3 is 64 bit)

mv  ${RPM_BUILD_ROOT}/%{_libdir}/*  ${RPM_BUILD_ROOT}/%{_libdir64}

# Add libgpgme.so.11 and libgpgme.so & .so.11.17.0 - they may be required
# Add libgpgmepp.so.6 and libgpgmepp.so & .so.6.3.0 - they may be required
# mkdir -p    ${RPM_BUILD_ROOT}%{_libdir64}
install -p src/.libs/libgpgme.so.%{libgpgme_version} ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.so.%{libgpgme_version}
ln -sf  libgpgme.so.%{libgpgme_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.so
ln -sf  libgpgme.so.%{libgpgme_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.so.%{libgpgme_fullversion}

install -p lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version} ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.so.%{libgpgmepp_version}
ln -sf  libgpgme.so.%{libgpgmepp_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.so
ln -sf  libgpgme.so.%{libgpgmepp_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.so.%{libgpgmepp_fullversion}

# Following not required, as lib64/libgpgme.a will be symlink to lib/libgpgme.a
# mv ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.a
# mv ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.a





cd ../32bit
export OBJECT_MODE=32

# Link for python3 is to 64 bit version, but python2 is to 32 bit version
%if %{is_python3}
ln -sf python3_32 /opt/freeware/bin/python3
%endif

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"


# Add libgpgme.so.11 and libgpgme.so & .so.11.17.0 - they may be required
# Add libgpgmepp.so.6 and libgpgmepp.so & .so.6.3.0 - they may be required
install -p src/.libs/libgpgme.so.%{libgpgme_version} ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.so.%{libgpgme_version}
ln -sf  libgpgme.so.%{libgpgme_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.so
ln -sf  libgpgme.so.%{libgpgme_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.so.%{libgpgme_fullversion}

install -p lang/cpp/src/.libs/libgpgmepp.so.%{libgpgmepp_version} ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.so.%{libgpgmepp_version}
ln -sf  libgpgmepp.so.%{libgpgmepp_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.so
ln -sf  libgpgmepp.so.%{libgpgmepp_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.so.%{libgpgmepp_fullversion}

# Following is done in case a future version is incompatible
mv    ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.a ${RPM_BUILD_ROOT}%{_libdir}/libgpgme-%{libgpgme_fullversion}.a
ln -s libgpgme-%{libgpgme_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libgpgme.a

# Create lib64/libgpgme.a symlink to lib/libgpgme.a
rm    ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.a
ln -s ../lib/libgpgme.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpgme.a

mv    ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.a ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp-%{libgpgmepp_fullversion}.a
ln -s libgpgmepp-%{libgpgmepp_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libgpgmepp.a

# Create lib64/libgpgmepp.a symlink to lib/libgpgmepp.a
rm    ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.a
ln -s ../lib/libgpgmepp.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpgmepp.a


# Currently there are 26 tests
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi

# rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

# Restore correct link for python3 to 64 bit version
%if %{is_python3}
ln -sf python3_64 /opt/freeware/bin/python3
%endif





%files
%doc 32bit/COPYING*
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/NEWS 32bit/README*
%doc 32bit/THANKS 32bit/TODO 32bit/VERSION
%{_bindir}/%{name}-json
%{_libdir}/lib%{name}.a
# %{_libdir}/lib%{name}-%{libgpgme_fullversion}.a
%{_libdir}/lib%{name}.so.11*
%{_libdir64}/lib%{name}.a
%{_libdir64}/lib%{name}.so.11*


%files devel
%{_bindir}/%{name}-config
%{_bindir}/%{name}-tool
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir64}/lib%{name}.so
%{_datadir}/aclocal/%{name}.m4
%{_infodir}/%{name}.info*


%files -n %{name}pp
%doc 32bit/lang/cpp/README
%{_libdir}/lib%{name}pp.so.*
%{_libdir64}/lib%{name}pp.so.*


%files -n %{name}pp-devel
%{_includedir}/%{name}++/
%{_libdir}/lib%{name}pp.so
%{_libdir}/cmake/Gpgmepp/
%{_libdir64}/lib%{name}pp.so
%{_libdir64}/cmake/Gpgmepp/


# %files -n q%{name}
# %doc 32bit/lang/qt/README
# %{_libdir}/libq%{name}.so.*


# %files -n q%{name}-devel
# %{_includedir}/q%{name}/
# %{_includedir}/QGpgME/
# %{_libdir}/libq%{name}.so
# %{_libdir}/cmake/QGpgme/
# %{_libdir64}/libq%{name}.so
# %{_libdir64}/cmake/QGpgme/


%files -n python2-gpg
%doc 32bit/lang/python/README
%{python_sitelib}/gpg-*.egg-info
%{python_sitelib}/gpg/
%{python_sitelib64}/gpg-*.egg-info
%{python_sitelib64}/gpg/


%files -n python3-gpg
# %doc 32bit/lang/python/README
%{python3_sitelib}/gpg-*.egg-info
%{python3_sitelib}/gpg/
%{python3_sitelib64}/gpg-*.egg-info
%{python3_sitelib64}/gpg/





%changelog
* Wed Dec 05 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.11.1-2
- Correction for TLS __thread type as AIX has no local-exec model
-    for thread-local storage (src/debug.c)

* Mon Oct 01 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.11.1-1
- Initial version 1.11.1

