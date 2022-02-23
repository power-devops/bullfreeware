# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


# Default compiler gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%{!?optimize:%define optimize 2}


Summary: The PHP HTML-embedded scripting language
Name: php
Version: 7.4.2
Release: 2
# License: The PHP License v3.01
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

Source10: %{name}-%{version}-%{release}.build.log

# Fedora has following
# See https://secure.php.net/gpg-keys.php 
# Source20: https://www.php.net/distributions/php-keyring.gpg
Source21: https://www.php.net/distributions/%{name}-%{version}.tar.xz.asc

Patch0: %{name}-7.4.2-aix-build.patch
Patch1: %{name}-7.3.10-aix-setrlimit.patch
Patch2: %{name}-7.3.10-aix-tests.patch
Patch3: %{name}-7.4.2-aix-trailing-slash.patch
Patch4: %{name}-7.4.2-phpini.patch

# Fedora patch changes
# < Patch1: php-7.4.0-httpd.patch
# > Patch1: php-7.1.7-httpd.patch
#
# < Patch6: php-7.4.0-embed.patch
# > Patch6: php-5.6.3-embed.patch
# > Patch7: php-5.3.0-recode.patch
# > Patch40: php-7.2.4-dlopen.patch
#
# < Patch43: php-7.4.0-phpize.patch
# > Patch43: php-7.3.0-phpize.patch
#
# < Patch45: php-7.4.0-ldap_r.patch
# > Patch45: php-7.2.3-ldap_r.patch


%define _libdir64 %{_prefix}/lib64

%define contentdir /var/www

BuildRequires: make, sed
# BuildRequires: gnupg2               In Fedora
BuildRequires: bzip2 >= 1.0.6-2
BuildRequires: curl-devel >= 7.47.1
BuildRequires: gd-devel >= 2.0.35
BuildRequires: httpd-devel >= 2.4
BuildRequires: libiconv >= 1.16-2
BuildRequires: libtool-ltdl-devel >= 2.4.6-3
BuildRequires: libxml2-devel >= 2.9.4-2
# The default is now AIX LPP
# BuildRequires: openssl-devel >= 1.0.2s-1
BuildRequires: openldap-devel >= 2.4.44
BuildRequires: zlib-devel >= 1.2.11-2
BuildRequires: sqlite-devel
BuildRequires: oniguruma-devel
BuildRequires: bzip2-devel
BuildRequires: libzip-devel

%description
Dummy description to satisfy RPM.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


# The mod_php RPM corresponds to php RPM on Fedora
%package mod_php
Summary: The PHP HTML-embedded scripting language module for Apache V2.4.X
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.6-2
Requires: curl >= 7.47.1
Requires: httpd >= 2.4
Requires: libiconv >= 1.16-2
Requires: libtool-ltdl >= 2.4.6-3
Requires: libxml2 >= 2.9.4-2
Requires: openldap >= 2.4.44
Requires: sqlite
Requires: oniguruma
# The default is now AIX LPP
# Requires: openssl >= 1.0.2s-1
Requires: zlib >= 1.2.11-2
Requires: libzip
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
# sapi/cli/ps_title.c is PostgreSQL
License: PHP and Zend and BSD and MIT and ASL 1.0 and NCSA and PostgreSQL
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.6-2
Requires: curl >= 7.47.1
Requires: libiconv >= 1.16-2
Requires: libtool-ltdl >= 2.4.6-3
Requires: libxml2 >= 2.9.4-2
Requires: openldap >= 2.4.44
# The default is now AIX LPP
# Requires: openssl >= 1.0.2s-1
Requires: zlib >= 1.2.11-2
Provides: %{name}-cgi = %{version}-%{release}


%description cli
The php-cli package contains the command-line interface 
executing PHP scripts, %{_bindir}/php, and the CGI interface.


%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
License: PHP and BSD


%description common
The php-common package contains files used by both the php
package and the php-cli package.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: bzip2 >= 1.0.6-2
Requires: curl-devel >= 7.47.1
Requires: httpd-devel >= 2.4
Requires: libiconv >= 1.16-2
Requires: libtool-ltdl-devel >= 2.4.6-3
Requires: libxml2-devel >= 2.9.4-2
Requires: openldap-devel >= 2.4.44
# The default is now AIX LPP
# Requires: openssl-devel >= 1.0.2s-1
# Fedora has    pcre2-devel >= 10.30
Requires: pcre-devel >= 8.43-1
Requires: zlib-devel >= 1.2.11-2


