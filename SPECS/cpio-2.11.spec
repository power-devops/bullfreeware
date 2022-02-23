Summary: A GNU archiving program.
Name: cpio
Version: 2.11
Release: 1
Copyright: GPL
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.gz
Patch1: cpio-2.11-replace_gnulibstat.patch
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot:  /var/tmp/%{name}-root
%define DEFCC xlc

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1 -p1 -b .gnulib

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
export CFLAGS=$RPM_OPT_FLAGS

CPPFLAGS="-I%{_prefix}/include" \
LDFLAGS="-L%{_prefix}/lib" \
CFLAGS="-O2" \
./configure  --prefix=%{_prefix}
make 

%install
rm -rf $RPM_BUILD_ROOT

touch %{_builddir}/%{name}-%{version}/lib/Makefile
make prefix=${RPM_BUILD_ROOT}%{_prefix} \
    localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
        install

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_prefix}/share/info/cpio.*

  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -s ../../..%{_prefix}/bin/cpio . 
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/cpio.info.gz %{_prefix}/share/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/share/info/cpio.info.gz %{_prefix}/share/info/dir
fi

%files
%defattr(-,root,system)
/usr/linux/bin/*
%doc README NEWS COPYING INSTALL THANKS TODO ABOUT-NLS AUTHORS
%ifos linux
/bin/cpio
#/bin/mt
%{_prefix}/man/man1/cpio.*
%else
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*
%endif
%{_prefix}/share/info/cpio.*
%{_prefix}/share/locale/*/LC_MESSAGES/*

%changelog
* Fri Apr 23 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.11
- Update to 2.11

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 2.5-1
- Update to 2.5

* Wed Mar 26 2003 David Clissold <cliss@austin.ibm.com> 2.4.2-19
- Build with the IBM VAC compiler.

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- missing defattr.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 17 1999 Jeff Johnson <jbj@redhat.com>
- revert the stdout patch (#3358), restoring original GNU cpio behavior
  (#6376, #7538), the patch was dumb.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- fix infinite loop unpacking empty files with hard links (#4208).
- stdout should contain progress information (#3358).

* Sun Mar 21 1999 Crstian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
