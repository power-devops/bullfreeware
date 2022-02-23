%define contentdir /var/www

Summary: The PHP HTML-embedded scripting language
Name: php
Version: 5.3.11
Release: 1
License: The PHP License v3.01
Group: Development/Languages
URL: http://www.php.net/

Source0: http://www.php.net/distributions/%{name}-%{version}.tar.bz2
Source1: %{name}.conf
Source2: %{name}.ini
Patch0: %{name}-%{version}-aixconfig.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: make

BuildRequires: gd-devel >= 2.0.35
BuildRequires: bzip2, libjpeg-devel, libpng-devel, zlib-devel
BuildRequires: httpd-devel >= 2.2.15-1
BuildRequires: curl-devel >= 7.19.7
BuildRequires: openssl-devel >= 0.9.8, freetype2-devel >= 2.3.12, t1lib-devel
BuildRequires: pcre-devel >= 7.9-2
BuildRequires: libxml2-devel >= 2.6.32-2

Provides: mod_php = %{version}-%{release}

Requires: httpd >= 2.2.15-1
Requires: %{name}-common = %{version}-%{release}
Requires: gd >= 2.0.35
Requires: bzip2, libjpeg, libpng, zlib
Requires: curl >= 7.19.7
Requires: openssl >= 0.9.8, freetype2 >= 2.3.12, t1lib
Requires: pcre >= 7.9-2
Requires: libxml2 >= 2.6.32-2

%description
#PHP is an HTML-embedded scripting language. PHP attempts to make it
#easy for developers to write dynamically generated webpages. PHP also
#offers built-in database integration for several commercial and
#non-commercial database management systems, so writing a
#database-enabled webpage with PHP is fairly simple. The most common
#use of PHP coding is probably as a replacement for CGI scripts. 

#The php package contains the module which adds support for the PHP
#language to Apache HTTP Server.


PHP is an HTML-embedded scripting language. Much of its syntax is 
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web
developers to write dynamically generated pages quickly.



%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Provides: %{name}-cgi = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: gd >= 2.0.35
Requires: bzip2, libjpeg, libpng, zlib
Requires: curl >= 7.19.7
Requires: openssl >= 0.9.8, freetype2 >= 2.3.12, t1lib
Requires: pcre >= 7.9-2
Requires: libxml2 >= 2.6.32-2
Requires: httpd >= 2.2.22

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
Requires: %{name} = %{version}-%{release}
Requires: gd-devel >= 2.0.35
Requires: bzip2, libjpeg-devel, libpng-devel, zlib-devel
Requires: curl-devel >= 7.19.7
Requires: httpd-devel >= 2.2.15-1
Requires: openssl-devel >= 0.9.8, freetype2-devel >= 2.3.12, t1lib-devel
Requires: pcre-devel >= 7.9-2
Requires: libxml2-devel >= 2.6.32-2

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.


%prep
%setup -q
%patch0 -p1 -b .aixconfig


%build
export CC="/usr/vac/bin/xlc_r"

# install extension modules in %{_libdir}/php/modules.
export EXTENSION_DIR=%{_libdir}/php/modules

# shell function to configure and build a PHP tree
buildphp() {
ln -sf ../configure
./configure \
    --cache-file=../config.cache \
    --prefix=%{_prefix} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --enable-shared --enable-static \
    --without-pear \
    --with-gd=%{_prefix} \
    --with-openssl=%{_prefix} \
    --with-zlib \
    --with-bz2 \
    --with-curl=%{_prefix} \
    --with-t1lib=%{_prefix} \
    --with-freetype-dir=%{_prefix} \
    --with-jpeg-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} \
    --with-zlib-dir=%{_prefix} \
    --enable-soap \
    --enable-bcmath \
    --enable-ftp \
    --enable-sockets \
    --with-iconv \
    --with-mysqli=mysqlnd \
    --enable-dom \
    --enable-json \
    --with-pcre-regex=%{_prefix} \
	-with-xml=shared \
    $*
make 
}


# build the command line and the CGI version of PHP
mkdir build-cgi
cd build-cgi
buildphp
cd ..


# build the Apache module
mkdir build-apache
cd build-apache
buildphp \
    --with-apxs2=%{_prefix}/apache2/bin/apxs
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
#mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/modules
#chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/apache2/modules
#cp .libs/libphp5.so ${RPM_BUILD_ROOT}%{_prefix}/apache2/modules
#chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/apache2/modules/libphp5.so
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
cp .libs/libphp5.so ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so
cd ..

