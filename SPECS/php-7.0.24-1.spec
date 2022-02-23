# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}
# compiler default gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%{!?optimize:%define optimize 2}


Summary: The PHP HTML-embedded scripting language
Name: php
Version: 7.0.24
Release: 1
License: The PHP License v3.01
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{name}-%{version}.tar.bz2
Source1: %{name}.conf
Source2: %{name}.ini
Source3: %{name}-%{version}-%{release}.build.log
Patch0: %{name}-7.0.7-aix-build.patch
#Patch1: %{name}-7.0.7-aix-network.patch
Patch1: %{name}-7.0.7-aix-setrlimit.patch
Patch2: %{name}-7.0.10-aix-tests.patch
Patch3: %{name}-7.0.7-aix-trailing-slash.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
%define _libdir64 %{_prefix}/lib64

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

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package mod_php
Summary: The PHP HTML-embedded scripting language module for Apache V2.4.X
Group: Development/Languages
Requires: %{name}-common = %{version}-%{release}
Requires: bzip2 >= 1.0.2-4
Requires: curl >= 7.47.1-1
Requires: httpd >= 2.4
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
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "optimize=%{optimize}"

%setup -q
%patch0 -p1 -b .build
#%patch1 -p1 -b .network
%patch1 -p1 -b .setrlimit
%patch2 -p1 -b .tests
%patch3 -p1 -b .trailing-slash

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

# shell function to configure and build a PHP tree
buildphp() {
    set -x
    ln -sf ../configure

./configure \
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
 --enable-zip=shared \
 --with-zlib-dir=/opt/freeware \
 --with-ldap=/opt/freeware \
 --enable-soap \
 --enable-bcmath \
 --enable-ftp \
 --enable-sockets \
 --enable-mbstring \
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


$MAKE --trace %{?_smp_mflags}
}

build_all()
{
set -x
# build the command line and the CGI version of PHP
mkdir -p build-cgi
cd build-cgi
buildphp \
    $*

if [ "%{dotests}" == 1 ]
then
    export http_proxy=""
    export https_proxy=""
    export TESTS="--offline"
    ( ( /usr/bin/yes n | $MAKE -k test ) || true )
    /usr/sbin/slibclean
fi
cd ..


# build the Apache module
mkdir -p  build-apache
cd build-apache
APXS=/opt/freeware/bin/apxs
# If IBM Apache LPP is installed, use it to build the Apache module
#SID if [ -f /usr/IBMAHS/bin/apxs ]; then
#SID    APXS=/usr/IBMAHS/bin/apxs
#SID fi
buildphp \
    --with-apxs2=${APXS} \
    $*

if [ "%{dotests}" == 1 ]
then
    export http_proxy=""
    export https_proxy=""
    export TESTS="--offline"
    ( ( /usr/bin/yes n | $MAKE -k test ) || true )
    /usr/sbin/slibclean
fi
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
export LDFLAGS="-L/opt/freeware/lib64"

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
export LD_LIBRARY_PATH="/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"

build_all \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}
cd .. 



%install
# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh
export AR="/usr/bin/ar "
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
cp .libs/libphp7.so ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir64}/httpd/modules/libphp7.so
cd ../..


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
cd 32bit

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
cp .libs/libphp7.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp7.so
cd ..


# move and strip binaries
for fic in php php-cgi
do
    /usr/bin/strip  -X32 ${RPM_BUILD_ROOT}%{_bindir}/$fic  > /dev/null 2>&1 || true
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
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf

# install the default configuration file and directories
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/php.ini
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf/php.ini
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
%{contentdir}/icons/php.gif


%files common
%defattr(-,root,system)
%doc 32bit/CODING_STANDARDS 32bit/CREDITS 32bit/EXTENSIONS 32bit/INSTALL 32bit/LICENSE 32bit/NEWS 32bit/README*
%doc 32bit/Zend/ZEND_*
%config(noreplace) %{_sysconfdir}/php.ini
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
/usr/bin/php
/usr/bin/php-cgi

%{_bindir}/php_*
%{_bindir}/php-cgi_*
#%{_mandir}/man1/php.1
/usr/bin/php_*
/usr/bin/php-cgi_*


%files devel
%defattr(-,root,system)
%dir %{_libdir}/php
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/build
#%{_mandir}/man1/php-config.1
#%{_mandir}/man1/phpize.1
/usr/bin/php-config
/usr/bin/phpize
/usr/include/*


%changelog
* Thu Oct  5 2017 Pascal Oliva <pascal.oliva@atos.net> 7.0.24-1
- Updated to version 7.0.24 (From 7.0.19)

* Tue May 11 2017 Tony Reix <tony.reix@atos.net> 7.0.19-1
- Updated to version 7.0.19 (From 7.0.17)

* Tue Mar 07 2017 Daniele Silvestre <daniele.silvestre@atos.net> 7.0.16-1
- updated to version 7.0.16 (From 7.0.15)

* Tue Feb 07 2017 Tony Reix <tony.reix@atos.net> 7.0.15-2
- Rebuilt for removing libssl.so as a requirement.

* Fri Jan 20 2017 Tony Reix <tony.reix@atos.net> 7.0.15-1
- First port on AIX 6.1

* Thu Jan 05 2017 Girardet Jean <jean.girardet@atos.net> 7.0.14-2
- build 64 bits version

* Thu Jan 05 2017 Girardet Jean <jean.girardet@atos.net> 7.0.14-1
- updated to version 7.0.14 (From 7.0.13)

* Mon Nov 21 2016 Girardet Jean <jean.girardet@atos.net> 7.0.13-1
- updated to version 7.0.13 (From 7.0.12)

* Wed Nov 16 2016 Girardet Jean <jean.girardet@atos.net> 7.0.12-1
- updated to version 7.0.12 (From 7.0.10)

* Fri Jul 22 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.9-1
- updated to version 7.0.9

* Wed Jul 21 2016 Jean Girardet <jean.girardet@atos.net> 7.0.8-1
- updated to version 7.0.8

* Wed Jun 15 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 7.0.7-1
- updated to version 7.0.7

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

