Summary: The PHP HTML-embedded scripting language
Name: php
Version: 7.0.3
Release: 2
License: The PHP License v3.01
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{name}-%{version}.tar.bz2
Source1: %{name}.conf
Source2: %{name}.ini
Patch0: %{name}-%{version}-aix-build.patch
Patch1: %{name}-%{version}-aix-network.patch
Patch2: %{name}-%{version}-aix-setrlimit.patch
Patch3: %{name}-%{version}-aix-strfmon.patch
Patch4: %{name}-%{version}-aix-tests.patch
Patch5: %{name}-%{version}-aix-trailing-slash.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

%define contentdir /var/www

BuildRequires: make
BuildRequires: bzip2 >= 1.0.2-4
BuildRequires: curl-devel >= 7.47.1
BuildRequires: gd-devel >= 2.0.35
#BuildRequires: httpd-devel >= 2.4
BuildRequires: libiconv >= 1.14-2
BuildRequires: libtool-ltdl-devel >= 1.5.26-1
BuildRequires: libxml2-devel >= 2.7.8-3
BuildRequires: openssl-devel >= 1.0.2g-1
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: zlib-devel >= 1.2.3-3

%description
Dummy description to satisfy RPM.

%package mod_php
Summary: The PHP HTML-embedded scripting language module for Apache V2.4.X
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.2-4
Requires: curl >= 7.47.1-1
#Requires: httpd >= 2.4
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl >= 1.5.26-1
Requires: libxml2 >= 2.7.8-3
Requires: openldap >= 2.4.23
Requires: openssl >= 1.0.2g-1
Requires: zlib >= 1.2.3-3
Provides: mod_php = %{version}-%{release}
Provides: php = %{version}-%{release}

%description mod_php
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The mod_php package contains the module which adds support for the PHP
language to Apache HTTP Server V2.4.X.


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.2-4
Requires: curl >= 7.47.1-1
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl >= 1.5.26-1
Requires: libxml2 >= 2.7.8-3
Requires: openldap >= 2.4.23
Requires: openssl >= 1.0.2g-1
Requires: zlib >= 1.2.3-3
Provides: %{name}-cgi = %{version}-%{release}


%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, %{_bindir}/php, and the CGI interface.


%package common
Group: Development/Languages
Summary: Common files for PHP


%description common
The php-common package contains files used by both the php
package and the php-cli package.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: bzip2 >= 1.0.2-4
Requires: curl-devel >= 7.47.1-1
#Requires: httpd-devel >= 2.4
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl-devel >= 1.5.26-1
Requires: libxml2-devel >= 2.7.8-3
Requires: openldap-devel >= 2.4.23
Requires: openssl-devel >= 1.0.2g-1
Requires: pcre-devel >= 7.9-2
Requires: zlib-devel >= 1.2.3-3


%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.


%prep
%setup -q
%patch0 -p1 -b .build
%patch1 -p1 -b .network
%patch2 -p1 -b .setrlimit
%patch3 -p1 -b .strfmon
%patch4 -p1 -b .tests
%patch5 -p1 -b .trailing-slash


%build
export CC=/opt/freeware/bin/gcc
export CXX=/opt/freeware/bin/g++
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
export LIBPATH=/opt/freeware/lib:/usr/lib

# install extension modules in %{_libdir}/php/modules.
export EXTENSION_DIR=%{_libdir}/php/modules

# shell function to configure and build a PHP tree
buildphp() {
ln -sf ../configure
./configure \
 --cache-file=../config.php-7.0.3.aix.cache \
 --prefix=/opt/freeware \
 --with-config-file-path=/opt/freeware/etc \
 --with-config-file-scan-dir=/opt/freeware/etc/php.d \
 --disable-debug \
 --enable-shared \
 --enable-static \
 --without-pear \
 --with-openssl=/opt/freeware \
 --with-zlib \
 --with-bz2 \
 --with-curl=/opt/freeware \
 --with-gd \
 --with-freetype-dir=/opt/freeware \
 --with-jpeg-dir=/opt/freeware \
 --with-png-dir=/opt/freeware \
 --with-xpm-dir=no \
 --with-zlib-dir=/opt/freeware \
 --with-ldap=/opt/freeware \
 --enable-soap \
 --enable-bcmath \
 --enable-ftp \
 --enable-sockets \
 --enable-mbstring \
 --enable-zip \
 --with-iconv=/opt/freeware \
 --with-iconv-dir=/opt/freeware \
 --with-mysqli=mysqlnd \
 --enable-dom \
 --enable-json \
    $*
sed -e "s/^CFLAGS_CLEAN = /CFLAGS_CLEAN = -fPIC /" -i Makefile
sed -e "s/-fvisibility=hidden//" -i Makefile
make %{?_smp_mflags}
}


