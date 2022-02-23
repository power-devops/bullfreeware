# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 3.7
Release: 1
License: GPLv3+
Group: Applications/Text
Source0: https://ftp.gnu.org/gnu/grep/grep-%{version}.tar.xz
Source1000: %{name}-%{version}-%{release}.build.log
URL: http://www.gnu.org/software/grep

BuildRequires: texinfo
BuildRequires: gettext-devel

Patch1: %{name}-3.8-gnulib-tests-remove-freezeing-test-sigsegv-catch-sta.patch


%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.


%prep
%setup -q
%patch1 -p1

%build

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export OBJECT_MODE=64
export CC="gcc -maix64"
export CFLAGS=$RPM_OPT_FLAGS

./configure \
    --prefix=%{_prefix}		\
    --infodir=%{_infodir}	\
    --mandir=%{_mandir}

make


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

make DESTDIR=${RPM_BUILD_ROOT} install

cd $RPM_BUILD_ROOT%{_prefix}

# Strip all of the executables
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :

gzip -9fn ${RPM_BUILD_ROOT}/%{_infodir}/%{name}.info*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

(make -k check || true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-,root,system,-)
%doc AUTHORS THANKS TODO NEWS README
%{_bindir}/*
%{_infodir}/*.info.gz
%{_mandir}/*
%{_datadir}/*

%changelog
* Sat Aug 21 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 3.7-1
- Update to 3.7

* Tue May 25 2021 Clement Chigot <clement.chigot@atos.net> 3.6-1
- Update to version 3.6
- BullFreeware Compatibility Improvements
- Rebuild in 64bit only
- Rebuild with RPMv4

* Wed Jun 28 2017 Daniele Silvestre <daniele.silvestre@atos.net> 3.0-1
- Update to 3.0
- Add texinfo BuildRequires
- Add pkg-config BuildRequires
- remove useless --disable-perl-regexp option in configure => 9 additional succesful PCRE tests

* Tue Nov 22 2016 Jean Girardet <jean.girardet@atos.net> 2.26-2
- Correction of links for binary files

* Tue Nov 15 2016 Jean Girardet <jean.girardet@atos.net> 2.26-1
- Third port on AIX 6.1 , add the 64 bits version

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
