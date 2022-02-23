Summary: An enhanced version of csh, the C shell.
Name: 	 tcsh
Version: 6.14
Release: 1
License: IBM_ILA
Group: 	 System Environment/Shells
URL: 	 http://www.tcsh.org
Source:  ftp://ftp.astron.com/pub/tcsh/old/tcsh-%{version}.00.tar.gz
Source1: tcsh.txt
Patch0:  tcsh-%{version}.00-config_nls.patch
Patch1:  tcsh-%{version}.00-closem.patch
Patch2:  tcsh-%{version}.00-lsF.patch
Patch3:  tcsh-%{version}.00-dashn.patch
Patch4:  tcsh-%{version}.00-read.patch
Patch5:  tcsh-%{version}.00-sigint.patch
Patch6:  tcsh-%{version}.00-wide-crash.patch
Patch7:  tcsh-%{version}.00-spell-crash.patch
Patch8:  tcsh-%{version}-aix_signal.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: coreutils grep

%description
Tcsh is an enhanced but completely compatible version of csh, the C shell.
Tcsh is a command language interpreter which can be used both as an interactive
login shell and as a shell script command processor.  Tcsh includes a command
line editor, programmable word completion, spelling correction, a history
mechanism, job control and a C language like syntax.
 
%prep
%setup -q -n %{name}-%{version}.00
%patch0 -p1 -b .confignls
%patch1 -p1 -b .closem
%patch2 -p1 -b .lsf
%patch3 -p1 -b .dashn
%patch4 -p1 -b .read
%patch5 -p1 -b .sigint
%patch6 -p1 -b .widecrash
%patch7 -p1 -b .spellcrash
%patch8 -p1 -b .aixsignal

# Add license info
cat $RPM_SOURCE_DIR/tcsh.txt >> LICENSE

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

#export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
#export CFLAGS="$RPM_OPT_FLAGS -D_AIX"
#CFLAGS="$RPM_OPT_FLAGS" \
CFLAGS="-I/opt/freeware/include/ -D_AIX"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure --prefix=%{_prefix}

make all # catalogs
perl tcsh.man2html
make -C nls catalogs
nroff -me eight-bit.me > eight-bit.txt

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/man/man1 $RPM_BUILD_ROOT%{_prefix}/bin
install -m 755 -s tcsh $RPM_BUILD_ROOT%{_prefix}/bin/tcsh
install -m 644 tcsh.man $RPM_BUILD_ROOT%{_prefix}/man/man1/tcsh.1
ln -sf tcsh $RPM_BUILD_ROOT%{_prefix}/bin/csh

while read lang language ; do
        dest=${RPM_BUILD_ROOT}%{_datadir}/locale/$lang/LC_MESSAGES
        if test -f tcsh.$language.cat ; then
                mkdir -p $dest
                install -m644 tcsh.$language.cat $dest/tcsh
                echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
        fi
done > tcsh.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 mkdir -p usr/linux/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/tcsh .
 cd ../linux/bin
 ln -sf ../../..%{_prefix}/bin/tcsh csh
 cd -
)


%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc FAQ Fixes NewThings complete.tcsh eight-bit.txt README
%doc LICENSE
%{_prefix}/bin/tcsh
%{_prefix}/bin/csh
/usr/bin/tcsh
/usr/linux/bin/csh
%{_prefix}/man/man1/tcsh.*
%{_datadir}/locale/*/LC_MESSAGES/*

%changelog
* Fri Dec 03 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 6.14-1
- Update to version 6.14

* Wed Feb 02 2005 David Clissold <cliss@austin.ibm.com> 6.11-3
- Rebuilt to specify coreutils as a req (not fileutils).

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Oct 09 2001 Marc Stephenson <marc@austin.ibm.com>
- New version

* Tue Aug 14 2001 David Clissold <cliss@austin.ibm.com>
- Update to level 6.10

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- append entries to spanking new /etc/shells.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- update to 6.09.
- fix strcoll oddness (#6000, #6244, #6398).

* Sat Sep 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix $shell by using --bindir

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Cristian Gafton <gafton@redhat.com>
- patch for using PATH_MAX instead of some silly internal #defines for
  variables that handle filenames.

* Fri Nov  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.08.00.

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 6.07.09 from the freebsd
- security fix
* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>

- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
 - Provides csh, adds and removes /bin/csh from /etc/shells if csh package
isn't installed.
