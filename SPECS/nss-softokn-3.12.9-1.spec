%global nspr_version 4.8.7
%global nss_util_version 3.12.9

%define _libdir64 %{_prefix}/lib64

Summary:          Network Security Services Softoken Module
Name:             nss-softokn
Version:          3.12.9
Release:          1
License:          MPLv1.1 or GPLv2+ or LGPLv2+
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    nss-util-devel >= %{nss_util_version}
BuildRequires:    sqlite-devel >= 3.6.23.1
BuildRequires:    zlib-devel
BuildRequires:    pkg-config

Requires:         nspr >= %{nspr_version}
Requires:         nss-util >= %{nss_util_version}
Requires:         nss-softokn-freebl >= %{version}

Source0:          %{name}-%{version}-stripped.tar.bz2
# The nss-softokn tar ball is a subset of nss-{version}-stripped.tar.bz2, 
# Therefore we use the nss-split-softokn.sh script to keep only what we need.
# Download the nss tarball via git from the nss propect and follow these
# steps to make the tarball for nss-util out of the one for nss:
# fedpkg clone nss
# fedpkg clone nss-softokn
# cd nss-softokn
# cp ../../nss/devel/${version}-stripped.tar.bz2  .
# sh ./nss-split-softokn.sh ${version}
# A file named {name}-{version}-stripped.tar.bz2 should appear
Source1:          nss-split-softokn.sh
Source2:          %{name}.pc.in
Source3:          %{name}-config.in

Patch0:           %{name}-%{version}-aix.patch
Patch1:           %{name}-%{version}-aix-shlibpath.patch

%description
Network Security Services Softoken Cryptographic Module

The library is available as 32-bit and 64-bit.


%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         nss-util-devel >= %{nss_util_version}
Requires:         pkg-config

%description devel
Header and Library files for doing development with Network Security Services.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%package freebl
Summary:          Freebl library for the Network Security Services
Group:            System Environment/Base
Requires:         %{name} = %{version}-%{release}

%description freebl
NSS Softoken Cryptographic Module Freelb Library

Install the nss-softokn-freebl package if you need the freebl 
library.


%package freebl-devel
Summary:          Header and Library files for doing development with the Freebl library for NSS
Group:            System Environment/Base
Requires:         %{name}-freebl = %{version}-%{release}

%description freebl-devel
NSS Softoken Cryptographic Module Freelb Library Development Tools


%prep
%setup -q
%patch0
mkdir mozilla-64
mv mozilla mozilla-32
cd mozilla-32
cp -r * ../mozilla-64
cd ..
%patch1


%build
export FREEBL_NO_DEPEND=1

# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

# Generate symbolic info for debuggers
XCFLAGS=
export XCFLAGS

export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

export NSS_USE_SYSTEM_SQLITE=1

#####################################################################

# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export USE_64=1

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config_64 --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config_64 --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

NSS_INCLUDE_DIR=`/usr/bin/pkg-config_64 --cflags-only-I nss-util | sed 's/-I//'`
NSS_LIB_DIR=`/usr/bin/pkg-config_64 --libs-only-L nss-util | sed 's/-L//'`

export NSS_INCLUDE_DIR
export NSS_LIB_DIR

# compile softokn plus needed support
gmake -C ./mozilla-64/security/coreconf
gmake -C ./mozilla-64/security/dbm
gmake -C ./mozilla-64/security/nss

# Set up our package file
# The nspr_version and nss_util_version globals used here
# must match the ones nss-softokn has for its Requires. 
%{__mkdir_p} ./mozilla-64/dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir64},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" \
                         > ./mozilla-64/dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat mozilla-64/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat mozilla-64/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat mozilla-64/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

export SOFTOKEN_VMAJOR 
export SOFTOKEN_VMINOR 
export SOFTOKEN_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir_64},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                         > ./mozilla-64/dist/pkgconfig/nss-softokn-config

chmod 755 ./mozilla-64/dist/pkgconfig/nss-softokn-config

#####################################################################

# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export USE_64=

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

NSS_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nss-util | sed 's/-I//'`
NSS_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nss-util | sed 's/-L//'`

export NSS_INCLUDE_DIR
export NSS_LIB_DIR

# compile softokn plus needed support
gmake -C ./mozilla-32/security/coreconf
gmake -C ./mozilla-32/security/dbm
gmake -C ./mozilla-32/security/nss

# Set up our package file
# The nspr_version and nss_util_version globals used here
# must match the ones nss-softokn has for its Requires. 
%{__mkdir_p} ./mozilla-32/dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{nss_util_version},g" \
                          -e "s,%%SOFTOKEN_VERSION%%,%{version},g" \
                         > ./mozilla-32/dist/pkgconfig/nss-softokn.pc

