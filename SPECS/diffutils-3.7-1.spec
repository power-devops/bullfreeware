# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A GNU collection of diff utilities.
Name: diffutils
Version: 3.7
Release: 1
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils
License: GPLv3+

Source0: http://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz
Source1000:	%{name}-%{version}-%{release}.build.log

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

export AR="/usr/bin/ar -X32_64"
export CC="gcc -maix64"
export CFLAGS=$RPM_OPT_FLAGS

./configure \
    --prefix=%{_prefix}		\
    --infodir=%{_infodir}	\
    --mandir=%{_mandir}

make PR_PROGRAM=%{_bindir}/pr

%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

# Strip all of the executables
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :

gzip -9fn ${RPM_BUILD_ROOT}/%{_infodir}/diffutils.info*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

(make -k check || true)

%post
/sbin/install-info %{_infodir}/diffutils.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/diffutils.info.gz %{_infodir}/dir --entry="* diff: (diff).                 The GNU diff."
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc NEWS README COPYING
%{_bindir}/*
%{_mandir}/*
%{_infodir}/diffutils.info*gz



%changelog
* Thu May 20 2021 Clément Chigot <clement.chigot@atos.net> 3.7-1
- Update to version 3.7
- Rebuild in 64bit
- Rebuild with RPMv4

* Mon Jan 18 2016 Tony Reix <tony.reix@atos.net> 3.3-1
- Initial port on AIX 6.1

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 3.0-4
- Initial port on aix6.1

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
