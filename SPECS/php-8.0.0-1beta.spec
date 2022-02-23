# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


# Default compiler gcc
# To use xlc : --define 'gcc_compiler=0'
# %%{!?gcc_compiler:%define gcc_compiler 1}
%bcond_without gcc_compiler


%define beta_message "THIS IS A BETA VERSION. DO NOT USE IT IN PRODUCTION."


# Deprecated
%bcond_with      mod_php
# No firebird available
%bcond_with   firebird
# configure error with U8T
%bcond_with   imap
# No sodium available
%bcond_with   sodium
# No aspell available
%bcond_with   pspell
# No tidy available
%bcond_with   tidy
# Will probably work, but we do not want to add db libs
%bcond_with db
# Used with db only
%bcond_with   lmdb
# No snmp available
%bcond_with snmp
# No enchant available
%bcond_with enchant
# intl (gettext) needs icu in php
%bcond_with intl

Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 8.0.0
Release: 1beta
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
Group: Development/Languages
URL: http://www.php.net/

Source0: https://www.php.net/distributions/%{name}-%{version}.tar.xz
Source1: %{name}.conf
Source2: %{name}.ini
Source3: %{name}64.ini
Source4: %{name}.conf_64
Source5: php-fpm.conf
Source6: www.conf

Source100: %{name}-%{version}-%{release}.build.log

# TODO compare with Fedora
Patch0: %{name}-7.2.19-aixconfig.patch
Patch1: php-8.0.0-build_export.patch
Patch2: %{name}-7.2.19-aix-network.patch
Patch3: %{name}-8.0.0-aix-setrlimit.patch
Patch4: %{name}-7.3.10-aix-tests.patch
Patch5: %{name}-8.0.0-aix-trailing-slash.patch
Patch6: %{name}-7.4.2-phpini.patch

#Patch to load mysqlnd.so before mysqli.so and pdo_mysql.so as they have dependency on mysqlnd.
#Otherwise loading of modules that are dependent on mysqlnd fail and hence the testcases fail
Patch7: php-8.0.0-mysqlnd_build_order.patch

# Name conflict between a temp php variable and an AIX system define.
Patch8: %{name}-8.0.0-rem_size.patch
# PHPDBG does not found .o
Patch9: php-8.0.0-PHPDBG_found_object.patch
# Workaround for recvmsg freeze bug
Patch10: php-8.0.0-workaround_recvmsg_freeze.patch
# The watch test hangs; XFAIL -> SKIP
Patch11: php-8.0.0-skip_watch_hang.patch
# Other hang, with waitpid / kill
Patch12: php-8.0.0-skip_waitpid_rusage.patch 
# Other hang, with fwrite
Patch13: php-8.0.0-skip_stream_ssl_hang.patch

%define _libdir64 %{_prefix}/lib64

%define contentdir /var/www

BuildRequires: make
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: sed, findutils
BuildRequires: bzip2-devel >= 1.0.8-4
BuildRequires: curl-devel >= 7.47.1
BuildRequires: gettext-devel
BuildRequires: gd-devel >= 2.1.1
BuildRequires: httpd-devel >= 2.4.46
BuildRequires: libiconv >= 1.16-5
BuildRequires: libtool-ltdl-devel >= 2.4.6-3
BuildRequires: libxml2-devel >= 2.9.5-1
BuildRequires: libzip-devel >= 1.7.0
BuildRequires: oniguruma-devel
BuildRequires: openldap-devel >= 2.4.44
BuildRequires: pcre2-devel >= 10.30
BuildRequires: sqlite-devel >= 3.33.0
BuildRequires: xz-devel >= 5.2.3
BuildRequires: zlib-devel >= 1.2.11-5

%if %{with zts}
Provides: php-zts = %{version}-%{release}
%endif

%if %{with mod_php}
Requires: php-mod_php
%endif
Requires: php-common     = %{version}-%{release}
# For backwards-compatibility, pull the "php" command
Recommends: php-cli      = %{version}-%{release}
# httpd have threaded MPM by default
Recommends: php-fpm      = %{version}-%{release}
# as "php" is now mostly a meta-package, commonly used extensions
# reduce diff with "dnf module install php"
Recommends: php-json     = %{version}-%{release}
Recommends: php-mbstring = %{version}-%{release}
Recommends: php-opcache  = %{version}-%{release}
Recommends: php-pdo      = %{version}-%{release}
%if %{with sodium}
Recommends: php-sodium   = %{version}-%{release}
%endif
Recommends: php-xml      = %{version}-%{release}


%description
%{beta_message}

PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

This package is a meta-package with the usual Recommends and Requires.

%if %{with gcc_compiler}
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif

%if %{with mod_php}
%package mod_php
Summary: The PHP HTML-embedded scripting language module for Apache V2.4.X
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}

Provides: mod_php = %{version}-%{release}
Provides: php = %{version}-%{release}

%description mod_php
%{beta_message}

PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

This package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server when
running in prefork mode. This module is deprecated.
%endif


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: %{name}-common = %{version}-%{release}

Provides: %{name}-cgi = %{version}-%{release}

%description cli
%{beta_message}

