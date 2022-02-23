Summary: Tools needed to create Texinfo format documentation files.
Name: texinfo
Version: 5.0
Release: 1
Copyright: GPL
Group: Applications/Publishing
URL: http://www.gnu.org/software/texinfo
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.gz.sig
Prereq: /sbin/install-info, info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

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
# Building binaries in 64bit mode
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/sbin

## /usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*info*

( 
cd ${RPM_BUILD_ROOT}
mkdir -p sbin
ln -sf ..%{_bindir}/install-info ./sbin
mkdir -p etc
cp ${RPM_BUILD_ROOT}%{_infodir}/dir ./etc/info-dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
chmod 0644 ./etc/info-dir
ln -sf /etc/info-dir ${RPM_BUILD_ROOT}%{_infodir}/dir
for dir in bin lib
  do
     mkdir -p usr/${dir}
     cd usr/${dir}
     ln -sf ../..%{_prefix}/${dir}/* .
     cd -
done
## cd usr
ln -sf ..%{_infodir} ./usr/info
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

%post
/sbin/install-info %{_infodir}/%{name}.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/%{name}.gz %{_infodir}/dir || :
fi

%post -n info
/sbin/install-info %{_infodir}/info-stnd.info.gz %{_infodir}/dir || :
echo "Please check that /etc/info-dir does exist."
echo "You might have to rename it from /etc/info-dir.rpmsave to /etc/info-dir."

%preun -n info 
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/info-stnd.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc AUTHORS COPYING INSTALL NEWS README TODO
%doc info/README
%{_bindir}/makeinfo
%{_bindir}/pdftexi2dvi
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/texindex
%{_libdir}/charset.alias
%{_mandir}/man1/makeinfo.1
%{_mandir}/man1/pdftexi2dvi.1
%{_mandir}/man1/texi2dvi.1
%{_mandir}/man1/texi2pdf.1
%{_mandir}/man1/texindex.1
%{_mandir}/man5/texinfo.5
%{_infodir}/texinfo*
%{_datadir}/%{name}
%{_datadir}/locale/*/*/*
/usr/bin/makeinfo
/usr/bin/pdftexi2dvi
/usr/bin/pod2texi
/usr/bin/texi2any
/usr/bin/texi2dvi
/usr/bin/texi2pdf
/usr/bin/texindex
/usr/lib/charset.alias

%files -n info
%defattr(-,root,system)
%doc COPYING
%config(missingok) /etc/X11/applnk/Utilities/info.desktop
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%{_bindir}/info
%{_bindir}/infokey
%{_bindir}/install-info
%{_mandir}/man1/info.1
%{_mandir}/man1/infokey.1
%{_mandir}/man1/install-info.1
%{_mandir}/man5/info.5
%{_infodir}/info.info*
%{_infodir}/info-stnd.info*
/usr/bin/info
/usr/bin/infokey
/sbin/install-info

%changelog
* Mon Mar 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.0-1
- Update to version 5.0

* Tue Sep 20 2011 Patricia Cugny <patricia.cugny@bull.net> 4.13-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri May 6 2011 Patricia Cugny <patricia.cugny@bull.net> 4.13-2
- minor modif in spec file

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

