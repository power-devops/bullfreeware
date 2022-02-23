# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define contentdir /var/www
%define suexec_caller apache
%define localstatedir /var
%define apache_uid 64500
%define apache_gid 64500

# Does not work on 2.4.41; libxml2 not found.
%bcond_with proxy_html

%define __bzip2		/opt/freeware/bin/bzip2
%define _smp_mflags	-j8

Summary:    Apache HTTP Server
Name:       httpd
Version:    2.4.48
Release:    2
URL:        http://httpd.apache.org/

Source0:    http://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
# Full path: https://www.apache.org/dyn/closer.cgi/perl/
# As it is not updated with each httpd version, we have file conflicts
Source1:    mod_perl-2.0.11.tar.gz
Source3:    %{name}.aix.init
Source4:    %{name}-2.4.41.conf.patch
Source5:    %{name}-ssl-2.4.X.conf.patch
Source6:    %{name}-ssl-2.4.X.conf64.patch
Source9:    %{name}-2.4.41.configure.patch
Source10:   %{name}-2.4.41.conf64.patch
Source1000: %{name}-%{version}-%{release}.build.log 

Patch0:     %{name}-2.4.41-apachectl.patch
Patch1:     %{name}-2.4.41-export.patch

License:    Apache Software License
Group:      System Environment/Daemons

BuildRequires: patch
BuildRequires: apr-devel >= 1.7.0
BuildRequires: apr-util-devel >= 1.6.1
BuildRequires: apr-util-ldap >= 1.6.1
# BuildRequires: db-devel >= 4.7.25-2
BuildRequires: expat-devel >= 2.0.0
BuildRequires: libxml2-devel >= 2.6.32-3
BuildRequires: lua-devel >= 5.3.4
BuildRequires: pcre-devel >= 8.44
BuildRequires: openldap-devel >= 2.4.48-3
BuildRequires: sqlite-devel >= 3.23.0-1
BuildRequires: libnghttp2-devel
BuildRequires: sed
# For building ./server/exports.c
BuildRequires: gawk, grep
%if %{with dotests}
BuildRequires: perl(perl) >= 5.30
%endif

Requires: apr >= 1.7.0
Requires: apr-util >= 1.6.1
# Requires: db >= 4.8
Requires: pcre >= 8.44
Requires: openldap >= 2.4.48-3
Requires: libgcc >= 6.3.0-1
#Requires: libiconv >= 1.14-1
Requires: zlib >= 1.2.11
Requires: expat >= 2.2.6
Requires: libnghttp2


%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.


%package devel
Group: Development/Libraries
Summary: Development tools for the Apache HTTP server.
Requires: %{name} = %{version}-%{release}
Requires: apr-devel  >= 1.7.0
Requires: apr-util-devel >= 1.6.1
Requires: expat >= 2.2.6

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
also be found at http://httpd.apache.org/docs/2.4/.


%package -n mod_lua
Group: System Environment/Daemons
Summary: Lua language module for the Apache HTTP server
BuildRequires: lua-devel >= 5.3.4
Requires: %{name} = %{version}-%{release}
Requires: lua >= 5.3.4
Requires: libgcc >= 6.3.0-1

%description -n mod_lua
The mod_lua module for the Apache HTTP server allows the server to be
extended with scripts written in the Lua programming language.


%if %{with proxy_html}
%package -n mod_proxy_html
Group: System Environment/Daemons
Summary: Proxy HTML filter modules for the Apache HTTP server
BuildRequires: libxml2-devel >= 2.6.32-3
Requires: %{name} = %{version}-%{release}
Requires: libxml2 >= 2.6.32-3
Requires: libgcc >= 6.3.0-1

%description -n mod_proxy_html
The mod_proxy_html module for the Apache HTTP server provides
a filter to rewrite HTML links within web content when used within
a reverse proxy environment. The mod_xml2enc module provides
enhanced charset/internationalisation support for mod_proxy_html.
%endif


%package -n mod_ssl
Group:    System Environment/Daemons
Summary:  SSL/TLS module for the Apache HTTP server
Epoch:    1
Requires: %{name} = %{version}-%{release}
Requires: libgcc >= 6.3.0-1

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n mod_http2
Group: System Environment/Daemons
Summary:Support for the HTTP/2 transport layer
Requires: %{name} = %{version}-%{release}
Requires: libnghttp2 >= 1.38.0
Requires: libgcc >= 6.3.0

