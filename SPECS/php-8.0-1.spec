# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


# Default compiler gcc
# To use xlc : --define 'gcc_compiler=0'
# %%{!?gcc_compiler:%define gcc_compiler 1}
%bcond_without gcc_compiler


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
%bcond_with   db
# Used with db only
%bcond_with   lmdb
# No snmp available
%bcond_with   snmp
# No enchant available
%bcond_with   enchant
# intl (gettext) needs icu in php
%bcond_with   intl
# php-gd has a lot of test in error. Unactivateid by default.
%bcond_with   gd
# TODO php-json does not produce .so
%bcond_with json


Summary: PHP scripting language for creating dynamic web sites
Name: php
Version: 8.0
Release: 1
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
# ext/date/lib is MIT
# Zend/zend_sort is NCSA
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA
Group: Development/Languages
URL: http://www.php.net

Source100: %{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64
%define contentdir /var/www

%if %{with zts}
Provides: php-zts = %{version}-%{release}
%endif

Requires: php%{version}
Requires: php-common     = %{version}-%{release}
# For backwards-compatibility, pull the "php" command
Requires: php-cli      = %{version}-%{release}
# httpd have threaded MPM by default
Recommends: php-fpm      = %{version}-%{release}
# as "php" is now mostly a meta-package, commonly used extensions
# reduce diff with "dnf module install php"
%if %{with json}
Recommends: php-json     = %{version}-%{release}
%endif
Recommends: php-mbstring = %{version}-%{release}
Recommends: php-opcache  = %{version}-%{release}
Recommends: php-pdo      = %{version}-%{release}
%if %{with sodium}
Recommends: php-sodium   = %{version}-%{release}
%endif
Recommends: php-xml      = %{version}-%{release}


%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

This package is a meta-package.


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
# sapi/cli/ps_title.c is PostgreSQL
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: %{name}-common = %{version}-%{release}
Requires: php%{version}-cli

%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, %{_bindir}/php, and the CGI interface.


%package dbg
Summary: The interactive PHP debugger
Requires: php-common = %{version}-%{release}
Requires: php%{version}-dbg

%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
Requires: php-common = %{version}-%{release}
Requires: php%{version}-fpm

%description fpm
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
Requires: php%{version}-common

%description common
The php-common package contains files used by both the php
package and the php-cli package.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: php%{version}-devel

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.

%package opcache
Summary:   The Zend OPcache
License:   PHP
Requires:  php-common = %{version}-%{release}
Requires: php%{version}-opcache

%description opcache
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
Requires: php%{version}-imap

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.
%endif


%package ldap
Summary: A module for PHP applications that use LDAP
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-ldap

%description ldap
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
Requires: php%{version}-pdo

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.


%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
Requires: php%{version}-mysqlnd

%description mysqlnd
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
Requires: php%{version}-pgsql

%description pgsql
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
Requires: php%{version}-process

%description process
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
Requires: php%{version}-odbc

%description odbc
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
Requires: php%{version}-soap

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.


%if %{with firebird}
%package pdo-firebird
Summary: PDO driver for Interbase/Firebird databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
Requires: php%{version}-firebird

%description pdo-firebird
The php-pdo-firebird package contains the PDO driver for
Interbase/Firebird databases.
%endif


%if %{with snmp}
%package snmp
Summary: A module for PHP applications that query SNMP-managed devices
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}, net-snmp
Requires: php%{version}-snmp

%description snmp
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
Requires: php%{version}-xml

%description xml
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
Requires: php%{version}-mbstring

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.


%if %{with gd}
%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libgd is licensed under BSD
License: PHP and BSD
Requires: %{name}-common = %{version}-%{release}
Requires: php%{version}-gd

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.
%endif


%package bcmath
Summary: A module for PHP applications for using the bcmath library
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: php-common = %{version}-%{release}
Requires: php%{version}-bcmath

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.


%package gmp
Summary: A module for PHP applications for using the GNU MP library
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: php-common = %{version}-%{release}
Requires: php%{version}-gmp

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.


%if %{with db}
%package dba
Summary: A database abstraction layer module for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-dba

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.
%endif


%if %{with tidy}
%package tidy
Summary: Standard PHP module provides tidy library support
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-tidy

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.
%endif


%if %{with db}
%package pdo-dblib
Summary: PDO driver for Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: php-pdo = %{version}-%{release}
Requires: php%{version}-pdo-dblib

%description pdo-dblib
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
Requires: php%{version}-pspell

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.
%endif