The php-cli package contains the command-line interface 
executing PHP scripts, %{_bindir}/php, and the CGI interface.


%package dbg
Summary: The interactive PHP debugger
Requires: php-common = %{version}-%{release}

%description dbg
%{beta_message}

The php-dbg package contains the interactive PHP debugger.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
Requires: php-common = %{version}-%{release}
Provides: php(httpd)

%description fpm
%{beta_message}

PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.


%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP and BSD

Requires: bzip2 >= 1.0.8-4
Requires: curl >= 7.47.1
Requires: gettext
Requires: httpd >= 2.4.46
Requires: libgcc >= 8.4.0
Requires: libiconv >= 1.16-2
Requires: libtool-ltdl >= 2.4.6-3
Requires: libxml2 >= 2.9.5-1
Requires: libzip >= 1.7.0
Requires: openldap >= 2.4.45
Requires: sqlite >= 3.33.0
Requires: oniguruma
Requires: xz-libs >= 5.2.3-1
Requires: zlib >= 1.2.11-5

%description common
%{beta_message}

The php-common package contains files used by both the php
package and the php-cli package.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions

Requires: make
Requires: gcc
Requires: gcc-c++
# see "php-config --libs"
Requires: krb5-devel
Requires: libxml2-devel
Requires: pcre2-devel
Requires: zlib-devel

%description devel
%{beta_message}

The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP
Requires:  php-common = %{version}-%{release}

%description opcache
%{beta_message}

The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.

%if %{with imap}
%package imap
Summary: A module for PHP applications that use IMAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}

%description imap
%{beta_message}

The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif


%package ldap
Summary: A module for PHP applications that use LDAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
Requires: openldap-devel
Requires: cyrus-sasl-devel
BuildRequires: openldap-devel
BuildRequires: cyrus-sasl-devel

%description ldap
%{beta_message}

The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.


%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}
Provides: php(pdo-abi) = %{pdover}
Provides: php-pdo_sqlite, php-pdo_sqlite

%description pdo
%{beta_message}

The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.


%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
Requires: libgcc >= 8.3.0-1
Provides: php_database
Provides: php-mysqli = %{version}-%{release}
Provides: php-pdo_mysql

%description mysqlnd
%{beta_message}

The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver


%package pgsql
Summary: A PostgreSQL database module for PHP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
BuildRequires: krb5-devel
BuildRequires: postgresql-devel
BuildRequires: postgresql-libs
Requires: postgresql-libs

%description pgsql
%{beta_message}

The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.


%package process
Summary: Modules for PHP script using system process interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}

%description process
%{beta_message}

The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.


%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: php-pdo = %{version}-%{release}
Provides: php_database
Provides: php-pdo_odbc, php-pdo_odbc
BuildRequires: unixODBC-devel >= 2.3.7
Requires: unixODBC >= 2.3.7

%description odbc
%{beta_message}

The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.


%package soap
Summary: A module for PHP applications that use the SOAP protocol
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}

%description soap
%{beta_message}

The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.


%if %{with firebird}
%package pdo-firebird
Summary: PDO driver for Interbase/Firebird databases
# All files licensed under PHP version 3.01
License: PHP
# for fb_config command
BuildRequires:  firebird-devel
Requires: php-pdo = %{version}-%{release}
Provides: php-pdo_firebird

%description pdo-firebird
%{beta_message}

The php-pdo-firebird package contains the PDO driver for
Interbase/Firebird databases.
%endif


%if %{with snmp}
%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}, net-snmp
BuildRequires: net-snmp-devel

%description snmp
%{beta_message}

The php-snmp package contains a dynamic shared object that will add
support for querying SNMP devices to PHP.  PHP is an HTML-embeddable
scripting language. If you need SNMP support for PHP applications, you
will need to install this package and the php package.
%endif


%package xml
Summary: A module for PHP applications which use XML
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
BuildRequires: libxslt-devel
Requires: libxslt 


%description xml
%{beta_message}

The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.


%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and OpenLDAP
Requires: php-common = %{version}-%{release}

%description mbstring
%{beta_message}

The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.


%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libgd is licensed under BSD
License: PHP and BSD
Requires: %{name}-common = %{version}-%{release}
BuildRequires: gd-devel >= 2.1.1

%description gd
%{beta_message}

The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.


%package bcmath
Summary: A module for PHP applications for using the bcmath library
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common = %{version}-%{release}

%description bcmath
%{beta_message}

The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.


%package gmp
Summary: A module for PHP applications for using the GNU MP library
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common = %{version}-%{release}

%description gmp
%{beta_message}

These functions allow you to work with arbitrary-length integers
using the GNU MP library.


%if %{with db}
%package dba
Summary: A database abstraction layer module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
BuildRequires db-devel
BuildRequires: tokyocabinet-devel
%if %{with lmdb}
BuildRequires: lmdb-devel
%endif
Requires: php-common = %{version}-%{release}

%description dba
%{beta_message}

The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.
%endif


%if %{with tidy}
%package tidy
Summary: Standard PHP module provides tidy library support
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
BuildRequires: libtidy-devel

%description tidy
%{beta_message}

The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.
%endif


%if %{with db}
%package pdo-dblib
Summary: PDO driver for Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
BuildRequires: freetds-devel

