%global WITH_LDAP 1
%global WITH_OPENSSL 1

%{!?dotests: %define dotests 1}


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Copied from krb5-1.9.4-3.spec
# To be adapted from FC .spec file: krb5-1.15.1-8.fc26.spec

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.15.1
Release: 3
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{version}.tar.gz.asc
Source2: %{name}-%{version}-pdf.tar
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
Patch23: %{name}-1.3.1-dns.patch
Patch39: %{name}-1.8-api.patch
# Still useful ? Code has changed...
#Patch59: %{name}-1.15.1-kpasswd_tcp.patch

# New patches for AIX
Patch100: %{name}-1.15.1-krb5int_thread_support_fini-v2.patch
#Patch100: %{name}-1.15.1-LHHd6fDW.patch
Patch101: %{name}-1.15.1-token.patch
Patch102: %{name}-1.15.1-maybe-uninitialized-v2.patch
Patch103: %{name}-1.15.1-shopts-workaround.patch
Patch104: %{name}-1.15.1-k5tls-lpthreads-v2.patch
Patch105: %{name}-1.15.1-sim-unsigned_int_len.patch

# Patches used by krb5-1.15.1-8.fc26.spec
#Patch1001: krb5-1.12.1-pam.patch
#Patch1002: krb5-1.15-beta1-selinux-label.patch
Patch1003: krb5-1.12-ksu-path.patch
Patch1004: krb5-1.12-ktany.patch
Patch1005: krb5-1.15-beta1-buildconf.patch
# Already applied ?!!
#Patch1006: krb5-1.3.1-dns.patch
Patch1007: krb5-1.12-api.patch
Patch1008: krb5-1.13-dirsrv-accountlock.patch
Patch1009: krb5-1.9-debuginfo.patch
#Patch1010: krb5-1.11-run_user_0.patch
Patch1011: krb5-1.11-kpasswdtest.patch
Patch1012: Build-with-Werror-implicit-int-where-supported.patch
Patch1015: Use-fallback-realm-for-GSSAPI-ccache-selection.patch
Patch1016: Use-GSSAPI-fallback-skiptest.patch
Patch1017: Improve-PKINIT-UPN-SAN-matching.patch
Patch1018: Add-test-cert-generation-to-make-certs.sh.patch
Patch1019: Add-PKINIT-UPN-tests-to-t_pkinit.py.patch
Patch1020: Deindent-crypto_retrieve_X509_sans.patch
Patch1022: Add-the-client_name-kdcpreauth-callback.patch
Patch1023: Use-the-canonical-client-principal-name-for-OTP.patch
Patch1024: Add-certauth-pluggable-interface.patch
Patch1025: Correct-error-handling-bug-in-prior-commit.patch
Patch1026: Add-k5test-expected_msg-expected_trace.patch


%define libdir64 /opt/freeware/lib64


# This is due in order to don't depend on libssl.so rather libssl.a(libssl.so.1.0.2) .
# When the build stops in the middle, files are not put back at their original place
# This is done at beg and end of %build
# Run:
# ln -s /opt/freeware/lib64/libssl.so.1.0.2 /opt/freeware/lib64/libssl.so ; ln -s /opt/freeware/lib64/libcrypto.so.1.0.2 /opt/freeware/lib64/libcrypto.so
# ln -s /opt/freeware/lib/libssl.so.1.0.2   /opt/freeware/lib/libssl.so ;   ln -s /opt/freeware/lib/libcrypto.so.1.0.2   /opt/freeware/lib/libcrypto.so


License: MIT
URL: http://web.mit.edu/kerberos/www/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gzip, info, make, patch, sed 

# Tests:
BuildRequires: tcl, tcl-devel

%if %{WITH_LDAP}
BuildRequires: openldap-devel >= 2.4.23
%endif
%if %{WITH_OPENSSL}
BuildRequires: openssl-devel >= 0.9.8
%endif
BuildRequires: db-devel >= 4.7.25-2

%define _libdir64 %{_prefix}/lib64

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of cleartext passwords.


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
Requires: openldap >= 2.4.23

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

%patch0
%patch1
%patch23 -p1 -b .dns
%patch39 -p1 -b .api
#%patch59 -p1 -b .kpasswd_tcp

%patch100 -p1 -b .krb5int_thread_support_fini-v2
#%patch100 -p1 -b .LHHd6fDW
%patch101 -p1 -b .token
%patch102 -p1 -b .maybe-uninitialized-v2
%patch103 -p1 -b .shopts-workaround
%patch104 -p1 -b .k5tls-lpthreads-v2
%patch105 -p1 -b .sim-unsigned_int_len


