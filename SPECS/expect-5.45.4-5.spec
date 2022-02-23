# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%{!?tcl_sitearch64: %global tcl_sitearch64 %{_libdir64}/tcl%{tcl_version}}

#%%global majorver 5.45.4

%define _libdir64 %{_prefix}/lib64

Summary: A program-script interaction and testing utility
Name:    expect
Version: 5.45.4
Release: 5
License: Public Domain
URL: https://core.tcl.tk/expect/index
Source: https://sourceforge.net/projects/expect/files/Expect/%{version}/%{name}%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: gcc tcl-devel >= 8.6.10-3 
BuildRequires: tcl-static sed autoconf automake
# BuildRequires: gcc tcl-devel autoconf automake chrpath

Requires: tcl >= 8.6.10-3
Requires: libgcc >= 8.0.0

# Fedora patches

# Patch0: fixes change log file permissions
Patch0: expect-5.45.4-log_file.patch
# Patch1: fixes install location, change pkgIndex
Patch1: expect-5.45.4-pkgpath.patch

# Fedora patches not applied by AIX toolbox

# Patch2: fixes minor man page formatting issue
Patch2: expect-5.45-man-page.patch
# Patch3: fixes segmentation fault during matching characters
Patch3: expect-5.45-match-gt-numchars-segfault.patch
# Patch4: fixes memory leak when using -re, http://sourceforge.net/p/expect/patches/13/
# Beware, just a workaround not validated by upstream!
Patch4: expect-5.45-re-memleak.patch
# Patch5: use vsnprintf instead of vsprintf to avoid buffer overflow
Patch5: expect-5.45-exp-log-buf-overflow.patch
# Patch6: fixes segfaults if Tcl is built with stubs and Expect is used directly
#   from C program rhbz#1091060
Patch6: expect-5.45-segfault-with-stubs.patch

# Patch7: fixes leaked fd, patch by Matej Mužila, rhbz#1001220
# This is a version for AIX which doesn't have F_DUPFD_CLOEXEC.
Patch7: expect-5.45-fix-fd-leak.patch

# Patch8: unificates usage message of expect binary and man page, adds -h flag
Patch8: expect-5.45.4-unification-of-usage-and-man-page.patch
# Patch9: fixes issues detected by static analysis
Patch9: expect-5.45.4-covscan-fixes.patch

# AIX specific patch for tclsh8.6_32, tclsh is 64 bit version by default
# Patch19: expect-5.45.4-tclshpath.patch
# examples patches
# Patch100: changes random function
Patch100: expect-5.45.4-random.patch
# Patch101: fixes bz674184 - mkpasswd fails randomly
Patch101: expect-5.45.4-mkpasswd-dash.patch
# Patch102: fixes bz703702 - let user know that telnet is needed for
# running some examples
Patch102: expect-5.45-check-telnet.patch
# Patch103: use full path to 'su', it's safer
Patch103: expect-5.45-passmass-su-full-path.patch
# Patch104: rhbz 963889, fixes inaccuracy in mkpasswd man page
Patch104: expect-5.45-mkpasswd-man.patch
# Patch105: Fix error with -Werror=format-security
Patch105: expect-5.45-format-security.patch

# Configure does not find correctly /dev/stty if you has redirection
# It thinks it can be read, and it is wrong.
Patch106: expect-5.45.4-configure_stty.patch

Patch107: expect-5.45.4-configure_brtl_bexpall.patch

%description
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expect and some scripts that use it.


%package devel
Summary: A program-script interaction and testing utility
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl-devel >= 8.6.8-3 
Requires: tk-devel >= 8.6.8-3

%description devel
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains development files for the expect library.


%package -n expectk
Summary: A program-script interaction and testing utility
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: tcl >= 8.6.8-3
Requires: tk >= 8.6.8-3

%description -n expectk
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package originally contained expectk and some scripts
that used it. As expectk was removed from upstream tarball
in expect-5.45, now the package contains just these scripts.
Please use tclsh with packages that require Tk and Expect
instead of expectk.