%description pdo-dblib
%{beta_message}

The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS library.
%endif


%if %{with pspell}
%package pspell
Summary: A module for PHP applications for using pspell interfaces
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0

%description pspell
%{beta_message}

The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.
%endif


%if %{with intl}
%package intl
Summary: Internationalization extension for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
BuildRequires: gettext-devel
Requires: gettext

%description intl
%{beta_message}

The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.
%endif


%if %{with enchant}
%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common = %{version}-%{release}

%description enchant
%{beta_message}

The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif

# Curently empty package
%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Requires: php-common = %{version}-%{release}

%description json
%{beta_message}

The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.


%if %{with sodium}
%package sodium
Summary: Wrapper for the Sodium cryptographic library
# All files licensed under PHP version 3.0.1
License: PHP

Requires: php-common = %{version}-%{release}

%description sodium
%{beta_message}

The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.
%endif


%package ffi
Summary: Foreign Function Interface
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
Requires: libffi
BuildRequires: libffi-devel


%description ffi
%{beta_message}

FFI is one of the features that made Python and LuaJIT very useful for fast
prototyping. It allows calling C functions and using C data types from pure
scripting language and therefore develop “system code” more productively.

For PHP, FFI opens a way to write PHP extensions and bindings to C libraries
in pure PHP.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .aixconfig
%patch1 -p1 -b .build_export
%patch2 -p1 -b .network
%patch3 -p1 -b .setrlimit
%patch4 -p1 -b .tests
%patch5 -p1 -b .trailing-slash
# Apply following to 64bit only
# %patch6 -p1 -b .php64_ini
# Patch apply to makefile only!
%patch7 -p1 -b .mysqlnd
%patch8 -p1 -b .rem_size
%patch9 -p1 -b .phpdbg_object
%patch10 -p1 -b .workaround_recvmsg
%patch11 -p1 -b .skip_watch_hang
%patch12 -p1 -b .skip_waitpid
%patch13 -p1 -b .skip_stream_ssl


# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/bcmath/libbcmath/LICENSE libbcmath_LICENSE
cp ext/date/lib/LICENSE.rst timelib_LICENSE

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/

# patch for php64.ini
cd 64bit
%patch6 -p1 -b .php64_ini
cd ..


%build
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export PATH=/opt/freeware/bin:$PATH
export CFLAGS="-mcmodel=large -pthread -O2"

# Choose XLC or GCC
%if %{with gcc_compiler}
export CC__="/opt/freeware/bin/gcc -fPIC"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"

export CXX__="/usr/vacpp/bin/xlC"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

export OPENSSL_LIBS="-lssl -lcrypto"
export OPENSSL_CFLAGS="-I/usr/include/openssl"
export GDLIB_LIBS="-lgd"
export GDLIB_CFLAGS="-I/opt/freeware/include"
export PNG_LIBS="-lpng"
export PNG_CFLAGS="-I/opt/freeware/include"
export KERBEROS_LIBS="-lkrb5"
export KERBEROS_CFLAGS="-I/opt/freeware/include"
export SASL_LIBS="-lsasl2"
export SASL_CFLAGS="-I/opt/freeware/include"
export GETTEXT_DIR=%{_prefix}


# shell function to configure and build a PHP tree
buildphp() {
set -x
ln -sf ../configure
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir64}/php \
	--with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
	--mandir=%{_mandir} \
	--enable-shared \
	--enable-cli \
	--disable-debug \
	--enable-bcmath \
	--with-zlib \
	--with-bz2=/opt/freeware \
	--with-curl=/opt/freeware \
	--with-freetype \
	--with-zlib-dir=/opt/freeware \
	--enable-sockets \
	--enable-mbstring \
	--with-zip \
	--enable-dom \
	--enable-soap=shared \
	--enable-ftp \
	--without-pear \
        --without-gdbm \
	--with-external-pcre \
	--with-openssl=/usr \
	--with-iconv=/opt/freeware \
        --with-zlib \
        --with-kerberos \
        --with-libxml \
	--enable-fpm \
	$*

# TODO: Needed or not?
# sed -e "s/^CFLAGS_CLEAN = /CFLAGS_CLEAN = -fPIC /" -i Makefile
# sed -e "s/-fvisibility=hidden//" -i Makefile

[ "$OBJECT_MODE" == 64 ] && {
    [ -e Makefile.sauve ] || cp Makefile Makefile.sauve;
    sed -e 's|-L/opt/freeware/lib|-L/opt/freeware/lib64 &|g' \
    -e 's|-R /opt/freeware/lib|-R /opt/freeware/lib64 &|g' \
    -e 's|/opt/freeware/lib/php/modules|/opt/freeware/lib64/php/modules|g' \
    <Makefile.sauve >Makefile
}

# TODO
# Fail first (phar), next OK because of .so copy.
# We cannot just said we prefer .la and not .so.

( $MAKE %{?_smp_mflags} || true )


# Due to changes in configure/libtool, the .so files are not copied to modules.
# As a result make test fails. Following is a workaround to solve this.
for i in `find . -name "*.so"`; do
  cp $i modules/`basename $i`
done