%if %{with intl}
%package intl
Summary: Internationalization extension for PHP applications
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-intl

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.
%endif


%if %{with enchant}
%package enchant
Summary: Enchant spelling extension for PHP applications
# All files licensed under PHP version 3.0
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-enchant

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.
%endif

%if %{with json}
%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-json

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.
%endif


%if %{with sodium}
%package sodium
Summary: Wrapper for the Sodium cryptographic library
# All files licensed under PHP version 3.0.1
License: PHP
Requires: php-common = %{version}-%{release}
Requires: php%{version}-sodium

%description sodium
The php-sodium package provides a simple,
low-level PHP extension for the libsodium cryptographic library.
%endif


%package ffi
Summary: Foreign Function Interface
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: php-common = %{version}-%{release}
Requires: php%{version}-ffi

%description ffi
FFI is one of the features that made Python and LuaJIT very useful for fast
prototyping. It allows calling C functions and using C data types from pure
scripting language and therefore develop “system code” more productively.

For PHP, FFI opens a way to write PHP extensions and bindings to C libraries
in pure PHP.


%prep
export PATH=/opt/freeware/bin:$PATH

%build

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Link to versionned files
(
  mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for bin in php php-cgi phar phpize phpdbg php-config; do
    ln -sf ${bin}%{version} ${bin}
    ln -sf ${bin}%{version}_64 ${bin}_64
    ln -sf ${bin}%{version}_32 ${bin}_32
  done

  mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
  cd ${RPM_BUILD_ROOT}%{_sbindir}
  for sbin in php-fpm; do
    ln -sf ${sbin}%{version} ${sbin}
    ln -sf ${sbin}%{version}_64 ${sbin}_64
    ln -sf ${sbin}%{version}_32 ${sbin}_32
  done


  mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
  cd ${RPM_BUILD_ROOT}%{_mandir}/man1
  for man in php php-cgi phar phpize phar.phar phpdbg php-config; do
    ln -sf ${man}%{version}.1 ${man}.1
  done

  mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
  cd ${RPM_BUILD_ROOT}%{_includedir}
  ln -sf php${version} php
)

# Folders
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib64/php

# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/php/preload
chmod 755 ${RPM_BUILD_ROOT}%{_datadir}/php/preload


%post common
echo "Each version of PHP has its own configuration file."
echo "If you have modified them, report your modification"
echo "from /opt/freeware/etc/php<version>.d for the new version."

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

%files
# Empty

%files fpm
%defattr(-,root,system)
%{_sbindir}/php-fpm*

%files common
%defattr(-,root,system)
%dir /var/lib/php
%dir /var/lib64/php

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
%{_bindir}/php-config*
%{_mandir}/man1/php-config.1
%{_includedir}/php

%files dbg
%defattr(-,root,system,-)
%{_bindir}/phpdbg*
%{_mandir}/man1/phpdbg.1*

%files pgsql
%files odbc
%if %{with imap}
%files imap
%endif
%files ldap
%if %{with snmp}
%files snmp
%endif
%files xml
%files mbstring
%if %{with gd}
%files gd
%endif
%files soap
%files bcmath
%files gmp
%if %{with db}
%files dba
%endif
%files pdo
%if %{with tidy}
%files tidy
%endif
%if %{with db}
%files pdo-dblib
%endif
%if %{with pspell}
%files pspell
%endif
%if %{with intl}
%files intl
%endif
%files process
%if %{with firebird}
%files pdo-firebird
%endif
%if %{with enchant}
%files enchant
%endif
%files mysqlnd
%files opcache
%defattr(-,root,system,-)
# %config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%if %{with zts}
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%endif
%if %{with json}
%files json
%endif
%if %{with sodium}
%files sodium
%endif
%files ffi
%defattr(-,root,system,-)
%dir %{_datadir}/php/preload


%changelog
* Tue Sep 28  2021 Etienne Guesnet <etienne.guesnet@atos.net> 8.0-1
- Parallel installation
- This is a metapackage

* Thu Nov 26 2020 Étienne Guesnet <etienne.guesnet@atos.net> 8.0.0-1beta
- New version 8.0.0
- Merge Toolbox, Fedora and Bullfreeware specfile.
- Add lot of subpackages and modules from Fedora
- Add link from /etc to %{_sysconfdir} to improve compatibility with Toolbox
- Add mysqlnd and pdo subpackages from Toolbox
- 64 bit by default
- the -bexpfull flag has been removed from patch

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