%description -n mod_http2
This module provides HTTP/2 (RFC 7540) support for the Apache HTTP Server.
This module relies on libnghttp2 to provide the core http/2 engine.


%prep
%setup -q

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

cd 64bit
%patch0
cd ../32bit
# Workaround: modify symbol export (upstream "ugly hack")
%patch1


%build

# starting with version 2.2.9 "export CC=xlc_r" fails to compile httpd properly
#export CC="/usr/vac/bin/xlc -qcpluscmt"
export CC="/opt/freeware/bin/gcc"
export LTFLAGS="--tag=CC --silent"
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
# Required for building ./server/exports.c
export GREP="/opt/freeware/bin/grep"


build_httpd ()
{
set -ex
export OBJECT_MODE=$1
cd ${OBJECT_MODE}bit
# starting with version 2.2.9 "export CC=xlc_r" fails to compile httpd properly
# XLC 32bit: export CFLAGS="-q32 -qchars=signed -D_LARGE_FILES -O2"
export CFLAGS="-maix${OBJECT_MODE} -fsigned-char -O2"
if [ ${OBJECT_MODE} -eq 32 ]
then
  export CFLAGS="${CFLAGS} -D_LARGE_FILES"
  export LDFLAGS="-L/opt/freeware/lib                       -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib                      -Wl,-bmaxdata:0x80000000"
  LIBDIR=%{_libdir}
else
  export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
  patch -p0 < %{SOURCE9}
  LIBDIR=%{_libdir}64
fi

./configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=${LIBDIR} \
    --sysconfdir=%{_sysconfdir}/httpd/conf \
    --includedir=%{_includedir}/httpd \
    --libexecdir=${LIBDIR}/httpd/modules \
    --localstatedir=%{localstatedir} \
    --datadir=%{contentdir} \
    --enable-mpms-shared=all \
    --with-apr=%{_bindir}/apr-1-config_${OBJECT_MODE} \
    --with-apr-util=%{_bindir}/apu-1-config_${OBJECT_MODE} \
    --with-ldap=yes \
    --enable-so \
    --enable-suexec --with-suexec \
    --with-suexec-caller=%{suexec_caller} \
    --with-suexec-bin=%{_sbindir}/suexec \
    --with-suexec-logfile=/var/log/httpd/suexec_log \
    --enable-cache --enable-mem-cache \
    --enable-file-cache --enable-disk-cache \
    --enable-dav \
    --with-lua=%{_prefix} \
    --with-pcre=%{_bindir}/pcre-config_${OBJECT_MODE} \
    --disable-auth-digest \
    --disable-distcache \
    --disable-imagemap \
    --enable-modules=all \
    --enable-mods-shared=all \
    --enable-ssl --with-ssl \
    --enable-proxy \
%if %{with proxy_html}
    --with-libxml2=%{_bindir}/xml2-config \
    --enable-proxy-html \
%endif
    --enable-cache \
    --enable-file-cache --enable-disk-cache \
    --enable-cgid --enable-cgi \
    --enable-ldap --enable-authnz-ldap \
    --enable-authn-anon --enable-authn-alias \
    --enable-http2 --with-nghttp2=%{_prefix}

gmake %{?_smp_mflags}

# Avoid bug with apxs. See https://bz.apache.org/bugzilla/show_bug.cgi?id=63307
sed -i 's|SH_LDFLAGS = $(EXTRA_LDFLAGS) $(EXTRA_LIBS)|SH_LDFLAGS = |' build/config_vars.mk

cd ..
}

#Build on 32bit
build_httpd 32

#Build on 64bit
build_httpd 64


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH
#install on 64bit mode
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

# for holding mod_dav lock database
mkdir -p ${RPM_BUILD_ROOT}%{localstatedir}/lib64/dav

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_64
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_64 .
patch -p0 < %{SOURCE6}
cp httpd-ssl.conf_64 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_64
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf_64
# move the build directory to within the library directory
mv ${RPM_BUILD_ROOT}%{contentdir}/build ${RPM_BUILD_ROOT}%{_libdir}64/httpd/build
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf .
patch -s < %{SOURCE10}
cp httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf_64
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/httpd.conf_64