%prep
%setup -q -n %{name}%{version}
export PATH=/opt/freeware/bin:$PATH
# TODO patches
%patch0 -p1 -b .log_file
%patch1 -p1 -b .pkgpath
%patch2 -p1 -b .man-page
%patch3 -p1 -b .match-gt-numchars-segfault
%patch4 -p1 -b .re-memleak
%patch5 -p1 -b .exp-log-buf-overflow
%patch6 -p1 -b .segfault-with-stubs
%patch7 -p1 -b .fifix-x-fd-leak
%patch8 -p1 -b .unification-of-usage-and-man-page
%patch9 -p1 -b .covscan-fixes
# examples fixes
%patch100 -p1 -b .random
%patch101 -p1 -b .mkpasswd-dash
%patch102 -p1 -b .check-telnet
%patch103 -p1 -b .passmass-su-full-path
%patch104 -p1 -b .mkpasswd-man
%patch105 -p0 -b .format-security
%patch106 -p1 -b .stty
%patch107 -p1 -b .brtl_bexpall

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

# 32 and 64 bit builds because there is a libexpect

# The previous tcl package did not include internal headers, so expect looked
# in BUILD at       /opt/freeware/src/packages/BUILD/tcl8.6.8/32bit/
# From 8.6.10 (8.6.8-2) tcl was repackaged as in Fedora and following not req
# export CFLAGS="$CFLAGS -I${RPM_BUILD_DIR}/tcl8.5.8/unix"

build_expect () {
  set -x

  ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=$1 \
    --enable-shared --enable-static \
    --enable-threads \
    --with-tcl=$1 \
    --with-tclinclude=%{_includedir} \
    --with-tkinclude=%{_includedir} \
    --with-x \
    $2

# X and tk not in configure --help
#   --with-tclinclude=%{_includedir}/tcl-private/generic

  gmake %{?_smp_mflags} libexpect.so.%{version}
  ${AR} -qc libexpect.a libexpect.so.%{version}
  gmake %{?_smp_mflags}
}


# First build the 64-bit version
cd 64bit
export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export CC="gcc -maix64"
export OBJECT_MODE=64
# DO NOT put -L here, else, system lib will be used, and not $BUILD lib
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export CFLAGS="$CFLAGS -I%{_includedir}"

build_expect %{_libdir64} --enable-64bit


# Now build the 32-bit version
cd ../32bit
export AR="/usr/bin/ar "
export NM="/usr/bin/nm -X32"
export CC="gcc -maix32"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CFLAGS="$CFLAGS -I%{_includedir}"

build_expect %{_libdir}


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
export OBJECT_MODE=64
gmake test || true
/usr/sbin/slibclean

cd ../32bit
export OBJECT_MODE=32
#By default, tclsh -> tclsh_64 is used, so it conflicts on 32 bits.
/opt/freeware/bin/sed -i 's|/opt/freeware/bin/tclsh8.6|/opt/freeware/bin/tclsh8.6_32|g' Makefile
gmake test || true
/usr/sbin/slibclean


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar"
export LN="/usr/bin/ln -s"

