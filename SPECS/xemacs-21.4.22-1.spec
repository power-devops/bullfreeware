# semi
%define semiver		1.13.7
Summary: An X Window System based version of GNU Emacs.
Name: xemacs
Version: 21.4.22
Release: 1
License: GPL
Group: Applications/Editors
Source0: ftp://ftp.xemacs.org/tux/xemacs/xemacs-21.4/xemacs-%{version}.tar.bz2
# The next three are bzipped, the original files are gzipped
Source4: ftp://ftp.xemacs.org/tux/xemacs/packages/xemacs-mule-sumo.tar.bz2
Source5: ftp://ftp.xemacs.org/tux/xemacs/packages/xemacs-sumo.tar.bz2
Source6: xemacs.desktop
Source9: xemacs-sitestart.el
#ispell 3.6
Source10: ispell.el
Source12: xemacs.png 
Source13: psgml-init.el.xemacs
Source14: rpm-spec-mode.el
Source17: mew-init.el
Source18: xemacs-%{version}-aix6-1.h
# Wanderlust  (http://www.gohome.org/wl/ )
Source100: ftp://ftp.gohome.org/wl/wl-2.4.0-xemacs.tar.gz
# semi
Source150: ftp://ftp.m17n.org/pub/mule/semi/semi-1.13-for-flim-1.13/semi-%{semiver}.tar.gz

Patch1: xemacs-21.4.22-aixconf.patch
Patch2: xemacs-21.4.22-png.patch

Prefix: %{_prefix}
Url: http://www.xemacs.org/
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: perl 
PreReq: info
Obsoletes: xemacs-extras xemacs-packages-el xemacs-packages xemacs-noX xemacs-X11 xemacs-mule xemacs-static
Obsoletes: semi-xemacs tm apel flim
Provides: apel-xemacs, flim-xemacs, semi-xemacs = %{semiver}, emh-xemacs , rmail-mime-xemacs

%description
XEmacs (and regular GNU Emacs, too) is a self-documenting,
customizable, extensible, real-time display editor.  XEmacs is
self-documenting because at any time you can type in control-h to find
out what your options are or to find out what a command does.  XEmacs
is customizable because you can change the definitions of XEmacs
commands to anything you want.  XEmacs is extensible because you can
write entirely new commands-programs in the Lisp language to be run
by Emacs' own Lisp interpreter.  XEmacs includes a real-time display,
which means that the text being edited is visible on the screen and is
updated very frequently (usually after every character or pair of
characters) as you type.

This XEmacs distribution consists of three rpms: xemacs (the main
portion, including the standard XEmacs binary which most people use),
xemacs-el (elisp sources, which you only need if you're going to
program with Lisp in XEmacs) and xemacs-info (optional information
about XEmacs)/

%package el
Summary: The .el source files for XEmacs.
Group: Applications/Editors
Requires: xemacs = %{version}
%description el
Xemacs-el is not necessary to run XEmacs.  You'll only need to install
it if you're planning on incorporating some Lisp programming into your
XEmacs experience.

%package info
Summary: Information files for XEmacs.
Group: Applications/Editors
Requires: xemacs = %{version}
Prereq: /sbin/install-info
%description info
Install this package if you want the information files that are
distributed with the XEmacs text editor.


%prep

%setup -q 
%patch1 -p1 -b .aixconf
%patch2 -p1 -b .png

cp %{SOURCE18} src/s/aix6-1.h

rm -f xemacs-packages

%build
export RM="/usr/bin/rm -f"

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
       export CFLAGS="$RPM_OPT_FLAGS -qmaxmem=16384"
fi

./configure --prefix=%{_prefix} --cppflags='-I. -I/opt/freeware/include -I/usr/include -I/usr/include/X11' --libs='-L/opt/freeware/lib -L/usr/lib -L/usr/lib/X11' \
	--extra-verbose=yes \
	--with-gpm=no \
        --with-sound=no \
        --with-pop \
        --mail-locking=lockf \
        --with-clash-detection \
        --debug=yes \
        --with-mule=yes \
	--with-ldap=no \
	--with-database=no \
        --with-menubars=lucid \
        --with-scrollbars=lucid \
        --with-dialogs=lucid \
        --with-xim=xlib \
        --with-canna=no \
        --with-wnn=no \
        --with-wnn6=no \
        --with-msw=no \
        --with-xfs=yes

