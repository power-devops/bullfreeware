%global WITH_LDAP 1
%global WITH_OPENSSL 1

Summary: The Kerberos network authentication system
Name: krb5
Version: 1.9.4
Release: 2
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{version}.tar.gz.asc
Source2: %{name}-%{version}-pdf.tar.bz2
Source3: kadmind.init
Source4: kpropd.init
Source5: krb5kdc.init
Source6: krb5.conf
Source10: kdc.conf
Source11: kadm5.acl
Source19: krb5kdc.sysconfig
Source20: kadmin.sysconfig

Patch0: %{name}-%{version}-aix.patch
Patch1: %{name}-%{version}-aix67.patch
Patch23: %{name}-1.3.1-dns.patch
Patch39: %{name}-1.8-api.patch
Patch59: %{name}-1.8-kpasswd_tcp.patch

License: MIT
URL: http://web.mit.edu/kerberos/www/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gzip, info, make, patch, sed 

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
export PATH=/opt/freeware/bin:$PATH
%setup -q -a 2
ln -s NOTICE LICENSE

%patch0
%patch1
%patch23 -p1 -b .dns
%patch39 -p1 -b .api
%patch59 -p1 -b .kpasswd_tcp

gzip -9 doc/*.ps

# Take the execute bit off of documentation.
chmod -x doc/krb5-protocol/*.txt doc/*.html doc/*/*.html

# Fix the LDIF file.
if test %{version} != 1.9.4 ; then
    # Hopefully this was fixed later.
    exit 1
fi
sed -i s,^attributetype:,attributetypes:,g \
    src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif

# Generate an FDS-compatible LDIF file.
inldif=src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
cat > 60kerberos.ldif << EOF
# This is a variation on kerberos.ldif which 389 Directory Server will like.
dn: cn=schema
EOF
egrep -iv '(^$|^dn:|^changetype:|^add:)' $inldif | \
sed -r 's,^		,                ,g' | \
sed -r 's,^	,        ,g' >> 60kerberos.ldif
touch -r $inldif 60kerberos.ldif

mv src src-32
mkdir -p src-64
cd src-32
tar cf - . | (cd ../src-64 ; tar xpf -)


%build
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"

export CXX=/usr/vacpp/bin/xlC
export CXXFLAGS=$CFLAGS

export LD=/usr/bin/ld
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"

# first build the 64-bit version
export OBJECT_MODE=64
cd src-64
DBLIB="-ldb" ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --localstatedir=/var/kerberos \
    --enable-dns-for-realm \
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


# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -blibpath:/opt/freeware/lib:/usr/lib:/lib -bmaxdata:0x80000000 -brtl"
cd ../src-32
DBLIB="-ldb" ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --localstatedir=/var/kerberos \
    --with-tcl=%{_libdir}/tclConfig.sh \
    --enable-dns-for-realm \
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
cp doc/*.info* ${RPM_BUILD_ROOT}%{_infodir}/
chmod 0644 ${RPM_BUILD_ROOT}%{_infodir}/*

# Unconditionally compress the info pages so that we know the right file name
# to pass to install-info in %%post.
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*


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

# also build AIX-style shared libraries
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
ln -s libkadm5srv_mit.a libkadm5srv.a


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
%doc doc/user*.ps.gz src-32/config-files/services.append
%doc doc/kdestroy.html
%doc doc/kinit.html
%doc doc/klist.html
%doc doc/kpasswd.html
%doc doc/ksu.html
%doc doc/krb5-user.html
%attr(0755,root,system) %doc src-32/config-files/convert-config-files
%{_infodir}/krb5-user.info*

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
%dir %{_datadir}/gnats
%{_datadir}/gnats/mit
%{_mandir}/man1/krb5-send-pr.1*


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

%doc doc/admin*.ps.gz
%doc doc/install*.ps.gz
%doc doc/krb5-admin.html
%doc doc/krb5-install.html

%{_infodir}/krb5-admin.info*
%{_infodir}/krb5-install.info*

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
%dir %{_datadir}/gnats
%{_datadir}/gnats/mit
%{_mandir}/man1/krb5-send-pr.1*

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
%doc src-32/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
%doc src-32/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%doc 60kerberos.ldif
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
%{_mandir}/man8/kdb5_ldap_util.8
%{_sbindir}/kdb5_ldap_util
%{_sbindir}/kdb5_ldap_util_64
%endif


%files libs
%defattr(-,root,system,-)
%doc README NOTICE LICENSE
%docdir %{_mandir}
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/krb5.conf
%{_mandir}/man1/kerberos.1*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/krb5.conf.5*
%{_libdir}/libcom_err.so
%{_libdir}/libcom_err.so.*
%{_libdir}/libcom_err.a
%{_libdir64}/libcom_err.so
%{_libdir64}/libcom_err.so.*
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssapi_krb5.so.*
%{_libdir}/libgssapi_krb5.a
%{_libdir64}/libgssapi_krb5.so
%{_libdir64}/libgssapi_krb5.so.*
%{_libdir}/libgssrpc.so
%{_libdir}/libgssrpc.so.*
%{_libdir}/libgssrpc.a
%{_libdir64}/libgssrpc.so
%{_libdir64}/libgssrpc.so.*
%{_libdir}/libk5crypto.so
%{_libdir}/libk5crypto.so.*
%{_libdir}/libk5crypto.a
%{_libdir64}/libk5crypto.so
%{_libdir64}/libk5crypto.so.*
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt.a
%{_libdir64}/libkadm5clnt.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5clnt_mit.a
%{_libdir64}/libkadm5clnt_mit.so
%{_libdir64}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv.a
%{_libdir64}/libkadm5srv.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkadm5srv_mit.so.*
%{_libdir}/libkadm5srv_mit.a
%{_libdir64}/libkadm5srv_mit.so
%{_libdir64}/libkadm5srv_mit.so.*
%{_libdir}/libkdb5.so
%{_libdir}/libkdb5.so.*
%{_libdir}/libkdb5.a
%{_libdir64}/libkdb5.so
%{_libdir64}/libkdb5.so.*
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5.a
%{_libdir64}/libkrb5.so
%{_libdir64}/libkrb5.so.*
%{_libdir}/libkrb5support.so
%{_libdir}/libkrb5support.so.*
%{_libdir}/libkrb5support.a
%{_libdir64}/libkrb5support.so
%{_libdir64}/libkrb5support.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%dir %{_libdir64}/krb5
%dir %{_libdir64}/krb5/plugins
%dir %{_libdir64}/krb5/plugins/*
%{_libdir}/krb5/plugins/preauth/encrypted_challenge.so
%{_libdir64}/krb5/plugins/preauth/encrypted_challenge.so
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
%doc doc/api/*.pdf
%doc doc/ccapi
%doc doc/implement/*.pdf
%doc doc/kadmin
%doc doc/kim
%doc doc/krb5-protocol
%doc doc/rpc
%doc doc/threads.txt

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