install_expect () {
  set -x

  gmake install DESTDIR="$RPM_BUILD_ROOT"

  cp libexpect.a ${RPM_BUILD_ROOT}$1

  # remove cryptdir/decryptdir, as AIX has no crypt command (bug 6668).
  rm -f ${RPM_BUILD_ROOT}%{_bindir}/*cryptdir
  rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/*cryptdir.1
  rm -f ${RPM_BUILD_ROOT}%{_bindir}/autopasswd

  /usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* ||

  # rename mkpasswd, as it collides with more powerful variant from whois package
  mv "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect
  mv "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd.1 "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
  /opt/freeware/bin/sed -i 's/mkpasswd/mkpasswd-expect/g;s/MKPASSWD/MKPASSWD-EXPECT/g' "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
  /opt/freeware/bin/sed -i 's/mkpasswd/mkpasswd-expect/g' "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect
}

cd 64bit
export OBJECT_MODE=64
install_expect %{_libdir64}

## move libexpect to the usual/expected libdir64 and rename utilities
# mkdir -p "$RPM_BUILD_ROOT"%{_libdir64}
# mv "$RPM_BUILD_ROOT"%{tcl_sitearch64}/expect%{version}/libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir64}

## for linking with -lexpect
# ln -s libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir64}/libexpect.so

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for fic in $(ls -1| grep -v -e _32 -e _64)
  do
    mv ${fic} ${fic}_64
  done
)

# TODO remove in future realese if OK
#ln -s tcl8.6/%{name}%{version}/libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir64}/libexpect%{version}.so
#ln -s libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir64}/libexpect.so


# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
install_expect %{_libdir}

## move libexpect to the usual/expected libdir
#mv "$RPM_BUILD_ROOT"%{tcl_sitearch}/expect%{version}/libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir}

#ln -s tcl8.6/%{name}%{version}/libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libexpect%{version}.so
#ln -s libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libexpect.so

# for linking with -lexpect
#ln -s libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir}/libexpect.so

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for fic in $(ls -1| grep -v -e _32 -e _64)
  do
    mv ${fic} ${fic}_32
    ln -sf ${fic}_64 ${fic}
  done
)

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -X64 -x libexpect.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -X64 -q libexpect.a ${RPM_BUILD_ROOT}%{_libdir64}/libexpect.so.%{version}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libexpect.so.%{version}
  
     # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/libexpect.a libexpect.a
)

## for linking with -lexpect
#ln -s tcl8.6/%{name}%{version}/libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libexpect%{version}.so
#ln -s libexpect%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libexpect.so


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/FAQ 32bit/HISTORY 32bit/NEWS 32bit/README
%{_bindir}/autoexpect*
%{_bindir}/dislocate*
%{_bindir}/expect*
%{_bindir}/ftp-rfc*
%{_bindir}/kibitz*
%{_bindir}/lpunlock*
%{_bindir}/mkpasswd-expect*
%{_bindir}/passmass*
%{_bindir}/rftp*
%{_bindir}/rlogin-cwd*
%{_bindir}/timed-read*
%{_bindir}/timed-run*
%{_bindir}/unbuffer*
%{_bindir}/weather*
%{_bindir}/xkibitz*
%dir %{tcl_sitearch}/expect%{version}
%{tcl_sitearch}/expect%{version}/pkgIndex.tcl
%dir %{tcl_sitearch64}/expect%{version}
%{tcl_sitearch64}/expect%{version}/pkgIndex.tcl
#%{_libdir}/libexpect%{version}.a
%{_libdir}/libexpect.a
#%{_libdir}/libexpect%{version}.so
#%{_libdir}/libexpect.so
#%{_libdir64}/libexpect%{version}.a
%{_libdir64}/libexpect.a
#%{_libdir64}/libexpect%{version}.so
#%{_libdir64}/libexpect.so
%dir %{_libdir}/tcl8.6/%{name}%{version}
%{_libdir}/tcl8.6/%{name}%{version}/*
%dir %{_libdir}64/tcl8.6/%{name}%{version}
%{_libdir}64/tcl8.6/%{name}%{version}/*
%{_mandir}/man1/autoexpect.1
%{_mandir}/man1/dislocate.1
%{_mandir}/man1/expect.1
%{_mandir}/man1/kibitz.1
%{_mandir}/man1/mkpasswd-expect.1
%{_mandir}/man1/passmass.1
%{_mandir}/man1/unbuffer.1
%{_mandir}/man1/xkibitz.1


%files devel
%defattr(-,root,system)
%{_mandir}/man3/libexpect.3*
%{_includedir}/*

%files -n expectk
%defattr(-,root,system)
%{_bindir}/multixterm*
%{_bindir}/tknewsbiff*
%{_bindir}/tkpasswd*
%{_bindir}/xpstat*
%{_mandir}/man1/multixterm.1*
%{_mandir}/man1/tknewsbiff.1*

%changelog
* Mon Nov 09 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 5.45.4-5
- Rebuild 5.45.4

* Thu Nov 05 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 5.45.4-4
- Rebuild with new tcl
- Remove -brtl in specfile
- Remove -bexpall in configure
- Stop providing .so

* Wed Sep 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 5.45.4-3
- Merge with Toolbox specfile

* Tue Jun 30 2020 Michael Wilson <michael.a.wilson@atos.net> - 5.45.4-2
- Add 64 bit build for libexpect and commands
- Set TCLSH_PROG to $(bindir)/tclsh8.6_32 only for 32 bit build, tclsh is 64 bit

* Fri Feb 07 2020 Michael Wilson <michael.a.wilson@atos.net> - 5.45.4-1
- Update to 5.45.4
- Modifications based on Fedora 5.45.4-11.fc32
- Include expect-5.45-fix-fd-leak.patch without using F_DUPFD_CLOEXEC
-      feature F_DUPFD_CLOEXEC implemented in AIX from 1813_72L July 2018
- Build with tcl 8.6.8/10 (test made by dejagnu configure on expect tcl_version)
- Patch required for tclsh8.6 naming  - tclsh8.6_32 & tclsh8.6_64 if/when built
- Add -brtl and -blibpath for libexpect5.45.4.so
- Archive libexpect5.45.4.so in libexpect.a, create symlink libexpect5.45.4.a
- Add -blibpath for /opt/freeware/bin/expect
- Remove symbolic links in /usr

* Thu Jun 09 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 5.44.1.15-1
- Port on Aix5.3 

