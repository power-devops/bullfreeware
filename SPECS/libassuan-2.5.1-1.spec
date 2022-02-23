%define libassuan_version 0
%define libassuan_fullversion 0.8.1
# The full version is significant as each new version of libassuan adds symbols

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}

%define _libdir64 %{_prefix}/lib64

Name:    libassuan
Summary: GnuPG IPC library
Group:   System Environment/Base
Version: 2.5.1
Release: 1

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
Source0: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
URL:     https://gnupg.org/software/libassuan/index.html

Source10: %{name}-%{version}-%{release}.build.log

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
Patch1:  libassuan-2.1.0-multilib.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8

%description
This is the IPC library used by GnuPG 2, GPGME and a few other packages.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif



%package devel 
Summary: GnuPG IPC library 
Group: System Environment/Base
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other packages.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".



%prep
%setup -q

%patch1 -p1 -b .multilib

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
export FLAG32=" -O2 -maix32"
export FLAG64=" -O2 -maix64"

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
export LDFLAGS=" -L/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"


%configure -v \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir}/libassuan2

gmake



# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export LDFLAGS=" -L/opt/freeware/lib:/usr/lib -Wl,-bmaxdata:0x80000000"


%configure -v \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir}/libassuan2

gmake

# Archive 64 bit shared object in 32 bit shared library

slibclean
${AR} -q src/.libs/libassuan.a ../64bit/src/.libs/libassuan.so.%{libassuan_version}

slibclean

strip -e -X32_64     src/.libs/libassuan.so.%{libassuan_version} ../64bit/src/.libs/libassuan.so.%{libassuan_version}




%install

export RM="/usr/bin/rm -f"

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# export CC="gcc -O2 -maix32"

cd 64bit
export OBJECT_MODE=64

gmake install DESTDIR=${RPM_BUILD_ROOT}

## Unpackaged files
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/lib*.la

# Add libassuan.so.0 and libassuan.so & .so.0.8.1 - they may be required
mkdir    ${RPM_BUILD_ROOT}%{_libdir64}
install -p src/.libs/libassuan.so.%{libassuan_version} ${RPM_BUILD_ROOT}%{_libdir64}/libassuan.so.%{libassuan_version}
ln -sf  libassuan.so.%{libassuan_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libassuan.so
ln -sf  libassuan.so.%{libassuan_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libassuan.so.%{libassuan_fullversion}


# %check is not recogized by RPM 3.0.5
#%check

# Currently there are 4 test suites
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}


cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR="$RPM_BUILD_ROOT"



# Add libassuan.so.0 and libassuan.so & .so.0.8.1 - they may be required
install -p src/.libs/libassuan.so.%{libassuan_version} ${RPM_BUILD_ROOT}%{_libdir}/libassuan.so.%{libassuan_version}
ln -sf  libassuan.so.%{libassuan_version}     ${RPM_BUILD_ROOT}%{_libdir}/libassuan.so
ln -sf  libassuan.so.%{libassuan_version}     ${RPM_BUILD_ROOT}%{_libdir}/libassuan.so.%{libassuan_fullversion}

# Following is done in case a future version is incompatible
mv    ${RPM_BUILD_ROOT}%{_libdir}/libassuan.a ${RPM_BUILD_ROOT}%{_libdir}/libassuan-%{libassuan_fullversion}.a
ln -s libassuan-%{libassuan_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libassuan.a
ln -s ../lib/libassuan.a ${RPM_BUILD_ROOT}%{_libdir64}/libassuan.a

# Currently there are 4 test suites
if [ "%{dotests}" == 1 ]
then
  (gmake check || true)
fi




%post devel 
/sbin/install-info %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :

%preun devel 
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :
fi



%files
#%license COPYING COPYING.LIB
%doc 32bit/COPYING 32bit/COPYING.LIB
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/NEWS 32bit/README
%doc 32bit/THANKS 32bit/TODO
%{_libdir}/libassuan.a
%{_libdir}/libassuan-%{libassuan_fullversion}.a
%{_libdir64}/libassuan.a
%{_libdir}/*.so.*
%{_libdir64}/*.so.*


%files devel 
%{_bindir}/libassuan-config
%{_includedir}/libassuan2/
%{_libdir}/libassuan.a
%{_libdir}/*.so
%{_libdir64}/*.so
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Wed Oct 10 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.5.1-1
- Add 64 bit library (required for 64 bit gpgme)
- Removed Fedora changelog as the notes contained no useful information

* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 2.4.3-1
- Port on AIX