#install on 32bit mode
export OBJECT_MODE=32
cd ../32bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

# fix definitions in httpd.conf
cp ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf .
patch -s < %{SOURCE4}
cp httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf
# fix definitions in extra/httpd-ssl.conf
(cp ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf . || true)
patch -s < %{SOURCE5}
(cp httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf || true)

mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_32
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf_32
# move the build directory to within the library directory
mv ${RPM_BUILD_ROOT}%{contentdir}/build ${RPM_BUILD_ROOT}%{_libdir}/httpd/build
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/httpd.conf_32
mv ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/httpd.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/original/httpd.conf_32

(
  cd ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/
  ln -sf httpd.conf_64 httpd.conf
  cd extra
  ln -sf httpd-ssl.conf_64 httpd-ssl.conf
  cd ../original
  ln -sf httpd.conf_64 httpd.conf
  cd extra
  ln -sf httpd-ssl.conf_64 httpd-ssl.conf
)


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

(
  cd ${RPM_BUILD_ROOT}%{contentdir}
  ln -s %{_libdir}/httpd/build build
)

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

# Find the right path for 64 bits
sed -i "s|/opt/freeware/lib/httpd|/opt/freeware/lib64/httpd|g" ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf_64


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Use httpd_test at https://httpd.apache.org/test/

check_httpd ()
{
set -x

export OBJECT_MODE=$1
cd ${OBJECT_MODE}bit

tar -xzvf %{SOURCE1}
cd mod_perl-*

# We need to adapt config location; so copy apxs
cp ${RPM_BUILD_ROOT}/%{_bindir}/apxs .
cp ${RPM_BUILD_ROOT}/%{_libdir}/httpd/build/config_vars.mk .

# Use RPM_BUILD_ROOT, except for apr and apu
sed -i "s|/opt|${RPM_BUILD_ROOT}/opt|g"                                                     config_vars.mk
sed -i "s|${RPM_BUILD_ROOT}/opt/freeware/bin/apr-1-config|/opt/freeware/bin/apr-1-config|g" config_vars.mk
sed -i "s|${RPM_BUILD_ROOT}/opt/freeware/bin/apu-1-config|/opt/freeware/bin/apu-1-config|g" config_vars.mk
sed -i 's|get_config_vars("$installbuilddir/|get_config_vars("./|' apxs
sed -i 's|get_config_vars($destdir . "$installbuilddir/|get_config_vars("./|' apxs

MP_APXS=./apxs /opt/freeware/bin/perl_${OBJECT_MODE} Makefile.PL

gmake
# An unused symbol causes crash
sed -i 's|RETVAL = ap_get_server_version();|RETVAL = 0;|g' WrapXS/Apache2/ServerUtil/ServerUtil.c
if [ ${OBJECT_MODE} -eq 32 ]
then
  # Default Perl is 64 bit
  sed -i 's|PERL = /opt/freeware/bin/perl|PERL = /opt/freeware/bin/perl_32|g' Makefile
fi
gmake

# If root, use apache user.
# Else, use directly user.
if [ "`id -u`" -eq "0" ]; then
    # New user/group apache if they do not exist
    result=`/usr/sbin/lsgroup apache | /usr/bin/awk '{ print $1 }' 2>/dev/null`
    if [[ "${result}" != "apache" ]] ; then
        /usr/bin/mkgroup -A id=%{apache_gid} apache 2> /dev/null || :
    fi
    result=`/usr/sbin/lsuser apache | /usr/bin/awk '{ print $1 }' 2>/dev/null`
    if [[ "${result}" != "apache" ]] ; then
        /usr/bin/mkuser id=%{apache_uid} pgrp='apache' gecos='Apache User' \
            login='false' rlogin='false' apache 2> /dev/null || :
    fi
    chown -R apache:apache .
fi

# We cannot change this conf location, so we copy original before alter it
cp ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf.orig

if [ ${OBJECT_MODE} -eq 32 ]
then
  # WHen 32bit, We want the 32bit conf file
  cp ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf_32 ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf
  # httpd is 64 bit as default. I dont know how to change httpd used, so we copy it and restore after tests...
  cp ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd    ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd_orig
  cp ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd_32 ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd
  grep -R /opt/freeware/bin/perl * | grep -v /opt/freeware/bin/perl_32 | awk -F: '{print $1}' | xargs sed -i "s|/opt/freeware/bin/perl|/opt/freeware/bin/perl_32|g"
  grep -R /opt/freeware/bin/perl_32_32 *                               | awk -F: '{print $1}' | xargs sed -i "s|/opt/freeware/bin/perl_32_32|/opt/freeware/bin/perl_32|g"
fi

sed -i "s|/opt|${RPM_BUILD_ROOT}/opt|g" ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf

if [ "`id -u`" -eq "0" ]; then
    su apache -c "(t/TEST || true)"
else
    (t/TEST || true)
fi

# Restore right conf
mv ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf.orig ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf/httpd.conf
if [ ${OBJECT_MODE} -eq 32 ]
then
  cp ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd_orig    ${RPM_BUILD_ROOT}/%{_prefix}/sbin/httpd
fi

cd ../..
}

