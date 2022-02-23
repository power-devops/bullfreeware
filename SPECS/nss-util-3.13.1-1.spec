%global nspr_version 4.8.7

%define _libdir64 %{_prefix}/lib64

Summary:          Network Security Services Utilities Library
Name:             nss-util
Version:          3.13.1
Release:          1
License:          MPLv1.1 or GPLv2+ or LGPLv2+
URL:              http://www.mozilla.org/projects/security/pki/nss/
Group:            System Environment/Libraries
Requires:         nspr >= %{nspr_version}
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:    nspr-devel >= %{nspr_version}
BuildRequires:    zlib-devel >= 1.2.3
BuildRequires:    pkg-config
BuildRequires:    make

Source0:          %{name}-%{version}.tar.bz2
# The nss-util tar ball is a subset of nss-%{version}-stripped.tar.bz2, 
# Therefore we use the nss-split-util.sh script to keeping only what we need.
# Download the nss tarball via CVS from the nss propect and follow these
# steps to make the r tarball for nss-util out of the for nss:
# cvs co nss
# cvs nss-util (as soon as it is in cvs - for now extract the srpm)
# cd nss-util/devel
# cp ../../nss/devel/${version}-stripped.tar.bz2  .
# sh ./nss-split-util.sh ${version}
# A %{name}-%{version}.tar.bz2 should appear
Source1:          nss-split-util.sh
Source2:          %{name}.pc.in
Source3:          %{name}-config.in

Patch0:           %{name}-%{version}-aix.patch
Patch1:           %{name}-%{version}-aix-shlibpath.patch

%description
Utilities for Network Security Services and the Softoken module

The library is available as 32-bit and 64-bit.


# We shouln't need to have a devel subpackage as util will be used in the
# context of nss or nss-softoken. keeping to please rpmlint.
# 
%package devel
Summary:          Development libraries for Network Security Services Utilities
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}
Requires:         pkg-config

%description devel
Header and library files for doing development with Network Security Services.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or gcc -maix64".


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
# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

# Generate symbolic info for debuggers
XCFLAGS=
export XCFLAGS

export PKG_CONFIG_ALLOW_SYSTEM_LIBS=1
export PKG_CONFIG_ALLOW_SYSTEM_CFLAGS=1

#####################################################################

# first build the 64-bit version
export OBJECT_MODE=64

export USE_64=1

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config_64 --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config_64 --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

# make util
gmake -C ./mozilla-64/security/coreconf
gmake -C ./mozilla-64/security/nss

# Set up our package file
%{__mkdir_p} ./mozilla-64/dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir64},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" \
                          > ./mozilla-64/dist/pkgconfig/nss-util.pc

NSSUTIL_VMAJOR=`cat mozilla-64/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMAJOR" | awk '{print $3}'`
NSSUTIL_VMINOR=`cat mozilla-64/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMINOR" | awk '{print $3}'`
NSSUTIL_VPATCH=`cat mozilla-64/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VPATCH" | awk '{print $3}'`

export NSSUTIL_VMAJOR 
export NSSUTIL_VMINOR 
export NSSUTIL_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir64},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSSUTIL_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSSUTIL_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSSUTIL_VPATCH,g" \
                          > ./mozilla-64/dist/pkgconfig/nss-util-config

chmod 755 ./mozilla-64/dist/pkgconfig/nss-util-config

#####################################################################

# now build the 32-bit version
export OBJECT_MODE=32

export USE_64=

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --cflags-only-I nspr | sed 's/-I//'`
NSPR_LIB_DIR=`/usr/bin/pkg-config --libs-only-L nspr | sed 's/-L//'`

export NSPR_INCLUDE_DIR
export NSPR_LIB_DIR

# make util
gmake -C ./mozilla-32/security/coreconf
gmake -C ./mozilla-32/security/nss

# Set up our package file
%{__mkdir_p} ./mozilla-32/dist/pkgconfig
%{__cat} %{SOURCE2} | sed -e "s,%%libdir%%,%{_libdir},g" \
                          -e "s,%%prefix%%,%{_prefix},g" \
                          -e "s,%%exec_prefix%%,%{_prefix},g" \
                          -e "s,%%includedir%%,%{_includedir}/nss3,g" \
                          -e "s,%%NSPR_VERSION%%,%{nspr_version},g" \
                          -e "s,%%NSSUTIL_VERSION%%,%{version},g" \
                          > ./mozilla-32/dist/pkgconfig/nss-util.pc

NSSUTIL_VMAJOR=`cat mozilla-32/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMAJOR" | awk '{print $3}'`
NSSUTIL_VMINOR=`cat mozilla-32/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VMINOR" | awk '{print $3}'`
NSSUTIL_VPATCH=`cat mozilla-32/security/nss/lib/util/nssutil.h | grep "#define.*NSSUTIL_VPATCH" | awk '{print $3}'`