SOFTOKEN_VMAJOR=`cat mozilla-32/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMAJOR" | awk '{print $3}'`
SOFTOKEN_VMINOR=`cat mozilla-32/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VMINOR" | awk '{print $3}'`
SOFTOKEN_VPATCH=`cat mozilla-32/security/nss/lib/softoken/softkver.h | grep "#define.*SOFTOKEN_VPATCH" | awk '{print $3}'`

export SOFTOKEN_VMAJOR 
export SOFTOKEN_VMINOR 
export SOFTOKEN_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$SOFTOKEN_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$SOFTOKEN_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$SOFTOKEN_VPATCH,g" \
                         > ./mozilla-32/dist/pkgconfig/nss-softokn-config

chmod 755 ./mozilla-32/dist/pkgconfig/nss-softokn-config


%install
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} ${RPM_BUILD_ROOT}%{_includedir}/nss3
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_bindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir64}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig

# Copy the binary libraries we want
for f in libsoftokn3.so libnssdbm3.so libfreebl3.so ; do
    install -p -m 755 mozilla-32/dist/*.OBJ/lib/${f} ${RPM_BUILD_ROOT}%{_libdir}
    install -p -m 755 mozilla-64/dist/*.OBJ/lib/${f} ${RPM_BUILD_ROOT}%{_libdir64}
done

# copy the include files we want
for f in mozilla-32/dist/public/nss/*.h ; do
    install -p -m 644 ${f} ${RPM_BUILD_ROOT}%{_includedir}/nss3
done

# copy a freebl include file we also want
for f in mozilla-32/dist/private/nss/blapi.h ; do
    install -p -m 644 ${f} ${RPM_BUILD_ROOT}%{_includedir}/nss3
done

# copy the package configuration files
install -p -m 644 ./mozilla-32/dist/pkgconfig/nss-softokn.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/nss-softokn.pc
install -p -m 644 ./mozilla-64/dist/pkgconfig/nss-softokn.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/nss-softokn.pc
install -p -m 755 ./mozilla-32/dist/pkgconfig/nss-softokn-config ${RPM_BUILD_ROOT}%{_bindir}/nss-softokn-config
install -p -m 755 ./mozilla-64/dist/pkgconfig/nss-softokn-config ${RPM_BUILD_ROOT}%{_bindir}/nss-softokn-config_64

# create AIX-style shared libraries
export AR="/usr/bin/ar -X32_64"
for f in libsoftokn3 libnssdbm3 libfreebl3 ; do
    ${AR} -rv ${RPM_BUILD_ROOT}%{_libdir}/${f}.a ${RPM_BUILD_ROOT}%{_libdir}/${f}.so
    ${AR} -q  ${RPM_BUILD_ROOT}%{_libdir}/${f}.a ${RPM_BUILD_ROOT}%{_libdir64}/${f}.so
done

# make symbolic links...
(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/libnssdbm3.a
%{_libdir}/libnssdbm3.so
%{_libdir64}/libnssdbm3.so
%{_libdir}/libsoftokn3.a
%{_libdir}/libsoftokn3.so
%{_libdir64}/libsoftokn3.so
/usr/lib/libnssdbm3.a
/usr/lib/libnssdbm3.so
/usr/lib64/libnssdbm3.so
/usr/lib/libsoftokn3.a
/usr/lib/libsoftokn3.so
/usr/lib64/libsoftokn3.so


%files devel
%defattr(-,root,system)
%{_bindir}/nss-softokn-config*
%{_libdir}/pkgconfig/nss-softokn.pc
%{_libdir64}/pkgconfig/nss-softokn.pc
# co-owned with nss
%dir %{_includedir}/nss3
#
# The following headers are those exported public in
# mozilla/security/nss/lib/freebl/manifest.mn and
# mozilla/security/nss/lib/softoken/manifest.mn
#
# The following list is short because many headers, such as
# the pkcs #11 ones, have been provided by nss-util-devel
# which installed them before us.
#
%{_includedir}/nss3/blapit.h
%{_includedir}/nss3/ecl-exp.h
%{_includedir}/nss3/hasht.h
%{_includedir}/nss3/sechash.h
%{_includedir}/nss3/nsslowhash.h
%{_includedir}/nss3/secmodt.h
%{_includedir}/nss3/shsign.h
/usr/bin/nss-softokn-config*


%files freebl
%defattr(-,root,system)
%{_libdir}/libfreebl3.a
%{_libdir}/libfreebl3.so
%{_libdir64}/libfreebl3.so
/usr/lib/libfreebl3.a
/usr/lib/libfreebl3.so
/usr/lib64/libfreebl3.so


%files freebl-devel
%defattr(-,root,system)
%{_includedir}/nss3/blapi.h


%changelog
* Thu Nov 20 2014 Gerard Visiedo <gerard.visiedo@bull.net> 3.12.9-1
- First port on Aix6.1

* Sun Feb 06 2011 Michael Perzl <michael@perzl.org> - 3.12.9-1
- first version for AIX5L v5.1 and higher