check_httpd 64

check_httpd 32


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
if [ "$1" = "0" ]; then
    /etc/rc.d/init.d/%{name} stop > /dev/null 2>&1

    # remove "apache" user and group
    /usr/sbin/rmuser -p apache || :
    /usr/sbin/rmgroup apache || :
fi


%preun manual
if [ "$1" = "0" ]; then
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
    /usr/bin/sed -e "s|Include conf/extra/httpd-manual.conf|#Include conf/extra/httpd-manual.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
    /usr/bin/sed -e "s|Include conf/extra/httpd-manual.conf|#Include conf/extra/httpd-manual.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post
echo "This version of httpd has 32bit and 64bit support"
echo "To start 64bit httpd use : /opt/freeware/sbin/apachectl_64 start"
if [ -f %{_sysconfdir}/httpd/conf/httpd.conf ];then
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf | \
    /usr/bin/sed -e "s|#LoadModule mpm_prefork_module /opt/freeware/lib/httpd/modules/mod_mpm_prefork.so|LoadModule mpm_prefork_module /opt/freeware/lib/httpd/modules/mod_mpm_prefork.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf | \
    /usr/bin/sed -e "s|LoadModule mpm_worker_module /opt/freeware/lib/httpd/modules/mod_mpm_worker.so|#LoadModule mpm_worker_module /opt/freeware/lib/httpd/modules/mod_mpm_worker.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
fi
    