%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.


%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: php-common = %{version}-%{release}
# ABI/API check - Arch specific
Provides: php-pdo-abi  = %{pdover}
Provides: php(pdo-abi) = %{pdover}
Provides: php-sqlite3, php-sqlite3
Provides: php-pdo_sqlite, php-pdo_sqlite

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.


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
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.


%prep

# %{gpgverify} --keyring='%{SOURCE20}' --signature='%{SOURCE21}' --data='%{SOURCE0}'

export PATH=/opt/freeware/bin:$PATH

echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "default_bits=%{default_bits}"
echo "optimize=%{optimize}"

%setup -q
%patch0 -p1 -b .build
%patch1 -p1 -b .setrlimit
%patch2 -p1 -b .tests
%patch3 -p1 -b .trailing-slash

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/bcmath/libbcmath/LICENSE libbcmath_LICENSE
cp ext/date/lib/LICENSE.rst timelib_LICENSE


# Fedora excluded tests   - TBC
## ----- Manage known as failed test -------
## affected by systzdata patch  - all pass on AIX
#rm ext/date/tests/timezone_location_get.phpt
#rm ext/date/tests/timezone_version_get.phpt
#rm ext/date/tests/timezone_version_get_basic1.phpt
## fails sometime  - skipped on AIX
#rm ext/sockets/tests/mcast_ipv?_recv.phpt
## cause stack exhausion
#rm Zend/tests/bug54268.phpt  - pass on AIX
#rm Zend/tests/bug68412.phpt  - pass on AIX
## tar issue
#rm ext/zlib/tests/004-mb.phpt  - pass on AIX


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


# patch for php64.ini
cd 64bit
%patch4 -p1 -b .php64_ini
#patch -p0 < %{PATCH4}
cd ..

%build

env
# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh

export AR="/usr/bin/ar "
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
export CFLAGS=-Wl,-bbigtoc
export GLOBAL_CC_OPTIONS=" -O%{optimize}"


# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC__="/opt/freeware/bin/gcc"
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


# install extension modules in %{_libdir}/php/modules.

# Unrecognized configure options from previous spec files
# --with-gd      -> --enable-gd & GDLIB_CFLAGS/GDLIB_LIBS to override pkg-config
# --with-freetype-dir -> --with-freetype & FREETYPE2_* to override pkg-config
# --with-jpeg-dir  -> --with-jpeg & JPEG_CFLAGS/JPEG_LIBS to override pkg-config
# But package libjpeg is missing libjpeg.pc  - so keep --with-jpeg-dir  TBC
# --with-png-dir   -> PNG_CFLAGS/PNG_LIBS to override pkg-config
# --with-xpm-dir   -> --with-xpm,
# But package xpm is missing xpm.pc  - so keep --with-xpm-dir  TBC
# --enable-zip     -> --with-zip,
# --with-onig      -> ONIG_CFLAGS/ONIG_LIBS to override pkg-config


# C compiler & linker flags for OPENSSL, overriding pkg-config
# Option --with-openssl=/opt/freeware changed to / for AIX LPP
# But configure insists on using pkg-config to find openssl RPM
#export OPENSSL_LIBS=/usr/lib/libssl.a
#export OPENSSL_CFLAGS=/usr/include/openssl
export OPENSSL_LIBS="-lssl -lcrypto"
export OPENSSL_CFLAGS="-I/usr/include/openssl"

