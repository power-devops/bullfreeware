# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 0}


# Default compiler gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%{!?optimize:%define optimize 2}

%define contentdir /var/www

Summary: The PHP HTML-embedded scripting language
Name: php
Version: 5.6.33
Release: 1
License: The PHP License v3.01
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{name}-%{version}.tar.bz2
Source1: %{name}.conf
Source2: %{name}.ini
Source3: %{name}-%{version}-%{release}.build.log

Patch0: %{name}-5.6.31-aix-build.patch
#Patch1: %{name}-%{version}-aix-strfmon.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define _libdir64 %{_prefix}/lib64

BuildRequires: make

BuildRequires: bzip2 >= 1.0.2-4
BuildRequires: curl-devel >= 7.19.7
BuildRequires: gd-devel >= 2.0.35
BuildRequires: httpd-devel >= 2.2.15-1
BuildRequires: libiconv >= 1.14-2
BuildRequires: libtool-ltdl-devel >= 1.5.26-1
BuildRequires: libxml2-devel >= 2.7.8-3
BuildRequires: openssl-devel >= 1.0.1i-1
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: pcre-devel >= 7.9-2
BuildRequires: zlib-devel >= 1.2.3-3

%description
Dummy description to satisfy RPM.


%package -n mod_php_ap22
Summary: The PHP HTML-embedded scripting language module for Apache V2.2.X
#Summary: The PHP HTML-embedded scripting language module for Apache V2.4.X
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.2-4
Requires: curl >= 7.19.7-1
#Requires: gd >= 2.0.35
#Requires: httpd >= 2.4
Requires: httpd >= 2.2.15-1
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl >= 1.5.26-1
Requires: libxml2 >= 2.7.8-3
Requires: openldap >= 2.4.23
Requires: openssl >= 1.0.1i-1
#Requires: pcre >= 7.9-2
Requires: zlib >= 1.2.3-3

Provides: mod_php = %{version}-%{release}
Provides: php = %{version}-%{release}

%description -n mod_php_ap22
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The mod_php_ap22 package contains the module which adds support for the PHP
language to Apache HTTP Server V2.2.X.


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP

Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.2-4
Requires: curl >= 7.19.7-1
#Requires: curl >= 7.47.1-1
#Requires: gd >= 2.0.35
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl >= 1.5.26-1
Requires: libxml2 >= 2.7.8-3
Requires: openldap >= 2.4.23
Requires: openssl >= 1.0.1i-1
#Requires: pcre >= 7.9-2
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
Requires: curl-devel >= 7.19.7
#Requires: curl-devel >= 7.47.1-1
#Requires: gd-devel >= 2.0.35
Requires: libiconv >= 1.14-2
Requires: libtool-ltdl-devel >= 1.5.26-1
Requires: libxml2-devel >= 2.7.8-3
Requires: openldap-devel >= 2.4.23
Requires: openssl-devel >= 1.0.2g-1
#Requires: openssl-devel >= 1.0.1i-1
Requires: pcre-devel >= 7.9-2
Requires: zlib-devel >= 1.2.3-3

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.


%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "default_bits=%{default_bits}"
echo "optimize=%{optimize}"

%setup -q
%patch0
###SID %patch1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

env
# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export GREP="/opt/freeware/bin/grep"
export EGREP="/opt/freeware/bin/egrep"
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
export EXTENSION_DIR=%{_libdir}/php/modules

