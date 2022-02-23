%define contentdir /var/www
%define suexec_caller apache
%define localstatedir /var
%define apache_uid 64500
%define apache_gid 64500
%define mpms prefork event

Summary: Apache HTTP Server
Name: httpd
Version: 2.2.29
Release: 1
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
Source1: http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2.md5
Source2: http://www.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2.sha1
Source3: %{name}.aix.init
Source4: %{name}-%{version}.conf.patch
Source5: %{name}-ssl-%{version}.conf.patch
Patch0:  httpd-2.2.29-aixconf.patch
License: Apache Software License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: patch
BuildRequires: apr-devel >= 1.4.6-2
BuildRequires: apr-util-devel >= 1.3.10-3
BuildRequires: apr-util-ldap >= 1.3.10-3
BuildRequires: db-devel >= 4.7.25-2
BuildRequires: expat-devel >= 2.0.0
BuildRequires: openssl-devel >= 1.0.1g-1
BuildRequires: pcre-devel >= 7.9-2
BuildRequires: zlib-devel

Requires: apr >= 1.4.6-2
Requires: apr-util >= 1.3.10-3
Requires: apr-util-ldap >= 1.3.10-3
Requires: db >= 4.7.25-2
Requires: expat >= 2.0.1
Requires: openssl >= 1.0.1g-1
Requires: pcre >= 7.9-2
Requires: zlib

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.


%package devel
Group: Development/Libraries
Summary: Development tools for the Apache HTTP server.
Requires: %{name} = %{version}-%{release}
Requires: apr-devel >= 1.4.6-2
Requires: apr-util-devel >= 1.3.10-3

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.


%package manual
Group: Documentation
Summary: Documentation for the Apache HTTP server.
Requires: %{name} = %{version}-%{release}

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP server. The information can
also be found at http://httpd.apache.org/docs/2.2/.


%package -n mod_ssl
Group: System Environment/Daemons
Summary: SSL/TLS module for the Apache HTTP server
BuildRequires: openssl-devel >= 1.0.1g-1
Requires: %{name} = %{version}-%{release}
Requires: openssl >= 1.0.1g-1

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.


%prep
%setup -q
%patch0 -p1 -b .aixconf.patch


%build
# starting with version 2.2.9 "export CC=xlc_r" fails to compile httpd properly
export CC="/usr/vac/bin/xlc"
export RM="/usr/bin/rm -f"
export LTFLAGS="--tag=CC --silent"

# shell function to configure and build an Apache HTTPD tree
mpmbuild()
{
mpm=$1; shift
mkdir ${mpm}; cd ${mpm}
../configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=%{_libdir}/httpd/modules \
    --localstatedir=%{localstatedir} \
    --datadir=%{contentdir} \
    --with-mpm=${mpm} \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config \
    --enable-so \
    --enable-suexec --with-suexec \
    --with-suexec-caller=%{suexec_caller} \
    --with-suexec-bin=%{_sbindir}/suexec \
    --with-suexec-logfile=/var/log/httpd/suexec_log \
    --enable-cache --enable-mem-cache \
    --enable-file-cache --enable-disk-cache \
    --enable-dav \
    --with-pcre=%{_prefix} \
    --disable-auth-digest \
    $*

make %{?_smp_mflags}
cd ..
}

# build everything and the kitchen sink with the worker build
mpmbuild worker \
    --enable-modules=all \
    --enable-mods-shared=all \
    --enable-ssl --with-ssl \
    --enable-proxy \
    --enable-cache \
    --enable-file-cache --enable-disk-cache \
    --enable-cgid \
    --enable-ldap --enable-authnz-ldap \
    --enable-authn-anon --enable-authn-alias

# for the other MPMs, just build httpd and no optional modules
for i in %{mpms}; do
    mpmbuild ${i} --enable-modules=none
done


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd worker
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# install alternative MPMs
for f in %{mpms}; do
   cp ${f}/httpd ${RPM_BUILD_ROOT}%{_sbindir}/httpd.${f}
   chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/httpd.${f}
done

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

