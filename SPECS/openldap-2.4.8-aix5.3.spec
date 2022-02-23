Summary: The configuration files, libraries, and documentation for OpenLDAP
Name: openldap
Version: 2.4.8
Release: 1
License: OpenLDAP
Group: System Environment/Daemons
Source: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz

# Patches for 2.4
Patch0: openldap-2.4.6-config.patch
Patch1: openldap-2.0.11-ldaprc.patch
Patch2: openldap-2.2.13-setugid.patch
Patch3: openldap-2.4.8-aix6-conf.patch

URL: http://www.openldap.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libtool >= 1.5.6-2, openssl-devel, db >= 4.2
Requires: glibc >= 2.2.3-48, mktemp
Obsoletes: compat-openldap < 2.4

%define ldbm_backend berkeley
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif


%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%prep
%setup -q 
%patch0 -p1 -b .config
%patch1 -p1 -b .ldaprc
%patch2 -p1 -b .setugid
%patch3 -p1 -b .aix6-conf

%build
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

libtool='%{_builddir}/openldap-%{version}/libtool'

# Find OpenSSL's header and library dependencies.
if pkg-config openssl ; then
    OPENSSL_CPPFLAGS=`pkg-config --cflags-only-I openssl`
    CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
    OPENSSL_LDFLAGS=`pkg-config --libs-only-L openssl`
    LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS
    echo $OPENSSL_LDFLAGS
fi

CPPFLAGS="-I${dbdir}/include $OPENSSL_CPPFLAGS" \
CFLAGS="-O2" \
LDFLAGS="-L${dbdir}/%{_lib} $OPENSSL_LDFLAGS" \
LD_LIBRARY_PATH=${dbdir}/%{_lib}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}} \
LIBS=-lpthread \
./configure \
    --prefix=%{_prefix} \
    --enable-local --enable-rlookups \
    --enable-passwd \
    --enable-cleartext \
    --enable-lmpasswd \
    --enable-dynamic \
    --enable-shared \
    --disable-static \
    --disable-sql \
    --enable-slapd \
    --without-keberos \
    --enable-plugins \
    --enable-slapd \
    --enable-multimaster \
    --enable-bdb \
    --enable-hdb \
    --enable-ldap \
    --enable-ldbm \
    --with-ldbm-api=%{ldbm_backend} \
    --enable-meta \
    --enable-monitor \
    --enable-null \
    --enable-shell \
    --enable-relay \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --libexecdir=%{_libdir}

make depend
make LIBTOOL="$libtool"


%install
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
libtool='%{_builddir}/openldap-%{version}/libtool'

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/
if [ ! -e %{_prefix}/lib/liblber.a ]; then
    ln -s %{_builddir}/openldap-%{version}/libraries/liblber/.libs/liblber.a %{_prefix}/lib/liblber.a
fi

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/openldap/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/openldap/*.so
rm  %{_prefix}/lib/liblber.a

%clean 
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%preun 
if [ "$1" = "0" ] ; then
  /sbin/service ldap stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del ldap
# Openldap-servers are being removed from system.
# Do not touch the database! Older versions of this
# package attempted to store database in LDIF format, so
# it can be restored later - but it's up to the administrator 
# to save the database, if he/she wants so.
fi


%files
%defattr(-,root,root)
%doc ANNOUNCEMENT
%doc CHANGES
%doc COPYRIGHT
%doc LICENSE
%doc README
%doc contrib/slapd-modules/smbk5pwd/README
%attr(0755,root,root) %dir %{_sysconfdir}/openldap
%attr(0640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.schema*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/schema/*.ldif
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/openldap/ldap*.conf
%attr(0755,root,root) %{_libdir}/liblber-2.4*
%attr(0755,root,root) %{_libdir}/libldap-2.4*
%attr(0755,root,root) %{_libdir}/libldap_r-2.4*
%attr(0644,root,root) %{_mandir}/man5/ldif.5*
%attr(0644,root,root) %{_mandir}/man5/ldap.conf.5*
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*

%changelog
* Wed Jul 9 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.8
- Port on AIX plateform