# shell function to configure and build a PHP tree
buildphp() {
    set -x
    ln -sf ../configure

sh -x ./configure \
 --prefix=/opt/freeware \
 --with-config-file-path=/opt/freeware/etc \
 --with-config-file-scan-dir=/opt/freeware/etc/php.d \
 --disable-debug \
 --enable-shared \
 --enable-static \
 --enable-bcmath \
 --without-pear \
 --with-openssl \
 --with-zlib \
 --with-bz2 \
 --with-curl=/opt/freeware \
 --enable-gd \
 --with-freetype \
 --with-jpeg-dir=/opt/freeware \
 --with-xpm-dir=no \
 --with-zlib-dir=/opt/freeware \
 --with-ldap=/opt/freeware \
 --enable-soap \
 --enable-ftp \
 --enable-sockets \
 --enable-mbstring \
 --with-zip \
 --with-iconv=/opt/freeware \
 --with-iconv-dir=/opt/freeware \
 --with-mysqli=mysqlnd \
 --enable-dom \
 --enable-json \
 $*

sed -e "s/^CFLAGS_CLEAN = /CFLAGS_CLEAN = -fPIC /" -i Makefile
sed -e "s/-fvisibility=hidden//" -i Makefile

[ "$OBJECT_MODE" == 64 ] && {
    [ -e Makefile.sauve ] || cp Makefile Makefile.sauve;
    sed -e 's|-L/opt/freeware/lib|-L/opt/freeware/lib64 &|g' \
    -e 's|-R /opt/freeware/lib|-R /opt/freeware/lib64 &|g' \
    -e 's|/opt/freeware/lib/php/modules|/opt/freeware/lib64/php/modules|g' \
    <Makefile.sauve >Makefile
}


$MAKE --trace %{?_smp_mflags} -j16
# $MAKE --trace %{?_smp_mflags} -j1


# Due to changes in configure/libtool, the .so files are not copied to modules.
# This causes the majority of tests to fail when attempting to load them
# Also, there are hangs during execution of test (cgi and apache) :
#   TLS server rate-limits client-initiated renegotiation
#                     [ext/openssl/tests/stream_server_reneg_limit.phpt]
# and a long delay in the test :
#   Bug #76705: feof might hang on TLS streams in case of fragmented TLS records
#                     [ext/openssl/tests/bug77390.phpt]

# For 32/64 bit build-cgi and build-apache
cp ext/odbc/.libs/odbc.so modules/
# For build-cgi
if [ -e ext/pdo/.libs/pdo.so ]; then
 cp ext/pdo/.libs/pdo.so modules/
 cp ext/pdo_odbc/.libs/pdo_odbc.so modules/
 cp ext/pdo_sqlite/.libs/pdo_sqlite.so modules/
fi
# For 32 bit build-apache
if [ -e ext/opcache/.libs/opcache.so ]; then
 cp ext/opcache/.libs/opcache.so modules/
fi


# Moved to %%check
# if [ "%{dotests}" == 1 ]
# then
#     ulimit -n unlimited
#     export http_proxy=""
#     export https_proxy=""
#     export TESTS="--offline"
#     ( ( /usr/bin/yes n | $MAKE -k test ) || true )
#     /usr/sbin/slibclean
# else
#     echo "NO TESTS DONE !"
# fi

}

build_all()
{
set -x

# build the command line and the CGI version of PHP
mkdir -p build-cgi
cd build-cgi
buildphp \
    --enable-pdo=shared \
    --with-pdo-odbc=shared,unixODBC,%{_prefix} \
    --with-pdo-sqlite=shared,%{_prefix} \
    --with-unixODBC=shared,%{_prefix} \
    $*

cd ..


# build the Apache module
mkdir -p  build-apache
cd build-apache
APXS=/opt/freeware/bin/apxs
# If IBM Apache LPP is installed, use it to build the Apache module
if [ -f /usr/IBMAHS/bin/apxs ]; then
    APXS=/usr/IBMAHS/bin/apxs
fi
buildphp \
    --with-unixODBC=shared,%{_prefix} \
    --with-apxs2=${APXS} \
    $*

cd ..

}


# build on 64bit mode

cd 64bit
export EXTENSION_DIR=%{_libdir64}/php/modules

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -lpthread -lm -lXpm"


#     --enable-opcache=no \

build_all \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    --enable-opcache=no 
 cd ..


# build on 32bit mode
cd 32bit
export EXTENSION_DIR=%{_libdir}/php/modules
 
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -lpthread -lm -lXpm -Wl,-bmaxdata:0x80000000"

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

for testdir in 64bit/build-cgi 64bit/build-apache 32bit/build-cgi 32bit/build-apache
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
    # ( ( /usr/bin/yes n | $MAKE -k test ) || true )
    ( $MAKE -k test || true )
    /usr/sbin/slibclean
    cd ../..
done
unset NO_INTERACTION


# Fedora under %%check has following
#cd build-apache
#
## Run tests, using the CLI SAPI
#export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
#export SKIP_ONLINE_TESTS=1
#export SKIP_IO_CAPTURE_TESTS=1
#unset TZ LANG LC_ALL
#if ! make test; then
#  set +x
#  for f in $(find .. -name \*.diff -type f -print); do
#    if ! grep -q XFAIL "${f/.diff/.phpt}"
#    then
#      echo "TEST FAILURE: $f --"
#      cat "$f"
#      echo -e "\n-- $f result ends."
#    fi
#  done
#  set -x
#  #exit 1
#fi
#unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_



