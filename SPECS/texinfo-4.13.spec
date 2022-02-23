Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 4.13
Release: 1
Copyright: GPL
Group: Applications/Publishing
URL: http://www.gnu.org/software/texinfo
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/tmp/texinfo-root
%define DEFCC cc

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file.  The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation.
Group: System Environment/Base
# By making info prereq bash, other packages which have triggers based on
# info don't run those triggers until bash is in place as well. This is an
# ugly method of doing it (triggers which fire on set intersection would
# be better), but it's the best we can do for now. Talk to Erik before
# removing this.
Prereq: bash 
  
%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.
  
You should install info, because GNU's texinfo documentation is a
valuable source of information about the software on your system.
  
%prep
%setup -q

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
make CFLAGS="$RPM_OPT_FLAGS"
make -C util LIBS=-lz

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/sbin

make install DESTDIR=${RPM_BUILD_ROOT}

( cd ${RPM_BUILD_ROOT}
  gzip -n -9f .%{prefix}/info/*info*
  install -m644 ${RPM_BUILD_ROOT}%{prefix}/info/dir ./etc/info-dir
  rm -f ${RPM_BUILD_ROOT}%{prefix}/info/dir
  ln -sf /etc/info-dir ${RPM_BUILD_ROOT}%{prefix}/info/dir
  for i in makeinfo texindex info install-info ; do
    /usr/bin/strip .%{prefix}/bin/$i
  done
  ln -sf ..%{prefix}/bin/install-info ./sbin
  mkdir -p usr/bin 
  cd usr/bin
  ln -sf ../..%{prefix}/bin/* .
  cd - 
  ln -sf ..%{prefix}/info ./usr/info

mkdir -p etc/X11/applnk/Utilities
cat > ./etc/X11/applnk/Utilities/info.desktop <<EOF
[Desktop Entry]
Name=Info Viewer
Name[sv]=Infovisare
Name[de]=Info-Viewer
Type=Application
Comment=GNU Info Page Reader
Comment[sv]=GNU Info-sidl�sare
Comment[de]=GNU Info-Seiten-Viewer
Exec=info
Terminal=true 
EOF

)

%clean
rm -rf ${RPM_BUILD_ROOT}

%pre -n info
# There is a possibility that /usr/bin/info is left around from a
# 3.2 migration
if [ ! -L /usr/bin/info ] && [ ! -f /usr/bin/info ]
then
      ln -s %{prefix}/bin/info /usr/bin/info
else
   if [ ! -L /usr/bin/info ]
   then
      if [[ ! -d /usr/linux/bin ]]
      then
         umask 022
         mkdir -p /usr/linux/bin
      fi 
      ln -sf %{prefix}/bin/info /usr/linux/bin/info
   fi
fi

%post
/sbin/install-info %{prefix}/info/texinfo.gz %{prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{prefix}/info/texinfo.gz %{prefix}/info/dir
fi

%post -n info
/sbin/install-info %{prefix}/info/info-stnd.info.gz %{prefix}/info/dir
/usr/bin/chmod -R o-w /etc/X11

%preun -n info 
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{prefix}/info/info-stnd.info.gz %{prefix}/info/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL INTRODUCTION NEWS README TODO
%doc info/README
/usr/bin/makeinfo
/usr/bin/texindex
/usr/bin/texi2dvi
%{prefix}/bin/makeinfo
%{prefix}/bin/texindex
%{prefix}/bin/texi2dvi
%{prefix}/info/texinfo*
%{prefix}/share/locale/*/*/*

%files -n info
%defattr(-,root,root)
%doc COPYING
%config(missingok) /etc/X11/applnk/Utilities/info.desktop
%config(noreplace) /etc/info-dir
%config(noreplace) %{prefix}/info/dir
%{prefix}/bin/info
%{prefix}/bin/install-info
%{prefix}/info/info.info*
%{prefix}/info/info-stnd.info*
/usr/info
/sbin/install-info

%changelog
* Wed Jun 2 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.13
- Update to version 4.13

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 4.6-1
- Update to version 4.6

* Tue Mar 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild with default compiler
- Rebuild without ncurses

* Fri Mar 02 2001 Marc Stephenson <marc@austin.ibm.com>
- Add desktop entry
- Fix INFODIR search path

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions

* Wed Jan 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move info-stnd.info* to the info package, /sbin/install-info it
  in %post (Bug #6632)

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- recompile to eliminate ncurses foul-up.
* Tue Nov  9 1999 Bernhard Rosenkr�nzer <bero@redhat.com>
- 4.0
- handle RPM_OPT_FLAGS

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- import version 3.12h into 6.1 tree from HJLu

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Erik Troan <ewt@redhat.com>
- hacked to use zlib to get rid of the requirement on gzip

* Wed Mar 17 1999 Matt Wilson <msw@redhat.com>
- install-info prerequires gzip

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- version 3.12f
- make /usr/info/dir to be a %config(noreplace)
* Wed Nov 25 1998 Jeff Johnson <jbj@redhat.com>
- rebuild to fix docdir perms.

* Thu Sep 24 1998 Cristian Gafton <gafton@redhat.com>
- fix allocation problems in install-info

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- /sbin/install-info should not depend on /usr/lib/libz.so.1 -- statically
  link with /usr/lib/libz.a.

* Fri Aug 07 1998 Erik Troan <ewt@redhat.com>
- added a prereq of bash to the info package -- see the comment for a
  description of why that was done

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add %attr to permit non-root build.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean
- manhattan build

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 3.12
- added buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- moved /usr/info/dir to /etc/info-dir and made /usr/info/dir a
  symlink to /etc/info-dir.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry for info

* Wed Oct 01 1997 Donnie Barnes <djb@redhat.com>
- stripped /sbin/install-info

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added info-dir to filelist

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added patch from sopwith to let install-info understand gzip'ed info files
- use skeletal dir file from texinfo tarball (w/ bash entry to reduce
  dependency chain) instead (and install-info command everywhere else)
- patches install-info to handle .gz names correctly

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- patched install-info.c for glibc.
- added /usr/bin/install-info to the filelist

* Tue Feb 18 1997 Michael Fulbright <msf@redhat.com>
- upgraded to version 3.9.

