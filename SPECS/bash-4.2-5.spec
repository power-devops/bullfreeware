Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}
Version: 4.2
Release: 5
Group: System Environment/Shells
License: GPLv2+
Url: http://www.gnu.org/software/bash
Source0: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
# patches from ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches
Patch0: bash42-001.patch
Patch1: bash42-002.patch 
Patch2: bash42-003.patch
Patch3: bash42-004.patch
Patch4: bash42-005.patch
Patch5: bash42-006.patch
Patch6: bash42-007.patch
Patch7: bash42-008.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Provides: bash
# Must keep this; have renamed the package from bash2
Obsoletes: bash2

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}, which improves POSIX
compliance over previous versions.

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash).
# Must keep this; have renamed the package from bash2
Obsoletes: bash2-doc

%description doc
The bash-doc package contains documentation for the GNU bash shell.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n bash-%{version}
#  patches
%patch0 -p0 -b .001
%patch1 -p0 -b .002
%patch2 -p0 -b .003
%patch3 -p0 -b .004
%patch4 -p0 -b .005
%patch5 -p0 -b .006
%patch6 -p0 -b .007
%patch7 -p0 -b .008

%build
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir}
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

cp doc/builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
ln -sf ../..%{_bindir}/bash ${RPM_BUILD_ROOT}/bin/bash
ln -sf ../..%{_prefix}/bin/bashbug ${RPM_BUILD_ROOT}/usr/bin/bashbug

{
  cd ${RPM_BUILD_ROOT}
  cd bin
  ln -sf bash bash2
  cd ../usr/bin
  ln -sf bashbug bash2bug
}


%post
if [ ! -f /etc/shells ]; then
    echo "%{_bindir}/bash" >> /etc/shells
else
    grep -q '^%{_bindir}/bash$' /etc/shells || \
        echo "%{_bindir}/bash" >> /etc/shells
fi


%postun
if [ ! -x %{_bindir}/bash ]; then
    grep -v '^%{_bindir}/bash$' /etc/shells > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGES COMPAT NEWS NOTES POSIX
%doc doc/FAQ doc/INTRO doc/article.ms doc/article.txt
%{_bindir}/*
%{_infodir}/bash.info*
%{_mandir}/man1/*
%{_datadir}/locale/*/*/*
/bin/bash*
/usr/bin/bash*

%files doc
%defattr(-,root,system)
%doc doc/*.ps
%doc examples/obashdb/ examples/functions/ examples/misc/
%doc examples/scripts.noah/ examples/scripts.v2/ examples/scripts/
%doc examples/startup-files/ examples/complete/

%changelog
* Tue Sep 20 2011 Patricia Cugny <patricia.cugny@bull.net> 4.2-5
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri May 6 2011 Patricia Cugny <patricia.cugny@bull.net> 4.2-4
- update to 4.2-4 + official patches

* Thu Jun 3 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.1-7
- Update to version 4.1 + 7 official patches

* Fri Apr 22 2005 David Clissold <cliss@austin.ibm.com> 3.0-1
- Update to version 3.0 (thru patchlevel 16).

* Mon Nov 24 2003 David Clissold <cliss@austin.ibm.com>
- Update to version 2.05b.

* Wed Apr 10 2002 David Clissold <cliss@austin.ibm.com>
- Rename package from bash2 to bash, for consistency with everything else.
- No functional change made.

* Wed Jan 30 2002 David Clissold <cliss@austin.ibm.com>
- Update to 2.05a

* Wed May 16 2001 Marc Stephenson <marc@austin.ibm.com>
- Work around real-time signals problem
- Removed extra configure in install phase

* Wed May 16 2001 Marc Stephenson <marc@austin.ibm.com>
- Work around real-time signals problem
- Removed extra configure in install phase

* Tue May 15 2001 Marc Stephenson <marc@austin.ibm.com>
- Initial build for version 2.05

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description

* Thu Dec  2 1999 Ken Estes <kestes@staff.mail.com>
- updated patch to detect what executables are required by a script.

* Fri Sep 14 1999 Dale Lovelace <dale@redhat.com>
- Remove annoying ^H's from documentation

* Fri Jul 16 1999 Ken Estes <kestes@staff.mail.com>
- patch to detect what executables are required by a script.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)
* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.
- include bash-doc correctly.

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- fixed post/postun /etc/shells work.

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- updated again text in the spec file

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 2.03.

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- build it as bash2 instead of bash

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- set 'NON_INTERACTIVE_LOGIN_SHELLS' so profile gets read

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- rename man pages in bash-doc to avoid packaging conflicts (#606).

* Wed Dec 02 1998 Cristian Gafton <gafton@redhat.com>
- patch for the arm
- use $RPM_ARCH-redhat-linux as the build target

* Tue Oct  6 1998 Bill Nottingham <notting@redhat.com>
- rewrite %pre, axe %postun (to avoid prereq loops)

* Wed Aug 19 1998 Jeff Johnson <jbj@redhat.com>
- resurrect for RH 6.0.

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.02.1

* Thu Jun 11 1998 Jeff Johnson <jbj@redhat.com>
- Package for 5.2.

* Mon Apr 20 1998 Ian Macdonald <ianmacd@xs4all.nl>
- added POSIX.NOTES doc file
- some extraneous doc files removed
- minor .spec file changes

* Sun Apr 19 1998 Ian Macdonald <ianmacd@xs4all.nl>
- upgraded to version 2.02
- Alpha, MIPS & Sparc patches removed due to lack of test platforms
- glibc & signal patches no longer required
- added documentation subpackage (doc)

* Fri Nov 07 1997 Donnie Barnes <djb@redhat.com>
- added signal handling patch from Dean Gaudet <dgaudet@arctic.org> that
  is based on a change made in bash 2.0.  Should fix some early exit
  problems with suspends and fg.

* Mon Oct 20 1997 Donnie Barnes <djb@redhat.com>
- added %clean


* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- added comment explaining why install-info isn't used
- added mips patch

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