# This one may not fail
$MAKE

}

build_all()
{
set -x

# build the command line and the CGI version of PHP
mkdir -p build-cgi
cd build-cgi
buildphp \
	--enable-mysqlnd=shared \
	--with-mysqli=shared,mysqlnd \
	--with-unixODBC=shared \
	--enable-pdo=shared \
	--with-pdo-sqlite=shared,%{_prefix} \
	--with-pdo-mysql=shared,mysqlnd \
	--with-pdo-odbc=shared,unixODBC,%{_prefix} \
        \
        --enable-pcntl \
      --enable-opcache \
      --enable-phpdbg \
%if %{with imap}
      --with-imap=shared --with-imap-ssl \
%endif
      --enable-mbstring=shared \
      --enable-mbregex \
      --enable-gd=shared \
      --with-external-gd \
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --enable-ctype=shared \
%if %{with db}
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-tcadb=%{_prefix} \
%if %{with lmdb}
                          --with-lmdb=%{_prefix} \
%endif
%endif
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-ldap=shared,/opt/freeware --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
%if %{with firebird}
      --with-pdo-firebird=shared \
%endif
      --enable-dom=shared \
      --with-pgsql=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
%if %{with snmp}
      --with-snmp=shared,%{_prefix} \
%endif
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-pgsql=shared,%{_prefix} \
      --with-pdo-sqlite=shared \
%if %{with db}
      --with-pdo-dblib=shared,%{_prefix} \
%endif
      --with-sqlite3=shared \
      --without-readline \
      --without-libedit \
%if %{with pspell}
      --with-pspell=shared \
%endif
      --enable-phar=shared \
%if %{with tidy}
      --with-tidy=shared,%{_prefix} \
%endif
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-ffi=shared \
%if %{with sodium}
      --with-sodium=shared \
%else
      --without-sodium \
%endif
%if %{with intl}
      --enable-intl=shared \
%endif
%if %{with enchant}
      --with-enchant=shared \
%endif
        \
	$*

cd ..

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-phpdbg \
      --disable-json \
      --without-ffi \
      --disable-xmlreader --disable-xmlwriter \
      --without-sodium \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"


%if %{with mod_php}
# build the Apache module
mkdir -p  build-apache
cd build-apache

buildphp \
	--with-apxs2=%{_bindir}/apxs_$OBJECT_MODE \
        --without-mysqli \
        --disable-pdo \
        ${without_shared} \
	$*

cd ..
%endif


mkdir -p  build-fpm
cd build-fpm

buildphp \
      --enable-fpm \
      --without-fpm-acl \
      --without-mysqli \
      --disable-pdo \
      ${without_shared} \
      $*

cd ..

}


# build on 64bit mode

cd 64bit

# install extension modules in %{_libdir}/php/modules.
export EXTENSION_DIR=%{_libdir64}/php/modules

export OBJECT_MODE=64
export CC="${CC64}"
export CXX="${CXX64}"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -lpthread -lm -lXpm -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export PHP_LDFLAGS="$LDFLAGS"


build_all \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64}
 cd ..


# build on 32bit mode
cd 32bit
export EXTENSION_DIR=%{_libdir}/php/modules
 
export OBJECT_MODE=32
export CC="${CC32}"
export CXX="${CXX32}"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -lpthread -lm -lXpm -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export PHP_LDFLAGS="$LDFLAGS"

build_all \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}
cd .. 



%check
export MAKE="/opt/freeware/bin/gmake"
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export TESTDIR="64bit/build-cgi 32bit/build-cgi 
64bit/build-fpm 32bit/build-fpm 
%if %{with mod_php}
64bit/build-apache 32bit/build-apache
%endif
"

for testdir in $TESTDIR
do
    cd $testdir
    ulimit -n unlimited
    export http_proxy=""
    export https_proxy=""
    export TESTS="--offline"
    export NO_INTERACTION=1
    export SKIP_ONLINE_TESTS=1
    export SKIP_IO_CAPTURE_TESTS=1
    unset TZ LANG LC_ALL
#    ( TEST_PHP_ARGS="%{?_smp_mflags}"  $MAKE -k test || true )
    ( $MAKE -k test || true )
    /usr/sbin/slibclean
    cd ../..
done
unset NO_INTERACTION


%install
export AR="/usr/bin/ar"
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export PATH=/opt/freeware/bin/:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# ===================================
# First  Install the 64 bits versions
# ===================================
cd 64bit
export OBJECT_MODE=64
# unfortunately 'make install-sapi' does not seem to work for us, therefore
# we have to install the targets separately

cd build-fpm
$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}
cd ..

cd build-cgi
$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}
cd ..

%if %{with mod_php}
# install the DSO
cd build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
cp .libs/libphp.so ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp.so
cd ..
%endif

# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/pear
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session
mkdir -p ${RPM_BUILD_ROOT}/var/lib64/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib64/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib64/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib64/php/session

(
for dir in %{_bindir} %{_sbindir}
do
  cd  ${RPM_BUILD_ROOT}$dir
  for fic in $(ls -1| grep -v -e _32 -e _64)
  do
    mv $fic "$fic"_64
    ( /usr/bin/strip "$fic"_64 || true )
  done
done
)


