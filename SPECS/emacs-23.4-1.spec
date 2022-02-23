Summary: The libraries needed to run the GNU Emacs text editor.
Name: emacs
%define	version	23.4
Version: %{version}
Release: 1
License: GPL
Group: Applications/Editors
Source0: ftp://ftp.gnu.org/pub/gnu/emacs-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/pub/gnu/leim-21.3.tar.gz
URL: http://www.gnu.org/software/emacs
Buildroot: /var/tmp/%{name}-root
Prereq: /sbin/install-info
Prefix: %{_prefix}
%define DEFCC cc

%description
Emacs is a powerful, customizable, self-documenting, modeless text editor.
Emacs contains special code editing features, a scripting language (elisp), and
the capability to read mail, news and more without leaving the editor.

This package includes the libraries you need to run the Emacs editor, so you
need to install this package if you intend to use Emacs.  You also need to
install the actual Emacs program package (emacs-nox or emacs-X11).  Install
emacs-nox if you are not going to use the X Window System; install emacs-X11 if
you will be using X.

%package el
Summary: The sources for elisp programs included with Emacs.
Group: Applications/Editors
Requires: emacs

%description el
Emacs-el contains the emacs-elisp sources for many of the elisp programs
included with the main Emacs text editor package.

You need to install emacs-el only if you intend to modify any of the Emacs
packages or see some elisp examples.

%package leim
Summary: Emacs Lisp code for input methods for international characters.
Group: Applications/Editors
Requires: emacs

%description leim
The emacs-leim package contains Emacs Lisp code for input methods for various
international character scripts.  Basically, the Lisp code provided by this
package describes the consecutive keystrokes that a user must press in order to
input a particular character in a non-English character set.  Input methods for
many different language's character sets are included in this package.

%package nox
Summary: The Emacs text editor without support for the X Window System.
Group: Applications/Editors
Requires: emacs

%description nox
Emacs-nox is the Emacs text editor program without support for the X Window
System.

You need to install this package only if you plan on exclusively using Emacs
without the X Window System (emacs-X11 will work both in X and out of X, but
emacs-nox will only work outside of X).  You'll also need to install the emacs
package in order to run Emacs.

%package X11
Summary: The Emacs text editor for the X Window System.
Group: Applications/Editors
Requires: emacs

%description X11
Emacs-X11 includes the Emacs text editor program for use with the X Window
System (it provides support for the mouse and other GUI elements).  Emacs-X11
will also run Emacs outside of X, but it has a larger memory footprint than the
'non-X' Emacs package (emacs-nox).

Install emacs-X11 if you're going to use Emacs with the X Window System.  You
should also install emacs-X11 if you're going to run Emacs both with and
without X (it will work fine both ways). You'll also need to install the emacs
package in order to run Emacs.

%prep
%setup -q -b 1

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

export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xLC_r"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

export CFLAGS=$RPM_OPT_FLAGS
PUREDEF="-DNCURSES_OSPEED_T"
XPUREDEF="-DNCURSES_OSPEED_T"
libtoolize --force --copy
CONFOPTS="--prefix=%{_prefix} --info=%{_infodir} --libexecdir=%{_prefix}/lib --sharedstatedir=/var  --with-pop"

#Build binary with X support
[ -d build-withx ] && rm -rf build-withx
mkdir build-withx && cd build-withx
CPPFLAGS=" -I/opt/freeware/include -I/usr/include" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib -s" \
CFLAGS="$RPM_OPT_FLAGS -I/opt/freeware/include -I/usr/include" \
  ../configure ${CONFOPTS} --with-x-toolkit=lucid
make
cd ..

%define recompile build-withx/src/emacs -batch --no-init-file --no-site-file -f batch-byte-compile

#Build binary without X support
[ -d build-nox ] && rm -rf build-nox
mkdir build-nox && cd build-nox
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s \
  ../configure ${CONFOPTS} --with-x=no
make
cd ..

# recompile patched .el files
#%{recompile} lisp/mail/mh-utils.el

%install
export RM="/usr/bin/rm -f"
### VSD rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}

make install -C build-withx \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
	libexecdir=$RPM_BUILD_ROOT%{_prefix}/lib \
	sharedstatedir=$RPM_BUILD_ROOT/var

