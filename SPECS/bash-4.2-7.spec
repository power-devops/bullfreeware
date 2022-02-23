Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}
Version: 4.2
Release: 7
Group: System Environment/Shells
License: GPLv2+
Url: http://www.gnu.org/software/bash
Source0: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz.sig
# Official upstream patches
Patch1: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-001
Patch2: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-002
Patch3: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-003
Patch4: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-004
Patch5: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-005
Patch6: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-006
Patch7: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-007
Patch8: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-008
Patch9: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-009
Patch10: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-010
Patch11: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-011
Patch12: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-012
Patch13: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-013
Patch14: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-014
Patch15: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-015
Patch16: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-016
Patch17: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-017
Patch18: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-018
Patch19: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-019
Patch20: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-020
Patch21: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-021
Patch22: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-022
Patch23: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-023
Patch24: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-024
Patch25: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-025
Patch26: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-026
Patch27: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-027
Patch28: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-028
Patch29: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-029
Patch30: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-030
Patch31: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-031
Patch32: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-032
Patch33: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-033
Patch34: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-034
Patch35: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-035
Patch36: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-036
Patch37: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-037
Patch38: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-038
Patch39: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-039
Patch40: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-040
Patch41: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-041
Patch42: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-042
Patch43: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-043
Patch44: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-044
Patch45: ftp://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-045

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: patch

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}, which improves POSIX
compliance over previous versions.

Binaries bash are avaible on 32bit and 64bit

%prep
export PATH=/opt/freeware/bin:$PATH

%setup -q
# Official upstream patches
%patch1 -p0 -b .001
%patch2 -p0 -b .002
%patch3 -p0 -b .003
%patch4 -p0 -b .004
%patch5 -p0 -b .005
%patch6 -p0 -b .006
%patch7 -p0 -b .007
%patch8 -p0 -b .008
%patch9 -p0 -b .009
%patch10 -p0 -b .010
%patch11 -p0 -b .011
%patch12 -p0 -b .012
%patch13 -p0 -b .013
%patch14 -p0 -b .014
%patch15 -p0 -b .015
%patch16 -p0 -b .016
%patch17 -p0 -b .017
%patch18 -p0 -b .018
%patch19 -p0 -b .019
%patch20 -p0 -b .020
%patch21 -p0 -b .021
%patch22 -p0 -b .022
%patch23 -p0 -b .023
%patch24 -p0 -b .024
%patch25 -p0 -b .025
%patch26 -p0 -b .026
%patch27 -p0 -b .027
%patch28 -p0 -b .028
%patch29 -p0 -b .029
%patch30 -p0 -b .030
%patch31 -p0 -b .031
%patch32 -p0 -b .032
%patch33 -p0 -b .033
%patch34 -p0 -b .034
%patch35 -p0 -b .035
%patch36 -p0 -b .036
%patch37 -p0 -b .037
%patch38 -p0 -b .038
%patch39 -p0 -b .039
%patch40 -p0 -b .040
%patch41 -p0 -b .041
%patch42 -p0 -b .042
%patch43 -p0 -b .043
%patch44 -p0 -b .044
%patch45 -p0 -b .045

mkdir ../32bit
mv  * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit

%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-largefile \
    --with-included-gettext
make

cd ../32bit
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-largefile \
    --with-included-gettext
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd 64bit
make DESTDIR=${RPM_BUILD_ROOT} install

mv ${RPM_BUILD_ROOT}/%{_bindir}/bash ${RPM_BUILD_ROOT}/%{_bindir}/bash_64
mv ${RPM_BUILD_ROOT}/%{_bindir}/bashbug ${RPM_BUILD_ROOT}/%{_bindir}/bashbug_64

cd ../32bit
make DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}/%{_bindir}/bash ${RPM_BUILD_ROOT}/%{_bindir}/bash_32
mv ${RPM_BUILD_ROOT}/%{_bindir}/bashbug ${RPM_BUILD_ROOT}/%{_bindir}/bashbug_32


cp doc/builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
ln -sf ..%{_bindir}/bash_32 ${RPM_BUILD_ROOT}/bin/bash_32
ln -sf ../..%{_prefix}/bin/bashbug_32 ${RPM_BUILD_ROOT}/usr/bin/bashbug_32
ln -sf ..%{_bindir}/bash_64 ${RPM_BUILD_ROOT}/bin/bash_64
ln -sf ../..%{_prefix}/bin/bashbug_64 ${RPM_BUILD_ROOT}/usr/bin/bashbug_64

{
  cd ${RPM_BUILD_ROOT}
  cd bin
  ln -sf bash_32 bash2_32
  ln -sf bash_64 bash
  ln -sf bash_64 bash2_64
  cd ../usr/bin
  ln -sf bashbug_32 bash2bug_32
  ln -sf bashbug_32 bash2bug
  ln -sf bashbug_64 bash2bug_64
  cd ../../%{_bindir}
  ln -sf bash_64 bash
  ln -sf bashbug_32 bashbug
}


%post
if [ ! -f /etc/shells ]; then
    echo "%{_bindir}/bash" >> /etc/shells
    echo "%{_bindir}/bash_64" >> /etc/shells
else
    grep -q '^%{_bindir}/bash$' /etc/shells || \
        echo "%{_bindir}/bash" >> /etc/shells
    grep -q '^%{_bindir}/bash_64$' /etc/shells || \
        echo "%{_bindir}/bash_64" >> /etc/shells
fi

echo "\n\t## Binary \"bash\" is avaible on 32bit and 64bit ##\n\n\tThe default used is 64bit\n\n\tPlease change symbolic link \n\tfrom \"bash\" into /bin directory\n\tTo do that tape:\n\t\t# rm -f /bin/bash\n\t\t# ln -sf /opt/freeware/bin/bash_32 /bin/bash"


%postun
if [ ! -x %{_bindir}/bash ]; then
    grep -v '^%{_bindir}/bash$' /etc/shells > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
fi
if [ ! -x %{_bindir}/bash_64 ]; then
    grep -v '^%{_bindir}/bash_64$' /etc/shells > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/COMPAT 32bit/NEWS 32bit/NOTES 32bit/POSIX
%doc 32bit/doc/FAQ 32bit/doc/INTRO 32bit/doc/article.ms 32bit/doc/article.txt
%doc 32bit/examples/obashdb/ 32bit/examples/functions/ 32bit/examples/misc/
%doc 32bit/examples/scripts.noah/ 32bit/examples/scripts.v2/ 32bit/examples/scripts/
%doc 32bit/examples/startup-files/ 32bit/examples/complete/
%{_bindir}/*
%{_infodir}/bash.info*
%{_mandir}/man1/*
%{_datadir}/locale/*/*/*
/bin/bash*
/usr/bin/bash*


%changelog
* Wed Oct 23 2013 Gerard Visiedo <gerard.visiedo@bull.net> 4.2-7
- update to 4.2-7 with all official patches until level 045.

* Tue Oct 30 2012 Gerard Visiedo <gerard.visiedo@bull.net - 4.2-6
- Update to version 4.2 patch level 37
- build binaries on 32bit and 64bit

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