make 

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=$RPM_BUILD_ROOT/%{_prefix} infodir=$RPM_BUILD_ROOT/%{_infodir} 


# These would clash with GNU Emacs
rm -f $RPM_BUILD_ROOT/usr/bin/[ce]tags
rm -f $RPM_BUILD_ROOT/usr/bin/rcs-checkin
rm -f $RPM_BUILD_ROOT/usr/bin/b2m
rm $RPM_BUILD_ROOT/%{_mandir}/man1/[ce]tags.1

mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/xemacs

# unpack lisp files from sumo packages

buildpath=`pwd`
cd  $RPM_BUILD_ROOT%{_prefix}/lib/xemacs
bunzip2 -c %{SOURCE4} | tar -xf -
cd $RPM_BUILD_ROOT%{_prefix}/lib/xemacs
bunzip2 -c %{SOURCE5} | tar -xf -
cd ${buildpath}

mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/xemacs/site-packages

find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages -name \*.pl -exec \
    perl -pi -e "s|/usr/local/bin/perl5|/usr/bin/perl|g; \
                 s|/usr/local/bin/perl|/usr/bin/perl|g;" {} \;

find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages -name file-newer -exec \
    perl -pi -e "s|/usr/local/bin/perl|/usr/bin/perl|g;" {} \;

%define recompile src/xemacs -batch --no-init-file --no-site-file -f batch-byte-compile

# ispell
cp %{SOURCE10} .
%{recompile} ispell.el
install -m 644 ispell.el ispell.elc $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/ispell

# rpm-spec-mode
cp %{SOURCE14} .
%{recompile}  rpm-spec-mode.el
install -m 644 rpm-spec-mode.el rpm-spec-mode.elc $RPM_BUILD_ROOT%{prefix}/lib/xemacs-%{version}/lisp/

rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
gzip -9nf $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/info/*info*

# These info pages are missed by the policy scripts

gzip -9nf $RPM_BUILD_ROOT%{prefix}/lib/xemacs/mule-packages/info/*
gzip -9nf $RPM_BUILD_ROOT%{prefix}/info/*info*

#These crash with other packages
rm -f $RPM_BUILD_ROOT/%{_infodir}/info*
rm -f $RPM_BUILD_ROOT/%{_infodir}/standards*
rm -f $RPM_BUILD_ROOT/%{_infodir}/termcap*

install -m 755 -d $RPM_BUILD_ROOT/etc/X11/applnk/Applications/
install -m 644  %SOURCE6  $RPM_BUILD_ROOT/etc/X11/applnk/Applications/
install -m 644 %SOURCE9 $RPM_BUILD_ROOT%{prefix}/lib/xemacs-%{version}/lisp/site-start.el

# Lockdir
mkdir -p $RPM_BUILD_ROOT/var/lock/xemacs

# sitestart dir
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d/

# psgml
install -m 644 %SOURCE13 $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d/psgml-init.el
# mew init
install -m 644 %SOURCE17 $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d/ 

# icon
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/pixmaps/
install -m 644 %SOURCE12 $RPM_BUILD_ROOT%{prefix}/share/pixmaps/xemacs.png


# Strip the executables
/usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

( cd $RPM_BUILD_ROOT
  mkdir -p usr/bin
  cd usr/bin
  ln -sf ../..%{prefix}/bin/xemacs .
  ln -sf ../..%{prefix}/bin/xemacs-%{version} .
  ln -sf ../..%{prefix}/bin/gnuattach .
  ln -sf ../..%{prefix}/bin/gnuclient .
  ln -sf ../..%{prefix}/bin/gnudoit .
  ln -sf ../..%{prefix}/bin/ootags .
  cd -

  mkdir -p usr/lib
  cd usr/lib
  ln -sf ../..%{prefix}/lib/xemacs-%{version} .
  cd -

  mkdir -p usr/share
  cd usr/share
  ln -sf ../..%{prefix}/xemacs-%{version} .
  cd -
)

# Wanderlust
cd $RPM_BUILD_ROOT
gunzip -c %{SOURCE100} |tar -xf -

# semi
gunzip -c %{SOURCE150} |tar -xf -

# remove the mailcap lisp files from semi-xemacs - they break stuff
rm -fr $RPM_BUILD_ROOT%{prefix}/xemacs/xemacs-packages/lisp/flim/mailcap.*

# Make sure nothing is 0400

chmod -R a+rX  $RPM_BUILD_ROOT%{prefix}


# separate files
cd $RPM_BUILD_DIR/%{name}-%{version}

echo "%defattr(-,root,root)" > lispfiles
echo "%defattr(-,root,root)" > notlispfiles

find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/  -type f -name "*.el" |grep -v -E "(tex-site.el|site-start.d|eieio.el)" >> lispfiles
find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/mule-packages/  -type f -name "*.el" >> lispfiles
find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/  -type f -not -name "*.el" >> notlispfiles
find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/mule-packages/  -type f -not -name "*.el" >> notlispfiles
find $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages -type d |grep -v /usr/lib/xemacs/xemacs-packages/lisp/site-start.d >> dirs

perl -pi -e "s|$RPM_BUILD_ROOT||" lispfiles
perl -pi -e "s|$RPM_BUILD_ROOT||" notlispfiles
perl -pi -e "s|$RPM_BUILD_ROOT||" dirs
perl -pi -e "s/^(.*)$/%dir \1/" dirs
cat dirs notlispfiles > mainpackagefiles

%pre                                   
#  
# Possibly being overly-paranoid here, but let's check /usr/lib/xemacs:
#                                                                 
if [[ -e /usr/lib/xemacs && ! -L /usr/lib/xemacs ]]               
then                                              
   echo "Cannot install: /usr/lib/xemacs already exists and is not a symlink"
   exit 1                                                         
fi                                                                
        
%post
if [[ ! -L /usr/lib/xemacs ]]
then                        
  ln -s %{prefix}/lib/xemacs /usr/lib/xemacs
fi               

%postun
if [[ -e /usr/lib/xemacs ]]
then                      
   rm -f /usr/lib/xemacs  
fi  

%triggerpostun -- aspell 0.33.6.3-1
# Because of an error in the original aspell, uninstall of it
# will cause /usr/lib/xemacs to be removed.  So:            
# If (xemacs is installed) and (the link is not there)      
# then (put the link back!)                          
if [[ -f %{prefix}/bin/xemacs ]] && [[ ! -L /usr/lib/xemacs ]]
then                                                         
  ln -s ../..%{prefix}/lib/xemacs /usr/lib/xemacs            
fi           


%files -f mainpackagefiles
%defattr(-, root, root)
%config /etc/X11/applnk/Applications/xemacs.desktop
%doc INSTALL README COPYING GETTING.GNU.SOFTWARE PROBLEMS 
%doc etc/NEWS etc/MAILINGLISTS BUGS README.packages
%doc etc/TUTORIAL
%attr(1777, root, root) /var/lock/xemacs
%{_mandir}/*/*
%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d/*
%{prefix}/lib/xemacs-%{version}
%{prefix}/share/pixmaps/xemacs.png
%{prefix}/lib/xemacs/xemacs-packages/lisp/auctex/tex-site.el
%{prefix}/bin/xemacs
%{prefix}/bin/xemacs-%{version}
%{prefix}/bin/gnuattach
%{prefix}/bin/gnuclient
%{prefix}/bin/gnudoit
%{prefix}/bin/ootags
/usr/bin/*
/usr/share/*
/usr/lib/*
# Wanderlust
%config %{prefix}/etc/skel/.wl


%files el -f lispfiles
%defattr(-, root, root)

%files info
%defattr(-, root, root)
%{_infodir}/*


%post info
/sbin/install-info %{_infodir}/xemacs.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/cl.info.gz %{_infodir}/dir  || :
/sbin/install-info %{_infodir}/internals.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/lispref.info.gz %{_infodir}/dir  || :
/sbin/install-info %{_infodir}/new-users-guide.info.gz %{_infodir}/dir || :
                                                                  
%preun info                                                      
if  [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/xemacs.info.gz %{_infodir}/dir || :
	/sbin/install-info --delete %{_infodir}/cl.info.gz %{_infodir}/dir || :
	/sbin/install-info --delete %{_infodir}/internals.info.gz %{_infodir}/dir || :
	/sbin/install-info --delete %{_infodir}/lispref.info.gz %{_infodir}/dir || :
	/sbin/install-info --delete %{_infodir}/new-users-guide.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Thu Mar 15 2012 Patricia Cugny <patricia.cugny@bull.net> 21.4.22-1
- Update to last stable version 21.4.22

* Thu Jan 31 2008 Reza Arbab <arbab@austin.ibm.com> 21.1.14-2
- Rebuild against newer libpng: libpng.a(libpng.so.3)

* Mon Jun 18 2001 David Clissold <cliss@austin.ibm.com>
- Initial build for AIX Toolbox

* Tue Apr 24 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New sumo packages

* Mon Mar 19 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed semi's mailcap issues.

* Fri Mar 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- remove the mailcap lisp files from semi-xemacs - they break stuff
- don't include our own sh-script files anymore, bash is now bash2

* Thu Mar  8 2001 Akira TAGOH <tagoh@redhat.com>
- 21.1.14-8
- Merged semi-xemacs into the main package, as
  wl (already bundled) needs it.
- Fixed the byte-compile for wl.

* Fri Mar 02 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Feb 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- minor fixes to psgml-init.el

* Mon Feb 12 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Move eieio.el to the main package (#26753)
- Prereq info

* Thu Feb  8 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add init file for mew

* Mon Feb  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Obsolete xemacs-static

* Fri Feb 02 2001 Trond Eivind Glomsrød <teg@redhat.com>
- obsolete xemacs-noX and xemacs-mule

* Sun Jan 29 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 21.1.14

* Wed Jan 24 2001 Yukihiro Nakai <ynakai@redhat.com>
- enable Wanderlust

* Tue Jan 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- added Japanese support to .desktop file

* Mon Jan 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- enable canna, wnn4, wnn6
- improve app-defaults file for Japanese and traditional
  Chineese

* Fri Jan 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- turn on --with-xfs to improve support for Japanese
- copy the app-defaults to /usr/X11R6/lib/X11/app-defaults
- add app-defaults for traditional Chineese

* Mon Jan 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 21.1.13
- update the rpm spec mode
- removed the alpha patch
- remove the elc sourcefile, these can be generated during the build 
  process

* Tue Jan 02 2001 Trond Eivind Glomsrød <teg@redhat.com>
- make sure it doesn't use canna, wnn or wnn6 by default

* Thu Dec 28 2000 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Tue Dec 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix psgml mode by adding the psgml-init.el file from the
  psgml package. Should fix #21827
- add rpm-spec-mode

* Sat Dec 09 2000 Than Ngo <than@redhat.com>
- added s390 port

* Mon Dec 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make sure that the info pages in /usr/lib/xemacs/mule-packages/info/ 
  are compressed

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add "--with-xim=xlib" to configure to avoid linking with Motif

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- move site-start.el to /usr/lib/xemacs/xemacs-packages/lisp/site-start.el
  (it shouldn't depend on xemacs version)
- add new directory  /usr/lib/xemacs/xemacs-packages/lisp/site-start.d
- change run .el files here on startup 
- revert to "normal" xemacs 

* Tue Nov 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix the "restore cursor" problem I submitted myself before I
  started here(#9853). Sometimes, you're digging your own grave
  without even knowing.

* Tue Nov 14 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new sumo tarballs
- new xemacs tarball
- fixing of the improved .desktop file 
- include xemacs.png file (from kdebase) to be used with
  above file

* Tue Oct 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new and better xemacs.desktop file

* Tue Oct 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use xemacs package from 2000-09-25
- move tex-site.el to main package (#18494)

* Tue Sep 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove README.i386-pc-linux - it's no longer anywhere
  near accurate
- update sumo package to 2000-09-04
- use mule by default, like we do for GNU Emacs
- use gtk-xemacs - it's in the XEmacs cvs now
- move the xemacs desktop file to "Applications"
- specify ldap (it was just detected before)
- enable native sound
- remove a binary which somehow had made it into the lisp package,
  compiled with libraries we don't have

* Thu Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- change locking mechanism to lockf

* Thu Aug 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use ispell.el from GNU Emacs, which work better
  than the ones found at the xemacs ftp site or at the 
  author's site. Fixes bug #16071

* Sun Aug 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 21.1.12 bugfix release
- removed security patch as it is now included
- gzip info packages in the package directory

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 21.1.11
- upgrade(? - it wasn't specified) to sumo tarball from 2000-05-24
- add a sitestart.rl file, for configuration of info and spelling
- fixed the ownership of lots of package directories (#14197)
- disabled ia64 patch as they know have their own support...
- ... which doesn't work. Excludearch coming up.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 03 2000 Than Ngo <than@redhat.de>
- don't use xemac to compile some lisp-source in byte code 

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- include the files in the %%{_infodir}, not the directory

* Wed Jun 28 2000 Than Ngo <than@redhat.de>
- add xemacs-extras xemacs-packages-el xemacs-packages in obsoletes
  to resolse conflicts (#13120)
- add missing stuff (#13176)

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't specify -O0
- do it anyway for IA64

* Tue Jun 20 2000 Bill Nottingham <notting@redhat.com>
- build on ia64

* Tue Jun 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- override optflags, use -O0 to avoid compiler bugs
  (last build, actually)
- don't include some info files which clash with others

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- redid most of the spec file

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- build in the main tree
- disabled static package (it was partially disabled...)
- don't change ownership while installing
- updated some of the documentation (s/21.1.8/21.1.10/)
- don't build on IA64
- use %%{_mandir} instead of hardcoding /usr/share/man

* Mon May 29 2000 Ngo Than <than@redhat.de>
- update to 2.1.10 for 7.0
- fix permission
- put man pages in correct place
- fix xemacs to build with gcc-2.96 (thanks Jakub)

* Wed May 24 2000 Ngo Than <than@redhat.de>
- fix a security problem in key strokes.
- fix a permission problem. XEmacs doesn't set proper permissions for the slave PTY device.
- remove xemacs static

* Thu Mar 23 2000 Ngo Than <than@redhat.de>
- updated to 21.1.9

* Fri Feb 11 2000 Ngo Than <than@redhat.de>
- fixed Bug #7694, #9149

* Tue Jan 18 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space
- fixed so that alpha builds properly
- removed the --with-xface stuff.

* Wed Dec 1 1999 Tim Powers <timp@redhat.com>
- updated to 21.1.8
- gzip man pages
- now builds for alpha :)

* Thu Oct 21 1999 Cristian Gafton <gafton@redhat.com>
- include /var/lock/xemacs as the lockdir to make it stop whining

* Thu Aug 19 1999 Tim Powers <timp@redhat.com>
- fixed problem with dirs not being removed during uninstall

* Sun Jul 11 1999 Tim Powers <timp@redhat.com>
- updated to version 21.1.4
- added the elc and info src.
- modified spec as needed
- had a beer after building

* Fri May 14 1999 Cristian Gafton <gafton@redhat.com>
- version 21.1.2
- require ctags

* Wed Oct 14 1998 Michael Maher <mike@redhat.com>
- built pacakge for 5.2, didn't use a pre update. 

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- updated to 20.4
- new package xemacs-mule with mule support
- Changed spec file almost completely

* Fri Dec  5 1997 Otto Hammersmith <otto@redhat.com>
- refixed perl problem.
- added wmconfig

* Tue Dec  2 1997 Otto Hammersmith <otto@redhat.com>
- added changelog
- configure for ncurses
- removed sound support on i386
- moved buildroot to /var/tmp