rm -f $RPM_BUILD_ROOT%{_prefix}/info/dir
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/info/*

install -m755 build-nox/src/emacs $RPM_BUILD_ROOT%{_prefix}/bin/emacs-nox

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/emacs/site-lisp

mv $RPM_BUILD_ROOT%{_prefix}/man/man1/ctags.1 $RPM_BUILD_ROOT%{_prefix}/man/man1/gctags.1
mv $RPM_BUILD_ROOT%{_prefix}/bin/ctags $RPM_BUILD_ROOT%{_prefix}/bin/gctags

install -m644 build-nox/etc/DOC-* $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{version}/etc

#
# create file lists
#
find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/lisp \
  -name '*.elc' -print | sed "s^$RPM_BUILD_ROOT^^" > core-filelist
find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/lisp \
  -type d -printf "%%%%dir %%p\n" | sed "s^$RPM_BUILD_ROOT^^" >> core-filelist
find $RPM_BUILD_ROOT%{_prefix}/lib/emacs/%{PACKAGE_VERSION} -type f | \
  sed "s^$RPM_BUILD_ROOT^^" | grep -v movemail >> core-filelist

# Include .el files which lack a corresponding byte compiled form
for I in `find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/lisp \
          -name '*.el'`; do
  if [ ! -e `dirname $I`/`basename $I .el`.elc ]; then
    echo $I | sed "s^$RPM_BUILD_ROOT^^"
  fi
done >> core-filelist

# Include all non elisp files which emacs installs
find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/lisp -type f | \
  sed "s^$RPM_BUILD_ROOT^^" | grep -v "\.el\(c\)\?$" >> core-filelist


find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/leim \
  -name '*.elc' -print | sed "s^$RPM_BUILD_ROOT^^" > leim-filelist
find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/leim \
  -mindepth 1 -type d -printf "%%%%dir %%p\n" | \
  sed "s^$RPM_BUILD_ROOT^^" >> leim-filelist

#
# be sure to exclude some files which are needed in the core package
#
> el-filelist
for I in `find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/lisp \
          -name '*.el'`; do
  if [ -e `dirname $I`/`basename $I .el`.elc ]; then
    echo $I | sed "s^$RPM_BUILD_ROOT^^"
  fi
done >> el-filelist

# grep -v doesn't work properly
find $RPM_BUILD_ROOT%{_prefix}/share/emacs/%{PACKAGE_VERSION}/leim \
  -name "*.el" -print  | sed "s^$RPM_BUILD_ROOT^^"  >>  el-filelist
##  grep -v "leim\/leim\-list.el" >> el-filelist 


vi el-filelist <<!
:g;leim/leim-list;d
:wq
!

# VSD ... le grep ne passe pas.  le char "-" fait planter le grep ???

( cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{prefix}/bin/* .
 cd -

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)


%clean
rm -rf $RPM_BUILD_ROOT
rm -rf build-nox
rm -rf build-withx

%define info_files ccmode cl dired-x ediff emacs forms gnus info message mh-e reftex sc vip viper widget
%post
for f in %{info_files}; do
  /sbin/install-info %{_prefix}/info/$f.gz %{_prefix}/info/dir --section="GNU Emacs"
done

%preun
if [ "$1" = 0 ]; then
for f in %{info_files}; do
  /sbin/install-info --delete %{_prefix}/info/$f.gz %{_prefix}/info/dir \
    --section="GNU Emacs"
done
fi

%triggerin nox -- emacs-X11
if [ -L %{_prefix}/bin/emacs ]; then
  rm %{_prefix}/bin/emacs
fi

%triggerpostun nox -- emacs-X11
[ $2 = 0 ] || exit 0
if [ ! -L %{_prefix}/bin/emacs ]; then
  ln -sf emacs-nox %{_prefix}/bin/emacs
fi

%post nox
if [ ! -x %{_prefix}/bin/emacs -a ! -L %{_prefix}/bin/emacs ]; then
  ln -sf emacs-nox %{_prefix}/bin/emacs
fi

%postun nox
[ $1 = 0 ] || exit 0
if [ -L %{_prefix}/bin/emacs ]; then
  rm %{_prefix}/bin/emacs
fi


%files -f core-filelist
%defattr(-,root,system)
%doc etc/AUTHORS BUGS README
%{_prefix}/bin/b2m
%{_prefix}/bin/emacsclient
%{_prefix}/bin/etags
%{_prefix}/bin/gctags
%{_prefix}/bin/rcs-checkin
/usr/bin/b2m
/usr/bin/emacsclient
/usr/bin/etags
/usr/bin/gctags
/usr/bin/rcs-checkin
%{_prefix}/man/*/*
%{_prefix}/info/*

%dir %{_prefix}/lib/emacs
%dir %{_prefix}/lib/emacs/site-lisp
%dir %{_prefix}/lib/emacs/%{PACKAGE_VERSION}
%dir %{_prefix}/lib/emacs/%{PACKAGE_VERSION}/*
/usr/lib/emacs
%attr(2755,root,mail) %{_prefix}/lib/emacs/%{PACKAGE_VERSION}/*/movemail

