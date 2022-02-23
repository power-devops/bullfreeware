# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler


%define		_libdir64 %{_prefix}/lib64

Summary: The GNU core utilities: a set of tools commonly used in shell scripts
Name:    coreutils
Version: 8.31
Release: 1
License: GPL
Group:   System Environment/Base
URL:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source2: %{name}-DIR_COLORS
Source3: %{name}-DIR_COLORS.xterm
Source4: %{name}-colorls.sh
Source5: %{name}-colorls.csh

Source1000:	%{name}-%{version}-%{release}.build.log

Patch0:  %{name}-%{version}-aix-uname.patch

# Fix linking with shared libraries
Patch1:   %{name}-%{version}-configure-fix-shrext-for-AIX-without-brtl.patch
Patch2:   %{name}-%{version}-configure-fix-disable-rpath.patch

# In 32bit with -Wl,-bmaxdata, configure programs about getline and getdelim will succeed
# even if they should and must fail. Therefore, this patch force the use of GNU provided
# getline and getdelim.
Patch3:     %{name}-%{version}-configure-force-GNU-getline-and-getdelim.patch


BuildRequires: gettext-devel, gmp-devel >= 4.3.2
# To create info.gz
BuildRequires: gzip
BuildRequires: make

Requires: /sbin/install-info
Requires: info, gmp >= 4.3.2
Requires: gettext >= 0.19.7
Requires: libiconv >= 1.14

# Texinfo perl packages are not installed in default perl library dirs
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$

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


%prep
%setup -q
%patch0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_BASE="-O2  -D_FILE_OFFSET_BITS=64"

%if %{with gcc_compiler}
export __CC="gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"
export CFLAGS_BASE="$CFLAGS_BASE -qcpluscmt -D_FILE_OFFSET_BITS=64"

%endif


build_coreutils() {
	./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--infodir=%{_infodir} \
		--libdir=$1 \
		--enable-largefile \
		--disable-rpath

	gmake %{?_smp_mflags}
}


cd 64bit
export OBJECT_MODE=64
# required if you run 'configure' as root user
export FORCE_UNSAFE_CONFIGURE=1
export CC="$__CC $FLAG64"
export CFLAGS="$CFLAGS_BASE"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_coreutils %{_libdir64}

cd ../32bit
export OBJECT_MODE=32
export CC="$__CC $FLAG32"
export CFLAGS="$CFLAGS_BASE -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
# Allow time_t to be on 32bit.
export TIME_T_32_BIT_OK=yes

build_coreutils %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_prefix}/bin/* 2>/dev/null || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*


mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR_COLORS
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR_COLORS.xterm
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/colorls.sh
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/colorls.csh
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/DIR*
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
export OBJECT_MODE=64
(gmake -k check || true)

cd ../32bit
export OBJECT_MODE=32
(gmake --trace -k check || true)



%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_prefix}/info/coreutils.info.gz %{_prefix}/info/dir
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/COPYING 32bit/ABOUT-NLS 32bit/ChangeLog 32bit/NEWS 32bit/README 32bit/THANKS 32bit/TODO
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_bindir}/*
%{_infodir}/coreutils*
# exclude %{_libdir}/charset.alias as it conflicts with glib2
# %{_libdir}/*
%{_infodir}/*info*
%{_mandir}/man?/*
%{_datadir}/locale/*/*/*


%changelog
* Mon Apr 6 2020 Clement Chigot <clement.chigot@atos.net> - 8.31-1
- BullFreeware Compatibility Improvements
- Move tests to %check section
- Remove /usr links

* Wed Jan 16 2019 Ayappan P <ayappap2@in.ibm.com> - 8.29-3
- Fix for an issue in AIX --> http://bugs.gnu.org/33946

* Fri Aug 03 2018 Harshita Jain<harjain9@in.ibm.com>- 8.29-1
- rebuild to fix the issue with /usr/bin/dirname

* Fri Apr 13 2018 Harshita Jain<harjain9@in.ibm.com> -8.29-1
- Updated to version 8.29

* Mon Apr 04 2016 Ravi Hirekurabar <rhirekur@in.ibm.com> -8.25-1
- updated to version 8.25
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
