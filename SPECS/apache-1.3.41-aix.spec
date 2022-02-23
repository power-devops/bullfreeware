# Use --define 'nossl 1' on the command line to disable SSL detection
%{!?nossl:%define SSL 1}
%{?nossl:%define SSL 0}
%define ssldir %{_prefix}

%define EAPI_vers  2.8.31
%define apache_vers 1.3.41
%define ssl_vers 0.9.71

Summary: The most widely used Web server on the Internet.
Name: apache
Version: %{apache_vers}
Release: 1%{!?nossl:ssl}
Group: System Environment/Daemons
Source0: ftp://ftp.apache.org/apache/dist/apache_%{apache_vers}.tar.gz
%if %{SSL} == 1
Source1: http://www.modssl.org/source/mod_ssl-%{EAPI_vers}-%{apache_vers}.tar.gz
%endif
Source2: IBM_ILA
Patch0: apache-nobody.patch
URL: http://www.apache.org
License: IBM_ILA
BuildRoot: %{_tmppath}/apache-root
Provides: webserver
Prefix: %{_prefix}
%if %{SSL} == 1
Prereq: openssl
%endif

# AIX BUILDERS, PLEASE NOTE:
#  If building with xlc version 3.6.X rather than gcc, you must ensure
# you have the following PTF's installed on your system, or
# you will see a runtime error that says:
#    "Expected </Directory> but saw </Directory>"
# PTFS needed: U462006 U462007 U462023 U462024 U462025 U462026 U462027
# Refer to http://service.software.ibm.com/support/rs6000, or
# set CC=gcc to force use of the GCC compiler.

%define stdlib lib
%define liblink ../..
%define DEFCC xlc

%description
Apache is a powerful, full-featured, efficient and freely-available
Web server. Apache is also the most popular Web server on the
Internet.

Install the apache package if you need a Web server.

%if %{SSL} == 1
%package -n mod_ssl
Group: System Environment/Daemons
URL: http://www.modssl.org
Version: %{EAPI_vers}
Summary: Cryptography support for the Apache web server.
Requires: apache = %{apache_vers}
Prereq: openssl

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache web
server via the Secure Sockets Layer (SSL) and Transport Layer Security
(TLS) protocols.
%endif

%package devel
Group: Development/Libraries
Summary: Development tools for the Apache Web server.
Version: %{apache_vers}
Obsoletes: secureweb-devel

%description devel
The apache-devel package contains the APXS binary.

If you are installing the Apache Web server, and you want to be 
able to compile or develop additional modules for Apache, you'll 
need to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache Web server.
Version: %{apache_vers}

%description manual
The apache-manual package contains the complete manual and reference
guide for the Apache Web server.  If you need Apache documentation
installed on the local machine, install this package.  The information
can also be found on the Web at http://www.apache.org/docs/.


%prep
%setup -q -n apache_%{apache_vers}
%patch0 -p1 -b .nobody

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE.new
cat LICENSE >> LICENSE.new
mv LICENSE.new LICENSE

#
# Add additional symbols to httpd's export file
#
cat >> src/support/httpd.exp <<EOF
ap_os_dso_error
ap_os_dso_init
ap_os_dso_load
ap_os_dso_sym
ap_os_dso_unload
EOF

%if %{SSL} == 1
cd ..
[[ -d mod_ssl-%{EAPI_vers}-%{apache_vers} ]] \
    && rm -rf mod_ssl-%{EAPI_vers}-%{apache_vers}
%setup -q -n mod_ssl-%{EAPI_vers}-%{apache_vers} -T -b 1
%endif


%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export OPTIM="-O2"
    else
       export CC=gcc
       export OPTIM=$RPM_OPT_FLAGS
    fi
fi

%if %{SSL} == 1
# Build the SSL Version, with mod_ssl
cd $RPM_BUILD_DIR/mod_ssl-%{EAPI_vers}-%{apache_vers}

OPTIM="$OPTIM" \
./configure --with-apache=../apache_%{apache_vers} --with-ssl=%{prefix} \
   --prefix=%{prefix}/apache --enable-shared=ssl --enable-module=most \
   --enable-shared=max --enable-module=so --with-layout=opt \
   --without-confadjust