# mod_ssl bits
for suffix in crl crt csr key prm ; do
    mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/ssl.${suffix}
done

# for holding mod_dav lock database
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/lib/dav

# create a prototype session cache
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/cache/mod_ssl
touch ${RPM_BUILD_ROOT}%{localstatedir}/cache/mod_ssl/scache.dir
touch ${RPM_BUILD_ROOT}%{localstatedir}/cache/mod_ssl/scache.pag
touch ${RPM_BUILD_ROOT}%{localstatedir}/cache/mod_ssl/scache.sem

# create cache root
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/cache/mod_proxy

# move the build directory to within the library directory
mv ${RPM_BUILD_ROOT}%{contentdir}/build ${RPM_BUILD_ROOT}%{_libdir}/httpd/build
(
  cd ${RPM_BUILD_ROOT}%{contentdir}
  ln -s %{_libdir}/httpd/build build
)

# move utilities to /opt/freeware/bin
for f in ab htdbm logresolve htpasswd htdigest ; do
    mv ${RPM_BUILD_ROOT}%{_sbindir}/${f} ${RPM_BUILD_ROOT}%{_bindir}
done

# fix definitions in httpd.conf
cp ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf .
patch -s < %{SOURCE4}
cp httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf

# fix definitions in extra/httpd-ssl.conf
cp ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf .
patch -s < %{SOURCE5}
cp httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf

# fix man page paths
sed -e "s|/usr/local/apache2|/opt/freeware/etc/httpd/conf|" < docs/man/httpd.8 \
  > ${RPM_BUILD_ROOT}%{_mandir}/man8/httpd.8

# create the /etc/rc.d/init.d/ scripts and symlinks
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d/
cp %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/%{name}
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/%{name}

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/
ln -sf '../init.d/httpd' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/S%{name}
ln -sf '../init.d/httpd' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/K%{name}
ln -sf '../init.d/httpd' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/S%{name}
ln -sf '../init.d/httpd' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/K%{name}

# logs
rmdir ${RPM_BUILD_ROOT}%{localstatedir}/logs
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/log/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/run

# symlinks for /etc/httpd
ln -s ../../../..%{localstatedir}/log/httpd ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/logs
ln -s ../../../..%{localstatedir}/run ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/run
ln -s ../../../..%{_libdir}/httpd/modules ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/modules
ln -s ../../../..%{_libdir}/httpd/build ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/build

# install log rotation stuff
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
cp ./build/rpm/httpd.logrotate ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}


%pre
# add the "apache" group only if it does not yet exist
result=`/usr/sbin/lsgroup apache | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [[ "${result}" != "apache" ]] ; then
    /usr/bin/mkgroup -A id=%{apache_gid} apache 2> /dev/null || :
fi
# add the "apache" user only if it does not yet exist
result=`/usr/sbin/lsuser apache | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [[ "${result}" != "apache" ]] ; then
    /usr/bin/mkuser id=%{apache_uid} pgrp='apache' gecos='Apache User' \
        login='false' rlogin='false' apache 2> /dev/null || :
fi


%preun
if [ $1 = 0 ]; then
    /etc/rc.d/init.d/%{name} stop > /dev/null 2>&1

    # remove "apache" user and group
    /usr/sbin/rmuser -p apache || :
    /usr/sbin/rmgroup apache || :
fi


%preun manual
if [ $1 = 0 ]; then
    cat %{_sysconfdir}/httpd/conf/httpd.conf | \
    sed -e "s|Include conf/extra/httpd-manual.conf|#Include conf/extra/httpd-manual.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post manual
cat %{_sysconfdir}/httpd/conf/httpd.conf | \
sed -e "s|#Include conf/extra/httpd-manual.conf|Include conf/extra/httpd-manual.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%preun -n mod_ssl
if [ $1 = 0 ]; then
    cat %{_sysconfdir}/httpd/conf/httpd.conf | \
    sed -e "s|Include conf/extra/httpd-ssl.conf|#Include conf/extra/httpd-ssl.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf

    if [ -f %{_sysconfdir}/httpd/conf/ssl.key/server.key ] ; then
        rm -f %{_sysconfdir}/httpd/conf/ssl.key/server.key
    fi

    if [ -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt ] ; then
        rm -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt
    fi
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post -n mod_ssl
cat %{_sysconfdir}/httpd/conf/httpd.conf | \
sed -e "s|#Include conf/extra/httpd-ssl.conf|Include conf/extra/httpd-ssl.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf

