Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 3.0
Release: 3
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils
Source: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.gz
Copyright: GPL
Prefix: %{_prefix}
Prereq: /sbin/install-info
Buildroot: /var/tmp/%{name}-root


%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

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
export CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" ./configure --prefix=%{_prefix} 

make PR_PROGRAM=%{_prefix}/bin/pr

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} install

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_prefix}/share/info/diff*
  /usr/bin/strip .%{_prefix}/bin/* || :
  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -sf ../../..%{prefix}/bin/* .
)

%post
/sbin/install-info %{_prefix}/share/info/diff.info.gz %{_prefix}/share/info/dir --entry="* diff: (diff).                 The GNU diff."

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/share/info/diff.info.gz %{_prefix}/share/info/dir --entry="* diff: (diff).                 The GNU diff."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README COPYING
%{_prefix}/bin/*
%{_prefix}/share/info/diff.info*gz
/usr/linux/bin/*


%changelog
* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 3.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 8 2011 Gerard Visiedo <gerard.visiedo@bull.net> 3.0-2
- Compile on toolbox3

* Wed May 26 2010 Jean Noel Cordenner <jea-noel.cordenner@bull.net> 3.0
- Update to version 3.0

* Wed Jun 11 2003 David Clissold <cliss@austin.ibm.com>
- Update to version 2.8.1.

* Wed Mar 26 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM VAC compiler.

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Mon Dec 11 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Set default ownership of files.

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages.

* Mon Apr 19 1999 Jeff Johnson <jbj@redhat.com>
- man pages not in %files.
- but avoid conflict for diff.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Sun Mar 14 1999 Jeff Johnson <jbj@redhat.com>
- add man pages (#831).
- add %configure and Prefix.

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul 14 1998 Bill Kawakami <billk@home.com>
- included the four man pages stolen from Slackware

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun May 03 1998 Cristian Gafton <gafton@redhat.com>
- fixed spec file to reference/use the $RPM_BUILD_ROOT always

* Wed Dec 31 1997 Otto Hammersmith <otto@redhat.com>
- fixed where it looks for 'pr' (/usr/bin, rather than /bin)

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- uses install-info

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