# shell function to configure and build a PHP tree
buildphp() {
  set -x
  ln -sf ../configure
# --cache-file=../config.cache \
#    --with-pcre-regex=%{_prefix} \
#    --enable-pdo \
#?? NEW --enable-soap \
#?? NEW --enable-mbstring \


./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --enable-shared \
    --enable-static \
    --enable-bcmath \
    --without-pear \
    --with-openssl=%{_prefix} \
    --with-zlib \
    --with-bz2 \
    --with-curl=%{_prefix} \
    --with-gd \
    --with-freetype-dir=%{_prefix} \
    --with-jpeg-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=no \
    --with-zlib-dir=%{_prefix} \
    --with-ldap=%{_prefix} \
    --enable-ftp \
    --enable-sockets \
    --enable-zip \
    --with-iconv=%{_prefix} \
    --with-iconv-dir=%{_prefix} \
    --with-mysqli=mysqlnd \
    --enable-dom \
    --enable-json \
    $*
# required since PHP V5.4.0, check out https://bugs.php.net/bug.php?id=61751
cat Makefile | \
    sed 's|PHP_CLI_OBJS =|PHP_CLI_OBJS = $(PHP_BINARY_OBJS) |g' | \
    sed 's|PHP_CGI_OBJS =|PHP_CGI_OBJS = main/internal_functions.lo |g' \
    > Makefile.tmp
mv -f Makefile.tmp Makefile
sed -e "s/-fvisibility=hidden//" -i Makefile

[ "$OBJECT_MODE" == 64 ] && {
    [ -e Makefile.sauve ] || cp Makefile Makefile.sauve;
    sed -e 's|-L/opt/freeware/lib|-L/opt/freeware/lib64 &|g' \
    -e 's|-R /opt/freeware/lib|-R /opt/freeware/lib64 &|g' \
    -e 's|/opt/freeware/lib/php/modules|/opt/freeware/lib64/php/modules|g' \
    <Makefile.sauve >Makefile
}

$MAKE %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    export http_proxy=""
    export https_proxy=""
    export TESTS="--offline"
    #export NO_INTERACTION=1 REPORT_EXIT_STATUS=1
    #export MALLOC_CHECK_=2
    #export SKIP_ONLINE_TESTS=1
    #unset TZ LANG LC_ALL

    ( ( /usr/bin/yes n | $MAKE -k test ) || true )
    /usr/sbin/slibclean
fi
}


build_all()
{
set -x

# build the command line and the CGI version of PHP

mkdir -p build-cgi
cd build-cgi
buildphp \
    $*

cd ..


# build the Apache module thread-safe
mkdir -p build-apache
cd build-apache
# for Apache 2.2.X: --with-apxs2=%{_sbindir}/apxs
# for Apache 2.4.X: --with-apxs2=%{_bindir}/apxs
#buildphp \
#
#    --with-apxs2=%{_bindir}/apxs
APXS=/opt/freeware/bin/apxs
# If IBM Apache LPP is installed, use it to build the Apache module
if [ -f /usr/IBMAHS/bin/apxs ]; then
    APXS=/usr/IBMAHS/bin/apxs
fi
buildphp \
    --with-apxs2=${APXS} \
    $*

cd ..

}


# build on 64bit mode

cd 64bit
# install extension modules in %{_libdir64}/php/modules
export EXTENSION_DIR=%{_libdir64}/php/modules

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

#     --enable-opcache=no \

build_all \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    --enable-opcache=no
cd ..


# build on 32bit mode
cd 32bit
# install extension modules in %{_libdir}/php/modules.
export EXTENSION_DIR=%{_libdir}/php/modules

export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

#    --enable-opcache=no
build_all \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}
cd ..


%install
# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace --print-directory "
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
export CFLAGS=-Wl,-bbigtoc
export GLOBAL_CC_OPTIONS=" -O%{optimize}"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# ===================================
# First  Install the 64 bits versions
# ===================================
cd 64bit

export OBJECT_MODE=64

# unfortunately 'make install-sapi' does not seem to work for use, therefore
# we have to install the targets separately
cd build-cgi
for TARGET in install-cli install-build install-headers install-programs ; do
    $MAKE INSTALL_ROOT=${RPM_BUILD_ROOT} ${TARGET}
done

# install the php-cgi binary
cp sapi/cgi/php-cgi ${RPM_BUILD_ROOT}%{_bindir}
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi

# install the DSO
cd ../build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
cp .libs/libphp5.so ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp5.so
cd ..

# strip binaries
/usr/bin/strip -X64 ${RPM_BUILD_ROOT}%{_bindir}/php
/usr/bin/strip -X64 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi
#/usr/bin/strip ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so


(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in * ;
    do
        mv $fic "$fic"_64
    done
)


# ===================================
# Second  Install the 32 bits versions
# ===================================
cd ../32bit

export OBJECT_MODE=32

# unfortunately 'make install-sapi' does not seem to work for use, therefore
# we have to install the targets separately
cd build-cgi
for TARGET in install-cli install-build install-headers install-programs ; do
    $MAKE INSTALL_ROOT=${RPM_BUILD_ROOT} ${TARGET}