# strip binaries
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/php
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/php-cgi
/usr/bin/strip ${RPM_BUILD_ROOT}%{_libdir}/httpd/modules/libphp5.so

# install the Apache httpd config file for PHP
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/httpd-php.conf

# install the default configuration file and directories
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/php.ini
#mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf
#cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/apache2/conf/php.ini
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


%preun
if [ "$1" = 0 ]; then
    cat %{_sysconfdir}/httpd/conf/httpd.conf | \
      grep -v "# PHP settings" | \
      grep -v "Include conf/extra/httpd-php.conf" \
      > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
    mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
    echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
fi
# remove some files to work with apache2
if [ -f %{_prefix}/apache2/bin/httpd -a -d %{_prefix}/apache2/conf ]
then
     [ -f  %{_prefix}/apache2/conf/php.ini ] && rm -f %{_prefix}/apache2/conf/php.ini
     [ -f  %{_prefix}/apache2/modules/libphp5.so ] && rm -f %{_prefix}/apache2/modules/libphp5.so
     grep -v "LoadModule php5_module" %{_prefix}/apache2/conf/httpd.conf >%{_prefix}/apache2/conf/httpd.conf.tmp
     [ -s %{_prefix}/apache2/conf/httpd.conf.tmp ] && \
      mv -f  %{_prefix}/apache2/conf/httpd.conf.tmp  %{_prefix}/apache2/conf/httpd.conf
fi


%post
slibclean
if [ -f %{_sysconfdir}/httpd/conf/httpd.conf ]
then
   cat %{_sysconfdir}/httpd/conf/httpd.conf | \
     grep -v "# PHP settings" | \
     grep -v "Include conf/extra/httpd-php.conf" \
     > %{_sysconfdir}/httpd/conf/tmp_httpd.conf
   mv -f %{_sysconfdir}/httpd/conf/tmp_httpd.conf %{_sysconfdir}/httpd/conf/httpd.conf
fi
echo "# PHP settings" >> %{_sysconfdir}/httpd/conf/httpd.conf
echo "Include conf/extra/httpd-php.conf" >> %{_sysconfdir}/httpd/conf/httpd.conf
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
# copy some files to work with apache2
if [ -f %{_prefix}/apache2/bin/httpd -a -d %{_prefix}/apache2/conf ]
then
     cp -p %{_sysconfdir}/php.ini %{_prefix}/apache2/conf
     [ -d %{_prefix}/apache2/modules ] && cp -p %{_libdir}/httpd/modules/libphp5.so %{_prefix}/apache2/modules
     grep -w "LoadModule php5_module" %{_prefix}/apache2/conf/httpd.conf; status=$?
     if [ "${status}" -eq 0 ]
     then
	:
     else
          awk "{  print \$0
               i=match(\$0,/^# LoadModule /) ;
                 if ( i != 0 ) {
                    print \"LoadModule php5_module modules/libphp5.so\"
                 }
               }" %{_prefix}/apache2/conf/httpd.conf > %{_prefix}/apache2/conf/httpd.conf.tmp
	       [ -s %{_prefix}/apache2/conf/httpd.conf.tmp ] && mv -f  %{_prefix}/apache2/conf/httpd.conf.tmp  %{_prefix}/apache2/conf/httpd.conf
     fi

fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
#%{_prefix}/apache2/modules/libphp5.so
%{_libdir}/httpd/modules/libphp5.so
%attr(0770,root,nobody) %dir /var/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf/extra/httpd-php.conf
%{contentdir}/icons/php.gif


%files common
%defattr(-,root,system)
%doc CODING_STANDARDS CREDITS EXTENSIONS INSTALL LICENSE NEWS README*
%doc Zend/ZEND_*
%config(noreplace) %{_sysconfdir}/php.ini
#%config(noreplace) %{_prefix}/apache2/conf/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%dir /var/lib/php
%dir %{_libdir}/php/pear


%files cli
%defattr(-,root,system)
%{_bindir}/php
%{_bindir}/php-cgi
%{_mandir}/man1/php.1
/usr/bin/php
/usr/bin/php-cgi


%files devel
%defattr(-,root,system)
%dir %{_libdir}/php
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php
%{_libdir}/php/build
%{_mandir}/man1/php-config.1
%{_mandir}/man1/phpize.1
/usr/bin/php-config
/usr/bin/phpize
/usr/include/*


%changelog
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