%else

# Build the regular version, no SSL
cd $RPM_BUILD_DIR/apache_%{apache_vers}
OPTIM="$OPTIM" \
./configure \
   --prefix=%{prefix}/apache --enable-module=most \
   --enable-shared=max --enable-module=so --with-layout=opt \
   --without-confadjust
%endif

cd $RPM_BUILD_DIR/apache_%{apache_vers}

if [[ "$CC" = "gcc" ]]
then
   make EXTRA_LDFLAGS="-L$(dirname $($CC -print-libgcc-file-name)) -lgcc" \
        LIBS_SHLIB="-L$(dirname $($CC -print-libgcc-file-name)) -lgcc"
else
   make
fi
	
%install
cd $RPM_BUILD_DIR/apache_%{apache_vers}
rm -rf $RPM_BUILD_ROOT
make install root=$RPM_BUILD_ROOT

# Link files in /usr/bin and /usr/sbin
(cd $RPM_BUILD_ROOT
 for dir in bin sbin
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/apache/$dir/* .
    cd -
 done
)

# The admin name is listed as the mail address of the person
# who builds the package.  But the builder (me) is not the administrator
# for everyone who installs this!
# It should be locally customized by the installer.
cd $RPM_BUILD_ROOT/etc/%{prefix}/apache
sed -e 's/^ServerAdmin.*$/ServerAdmin you@yourhost.domain/'  \
  -e 's/#ServerName.*$/#ServerName localhost.your.domain/' httpd.conf > ht.tmp 
mv ht.tmp httpd.conf
cd -

# install apache source code for devel package
#mkdir -p $RPM_BUILD_ROOT%{prefix}/src
#tar xzf $RPM_SOURCE_DIR/apache_%{apache_vers}.tar.gz -C $RPM_BUILD_ROOT%{prefix}/src
#find $RPM_BUILD_ROOT -type f | \
#	xargs grep -l "/usr/local/bin/perl5" | \
#	xargs perl -pi -e "s|/usr/local/bin/perl5|/usr/bin/perl|g;"

#find $RPM_BUILD_ROOT -type f | \
#	xargs grep -l "/usr/local/bin/perl" | \
#	xargs perl -pi -e "s|/usr/local/bin/perl|/usr/bin/perl|g;"

%if %{SSL} == 1
#install EAPI addons doc
install -m644  \
  $RPM_BUILD_DIR/mod_ssl-%{EAPI_vers}-%{apache_vers}/pkg.addon/mod_define.html \
  $RPM_BUILD_ROOT/%{prefix}/apache/share/htdocs/manual/mod/mod_define.html

# We don't want to ship these dummy files; we will generate them in %post.
rm -f $RPM_BUILD_ROOT/etc%{prefix}/apache/ssl.key/server.key || :
rm -f $RPM_BUILD_ROOT/etc%{prefix}/apache/ssl.crt/server.crt || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{SSL} == 1
%post -n mod_ssl
if [ ! -f /etc%{prefix}/apache/ssl.key/server.key ] ; then
%{prefix}/bin/openssl genrsa -rand \
/var/adm/wtmp:/unix:/etc/utmp:/etc/passwd:/var/adm/ras/errlog 1024 \
   > /etc%{prefix}/apache/ssl.key/server.key
fi

if [ ! -f /etc%{prefix}/apache/ssl.crt/server.crt ] ; then
cat << EOF | %{prefix}/bin/openssl req -new -key /etc%{prefix}/apache/ssl.key/server.key -x509 -days 365 -out /etc%{prefix}/apache/ssl.crt/server.crt 2>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
fi

%endif

%preun
if [ $1 = 0 ]; then
   %{prefix}/apache/sbin/apachectl stop > /dev/null 2>&1
fi
  
%files
%defattr(-,root,root)
%doc LICENSE ABOUT_APACHE Announcement README
%dir /etc/%{prefix}/apache
%config /etc/%{prefix}/apache/access.conf
%config /etc/%{prefix}/apache/srm.conf
%config /etc/%{prefix}/apache/httpd.conf
%config /etc/%{prefix}/apache/magic
%config /etc/%{prefix}/apache/mime.types
%dir /var/%{prefix}/apache
%dir /var/%{prefix}/apache/logs
%dir /var/%{prefix}/apache/run
%dir /var/%{prefix}/apache/proxy
%dir %{prefix}/apache
%dir %{prefix}/apache/share
%{prefix}/apache/share/cgi-bin
%{prefix}/apache/share/icons
%dir %{prefix}/apache/man
%dir %{prefix}/apache/man/man1
%dir %{prefix}/apache/man/man8
%{prefix}/apache/man/man1/*
%{prefix}/apache/man/man8/ab.8
%{prefix}/apache/man/man8/apachectl.8
%{prefix}/apache/man/man8/httpd.8
%{prefix}/apache/man/man8/logresolve.8
%{prefix}/apache/man/man8/rotatelogs.8
%dir %{prefix}/apache/sbin
%{prefix}/apache/sbin/ab
%{prefix}/apache/sbin/httpd
%{prefix}/apache/sbin/logresolve
%{prefix}/apache/sbin/rotatelogs
%{prefix}/apache/sbin/apachectl
%dir %{prefix}/apache/bin
%{prefix}/apache/bin/dbmmanage
%{prefix}/apache/bin/htdigest
%{prefix}/apache/bin/htpasswd
%dir %{prefix}/apache/libexec
%{prefix}/apache/libexec/mod*.so
%{prefix}/apache/libexec/libproxy.so
/usr/bin/dbmmanage
/usr/bin/htdigest
/usr/bin/htpasswd
/usr/sbin/ab
/usr/sbin/apachectl
/usr/sbin/httpd
/usr/sbin/logresolve
/usr/sbin/rotatelogs

#%attr(-,nobody,nobody) %dir /var/cache/httpd
#%dir /var/log/httpd

%files manual
%defattr(-,root,root)
%doc LICENSE
%{prefix}/apache/share/htdocs

%files devel
%defattr(-,root,root)
%doc LICENSE
%dir %{prefix}/apache/include
%{prefix}/apache/include/*
%dir %{prefix}/apache/sbin
%{prefix}/apache/sbin/apxs
%{prefix}/apache/libexec/httpd.exp
%dir %{prefix}/apache/man
%dir %{prefix}/apache/man/man8
%{prefix}/apache/man/man8/apxs.8*
/usr/sbin/apxs

%if %{SSL} == 1
%files -n mod_ssl
%defattr(-,root,root)
%doc LICENSE $RPM_SOURCE_DIR/SSL-Certificate-Creation
%{prefix}/apache/share/htdocs/manual/mod/mod_ssl/
%{prefix}/apache/libexec/libssl.so
%attr(0700,root,root) %dir /etc%{prefix}/apache/ssl.*
/etc%{prefix}/apache/ssl.*/*
%endif

%changelog
* Wed Sep 24 2008 Jean-Noel Cordenner <jean-noel.cordenner@bull.net> 1.3.41
- Update to 1.3.41 with mod_ssl 2.8.31.

* Wed Jun 16 2004 David Clissold <cliss@austin.ibm.com> 1.3.31-1
- Update to 1.3.31.

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

* Wed Mar 01 2000 Nalin Dahyabhai <nalin@redhat.com>
- make suexec limit UIDs and GIDs to < 51 instead of 100

* Fri Feb 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.3.12
- add EAPI patch

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- ifmodule directive for php stuff.
- load mod_perl before mod_php (#8169)

* Tue Feb 14 2000 Zach Brown <zab@redhat.com>
- minor fix to phhttpd patch

* Thu Feb 10 2000 Preston Brown <pbrown@redhat.com>
- improved default index.html.

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- strip dynamically loadable modules.

* Mon Feb 02 2000 Zach Brown <zab@redhat.com>
- add phhttpd 'Tunnel' directive and code to use it

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix depenencies

* Tue Jan 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.11
- deal with the fact that RPM now gzips man pages

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- new poweredby.png w/new logo
- apxs.8 man page moved to devel archive (#6661)
- don't remove old logfiles on package de-install (#8268)
- more updates to logrotate to avoid spurious cron mail (#8110)

* Mon Jan 10 2000 Preston Brown <pbrown@redhat.com>
- mod_throttle added; mod_bandwidth updated.

* Mon Dec 17 1999 Dale Lovelace <dale@redhat.com>
- Add configuration for mod_put to httpd.conf

* Mon Dec 06 1999 Preston Brown <pbrown@redhat.com>
- documentation cleanups in httpd.conf (#5357, #6655)
- fixed logrotate script to ignore error if no apache running (#7074)

* Wed Nov 10 1999 Jeff Johnson <jbj@redhat.com>
- add put module.

* Thu Nov 04 1999 Preston Brown <pbrown@redhat.com>
- make suexec non-suid.  People can enable it if they wish themselves.
- somehow the unified httpd.conf got trashed.  fixed.
- manual is now a subpackage
- point to /usr/share/magic as the magic file location; don't use the
  apache-specific one.
- fix apxs module installation issues (#5650)


* Tue Sep 21 1999 Bill Nottingham <notting@redhat.com>
- move DSO in httpd.conf to after ServerRoot

* Mon Sep 20 1999 Preston Brown <pbrown@redhat.com>
- it is httpd stop, not httpsd stop (# 5254)
- suexec added (# 5257)

* Thu Sep 09 1999 Preston Brown <pbrown@redhat.com>
- remove apachectl man page (# 4459)

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.3.9
- fix bug # 3680 (suexec docroot was wrong)
- fix bug # 2378 (logrotate with -USR1 not -HUP)
- fix bug # 3548 (logrotate complains if apache not running)
- httpd.conf is now in the unified apache format as distributed

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Sat May 21 1999 Bill Nottingham <notting@redhat.com>
- fix broken link in index.html

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- allow indexes in /doc

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Mon Apr 05 1999 Preston Brown <pbrown@redhat.com>
- prerequire /bin/rm, added /doc path pointing to /usr/doc for localhost

* Fri Mar 26 1999 Preston Brown <pbrown@redhat.com>
- updated log rotating scripts to not complain if logs aren't present.

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- fixed up path to perl

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- updated init script to conform to new standards
- upgraded to 1.3.6, fixed apxs patch

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- clean up logfiles on deinstallation

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Mar 12 1999 Cristian Gafton <gafton@redhat.com>
- added mod_bandwidth
- updated to 1.3.4
- prereq mailcap

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- added patch to disable building support for ndbm
- build against glibc 2.1

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.3.3 to catch up with bug fixes
- added the /usr/bin/* binaries to the spec file list

* Fri Sep 25 1998 Cristian Gafton <gafton@redhat.com>
- change ownership of cache dir to nobody
- added "Red Hat" to the server string
- updated to version 1.3.2
- fixed all references to httpsd in config files

* Fri Sep 04 1998 Cristian Gafton <gafton@redhat.com>
- small fixes to the spec file
- patch to handle correctly the -d <newroot> option
- leave out the .usr.src.apache_%{version} for now

* Thu Sep 03 1998 Preston Brown <pbrown@redhat.com>
- patched apxs not to bomb out if it can't find httpd

* Wed Sep 02 1998 Preston Brown <pbrown@redhat.com>
- upgraded to apache 1.3.1.
- Heavy rewrite.
- changed providing a_web_server to just webserver.  Humor is not an option.

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- updated to build as non-root user
- added patch to defeat header dos attack

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- fixed the default config files to be more paranoid about security

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed init script
- added index.htm to the list of acceptable indexes

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.2.6
- added post script to install htm extension for text/html into
  /etc/mime.types

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced sysv init script

* Tue Jan 06 1998 Erik Troan <ewt@redhat.com>
- updated to 1.2.5, which includes many security fixes

* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed overkill on http.init stop

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- added patch for backslash DOS attach

* Thu Nov 06 1997 Donnie Barnes <djb@redhat.com>
- added htdigest binary to file list

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- made the default index.html be config(noreplace) so we no longer
  blow away other folks' index.html

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- added restart|status options to initscript
- renamed httpd.init to httpd

* Tue Oct 07 1997 Elliot Lee <sopwith@redhat.com>
- Redid spec file, patches, etc. from scratch.
