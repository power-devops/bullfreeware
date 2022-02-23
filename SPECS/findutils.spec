Summary: The GNU versions of find utilities (find and xargs).
Name: findutils
Version: 4.1
Release: 3
Copyright: GPL
Group: Applications/File
Source0: ftp://ftp.gnu.org/gnu/findutils/findutils-%{version}.tar.gz
URL: http://www.gnu.org/software/findutils
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/tmp/findutils-root

%define DEFCC cc

%description
The findutils package contains programs which will help you locate
files on your system.  The find utility searches through a hierarchy
of directories looking for files which match a certain set of criteria
(such as a filename pattern).  The xargs utility builds and executes
command lines from standard input arguments (usually lists of file
names generated by the find command).

You should install findutils because it includes tools that are very
useful for finding things on your system.

%prep
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
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

./configure --prefix=%{_prefix}
make CFLAGS="$CFLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
./configure --prefix=${RPM_BUILD_ROOT}%{_prefix}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/findutils
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

(   cd $RPM_BUILD_ROOT
    gzip -9fn .%{_prefix}/info/find.info*
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    ln -sf ../../..%{prefix}/bin/* .
    cd -
    mkdir -p usr/bin
    cd usr/bin
    for f in locate updatedb 
    do
      ln -sf ../..%{prefix}/bin/$f .
    done
)

%post
/sbin/install-info %{_prefix}/info/find.info.gz %{_prefix}/info/dir
if [ ! -d  /usr/libexec ]
then
   ln -sf %{_prefix}/libexec /usr/libexec
fi

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/find.info.gz %{_prefix}/info/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README COPYING
/usr/bin/*
/usr/linux/bin/*
%{_prefix}/bin/find
%{_prefix}/bin/locate
%{_prefix}/bin/updatedb
%{_prefix}/bin/xargs
%{_prefix}/libexec/*
%{_prefix}/man/man1/find.1*
%{_prefix}/man/man1/xargs.1*
%{_prefix}/info/find.info*

%changelog
* Thu Jul 10 2003 David Clissold <cliss@austin.ibm.com>
- Switch to the IBM VAC compiler for performance and size.

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix summary
- ma  pages are compressed

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- new description.

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- fixed block count bug (# 2141)

* Mon Mar 29 1999 Preston Brown <pbrown@redhat.com>
- patch to fix xargs out of bounds overflow (bug # 1279)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 30)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- remove further updatedb remnants (#1072).

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- added patch for glibc21

* Mon Nov 16 1998 Erik Troan <ewt@redhat.com>
- removed locate stuff (as we now ship slocate)

* Wed Jun 10 1998 Erik Troan <ewt@redhat.com>
- updated updatedb cron script to not look for $TMPNAME.n (which was
  a relic anyway)
- added -b parameters to all of the patches

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Mar 09 1998 Michael K. Johnson <johnsonm@redhat.com>
- make updatedb.cron use mktemp correctly
- make updatedb use mktemp

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- nobody should own tmpfile
- ignore /net

* Wed Nov 05 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron do a better job of cleaning up after itself.

* Tue Oct 28 1997 Donald Barnes <djb@redhat.com>
- fixed 64 bit-ism in getline.c, patch tacked on to end of glibc one

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- added patch for glibc 2.1

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot support

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>
- made updatedb.cron work even if "nobody" can't read /root
- use mktemp in updatedb.cron

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added missing info pages
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built with glibc

* Mon Apr 21 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed updatedb.cron