%{_prefix}/share/emacs/site-lisp
%dir %{_prefix}/share/emacs/%{PACKAGE_VERSION}
%dir %{_prefix}/share/emacs/%{PACKAGE_VERSION}/site-lisp
%dir %{_prefix}/share/emacs/%{PACKAGE_VERSION}/leim
%{_prefix}/share/emacs/%{PACKAGE_VERSION}/etc

%files -f el-filelist el
%defattr(-,root,system)

%files -f leim-filelist leim
%defattr(-,root,system)
%{_prefix}/share/emacs/%{PACKAGE_VERSION}/leim/leim-list.el

%files nox
%defattr(-,root,system)
%{_prefix}/bin/emacs-nox
/usr/bin/emacs-nox

%files X11
%defattr(-,root,system)
%attr(755,root,root) %{_prefix}/bin/emacs
%attr(755,root,root) %{_prefix}/bin/emacs-%{version}
/usr/bin/emacs
/usr/bin/emacs-%{version}

%changelog
* Tue Feb 22 2005 David Clissold <cliss@austin.ibm.com> 21.3-1
- Update to version 21.3
- Add movemail security patch, CAN-2005-0100

* Tue Apr 23 2002 David Clissold <cliss@austin.ibm.com>
- No functional change.  Remove unnecessary political statement
- from the original gzipped tarball, per request.

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Mon Feb 21 2000 Preston Brown <pbrown@redhat.com>
- add .emacs make the delete key work to delete forward character for X ver.

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #2988
- recompile patched .el files (suggested by Pavel.Janik@linux.cz)
- prereq /sbin/install-info

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig gone

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions and summary
- fix permissions for emacs niaries (what the hell does 1755 means for a
  binary?)
- added missing, as per emacs Changelog, NCURSES_OSPEED_T compilation
  flag; without it emacs on Linux is making global 'ospeed' short which
  is not the same as 'speed_t' expected by libraries. (reported by Michal
  Jaegermann <michal@harddata.com>)

* Mon Jan 10 2000 David S. Miller <davem@redhat.com>
- Revert src/unexecelf.c to 20.4 version, fixes SPARC problems.

* Sun Jan  9 2000 Matt Wilson <msw@redhat.com>
- strip emacs binary
- disable optimizations for now, they cause illegal instructions on SPARC.

* Sun Jan 09 2000 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.5a
- remove python-mode, wheelmouse support, and auctex menu
- import emacs.desktop with icon from GNOME

* Wed Dec 08 1999 Ngo Than <than@redhat.de>
- added python-mode, wheelmouse support and auctex menu
- added Comment[de] in emacs.desktop

* Sat Sep 25 1999 Preston Brown <pbrown@redhat.com>
- added desktop entry

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- tried to fix triggers, hopefully working now.

* Wed Sep 01 1999 Preston Brown <pbrown@redhat.com>
- added trigger for making symlink to /usr/bin/emacs in emacs-nox package

* Thu Jul 22 1999 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.4
- cleaned up spec

* Fri Apr 16 1999 Owen Taylor <otaylor@redhat.com>
- replace bad xemacs compiled .elc file for mh-e with one compiled
  on emacs

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- make sure movemail doesn't get %defattr()'d to root.root

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- patch to make it work with dxpc

* Wed Mar 31 1999 Preston Brown <pbrown@redhat.com>
- updated mh-utils emacs lisp file to match our nmh path locations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 9)

* Fri Feb 26 1999 Cristian Gafton <gafton@redhat.com>
- linker scripts hack to make it build on the alpha

* Fri Jan  1 1999 Jeff Johnson <jbj@redhat.com>
- add leim package (thanks to Pavel.Janik@inet.cz).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- backed up changes to uncompress.el (it seems that the one from 20.2 works
  much better)

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- eliminate /tmp race in rcs2log

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to 20.3

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add --with-pop to X11 compile.
- include contents of /usr/share/.../etc with main package.

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- fix signals when linked with glibc on non-Intel architectures
  NOTE: This patch is not needed with emacs >20.2

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/lib/emacs/20.2/*-redhat-linux directory in the filelist

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- alpha started to like emacs-nox again :-)

* Thu Nov  6 1997 Michael Fulbright <msf@redhat.com>
- alpha just doesnt like emacs-nox, taking it out for now

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- added multibyte support back into emacs 20.2
- added wmconfig for X11 emacs
- fixed some errant buildroot references

* Thu Oct 23 1997 Michael Fulbright <msf@redhat.com>
- joy a new version of emacs! Of note - no lockdir any more.
- use post/preun sections to handle numerous GNU info files

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- stopped stripping it as it seems to break things

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- turned off ecoff support on the Alpha (which doesn't build anymore)

* Mon Jun 16 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved ctags to gctags to fit in the more powerful for C (but less
  general) exuberant ctags as the binary /usr/bin/ctags and the
  man page /usr/man/man1/ctags.1
