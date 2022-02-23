Summary: The PHP scripting language.
Name: php
Version: 5.2.4
Release: 1
Group: Development/Languages
URL: http://www.php.net/
Source0: http://www.php.net/distributions/php-%{version}.tar.bz2
License: PHP
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: mod_php, php3, phpfi
Prefix: %{_prefix}
%define DEFCC cc

%define contentdir %{prefix}/%{name}-%{version}

%description
PHP is an HTML-embeddable scripting language.  PHP offers built-in database
integration for several commercial and non-commercial database management
systems, so writing a database-enabled script with PHP is fairly simple.  The
most common use of PHP coding is probably as a replacement for CGI scripts.

%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions.

%description devel
The php-devel package contains the files needed for building PHP
extensions.  If you need to compile your own PHP extensions, you will
need to install this package.

%prep
%setup -q

cp Zend/LICENSE Zend/ZEND_LICENSE

%build
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export CXX=xlC
    else 
       export CC=gcc
    fi
fi
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

# A basic configure and make


#./configure --prefix=%{prefix} --with-apxs2 --without-mysql \
#    --with-config-file-path=%{prefix}/apache/conf --with-ftp \
#    --with-zlib --with-system-regex --with-ftp 

#Using Nicolas' options
./configure --prefix=%{prefix} \
            --with-apxs2=%{prefix}/apache/bin/apxs \
            --disable-cgi --enable-cli \
            --with-mysqli=%{prefix}/mysql/bin/mysql_config \
            --with-config-file-path=%{prefix}/apache/conf

make

%install
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

for dir in Zend TSRM main regex ext/standard ; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/php/$dir
  cd $dir
  cp -p *.h $RPM_BUILD_ROOT%{_prefix}/include/php/$dir
  cd -
done
cp -p *.h $RPM_BUILD_ROOT%{_prefix}/include/php

mkdir -p $RPM_BUILD_ROOT%{_prefix}/apache/modules
cp .libs/libphp5.so $RPM_BUILD_ROOT%{_prefix}/apache/modules/libphp5.so
chmod 755 $RPM_BUILD_ROOT%{_prefix}/apache/modules/libphp5.so
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/extensions/no-debug-non-zts-20001214


./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Benchmark
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Crypt
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Date
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/DB
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/File
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/HTML
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Mail
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Net
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/Payment
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/PEAR
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/php/XML
./build/shtool mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
./build/shtool mkdir -p $RPM_BUILD_ROOT/etc%{_prefix}/apache
./build/shtool install -c -m 644 ./php.ini-dist $RPM_BUILD_ROOT/etc%{_prefix}/apache/php.ini

for prog in phpize php-config ; do
  ./build/shtool install -c -m 755 scripts/$prog $RPM_BUILD_ROOT%{_prefix}/bin/$prog
done


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%post
#echo "The php5 module is now installed.  For Apache, you will need to add the"
#echo "module to your /opt/freeware/apache/conf/httpd.conf file, e.g.:"
#echo "LoadModule php5_module	modules/libphp5.so"
#echo "  and"
#echo "AddModule mod_php5.c"
perl -pi -e 's|#AddType application/x-httpd-php .php|AddType application/x-httpd-php .php|g' \
        /opt/freeware/apache/conf/httpd.conf
perl -pi -e 's|#AddType application/x-httpd-php-source .phps|AddType application/x-httpd-php-source .phps|g' \
        /opt/freeware/apache/conf/httpd.conf

%files
%defattr(-,root,system)
%doc CODING_STANDARDS CREDITS INSTALL LICENSE
%doc NEWS README.* Zend/ZEND_*
%config /etc/%{prefix}/apache/php.ini
%{prefix}/apache/modules/libphp5.so

%files devel
%defattr(-,root,system)
%{_bindir}/php-config
%{_bindir}/phpize
%{_includedir}/php


%changelog
* Wed Oct 10 2007 Christophe Belle <christophe.belle@bull.net> - 5.2.4-1
- Update to version 5.2.4 for AIX 52S

* Mon Jul 09 2007 xxxx xxxx <xxxx@austin.ibm.com> 5.2.3-1
- Update to version 5.2.3

* Mon May 14 2007 xxxx xxxx <xxxx@austin.ibm.com> 5.2.2-1
- Update to version 5.2.2

