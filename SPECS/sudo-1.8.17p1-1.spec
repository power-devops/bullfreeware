# LDAP is enabled by default.  Disable with --define 'noldap 1'.
# enable LDAP by default.
#%define noldap 0
#%{!?noldap:%define LDAP 1}
#%{?noldap:%define LDAP 0}
%define LDAP 1

Summary: Allows restricted root access for specified users.
Summary(ja): »ØÄê¥æ¡¼¥¶¤ËÀ©¸ÂÉÕ¤Îroot¸¢¸Â¤òµö²Ä¤¹¤ë
Name: sudo
Version: 1.8.17p1
Release: 1
Group: Applications/System
License: IBM_ILA
Source: http://www.sudo.ws/sudo/dist/sudo-1.8.17p1.tar.gz
Source1: IBM_ILA
URL: http://www.sudo.ws
#Serial: 2008050201
BuildRoot: /var/tmp/%{name}-%{version}-root
Prefix:	%{_prefix}
%if %{LDAP} == 1
Requires: openldap >= 2.4.35
BuildRequires: openldap-devel >= 2.4.35
BuildRequires: sed
BuildRequires: coreutils
%endif
%define DEFCC cc

%description
Sudo (superuser do) allows a system administrator to give certain users (or
groups of users) the ability to run some (or all) commands as root while
logging all commands and arguments. Sudo operates on a per-command basis.  It
is not a replacement for the shell.  Features include: the ability to restrict
what commands a user may run on a per-host basis, copious logging of each
command (providing a clear audit trail of who did what), a configurable timeout
of the sudo command, and the ability to use the same configuration file
(sudoers) on many different machines.

%description -l ja
sudo (superuser do) ¤È¤Ï¥·¥¹¥Æ¥à´ÉÍý¼Ô¤¬¡¢¿®ÍÑ¤Ç¤­¤ë¥æ¡¼¥¶(¤Þ¤¿¤Ï¥°¥ë¡¼¥×)¤ËÂÐ
¤·¤Æ¡¢¤¤¤¯¤Ä¤«(¤â¤·¤¯¤ÏÁ´¤Æ)¤Î¥³¥Þ¥ó¥É¤ò root ¤È¤·¤Æ¼Â¹Ô¤Ç¤­¤ë¤è¤¦¡¢¤½¤Î¥³¥Þ¥ó
¥É¤Î¼Â¹ÔÍúÎò¤Î¥í¥°¤ò¤È¤ê¤Ä¤Äµö²Ä¤¹¤ë»ÅÁÈ¤ß¤Ç¤¹¡£sudo ¤Ï¥³¥Þ¥ó¥É°ì¹ÔÃ±°Ì¤ÇÆ°ºî
¤·¤Þ¤¹¡£¥·¥§¥ë¤ÎÃÖ¤­´¹¤¨¤Ç¤Ï¤¢¤ê¤Þ¤»¤ó¡£°Ê²¼¤Îµ¡Ç½¤òÆâÂ¢¤·¤Æ¤¤¤Þ¤¹¡£¥Û¥¹¥ÈÃ±°Ì
¤Ç¡¢¤½¤Î¥³¥Þ¥ó¥É¤ò¼Â¹Ô²ÄÇ½¤Ê¥æ¡¼¥¶¤òÀ©¸Â¤¹¤ëµ¡Ç½¡¢³Æ¥³¥Þ¥ó¥É¤Ë¤Ä¤¤¤Æ¤Î(Ã¯¤¬¤Ê
¤Ë¤ò¼Â¹Ô¤·¤¿¤«¤Îº¯À×¤ò»Ä¤¹¤¿¤á¤Î)Ë­ÉÙ¤Ê¥í¥®¥ó¥°µ¡Ç½¡¢sudo ¥³¥Þ¥ó¥É¤Î¥¿¥¤¥à¥¢¥¦
¥È»þ´Ö¤òÀßÄê²ÄÇ½¡¢Ê£¿ô¤Î¥Þ¥·¥ó¤ÇÆ±°ì¤ÎÀßÄê¥Õ¥¡¥¤¥ë(sudoers)¤ò¶¦Í­¤¹¤ëµ¡Ç½¡¢¤¬
tat¢¤ê¤Þ¤¹¡£

