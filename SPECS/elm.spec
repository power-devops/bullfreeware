%define	_datadir	%{_prefix}/lib

Summary: The elm mail user agent.
Name: elm
Version: 2.5.6
Release: 2
License: IBM_ILA
Group: Applications/Internet
URL: http://www.myxa.com/elm.html
Source0: ftp://ftp.virginia.edu/pub/elm/elm%{version}.tar.gz
Source1: elm.desktop
Source2: IBM_ILA
Patch0: elm%{version}-preconf.patch
# XXX for mmencode
Requires: metamail
BuildRoot: %{_tmppath}/%{name}-root

%define DEFCC cc

%description
Elm is a popular terminal mode email user agent. Elm includes all
standard mailhandling features, including MIME support via metamail.

Elm is still used by some people, but is no longer in development. If
you've used Elm before and you're devoted to it, you should install the
elm package.  If you would like to use metamail's MIME support, you'll
also need to install the metamail package.

%prep
%setup -q -n elm%{version}

%patch0 -p1 -b .pre

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat NOTICE >> LICENSE

%build
mkdir -p bin

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

make OPTIMIZE="$RPM_OPT_FLAGS"
strip bin/* || :

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/elm
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1

make	DESTBIN=${RPM_BUILD_ROOT}%{_bindir} \
	BIN=${RPM_BUILD_ROOT}%{_bindir} \
	DESTLIB=${RPM_BUILD_ROOT}%{_datadir}/elm \
	LIB=${RPM_BUILD_ROOT}%{_datadir}/elm \
	MAN=${RPM_BUILD_ROOT}%{_mandir}/man1 \
	install



mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Internet
install -m 644 %SOURCE1 $RPM_BUILD_ROOT/etc/X11/applnk/Internet/

# Let metamail provide mmencode
rm -f $RPM_BUILD_ROOT%{_bindir}/mmencode

(cd $RPM_BUILD_ROOT
 for dir in bin lib
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config(missingok) /etc/X11/applnk/Internet/elm.desktop
%attr(-,-,-) %{_bindir}/elm
%doc LICENSE
%{_bindir}/answer
%{_bindir}/checkalias
%{_bindir}/elmalias
%{_bindir}/fastmail
%{_bindir}/frm
%{_bindir}/listalias
%{_bindir}/messages
#%{_bindir}/mmencode
%{_bindir}/newalias
%{_bindir}/newmail
%{_bindir}/nfrm
%{_bindir}/printmail
%{_bindir}/prlong
%{_bindir}/readmsg
%{_bindir}/wnewmail
%{_datadir}/elm
/usr/bin/*
/usr/lib/*
%{_mandir}/man1/answer.*
%{_mandir}/man1/checkalias.*
%{_mandir}/man1/elm.*
%{_mandir}/man1/elmalias.*
%{_mandir}/man1/fastmail.*
%{_mandir}/man1/frm.*
%{_mandir}/man1/listalias.*
%{_mandir}/man1/messages.*
#%{_mandir}/man1/mmencode.*
%{_mandir}/man1/newalias.*
%{_mandir}/man1/newmail.*
%{_mandir}/man1/printmail.*
%{_mandir}/man1/readmsg.*
%{_mandir}/man1/wnewmail.*


%changelog
* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Thu Oct 04 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 2.5.6

* Wed May 30 2001 Marc Stephenson <marc@austin.ibm.com>
- Remnove mmencode

* Tue May 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Adapt for AIX Toolbox

* Fri Jan 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add Swedish translation to .desktop file (#15318)
- don't generate the .desktop file in the spec file

* Mon Oct 23 2000 Jeff Johnson <jbj@redhat.com>
- don't check errno if fcntl returns 0 (#17783).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com.
- FHS packaging.

* Wed Mar 29 2000 Jeff Johnson <jbj@redhat.com>
- fix long vs. int problem in elmalias (#10042).

* Tue Feb 29 2000 Jeff Johnson <jbj@redhat.com>
- create mbox tempfile as $home/.elm/.mbox. rather than /tmp/mbox.

* Thu Feb 10 2000 Jeff Johnson <jbj@redhat.com>
- remove mmencode man page, the metamail page is preferred.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig --> desktop

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make build use $RPM_OPT_FLAGS
- Fix bug #9048 ('answer -u' segfault)

* Thu Jan 20 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.5.3.

* Tue Jan  4 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.5.2.
- y2k fix (#8099)

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.5.1.

* Thu Jun 24 1999 Jeff Johnson <jbj@redhat.com>
- vet files list (#3707)

* Fri Jun 18 1999 Jeff Johnson <jbj@redhat.com>
- fix to be 8bit cleaner from H.J. Lu.

* Sat Jun  5 1999 Jeff Prosa <jprosa@limowreck.com>
- fix stand-alone readmsg seg fault (#3189)

* Fri Jun  4 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 2.5.0.

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- enable metamail support (#823)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.5.0pre8.

* Tue Jan 19 1999 Alex deVries <puffin@redhat.com>
- fixed it to build for all architectures

* Thu Jan 14 1999 Bill Nottingham <notting@redhat.com>
- build for arm

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue Jun 16 1998 Alan Cox <alan@redhat.com>
- Make elm non setgid and use fcntl locking (this is fine
  with procmail and matches our PINE setup).

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Jan 07 1998 Erik Troan <ewt@redhat.com>
- removed filter -- it's a security problem

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- added wmconfig entries.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
