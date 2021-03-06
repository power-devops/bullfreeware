%global WITH_LDAP 1
%global WITH_OPENSSL 1

%bcond_without dotests

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Copied from krb5-1.15.1-5.spec (1.15.1-3 plus modifs to explore test errors)
# originally adapted from Fedora 26 .spec file: krb5-1.15.1-8.fc26.spec
# and adapted from Fedora 29 .spec file: krb5-1.16.1-2.fc29.spec

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.18.2
Release: 1

Source0: https://web.mit.edu/kerberos/dist/krb5/1.18/krb5-%{version}.tar.gz
Source1: https://web.mit.edu/kerberos/dist/krb5/1.18/krb5-%{version}.tar.gz.asc

# Documentation Source generated during the build or copied from upstream
# Source2: %{name}-%{version}-pdfs.tar

Source3: kadmind.init
Source4: kpropd.init
Source5: krb5kdc.init
Source6: krb5.conf
Source10: kdc.conf
Source11: kadm5.acl
Source19: krb5kdc.sysconfig
Source20: kadmin.sysconfig
Source1000: %{name}-%{version}-%{release}.build.log


# AIX5 patch.
# Patch0: %{name}-1.18-aix.patch

Patch1: %{name}-1.18-aix-test-config.patch

# Following not currently applied due to lack of libdb6
# AIX Toolbox has version specific library name for db (libdb6.a)
# This patch changes -ldb in configure to -ldb6
# Patch108: krb5-1.16.1-aix-db.patch

Patch103: %{name}-1.18-shopts-workaround.patch
Patch104: %{name}-1.15.1-k5tls-lpthreads-v2.patch

# unsigned int changed to socklen_t
#Patch105: %{name}-1.15.1-sim-unsigned_int_len.patch

# New patch for exit handling inspired from Kerberos ticket 6930, July 2011
#Patch106: %{name}-1.15.1-exit-key_delete-assert.patch
Patch106: %{name}-1.16.1-exit-key_delete-assert.patch

# New patch due to -D_LINUX_SOURCE_COMPAT for scandir() and strerror_r()
# Pb recursive #define on strerror_r()
#Patch107: %{name}-1.16.1-strerror_r-k5-platform_h.patch
# Try work around not to error on char* and const char* in scandir() I/Fs
#Patch107: Build-without-Werror-incompatible-pointer-types.patch


# Patches used by krb5-1.17-7.fc31.spec
# Patch1028: krb5-1.12-ksu-path.patch
Patch1029: krb5-1.18-ktany.patch
# Patch1030: krb5-1.15-beta1-buildconf.patch

Patch1032: krb5-1.12-api.patch
Patch1033: krb5-1.18-dirsrv-accountlock.patch
Patch1034: krb5-1.9-debuginfo.patch

Patch1036: krb5-1.11-kpasswdtest.patch

# New AIX patches for 1.18+
# AIX 6 does not support NOFOLLOW flag
Patch1037: krb5-1.18-aix-NOFOLLOW.patch
# Error during test compilation
# Pragma not available on AIX and flag undefined
# Patch1038: krb5-1.18-aix-krb5-os.patch

%define _libdir64 %{_prefix}/lib64


License: MIT
URL: http://web.mit.edu/kerberos/www/
Group: System Environment/Libraries

BuildRequires: gzip, info, make, patch, bison
BuildRequires: sed, findutils
BuildRequires: compat-getifaddrs-devel

# Tests:
BuildRequires: tcl, tcl-devel

%if %{WITH_LDAP}
BuildRequires: openldap-devel >= 2.4.40
%endif


%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of sending passwords over the network in unencrypted form.


%package devel
Summary: Development files needed to compile Kerberos 5 programs
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
Kerberos is a network authentication system. The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you need
to install this package.


%package libs
Summary: The shared libraries used by Kerberos 5
Group: System Environment/Libraries
Requires: libgcc >= 8.4.0
Requires: compat-getifaddrs

%description libs
Kerberos is a network authentication system. The krb5-libs package
contains the shared libraries needed by Kerberos 5. If you are using
Kerberos, you need to install this package.