export NSSUTIL_VMAJOR 
export NSSUTIL_VMINOR 
export NSSUTIL_VPATCH

%{__cat} %{SOURCE3} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,$NSSUTIL_VMAJOR,g" \
                          -e "s,@MOD_MINOR_VERSION@,$NSSUTIL_VMINOR,g" \
                          -e "s,@MOD_PATCH_VERSION@,$NSSUTIL_VPATCH,g" \
                          > ./mozilla-32/dist/pkgconfig/nss-util-config

chmod 755 ./mozilla-32/dist/pkgconfig/nss-util-config


%install
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# There is no make install target so we'll do it ourselves.

%{__mkdir_p} ${RPM_BUILD_ROOT}%{_bindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_includedir}/nss3
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir64}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/nss3
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir64}/nss3
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig

# copy RTL-style shared library
for f in libnssutil3.so
do
    install -p -m 755 mozilla-32/dist/*.OBJ/lib/${f} ${RPM_BUILD_ROOT}%{_libdir}
    install -p -m 755 mozilla-64/dist/*.OBJ/lib/${f} ${RPM_BUILD_ROOT}%{_libdir64}
done

# build AIX-style shared library
export AR="ar -X32_64"
${AR} -rv ${RPM_BUILD_ROOT}%{_libdir}/libnssutil3.a \
        mozilla-32/dist/*.OBJ/lib/libnssutil3.so
${AR} -q  ${RPM_BUILD_ROOT}%{_libdir}/libnssutil3.a \
        mozilla-64/dist/*.OBJ/lib/libnssutil3.so

# copy the include files we want
# only the util headers, the rest come from softokn and nss
for f in mozilla-32/dist/public/nss/*.h ; do
    install -p -m 644 ${f} ${RPM_BUILD_ROOT}%{_includedir}/nss3
done

# Copy the package configuration files
install -p -m 644 ./mozilla-32/dist/pkgconfig/nss-util.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/nss-util.pc
install -p -m 644 ./mozilla-64/dist/pkgconfig/nss-util.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/nss-util.pc
install -p -m 755 ./mozilla-32/dist/pkgconfig/nss-util-config ${RPM_BUILD_ROOT}%{_bindir}/nss-util-config
install -p -m 755 ./mozilla-64/dist/pkgconfig/nss-util-config ${RPM_BUILD_ROOT}%{_bindir}/nss-util-config_64

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
%{_libdir}/libnssutil3.a
/usr/lib/libnssutil3.a
%{_libdir}/libnssutil3.so
/usr/lib/libnssutil3.so
%{_libdir64}/libnssutil3.so
/usr/lib64/libnssutil3.so


%files devel
%defattr(-,root,system)
%{_bindir}/nss-util-config
/usr/bin/nss-util-config
%{_bindir}/nss-util-config_64
/usr/bin/nss-util-config_64
# package configuration files
%{_libdir}/pkgconfig/nss-util.pc
%{_libdir64}/pkgconfig/nss-util.pc
# co-owned with nss
%dir %{_includedir}/nss3
%{_includedir}/nss3/*
/usr/include/nss3


%changelog
* Thu Nov 20 2014 Gerard Visiedo <gerard.visiedo@bull.net> 3.13.1-1
- First port on Aix6.1

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 3.13.1-1
- updated to version 3.13.1

* Fri Jul 01 2011 Michael Perzl <michael@perzl.org> - 3.12.10-1
- updated to version 3.12.10

* Sat Feb 05 2011 Michael Perzl <michael@perzl.org> - 3.12.9-1
- updated to version 3.12.9

* Thu Oct 21 2010 Michael Perzl <michael@perzl.org> - 3.12.8-1
- updated to version 3.12.8

* Fri Oct 01 2010 Michael Perzl <michael@perzl.org> - 3.12.4-1
- first version for AIX5L v5.1 and higher
