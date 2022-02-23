Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 3.1.3
Release: 1
Copyright: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/gawk
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Source2: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-doc.tar.gz
Prefix: %{_prefix}
Prereq: /sbin/install-info
BuildRoot: /var/tmp/%{name}-root
%define DEFCC cc

%description
The gawk package contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard tool for processing text.

%prep
%setup -q -b 1 -b 2 

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
export CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=${RPM_BUILD_ROOT}%{_prefix}
/usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{prefix}/libexec/awk/* || :

(cd $RPM_BUILD_ROOT
  rm -f .%{_prefix}/info/dir
  gzip -9nf .%{_prefix}/info/gawk.info*
  gzip -9nf .%{_prefix}/info/gawkinet.info*

 for dir in bin lib share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done

 rm usr/bin/awk
 mkdir -p usr/linux/bin
 ln -sf ../../..%{_prefix}/bin/awk usr/linux/bin
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/info/gawk.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/gawkinet.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/gawk.info.gz %{_prefix}/info/dir
   /sbin/install-info --delete %{_prefix}/info/gawkinet.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS PROBLEMS
%doc README COPYING FUTURES INSTALL LIMITATIONS NEWS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps doc/*.dvi
%dir %{_prefix}/share/awk
%dir %{_prefix}/libexec/awk
%{_prefix}/bin/*
%{_prefix}/man/man1/*
%{_prefix}/info/gawk*.info*
%{_prefix}/libexec/awk/*
%{_prefix}/share/awk/*
%{_prefix}/share/locale/*/LC_MESSAGES/*
/usr/bin/*
/usr/linux/bin/*
/usr/share/awk

%changelog
* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 3.1.3-1
- Update to version 3.1.3

* Thu Aug 15 2002 David Clissold <cliss@austin.ibm.com>
- packaging bug with libexec dir; symlinking to nowhere. Rel 2

* Wed Jun 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 3.1.0

* Thu Apr 19 2001 David Clissold <cliss@austin.ibm.com>
- Binaries weren't being stripped correctly

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Use default compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix man page symlinks
- Fix description
- Fix download URL

* Wed Jun 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.0.4.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

