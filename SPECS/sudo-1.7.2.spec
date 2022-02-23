Summary: Allows restricted root access for specified users.
Name: sudo
Version: 1.7.2p6
Release: 1
Group: Applications/System
License: BSD
Source: http://www.courtesan.com/sudo/dist/sudo-%{version}.tar.gz
URL: http://www.courtesan.com/sudo
BuildRoot: /var/tmp/%{name}-%{version}-root
Prefix:	%{_prefix}
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

%prep
%setup -q -n sudo-%{version}

%build
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
	--with-tty-tickets
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

sed -e 's/-o $(sudoers_uid) -g $(sudoers_gid) / /g' \
    -e 's/-o $(install_uid) -g $(install_gid) / /g' \
    -e 's/-m 4111//' -e 's/-m 0111//' Makefile > Makefile.$$

mv Makefile.$$ Makefile

CFLAGS="$RPM_OPT_FLAGS" \
make \
	prefix="$RPM_BUILD_ROOT%{prefix}" \
	sbindir="$RPM_BUILD_ROOT%{prefix}/sbin" \
	sysconfdir="$RPM_BUILD_ROOT/etc" \
	mandir="$RPM_BUILD_ROOT%{_mandir}" \
	install
install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo

(cd $RPM_BUILD_ROOT
 for dir in bin sbin 
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
%defattr(-,root,root)
%doc HISTORY LICENSE README TROUBLESHOOTING UPGRADE *.pod
%config(noreplace) %attr(0440,root,root) /etc/sudoers
%attr(0700,root,root) %dir /var/run/sudo
%attr(4111,root,root) %{prefix}/bin/sudo
%attr(0111,root,root) %{prefix}/sbin/visudo
%{_libexecdir}/sudo_noexec.*
/usr/bin/sudo
/usr/sbin/visudo
%{_mandir}/man5/sudoers.5*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/visudo.8*

%changelog
* Wed May 19 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.7.2p6
- Update to version 1.7.2p6

* Tue Apr 14 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.7.0
- Update to version 1.7.0

* Thu Jul 07 2005 Philip K. Warren <pkw@us.ibm.com> 1.6.7p5-3
- Add patch for CAN-2004-1051 vulnerability.
- Add patch for CAN-2005-1993 vulnerability.

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
