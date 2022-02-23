Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.22
Release: 2
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep//grep-%{version}.tar.gz
Patch0: %{name}-%{version}-en_US.UTF-8_tests.patch
Patch1: %{name}-%{version}-en_US.UTF-8_others.patch
URL: http://www.gnu.org/software/grep
Prefix: %{_prefix}
Prereq: /sbin/install-info
Buildroot: /var/tmp/grep-root

%define DEFCC cc

%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%prep
%setup -q
# These 2 patches are designed for handling en_US.UTF8 which is EN_US.UTF8 on AIX
# Patches are not applied since it makes (only) 1 test fail (surrogate-pair) in tests directory
#  (same result for gnulib-tests directory)
# Without patches:
 # TOTAL: 95
 # PASS:  53
 # SKIP:  41
 # XFAIL: 1
 # FAIL:  0
# With patches:
 # TOTAL: 95
 # PASS:  70
 # SKIP:  22
 # XFAIL: 2
 # FAIL:  1 surrogate-pair
#%patch0 -p1 -b .en_US.UTF-8_tests
#%patch1 -p1 -b .en_US.UTF-8_others

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s \
  ./configure --prefix=%{_prefix} --disable-perl-regexp
make CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s

%install
rm -rf ${RPM_BUILD_ROOT}

# Files grep.info.gz and man1 are built at:
#	 $RPM_BUILD_ROOT%{prefix}/share
# though our grep-2.6.3-4.spec file expects them at:
#	 $RPM_BUILD_ROOT%{prefix}/
# Don't know why.
# Anyway, IBM grep-2.20-1.spec expects them at .../share .
# So do I now. Adding /share before /info and /man here below.

make LDFLAGS=-s DESTDIR=${RPM_BUILD_ROOT} \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}%{prefix} \
	infodir=${RPM_BUILD_ROOT}%{prefix}/info \
	mandir=${RPM_BUILD_ROOT}%{prefix}/man \
	install

#echo $RPM_BUILD_ROOT%{prefix}/share/info/grep*
gzip -9f $RPM_BUILD_ROOT%{prefix}/share/info/grep*

(cd $RPM_BUILD_ROOT
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    ln -sf ../../..%{_prefix}/bin/* .
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info --quiet --info-dir=%{_prefix}/info %{_prefix}/share/info/grep.info.gz

%preun
if [ $1 = 0 ]; then
        /sbin/install-info --quiet --info-dir=%{_prefix}/share/info --delete %{_prefix}/share/info/grep.info.gz
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README COPYING ChangeLog

%{_prefix}/bin/*
/usr/linux/bin/*
%{_prefix}/share/info/*.info.gz
%{_prefix}/share/man/*/*
%{_prefix}/share/locale/*/*/grep.*

%changelog
* Fri Jan 08 2016 Tony Reix <tony.reix@bull.net> 2.22-2
- Second port on AIX 6.1

* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.3-4
- Initial port on Aix6.1

* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 2.6.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.3-2
- Compile on toolbox3

* Fri May 28 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.6.3
- Update to 2.6.3

* Wed May 07 2003 David Clissold <cliss@austin.ibm.com>
- Update to 2.5.1.
- Patch from last entry now in main code, so not needed.

* Fri Jul 06 2001 David Clissold <cliss@austin.ibm.com>
- Add patch to fix problem with "grep -r" not working.

* Tue Apr 10 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix path to install-info in preun

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb 03 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- gzip info pages (Bug #9035)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.4.

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- prereq install-info

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %post/%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
