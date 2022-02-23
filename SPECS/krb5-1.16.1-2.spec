%global WITH_LDAP 1
%global WITH_OPENSSL 1

%{!?dotests: %define dotests 1}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Copied from krb5-1.15.1-5.spec (1.15.1-3 plus modifs to explore test errors)
# originally adapted from Fedora 26 .spec file: krb5-1.15.1-8.fc26.spec
# and adapted from Fedora 29 .spec file: krb5-1.16.1-2.fc29.spec

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.16.1
Release: 2

# Source0: %{name}-%{version}.tar.gz
# Source1: %{name}-%{version}.tar.gz.asc

Source0: https://web.mit.edu/kerberos/dist/krb5/1.16/krb5-%{version}.tar.gz
Source1: https://web.mit.edu/kerberos/dist/krb5/1.16/krb5-%{version}.tar.gz.asc

# Documentation Source generated during the build or copied from upstream
Source2: %{name}-%{version}-pdfs.tar

Source3: kadmind.init
Source4: kpropd.init
Source5: krb5kdc.init
Source6: krb5.conf
Source10: kdc.conf
Source11: kadm5.acl
Source19: krb5kdc.sysconfig
Source20: kadmin.sysconfig

Source1000: %{name}-%{version}-%{release}.build.log


Patch0: %{name}-%{version}-aix.patch

# Now partly fixed for config/config.guess in source code of krb5 1.15.1
# However sub-part of patch for config/shlib.conf still required
Patch1: %{name}-%{version}-aix67.patch

# Do not specify INIT_FINI_PREP/-binitfini for MAKE_SHLIB_COMMAND
Patch2: %{name}-%{version}-aix68.patch

# Following not currently applied due to lack of libdb6
#AIX Toolbox has version specific library name for db (libdb6.a)
#This patch changes -ldb in configure to -ldb6
# Patch108: krb5-1.16.1-aix-db.patch


Patch23: %{name}-1.3.1-dns.patch

# Supplanted by Fedora patch krb5-1.12-api.patch
#Patch39: %{name}-1.8-api.patch
# Still useful ? Code has changed...
#Patch59: %{name}-1.15.1-kpasswd_tcp.patch

# New patches for AIX (from version 1.15)
# following integrated in source
#Patch100: %{name}-1.15.1-krb5int_thread_support_fini-v2.patch
#Patch100: %{name}-1.15.1-LHHd6fDW.patch
#Patch101: %{name}-1.15.1-token.patch
#Patch102: %{name}-1.15.1-maybe-uninitialized-v2.patch

Patch103: %{name}-1.16.1-shopts-workaround.patch
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


# Patches used by krb5-1.16.1-2.fc29.spec (common with 1.15.1/2)

# ksu modifs to perform account and session management
#Patch1001: krb5-1.12.1-pam.patch
# Security Enhanced Linux
#Patch1002: krb5-1.15-beta1-selinux-label.patch (1.15.1)
#Patch1002: krb5-1.15.1-selinux-label.patch (1.15.2 and 1.16.1)

Patch1003: krb5-1.12-ksu-path.patch
Patch1004: krb5-1.12-ktany.patch
Patch1005: krb5-1.15-beta1-buildconf.patch

# Already applied (patch dates back to 2001) ?
#Patch1006: krb5-1.3.1-dns.patch

Patch1007: krb5-1.12-api.patch
Patch1008: krb5-1.13-dirsrv-accountlock.patch
Patch1009: krb5-1.9-debuginfo.patch

# Security Enhanced Linux
#Patch1010: krb5-1.11-run_user_0.patch

Patch1011: krb5-1.11-kpasswdtest.patch


# Some Fedora 1.16 patches touch same files, must apply most in following order

Patch1020: Process-included-directories-in-alphabetical-order.patch

# Work around for valid_name_scandir() / prof_parse.c error on
# const dirent* incompatible with AIX 6.1 dirent* in scandir() I/Fs
Patch107: Workaround-scandir-dirent-pointer.patch

