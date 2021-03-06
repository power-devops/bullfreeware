Summary: The GNU Bourne Again shell (bash).
Name: bash
Version: 4.1
Release: 9
Group: System Environment/Shells
Copyright: GPL
URL: http://www.gnu.org/software/bash
Source0: ftp://ftp.gnu.org/gnu/bash/bash-%{version}.tar.gz
Patch0: %{name}-%{version}-001.patch
Patch1: %{name}-%{version}-002.patch
Patch2: %{name}-%{version}-003.patch
Patch3: %{name}-%{version}-004.patch
Patch4: %{name}-%{version}-005.patch
Patch5: %{name}-%{version}-006.patch
Patch6: %{name}-%{version}-007.patch
Patch7: %{name}-%{version}-aixconf.patch
Prefix: %{_prefix}
Provides: bash
# Must keep this; have renamed the package from bash2
Obsoletes: bash2
BuildRoot: /var/tmp/%{name}-root

# Fails on 4.3 if not using stdc (i.e., use xlc instead of cc)
%define DEFCC xlc

%description
The GNU bash shell is a command language interpreter that attempts
compatibility with the Bourne shell (sh).  Bash incorporates useful features
from the Korn shell (ksh) and the C shell (csh).  Most sh scripts can be run by
bash without modification.  Bash is intended to be a conformant implementation
of the IEEE Posix Shell and Tools specification (IEEE Working Group 1003.2).

%package doc
Group: Documentation
Summary: Documentation for the GNU Bourne Again shell (bash).
# Must keep this; have renamed the package from bash2
Obsoletes: bash2-doc
  
%description doc
The bash-doc package contains documentation for the GNU bash shell.

%prep
%setup -q -n bash-%{version} 
%patch0 -p0 -b .001
%patch1 -p0 -b .002
%patch2 -p0 -b .003
%patch3 -p0 -b .004
%patch4 -p0 -b .005
%patch5 -p0 -b .006
%patch6 -p0 -b .007
%patch7 -p1 -b .aixconf

echo %{version} > _distribution
echo %{release} > _patchlevel
echo %{_prefix}

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
fi
export CFLAGS="$RPM_OPT_FLAGS"

%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} \
     bindir=${RPM_BUILD_ROOT}%{_prefix}/bin \
     mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
     install

[[ ! -d $RPM_BUILD_ROOT/usr/bin ]] && mkdir -p $RPM_BUILD_ROOT/usr/bin
[[ ! -d $RPM_BUILD_ROOT/bin ]] && mkdir -p $RPM_BUILD_ROOT/bin
ln -sf ../..%{_prefix}/bin/bash $RPM_BUILD_ROOT/bin/bash
ln -sf ../..%{_prefix}/bin/bashbug $RPM_BUILD_ROOT/usr/bin/bashbug

{ cd $RPM_BUILD_ROOT
  strip ./%{_prefix}/bin/* || :
  cd bin 
  ln -sf bash bash2
  cd ../usr/bin
  ln -sf bashbug bash2bug
}

%clean 
rm -rf $RPM_BUILD_ROOT

# ***** bash doesn't use install-info. It's always listed in /usr/info/dir
# to prevent prereq loops

%files
%defattr(-,root,system)
%doc COPYING CHANGES COMPAT NEWS NOTES
%doc doc/FAQ doc/INTRO doc/article.ms
%doc doc/*.ps doc/*.html doc/*.txt
/bin/bash
/bin/bash2
%{_prefix}/bin/bash
/usr/bin/bashbug
/usr/bin/bash2bug
%{_prefix}/bin/bashbug
%{_prefix}/man/man1/*bash.1*
%{_prefix}/man/man1/bashbug.1*

%files doc
%defattr(-,root,system)
%doc doc/*.ps

%changelog
* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 4.1-9
- Initial port on Aix6.1

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