%install
# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh
export AR="/usr/bin/ar "
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
export CFLAGS=-Wl,-bbigtoc
export GLOBAL_CC_OPTIONS=" -O%{optimize}"

export PATH=/opt/freeware/bin/:$PATH

[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


# ===================================
# First  Install the 64 bits versions
# ===================================
cd 64bit

export OBJECT_MODE=64



# unfortunately 'make install-sapi' does not seem to work for us, therefore
# we have to install the targets separately - changes due to RPM v4  ?
cd build-cgi

$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}

#for TARGET in install-cli install-build install-headers install-programs ; do
#    $MAKE INSTALL_ROOT=${RPM_BUILD_ROOT} ${TARGET} 
#done

#$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT} ext/pdo
#$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT} ext/odbc

# install the php-cgi binary - Not built in .libs due to RPM v4  ?
#cp sapi/cgi/.libs/php-cgi ${RPM_BUILD_ROOT}%{_bindir}
#chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi

# install the php binary - Not built in .libs due to RPM v4  ?
#cp sapi/cli/.libs/php ${RPM_BUILD_ROOT}%{_bindir}
#chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php

# install the DSO
cd ../build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
cp .libs/libphp7.so ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp7.so
cd ..


# install the pdo .so file
(
  cd build-cgi/ext/pdo
  mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/modules
  cp .libs/pdo.so ${RPM_BUILD_ROOT}%{_libdir64}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/modules/pdo.so
)

# install the pdo_odbc .so file
(
  cd build-cgi/ext/pdo_odbc
  cp .libs/pdo_odbc.so ${RPM_BUILD_ROOT}%{_libdir64}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/modules/pdo_odbc.so
)

# install the odbc .so file
(
  cd build-apache/ext/odbc
  cp .libs/odbc.so ${RPM_BUILD_ROOT}%{_libdir64}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/modules/odbc.so
)



# move and strip binaries
for fic in php php-cgi
do
    /usr/bin/strip -X64 ${RPM_BUILD_ROOT}%{_bindir}/$fic > /dev/null 2>&1 || true
    mv ${RPM_BUILD_ROOT}%{_bindir}/$fic ${RPM_BUILD_ROOT}%{_bindir}/"$fic"_64
done

# /usr/bin/strip -X64 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp7.so


# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib64/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib64/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib64/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib64/php/session



# ===================================
# Second  Install the 32 bits versions
# ===================================
cd ../32bit

export OBJECT_MODE=32

# unfortunately 'make install-sapi' does not seem to work for us, therefore
# we have to install the targets separately - changes due to RPM v4  ?
cd build-cgi
$MAKE install INSTALL_ROOT=${RPM_BUILD_ROOT}

#for TARGET in install-cli install-build install-headers install-programs ; do
#    $MAKE INSTALL_ROOT=${RPM_BUILD_ROOT} ${TARGET}
#done

# install the php-cgi binary. That fixes an issue
# in make install - Not built in .libs due to RPM v4  ?
#cp sapi/cgi/.libs/php-cgi ${RPM_BUILD_ROOT}%{_bindir}
#chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi

# install the php binary. That fixes an issue
# in make install - Not built in .libs due to RPM v4  ?
#cp sapi/cli/.libs/php ${RPM_BUILD_ROOT}%{_bindir}
#chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php

# install the DSO
cd ../build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
cp .libs/libphp7.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.so
cd ..

# install the pdo .so file
(
  cd build-cgi/ext/pdo
  mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/modules
  cp .libs/pdo.so ${RPM_BUILD_ROOT}%{_libdir}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/modules/pdo.so
)

# install the odbc .so file
(
  cd build-cgi/ext/pdo_odbc
  cp .libs/pdo_odbc.so ${RPM_BUILD_ROOT}%{_libdir}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/modules/pdo_odbc.so
)

# install the odbc .so file
(
  cd build-apache/ext/odbc
  cp .libs/odbc.so ${RPM_BUILD_ROOT}%{_libdir}/php/modules
  chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/modules/odbc.so
)


# move and strip binaries
for fic in php php-cgi
do
    /usr/bin/strip  -X32 ${RPM_BUILD_ROOT}%{_bindir}/$fic > /dev/null 2>&1 || true
    mv ${RPM_BUILD_ROOT}%{_bindir}/$fic ${RPM_BUILD_ROOT}%{_bindir}/"$fic"_32
    (
	cd ${RPM_BUILD_ROOT}%{_bindir}
	ln -s "$fic"_64 $fic
    )

