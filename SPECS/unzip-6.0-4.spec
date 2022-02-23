# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary:	Unpacks ZIP files such as those made by pkzip under DOS
Name:		unzip
Version:	6.0
Release:	4
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/UnZip.html
Source0:        http://downloads.sourceforge.net/infozip/unzip60.tar.bz2
Source1000: %{name}-%{version}-%{release}.build.log

# Patch from FEDORA 6.0-52

# Upstream plans to do similar thing.
Patch1: unzip-6.0-close.patch
# Details in rhbz#532380.
# Reported to upstream: http://www.info-zip.org/board/board.pl?m-1259575993/
Patch2: unzip-6.0-attribs-overflow.patch

# Update match.c with recmatch() from zip 3.0's util.c
# This also resolves the license issue in that old function.
# Original came from here: https://projects.parabolagnulinux.org/abslibre.git/plain/libre/unzip-libre/match.patch
Patch3: unzip-6.0-fix-recmatch.patch
# Update process.c
Patch4: unzip-6.0-symlink.patch
# change using of macro "case_map" by "to_up"
Patch5: unzip-6.0-caseinsensitive.patch
# downstream fix for "-Werror=format-security"
# upstream doesn't want hear about this option again
Patch6: unzip-6.0-format-secure.patch

Patch7: unzip-6.0-valgrind.patch
Patch8: unzip-6.0-x-option.patch
Patch9: unzip-6.0-overflow.patch
Patch10: unzip-6.0-cve-2014-8139.patch
Patch11: unzip-6.0-cve-2014-8140.patch
Patch12: unzip-6.0-cve-2014-8141.patch
Patch13: unzip-6.0-overflow-long-fsize.patch

# Fix heap overflow and infinite loop when invalid input is given (#1260947)
Patch14: unzip-6.0-heap-overflow-infloop.patch

# support non-{latin,unicode} encoding
Patch15: unzip-6.0-alt-iconv-utf8.patch
Patch16: unzip-6.0-alt-iconv-utf8-print.patch
Patch17: unzip-6.0-Fix-CVE-2016-9844-rhbz-1404283.patch

# restore unix timestamp accurately
Patch18: unzip-6.0-timestamp.patch

# fix possible heap based stack overflow in passwd protected files
Patch19: unzip-6.0-cve-2018-1000035-heap-based-overflow.patch

Patch20: unzip-6.0-cve-2018-18384.patch

# covscan issues
Patch21: unzip-6.0-COVSCAN-fix-unterminated-string.patch


%description
The unzip utility is used to list, test, or extract files from a zip
archive.  Zip archives are commonly found on MS-DOS systems.  The zip
utility, included in the zip package, creates zip archives.  Zip and
unzip are both compatible with archives created by PKWARE(R)'s PKZIP
for MS-DOS, but the programs' options and default behaviors do differ
in some respects.

Install the unzip package if you need to list, test or extract files from
a zip archive.

%prep

%setup -qn %{name}60
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

%build

export AR="/usr/bin/ar -X32_64"
export OBJECT_MODE=64
export CC="gcc -maix64"

# libiconv is needed
gmake --trace -f unix/Makefile generic \
      CC="$CC" CFALGS="$RPM_OPT_FLAGS" \
      LD="$CC -L/opt/freeware/lib64 -L/opt/freeware/lib -liconv"


%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

gmake -f unix/Makefile prefix=$RPM_BUILD_ROOT%{_prefix} MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 INSTALL="cp -p" install

cd $RPM_BUILD_ROOT%{_prefix}

# Strip all of the executables
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# No tests

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc README BUGS COPYING.OLD LICENSE
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Tue May 25 2021 Clement Chigot <clement.chigot@atos.net> 6.0-4
- BullFreeware Compatibility Improvements
- Rebuild in 64bit only
- Rebuild with RPMv4

* Wed Apr 15 2015 Gerard Visiedo <gerard.visiedo@bull.net> - 6.0-3
- Fix security bug - CVE-2014-9636

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