# ===================================
# Second  Install the 32 bits versions
# ===================================
cd ../32bit
export OBJECT_MODE=32

# unfortunately 'make install-sapi' does not seem to work for us, therefore
# we have to install the targets separately
cd build-fpm
$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}
cd ..

cd build-cgi
$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}
cd ..

%if %{with mod_php}
# install the DSO
cd build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
cp .libs/libphp.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp.so
cd ..
%endif

(
for dir in %{_bindir} %{_sbindir}
do
  cd  ${RPM_BUILD_ROOT}$dir
  for fic in $(ls -1| grep -v -e _32 -e _64)
  do
    mv $fic "$fic"_32
    ( /usr/bin/strip "$fic"_32 || true )
    ln -sf "$fic"_64 $fic
  done
done
)


# ===================================
# End  Install the 32 bits versions
# ===================================

%if %{with mod_php}
$AR  -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp.a ${RPM_BUILD_ROOT}/%{_libdir}/httpd/modules/libphp.so
$AR  -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp.a ${RPM_BUILD_ROOT}/%{_libdir64}/httpd/modules/libphp.so

(
    cd ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/
    ln -s ../../../lib/httpd/modules/libphp.a libphp.a
)
%endif

# install the Apache httpd config file for PHP
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
(
  cd ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
  cp %{SOURCE1} httpd-php.conf_32
  cp %{SOURCE4} httpd-php.conf_64
  ln -sf httpd-php.conf_64 httpd-php.conf
  chmod 644 httpd-php.conf_32
  chmod 644 httpd-php.conf_64
)

# install the default configuration file and directories
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php.d
mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php-fpm.d
(
  cd ${RPM_BUILD_ROOT}%{_sysconfdir}
  cp %{SOURCE2} php32.ini
  cp %{SOURCE3} php64.ini
  ln -sf php64.ini php.ini

  cd ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
  cp %{SOURCE2} php32.ini
  cp %{SOURCE3} php64.ini
  ln -sf php64.ini php.ini

  cd ${RPM_BUILD_ROOT}%{_sysconfdir}
  cp %{SOURCE5} php-fpm.conf
  cp %{SOURCE6} ./php-fpm.d

  # Compatibility with older versions
  cd ${RPM_BUILD_ROOT}/etc
  ln -sf ..%{_sysconfdir}/php32.ini php32.ini
  ln -sf ..%{_sysconfdir}/php64.ini php64.ini
  ln -sf ..%{_sysconfdir}/php.ini php.ini
  ln -sf ..%{_sysconfdir}/php.d php.d
  ln -sf ..%{_sysconfdir}/php-fpm.d php-fpm.d
  ln -sf ..%{_sysconfdir}/php-fpm.conf php-fpm.conf
)


#Generate .ini files
for mod in gd pdo mysqli mysqlnd pdo_mysql pdo_sqlite
do
case $mod in
 pdo_*|mysqli)
 # Extensions with dependencies on 20-*
 ini=30-${mod}.ini;;
 *)
 # Extensions with no dependency
 ini=20-${mod}.ini;;
esac
cat > $RPM_BUILD_ROOT/%{_sysconfdir}/php.d/${ini} <<EOF
;Enable $mod extension module
extension=${mod}.so
EOF
done

# Generate files lists and stub .ini files for each subpackage
# The following includes .so files which are not installed to RPM_BUILD_ROOT
# The file libphp.so was copied, but not pdo.so, odbc.so and pdo_odbc.so
for mod in pgsql odbc ldap \
%if %{with snmp}
    snmp \
%endif
%if %{with imap}
    imap \
%endif
    json \
    mysqlnd mysqli \
    mbstring gd dom xsl soap bcmath dba \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    sqlite3 \
%if %{with enchant}
    enchant \
%endif
    phar fileinfo \
%if %{with intl}
    intl \
%endif
    ffi \
%if %{with tidy}
    tidy \
%endif
%if %{with pspell}
    pspell \
%endif
    curl \
%if %{with sodium}
    sodium \
%endif
    posix shmop sysvshm sysvsem sysvmsg xml \
    pdo pdo_mysql pdo pdo_pgsql pdo_odbc pdo_sqlite \
%if %{with firebird}
    pdo_firebird \
%endif
%if %{with db}
    pdo_dblib \
%endif
    xmlrpc xmlreader xmlwriter
do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      pdo_*|mysqli|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac

    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}
EOF
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%{_libdir64}/php/modules/${mod}.so
%config(noreplace) %{_sysconfdir}/php.d/${ini}
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xmlreader files.xmlwriter \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_pgsql >> files.pgsql
cat files.pdo_odbc >> files.odbc

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
cat files.sqlite3 >> files.pdo

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common

# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php/preload
chmod 755 ${RPM_BUILD_ROOT}%{_datadir}/php/preload

%if %{with mod_php}
%preun mod_php
if [ "$1" = 0 ]; then
    cat %{_sysconfdir}/httpd/conf/httpd.conf | \
      grep -v "# PHP settings" | \
      grep -v "Include conf/extra/httpd-php.conf" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
    cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
      grep -v "# PHP settings" | \
      grep -v "Include conf/extra/httpd-php.conf_64" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
    mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
    echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