# Fedora patches
#%patch1001 -p1 -b .krb5-1.12.1-pam
#%patch1002 -p1 -b .krb5-1.15-beta1-selinux-label
%patch1003 -p1 -b .krb5-1.12-ksu-path
%patch1004 -p1 -b .krb5-1.12-ktany
%patch1005 -p1 -b .krb5-1.15-beta1-buildconf
#%patch1006 -p1 -b .krb5-1.3.1-dns
%patch1007 -p1 -b .krb5-1.12-api
%patch1008 -p1 -b .krb5-1.13-dirsrv-accountlock
%patch1009 -p1 -b .krb5-1.9-debuginfo
#%patch1010 -p1 -b .krb5-1.11-run_user_0
%patch1011 -p1 -b .krb5-1.11-kpasswdtest
%patch1012 -p1 -b .Build-with-Werror-implicit-int-where-supported
%patch1015 -p1 -b .Use-fallback-realm-for-GSSAPI-ccache-selection
%patch1016 -p1 -b .Use-GSSAPI-fallback-skiptest
%patch1017 -p1 -b .Improve-PKINIT-UPN-SAN-matching
%patch1018 -p1 -b .Add-test-cert-generation-to-make-certs.sh
%patch1019 -p1 -b .Add-PKINIT-UPN-tests-to-t_pkinit.py
%patch1020 -p1 -b .Deindent-crypto_retrieve_X509_sans
%patch1022 -p1 -b .Add-the-client_name-kdcpreauth-callback
%patch1023 -p1 -b .Use-the-canonical-client-principal-name-for-OTP
%patch1024 -p1 -b .Add-certauth-pluggable-interface
%patch1025 -p1 -b .Correct-error-handling-bug-in-prior-commit
%patch1026 -p1 -b .Add-k5test-expected_msg-expected_trace


gzip -9 src/plugins/kdb/db2/libdb2/docs/*.ps src/plugins/kdb/db2/libdb2/man/*.ps

# Take the execute bit off of documentation.
chmod -x doc/*/*/*/*/*/*.txt doc/*/*.html doc/*/*/*.html doc/*/*/*/*.html

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


export PATH=/usr/bin:$ACTUALPATH
export GREP=/usr/bin/grep
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

# XLC export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CC="gcc -maix64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

export CXX=g++
export CXXFLAGS=$CFLAGS

export LD=/usr/bin/ld
# XLC export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-brtl"


# first build the 64-bit version
export OBJECT_MODE=64
cd src-64

#export INCLUDES=-I%{_includedir}/et
#export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all $CFLAGS`"
export CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing $CFLAGS`"
#export CPPFLAGS="`echo $DEFINES $INCLUDES`"

#        --with-netlib=-lresolv \

DBLIB="-ldb" ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
        SS_LIB="-lss" \
    --enable-shared --disable-static \
    --localstatedir=/var/kerberos \
    --with-tcl=%{_libdir64} \
    --enable-dns-for-realm \
    --with-system-verto=no \
    --with-tcl==/opt/freeware/lib64 \
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
        --with-pkinit-crypto-impl=openssl \
        --with-tls-impl=openssl \
        --with-pam \
        --with-prng-alg=os


# now build it... parallel make (j>1) does not seem to work
PATH=/opt/freeware/bin:$PATH gmake


if [ "%{dotests}" == 1 ]
then
    (gmake check || true)
    /usr/sbin/slibclean
    cd ./lib/crypto/krb
      gmake nfold.so
    cd -
    (gmake check || true)
    /usr/sbin/slibclean
fi


# now build the 32-bit version

export CC="gcc -maix32 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"
# XLC export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-brtl"

export OBJECT_MODE=32
cd ../src-32
DBLIB="-ldb" ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --localstatedir=/var/kerberos \
    --with-tcl=/opt/freeware \
    --enable-dns-for-realm \
    --with-tcl=%{_libdir} \
    --with-system-verto=no \
%if %{WITH_LDAP}
    --with-ldap \
%endif
%if %{WITH_OPENSSL}
    --enable-pkinit
%else
    --disable-pkinit
%endif

# now build it... parallel make (j>1) does not seem to work
PATH=/opt/freeware/bin:$PATH gmake

if [ "%{dotests}" == 1 ]
then
    (gmake check || true)
    /usr/sbin/slibclean
    cd ./lib/crypto/krb
      gmake nfold.so
    cd -
    (gmake check || true)
    /usr/sbin/slibclean
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
cp doc/*/*/*/*/*/*.txt doc/*/*.html doc/*/*/*.html doc/*/*/*/*.html ${RPM_BUILD_ROOT}%{_infodir}/
chmod 0644 ${RPM_BUILD_ROOT}%{_infodir}/*

# Unconditionally compress the info pages so that we know the right file name
# to pass to install-info in %%post.
echo "No *.info.* files ?!!!"
#gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*


# Sample KDC config files (bundled kdc.conf and kadm5.acl).
mkdir -p ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc
cp %{SOURCE10} %{SOURCE11} ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc/
chmod 0600 ${RPM_BUILD_ROOT}/var/kerberos/krb5kdc/*

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
; do
	ln -sf ./%{_libdir}/${f}.a	./%{_libdir64}/${f}.a
done

%if %{WITH_LDAP}
for f in libkdb_ldap ; do
	ln -sf ./%{_libdir}/${f}.a	./%{_libdir64}/${f}.a
done
%endif



%post server
# Install info pages.
/sbin/install-info %{_infodir}/krb5-admin.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/krb5-install.info.gz %{_infodir}/dir || :


%preun server
if [ "$1" -eq "0" ] ; then
    /etc/rc.d/init.d/krb5kdc stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kadmin stop > /dev/null 2>&1 || :
    /etc/rc.d/init.d/kprop stop > /dev/null 2>&1 || :
    /sbin/install-info --delete %{_infodir}/krb5-admin.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/krb5-install.info.gz %{_infodir}/dir || : 
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
/sbin/install-info %{_infodir}/krb5-user.info.gz %{_infodir}/dir || :


%preun workstation
if [ "$1" -eq "0" ] ; then
    /sbin/install-info --delete %{_infodir}/krb5-user.info.gz %{_infodir}/dir || :
fi


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
# For enabling testing (which uses /opt/freeware/lib ...)
%{_libdir}/libprofile.a
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/*
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
