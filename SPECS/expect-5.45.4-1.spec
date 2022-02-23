# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%global majorver 5.45.4

Summary: A program-script interaction and testing utility
Name: expect
Version: %{majorver}
Release: 1
License: Public Domain
URL: https://core.tcl.tk/expect/index
Source: http://downloads.sourceforge.net/%{name}/%{name}%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log


BuildRequires: gcc tcl-devel tcl-static sed autoconf automake
# BuildRequires: gcc tcl-devel autoconf automake chrpath

# Fedora patches

# Patch0: fixes change log file permissions
Patch0: expect-5.43.0-log_file.patch
# Patch1: fixes install location, change pkgIndex
Patch1: expect-5.43.0-pkgpath.patch
# Patch2: fixes minor man page formatting issue
Patch2: expect-5.45-man-page.patch
# Patch3: fixes segmentation fault during matching characters
Patch3: expect-5.45-match-gt-numchars-segfault.patch
# Patch4: fixes memory leak when using -re, http://sourceforge.net/p/expect/patches/13/
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
# examples patches
# Patch100: changes random function
Patch100: expect-5.32.2-random.patch
# Patch101: fixes bz674184 - mkpasswd fails randomly
Patch101: expect-5.45-mkpasswd-dash.patch
# Patch102: fixes bz703702 - let user know that telnet is needed for
# running some examples
Patch102: expect-5.45-check-telnet.patch
# Patch103: use full path to 'su', it's safer
Patch103: expect-5.45-passmass-su-full-path.patch
# Patch104: rhbz 963889, fixes inaccuracy in mkpasswd man page
Patch104: expect-5.45-mkpasswd-man.patch
# Patch105: Fix error with -Werror=format-security
Patch105: expect-5.45-format-security.patch

# AIX specific patch for tclsh8.6_32 (and tclsh8.6_64 if/when built)
Patch19: expect-5.45.4-tclshpath.patch

%description
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expect and some scripts that use it.

%package devel
Summary: A program-script interaction and testing utility
Requires: expect = %{version}-%{release}

%description devel
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains development files for the expect library.

%package -n expectk
Summary: A program-script interaction and testing utility
Requires: expect = %{version}-%{release}

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

echo "dotests=%{dotests}"

%setup -q -n expect%{version}
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

# AIX specific patch for tclsh8.6_32 (and 64 if/when built)
%patch19 -p1 -b .tclpath

# -pkgpath.patch touch configure.in
aclocal
autoconf
( cd testsuite
  autoconf -I.. )

%build

# Only 32 bit build TBC

export AR="/usr/bin/ar "
export NM="/usr/bin/nm -X32"
export CC="gcc -maix32"
# The tcl package does not include internal headers, so expect looks in BUILD at
#     /opt/freeware/src/packages/BUILD/tcl8.6.8/32bit/
# Should rebuild/repackage tcl as in Fedora
# export CFLAGS="$CFLAGS -I${RPM_BUILD_DIR}/tcl8.5.8/unix"
export LDFLAGS="${LDFLAGS} -Wl,-brtl -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

# %configure --with-tcl=%{_libdir} --with-tk=%{_libdir} --enable-shared \
# 	--with-tclinclude=%{_includedir}/tcl-private/generic

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static \
    --with-tcl=%{_libdir} \
    --with-tk=%{_libdir} \
    --with-tclinclude=/opt/freeware/include


# From previous AIX version ?
#    --with-tclinclude=${RPM_BUILD_DIR}/tcl8.6.8
#    --with-tkinclude=${RPM_BUILD_DIR}/tk8.6.8/generic
#    --with-x

gmake %{?_smp_mflags}


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

gmake test || true


%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar "
export LN="/usr/bin/ln -s"

gmake install DESTDIR="$RPM_BUILD_ROOT"

# move libexpect to the usual/expected libdir
mv "$RPM_BUILD_ROOT"%{tcl_sitearch}/expect%{version}/libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir}

# for linking with -lexpect
ln -s libexpect%{majorver}.so "$RPM_BUILD_ROOT"%{_libdir}/libexpect.so