fi
# remove some files to work with apache2
if [ -f %{_prefix}/sbin/httpd -a -d %{_sysconfdir}/httpd/conf ]
then
     [ -f  %{_sysconfdir}/httpd/conf/php.ini ] && rm -f %{_sysconfdir}/httpd/conf/php.ini
     grep -v "LoadModule php7_module" %{_sysconfdir}/httpd/conf/httpd.conf >%{_sysconfdir}/httpd/conf/httpd.conf.tmp
     [ -s %{_sysconfdir}/httpd/conf/httpd.conf.tmp ] && \
      mv -f  %{_sysconfdir}/httpd/conf/httpd.conf.tmp  %{_sysconfdir}/httpd/conf/httpd.conf
     grep -v "LoadModule php7_module" %{_sysconfdir}/httpd/conf/httpd.conf_64 >%{_sysconfdir}/httpd/conf/httpd.conf.tmp_64
     [ -s %{_sysconfdir}/httpd/conf/httpd.conf.tmp_64 ] && \
      mv -f  %{_sysconfdir}/httpd/conf/httpd.conf.tmp_64  %{_sysconfdir}/httpd/conf/httpd.conf_64
fi

%post mod_php
slibclean
echo ""
echo "This version of php has 32bit and 64bit support"
echo "64bit php uses %{_sysconfdir}/php64.ini"
echo ""
echo "This version of php is also built with fpm support."
echo "From httpd 2.4.39-2 onwards, http2 module is provided."
echo "Inorder to use php with http2, make use of php-fpm instead of mod_php."
echo ""
if [ -f %{_sysconfdir}/httpd/conf/httpd.conf ]
then
   cat %{_sysconfdir}/httpd/conf/httpd.conf | \
     grep -v "# PHP settings" | \
     grep -v "Include conf/extra/httpd-php.conf" \
     > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
   mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
fi
if [ -f %{_sysconfdir}/httpd/conf/httpd.conf_64 ]
then
   cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
     grep -v "# PHP settings" | \
     grep -v "Include conf/extra/httpd-php.conf_64" \
     > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
   mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64
fi
echo "extension=soap.so" >> %{_sysconfdir}/php.ini
echo "extension=soap.so" >> %{_sysconfdir}/php64.ini
echo "# PHP settings" >> %{_sysconfdir}/httpd/conf/httpd.conf
echo "# PHP settings" >> %{_sysconfdir}/httpd/conf/httpd.conf_64
echo "Include conf/extra/httpd-php.conf" >> %{_sysconfdir}/httpd/conf/httpd.conf
echo "Include conf/extra/httpd-php.conf_64" >> %{_sysconfdir}/httpd/conf/httpd.conf_64
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
%endif


%post fpm
/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf | \
/usr/bin/sed -e "s|#LoadModule proxy_module /opt/freeware/lib/httpd/modules/mod_proxy.so|LoadModule proxy_module /opt/freeware/lib/httpd/modules/mod_proxy.so|" \
 > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf

/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf | \
/usr/bin/sed -e "s|#LoadModule proxy_fcgi_module /opt/freeware/lib/httpd/modules/mod_proxy_fcgi.so|LoadModule proxy_fcgi_module /opt/freeware/lib/httpd/modules/mod_proxy_fcgi.so|" \
 > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf

/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#LoadModule proxy_module /opt/freeware/lib64/httpd/modules/mod_proxy.so|LoadModule proxy_module /opt/freeware/lib64/httpd/modules/mod_proxy.so|" \
 > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64

/usr/bin/cat %{_sysconfdir}/httpd/conf/httpd.conf_64 | \
/usr/bin/sed -e "s|#LoadModule proxy_fcgi_module /opt/freeware/lib64/httpd/modules/mod_proxy_fcgi.so|LoadModule proxy_fcgi_module /opt/freeware/lib64/httpd/modules/mod_proxy_fcgi.so|" \
 > %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64
/usr/bin/mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf_64 %{_sysconfdir}/httpd/conf/httpd.conf_64


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
exit 0

%if %{with mod_php}
%files mod_php
%defattr(-,root,system)
%{_libdir}/httpd/modules/libphp.so
%{_libdir64}/httpd/modules/libphp.so
%{_libdir}/httpd/modules/libphp.a
%{_libdir64}/httpd/modules/libphp.a
%{_libdir}/php/modules/soap.so
%{_libdir64}/php/modules/soap.so
%attr(0770,root,nobody) %dir /var/lib/php/session
%attr(0770,root,nobody) %dir /var/lib64/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf_32
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf_64
%endif

