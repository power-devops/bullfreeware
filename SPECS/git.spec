Summary: A set of GNU Interactive Tools.
Name: git
Version: 4.3.20
Release: 4
Copyright: GNU
Group: Applications/File
Source: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
URL: http://www.gnu.org/software/git
Buildroot: /var/tmp/git-root
Prefix: %{_prefix}
Prereq: /sbin/install-info
%define DEFCC cc

%description
GIT (GNU Interactive Tools) provides an extensible file system
browser, an ASCII/hexadecimal file viewer, a process viewer/killer and
other related utilities and shell scripts.  GIT can be used to
increase the speed and efficiency of copying and moving files and
directories, invoking editors, compressing and uncompressing files,
creating and expanding archives, compiling programs, and sending mail.
GIT uses standard ANSI color sequences, if they are available.

You should install the git package if you are interested in using its
file management capabilities.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

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
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS="-D_GNU_SOURCE $RPM_OPT_FLAGS"

LDFLAGS='-s' ./configure --prefix=%{prefix} \
	--with-terminfo
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix}/ install-strip
gzip -9nf $RPM_BUILD_ROOT%{prefix}/info/git.info*


(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/* .
 cd -
 mkdir -p usr/share
 cd usr/share
 ln -s ../..%{prefix}/share/git .
)

%files
%defattr(-,root,system)
%doc COPYING ChangeLog LSM NEWS PLATFORMS PROBLEMS README INSTALL
%{prefix}/bin/*
%{prefix}/info/git*
%dir %{prefix}/share/git
%{prefix}/share/git/.gitrc*
%{prefix}/man/man1/*
/usr/bin/*
/usr/share/git
%docdir %{prefix}/lib/git/html

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{prefix}/info/git.info.gz %{prefix}/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{prefix}/info/git.info.gz %{prefix}/info/dir
fi

%changelog
* Fri Feb 27 2004 David Clissold <cliss@austin.ibm.com>  4.3.20-4
- %defattr was missing from %files.

* Wed Feb 25 2004 David Clissold <cliss@austin.ibm.com>  4.3.20-3
- Remove link to nowhere; make /usr/share/git link to /opt/freeware/share/git
- Rebuild with IBM VAC compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Fri Feb  4 2000 Matt Wilson <msw@redhat.com>
- only get /usr/info/get* to avoid pulling in dir

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- version 4.3.19
- man pages are compressed

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- Fixed the dumb requirement for /usr/lib/git/term

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.3.17

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot to spec file; added the path-correction patch
- added info file handling

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- built against readline library w/ proper soname

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 4.3.16