Patch1021: Fix-hex-conversion-of-PKINIT-certid-strings.patch
Patch1022: Exit-with-status-0-from-kadmind.patch
Patch1023: Include-etype-info-in-for-hardware-preauth-hints.patch
Patch1024: Fix-securid_sam2-preauth-for-non-default-salt.patch
Patch1025: Refactor-KDC-krb5_pa_data-utility-functions.patch
Patch1026: Simplify-kdc_preauth.c-systems-table.patch
Patch1027: Add-PKINIT-client-support-for-freshness-token.patch
Patch1028: Add-PKINIT-KDC-support-for-freshness-token.patch
Patch1029: Fix-read-overflow-in-KDC-sort_pa_data.patch

Patch1030: Include-preauth-name-in-trace-output-if-possible.patch
Patch1031: Report-extended-errors-in-kinit-k-t-KDB.patch
Patch1032: Add-libkrb5support-hex-functions-and-tests.patch
Patch1033: Use-libkrb5support-hex-functions-where-appropriate.patch
Patch1034: Add-ASN.1-encoders-and-decoders-for-SPAKE-types.patch
Patch1035: Add-k5_buf_add_vfmt-to-k5buf-interface.patch
Patch1036: Add-vector-support-to-k5_sha256.patch
Patch1037: Move-zap-definition-to-k5-platform.h.patch
Patch1038: Implement-k5_buf_init_dynamic_zap.patch
Patch1039: Use-k5_buf_init_dynamic_zap-where-appropriate.patch

Patch1040: Add-SPAKE-preauth-support.patch
Patch1041: Add-doc-index-entries-for-SPAKE-constants.patch
Patch1042: Fix-SPAKE-memory-leak.patch
Patch1043: Zap-data-when-freeing-krb5_spake_factor.patch
Patch1044: Be-more-careful-asking-for-AS-key-in-SPAKE-client.patch
Patch1045: Restrict-pre-authentication-fallback-cases.patch
Patch1046: Remove-nodes-option-from-make-certs-scripts.patch


%define libdir64 /opt/freeware/lib64
%define _libdir64 %{_prefix}/lib64


# Following is done to avoid dependency on libssl.so rather than
#           libssl.a(libssl.so.1.0.2)
# When the build stops in the middle, files are not restored to
# their original place
# This is done at beg and end of %build
# Run:
#
# ln -s /opt/freeware/lib64/libssl.so.1.0.2 /opt/freeware/lib64/libssl.so
# ln -s /opt/freeware/lib64/libcrypto.so.1.0.2 /opt/freeware/lib64/libcrypto.so
#
# ln -s /opt/freeware/lib/libssl.so.1.0.2   /opt/freeware/lib/libssl.so
# ln -s /opt/freeware/lib/libcrypto.so.1.0.2   /opt/freeware/lib/libcrypto.so


License: MIT
URL: http://web.mit.edu/kerberos/www/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gzip, info, make, patch, sed 

# Tests:
BuildRequires: tcl, tcl-devel

%if %{WITH_LDAP}
BuildRequires: openldap-devel >= 2.4.40
%endif
%if %{WITH_OPENSSL}
BuildRequires: openssl-devel >= 0.9.8
%endif
BuildRequires: db-devel >= 4.8.24


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
Requires: db  >= 4.7.25-2
Requires: libgcc >= 6.3.0

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


%prep
ACTUALPATH=$PATH
export PATH=/opt/freeware/bin:$ACTUALPATH
export GREP=/usr/bin/grep

%setup -q -a 2
ln -s NOTICE LICENSE

%patch0 -p1 -b .aix
%patch1 -p1 -b .aix67
%patch2 -p1 -b .aix68
#%patch108 -p1 -b .aix-db
%patch23 -p1 -b .dns
#%patch39 -p1 -b .api
#%patch59 -p1 -b .kpasswd_tcp

#%patch100 -p1 -b .krb5int_thread_support_fini-v2
#%patch100 -p1 -b .LHHd6fDW
#%patch101 -p1 -b .token
#%patch102 -p1 -b .maybe-uninitialized-v2
%patch103 -p1 -b .shopts-workaround
%patch104 -p1 -b .k5tls-lpthreads-v2
#%patch105 -p1 -b .sim-unsigned_int_len
%patch106 -p1 -b .exit-key_delete-assert