%package server
Group: System Environment/Daemons
Summary: The KDC and related programs for Kerberos 5
Requires: %{name}-libs = %{version}-%{release}
Requires: /sbin/install-info, info

%description server
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
you need to install this package (in other words, most people should
NOT install this package).


%if %{WITH_LDAP}
%package server-ldap
Group: System Environment/Daemons
Summary: The LDAP storage plugin for the Kerberos 5 KDC
Requires: %{name}-server = %{version}-%{release}
Requires: openldap >= 2.4.40
Requires: libgcc >= 6.3.0

%description server-ldap
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
and you wish to use a directory server to store the data for your
realm, you need to install this package.
%endif


%package workstation
Summary: Kerberos 5 programs for use on workstations
Group: System Environment/Base
Requires: %{name}-libs = %{version}-%{release}
Requires: /sbin/install-info, info

%description workstation
Kerberos is a network authentication system. The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be
installed on every workstation.


%if %{WITH_OPENSSL}
%package pkinit-openssl
Summary: The PKINIT module for Kerberos 5
Group: System Environment/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: libgcc >= 6.3.0

%description pkinit-openssl
Kerberos is a network authentication system. The krb5-pkinit-openssl
package contains the PKINIT plugin, which uses OpenSSL to allow clients
to obtain initial credentials from a KDC using a private key and a
certificate.
%endif


%package db
Summary: The DB module for Kerberos 5
BuildRequires: db-devel >= 5.3.28
Requires: %{name}-libs = %{version}-%{release}
Requires: db >= 5.3.28

%description db
Kerberos is a network authentication system. The krb5-db package
contains the db2 plugin.


%prep
ACTUALPATH=$PATH
export PATH=/opt/freeware/bin:$ACTUALPATH
export GREP=/usr/bin/grep

%setup -q
ln -s NOTICE LICENSE

%patch1 -p1 -b .aix-test-config

%patch103 -p1 -b .shopts-workaround
%patch104 -p1 -b .k5tls-lpthreads-v2
#%patch105 -p1 -b .sim-unsigned_int_len
%patch106 -p1 -b .exit-key_delete-assert


# Fedora patches
# %patch1026 -p1 -b .krb5-1.12.1-pamUPDATED2
# %patch1027 -p1 -b .krb5-1.17-beta1-selinux-label
# %patch1028 -p1 -b .krb5-1.12-ksu-path
%patch1029 -p1 -b .krb5-1.18-ktany
# %patch1030 -p1 -b .krb5-1.15-beta1-buildconf
%patch1032 -p1 -b .krb5-1.12-api
%patch1033 -p1 -b .krb5-1.13-dirsrv-accountlockUPDATED2
%patch1034 -p1 -b .krb5-1.9-debuginfo
#%patch1035 -p1 -b .krb5-1.11-run_user_0
%patch1036 -p1 -b .krb5-1.11-kpasswdtest

# AIX
%patch1037 -p1 -b .krb5-1.18-aix-NOFOLLOW
# %patch1038 -p1 -b .krb5-1.18-aix-krb5-os

