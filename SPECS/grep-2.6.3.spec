Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.6.3
Release: 1
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep//grep-%{version}.tar.gz
Patch0: grep-%{version}_kwset_def_xmalloc.patch
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

# may be integrated in future release
# make kwset's obstack use xmalloc, not malloc
%patch0 -p1 

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
make LDFLAGS=-s prefix=${RPM_BUILD_ROOT}%{_prefix} \
	 exec_prefix=${RPM_BUILD_ROOT}%{prefix} \
	 infodir=${RPM_BUILD_ROOT}%{prefix}/info \
	 mandir=${RPM_BUILD_ROOT}%{prefix}/man \
	 install
gzip -9f $RPM_BUILD_ROOT%{prefix}/info/grep*

(cd $RPM_BUILD_ROOT
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    ln -sf ../../..%{_prefix}/bin/* .
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info --quiet --info-dir=%{_prefix}/info %{_prefix}/info/grep.info.gz

%preun
if [ $1 = 0 ]; then
        /sbin/install-info --quiet --info-dir=%{_prefix}/info --delete %{_prefix}/info/grep.info.gz
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README COPYING ChangeLog

%{_prefix}/bin/*
/usr/linux/bin/*
%{_prefix}/info/*.info.gz
%{_prefix}/man/*/*
%{_prefix}/share/locale/*/*/grep.*

%changelog
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