# Fedora patches
#%patch1001 -p1 -b .krb5-1.12.1-pam
#%patch1002 -p1 -b .krb5-1.15.1-selinux-label
%patch1003 -p1 -b .krb5-1.12-ksu-path
%patch1004 -p1 -b .krb5-1.12-ktany
%patch1005 -p1 -b .krb5-1.15-beta1-buildconf
#%patch1006 -p1 -b .krb5-1.3.1-dns
%patch1007 -p1 -b .krb5-1.12-api
%patch1008 -p1 -b .krb5-1.13-dirsrv-accountlock
%patch1009 -p1 -b .krb5-1.9-debuginfo
#%patch1010 -p1 -b .krb5-1.11-run_user_0
%patch1011 -p1 -b .krb5-1.11-kpasswdtest


# Some Fedora patches touch same files, must apply most in following order
%patch1020 -p1 -b .Process-included-directories-in-alphabetical-order

%patch107 -p1 -b .Workaround-scandir-dirent-pointer

%patch1021 -p1 -b .Fix-hex-conversion-of-PKINIT-certid-strings
%patch1022 -p1 -b .Exit-with-status-0-from-kadmind
%patch1023 -p1 -b .Include-etype-info-in-for-hardware-preauth-hints
%patch1024 -p1 -b .Fix-securid_sam2-preauth-for-non-default-salt
%patch1025 -p1 -b .Refactor-KDC-krb5_pa_data-utility-functions
%patch1026 -p1 -b .Simplify-kdc_preauth.c-systems-table
%patch1027 -p1 -b .Add-PKINIT-client-support-for-freshness-token
%patch1028 -p1 -b .Add-PKINIT-KDC-support-for-freshness-token
%patch1029 -p1 -b .Fix-read-overflow-in-KDC-sort_pa_data

%patch1030 -p1 -b .Include-preauth-name-in-trace-output-if-possible
%patch1031 -p1 -b .Report-extended-errors-in-kinit-k-t-KDB
%patch1032 -p1 -b .Add-libkrb5support-hex-functions-and-tests
%patch1033 -p1 -b .Use-libkrb5support-hex-functions-where-appropriate
%patch1034 -p1 -b .Add-ASN.1-encoders-and-decoders-for-SPAKE-types
%patch1035 -p1 -b .Add-k5_buf_add_vfmt-to-k5buf-interface
%patch1036 -p1 -b .Add-vector-support-to-k5_sha256
%patch1037 -p1 -b .Move-zap-definition-to-k5-platform.h
%patch1038 -p1 -b .Implement-k5_buf_init_dynamic_zap
%patch1039 -p1 -b .Use-k5_buf_init_dynamic_zap-where-appropriate

%patch1040 -p1 -b .Add-SPAKE-preauth-support
%patch1041 -p1 -b .Add-doc-index-entries-for-SPAKE-constants
%patch1042 -p1 -b .Fix-SPAKE-memory-leak
%patch1043 -p1 -b .Zap-data-when-freeing-krb5_spake_factor
%patch1044 -p1 -b .Be-more-careful-asking-for-AS-key-in-SPAKE-client
%patch1045 -p1 -b .Restrict-pre-authentication-fallback-cases
%patch1046 -p1 -b .Remove-nodes-option-from-make-certs-scripts


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

echo "dotests=%{dotests}"

###############################################
# for linking with openssl archive (not soname)
###############################################
if [ -f %{_libdir}/libcrypto.so ]; then
    mv %{_libdir}/libcrypto.so /tmp/libcrypto.so.32
fi
if [ -f %{_libdir}/libssl.so ]; then
    mv %{_libdir}/libssl.so /tmp/libssl.so.32
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{libdir64}/libcrypto.so /tmp/libcrypto.so.64
fi
if [ -f %{_libdir64}/libssl.so ]; then
    mv %{libdir64}/libssl.so /tmp/libssl.so.64
fi

# Have to set runstatedir for configure, because autoconf does not set it.
export runstatedir=%{_localstatedir}/run

export PATH=/usr/bin:$ACTUALPATH
export GREP=/usr/bin/grep
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

# XLC export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CC="gcc -maix64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

# The function scandir()/(sys/dir.h) has a different I/F AIX 6.1 vs. Linux
# export CFLAGS="-D_LINUX_SOURCE_COMPAT -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

export CXX="g++ -maix64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXXFLAGS=$CFLAGS

export LD=/usr/bin/ld
# XLC export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib  -Wl,-brtl -lpthreads"

export TCL_LIB_SPEC='-L/opt/freeware/lib64 -ltcl8.6'
export TCL_STUB_LIB_PATH='/opt/freeware/lib64/libtclstub8.6.a'

