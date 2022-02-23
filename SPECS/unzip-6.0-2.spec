Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.0
Release:	2
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:	http://ftp.info-zip.org/pub/infozip/src/%{name}60.tar.bz2
Prefix: 	%{_prefix}
BuildRoot:	%{_tmppath}/%{name}-root
%define DEFCC cc


%description
unzip will list, test, or extract files from a ZIP archive, commonly found
on MS-DOS systems. A companion program, zip, creates ZIP archives; both
programs are compatible with archives created by PKWARE's PKZIP and
PKUNZIP for MS-DOS, but in many cases the program options or default
behaviors differ.

This version also has encryption support.

%prep

%setup -qn %{name}60

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
export RM="/usr/bin/rm -f"

make -f unix/Makefile CC=$CC generic


%install
rm -rf %{RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make -f unix/Makefile \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=%{_prefix}/man \
	install

strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/* .
 cd -
)

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README BUGS COPYING.OLD LICENSE INSTALL ToDo WHERE
%{_prefix}/bin/funzip
%{_prefix}/bin/unzip
%{_prefix}/bin/unzipsfx
%{_prefix}/bin/zipgrep
%{_prefix}/bin/zipinfo
/usr/bin/funzip
/usr/bin/unzip
/usr/bin/unzipsfx
/usr/bin/zipgrep
/usr/bin/zipinfo
%{_prefix}/man/man1/*

%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 6.0-2
- Initial port on Aix6.1

* Mon May 31 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 6.0
- Update to 6.0 release

* Mon May 24 2004 Philip K. Warren <pkw@us.ibm.com> 5.51-1
- Update to latest 5.51 release, which fixes several directory traversal
  vulnerabilities.

* Tue Apr 13 2004 David Clissold <cliss@austin.ibm.com> 5.50-1
- Update to version 5.50.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri May 18 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 5.42
- Build with large files enabled

* Thu Mar 22 2001 David Clissold <cliss@austin.ibm.com>
- Change to use cc as default compiler if available (over gcc)

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- update to 5.40

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- builds on non i386 platforms

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- updated the version

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