%prep
%setup -q -n sudo-%{version}

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > doc/LICENSE.new
cat doc/LICENSE >> doc/LICENSE.new
mv doc/LICENSE.new doc/LICENSE

%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
# Strangely, build does not work when $RM is set to /usr/bin/rm
# (which is set when using /usr/bin/rpm), but works fine when RM
# is not set and /usr/bin is first in the PATH
unset RM
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else 
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{prefix} \
	--sbindir=%{prefix}/sbin \
	--mandir=%{_mandir} \
	--with-logging=syslog \
	--with-logfac=auth \
	--without-pam \
	--with-env-editor \
	--with-ignore-dot \
	--with-authenticate \
	--with-tty-tickets \
%if %{LDAP} == 1
	--with-ldap=/opt/freeware \
	--with-ldap-conf-file=/opt/freeware/etc/openldap/ldap.conf \
	--with-ldap-secret-file=/opt/freeware/etc/openldap/slapd.conf
%endif

#They have put /opt/freeware/lib at the back of the libpath.  Bad.
#perl -pi -e 's|-Wl,-blibpath:/usr/lib:/lib:/opt/freeware/lib|-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib|g' Makefile
make

%install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
# Strangely, build does not work when $RM is set to /usr/bin/rm
# (which is set when using /usr/bin/rpm), but works fine when RM
# is not set and /usr/bin is first in the PATH
unset RM
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

sed -e 's/-o $(sudoers_uid) -g $(sudoers_gid) / /g' \
    -e 's/-o $(install_uid) -g $(install_gid) / /g' \
    -e 's/-m 4111//' -e 's/-m 0111//' Makefile > Makefile.$$

mv Makefile.$$ Makefile

#make \
#	prefix="$RPM_BUILD_ROOT%{prefix}" \
#	sbindir="$RPM_BUILD_ROOT%{prefix}/sbin" \
#	sysconfdir="$RPM_BUILD_ROOT/etc" \
#	mandir="$RPM_BUILD_ROOT%{_mandir}" \
#	install
make check