%files fpm
%defattr(-,root,system)
%config(noreplace) %{_sysconfdir}/php-fpm.conf*
%config(noreplace) %{_sysconfdir}/php-fpm.d/*
%config(noreplace) /etc/php-fpm.conf*
/etc/php-fpm.d
%{_sbindir}/php-fpm*

# %files pdo
# %defattr(-,root,system)
# %config(noreplace) %{_sysconfdir}/php.d/20-pdo.ini
# %config(noreplace) %{_sysconfdir}/php.d/30-pdo_sqlite.ini
# %{_libdir}/php/modules/pdo.so
# %{_libdir64}/php/modules/pdo.so
# %{_libdir}/php/modules/pdo_sqlite.so
# %{_libdir64}/php/modules/pdo_sqlite.so

# %files mysqlnd
# %defattr(-,root,system)
# %config(noreplace) %{_sysconfdir}/php.d/20-mysqlnd.ini
# %config(noreplace) %{_sysconfdir}/php.d/30-mysqli.ini
# %config(noreplace) %{_sysconfdir}/php.d/30-pdo_mysql.ini
# %{_libdir}/php/modules/mysqlnd.so
# %{_libdir64}/php/modules/mysqlnd.so
# %{_libdir}/php/modules/mysqli.so
# %{_libdir64}/php/modules/mysqli.so
# %{_libdir}/php/modules/pdo_mysql.so
# %{_libdir64}/php/modules/pdo_mysql.so

%files common
%defattr(-,root,system)
%doc 32bit/EXTENSIONS 32bit/NEWS 32bit/UPGRADING* 32bit/README.REDIST.BINS 32bit/*md 32bit/docs
#%doc 32bit/Zend/README.ZEND_*
%doc 32bit/LICENSE 32bit/TSRM_LICENSE
%doc 32bit/libmagic_LICENSE
%doc 32bit/timelib_LICENSE
/etc/php.d
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir64}/php
%dir %{_libdir}/php/modules
%dir %{_libdir64}/php/modules
%dir /var/lib/php
%dir /var/lib64/php
%dir %{_libdir}/php/pear
%dir %{_libdir64}/php/pear
%config(noreplace) %{_sysconfdir}/php.ini
%config(noreplace) %{_sysconfdir}/php32.ini
%config(noreplace) %{_sysconfdir}/php64.ini
%config(noreplace) /etc/php.ini
%config(noreplace) /etc/php32.ini
%config(noreplace) /etc/php64.ini

%files cli
%defattr(-,root,system)
%{_bindir}/php
%{_bindir}/php_32
%{_bindir}/php_64
%{_bindir}/php-cgi*
%{_bindir}/phar*
%{_bindir}/phpize*
%{_mandir}/man1/php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar*.1*
%{_mandir}/man1/phpize.1*

%files devel
%defattr(-,root,system)
%dir %{_libdir}/php
%dir %{_libdir64}/php
%{_bindir}/php-config*
%{_includedir}/php
%{_libdir}/build
%{_libdir64}/build
%{_mandir}/man1/php-config.1

%files dbg
%defattr(-,root,system,-)
%doc 32bit/sapi/phpdbg/CREDITS*
%{_bindir}/phpdbg*
%{_mandir}/man1/phpdbg.1*

%files pgsql -f 32bit/files.pgsql
%files odbc -f 32bit/files.odbc
%if %{with imap}
%files imap -f 32bit/files.imap
%endif
%files ldap -f 32bit/files.ldap
%if %{with snmp}
%files snmp -f 32bit/files.snmp
%endif
%files xml -f 32bit/files.xml
%files mbstring -f 32bit/files.mbstring
%defattr(-,root,system,-)
%doc 32bit/libmbfl_LICENSE
%files gd -f 32bit/files.gd
%files soap -f 32bit/files.soap
%files bcmath -f 32bit/files.bcmath
%defattr(-,root,system,-)
%doc 32bit/libbcmath_LICENSE
%files gmp -f 32bit/files.gmp
%if %{with db}
%files dba -f 32bit/files.dba
%endif
%files pdo -f 32bit/files.pdo
%if %{with tidy}
%files tidy -f 32bit/files.tidy
%endif
%if %{with db}
%files pdo-dblib -f 32bit/files.pdo_dblib
%endif
%if %{with pspell}
%files pspell -f 32bit/files.pspell
%endif
%if %{with intl}
%files intl -f 32bit/files.intl
%endif
%files process -f 32bit/files.process
%if %{with firebird}
%files pdo-firebird -f 32bit/files.pdo_firebird
%endif
%if %{with enchant}
%files enchant -f 32bit/files.enchant
%endif
%files mysqlnd -f 32bit/files.mysqlnd
%files opcache -f 32bit/files.opcache
%defattr(-,root,system,-)
# %config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
# TODO
# json seems disabled. Why?
# %%files json -f 32bit/files.json
%if %{with sodium}
%files sodium -f 32bit/files.sodium
%endif
%files ffi -f 32bit/files.ffi
%defattr(-,root,system,-)
%dir %{_datadir}/php/preload


%changelog
* Thu Nov 26 2020 Étienne Guesnet <etienne.guesnet@atos.net> 8.0.0-1beta
- New version 8.0.0
- Merge Toolbox, Fedora and Bullfreeware specfile.
- Add lot of subpackages and modules from Fedora
- Add link from /etc to %{_sysconfdir} to improve compatibility with Toolbox
- Add mysqlnd and pdo subpackages from Toolbox
- The deprecated module mod_php is not build by default
- 64 bit by default
- the -bexpfull flag has benn removed from patch

* Fri Nov 20 2020 Étienne Guesnet <etienne.guesnet@atos.net> 7.4.13-1
- New version 7.4.13

* Tue Mar 10 2020 Michael Wilson <michael.a.wilson@atos.net> 7.4.2-3
- Integration of FPM & GD IBM Toolbox modifications for 7.2.19-2 & 7.2.24-2

* Mon Mar 09 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 7.4.2-2
- Bullfreeware OpenSSL removal
- No more provide link to /usr

* Tue Jan 28 2020 Michael Wilson <michael.a.wilson@atos.net> 7.4.2-1
- Update to version 7.4.2
- Add  --with-onig  to include the bundled oniguruma (tested by configure)
- Configure for AIX LPP OpenSSL
- Move tests to %%check

* Tue Jan 21 2020 Michael Wilson <michael.a.wilson@atos.net> 7.3.13-1
- Update to version 7.3.13

* Tue Dec 10 2019 Michael Wilson <michael.a.wilson@atos.net> 7.3.10-1
- Update to version 7.3.10
- Using brpm on build environment laurel2
- Modification inspired by Fedora diff 7.3.10 vs 7.2.9
- Include explicit LDFLAGS "-lpthreads -lm"   unexplained 32 bit config error
- Include explicit LDFLAGS "-lXpm"   required for tests ?
- Copy .so files to modules directory for tests
- Partial integration of IBM Toolbox modifications for 7.2.19-2

* Mon Oct 21 2019 Michael Wilson <michael.a.wilson@atos.net> 7.2.9-2
- Adaptation to RPM version 4, brpm.OLD and build environment laurel2

* Tue Sep 04 2018 Tony Reix <tony.reix@atos.net> 7.2.9-1
- New version.

* Thu May 24 2018 Sena Apeke <sena.apeke.external@atos.net> 7.2.5-1
- New version. Update to 7.2.5
- Patch openssl-load-config, backported from 7.2, removed.

* Tue May 22 2018 Sena Apeke <sena.apeke.external@atos.net> 7.1.17-1
- New version. Update to 7.1.17
- Fix issue about delivery of php-cgi & php binaries (in .libs now).

* Wed May 16 2018 Sena Apeke <sena.apeke.external@atos.net> 7.1.16-2
- Add php-pdo %files

* Thu Apr 26 2018 Sena Apeke <sena.apeke.external@atos.net> 7.1.16-1
- New version. Update to 7.1.16
- Add ODBC

* Wed Feb 21 2018 Daniele Silvestre <daniele.silvestre@atos.net>
- New version. Update to 7.1.14

* Wed Oct  4 2017 Pascal Oliva <pascal.oliva@atos.net> 7.1.10-1
- New version. Update to 7.1.10

* Fri Sep 22 2017 Pascal Oliva <pascal.oliva@atos.net> 7.1.9-1
- New version. Update to 7.1.9
- Automatically load OpenSSL configuration file, from PHP 7.2

* Fri May 12 2017 Tony Reix <tony.reix@atos.net> 7.1.5-1
- New version.

* Thu May 11 2017 Tony Reix <tony.reix@atos.net> 7.1.4-1
- New version.

* Wed Mar 01 2017 Daniele Silvestre <daniele.silvestre@atos.net> 7.1.2-1
- updated to version 7.1.2 (From 7.1.1)
- remove 7.0.7-aix-strfmon.patch as included in 7.1.2 sources (see http://php.net/ChangeLog-7.php#7.1.2 bug 72979)
- remove 7.0.7-aix-network.patch as included in 7.1.2 sources (see http://php.net/ChangeLog-7.php#7.1.2 bug 72974)

* Tue Feb 07 2017 Tony Reix <tony.reix@atos.net> 7.1.1-2
- Rebuilt for removing libssl.so as a requirement.

* Fri Jan 20 2017 Tony Reix <tony.reix@atos.net> 7.1.1-1
- First port on AIX 6.1

* Fri Jan 06 2017 Girardet Jean <jean.girardet@atos.net> 7.1.0-2
- build 64 bits version

* Thu Dec 22 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.1.0-1
- updated to version 7.1.0 (From 7.0.13)

* Mon Nov 21 2016 Girardet Jean <jean.girardet@atos.net> 7.0.13-1
- updated to version 7.0.13 (From 7.0.12)

* Wed Nov 16 2016 Girardet Jean <jean.girardet@atos.net> 7.0.12-1
- updated to version 7.0.12 (From 7.0.10)

* Fri Jul 22 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.9-1
- updated to version 7.0.9

* Thu Jul 21 2016 Jean Girardet <jean.girardet@atos.net> 7.0.8-1
- updated to version 7.0.8

* Wed Jun 15 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.7-1
- updated to version 7.0.7

* Mon Mar 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.3-2
- updated dependencies to OpenSSL 1.0.2g and curl 7.47.1 (older versions of curl
  package does not work with OpenSSL 1.0.2g, and older versions of OpenSSL are
  unsecure)
- fixed mod_php package summary
- added mbstring

* Tue Mar 15 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.3-1
- updated to version 7.0.3
- added support for IBM Apache HTTP Server

* Fri Sep 19 2014 Michael Perzl <michael@perzl.org> - 5.5.17-1
- updated to version 5.5.17

