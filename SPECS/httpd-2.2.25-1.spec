%define apache_vers 2.2.25

Summary: The most widely used Web server on the Internet.
Name: httpd
Version: %{apache_vers}
Release: 1
Group: System Environment/Daemons
Source0: ftp://ftp.apache.org/apache/dist/%{name}-%{version}.tar.bz2
Patch0: %{name}-%{version}-aixconf.patch
Patch1: %{name}-%{version}-httpdconf.patch

URL: http://www.apache.org
License: Apache
BuildRoot: /var/tmp/httpd-%{apache_vers}-root
Provides: webserver
Prefix: %{_prefix}

%define DEFCC cc

%description
Apache is a powerful, full-featured, efficient and freely-available Web server.
Apache is also the most popular Web server on the Internet.

%package devel
Group: Development/Libraries
Summary: Development tools for the Apache Web server.
Version: %{apache_vers}
Obsoletes: secureweb-devel

%description devel
The apache-devel package contains the APXS binary.

If you are installing the Apache Web server, and you want to compile or develop
additional modules for Apache, you'll need to install this package.

%package manual
Group: Documentation
Summary: Documentation for the Apache Web server.
Version: %{apache_vers}

%description manual
The apache-manual package contains the complete manual and reference guide for
the Apache Web server.  The information can also be found on the Web at
http://www.apache.org/docs/.


%prep
%setup -q

%patch0 -p1 -b .aixconf
%patch1 -p1 -b .httpdconf


%build
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export RM="/usr/bin/rm -f"

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

cd $RPM_BUILD_DIR/httpd-%{apache_vers}

LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
OPTIM="$OPTIM" \
./configure \
    --prefix=%{prefix}/apache2 \
    --enable-so \
    --enable-proxy \
    --enable-dav \
    --enable-cache --enable-mem-cache \
    --enable-file-cache --enable-disk-cache \
    --enable-ldap \
    --enable-mods-shared="all ssl ldap cache proxy \
	authn_alias mem_cache file_cache authnz_ldap charset_lite dav_lock disk_cache" \


cd $RPM_BUILD_DIR/httpd-%{apache_vers}

if [[ "$CC" = "gcc" ]]
then
   make EXTRA_LDFLAGS="-L$(dirname $($CC -print-libgcc-file-name)) -lgcc" \
        LIBS_SHLIB="-L$(dirname $($CC -print-libgcc-file-name)) -lgcc"
else
   make
fi
	
%install
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

cd $RPM_BUILD_DIR/httpd-%{apache_vers}
rm -rf $RPM_BUILD_ROOT

make LIBPATH="$RPM_BUILD_ROOT/opt/freeware/apache2/lib:/opt/freeware/lib" DESTDIR=$RPM_BUILD_ROOT root=$RPM_BUILD_ROOT install

cd $RPM_BUILD_ROOT%{prefix}/apache2/bin
for file in $(ls *)
do
   [ filexecutable=`file ${file} | grep -v script | grep -q executable; echo $?` -eq 0 ] && \
      /usr/bin/strip ${file}
done

# Link files in /usr/bin
(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{prefix}/apache2/bin/* .
 cd -
)

# Link files in /usr/include

[ ! -d $RPM_BUILD_ROOT/usr/include/apache2/include ] && mkdir -p $RPM_BUILD_ROOT/usr/include/apache2/include
cd $RPM_BUILD_ROOT/usr/include/apache2/include
for file in $(find $RPM_BUILD_ROOT%{prefix}/apache2/include)
do
  ln -sf ../../../..%{prefix}/apache2/include/`basename ${file}` .
done

# conflict when installing  apr module
[ -e $RPM_BUILD_ROOT/usr/bin/apr-1-config ] \
	&& rm -f $RPM_BUILD_ROOT/usr/bin/apr-1-config
[ -e $RPM_BUILD_ROOT/usr/bin/apu-1-config ] \
	&& rm -f $RPM_BUILD_ROOT/usr/bin/apu-1-config

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ $1 = 0 ]; then
   %{prefix}/apache2/bin/apachectl stop > /dev/null 2>&1
fi
exit 0  # force exit; apache may not have been running
  
%files
%defattr(-,root,system)
%doc LICENSE ABOUT_APACHE README NOTICE VERSIONING
%config %{prefix}/apache2/conf/httpd.conf
%config %{prefix}/apache2/conf/magic
%config %{prefix}/apache2/conf/mime.types
%dir %{prefix}/apache2
%dir %{prefix}/apache2/conf
%{prefix}/apache2/conf/extra
%{prefix}/apache2/conf/original
%dir %{prefix}/apache2/logs
%dir %{prefix}/apache2/cgi-bin
%{prefix}/apache2/cgi-bin/*
%dir %{prefix}/apache2/error
%{prefix}/apache2/error/*
%dir %{prefix}/apache2/icons
%{prefix}/apache2/icons/*
%dir %{prefix}/apache2/htdocs
%{prefix}/apache2/htdocs/*
%dir %{prefix}/apache2/man
%dir %{prefix}/apache2/man/man1
%{prefix}/apache2/man/man1/*
%dir %{prefix}/apache2/man/man8
%{prefix}/apache2/man/man8/*
%dir %{prefix}/apache2/modules
%{prefix}/apache2/modules/*
#%dir %{prefix}/apache2/lib
#%{prefix}/apache2/lib/*
%dir %{prefix}/apache2/bin
%{prefix}/apache2/bin/*
/usr/bin/*

%files manual
%defattr(-,root,system)
%doc LICENSE
%dir %{prefix}/apache2/manual
%{prefix}/apache2/manual/*

%files devel
%defattr(-,root,system)
%doc LICENSE
%dir %{prefix}/apache2/build
%{prefix}/apache2/build/*
%dir %{prefix}/apache2/include
%{prefix}/apache2/include/*
%dir /usr/include/apache2
%dir /usr/include/apache2/include
/usr/include/apache2/include/*

%changelog
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

* Thu Feb  9 2006 Reza Arbab <arbab@austin.ibm.com> 1.3.31-2
- Rebuild ssl version to use OpenSSL 0.9.7g.

* Thu Jul 22 2004 David Clissold <cliss@austin.ibm.com> 1.3.31-1
- Rebuild ssl version to use OpenSSL 0.9.7d.

* Thu Jul 22 2004 David Clissold <cliss@austin.ibm.com>
- Update to 1.3.31, (and mod_ssl 2.8.19).

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