* Fri May 04 2007 xxxx xxxx <xxxx@austin.ibm.com> 5.2.1-1
- Update to version 5.2.1

* Mon Apr 24 2006 Reza Arbab <arbab@austin.ibm.com> 5.1.2-1
- Update to version 5.1.2

* Tue Oct 12 2004 David Clissold <cliss@austin.ibm.com> 5.0.2-1
- Update to version 5.0.2

* Mon Oct 11 2004 David Clissold <cliss@austin.ibm.com> 4.3.9-1
- Update to version 4.3.9

* Fri Apr 26 2002 David Clissold <cliss@austin.ibm.com>
- The ext/xml subdirectory is GPL, but PHP is distributed under the
- PHP license.  GPL does not allow that.  Removed all of ext/xml
- from the tar image and am building --without-xml.

* Wed Feb 27 2002 David Clissold <cliss@austin.ibm.com>
- Add security patch posted today on php.net

* Mon Sep 17 2001 David Clissold <cliss@austin.ibm.com>
- Add a build conflict with the non-ssl apache.
- Now build with --with-mysql

* Wed Sep 05 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 4.0.6.
- Now build with --with-mysql

* Thu Jul 12 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix typo in contentdir definition for manuals
- Put manuals under %{prefix}/share

* Tue Jul 10 2001 David Clissold <cliss@austin.ibm.com>
- The php-%{version}-conf.patch was only being included in the SRPM
- when built on 'ppc' platform. (We only want it applied on ppc, but
- should always be included in the source).

* Thu Jun 07 2001 David Clissold <cliss@austin.ibm.com>
- update to version 4.0.5.  Add the php.ini file and some addt'l
- configure options to more closely match RedHat's PHP build.
- Also, build with gcc; otherwise include and require does not
- work, for some reason.