# build the command line and the CGI version of PHP
mkdir build-cgi
cd build-cgi
buildphp
#export http_proxy=""
#export https_proxy=""
#export TESTS="--offline"
#make test
cd ..


# build the Apache module
mkdir build-apache
cd build-apache
APXS=/opt/freeware/bin/apxs
# If IBM Apache LPP is installed, use it to build the Apache module
if [ -f /usr/IBMAHS/bin/apxs ]; then
    APXS=/usr/IBMAHS/bin/apxs
fi
buildphp \
    --with-apxs2=${APXS}
cd ..


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# unfortunately 'make install-sapi' does not seem to work for use, therefore
# we have to install the targets separately
cd build-cgi
for TARGET in install-cli install-build install-headers install-programs ; do
    make INSTALL_ROOT=${RPM_BUILD_ROOT} ${TARGET}
done

# install the php-cgi binary
cp sapi/cgi/php-cgi ${RPM_BUILD_ROOT}%{_bindir}
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi

# install the DSO
cd ../build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
cp .libs/libphp7.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.so
cd ..

# strip binaries
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/php
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/php-cgi
/usr/bin/strip ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.so

# install the Apache httpd config file for PHP
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf

# install the default configuration file and directories
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/php.ini
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf/php.ini
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php.d

# create the PHP extension modules directory
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/modules

# install the default icons
mkdir -p ${RPM_BUILD_ROOT}%{contentdir}/icons
chmod 755 ${RPM_BUILD_ROOT}%{contentdir}/icons
cp php.gif ${RPM_BUILD_ROOT}%{contentdir}/icons

# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%preun mod_php
removeFromHTTPDconf() {
    if [ -f $1 ]
    then
        grep -v "Include conf/extra/httpd-php.conf" $1 > $1.tmp
        [ -s $1.tmp ] && mv -f $1.tmp $1
        echo "Please restart your web server using: '$2 restart'"
    fi
}
preunAlternateLocation() {
    if [ -f $1/bin/httpd -a -d $1/conf ]
    then
        [ -f  $1/conf/extra/httpd-php.conf ] && rm -f $1/conf/extra/httpd-php.conf
        [ -f  $1/modules/libphp7.so ] && rm -f $1/modules/libphp7.so
	removeFromHTTPDconf $1/conf/httpd.conf $1/bin/apachectl
    fi
}
rm -rf /var/lib/php/session/*
removeFromHTTPDconf %{_sysconfdir}/httpd/conf/httpd.conf %{_prefix}/sbin/apachectl
# remove some files to work with apache2
preunAlternateLocation %{_prefix}/apache2
# remove some files to work with IBMAHS
preunAlternateLocation /usr/IBMAHS


%pre mod_php
# Verify if Apache 2.4.x is installed, as it is not handled by the RPM dependancy check (IBM Apache is installed via LPP, not via RPM)
(/usr/IBMAHS/bin/httpd -version 2>&1 ; %{_prefix}/sbin/httpd -version 2>&1 ;  %{_prefix}/apache2/httpd -version 2>&1) | grep -q "Apache/2.4"
if [ $? != 0 ]
then
    echo "Apache httpd version 2.4.x must be installed in /usr/IBMAHS/bin/httpd, %{_prefix}/bin/httpd or %{_prefix}/apache2/httpd"
    exit 1
fi


%post mod_php
slibclean
addToHTTPDconf() {
    if [ -f $1 ]
    then
        grep -v "Include conf/extra/httpd-php.conf" $1 > $1.tmp
        [ -s $1.tmp ] && mv -f $1.tmp $1
        echo "Include conf/extra/httpd-php.conf" >> $1
        echo "Please restart your web server using: '$2 restart'"
    fi
}
postAlternateLocation() {
    if [ -f $1/bin/httpd -a -d $1/conf -a `$1/bin/httpd -version 2>&1 | grep "Apache/2.4" | wc -l` = "1" ]
    then
        [ -d $1/modules ] && cp -p %{_libdir}/httpd/modules/libphp7.so $1/modules
        [ -d $1/conf/extra ] && cp -p  %{_sysconfdir}/httpd/conf/extra/httpd-php.conf $1/conf/extra
        addToHTTPDconf $1/conf/httpd.conf $1/bin/apachectl
    fi
}
if [ -f %{_prefix}/sbin/httpd -a `%{_prefix}/sbin/httpd -version 2>&1 | grep "Apache/2.4" | wc -l` = "1" ]
then
    addToHTTPDconf %{_sysconfdir}/httpd/conf/httpd.conf %{_prefix}/sbin/apachectl
fi
# copy some files to work with apache2
postAlternateLocation %{_prefix}/apache2
# copy some files to work with IBMAHS
postAlternateLocation /usr/IBMAHS


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files mod_php
%defattr(-,root,system)
%{_libdir}/httpd/modules/libphp7.so
%attr(0770,root,nobody) %dir /var/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf
%{contentdir}/icons/php.gif


%files common
%defattr(-,root,system)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir /var/lib/php
%dir %{_libdir}/php/pear


%files cli
%defattr(-,root,system)
%{_bindir}/php
%{_bindir}/php-cgi
#%{_mandir}/man1/php.1
/usr/bin/php
/usr/bin/php-cgi


%files devel
%defattr(-,root,system)
%dir %{_libdir}/php
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build
#%{_mandir}/man1/php-config.1
#%{_mandir}/man1/phpize.1
/usr/bin/php-config
/usr/bin/phpize
/usr/include/*


%changelog
* Mon Mar 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.3-2
- updated dependencies to OpenSSL 1.0.2g and curl 7.47.1 (older versions of curl
  package does not work with OpenSSL 1.0.2g, and older versions of OpenSSL are
  unsecure)
- fixed mod_php package summary
- added mbstring

* Thu Mar 15 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.3-1
- updated to version 7.0.3
- added support for IBM Apache HTTP Server

* Fri Sep 19 2014 Michael Perzl <michael@perzl.org> - 5.5.17-1
- updated to version 5.5.17

* Sat Aug 23 2014 Michael Perzl <michael@perzl.org> - 5.5.16-1
- updated to version 5.5.16

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.15-1
- updated to version 5.5.15

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.14-1
- updated to version 5.5.14

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.13-1
- updated to version 5.5.13

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.12-1
- updated to version 5.5.12

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.11-1
- updated to version 5.5.11

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.10-1
- updated to version 5.5.10

* Thu Aug 21 2014 Michael Perzl <michael@perzl.org> - 5.5.9-1
- updated to version 5.5.9

* Sat Jan 11 2014 Michael Perzl <michael@perzl.org> - 5.5.8-1
- updated to version 5.5.8

* Sat Jan 11 2014 Michael Perzl <michael@perzl.org> - 5.5.7-1
- updated to version 5.5.7

* Mon Nov 18 2013 Michael Perzl <michael@perzl.org> - 5.5.6-1
- updated to version 5.5.6

* Wed Oct 23 2013 Michael Perzl <michael@perzl.org> - 5.5.5-1
- updated to version 5.5.5

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 5.5.4-1
- updated to version 5.5.4

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 5.5.3-1
- updated to version 5.5.3

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 5.5.2-1
- updated to version 5.5.2

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 5.5.1-2
- enabled '--enable-pdo'' option

* Mon Jul 22 2013 Michael Perzl <michael@perzl.org> - 5.5.1-1
- updated to version 5.5.1

* Mon Jun 24 2013 Michael Perzl <michael@perzl.org> - 5.5.0-1
- updated to version 5.5.0

* Thu Jun 20 2013 Michael Perzl <michael@perzl.org> - 5.4.16-1
- updated to version 5.4.16

* Fri May 24 2013 Michael Perzl <michael@perzl.org> - 5.4.15-1
- updated to version 5.4.15

* Mon Apr 15 2013 Michael Perzl <michael@perzl.org> - 5.4.14-1
- updated to version 5.4.14

* Mon Mar 18 2013 Michael Perzl <michael@perzl.org> - 5.4.13-1
- updated to version 5.4.13

* Mon Feb 25 2013 Michael Perzl <michael@perzl.org> - 5.4.12-1
- updated to version 5.4.12

* Wed Jan 23 2013 Michael Perzl <michael@perzl.org> - 5.4.11-1
- updated to version 5.4.11

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 5.4.10-1
- updated to version 5.4.10

* Tue Dec 18 2012 Michael Perzl <michael@perzl.org> - 5.4.9-2
- added PFM support
- enabled Zip read/write support
- changed OpenSSL dependency to latest version to avoid version mismatches

* Thu Dec 06 2012 Michael Perzl <michael@perzl.org> - 5.4.9-1
- added LDAP support and thus introduced a dependency on openldap
- updated to version 5.4.9

* Fri Nov 23 2012 Michael Perzl <michael@perzl.org> - 5.4.8-2
- fixed wrong dependency on libbz2.so

* Fri Nov 16 2012 Michael Perzl <michael@perzl.org> - 5.4.8-1
- updated to version 5.4.8

* Mon Sep 17 2012 Michael Perzl <michael@perzl.org> - 5.4.7-1
- updated to version 5.4.7

* Tue Aug 28 2012 Michael Perzl <michael@perzl.org> - 5.4.6-1
- updated to version 5.4.6

* Tue Aug 28 2012 Michael Perzl <michael@perzl.org> - 5.4.5-1
- updated to version 5.4.5

* Tue Aug 28 2012 Michael Perzl <michael@perzl.org> - 5.4.4-1
- updated to version 5.4.4

* Tue Aug 28 2012 Michael Perzl <michael@perzl.org> - 5.4.3-2
- restructured package to better adapt to different Apache (httpd) versions

* Mon Jun 04 2012 Michael Perzl <michael@perzl.org> - 5.4.3-1
- updated to version 5.4.3
- removed dependency on external GD library as PHP can only be compiled with
  the packaged (and modified) GD library

* Fri May 11 2012 Gerard Visiedo <gerard.visiedo@bull.net> 5.3.10-1
- Port on Aix61

* Fri Feb 17 2012 Michael Perzl <michael@perzl.org> - 5.3.10-1
- updated to version 5.3.10

* Wed Aug 24 2011 Michael Perzl <michael@perzl.org> - 5.3.8-1
- updated to version 5.3.8

* Tue Aug 23 2011 Michael Perzl <michael@perzl.org> - 5.3.7-1
- updated to version 5.3.7, added patch for php_crypt_r()

* Tue Aug 23 2011 Michael Perzl <michael@perzl.org> - 5.3.6-2
- added "--enable-sockets" and "--with-mysqli=mysqlnd" to configure options

* Wed May 18 2011 Michael Perzl <michael@perzl.org> - 5.3.6-1
- updated to version 5.3.6

* Wed May 18 2011 Michael Perzl <michael@perzl.org> - 5.3.5-2
- fixed wrong dependency on bzip2-devel of php-devel (needs bzip2 only)

* Fri Jan 07 2011 Michael Perzl <michael@perzl.org> - 5.3.5-1
- updated to version 5.3.5

* Tue Dec 14 2010 Michael Perzl <michael@perzl.org> - 5.3.4-1
- updated to version 5.3.4

* Fri Jul 23 2010 Michael Perzl <michael@perzl.org> - 5.3.3-1
- updated to version 5.3.3

* Tue Apr 13 2010 Michael Perzl <michael@perzl.org> - 5.3.2-1
- updated to version 5.3.2

* Tue Mar 02 2010 Michael Perzl <michael@perzl.org> - 5.2.13-1
- updated to version 5.2.13

* Thu Feb 18 2010 Michael Perzl <michael@perzl.org> - 5.2.12-2
- enable fastcgi for the CLI version

* Tue Jan 19 2010 Michael Perzl <michael@perzl.org> - 5.2.12-1
- updated to version 5.2.12

* Fri Nov 27 2009 Michael Perzl <michael@perzl.org> - 5.2.11-1
- updated to version 5.2.11

* Thu Nov 26 2008 Michael Perzl <michael@perzl.org> - 5.2.8-1
- updated to version 5.2.8

* Fri May 02 2008 Michael Perzl <michael@perzl.org> - 5.2.6-1
- updated to version 5.2.6

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 5.2.5-2
- some minor spec file fixes

* Mon Dec 03 2007 Michael Perzl <michael@perzl.org> - 5.2.5-1
- first version for AIX V5.1 and higher
