Summary: A version control system.
Name: cvs
Version: 1.11.17
Release: 3
License: GPL
Group: Development/Tools
Source0: ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.bz2
Patch0: %{name}-%{version}-cvspass.patch
Patch1: %{name}-%{version}-use-system-zlib.patch
Patch2: %{name}-%{version}-CAN-2005-0753.patch
Prefix: %{_prefix}
Buildroot: %{_tmppath}/%{name}-root
Requires: zlib
BuildRequires: zlib-devel
%define DEFCC cc

%description
CVS (Concurrent Version System) is a version control system which can record
the history of your files (usually, but not always, source code).  CVS only
stores the differences between versions, instead of every version of every file
you've ever created.  CVS also keeps a log of who, when and why changes
occurred.

CVS is very helpful for managing releases and controlling the concurrent
editing of source files among multiple authors.  Instead of providing version
control for a collection of files in a single directory, CVS provides version
control for a hierarchical collection of directories consisting of revision
controlled files.  These directories and files can then be combined together to
form a software release.

%prep
%setup -q
%patch0 -p1 -b .cvspass
%patch1 -p0 -b .use-system-zlib
%patch2 -p0 -b .CAN-2005-0753

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

export CSH=/usr/bin/csh  #So we don't prereq the tcsh package
export CFLAGS="-DSIZE_MAX=LONG_MAX"  # size of size_t
./configure --prefix=%{_prefix}

make LDFLAGS=-s
make -C doc info

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

gzip -9nf $RPM_BUILD_ROOT/%{_prefix}/info/cvs*
/usr/bin/strip $RPM_BUILD_ROOT/%{_prefix}/bin/cvs || :

(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/* .
 cd -
)

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/info/cvs.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/cvsclient.info.gz %{_prefix}/info/dir 

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/cvs.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/cvsclient.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README 
%doc doc/RCSFILES doc/*.ps
/usr/bin/*
/%{_prefix}/bin/cvs
/%{_prefix}/bin/cvsbug
/%{_prefix}/bin/rcs2log
/%{_prefix}/man/man1/cvs.1*
/%{_prefix}/man/man5/cvs.5*
/%{_prefix}/man/man8/cvsbug.8*
/%{_prefix}/info/cvs*
/%{_prefix}/share/cvs

%changelog
* Tue Dec 27 2005 Reza Arbab <arbab@austin.ibm.com> 1.11.17-3
- Add a patch to use the system zlib rather than our bundled one.
- Add a patch for CAN-2005-0753.

* Tue Oct 19 2004 David Clissold <cliss@austin.ibm.com> 1.11.17-2
- Add a patch for a login failure w/o .cvspass bug.

* Fri Jun 11 2004 David Clissold <cliss@austin.ibm.com> 1.11.17-1
- Update to version 1.11.17.

* Wed Jun 09 2004 David Clissold <cliss@austin.ibm.com> 1.11.5-5
- Latest cvs patches (CAN-2004-0414, 0416, 0417, 0418).

* Wed May 19 2004 Philip K. Warren <pkw@us.ibm.com> 1.11.5-4
- Add fix for latest CVS vulnerability (CAN-2004-0396).

* Tue May 18 2004 David Clissold <cliss@austin.ibm.com> 1.11.5-3
- Force CSH=/usr/bin/csh so we don't have a mandatory req on tcsh rpm.

* Thu May 06 2004 Philip K. Warren <pkw@us.ibm.com> 1.11.5-2
- Apply three patches for CVS security issues.
- Remove build requirement on autoconf.

* Mon Jan 20 2003 David Clissold <cliss@austin.ibm.com>
- Update to new version, 1.11.5.

* Fri Apr 26 2002 David Clissold <cliss@austin.ibm.com>
- Update to new version, 1.11.2
- Pdf file is "cederqvist-1.11.2.pdf".  Renaming to cvs-1.11.2.pdf
- for the distribution, to match what it was before.

* Tue Jun 26 2001 Marc Stephenson <marc@austin.ibm.com>
- Remove dependency on CVS rpm

* Mon May 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 1.11.1p1
- Added documentation

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Use default compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Mar  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- make kerberos support conditional at build-time

* Wed Mar  1 2000 Bill Nottingham <notting@redhat.com>
- integrate kerberos support into main tree

* Mon Feb 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- build with gssapi auth (--with-gssapi, --with-encryption)
- apply patch to update libs to krb5 1.1.1

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- fix the damn info pages too while we're at it.
- fix description
- man pages are compressed
- make sure %post and %preun work okay

* Sun Jan 9 2000  Jim Kingdon <http://bugzilla.redhat.com/bugzilla>
- update to 1.10.7.

* Wed Jul 14 1999 Jim Kingdon <http://developer.redhat.com>
- add the patch to make 1.10.6 usable
  (http://www.cyclic.com/cvs/dev-known.html).

* Tue Jun  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.6.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.5.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.4.

* Tue Oct 20 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.3.

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.2.

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- remove trailing characters from rcs2log mktemp args

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.1

* Mon Aug 31 1998 Jeff Johnson <jbj@redhat.com>
- fix race conditions in cvsbug/rcs2log

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.30.

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun  8 1998 Jeff Johnson <jbj@redhat.com>
- build root
- update to 1.9.28

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added install-info stuff
- added changelog section