* Mon Mar 26 2001 David Clissold <cliss@austin.ibm.com>
- simplify and rework file for AIX 4.3.

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Feb 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- obsolete the old phpfi (PHP 2.x) package

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a commented-out curl extension to the config file (part of #24933)
- fix the PEAR-installation-directory-not-being-eval'ed problem (#24938)
- find the right starting point for multipart form data (#24933)

* Tue Jan 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- aaarrgh, the fix breaks something else, aaarrgh; revert it (#24933)
- terminate variable names at the right place (#24933)

* Sat Jan 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the fix some more

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- extract stas's fix for quoting problems from CVS for testing
- tweak the fix, ask the PHP folks about the tweak
- tweak the fix some more

* Wed Jan 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge mod_php into the main php package (#22906)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- try to fix a quoting problem

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.4 to get a raft of bug fixes
- enable sockets
- enable wddx

* Fri Nov  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in updated environment

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- add more commented-out modules to the default config file (#19276)

* Wed Nov  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix not-using-gd problem (#20137)

* Tue Oct 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.3pl1 to get some bug fixes

* Sat Oct 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- build for errata

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.3 to get security fixes integrated
- patch around problems configuring without Oracle support
- add TSRM to include path when building individual modules

* Fri Sep  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment
- enable OpenSSL support

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.2, and move the peardir settings to configure (#17171)
- require %%{version}-%%{release} for subpackages
- add db2-devel and db3-devel prereqs (#17168)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (new imap-devel)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summary and descriptions to match the specspo package

* Wed Aug  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- hard-code the path to apxs in build_ext() (#15799)

* Tue Aug  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add "." to the include path again, which is the default

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable PEAR and add it to the include path
- add the beginnings of a -devel subpackage

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweaks to post and postun from Bill Peck

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- fixes from Nils for building the MySQL client
- change back to requiring %{version} instead of %{version}-%{release}

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.1pl2
- enable MySQL client
- move the php.ini file to %{_sysconfdir}

* Fri Jun 30 2000 Nils Philippsen <nils@redhat.de>
- build_ext defines HAVE_PGSQL so pgsql.so in fact contains symbols
- post/un scripts tweak php.ini correctly now

* Thu Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.0.1
- refresh manual

* Tue Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new krb5 package

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new db3 package

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix syntax error in post and preun scripts.
- Disable IMAP, LDAP, PgSql in the standalone version because it picks up
  the extensions.

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- Unexclude the Sparc arch.
- Exclude the ia64 arch until we get a working Postgres build.
- Stop stripping extensions as aggressively.
- Start linking the IMAP module to libpam again.
- Work around extension loading problems.
- Reintroduce file-editing post and preun scripts for the mod_php extensions
  until we come up with a better way to do it.

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- ExcludeArch: sparc for now

* Sun Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Obsoletes: phpfi, because their content handler names are the same
- add standalone binary, rename module packages to mod_php
- FHS fixes

* Tue May 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- change license from "GPL" to "PHP"
- add URL: tag
- disable mysql support by default (license not specified)

* Mon May 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to PHP 4.0.0
- nuke the -mysql subpackage (php comes with a bundled mysql client lib now)

* Tue May 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- link IMAP module against GSS-API and PAM to get dependencies right
- change most of the Requires to Prereqs, because the post edits config files
- move the PHP *Apache* module back to the right directory
- fix broken postun trigger that broke the post
- change most of the postuns to preuns in case php gets removed before subpkgs

* Thu May 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuilt against new postgres libraries

* Tue May 09 2000 Preston Brown <pbrown@redhat.com>
- php3 .so modules moved to /usr/lib/php3 from /usr/lib/apache (was incorrect)

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- make subpackages require php = %{version} (bug #10671)

* Thu Apr 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0.16

* Fri Mar 03 2000 Cristian Gafton <gafton@redhat.com>
- fixed the post script to work when upgrading a package
- add triggere to fix the older packages

* Tue Feb 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0.15
- add build-time dependency for openldap-devel
- enable db,ftp,shm,sem support to fix bug #9648

* Fri Feb 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- add dependency for imap subpackage
- rebuild against Apache 1.3.12

* Thu Feb 24 2000 Preston Brown <pbrown@redhat.com>
- don't include old, outdated manual.  package one from the php distribution.

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependency problem

* Fri Jan 14 2000 Preston Brown <pbrown@redhat.com>
- added commented out mysql module, thanks to Jason Duerstock 
  (jason@sdi.cluephone.com). Uncomment to build if you have mysql installed.

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- rely on imap-devel, don't include imap in src.rpm (#5099).
- xml enabled (#5393)

* Tue Nov 02 1999 Preston Brown <pborwn@redhat.com>
- added post/postun sections to modify httpd.conf (#5259)
- removed old obsolete faq and gif (#5260)
- updated manual.tar.gz package (#5261)

* Thu Oct 07 1999 Matt Wilson <msw@redhat.com>
- rebuilt for sparc glibc brokenness

* Fri Sep 24 1999 Preston Brown <pbrown@redhat.com>
- --with-apxs --> --with-apxs=/usr/sbin/apxs (# 5094)
- ldap support (# 5097)

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- fix cmdtuples for postgresql, I had it slightly wrong

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- subpackages must obsolete old stuff...

* Sun Aug 29 1999 Preston Brown <pbrown@redhat.com>
- added -DHAVE_PGCMDTUPLES for postgresql module (bug # 4767)

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- name change to php to follow real name of package
- fix up references to php3 to refer to php
- upgrade to 3.0.12
- fixed typo in pgsql postun script (bug # 4686)

* Mon Jun 14 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.9
- fixed postgresql module and made separate package
- separated manual into separate documentation package

* Mon May 24 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.8, which fixes problems with glibc 2.1.
- took some ideas grom Gomez's RPM.

* Tue May 04 1999 Preston Brown <pbrown@redhat.com>
- hacked in imap support in an ugly way until imap gets an official
  shared library implementation

* Fri Apr 16 1999 Preston Brown <pbrown@redhat.com>
- pick up php3.ini

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- build against apache 1.3.6

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 3.0.7.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to php 3.0.6, built against apache 1.3.4

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- rebuild for apache 1.3.3

* Thu Oct 08 1998 Preston Brown <pbrown@redhat.com>
- updated to 3.0.5, fixes nasty bugs in 3.0.4.

* Sun Sep 27 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.0.4 and recompiled for apache 1.3.2

* Thu Sep 03 1998 Preston Brown <pbrown@redhat.com>
- improvements; builds with apache-devel package installed.

* Tue Sep 01 1998 Preston Brown <pbrown@redhat.com>
- Made initial cut for PHP3.