done

# install the php-cgi binary
cp sapi/cgi/php-cgi ${RPM_BUILD_ROOT}%{_bindir}
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi

# install the DSO
cd ../build-apache
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
cp .libs/libphp5.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so
cd ..

# strip binaries
/usr/bin/strip -X32 ${RPM_BUILD_ROOT}%{_bindir}/php
/usr/bin/strip -X32 ${RPM_BUILD_ROOT}%{_bindir}/php-cgi
#/usr/bin/strip ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so

# move <files> (/opt/freeware/) bin to <files>_32 and link <files>_64 to <files> as 64bit is the default
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in bin
  do
      cd $dir
      for fic in * ;
      do
	  [ -L "$fic" ] && continue
          [ -f "$fic" ] || continue
	  echo  $fic | grep -e _32 -e _64 && continue	
          mv $fic $fic"_32"
          ln -s $fic"_64" $fic
      done
      cd -
  done
)




# ===================================
# End  Install the 32 bits versions
# ===================================

#SID $AR  -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.a ${RPM_BUILD_ROOT}/%{_libdir}/httpd/modules/libphp5.so
$AR -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.a ${RPM_BUILD_ROOT}/%{_libdir}/httpd/modules/libphp5.so
#SID $AR  -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.a ${RPM_BUILD_ROOT}/%{_libdir64}/httpd/modules/libphp5.so
$AR -q ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.a ${RPM_BUILD_ROOT}/%{_libdir64}/httpd/modules/libphp5.so

(
    cd ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/
    ln -s ../../../lib/httpd/modules/libphp5.a libphp5.a

)

/usr/bin/strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so
/usr/bin/strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp5.so


# install the Apache httpd config file for PHP
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf

# install the default configuration file and directories
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/php.ini
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/php.d

# create the PHP extension modules directory
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/modules
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/modules

# install the default icons
mkdir -p ${RPM_BUILD_ROOT}%{contentdir}/icons
chmod 755 ${RPM_BUILD_ROOT}%{contentdir}/icons
cp php.gif ${RPM_BUILD_ROOT}%{contentdir}/icons

# for third-party packaging:
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/php/pear
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/php/pear
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php
chmod 755 ${RPM_BUILD_ROOT}/var/lib/php
mkdir -p ${RPM_BUILD_ROOT}/var/lib/php/session
chmod 700 ${RPM_BUILD_ROOT}/var/lib/php/session


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin include
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%preun -n mod_php_ap22
removeFromHTTPDconf() {
    if [ -f $1 ]
    then
        cat $1 | \
        grep -v "# PHP settings" | \
        grep -v "Include conf/extra/httpd-php.conf" \
        >  $1.tmp
        [ -s $1.tmp ] && mv -f $1.tmp $1
        echo "Please restart your web server using: '$2 restart'"
    fi
}
preunAlternateLocation() {
    if [ -f $1/bin/httpd -a -d $1/conf ]
    then
        [ -f  $1/conf/extra/httpd-php.conf ] && rm -f $1/conf/extra/httpd-php.conf
        [ -f  $1/modules/libphp5.so ] && rm -f $1/modules/libphp5.so
        [ -f  $1/modules/libphp5.a ] && rm -f $1/modules/libphp5.a
        removeFromHTTPDconf $1/conf/httpd.conf $1/bin/apachectl
    fi
}


removeFromHTTPDconf %{_sysconfdir}/httpd/conf/httpd.conf %{_prefix}/sbin/apachectl
# remove some files to work with apache2
preunAlternateLocation %{_prefix}/apache2
# remove some files to work with IBMAHS
preunAlternateLocation /usr/IBMAHS

#if [ "$1" = 0 ]; then
# cat %{_sysconfdir}/httpd/conf/httpd.conf | \
# grep -v "# PHP settings" | \
# grep -v "Include conf/extra/httpd-php.conf" \
# > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
# mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
# echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
# fi


