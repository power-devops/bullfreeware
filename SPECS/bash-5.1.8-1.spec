# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

%define		_libdir64 %{_prefix}/lib64

Name: bash
Version: 5.1.8
Release: 1
Summary: The GNU Bourne Again shell (bash) version %{version}
Group: System Environment/Shells
License: GPLv3+
Url: http://www.gnu.org/software/bash

Source0: ftp://ftp.gnu.org/gnu/bash/%{name}-%{version}.tar.gz
Source2: %{name}-%{version}-%{release}.build.log

# Locale names for UTF8 for make check on AIX are all capitals, eg EN_US.UTF-8
# This patch can be remove for AIX 7.1+
Patch901: bash-5.1-locale_make_check.patch

# Fix the issue with test -x when root
Patch902: bash-5.1.test-x-root.patch

# Fix linking with shared libraries
Patch903:   %{name}-configure-fix-shrext-for-AIX-without-brtl.patch
Patch904:   %{name}-5.1-configure-fix-disable-rpath.patch

# Some tests use a wrong locale name, or have wrong output for AIX.
Patch905:   %{name}-5.0-test.patch

# Bash coredumps by getting into a loop in readline code if it gets a SIGHUP and terminal already gone
Patch906: bash-5.1-fix-SIGHUP-aix.patch

# Hardcode library search path for libiconv to /opt/freeware/lib/libiconv.a
Patch907: bash-5.1-hardcode-libiconv-linking.patch

# Disable plugin examples.
Patch908: bash-5.1-support-disable-plugin-creation.patch

BuildRequires: libiconv >= 1.16
BuildRequires: texinfo
Requires: libiconv >= 1.16

# We can't distribute /bin/bash in %file anymore as it might erase
# the AIX bash added in 7.3.
# Thus, we manually provide it and install it in %posttrans if needed.
Provides: /usr/bin/bash
Provides: /bin/bash

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification. This
package (bash) contains bash version %{version}.

There are 32bit and 64bit binary versions available for bash

In this release, process substitution is not completely working. The output
of a command might not be redirected correctly when using <(cmd) or >(cmd).


%prep
%if %{with gcc_compiler}
  export PATH=/opt/freeware/bin:$PATH
%endif

%setup -q

%patch901 -p1
%patch902 -p1
%patch903 -p1
%patch904 -p1
%patch905 -p1
%patch906 -p1
%patch907 -p1
%patch908 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export INSTALL=/opt/freeware/bin/install

%if %{with gcc_compiler}
  export PATH=/opt/freeware/bin:$PATH
%endif
export LIBPATH=

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export SIZE="/usr/bin/size -X32_64"
# export CFLAGS=-O2
export CFLAGS=-g


%if %{with gcc_compiler}
export __CC="gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="/opt/IBM/xlc/13.1.3/bin/xlc"
export FLAG32="-q32"
export FLAG64="-q64"
%endif

build_bash(){
	./configure \
		--prefix=%{_prefix} \
		--infodir=%{_infodir} \
		--mandir=%{_mandir} \
		--libdir=$1 \
		--disable-rpath \
		--with-included-gettext \
%if %{with gcc_compiler}
                --with-libiconv-prefix=/opt/freeware/
%else
                --with-libiconv-prefix=/usr/
%endif

	make	
}


cd 64bit
export OBJECT_MODE=64
export CC="$__CC $FLAG64"
%if %{with gcc_compiler}
  export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
%else
  export LDFLAGS="-Wl,-blibpath:/usr/lib:/lib"
%endif
build_bash %{_libdir64}



cd ../32bit
export OBJECT_MODE=32
export CC="$__CC $FLAG32"
export CFLAGS="-D_LARGE_FILES"
%if %{with gcc_compiler}
  export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
%else
  export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/usr/lib:/lib"
%endif
build_bash %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


export INSTALL=/opt/freeware/bin/install
%if %{with gcc_compiler}
  export PATH=/opt/freeware/bin:$PATH
