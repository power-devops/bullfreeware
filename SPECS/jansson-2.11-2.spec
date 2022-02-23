%define libjansson_version 4
%define libjansson_fullversion 4.11.0
# The full version is significant as each new version of libjansson adds symbols

%define name jansson
%define srcname jansson
%define version 2.11
%define release 2

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}


%define _libdir64 %{_prefix}/lib64


Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        C library for encoding, decoding and manipulating JSON data
Group:          System Environment/Libraries
BuildArch:      ppc

License:        MIT
URL:            http://www.digip.org/jansson/
Source0:        http://www.digip.org/jansson/releases/jansson-%{version}.tar.gz
Source1:        http://www.digip.org/jansson/releases/jansson-%{version}.tar.gz.asc

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires:  gcc
BuildRequires:  python-sphinx

Patch1:        jansson-2.11-no_builtins.patch

%description
Small library for parsing and writing JSON documents.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary: Header files for jansson
Group: Development/Libraries
BuildArch: ppc


%description devel
Header files for developing applications making use of jansson.


%package devel-doc
Summary: Development documentation for jansson
Group: Development/Libraries
BuildArch: noarch

%description devel-doc
Development documentation for jansson.



%prep
# %autosetup not recognized by RPM 3.0.5

%setup -q

%patch1

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



%build

/usr/bin/env | /usr/bin/sort

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export CFLAGS=" -fno-builtin"
export FLAG32="-maix32"
export FLAG64="-maix64"

export have_atomic_builtins=no
export have_sync_builtins=no

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
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
export LIBS=" -lm "

# TEMPORARY WORK AROUND for GCC builtins which break XLC compile
# The configure.ac/configure script always finds the GCC __atomic and __sync
# builtin functions, following will avoid the problem
#sed -i -e 's|__atomic_test_and_set|__NOatomic_test_and_set|' ./configure.ac
#sed -i -e 's|__sync_bool_compare_and_swap|__NOsync_bool_compare_and_swap|' ./configure.ac


./configure -v \
            --prefix=%{_prefix} --disable-static

gmake %{?_smp_mflags}

# gmake html



# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export LIBS=" -lm "
export LDFLAGS=" -Wl,-bmaxdata:0x80000000"

# TEMPORARY WORK AROUND for GCC builtins which break XLC compile
# The configure.ac/configure script always finds the GCC __atomic and __sync
# builtin functions, following will avoid the problem
#sed -i -e 's|__atomic_test_and_set|__NOatomic_test_and_set|' ./configure.ac
#sed -i -e 's|__sync_bool_compare_and_swap|__NOsync_bool_compare_and_swap|' ./configure.ac


./configure -v \
            --prefix=%{_prefix} --disable-static

gmake %{?_smp_mflags}

gmake html


# Archive 64 bit shared object in 32 bit shared library

slibclean
${AR} -q src/.libs/libjansson.a ../64bit/src/.libs/libjansson.so.%{libjansson_version}

slibclean

strip -e -X32_64     src/.libs/libjansson.so.%{libjansson_version} ../64bit/src/.libs/libjansson.so.%{libjansson_version}





%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"


# Add libjansson.so.4 and libjansson.so & .so.4.11.0 - they may be required
mkdir    ${RPM_BUILD_ROOT}%{_libdir64}
install -p src/.libs/libjansson.so.%{libjansson_version} ${RPM_BUILD_ROOT}%{_libdir64}/libjansson.so.%{libjansson_version}
ln -sf  libjansson.so.%{libjansson_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libjansson.so
ln -sf  libjansson.so.%{libjansson_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libjansson.so.%{libjansson_fullversion}

# Following not required, as lib64/libjansson.a is symlink to lib/libjansson.a
# mv ${RPM_BUILD_ROOT}%{_libdir}/libjansson.a ${RPM_BUILD_ROOT}%{_libdir64}/libjansson.a


# %check is not recogized by RPM 3.0.5
#%check


# Currently there are 4 test suites
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi

rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}

cd ../32bit
export OBJECT_MODE=32

gmake install INSTALL="install -p" DESTDIR="$RPM_BUILD_ROOT"


# Add libjansson.so.4 and libjansson.so & .so.4.11.0 - they may be required
install -p src/.libs/libjansson.so.%{libjansson_version} ${RPM_BUILD_ROOT}%{_libdir}/libjansson.so.%{libjansson_version}
ln -sf  libjansson.so.%{libjansson_version}     ${RPM_BUILD_ROOT}%{_libdir}/libjansson.so
ln -sf  libjansson.so.%{libjansson_version}     ${RPM_BUILD_ROOT}%{_libdir}/libjansson.so.%{libjansson_fullversion}

# Following is done in case a future version is incompatible
mv    ${RPM_BUILD_ROOT}%{_libdir}/libjansson.a ${RPM_BUILD_ROOT}%{_libdir}/libjansson-%{libjansson_fullversion}.a
ln -s libjansson-%{libjansson_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libjansson.a
ln -s ../lib/libjansson.a ${RPM_BUILD_ROOT}%{_libdir64}/libjansson.a


# Currently there are 4 test suites
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi

rm "$RPM_BUILD_ROOT%{_libdir}"/*.la




%files
%doc 32bit/LICENSE 32bit/CHANGES
%{_libdir}/libjansson.a
%{_libdir}/libjansson-%{libjansson_fullversion}.a
%{_libdir64}/libjansson.a
%{_libdir}/*.so.*
%{_libdir64}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir64}/*.so
# Not installed  %{_libdir64}/pkgconfig/%{name}.pc
%{_includedir}/*

%files devel-doc
%doc 32bit/doc/_build/html/*




%changelog
* Thu Oct 04 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.11-2
- Modify configure.ac script to avoid finding the GCC __atomic and __sync
-   builtin functions

* Mon Sep 24 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.11-1
- Initial version 2.11