%post -n mod_php_ap22
slibclean
addToHTTPDconf() {
    if [ -f $1 ]
    then
        cat $1 | \
        grep -v "# PHP settings" | \
        grep -v "Include conf/extra/httpd-php.conf" \
        >  $1.tmp
        [ -s $1.tmp ] && mv -f $1.tmp $1
        echo "# PHP settings" >> $1
        echo "Include conf/extra/httpd-php.conf" >> $1
        echo "Please restart your web server using: '$2 restart'"
    fi
}
postAlternateLocation() {
    if [ -f $1/bin/httpd -a -d $1/conf -a `$1/bin/httpd -version 2>&1 | grep "Apache/2.4" | wc -l` = "1" ]
    then
        [ -d $1/modules ] && cp -p %{_libdir}/httpd/modules/libphp5.so $1/modules
        [ -d $1/modules ] && cp -p %{_libdir}/httpd/modules/libphp5.a $1/modules
#        [ -d $1/modules ] && cp -p %{_libdir64}/httpd/modules/libphp5.so $1/modules   No it's links, we copied same file in fact
#        [ -d $1/modules ] && cp -p %{_libdir64}/httpd/modules/libphp5.a $1/modules
        [ -d $1/conf/extra ] && cp -p  %{_sysconfdir}/httpd/conf/extra/httpd-php.conf $1/conf/extra
        addToHTTPDconf $1/conf/httpd.conf $1/bin/apachectl
    fi
}
if [ -f %{_prefix}/sbin/httpd -a `%{_prefix}/sbin/httpd -version 2>&1 | grep "Apache/2.2" | wc -l` = "1" ]
then
    addToHTTPDconf %{_sysconfdir}/httpd/conf/httpd.conf %{_prefix}/sbin/apachectl
fi
# copy some files to work with apache2
postAlternateLocation %{_prefix}/apache2
# copy some files to work with IBMAHS
postAlternateLocation /usr/IBMAHS

#cat %{_sysconfdir}/httpd/conf/httpd.conf | \
#  grep -v "# PHP settings" | \
# grep -v "Include conf/extra/httpd-php.conf" \
#  > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
#mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
#echo "# PHP settings" >> %{_sysconfdir}/httpd/conf/httpd.conf
#echo "Include conf/extra/httpd-php.conf" >> %{_sysconfdir}/httpd/conf/httpd.conf
#echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -n mod_php_ap22
%defattr(-,root,system)
%{_libdir}/httpd/modules/libphp5.so
%{_libdir64}/httpd/modules/libphp5.so
%{_libdir}/httpd/modules/libphp5.a
%{_libdir64}/httpd/modules/libphp5.a
%attr(0770,root,apache) %dir /var/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf
%{contentdir}/icons/php.gif


%files common
%defattr(-,root,system)
%doc 32bit/CODING_STANDARDS 32bit/CREDITS 32bit/EXTENSIONS 32bit/INSTALL 32bit/LICENSE 32bit/NEWS 32bit/README*
%doc 32bit/Zend/ZEND_*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir64}/php
%dir %{_libdir}/php/modules
%dir %{_libdir64}/php/modules
%dir /var/lib/php
%dir %{_libdir}/php/pear
%dir %{_libdir64}/php/pear


%files cli
%defattr(-,root,system)
%{_bindir}/php
%{_bindir}/php-cgi
%{_mandir}/man1/php.1
/usr/bin/php
/usr/bin/php-cgi

%{_bindir}/php_*
%{_bindir}/php-cgi_*
/usr/bin/php_*
/usr/bin/php-cgi_*


%files devel
%defattr(-,root,system)
#SID pourquoi pas
%dir %{_libdir64}/php
%dir %{_libdir}/php
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
#%{_libdir}/php/build
%{_mandir}/man1/php-config.1
%{_mandir}/man1/phpize.1
/usr/bin/php-config
/usr/bin/phpize
/usr/include/*


%{_bindir}/php-config_*
%{_bindir}/phpize_*
/usr/bin/php-config_*
/usr/bin/phpize_*

%changelog
* Tue Sep 27 2017 Daniele Silvestre <Daniele.Silvestre@atos.net> - 5.6.31-1
- updated to version 5.6.31 from 5.6.30

* Tue Mar 14 2017 Daniele Silvestre <Daniele.Silvestre@atos.net> - 5.6.30-1
- updated to version 5.6.30 from 5.5.17

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

* Tue Apr 03 2012 Michael Perzl <michael@perzl.org> - 5.3.10-2
- enabled multibyte string support and mcrypt support

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

