%bcond_without dotests

Summary: A GNU file archiving program.
Name: tar
Version: 1.34
Release: 1
License: GPL
Group: Applications/Archiving
Source0: http://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz
Source1: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source100: %{name}-%{version}-%{release}.build.log
URL: http://www.gnu.org/software/tar/
BuildRequires: gettext-devel >= 0.20.1
Requires: /sbin/install-info, info
Requires : gettext >= 0.20.1
Requires : libiconv >= 1.16

%description
The GNU tar program saves many files together into one archive and can restore
individual files (or all of the files) from the archive.  Tar can also be used
to add supplemental files to an archive and to update or list files in the
archive. Tar includes multivolume support, automatic archive
compression/decompression, the ability to perform remote archives and the
ability to perform incremental and full backups.

%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build
# Avoid redefinitions of feof_unlocked & cie macros
export CFLAGS_COMMON="$RPM_OPT_FLAGS -D_STDIO_UNLOCK_CHAR_IO -D_THREAD_SAFE"
export AR="/usr/bin/ar -X32_64"

# we are building this as root
export FORCE_UNSAFE_CONFIGURE=1

# pthread isn't added when building tar binary
export LIBS=-pthread

build_tar () {
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-largefile \
    --disable-silent-rules

gmake %{?_smp_mflags}
}

cd 64bit
export OBJECT_MODE=64

export CC="/opt/freeware/bin/gcc -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export CFLAGS="$CFLAGS_COMMON"
build_tar

cd ../32bit
export OBJECT_MODE=32

export CC="/opt/freeware/bin/gcc -maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
build_tar


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in *
  do
    mv ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in $(ls -1| grep -v -e _32 -e _64)
  do
    mv ${f} ${f}_32
    ln -sf ${f}_64 ${f}
  done
)

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/%{name}*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%check
%if %{with dotests}
cd 64bit
( gmake -k check || true )
cd ../32bit
( gmake -k check || true )
%endif


%post
/sbin/install-info %{_infodir}/tar.info.gz %{_infodir}/dir  || :


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/tar.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 64bit/AUTHORS 64bit/NEWS 64bit/README 64bit/THANKS 64bit/TODO
%{_bindir}/*
%{_infodir}/*
%{_prefix}/share/locale/*/LC_MESSAGES/*


%changelog
* Fri Feb 19 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.34-1
- Update to 1.34

* Mon Feb 08 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.33-1
- Update to 1.33

* Tue Oct 27 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.32-1
- Update to 1.32

* Tue Oct 27 2020 Étienne Guesnet <etienne.guesnet@atos.net> 1.29-2
- Merge with Toolbox specfile
- Update specfile for automated build
- Stop providing link to /usr

* Wed Mar 13 2019 Baanu Tumma <btumma15@in.ibm.com> 1.32-1
- security vulnerabilities update 

* Fri Apr 20 2018 Harshita Jain <harjain9@in.ibm.com> 1.30-1
- Update to version 1.30

* Wed Nov 30 2016 Ravi Hirekurabar <rhirekur@in.ibm.com>  1.29-1
- Update to version  1.29

* Thu Oct 24 2013 Gerard Visiedo <gerard.visiedo@bull.net>  1.27-1
- Update to version  1.27

* Tue Sep 20 2011 Patricia Cugny <patricia.cugny@bull.net>  1.26-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue May 10 2011 Patricia Cugny <patricia.cugny@bull.net> 1.26-1
- Update to version  1.26.

* Mon Jun 22 2009 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.22-1
- Update to version  1.22.

* Mon Jan 26 2009 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.21-1
- Update to version  1.21.

* Wed Aug 23 2006 Reza Arbab <arbab@austin.ibm.com> 1.14-2
- Add patch to fix tar bug #8902.

* Fri Aug 06 2004 David Clissold <cliss@austin.ibm.com> 1.14-1
- Update to version 1.14

* Fri Aug 02 2002 Chris Tysor <cjtysor@us.ibm.com>
- Fix bug where it prints an error when you tar a file owned by nobody
- Now just prints a warning. AIX tar does same thing, but no warning.

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- fix fnmatch build problems

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.13.11.

* Wed Aug 18 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.9.

* Thu Aug 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.6.
- support -y --bzip2 options for bzip2 compression (#2415).

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.13.5.

* Tue Jul 13 1999 Bill Nottingham <notting@redhat.com>
- update to 1.13

* Sat Jun 26 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.12.64014.
- pipe patch corrected for remote tars now merged in.

* Sun Jun 20 1999 Jeff Johnson <jbj@redhat.com>
- update to tar-1.12.64013.
- subtract (and reopen #2415) bzip2 support using -y.
- move gtar to /bin.

* Tue Jun 15 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to tar-1.12.64011 to
-   add bzip2 support (#2415)
-   fix filename bug (#3479)

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- fix suspended tar with compression over pipe produces error (#390).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Michael Maher <mike@redhat.com>
- added patch for bad name cache.
- FIXES BUG 320

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/gtar symlink (change #421)

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump.
- Turn on nls.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.11.8 to 1.12
- various spec file cleanups
- /sbin/install-info support

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu May 29 1997 Michael Fulbright <msf@redhat.com>
- Fixed to include rmt
