Summary: A screen manager that supports multiple logins on one terminal.
Name: screen
Version: 3.9.10
Release: 3
License: GPL
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/screen//screen-%{version}.tar.gz
URL: http://www.gnu.org/software/screen

Patch0: %{name}-3.9.10.loadaverage-kernelinfo.patch

Prefix: %{_prefix}
Prereq: /sbin/install-info
BuildRoot: /var/tmp/%{name}-root
%define DEFCC cc

%description
The screen utility allows you to have multiple logins on just one
terminal.  Screen is useful for users who telnet into a machine or are
connected via a dumb terminal, but want to use more than just one
login.

Install the screen package if you need a screen manager that can
support multiple logins on one terminal.


%prep
%setup -q

%patch0 -p1 -b .loadaverage-kernelinfo


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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

%configure


perl -pi -e 's|.*#.*PTYMODE.*|#define PTYMODE 0620|' config.h
perl -pi -e 's|.*#.*PTYGROUP.*|#define PTYGROUP 5|' config.h

perl -pi -e 's|.*#undef BUILTIN_TELNET.*|#define BUILTIN_TELNET 1|' config.h

perl -pi -e 's|%{_prefix}/etc/screenrc|/etc/screenrc|' config.h
perl -pi -e 's|/usr/local/etc/screenrc|/etc/screenrc|' etc/etcscreenrc doc/*
perl -pi -e 's|/local/etc/screenrc|/etc/screenrc|' doc/*
rm doc/screen.info*

gmake CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/skel

%makeinstall

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_infodir}/screen.info*
  strip .%{_bindir}/screen || :

  rm -f .%{_bindir}/screen.old     .%{_bindir}/screen
  mv .%{_bindir}/screen-%{version} .%{_bindir}/screen
)

install -c -m 0444 etc/etcscreenrc $RPM_BUILD_ROOT/etc/screenrc
install -c -m 0644 etc/screenrc    $RPM_BUILD_ROOT/etc/skel/.screenrc


(cd $RPM_BUILD_ROOT
 for dir in bin
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done
)


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."

if [ -d /tmp/screens ]; then
    # we're not setuid root anymore
    chmod 777 /tmp/screens
fi


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/screen.info.gz %{_infodir}/dir --entry="* screen: (screen).             Terminal multiplexer."
fi


%files
%defattr(-,root,root)
%doc COPYING NEWS README FAQ doc/README.DOTSCREEN

%attr(755,root,root) %{_bindir}/screen
%{_mandir}/man1/screen.*
%{_infodir}/screen.info*
/usr/bin/screen

%config /etc/screenrc
%config /etc/skel/.screenrc


%changelog
* Tue Sep 20 2016 Tony Reix <tony.reix@atos.net> - 3.9.10-3
- Fix issue dealing with /dev/kmem opened and stay opened

* Mon Jun 02 2003 David Clissold <cliss@austin.ibm.com>
- Stop turning on the HAVE_BRAILLE define because of CERT security
- vulnerability #524227.  Not really exposed because our image is
- not installed setuid or setgid, but will turn it off anyway to be prudent.

* Tue Oct 02 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 3.9.10

* Wed Aug 29 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 3.9.9

* Thu Jul 05 2001 Marc Stephenson <marc@austin.ibm.com>
- First version for AIX toolbox

* Tue Feb 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix configure.in to use correct code to check for select()

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Rebuild, which will hopefully fix bug #22537

* Sun Oct 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.9.8
- change the .jbj patch and add some more "user" -> "auser" cases

* Thu Aug 15 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Patched the documentation to change the 'C-a C-\' to 'C-a \',
- which is what is the real behaviour. this fixes bug #16103

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed my fix, so that the hack goes in the /global/ file :)

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Stuck an entry into the default screenrc file that forces
- '^?' (backspace) to send '^H'.
- Its an ugly fix for a termcap inheritance problem,
- but it works, if anyone REALLY needs '^?' they can change it,
- and I think we anger less people with this than the way it 
- currently behaves. (Read: vi and emacs work now)
- POST NOTE (Aug 15): emacs is NOT happy with ^H, BUT screen thinks
- that this is what backspace is supposed to do, so we don't change it.

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- Fixed some conflicting descriptions in the documentation

* Thu Aug  3 2000 Crutcher Dunnavant <crutcher@redhat.com>
- got a patch from rzm@icm.edu.pl to fix bug #10353
- which caused screen to crash when copying to a file buffer

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS tweaks

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- fix build for ia64

* Mon Apr  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- rebuild with new ncurses

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Feb 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix MD5 password support (Bug #9463)

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Dec 10 1999 Bill Nottingham <notting@redhat.com>
- update to 3.9.5

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- you know, we weren't just patching in Unix98 pty support for fun.

* Wed Aug 18 1999 Bill Nottingham <notting@redhat.com>
- put screendir in ~

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.9.4.

* Wed Jun 16 1999 Bill Nottingham <notting@redhat.com>
- force tty permissions/group

* Wed Jun 5 1999 Dale Lovelace <dale@redhat.com>
- permissions on /etc/skel/.screenrc to 644

* Mon Apr 26 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory permissions so root can still use screen

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- take out warning of directory ownership so root can still use screen

* Wed Apr 07 1999 Erik Troan <ewt@redhat.com>
- patched in utempter support, turned off setuid bit

* Fri Mar 26 1999 Erik Troan <ewt@redhat.com>
- fixed unix98 pty support

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- add patch for Unix98 pty support

* Mon Dec 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.7.6.

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.7.4

* Wed Oct 08 1997 Erik Troan <ewt@redhat.com>
- removed glibc 1.99 specific patch

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- added install-info support

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
