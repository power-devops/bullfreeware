Name: bash
Summary: The GNU Bourne Again shell (bash) version %{version}
Version: 4.3.30
Release: 1
Group: System Environment/Shells
License: GPLv3+
Url: http://www.gnu.org/software/bash
Source0: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz.sig

# Official upstream patches


# Other patches
# Locale names for UTF8 for make check on AIX are all capitals, eg EN_US.UTF-8
Patch901: bash-4.3.30-locale_make_check.patch


BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: patch

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}.

There are 32bit and 64bit binary versions available for bash

%prep
export PATH=/opt/freeware/bin:$PATH

%setup -q

# Official upstream patches

# Other patches
# Locale names for UTF8 for make check on AIX are all capitals, eg EN_US.UTF-8
%patch901 -p1 -b .locale_make_check


mkdir ../32bit
mv  * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit

%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export SIZE="/usr/bin/size -X32_64"

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

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

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

echo "\n\t## Binary \"bash\" is avaible in 32bit and 64bit ##\n\n\tThe default used is 64bit\n\n\tPlease change symbolic link \n\tfor \"bash\" in /bin directory\n\tTo do that type:\n\t\t# rm -f /bin/bash\n\t\t# ln -sf /opt/freeware/bin/bash_32 /bin/bash"


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
%doc 32bit/examples/functions/ 32bit/examples/misc/
%doc 32bit/examples/scripts/
%doc 32bit/examples/startup-files/ 32bit/examples/complete/
%doc 32bit/examples/loadables
%{_bindir}/*
%{_infodir}/bash.info*
%{_mandir}/man1/*
%{_datadir}/locale/*/*/*
/bin/bash*
/usr/bin/bash*


%changelog
* Thu Jul 27 2015 Michael Wilson <michael.wilson@bull.net> 4.3
- Update to version 4.3.30

* Tue Sep 30 2014 Gerard Visiedo <gerard.visiedo@bull.net> 4.2-9
- Add patch bash-4.2-50

* Mon Sep 29 2014 Gerard Visiedo <gerard.visiedo@bull.net> 4.2-8
- Patches with Bash shell vulnerability  CVE-2014-6271 and CVE-2014-7169

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