done


# ===================================
# End  Install the 32 bits versions
# ===================================


$AR  -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.a ${RPM_BUILD_ROOT}/%{_libdir}/httpd/modules/libphp7.so
$AR  -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.a ${RPM_BUILD_ROOT}/%{_libdir64}/httpd/modules/libphp7.so

(
    cd ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/
    ln -s ../../../lib/httpd/modules/libphp7.a libphp7.a
    
)

/usr/bin/strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.so
/usr/bin/strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp7.so


# install the Apache httpd config file for PHP
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf_64
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf_64

# install the default configuration file and directories
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/php.ini
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/php64.ini
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf/php.ini
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf/php64.ini
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php.d

# create the PHP extension modules directory
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/modules
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/modules

# There are no longer default icons to install

# install PHP-FPM files
# Log
# install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
# install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm

# Config
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php-fpm.d
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_sysconfdir}/php-fpm.d

# LogRotate
# install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
# install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Nginx configuration
# install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
# install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf




# Generate files lists and stub .ini files for each subpackage
# The following includes .so files which are not installed to RPM_BUILD_ROOT
# The file libphp7.so was copied , but not pdo.so, odbc.so and pdo_odbc.so
# Perhaps this was done on hardy1/RPM v3.0.5, but not on laurel2/RPM v4

for mod in  odbc ldap \
    mbstring soap bcmath  \
    bz2  exif ftp  iconv \
    sockets tokenizer opcache \
    pdo pdo_pgsql pdo_odbc 
do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]
    then
       cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
    fi
    cat > files.${mod} <<EOF
%{_libdir}/php/modules/${mod}.so
%{_libdir64}/php/modules/${mod}.so
#%config(noreplace) %{_sysconfdir}/php.d/${ini}
EOF
done


# Split out the PDO modules
cat files.pdo_odbc >> files.odbc

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
#cat files.pdo_sqlite >> files.pdo



# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session

# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin include
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )


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
        [ -f  $1/modules/libphp7.a ] && rm -f $1/modules/libphp7.a
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
        [ -d $1/modules ] && cp -p %{_libdir}/httpd/modules/libphp7.a $1/modules
#        [ -d $1/modules ] && cp -p %{_libdir64}/httpd/modules/libphp7.so $1/modules   No it's links, we copied same file in fact
#        [ -d $1/modules ] && cp -p %{_libdir64}/httpd/modules/libphp7.a $1/modules
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
exit 0


%files mod_php
%defattr(-,root,system)
%{_libdir}/httpd/modules/libphp7.so
%{_libdir64}/httpd/modules/libphp7.so
%{_libdir}/httpd/modules/libphp7.a
%{_libdir64}/httpd/modules/libphp7.a
%attr(0770,root,nobody) %dir /var/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf


%files common
%defattr(-,root,system)
%doc 32bit/EXTENSIONS 32bit/NEWS 32bit/UPGRADING* 32bit/README.REDIST.BINS 32bit/*md 32bit/docs
#%doc 32bit/Zend/README.ZEND_*
%license 32bit/LICENSE 32bit/TSRM_LICENSE
%license 32bit/libmagic_LICENSE
%license 32bit/timelib_LICENSE
%config(noreplace) %{_sysconfdir}/php.ini
%config(noreplace) %{_sysconfdir}/php64.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir %{_libdir64}/php
%dir %{_libdir64}/php/modules
%dir /var/lib/php
%dir %{_libdir}/php/pear
%dir %{_libdir64}/php/pear


%files cli
%defattr(-,root,system)
%{_bindir}/php
%{_bindir}/php-cgi
#%{_mandir}/man1/php.1
# /usr/bin/php
# /usr/bin/php-cgi

%{_bindir}/php_*
%{_bindir}/php-cgi_*
#%{_mandir}/man1/php.1
# /usr/bin/php_*
# /usr/bin/php-cgi_*


%files devel
%defattr(-,root,system)
%dir %{_libdir}/php
%{_bindir}/php-config
%{_bindir}/phpize
%{_bindir}/phpdbg
%{_includedir}/php
%{_libdir}/build
#%{_mandir}/man1/php-config.1
#%{_mandir}/man1/phpize.1
# /usr/bin/php-config
# /usr/bin/phpize
# /usr/include/*


%files odbc -f 32bit/files.odbc

%files pdo -f  32bit/files.pdo

%changelog
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