# Create AIX libexpect.a and a symlink libexpect<major_version>.a
${AR} -q "$RPM_BUILD_ROOT"%{_libdir}/libexpect.a "$RPM_BUILD_ROOT"%{_libdir}/libexpect%{majorver}.so
${LN}  libexpect.a "$RPM_BUILD_ROOT"%{_libdir}/libexpect%{majorver}.a

# remove cryptdir/decryptdir, as AIX has no crypt command (bug 6668).
rm -f "$RPM_BUILD_ROOT"%{_bindir}/{cryptdir,decryptdir}
rm -f "$RPM_BUILD_ROOT"%{_mandir}/man1/{cryptdir,decryptdir}.1*
rm -f "$RPM_BUILD_ROOT"%{_bindir}/autopasswd

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# rename mkpasswd, as it collides with more powerful variant from whois package (bug 1649456)
mv "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect
mv "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd.1 "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
sed -i 's/mkpasswd/mkpasswd-expect/g;s/MKPASSWD/MKPASSWD-EXPECT/g' "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
sed -i 's/mkpasswd/mkpasswd-expect/g' "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect

# AIX links
(
 cd ${RPM_BUILD_ROOT}
 for dir in bin include lib
 do
   mkdir -p usr/${dir}
   cd usr/${dir}
   ln -sf ../..%{_prefix}/${dir}/* .
   cd -
 done

# AIX created a symlink to preserve  /usr/bin/mkpasswd
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf ../../..%{_bindir}/mkpasswd-expect .
 cd -
)


# remove rpath
# Not on AIX chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libexpect%{version}.so


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc FAQ HISTORY NEWS README
%{_bindir}/expect
%{_bindir}/autoexpect
%{_bindir}/dislocate
%{_bindir}/ftp-rfc
%{_bindir}/kibitz
%{_bindir}/lpunlock
%{_bindir}/mkpasswd-expect
%{_bindir}/passmass
%{_bindir}/rftp
%{_bindir}/rlogin-cwd
%{_bindir}/timed-read
%{_bindir}/timed-run
%{_bindir}/unbuffer
%{_bindir}/weather
%{_bindir}/xkibitz
%dir %{tcl_sitearch}/expect%{version}
%{tcl_sitearch}/expect%{version}/pkgIndex.tcl
%{_libdir}/libexpect%{version}.a
%{_libdir}/libexpect.a
%{_libdir}/libexpect%{version}.so
%{_libdir}/libexpect.so
%{_mandir}/man1/autoexpect.1
%{_mandir}/man1/dislocate.1
%{_mandir}/man1/expect.1
%{_mandir}/man1/kibitz.1
%{_mandir}/man1/mkpasswd-expect.1
%{_mandir}/man1/passmass.1
%{_mandir}/man1/unbuffer.1
%{_mandir}/man1/xkibitz.1
# /usr/bin/autoexpect
# /usr/bin/autopasswd
# /usr/bin/dislocate
# /usr/bin/expect
# /usr/bin/ftp-rfc
# /usr/bin/kibitz
# /usr/bin/lpunlock
# /usr/bin/passmass
# /usr/bin/rftp
# /usr/bin/rlogin-cwd
# /usr/bin/timed-read
# /usr/bin/timed-run
# /usr/bin/unbuffer
# /usr/bin/weather
# /usr/bin/xkibitz
# /usr/linux/bin/mkpasswd-expect
# /usr/lib/lib*.so

%files devel
%defattr(-,root,system)
%{_mandir}/man3/libexpect.3*
%{_includedir}/*

%files -n expectk
%defattr(-,root,system)
%{_bindir}/multixterm
%{_bindir}/tknewsbiff
%{_bindir}/tkpasswd
%{_bindir}/xpstat
%{_mandir}/man1/multixterm.1*
%{_mandir}/man1/tknewsbiff.1*
# /usr/bin/multixterm
# /usr/bin/tknewsbiff
# /usr/bin/tkpasswd
# /usr/bin/xpstat

%changelog
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