#This is needed otherwise kinit will coredump with Illegal instruction
export krb5_cv_func_res_nsearch=no

# first build the 64-bit version
export OBJECT_MODE=64
cd src-64

#export INCLUDES=-I%{_includedir}/et
#export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all $CFLAGS`"

export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing $CFLAGS`"

# Alternative work around for scandir() prototype I/F error
export CFLAGS="-Wno-error=incompatible-pointer-types $CFLAGS"

#export CPPFLAGS="`echo $DEFINES $INCLUDES`"

#        --with-netlib=-lresolv 
#    --disable-delayed-initialization 


DBLIB="-ldb" ./configure \
    SS_LIB="-lss" \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
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
    --with-prng-alg=os


# now build it... parallel make (j>1) does not seem to work
PATH=/opt/freeware/bin:$PATH gmake


if [ "%{dotests}" == 1 ]
then
    export LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib
    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -i check || true)
    /usr/sbin/slibclean
    cd ./lib/crypto/krb
      gmake nfold.so
    cd -
    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -i check || true)

# Fedora make check sequence is following
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake runenv.py || true)
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -C lib check OFFLINE=yes || true)
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -C kdc check || true)
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -C appl check || true)
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -C clients check || true)
#    (LIBPATH=./lib:%{_libdir64}:/usr/lib64:/usr/lib gmake -C util check || true)
    /usr/sbin/slibclean
    unset LIBPATH
fi


# now build the 32-bit version

export CC="gcc -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CXX="g++ -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CXXFLAGS=$CFLAGS

# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"
# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib  -Wl,-bmaxdata:0x80000000 -Wl,-brtl -lpthreads"

export TCL_LIB_SPEC='-L/opt/freeware/lib -ltcl8.6'
export TCL_STUB_LIB_PATH='/opt/freeware/lib/libtclstub8.6.a'

export OBJECT_MODE=32
cd ../src-32

#    --disable-delayed-initialization 


DBLIB="-ldb" ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --localstatedir=/var/kerberos \
    --enable-dns-for-realm \
    --with-netlib=-lnsl \
    --with-tcl \
    --with-system-verto=no \
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
    --with-prng-alg=os

# now build it... parallel make (j>1) does not seem to work
PATH=/opt/freeware/bin:$PATH gmake

if [ "%{dotests}" == 1 ]
then
    export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-brtl -lpthreads"
    export LIBPATH=./lib:%{_libdir}:/usr/lib
    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -i check || true)
    /usr/sbin/slibclean
    cd ./lib/crypto/krb
      gmake nfold.so
    cd -
    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -i check || true)

# Fedora make check sequence is following
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake runenv.py || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -C lib check OFFLINE=yes || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -C kdc check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -C appl check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -C clients check || true)
#    (LIBPATH=./lib:%{_libdir}:/usr/lib gmake -C util check || true)
    /usr/sbin/slibclean
    unset LIBPATH
fi

##################################################################
# revert previous move - linking with openssl archive (not soname)
##################################################################

if [ -f /tmp/libcrypto.so.32 ]; then
    mv /tmp/libcrypto.so.32 %{_libdir}/libcrypto.so
fi
if [ -f /tmp/libssl.so.32 ]; then
    mv /tmp/libssl.so.32 %{_libdir}/libssl.so
fi
if [ -f /tmp/libcrypto.so.64 ]; then
    mv /tmp/libcrypto.so.64 %{libdir64}/libcrypto.so
fi
if [ -f /tmp/libssl.so.64 ]; then
    mv /tmp/libssl.so.64 %{libdir64}/libssl.so
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export OBJECT_MODE=64
cd src-64
gmake install DESTDIR=${RPM_BUILD_ROOT}

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
gmake install DESTDIR=${RPM_BUILD_ROOT}

cd ..

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

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

# Unconditionally compress the info pages so that we know the right file name
# to pass to install-info in %%post.
echo "No *.info.* files ?!!!"
#gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*


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
; do
    /usr/bin/ar -X32 -rv ${f}.a ${f}.so
    /usr/bin/ar -X64 -q  ${f}.a ../lib64/${f}.so
done

%if %{WITH_LDAP}
for f in libkdb_ldap ; do
    /usr/bin/ar -X32 -rv ${f}.a ${f}.so
    /usr/bin/ar -X64 -q  ${f}.a ../lib64/${f}.so
done
%endif

ln -s libkadm5clnt_mit.a libkadm5clnt.a
ln -s libkadm5srv_mit.a  libkadm5srv.a


# And link 32bit libraries to 64bit
cd ${RPM_BUILD_ROOT}
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
; do
	ln -sf %{_libdir}/${f}.a	./%{_libdir64}/${f}.a
done

%if %{WITH_LDAP}
for f in libkdb_ldap ; do
	ln -sf %{_libdir}/${f}.a	./%{_libdir64}/${f}.a
done
%endif



%post server
# Install info pages.
#/sbin/install-info %{_infodir}/krb5-admin.info.gz %{_infodir}/dir || :
#/sbin/install-info %{_infodir}/krb5-install.info.gz %{_infodir}/dir || :


%preun server
if [ "$1" -eq "0" ] ; then
    /etc/rc.d/init.d/krb5kdc stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kadmin stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kprop stop > /dev/null 2>&1 || :
#    /sbin/install-info --delete %{_infodir}/krb5-admin.info.gz %{_infodir}/dir || :
#    /sbin/install-info --delete %{_infodir}/krb5-install.info.gz %{_infodir}/dir || : 
fi
exit 0


%postun server
if [ "$1" -ge 1 ] ; then
    /etc/rc.d/init.d/krb5kdc condrestart > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kadmin condrestart > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kprop condrestart > /dev/null 2>&1 || :
fi
exit 0


%post workstation
#/sbin/install-info %{_infodir}/krb5-user.info.gz %{_infodir}/dir || :


%preun workstation
if [ "$1" -eq "0" ] ; then
#    /sbin/install-info --delete %{_infodir}/krb5-user.info.gz %{_infodir}/dir || :
fi


%clean
# [ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


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
#%{_infodir}/krb5-user.info*

# Clients of the KDC, including tools you're likely to need if you're running
# app servers other than those built from this source package.
%{_bindir}/kdestroy
%{_bindir}/kdestroy_64
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kinit
%{_bindir}/kinit_64
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_bindir}/klist_64
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_bindir}/kpasswd_64
%{_mandir}/man1/kpasswd.1*

%{_bindir}/kvno
%{_bindir}/kvno_64
%{_mandir}/man1/kvno.1*
%{_bindir}/kadmin
%{_bindir}/kadmin_64
%{_mandir}/man1/kadmin.1*
%{_bindir}/k5srvutil
%{_bindir}/k5srvutil_64
%{_mandir}/man1/k5srvutil.1*
%{_bindir}/ktutil
%{_bindir}/ktutil_64
%{_mandir}/man1/ktutil.1*

# Doesn't really fit anywhere else.
%attr(4755,root,system) %{_bindir}/ksu
%attr(4755,root,system) %{_bindir}/ksu_64
%{_mandir}/man1/ksu.1*

# Problem-reporting tool.
%{_sbindir}/krb5-send-pr
%{_sbindir}/krb5-send-pr_64
#%dir %{_datadir}/gnats
#%{_datadir}/gnats/mit
#%{_mandir}/man1/krb5-send-pr.1*


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

#%{_infodir}/krb5-admin.info*
#%{_infodir}/krb5-install.info*

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
%{_sbindir}/kadmin.local
%{_sbindir}/kadmin.local_64
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_sbindir}/kadmind_64
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_sbindir}/kdb5_util_64
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_sbindir}/kprop_64
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_sbindir}/kpropd_64
%{_mandir}/man8/kpropd.8*
%{_sbindir}/kproplog
%{_sbindir}/kproplog_64
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc
%{_sbindir}/krb5kdc_64
%{_mandir}/man8/krb5kdc.8*

# This is here for people who want to test their server, and also 
# included in devel package for similar reasons.
%{_bindir}/sclient
%{_bindir}/sclient_64
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_sbindir}/sserver_64
%{_mandir}/man8/sserver.8*


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
%{_libdir}/libkdb_ldap.so
%{_libdir}/libkdb_ldap.so.*
%{_libdir}/libkdb_ldap.a
%{_libdir64}/libkdb_ldap.so
%{_libdir64}/libkdb_ldap.so.*
%{_libdir64}/libkdb_ldap.a
%{_mandir}/man8/kdb5_ldap_util.8
%{_sbindir}/kdb5_ldap_util
%{_sbindir}/kdb5_ldap_util_64
%endif


%files libs
%defattr(-,root,system,-)
%doc README NOTICE LICENSE
%docdir %{_mandir}
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/krb5.conf
#%{_mandir}/man1/kerberos.1*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*
%{_libdir}/libcom_err.so
%{_libdir}/libcom_err.so.*
%{_libdir}/libcom_err.a
%{_libdir64}/libcom_err.so
%{_libdir64}/libcom_err.so.*
%{_libdir64}/libcom_err.a
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssapi_krb5.so.*
%{_libdir}/libgssapi_krb5.a
%{_libdir64}/libgssapi_krb5.so
%{_libdir64}/libgssapi_krb5.so.*
%{_libdir64}/libgssapi_krb5.a
%{_libdir}/libgssrpc.so
%{_libdir}/libgssrpc.so.*
%{_libdir}/libgssrpc.a
%{_libdir64}/libgssrpc.so
%{_libdir64}/libgssrpc.so.*
%{_libdir64}/libgssrpc.a
%{_libdir}/libk5crypto.so
%{_libdir}/libk5crypto.so.*
%{_libdir}/libk5crypto.a
%{_libdir64}/libk5crypto.so
%{_libdir64}/libk5crypto.so.*
%{_libdir64}/libk5crypto.a
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt.a
%{_libdir64}/libkadm5clnt.so
%{_libdir64}/libkadm5clnt.a
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5clnt_mit.a
%{_libdir64}/libkadm5clnt_mit.so
%{_libdir64}/libkadm5clnt_mit.so.*
%{_libdir64}/libkadm5clnt_mit.a
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv.a
%{_libdir64}/libkadm5srv.so
%{_libdir64}/libkadm5srv.a
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkadm5srv_mit.a
%{_libdir64}/libkadm5srv_mit.so
%{_libdir64}/libkadm5srv_mit.so.*
%{_libdir64}/libkadm5srv_mit.a
%{_libdir}/libkdb5.so
%{_libdir}/libkdb5.so.*
%{_libdir}/libkdb5.a
%{_libdir64}/libkdb5.so
%{_libdir64}/libkdb5.so.*
%{_libdir64}/libkdb5.a
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5.a
%{_libdir64}/libkrb5.so
%{_libdir64}/libkrb5.so.*
%{_libdir64}/libkrb5.a
%{_libdir}/libkrb5support.so
%{_libdir}/libkrb5support.so.*
%{_libdir}/libkrb5support.a
%{_libdir64}/libkrb5support.so
%{_libdir64}/libkrb5support.so.*
%{_libdir64}/libkrb5support.a
%{_libdir}/libverto.so
%{_libdir}/libverto.so.*
%{_libdir}/libverto.a
%{_libdir64}/libverto.so
%{_libdir64}/libverto.so.*
%{_libdir64}/libverto.a
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
%{_libdir}/krb5/plugins/kdb/db2.so
%{_libdir64}/krb5/plugins/kdb/db2.so


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
%doc doc/ccapi
#%doc doc/implement/*.pdf
#%doc doc/kadmin
#%doc doc/kim
#%doc doc/krb5-protocol
#%doc doc/rpc
#%doc doc/threads.txt

%{_includedir}/*

%{_bindir}/compile_et
%{_bindir}/compile_et_64
%{_bindir}/krb5-config
%{_bindir}/krb5-config_64
%{_bindir}/sclient
%{_bindir}/sclient_64
%{_mandir}/man1/krb5-config.1*
%{_mandir}/man1/sclient.1*
%{_mandir}/man8/sserver.8*
%{_sbindir}/sserver
%{_sbindir}/sserver_64

# Protocol test clients.
%{_bindir}/sim_client
%{_bindir}/sim_client_64
%{_bindir}/gss-client
%{_bindir}/gss-client_64
%{_bindir}/uuclient
%{_bindir}/uuclient_64

# Protocol test servers.
%{_sbindir}/sim_server
%{_sbindir}/sim_server_64
%{_sbindir}/gss-server
%{_sbindir}/gss-server_64
%{_sbindir}/uuserver
%{_sbindir}/uuserver_64


%changelog
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