gzip -9 src/plugins/kdb/db2/libdb2/docs/*.ps src/plugins/kdb/db2/libdb2/man/*.ps

# Take the execute bit off of documentation (multi commands for shorter lines)
chmod -x doc/*/*/*/*/*/*.txt
chmod -x doc/*/*.html
chmod -x doc/*/*/*.html
chmod -x doc/*/*/*/*.html

# Fix the LDIF file.
if test %{version} == 1.9.4 ; then
    # This has been fixed in 1.15.1, at least
    sed -i s,^attributetype:,attributetypes:,g \
        src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
fi

# Generate an FDS-compatible LDIF file.
inldif=src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
cat > 60kerberos.ldif << EOF
# This is a variation on kerberos.ldif which 389 Directory Server will like.
dn: cn=schema
EOF
/usr/bin/egrep -iv '(^$|^dn:|^changetype:|^add:)' $inldif | \
sed -r 's,^		,                ,g' | \
sed -r 's,^	,        ,g' >> 60kerberos.ldif
touch -r $inldif 60kerberos.ldif

mv src src-32
mkdir -p src-64
cd src-32
tar cf - . | (cd ../src-64 ; tar xpf -)


%build
export MAKE="gmake --trace"

# Have to set runstatedir for configure, because autoconf does not set it.
export runstatedir=%{_localstatedir}/run

export PATH=/opt/freeware/bin:/usr/bin:$ACTUALPATH
export GREP=/usr/bin/grep
# export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

# XLC export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"



# The function scandir()/(sys/dir.h) has a different I/F AIX 6.1 vs. Linux
# export CFLAGS="-D_LINUX_SOURCE_COMPAT -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

export LD=/usr/bin/ld
# XLC export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"

#This is needed otherwise kinit will coredump with Illegal instruction
export krb5_cv_func_res_nsearch=no

export CFLAGS="-DSYSV -D_AIX -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

configure_krb5 () {
    set -ex
     DBLIB="-ldb" ./configure \
        SS_LIB="-lss" \
        --prefix=%{_prefix} \
        --libdir=$1 \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --enable-shared \
        --disable-static \
        --localstatedir=/var/kerberos \
        --with-netlib=-lnsl \
        --with-tcl \
        --enable-dns-for-realm \
        --with-system-verto=no \
        --with-system-et=no \
        --with-system-ss=no \
    %if %{WITH_LDAP}
        --with-ldap \
    %endif
    %if %{WITH_OPENSSL}
        --enable-pkinit \
    %else
        --disable-pkinit \
    %endif
        --with-crypto-impl=openssl \
        --with-pkinit-crypto-impl=openssl \
        --with-tls-impl=openssl \
        --with-pam \
        --with-prng-alg=os \
        || (cat config.log; exit 1)
  
    #        --with-system-db=yes \
    #        --with-netlib=-lresolv 
    #    --disable-delayed-initialization 
    
    # Some -brtl flag are added automatically
    find -name Makefile | xargs /opt/freeware/bin/sed -i 's|-brtl||g'
}

build_krb5_lib () {
    set -ex
    export OBJECT_MODE=$1
    cd src-$1
    configure_krb5 $2

    # We must create manually all libraries.
    # make juste create .so, and some .so depends of other.
    # So we create manually one by one in the right dependy order .a lib...
    cd util/support
    $MAKE
    cd ../../lib
    $AR -qc libkrb5support.a libkrb5support.so.*
    
    cd ../util/et
    $MAKE
    cd ../../lib
    $AR -qc libcom_err.a libcom_err.so.*
    
    cd ../util/profile
    $MAKE
    cd ..
    
    cd ../include
    $MAKE
    
    cd  ../lib/crypto
    $MAKE
    cd ..
    $AR -qc libk5crypto.a libk5crypto.so.*
    
    cd krb5
    $MAKE -j8
    cd ..
    $AR -qc libkrb5.a libkrb5.so.*
    
    cd ../util/verto
    $MAKE
    cd ../../lib
    $AR -qc libverto.a libverto.so.*
    
    cd krad
    $MAKE
    cd ..
    $AR -qc libkrad.a libkrad.so.*
    
    cd gssapi
    $MAKE
    cd ..
    $AR -qc libgssapi_krb5.a libgssapi_krb5.so.*
    
    # 'client' binary is created here...
    # So we '$MAKE' in two parts.
    cd rpc
    $MAKE libgssrpc.so
    cp libgssrpc.so.* ..
    cd ..
    $AR -qc libgssrpc.a libgssrpc.so.*
    cd rpc
    $MAKE
    cd ..
    
    cd kdb
    $MAKE
    cd ..
    $AR -qc libkdb5.a libkdb5.so.*
    
    cd kadm5
    $MAKE
    cd ..
    $AR -qc libkadm5clnt_mit.a libkadm5clnt_mit.so.*
    
    cd kadm5/srv/
    $MAKE
    cd ../..
    $AR -qc libkadm5srv_mit.a libkadm5srv_mit.so.*
    
    cd ../plugins/kdb/ldap/libkdb_ldap/
    $MAKE
    cd ../../../../lib
    $AR -qc libkdb_ldap.a libkdb_ldap.so.*
    
    cd ../..
}

build_krb5_bin () {
    set -ex
    export OBJECT_MODE=$1
    cd src-$1
    
    $MAKE
    cd ..
}

################
# 64 bit build #
################

#export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all $CFLAGS`"
export CC="gcc -maix64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX="g++ -maix64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXXFLAGS=$CFLAGS
export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing $CFLAGS`"

export TCL_LIB_SPEC='-L/opt/freeware/lib64 -ltcl8.6'
export TCL_STUB_LIB_PATH='/opt/freeware/lib64/libtclstub8.6.a'
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib  -lpthreads -lcompat-getifaddrs"
# -Wl,-brtl"

# Alternative work around for scandir() prototype I/F error
export CFLAGS="-Wno-error=incompatible-pointer-types $CFLAGS"

# To fullfill corectly LIBPATH for test (see kadmin/testing/scripts/env-setup.shin and kadmin/testing/scripts/env-setup.sh
export LIBPATH=`pwd`/src-64/lib:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib
export RUN_ENV=$LIBPATH

build_krb5_lib 64 %{_libdir64}

build_krb5_bin 64 %{_libdir64}

################
# 32 bit build #
################

export CC="gcc -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXX="g++ -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXXFLAGS=$CFLAGS

# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"
# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib"

export TCL_LIB_SPEC='-L/opt/freeware/lib -ltcl8.6'
export TCL_STUB_LIB_PATH='/opt/freeware/lib/libtclstub8.6.a'
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib  -Wl,-bmaxdata:0x80000000 -lpthreads -lcompat-getifaddrs"

export CFLAGS="-Wno-error=incompatible-pointer-types $CFLAGS"
export LIBPATH=`pwd`/src-32/lib:%{_libdir}:/usr/lib
export RUN_ENV=$LIBPATH

build_krb5_lib 32 %{_libdir}

build_krb5_bin 32 %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export MAKE="gmake --trace"

export OBJECT_MODE=64
cd src-64
$MAKE install DESTDIR=${RPM_BUILD_ROOT}
cp lib/*.a ${RPM_BUILD_ROOT}%{_libdir64}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv ${f} ${f}_64
  done

  cd ${RPM_BUILD_ROOT}%{_sbindir}
  for f in * ; do
    mv ${f} ${f}_64
  done
)


export OBJECT_MODE=32
cd ../src-32
$MAKE install DESTDIR=${RPM_BUILD_ROOT}
cp lib/*.a ${RPM_BUILD_ROOT}%{_libdir}

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

(
    cd  ${RPM_BUILD_ROOT}/%{_sbindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

cd ..

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_sbindir}/* || :

# Info docs.
mkdir -p ${RPM_BUILD_ROOT}%{_infodir}

# Some of the following docs have the same file name and cp detects it and fails
# This is not the way Fedora builds docs  -  TBC
# Temporarily just separate into several commands

# cp -f doc/*/*/*/*/*/*.txt doc/*/*.html doc/*/*/*.html doc/*/*/*/*.html ${RPM_BUILD_ROOT}%{_infodir}/

/usr/bin/cp -f doc/*/*/*/*/*/*.txt ${RPM_BUILD_ROOT}%{_infodir}/
/usr/bin/cp -f doc/*/*.html ${RPM_BUILD_ROOT}%{_infodir}/
/usr/bin/cp -f doc/*/*/*.html ${RPM_BUILD_ROOT}%{_infodir}/
/usr/bin/cp -f doc/*/*/*/*.html ${RPM_BUILD_ROOT}%{_infodir}/
chmod 0644 ${RPM_BUILD_ROOT}%{_infodir}/*


# Sample KDC config files (bundled kdc.conf and kadm5.acl).
mkdir -p ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc
cp %{SOURCE10} %{SOURCE11} ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc/
chmod 0600 ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc/*
mkdir -p ${RPM_BUILD_ROOT}/var/kerberos/run/krb5kdc
chmod 0644 ${RPM_BUILD_ROOT}/var/kerberos/run/krb5kdc

# Default configuration file for everything.
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_sysconfdir}/krb5.conf
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/krb5.conf

# Server init scripts (kadmind,kpropd,krb5kdc) and their sysconfig files.
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d
for init in \
    %{SOURCE3}\
    %{SOURCE4} \
    %{SOURCE5} ; do
	# In the past, the init script was supposed to be named after the
	# service that the started daemon provided.  Changing their names
	# is an upgrade-time problem I'm in no hurry to deal with.
    service=`basename ${init} .init`
    cp ${init} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/${service%d}
    ln -sf ../init.d/${service%d} ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/S${service%d}
    ln -sf ../init.d/${service%d} ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/K${service%d}
    ln -sf ../init.d/${service%d} ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/S${service%d}
    ln -sf ../init.d/${service%d} ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/K${service%d}
done
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/*

mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
for sysconfig in \
    %{SOURCE19}\
    %{SOURCE20} ; do
    cp ${sysconfig} ${RPM_BUILD_ROOT}/etc/sysconfig/`basename ${sysconfig} .sysconfig`
done
chmod 0644 ${RPM_BUILD_ROOT}/etc/sysconfig/*

# Still useful ???????
# GCC - Fix issue for re-build
# 1) ld: ERROR: Undefined symbol: .asn1buf_expand
#/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}/%{_libdir}/libkrb5.a ./src-64/lib/krb5/asn.1/asn1buf.o
# 2) ld: ERROR: Undefined symbol: .asn1_get_tag_2
#/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}/%{_libdir}/libkrb5.a ./src-64/lib/krb5/asn.1/asn1_encode.o _get
# 1) ld: ERROR: Undefined symbol: .asn1buf_expand
#/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}/%{_libdir}/libkrb5.a ./src-32/lib/krb5/asn.1/asn1buf.o
# 2) ld: ERROR: Undefined symbol: .asn1_get_tag_2
#/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}/%{_libdir}/libkrb5.a ./src-32/lib/krb5/asn.1/asn1_encode.o _get

# GCC - Fix issue for testing
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}/%{_libdir}/libprofile.a ./src-64/util/profile/libprofile.so
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}/%{_libdir}/libprofile.a ./src-32/util/profile/libprofile.so

(
# Build AIX-style shared libraries
cd ${RPM_BUILD_ROOT}%{_libdir}
for f in \
libcom_err \
libgssapi_krb5 \
libgssrpc \
libk5crypto \
libkadm5clnt_mit \
libkadm5srv_mit \
libkdb5 \
libkrb5 \
libkrb5support \
libverto \
libkrad \
; do
    /usr/bin/ar -X64 -q  ${f}.a ../lib64/${f}.so.*
done

%if %{WITH_LDAP}
for f in libkdb_ldap ; do
    /usr/bin/ar -X64 -q  ${f}.a ../lib64/${f}.so.*
done
%endif

ln -s libkadm5clnt_mit.a libkadm5clnt.a
ln -s libkadm5srv_mit.a  libkadm5srv.a
)


(
# And link 32bit libraries to 64bit
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in \
libcom_err \
libgssapi_krb5 \
libgssrpc \
libk5crypto \
libkadm5clnt_mit \
libkadm5srv_mit \
libkdb5 \
libkrb5 \
libkrb5support \
libkadm5clnt \
libkadm5srv \
libverto \
libkrad \
; do
    ln -sf ../lib/${f}.a	${f}.a
done

%if %{WITH_LDAP}
for f in libkdb_ldap ; do
    ln -sf ../lib/${f}.a	${f}.a
done
%endif
)

%check
export MAKE="gmake --trace"
# Fedora make check sequence is following
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE runenv.py || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE -C lib check OFFLINE=yes || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE -C kdc check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE -C appl check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE -C clients check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib $MAKE -C util check || true)
%if %{with dotests}
export PATH=%{_bindir}:/usr/bin:$PATH
cd src-64
export OBJECT_MODE=64
export LIBPATH=`pwd`/lib:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib
export krb5_cv_func_res_nsearch=no
# ( $MAKE -i check || true)
/usr/sbin/slibclean
cd ./lib/crypto/krb
    $MAKE nfold.so
cd -
( $MAKE -i check || true)
/usr/sbin/slibclean
unset LIBPATH
unset krb5_cv_func_res_nsearch

cd ../src-32
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -lpthreads -Wl,-brtl "
export LIBPATH=`pwd`/lib:%{_libdir}:/usr/lib
export krb5_cv_func_res_nsearch=no
# ( $MAKE -i check || true)
/usr/sbin/slibclean
cd ./lib/crypto/krb
    $MAKE nfold.so
cd -
( $MAKE -i check || true)

/usr/sbin/slibclean
unset LIBPATH
unset krb5_cv_func_res_nsearch
%endif


%preun server
if [ "$1" -eq "0" ] ; then
    /etc/rc.d/init.d/krb5kdc stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kadmin stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kprop stop > /dev/null 2>&1 || :
fi
exit 0


%postun server
if [ "$1" -ge 1 ] ; then
    /etc/rc.d/init.d/krb5kdc condrestart > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kadmin condrestart > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kprop condrestart > /dev/null 2>&1 || :
fi
exit 0


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files workstation
%defattr(-,root,system,-)
#%doc doc/user*.ps.gz
%doc src-32/config-files/services.append
#%doc doc/kdestroy.html
#%doc doc/kinit.html
#%doc doc/klist.html
#%doc doc/kpasswd.html
#%doc doc/ksu.html
#%doc doc/krb5-user.html
#%attr(0755,root,system) %doc src-32/config-files/convert-config-files

# Clients of the KDC, including tools you're likely to need if you're running
# app servers other than those built from this source package.
%{_bindir}/kdestroy*
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kinit*
%{_mandir}/man1/kinit.1*
%{_bindir}/klist*
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd*
%{_mandir}/man1/kpasswd.1*

%{_bindir}/kvno*
%{_mandir}/man1/kvno.1*
%{_bindir}/kadmin*
%{_mandir}/man1/kadmin.1*
%{_bindir}/k5srvutil
%{_bindir}/k5srvutil_64
%{_mandir}/man1/k5srvutil.1*
%{_bindir}/ktutil*
%{_mandir}/man1/ktutil.1*

# Doesn't really fit anywhere else.
%attr(4755,root,system) %{_bindir}/ksu*
%{_mandir}/man1/ksu.1*

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr
%{_sbindir}/krb5-send-pr_64


%files server
%defattr(-,root,system,-)
%docdir %{_mandir}

/etc/rc.d/init.d/krb5kdc
/etc/rc.d/init.d/kadmin
/etc/rc.d/init.d/kprop
/etc/rc.d/rc2.d/Skrb5kdc
/etc/rc.d/rc2.d/Kkrb5kdc
/etc/rc.d/rc3.d/Skrb5kdc
/etc/rc.d/rc3.d/Kkrb5kdc
/etc/rc.d/rc2.d/Skadmin
/etc/rc.d/rc2.d/Kkadmin
/etc/rc.d/rc3.d/Skadmin
/etc/rc.d/rc3.d/Kkadmin
/etc/rc.d/rc2.d/Skprop
/etc/rc.d/rc2.d/Kkprop
/etc/rc.d/rc3.d/Skprop
/etc/rc.d/rc3.d/Kkprop
%config(noreplace) /etc/sysconfig/krb5kdc
%config(noreplace) /etc/sysconfig/kadmin

#%doc doc/admin*.ps.gz
#%doc doc/install*.ps.gz
#%doc doc/krb5-admin.html
#%doc doc/krb5-install.html

%dir /var/kerberos
%dir /var/kerberos/krb5kdc
%dir /var/kerberos/run/krb5kdc
%config(noreplace) /var/kerberos/krb5kdc/kdc.conf
%config(noreplace) /var/kerberos/krb5kdc/kadm5.acl

%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/authdata
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/authdata
%dir %{_libdir64}/krb5/plugins/kdb
%dir %{_libdir64}/krb5/plugins/preauth

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr
%{_sbindir}/krb5-send-pr_64
#%dir %{_datadir}/gnats
#%{_datadir}/gnats/mit
#%{_mandir}/man1/krb5-send-pr.1*

# KDC binaries and configuration.
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local*
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind*
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util*
%{_mandir}/man8/kdb5_util.8*
# kprop, krpopd, kroplog
%{_sbindir}/kprop*
%{_mandir}/man8/kprop.8*
%{_mandir}/man8/kpropd.8*
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc*
%{_mandir}/man8/krb5kdc.8*

# This is for people who want to test their server, and is 
# included in devel package for similar reasons.
#%{_bindir}/sclient*
#%{_mandir}/man1/sclient.1*
#%{_sbindir}/sserver*
#%{_mandir}/man8/sserver.8*


%if %{WITH_LDAP}
%files server-ldap
%defattr(-,root,system,-)
%docdir %{_mandir}
#%doc src-32/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
#%doc src-32/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
#%doc 60kerberos.ldif
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/kdb
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_libdir64}/krb5/plugins/kdb/kldap.so
%{_libdir}/libkdb_ldap.a
%{_libdir64}/libkdb_ldap.a
%{_mandir}/man8/kdb5_ldap_util.8
%{_sbindir}/kdb5_ldap_util*
%endif


%files libs
%defattr(-,root,system,-)
%doc README NOTICE LICENSE
%docdir %{_mandir}
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/krb5.conf
#%{_mandir}/man1/kerberos.1*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/man7/kerberos.7*
%{_libdir}/libcom_err.a
%{_libdir64}/libcom_err.a
%{_libdir}/libgssapi_krb5.a
%{_libdir64}/libgssapi_krb5.a
%{_libdir}/libgssrpc.a
%{_libdir64}/libgssrpc.a
%{_libdir}/libk5crypto.a
%{_libdir64}/libk5crypto.a
%{_libdir}/libkadm5clnt.a
%{_libdir64}/libkadm5clnt.a
%{_libdir}/libkadm5clnt_mit.a
%{_libdir64}/libkadm5clnt_mit.a
%{_libdir}/libkadm5srv.a
%{_libdir64}/libkadm5srv.a
%{_libdir}/libkadm5srv_mit.a
%{_libdir64}/libkadm5srv_mit.a
%{_libdir}/libkdb5.a
%{_libdir64}/libkdb5.a
%{_libdir}/libkrb5.a
%{_libdir64}/libkrb5.a
%{_libdir}/libkrb5support.a
%{_libdir64}/libkrb5support.a
%{_libdir}/libverto.a
%{_libdir64}/libverto.a
%{_libdir}/libkrad.a
%{_libdir64}/libkrad.a
# For enabling testing (which uses /opt/freeware/lib ...)
%{_libdir}/libprofile.a
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%{_libdir}/krb5/plugins/tls/k5tls.so
# Not currently building
# %{_libdir}/krb5/plugins/preauth/spake.so
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/*
%{_libdir64}/krb5/plugins/tls/k5tls.so
# Not currently building
# %{_libdir64}/krb5/plugins/preauth/spake.so
#%{_libdir}/krb5/plugins/preauth/encrypted_challenge.so
#%{_libdir64}/krb5/plugins/preauth/encrypted_challenge.so


%if %{WITH_OPENSSL}
%files pkinit-openssl
%defattr(-,root,system,-)
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so
%{_libdir64}/krb5/plugins/preauth/pkinit.so
%endif


%files devel
%defattr(-,root,system,-)
%docdir %{_mandir}
#%doc doc/api/*.pdf
#%doc doc/ccapi
#%doc doc/implement/*.pdf
#%doc doc/kadmin
#%doc doc/kim
#%doc doc/krb5-protocol
#%doc doc/rpc
#%doc doc/threads.txt
%doc doc/*

%{_includedir}/*

%{_bindir}/compile_et
%{_bindir}/compile_et_64
%{_bindir}/krb5-config*
%{_mandir}/man1/krb5-config.1*

# This is for people who want to test their server
# Was included in server package for similar reasons
%{_bindir}/sclient*
%{_mandir}/man1/sclient.1*
%{_mandir}/man8/sserver.8*
%{_sbindir}/sserver*

# Protocol test clients.
%{_bindir}/sim_client*
%{_bindir}/gss-client*
%{_bindir}/uuclient*

# Protocol test servers.
%{_sbindir}/sim_server*
%{_sbindir}/gss-server*
%{_sbindir}/uuserver*


%files db
%defattr(-,root,system,-)
%{_libdir}/krb5/plugins/kdb/db2.so
%{_libdir64}/krb5/plugins/kdb/db2.so


%changelog
* Mon Oct 26 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.18.2-1
- Update to 1.18.2

* Tue Oct 20 2020 ??tienne Guesnet <etienne.guesnet@atos.net> - 1.18-2
- Put DB dependedncy in a subpackage
- Clean patch and specfile

* Thu Mar 05 2020 ??tienne Guesnet <etienne.guesnet.external@atos.net> - 1.18-1
- New version 1.18
- Merge with AIX Tollbox specfile
- Bullfreeware OpenSSL removal
- No more provide .so
- Erase -brtl flag

* Tue Apr 09 2019 Michael Wilson <michael.a.wilson@atos.net> - 1.17-1
- Update to version 1.17 inspired from Fedora 31 1.17-7 and its 25 patches

* Fri Apr 05 2019 Michael Wilson <michael.a.wilson@atos.net> - 1.16.1-3
- Align to Fedora 1.16.1-25 --  25 new patches, 1 modified, 3 updated
- Includes migration to SHA-256 for audit ticket IDs and Python 3 for docs

* Wed Sep 26 2018 Michael Wilson <michael.a.wilson@atos.net> - 1.16.1-2
- Fix bad symbolic links in lib64 pointing to libraries in lib

* Fri May 18 2018 Michael Wilson <michael.a.wilson@atos.net> - 1.16.1-1
- Update to version 1.16.1 inspired from Fedora 29

* Wed Aug 23 2017 Tony Reix <tony.reix@bull.net> - 1.15.1-1
- Move .spec file to version 1.15.1

* Thu Jun 22 2017 Tony Reix <tony.reix@bull.net> - 1.9.4-3
- Suppress dependency on libssl.so and libcrypto.so.
  Rather .a files
- Add build.log

* Tue Jul 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.9.4-2
- Initial port on Aix6.1

* Tue Oct 16 2012 Michael Perzl <michael@perzl.org> - 1.9.4-1
- updated to version 1.9.4
- fixed the start/stop scripts

* Fri Feb 17 2012 Michael Perzl <michael@perzl.org> - 1.9.3-1
- updated to version 1.9.3

* Wed Nov 16 2011 Michael Perzl <michael@perzl.org> - 1.9.2-2
- fixed missing dependency on db4

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 1.9.2-1
- updated to version 1.9.2

* Mon May 16 2011 Michael Perzl <michael@perzl.org> - 1.9.1-1
- updated to version 1.9.1

* Tue Apr 19 2011 Michael Perzl <michael@perzl.org> - 1.9-3
- updated to latest security advisory MITKRB5-SA-2011-004

* Thu Mar 17 2011 Michael Perzl <michael@perzl.org> - 1.9-2
- updated to latest security advisories
  MITKRB5-SA-2011-001, MITKRB5-SA-2011-002 and MITKRB5-SA-2011-003

* Mon Jan 10 2011 Michael Perzl <michael@perzl.org> - 1.9-1
- updated to version 1.9

* Mon Jan 10 2011 Michael Perzl <michael@perzl.org> - 1.8.3-2
- updated to latest security advisories
  MITKRB5-SA-2010-006 and MITKRB5-SA-2010-007

* Thu Sep 30 2010 Michael Perzl <michael@perzl.org> - 1.8.3-1
- updated to version 1.8.3, based on Fedora 15 version 1.8.3-5

* Sun Jun 06 2010 Michael Perzl <michael@perzl.org> - 1.8.1-1
- first version for AIX V5.1 and higher based on Fedora 13 version 1.8.1-5