%endif
export LIBPATH=

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export SIZE="/usr/bin/size -X32_64"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 64bit binaries' name
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)

cd ../32bit
make DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 32bit binaries' name and make default link towards 64bit
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in $(ls | grep -v -e _32 -e _64)
	do
		mv ${f} ${f}_32
		ln -sf ${f}_64 ${f}
	done
)


cp doc/builtins.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

%if %{with gcc_compiler}
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
%endif

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

echo "\n\t## Binary \"bash\" is available in 32bit and 64bit ##\n\n\tDefault is 64bit. For 32bit, use /opt/freeware/bin/bash_32\n"

%posttrans
if lslpp -Lc bash.rte  > /dev/null 2>&1;then
    if ! ls -l /bin/bash 2>&1 | grep /usr/opt/bash/bin/bash > /dev/null;then
	ln -sf /usr/opt/bash/bin/bash /bin/bash
    fi
else
    ln -sf ..%{_bindir}/bash /bin/bash
    ln -sf ..%{_bindir}/bash_32 /bin/bash_32
    ln -sf ..%{_bindir}/bash_64 /bin/bash_64
fi

%postun
if [ ! -x %{_bindir}/bash ]; then
    grep -v '^%{_bindir}/bash$' /etc/shells > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
fi
if [ ! -x %{_bindir}/bash_64 ]; then
    grep -v '^%{_bindir}/bash_64$' /etc/shells > /etc/shells.rpm && \
        mv /etc/shells.rpm /etc/shells
fi


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export LIBPATH=

cd 64bit
(make -k check || true)

cd ../32bit
(make -k check || true)

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
%if %{with gcc_compiler}
%{_infodir}/bash.info*
%{_datadir}/locale/*/*/*
%endif
%{_mandir}/man1/*


%changelog
* Thu Sep 30 2021 Clément Chigot <clement.chigot@atos.net> 5.1.8-1
- Update to 5.1.8

* Fri Aug 13 2021 Reshma V Kumar <reskumar@in.ibm.com> - 5.1.4-2
- Rebuild to fix /bin/bash symbolic links

* Thu Apr 22 2021 Clément Chigot <clement.chigot@atos.net> 5.1.4-1
- New version 5.1

* Thu Sep 17 2020 Ayappan P <ayappap2@in.ibm.com> 5.0.18-1
- Fix terminal hangup issue
- Hardcode libiconv library 

* Wed Jul 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 5.0.17-2
- Fix compilation with xlc
- Correct test

* Wed Jul 22 2020 Clément Chigot <clement.chigot@atos.net> 5.0.17-1
- Update to 5.0.17

* Mon Feb 10 2020 Clément Chigot <clement.chigot@atos.net> 5.0.11-1
- Update to 5.0.11
- BullFreeware Mass Rebuild for clean builds
- Build with gcc
- Move tests to %check section
- Fix and add --disable-rpath option to configure

* Wed Mar 06 2019 Tony Reix <tony.reix@atos.net> 4.4-4
- Fix issue with "test -x" when root
- Build with -O2

* Fri Sep 23 2016 Jean Girardet <Jean.Girardet@Atos.net> 4.4-3
- Fix issue with name of version in message

* Thu Sep 22 2016 Jean Girardet <Jean.Girardet@Atos.net> 4.4-2
- Add patchs to version 4.4-2

* Wed Sep 21 2016 Jean Girardet <Jean.Girardet@Atos.net> 4.4-1
- Update to version 4.4-1

* Tue Sep 13 2016 Jean Girardet <Jean.Girardet@Atos.net> 4.3.46-1
- Update to version 4.3.46-1 : Integrate new patchs

* Mon Jul 27 2015 Michael Wilson <michael.wilson@bull.net> 4.3
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

* Tue Sep 14 1999 Dale Lovelace <dale@redhat.com>
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