CFLAGS="$RPM_OPT_FLAGS" \
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/* 

#install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo
/opt/freeware/bin/install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo
(cd $RPM_BUILD_ROOT
 for dir in bin sbin include 
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc INSTALL NEWS doc/HISTORY doc/LICENSE README README.LDAP doc/TROUBLESHOOTING doc/UPGRADE
%config(noreplace) %attr(0440,root,root) /etc/sudoers
%attr(0750,root,system) %dir /etc/sudoers.d
%attr(0711,root,system) %dir /var/lib/sudo
%attr(0711,root,system) %dir /var/lib/sudo/lectured
%attr(0700,root,system) %dir /var/run/sudo
%attr(4111,root,system) %{prefix}/bin/sudo
%attr(4111,root,system) %{prefix}/bin/sudoreplay
%attr(4111,root,system) %{prefix}/bin/sudoedit
%attr(0111,root,system) %{prefix}/sbin/visudo
/usr/bin/sudo
/usr/bin/sudoreplay
/usr/bin/sudoedit
/usr/sbin/visudo
%{_libexecdir}/sudo
/etc/rc.d/init.d/*
/etc/rc.d/rc2.d/*
#%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man5/*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%{_includedir}/*
/usr/include/*

%changelog
* Mon Jul 11 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.8.17o1-1
- Update to 1.8.17p1

* Sat Jul 02 2016 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.15-2
- Rebuild with ldap support.

* Thu Mar 17 2016 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.15-1
- Update to 1.8.15

* Tue Apr 7 2015 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.13-1
- Update to 1.8.13

* Thu Nov 11 2011 Sangamesh Mallayya <smallayy@in.ibm.com> 1.6.9p23
- Update to 1.6.9p23

* Fri Aug 22 2008 Garrick Trowsdale <garrick.trowsdale@telus.com>
- Move BuildRequires: openldap-devel inside conditional block

* Tue Jul 29 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-2noldap
- Create a non-LDAP enabled release.  Build with --define 'noldap 1'.

* Wed Jul  2 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-2
- Change the order of the libpath encoded in the sudo binary.  

* Fri May  2 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-1
- Update to 1.6.9p15.
- Configure with-ldap and with-noexec.  Require openldap.

* Tue Apr 27 2004 David Clissold <cliss@austin.ibm.com> 1.6.7p5-2
- Make sure /etc/sudoers installs with 0440 permissions.
- Thanks to Leigh Brown (leigh@solinno.co.uk) for pointing this out.

* Wed May 21 2003 David Clissold <cliss@austin.ibm.com> 1.6.7p5-1
- New version, 1.6.7p5.  (Includes earlier security fix; separate
-  patch no longer required).

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Wed Jul 17 2002 David Clissold <cliss@austin.ibm.com>
- New version, 1.6.5p2.  Security patch still required.

* Thu Apr 25 2002 David Clissold <cliss@austin.ibm.com>
- Security patch announced today; added.

* Fri Feb 08 2002 Marc Stephenson <marc@austin.ibm.com>
- New version

* Tue Oct 23 2001 David Clissold <cliss@austin.ibm.com>
- No functional change.  Remove unneccessary libtool use.

* Thu Oct 11 2001 Marc Stephenson <marc@austin.ibm.com>
- Use configure with-authenticate

* Fri Apr 20 2001 Marc Stephenson <marc@austin.ibm.com>
- Build for AIX Toolbox for Linux Distributions

* Mon Mar 5 2001 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.3p7

* Thu Feb 22 2001 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.3p6

* Sat Dec 30 2000 Roger Luethi <rluethi@turbolinux.com>
- 1.6.3p5-2: libtoolized build

* Thu Sep 21 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>                  
- rewrite spec file for FHS 2.1                                              
- updated to 1.6.3p5
  o Fixed a case where a string was used after it had been freed.
  o Fixed a bug that prevented the -H option from working.
  o Fixed targetpw, rootpw, and runaspw options when used with non-passwd
    file authentication (PAM, etc).
  o When the targetpw flag is set, use the target username as part
    of the timestamp path.
  o The listpw and verifypw options had no effect.

* Mon Jul 17 2000 SL Baur  <steve@turbolinux.co.jp>
- alpha port

* Mon Mar 27 2000 Takeshi Aihana <aihana@turbolinux.co.jp>
- updated to 1.6.3
- patch pathname of libpam

* Sat Mar 25 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.2p3

* Fri Feb 4 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>
- Repackaged for TurboLinux Workstation 6.0J

* Sun Jan 9 2000 Takaaki Tabuchi <tab@kondara.org>
- be able to rebuild non-root user.

* Sun Dec 19 1999 Taichi Nakamura <pdf30044@biglobe.ne.jp>
- update to 1.6.1

* Tue Dec 14 1999 Tenkou N. Hattori <tnh@kondara.org>
- change /etc/sudoers to noreplace.

* Tue Nov 30 1999 Tenkou N. Hattori <tnh@kondara.org>
- updated to 1.6
- be a NoSrc :-P

* Thu Jul 22 1999 Tim Powers <timp@redhat.com>
- updated to 1.5.9p2 for Powertools 6.1

* Wed May 12 1999 Bill Nottingham <notting@redhat.com>
- sudo is configured with pam. There's no pam.d file. Oops.

* Mon Apr 26 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.59p1 for powertools 6.0

* Tue Oct 27 1998 Preston Brown <pbrown@redhat.com>
- fixed so it doesn't find /usr/bin/vi first, but instead /bin/vi (always installed)

* Fri Oct 08 1998 Michael Maher <mike@redhat.com>
- built package for 5.2 

* Mon May 18 1998 Michael Maher	<mike@redhat.com>
- updated SPEC file. 

* Thu Jan 29 1998 Otto Hammersmith <otto@redhat.com>
- updated to 1.5.4

* Tue Nov 18 1997 Otto Hammersmith <otto@redhat.com>
- built for glibc, no problems

* Fri Apr 25 1997 Michael Fulbright <msf@redhat.com>
- Fixed for 4.2 PowerTools 
- Still need to be pamified
- Still need to move stmp file to /var/log

* Mon Feb 17 1997 Michael Fulbright <msf@redhat.com>
- First version for PowerCD.
