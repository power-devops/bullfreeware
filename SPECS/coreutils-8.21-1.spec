Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 8.21
Release: 1
License: GPL
Group:   System Environment/Base
URL:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source2: %{name}-DIR_COLORS
Source3: %{name}-DIR_COLORS.xterm
Source4: %{name}-colorls.sh
Source5: %{name}-colorls.csh
Patch0:  %{name}-%{version}-aix-uname.patch
Patch1:  %{name}-%{version}-aix-configure.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gettext, gmp-devel >= 4.3.2
BuildRequires: make

Requires: /sbin/install-info
Requires: info, gettext, gmp >= 4.3.2

Conflicts: mktemp, coreutils-64bit

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21


%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

These tools are the GNU versions of common useful and popular file and text
utilities which are used for:
- file management
- shell scripts
- modifying text file (spliting, joining, comparing, modifying, ...)

Most of these programs have significant advantages over their Unix
counterparts, such as greater speed, additional options, and fewer arbitrary
limits.


%prep
%setup -q
%patch0
%patch1


%build
# required if you run 'configure' as root user
export FORCE_UNSAFE_CONFIGURE=1

## export CC="cc -qcpluscmt -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CC="/usr/vac/bin/xlc_r -qcpluscmt -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-largefile \
    --enable-nls
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

bzip2 -9f ChangeLog

(
  cd ${RPM_BUILD_ROOT}
  /usr/bin/strip .%{_bindir}/* || :
  gzip --best .%{_infodir}/*info*

  mkdir -p usr/linux/bin
  mkdir -p usr/bin
  cd usr/linux/bin
  ln -sf ../../..%{_bindir}/* .
  cd ../../bin
  for i in dir dircolors vdir tac md5sum pinky seq
  do
     rm ../linux/bin/$i
     ln -sf ../..%{_bindir}/$i .
  done
)

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR_COLORS
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR_COLORS.xterm
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/colorls.sh
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/colorls.csh
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR*
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*


%pre
# We must deinstall these info files since they're merged in
# coreutils.info. else their postun'll be run too late
# and install-info will fail badly because of duplicates
for file in sh-utils textutils fileutils; do
    /sbin/install-info --delete %{_infodir}/$file.info.gz --dir=%{_infodir}/dir &> /dev/null || :
done


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%post
/usr/bin/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
  %{_infodir}/dir.rpmmodify || exit 0
    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc COPYING ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_infodir}/coreutils*
# exclude %{_libdir}/charset.alias as it conflicts with glib2
# %{_libdir}/*
%{_mandir}/man?/*
%{_datadir}/locale/*/*/*
/usr/bin/*
/usr/linux/bin/*


%changelog
* Mon Feb 18 2013 Michael Perzl <michael@perzl.org> - 8.21-1
- updated to version 8.21

* Tue Aug 21 2012 Michael Perzl <michael@perzl.org> - 8.19-1
- updated to version 8.19

* Mon Aug 13 2012 Michael Perzl <michael@perzl.org> - 8.18-1
- updated to version 8.18

* Fri May 11 2012 Michael Perzl <michael@perzl.org> - 8.17-1
- updated to version 8.17

* Mon Mar 26 2012 Michael Perzl <michael@perzl.org> - 8.16-1
- updated to version 8.16

* Fri Jan 13 2012 Michael Perzl <michael@perzl.org> - 8.15-1
- updated to version 8.15

* Thu Oct 13 2011 Michael Perzl <michael@perzl.org> - 8.14-1
- updated to version 8.14

* Thu Sep 08 2011 Michael Perzl <michael@perzl.org> - 8.13-1
- updated to version 8.13

* Tue Apr 26 2011 Michael Perzl <michael@perzl.org> - 8.12-1
- updated to version 8.12

* Fri Apr 01 2011 Michael Perzl <michael@perzl.org> - 8.10-2
- rebuilt to remove wrong dependency on libiconv

* Sat Feb 05 2011 Michael Perzl <michael@perzl.org> - 8.10-1
- updated to version 8.10

* Tue Jan 04 2011 Michael Perzl <michael@perzl.org> - 8.9-1
- updated to version 8.9

* Wed Dec 22 2010 Michael Perzl <michael@perzl.org> - 8.8-1
- updated to version 8.8

* Mon Nov 15 2010 Michael Perzl <michael@perzl.org> - 8.7-1
- updated to version 8.7

* Sat Oct 16 2010 Michael Perzl <michael@perzl.org> - 8.6-1
- updated to version 8.6

* Thu Jul 01 2010 Michael Perzl <michael@perzl.org> - 8.5-2
- removed dependency on gettext >= 0.17

* Sun Apr 25 2010 Michael Perzl <michael@perzl.org> - 8.5-1
- updated to version 8.5

* Fri Jan 15 2010 Michael Perzl <michael@perzl.org> - 8.4-1
- updated to version 8.4

* Fri Jan 08 2010 Michael Perzl <michael@perzl.org> - 8.3-1
- updated to version 8.3

* Mon Dec 14 2009 Michael Perzl <michael@perzl.org> - 8.2-1
- updated to version 8.2

* Fri Nov 20 2009 Michael Perzl <michael@perzl.org> - 8.1-1
- updated to version 8.1

* Tue Nov 17 2009 Michael Perzl <michael@perzl.org> - 7.6-2
- fixed a spec file issue (wrong Conflicts:)

* Wed Sep 23 2009 Michael Perzl <michael@perzl.org> - 7.6-1
- updated to version 7.6

* Mon Sep 07 2009 Michael Perzl <michael@perzl.org> - 7.5-1
- updated to version 7.5

* Wed Jul 15 2009 Michael Perzl <michael@perzl.org> - 7.4-1
- updated to version 7.4

* Mon Jun 23 2008 Michael Perzl <michael@perzl.org> - 6.12-1
- updated to version 6.12

* Wed May 07 2008 Michael Perzl <michael@perzl.org> - 6.11-1
- updated to version 6.11

* Tue Feb 05 2008 Michael Perzl <michael@perzl.org> - 6.10-1
- first version for AIX V5.1 and higher
- slightly based on the original SPEC file from IBM