%post manual
if [ "$1" = "1" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#Include conf/extra/httpd-manual.conf|Include conf/extra/httpd-manual.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
fi

/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#Include conf/extra/httpd-manual.conf|Include conf/extra/httpd-manual.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"

if [ "$1" = "2" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#LoadModule negotiation_module /opt/freeware/lib/httpd/modules/mod_negotiation.so|LoadModule negotiation_module /opt/freeware/lib/httpd/modules/mod_negotiation.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#LoadModule negotiation_module /opt/freeware/lib64/httpd/modules/mod_negotiation.so|LoadModule negotiation_module /opt/freeware/lib64/httpd/modules/mod_negotiation.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi


%preun -n mod_ssl
if [ "$1" = "0" ]; then
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
    /usr/bin/sed -e "s|Include conf/extra/httpd-ssl.conf_32|#Include conf/extra/httpd-ssl.conf_32|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32

    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
    /usr/bin/sed -e "s|Include conf/extra/httpd-ssl.conf_64|#Include conf/extra/httpd-ssl.conf_64|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64

    if [ -f %{_sysconfdir}/httpd/conf/ssl.key/server.key ] ; then
        /usr/bin/rm -f %{_sysconfdir}/httpd/conf/ssl.key/server.key
    fi

    if [ -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt ] ; then
        /usr/bin/rm -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt
    fi
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post -n mod_ssl
if [ "$1" = "1" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#Include conf/extra/httpd-ssl.conf|Include conf/extra/httpd-ssl.conf_32|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
fi

if [ "$1" = "2" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#LoadModule socache_shmcb_module /opt/freeware/lib/httpd/modules/mod_socache_shmcb.so|LoadModule socache_shmcb_module /opt/freeware/lib/httpd/modules/mod_socache_shmcb.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#LoadModule socache_shmcb_module /opt/freeware/lib64/httpd/modules/mod_socache_shmcb.so|LoadModule socache_shmcb_module /opt/freeware/lib64/httpd/modules/mod_socache_shmcb.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi

/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#Include conf/extra/httpd-ssl.conf_64|Include conf/extra/httpd-ssl.conf_64|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64

umask 077

if [ ! -f %{_sysconfdir}/httpd/conf/ssl.key/server.key ] ; then
    openssl genrsa -rand /etc/passwd:/etc/group:/etc/security/passwd:/etc/security/group 1024 > %{_sysconfdir}/httpd/conf/ssl.key/server.key 2> /dev/null
fi

FQDN=`hostname`
if [ "x${FQDN}" = "x" ]; then
    FQDN=localhost.localdomain
fi

if [ ! -f %{_sysconfdir}/httpd/conf/ssl.crt/server.crt ] ; then
    /usr/bin/cat << EOF | openssl req -new -key %{_sysconfdir}/httpd/conf/ssl.key/server.key -x509 -days 365 -out %{_sysconfdir}/httpd/conf/ssl.crt/server.crt 2> /dev/null
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


%preun -n mod_lua
if [ "$1" = "0" ]; then
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
    /usr/bin/sed -e "s|LoadModule lua_module /opt/freeware/lib/httpd/modules/mod_lua.so|#LoadModule lua_module /opt/freeware/lib/httpd/modules/mod_lua.so|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
    /usr/bin/sed -e "s|LoadModule lua_module /opt/freeware/lib64/httpd/modules/mod_lua.so|#LoadModule lua_module /opt/freeware/lib64/httpd/modules/mod_lua.so|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post -n mod_lua
if [ "$1" = "1" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#LoadModule lua_module /opt/freeware/lib/httpd/modules/mod_lua.so|LoadModule lua_module /opt/freeware/lib/httpd/modules/mod_lua.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
fi
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#LoadModule lua_module /opt/freeware/lib64/httpd/modules/mod_lua.so|LoadModule lua_module /opt/freeware/lib64/httpd/modules/mod_lua.so|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"

%if %{with proxy_html}
%preun -n mod_proxy_html
if [ "$1" = "0" ]; then
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
    /usr/bin/sed -e "s|Include conf/extra/proxy-html.conf|#Include conf/extra/proxy-html.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
    /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
    /usr/bin/sed -e "s|Include conf/extra/proxy-html.conf|#Include conf/extra/proxy-html.conf|" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
    /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%post -n mod_proxy_html
if [ "$1" = "1" ]; then
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
/usr/bin/sed -e "s|#Include conf/extra/proxy-html.conf|Include conf/extra/proxy-html.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
fi
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#Include conf/extra/proxy-html.conf|Include conf/extra/proxy-html.conf|" \
  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
%endif


%post -n mod_http2
if [ "$1" = "1" ]; then
  /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
  /usr/bin/sed -e "s|#LoadModule http2_module /opt/freeware/lib/httpd/modules/mod_http2.so|LoadModule http2_module /opt/freeware/lib/httpd/modules/mod_http2.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
  /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
  /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
  /usr/bin/sed -e "s|#LoadModule http2_module /opt/freeware/lib64/httpd/modules/mod_http2.so|LoadModule http2_module /opt/freeware/lib64/httpd/modules/mod_http2.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
  /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "To use http2, disable mpm_prefork_module and enable mpm_worker_module in /opt/freeware/etc/httpd/conf/httpd.conf"
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%preun -n mod_http2
if [ "$1" = "0" ]; then
  /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_32 | \
  /usr/bin/sed -e "s|LoadModule http2_module /opt/freeware/lib/httpd/modules/mod_http2.so|#LoadModule http2_module /opt/freeware/lib/httpd/modules/mod_http2.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32
  /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_32 %{_sysconfdir}/httpd/conf/httpd.conf_32
  /usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
  /usr/bin/sed -e "s|LoadModule http2_module /opt/freeware/lib64/httpd/modules/mod_http2.so|#LoadModule http2_module /opt/freeware/lib64/httpd/modules/mod_http2.so|" \
    > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
  /usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)

%doc 32bit/ABOUT_APACHE 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE 32bit/README 32bit/VERSIONING

%dir %{_sysconfdir}/httpd
%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf_32
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf_64
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%dir %{_sysconfdir}/httpd/conf/extra
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-autoindex.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-default.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-info.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-languages.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-mpm.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-multilang-errordoc.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-userdir.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-vhosts.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/proxy-html.conf
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
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/proxy-html.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf_32
%config(noreplace) %{_sysconfdir}/httpd/conf/original/httpd.conf_64

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

/etc/rc.d/init.d/httpd
/etc/rc.d/rc2.d/Shttpd
/etc/rc.d/rc2.d/Khttpd
/etc/rc.d/rc3.d/Shttpd
/etc/rc.d/rc3.d/Khttpd

%{_bindir}/ab*
%{_bindir}/htdbm*
%{_bindir}/htdigest*
%{_bindir}/htpasswd*
%{_bindir}/httxt2dbm*
%{_bindir}/logresolve*

%{_sbindir}/apachectl*
%{_sbindir}/fcgistarter*
%{_sbindir}/htcacheclean*
%{_sbindir}/httpd*
%{_sbindir}/rotatelogs*
%attr(4510,root,%{suexec_caller}) %{_sbindir}/suexec*

%dir %{_libdir}/httpd
%dir %{_libdir}64/httpd
%dir %{_libdir}/httpd/modules
%dir %{_libdir}64/httpd/modules
# everything but mod_ssl.so:
%{_libdir}/httpd/modules/httpd.exp
%{_libdir}64/httpd/modules/httpd.exp
%{_libdir}/httpd/modules/mod_[a-g]*.so
%{_libdir}64/httpd/modules/mod_[a-g]*.so
%{_libdir}/httpd/modules/mod_[i-k]*.so
%{_libdir}64/httpd/modules/mod_[i-k]*.so
%{_libdir}/httpd/modules/mod_h[a-f]*.so
%{_libdir}64/httpd/modules/mod_h[a-f]*.so
%{_libdir}/httpd/modules/mod_l[a-o]*.so
%{_libdir}64/httpd/modules/mod_l[a-o]*.so
%{_libdir}/httpd/modules/mod_[m-o]*.so
%{_libdir}64/httpd/modules/mod_[m-o]*.so
%{_libdir}/httpd/modules/mod_proxy.so
%{_libdir}64/httpd/modules/mod_proxy.so
%{_libdir}/httpd/modules/mod_proxy_[a-f]*.so
%{_libdir}64/httpd/modules/mod_proxy_[a-f]*.so
%{_libdir}/httpd/modules/mod_proxy_http.so
%{_libdir}64/httpd/modules/mod_proxy_http.so
%{_libdir}/httpd/modules/mod_proxy_[i-z]*.so
%{_libdir}64/httpd/modules/mod_proxy_[i-z]*.so
%{_libdir}/httpd/modules/mod_[q-r]*.so
%{_libdir}64/httpd/modules/mod_[q-r]*.so
%{_libdir}/httpd/modules/mod_s[eloptu]*.so
%{_libdir}64/httpd/modules/mod_s[eloptu]*.so
%{_libdir}/httpd/modules/mod_[t-w]*.so
%{_libdir}64/httpd/modules/mod_[t-w]*.so

%{_mandir}/man1/ab*
%{_mandir}/man1/[d,h,l]*
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
%attr(0700,apache,apache) %dir %{localstatedir}/lib64/dav

%files devel
%defattr(-,root,system)
%{_includedir}/httpd
%{_sysconfdir}/httpd/build
%{_bindir}/apxs*
%{_bindir}/dbmmanage*
%{_sbindir}/checkgid*
%{_sbindir}/envvars*
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%dir %{_libdir}64/httpd/build
%{contentdir}/build
%{_libdir}/httpd/build/config.nice
%{_libdir}64/httpd/build/config.nice
%{_libdir}/httpd/build/*.mk
%{_libdir}64/httpd/build/*.mk
%{_libdir}/httpd/build/instdso.sh
%{_libdir}64/httpd/build/instdso.sh
%{_libdir}/httpd/build/mkdir.sh
%{_libdir}64/httpd/build/mkdir.sh


%files manual
%defattr(-,root,system)
%dir %{contentdir}/manual
%{contentdir}/manual/*
%dir %{_sysconfdir}/httpd/conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-manual.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-manual.conf


%files -n mod_lua
%defattr(-,root,system)
%{_libdir}/httpd/modules/mod_lua.so
%{_libdir}64/httpd/modules/mod_lua.so


%files -n mod_http2
%defattr(-,root,system)
%{_libdir}/httpd/modules/mod_http2.so
%{_libdir}64/httpd/modules/mod_http2.so


%if %{with proxy_html}
%files -n mod_proxy_html
%defattr(-,root,system)
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}64/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%{_libdir}64/httpd/modules/mod_xml2enc.so
%endif


%files -n mod_ssl
%defattr(-,root,system)
%{_libdir}/httpd/modules/mod_ssl.so
%{_libdir}64/httpd/modules/mod_ssl.so
%attr(0700,root,system) %dir %{_sysconfdir}/httpd/conf/ssl.crl
%attr(0700,root,system) %dir %{_sysconfdir}/httpd/conf/ssl.crt
%attr(0700,root,system) %dir %{_sysconfdir}/httpd/conf/ssl.csr
%attr(0700,root,system) %dir %{_sysconfdir}/httpd/conf/ssl.key
%attr(0700,root,system) %dir %{_sysconfdir}/httpd/conf/ssl.prm
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_32
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-ssl.conf_64
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf_32
%config(noreplace) %{_sysconfdir}/httpd/conf/original/extra/httpd-ssl.conf_64
%attr(0700,apache,system) %dir %{localstatedir}/cache/mod_ssl
%attr(0600,apache,system) %{localstatedir}/cache/mod_ssl/scache.dir
%attr(0600,apache,system) %{localstatedir}/cache/mod_ssl/scache.pag
%attr(0600,apache,system) %{localstatedir}/cache/mod_ssl/scache.sem
%attr(0700,apache,system) %dir %{localstatedir}/cache/mod_proxy


%changelog
* Mon Jun 28 2021 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 2.4.48-2
- Create build_httpd and check_httpd
- Manage 32bit tests to work

* Fri Jun 25 2021 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 2.4.48-1
- Update to 2.4.48

* Fri Oct 23 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 2.4.46-1
- Update to 2.4.46

* Mon Oct 19 2020 Étienne Guesnet <etienne.guesnet@atos.net> 2.4.41-3
- Remove db module and dependency

* Thu Feb 13 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 2.4.41-2
- Port on Bullfreeware
- Add nghttp dependency
- Add conditionnal for proxy_html
- Rebuild with new apr
- Add check
- Bullfreeware OpenSSL removal

* Thu Sep 26 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.41-1
- Update to fix CVE-2019-9517,CVE-2019-10098,CVE-2019-10082,CVE-2019-10092,CVE-2019-10081

* Tue Jun 18 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.39-2
- Rebuild with libnghttp2

* Tue Apr 23 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.39-1
- Updated to fix CVE-2019-0211

* Mon Mar 04 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.38-2
- Rebuilt with apr and apr-util rpms
- Fix httpd 64bit issues

* Tue Feb 05 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.38-1
- Update to fix
- CVE-2018-17199
- CVE-2018-17189
- CVE-2019-0190

* Wed Nov 28 2018 Reshma V Kumar <reskumar@in.ibm.com> 2.4.37-2
- Rebuild with gcc

* Mon Nov 12 2018 Reshma V Kumar <reskumar@in.ibm.com> 2.4.37-1
- Updated to version 2.4.37 to fix security vulnerability

* Mon Jul 30 2018 Reshma V Kumar <reskumar@in.ibm.com> 2.4.34-1
- Updated to version 2.4.34 to fix security vulnerability

* Wed Jun 6 2018 Nitish K Mishra <nitismis@in.ibm.com> 2.4.33-1
- Update for security vulnerability

* Mon Mar 21 2016 Ayappan P <ayappap2@in.ibm.com> 2.4.18-1
- Update to version 2.4.18

* Tue Dec 09 2014 Gerard Visiedo <gerard.visiedo@bull.net> 2.4.10-1
- Update to version 2.4.10
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