umask 077

if [ ! -f %{_sysconfdir}/httpd/conf/ssl.key/server.key ] ; then
    %{_bindir}/openssl genrsa -rand /etc/passwd:/etc/group:/etc/security/passwd:/etc/security/group 1024 > %{_sysconfdir}/httpd/conf/ssl.key/server.key 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
    FQDN=localhost.localdomain
fi

if [ ! -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt ] ; then
    cat << EOF | %{_bindir}/openssl req -new -key %{_sysconfdir}/httpd/conf/ssl.key/server.key -x509 -days 365 -out %{_sysconfdir}/httpd/conf/ssl.crt/server.crt 2> /dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
${FQDN}
root@${FQDN}
EOF
fi

echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)

%doc ABOUT_APACHE CHANGES LICENSE NOTICE README VERSIONING

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%dir %{_sysconfdir}/httpd/conf/extra
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-vhosts.conf
%dir %{_sysconfdir}/httpd/conf/original
%dir %{_sysconfdir}/httpd/conf/original/extra
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

/etc/rc.d/init.d/httpd
/etc/rc.d/rc2.d/Shttpd
/etc/rc.d/rc2.d/Khttpd
/etc/rc.d/rc3.d/Shttpd
/etc/rc.d/rc3.d/Khttpd

%{_bindir}/ab
%{_bindir}/htdbm
%{_bindir}/htdigest
%{_bindir}/htpasswd
%{_bindir}/logresolve

%{_sbindir}/apachectl
%{_sbindir}/htcacheclean
%{_sbindir}/httpd
%{_sbindir}/httpd.prefork
%{_sbindir}/httpd.event
%{_sbindir}/httxt2dbm
%{_sbindir}/rotatelogs
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
# everything but mod_ssl.so:
%{_libdir}/httpd/modules/httpd.exp
%{_libdir}/httpd/modules/mod_[a-r]*.so
%{_libdir}/httpd/modules/mod_s[eptu]*.so
%{_libdir}/httpd/modules/mod_[t-z]*.so

%{_mandir}/man1/[d,h,l]*
%{_mandir}/man8/ab*
%{_mandir}/man8/apachectl.8*
%{_mandir}/man8/htcacheclean.8*
%{_mandir}/man8/httpd.8*
%{_mandir}/man8/rotatelogs*
%{_mandir}/man8/suexec*

%{contentdir}/htdocs/
%{contentdir}/cgi-bin/
%{contentdir}/error/
%{contentdir}/icons/

%attr(0755,root,system) %dir %{localstatedir}/log/httpd
%attr(0700,root,system) %dir %{localstatedir}/run

%attr(0700,apache,apache) %dir %{localstatedir}/lib/dav


%files devel
%defattr(-,root,system)
%{_includedir}/httpd/*
%{_sysconfdir}/httpd/build
%{_sbindir}/apxs
%{_sbindir}/checkgid
%{_sbindir}/dbmmanage
%{_sbindir}/envvars*
%{_mandir}/man8/apxs.8*
%dir %{_libdir}/httpd/build
%{contentdir}/build
%{_libdir}/httpd/build/config.nice
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/instdso.sh
%{_libdir}/httpd/build/mkdir.sh


%files manual
%defattr(-,root,system)
%dir %{contentdir}/manual
%{contentdir}/manual/*
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-manual.conf


%files -n mod_ssl
%defattr(-,root,system)
%{_libdir}/httpd/modules/mod_ssl.so
%attr(0700,root,root) %dir %{_sysconfdir}/httpd/conf/ssl.crl
%attr(0700,root,root) %dir %{_sysconfdir}/httpd/conf/ssl.crt
%attr(0700,root,root) %dir %{_sysconfdir}/httpd/conf/ssl.csr
%attr(0700,root,root) %dir %{_sysconfdir}/httpd/conf/ssl.key
%attr(0700,root,root) %dir %{_sysconfdir}/httpd/conf/ssl.prm
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf
%attr(0700,apache,root) %dir %{localstatedir}/cache/mod_ssl
%attr(0600,apache,root) %{localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,apache,root) %{localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,apache,root) %{localstatedir}/cache/mod_ssl/scache.sem
%attr(0700,apache,root) %dir %{localstatedir}/cache/mod_proxy


%changelog
* Tue Dec 09 2014 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.29-1
- Update to version 2.2.29

* Tue Dec 09 2014 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.25-2
- Rebuild due tu issue whith last openssl-1g

* Wed Aug 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.25-1
- Update to 2.2.25
- Add all shared modules extensions

* Fri May 11 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.22-1
- Port on Aix61

* Wed Jun 29 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.17-2
- conflit installation with apr-util-devel module

* Thu Mar 3 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.17-0
- Update to  2.2.17

* Fri Sep 26 2008 Jean-Noel Cordenner (jean-noel.cordenner@bull.net) 2.2.9-1
- Update to 2.2.9

* Thu Oct 11 2007 Christophe BELLE (christophe.belle@bull.net) 2.2.4-1
- Version for AIX 52S
- Update to 2.2.4
- Release 1

* Thu Feb  9 2006 Reza Arbab <arbab@austin.ibm.com> 1.3.31-2
- Rebuild ssl version to use OpenSSL 0.9.7g.

* Thu Jul 22 2004 David Clissold <cliss@austin.ibm.com> 1.3.31-1
- Rebuild ssl version to use OpenSSL 0.9.7d.

* Thu Jul 22 2004 David Clissold <cliss@austin.ibm.com>
- Update to 1.3.31, (and mod_ssl 2.8.19).

* Wed Oct 29 2003 David Clissold <cliss@austin.ibm.com>
- Update to 1.3.29.

* Fri Mar 21 2003 David Clissold <cliss@austin.ibm.com>
- Update mod_ssl to 2.8.14; add OPENSSL_free patch.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Mon Oct 07 2002 David Clissold <cliss@austin.ibm.com>
- Update mod_ssl to 2.8.11

* Thu Oct 03 2002 David Clissold <cliss@austin.ibm.com>
- Update to 1.3.27

* Tue Oct 01 2002 David Clissold <cliss@austin.ibm.com>
- Make openssl version a variable; that is,  --with-ssl=../openssl-%{ssl_vers}
- Only affects the mod_ssl binary package.

* Wed Jun 19 2002 David Clissold <cliss@austin.ibm.com>
- Update to Apache 1.3.26 and mod_ssl 2.8.9.
- Includes a patch for a security exposure, just announced by Apache.

* Mon Mar 04 2002 David Clissold <cliss@austin.ibm.com>
- Add patch for an announced mod_ssl security exposure.
- Does not affect apache itself, just the mod_ssl module.
- So I am incrementing the version, but will only upload mod_ssl.
- (Meaning, apache-1.3.22-2 is no change and will not see the light of day)

* Wed Oct 17 2001 David Clissold <cliss@austin.ibm.com>
- Update to Apache 1.3.22.

* Fri Sep 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix to build correctly with gcc

* Wed Aug 01 2001 David Clissold <cliss@austin.ibm.com>
- File list was missing httpd.exp.

* Mon Jul 23 2001 David Clissold <cliss@austin.ibm.com>
- Update to Apache 1.3.20; add SSL support and mod_ssl pkg
- Source package is different whether SSL is defined or not;
- the next line tells our packaging this; do not remove it!
- SOURCE EXPORT RESTRICTED

* Sun Mar 25 2001 David Clissold <cliss@austin.ibm.com>
- needed to add configure option to build shared so's

* Mon Mar 19 2001 David Clissold <cliss@austin.ibm.com>
- adapt this spec file for AIX with Apache 1.3.19
