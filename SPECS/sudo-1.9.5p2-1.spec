# enable tests by default
%bcond_without dotests

# LDAP is enabled by default.
%define LDAP 1

# With 1, this does not create sudo plugins
# It also fixes the issue with configure adding -Wl,-brtl and libtools not creating libsudo_util.a
# With 0: as BullFreeware previous versions
%global sudo_static 0

%define _libdir64 %{_libdir}64

Summary:     Allows restricted root access for specified users.
Name:        sudo
Version:     1.9.5p2
Release:     1
Group:       Applications/System
License:     ISC-style
Source:      https://www.sudo.ws/dist/sudo-%{version}.tar.gz
Source1000:  %{name}-%{version}-%{release}.build.log
URL:         http://www.sudo.ws

%if %{LDAP} == 1
Requires:    openldap >= 2.4.48-2
Requires:    gettext >= 0.20.1
Requires:    zlib >= 1.2.11-3
BuildRequires: openldap-devel >= 2.4.48-3
BuildRequires: sed
BuildRequires: coreutils
BuildRequires: libtool >= 2.4.6-5
BuildRequires: zlib-devel >= 1.2.11-3
%endif

#To fix expired password login issue
Patch1:     sudo-%{version}-exppasswd2-aix.patch
Patch2:     sudo-ldr-preload64-aix.patch

# -brtl is added by the community to generate .so instead of .a.
# But, as we are in a RPM, we can avoid -brtl and simply extract
# them for .a.
Patch3:     sudo-1.9.5p2-aix-remove-brtl-in-configure.patch

# Force libtool to use .exp provided by sudo and not
# generate its own.
Patch4:     sudo-1.8.31-keep_LT_LDEXPORTS_for_aix.patch

%description
Sudo (superuser do) allows a system administrator to give certain users (or
groups of users) the ability to run some (or all) commands as root while
logging all commands and arguments. Sudo operates on a per-command basis.  It
is not a replacement for the shell.  Features include: the ability to restrict
what commands a user may run on a per-host basis, copious logging of each
command (providing a clear audit trail of who did what), a configurable timeout
of the sudo command, and the ability to use the same configuration file
(sudoers) on many different machines.


%prep
%setup -q -n sudo-%{version}
%patch1 -p0
%patch3 -p1
%patch4 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

cd 64bit
%patch2 -p1


%build

export AR="/usr/bin/ar -X32_64"
export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:.

# This option no more exists in version 1.9.5p2
#    --with-authenticate

build_sudo () {
    set -ex
    ./configure \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--mandir=%{_mandir} \
	--sysconfdir=/etc/ \
	--libdir=$1 \
	--libexecdir=$1 \
	--with-logging=syslog \
	--with-logfac=auth \
	--with-pam \
	--with-pam-login \
	--with-env-editor \
	--with-ignore-dot \
	--with-aixauth \
	--with-tty-tickets \
%if %{sudo_static} == 1
        --enable-static-sudoers \
	--disable-shared-libutil \
%endif
%if %{LDAP} == 1
        --with-ldap=/opt/freeware \
	--with-ldap-conf-file=/opt/freeware/etc/openldap/ldap.conf \
	--with-ldap-secret-file=/opt/freeware/etc/openldap/slapd.conf
%endif

    # libexec contains libraries with .a and .so.
    # We cannot easily install both 32 and 64 bits version in this case.
    # We install all libraries on lib and lib64.

    gmake

}

cd 64bit
export CC="gcc -maix64"
export OBJECT_MODE=64
export CFLAGS="-O2 -fstack-check"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64/sudo:/opt/freeware/lib/sudo:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
build_sudo %{_libdir64}

cd ../32bit
export CC="gcc -maix32"
export OBJECT_MODE=32
export CFLAGS="-O2 -fstack-check -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib/sudo:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
build_sudo %{_libdir}


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"
export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:.

install_sudo () {
set -ex
sed -e 's/-o $(sudoers_uid) -g $(sudoers_gid)/ /g' \
    -e 's/-o $(install_uid) -g $(install_gid)/ /g' \
    -e 's/-m 4111//' -e 's/-m 0111//' Makefile > Makefile.$$

mv Makefile.$$ Makefile

(
  cd src/.libs
  ln -fs libsudo_noexec.a sudo_noexec.a
)

export INSTALL_OWNER="-o `id -un` -g `id -gn`"
CFLAGS="$RPM_OPT_FLAGS" \
gmake DESTDIR=${RPM_BUILD_ROOT} install install_uid=`id -u` install_gid=`id -g`

(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv ${fic} ${fic}_$1
    done
    cd ${RPM_BUILD_ROOT}%{_sbindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv ${fic} ${fic}_$1
    done
)
}


cd 64bit
export OBJECT_MODE=64
install_sudo 64

cd ../32bit
export OBJECT_MODE=32
install_sudo 32
# Fix a mess with sudoedit 32bit:
(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    rm sudoedit_32
    ln -s sudo_32 sudoedit_32
)

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for fic in $(ls -1| grep -v -e _32)
  do
    ln -sf ${fic} `basename ${fic} _64`
  done
  cd ${RPM_BUILD_ROOT}%{_sbindir}
  for fic in $(ls -1| grep -v -e _32)
  do
    ln -sf ${fic} `basename ${fic} _64`
  done
)

cd $RPM_BUILD_ROOT
mkdir -p etc/rc.d/rc2.d
ln -s /etc/rc.d/init.d/sudo etc/rc.d/rc2.d/S90sudo

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_sbindir}/* || :

chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/*
/opt/freeware/bin/install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo
rm $RPM_BUILD_ROOT/opt/freeware/lib*/sudo/*.la

(

    # Extract 64bit .so files and creates links for .a files.
    # .so are needed by sudo and must not be removed !
    cd ${RPM_BUILD_ROOT}/%{_libdir64}/sudo
    for fic in *.a; do
	$AR -x -X64 ${fic}
	rm ${fic}
	ln -sf ../../lib/sudo/${fic} ${fic}
    done

    # Extract 32bit .so files and includes 64bit .so in archives
    cd ${RPM_BUILD_ROOT}/%{_libdir}/sudo
    for fic in *.a; do
	$AR -x -X32 ${fic}
	$AR -qc -X64 ${fic} ../../lib64/sudo/*`basename ${fic} .a`.so*
    done


    # Rename libsudo_exec.so into sudo_exec.so, as that's
    # what sudo is expected.
    mv ${RPM_BUILD_ROOT}/%{_libdir}/sudo/libsudo_noexec.so ${RPM_BUILD_ROOT}/%{_libdir}/sudo/sudo_noexec.so
    mv ${RPM_BUILD_ROOT}/%{_libdir64}/sudo/libsudo_noexec.so ${RPM_BUILD_ROOT}/%{_libdir64}/sudo/sudo_noexec.so
)

# %if %{sudo_static} != 1
# # sudoers.so is loaded during execution, so it is needed.
# (
#   cd ${RPM_BUILD_ROOT}%{_libdir}/sudo
#   /usr/bin/ar -X32 -x sudoers.a sudoers.so
#   cd ${RPM_BUILD_ROOT}%{_libdir64}/sudo
#   /usr/bin/ar -X64 -x sudoers.a sudoers.so
# )
# %endif


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
export OBJECT_MODE=64
( gmake -k check || true )
/usr/sbin/slibclean

cd ../32bit
export OBJECT_MODE=32
( gmake -k check || true )
/usr/sbin/slibclean


%clean 
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/INSTALL 32bit/NEWS 32bit/doc/HISTORY 32bit/doc/LICENSE 32bit/README 32bit/README.LDAP 32bit/doc/TROUBLESHOOTING 32bit/doc/UPGRADE
%config(noreplace) %attr(0440,root,system) /etc/sudoers
%config(noreplace) %attr(0640,root,system) /etc/sudo.conf
%attr(0750,root,system) %dir /etc/sudoers.d
%attr(0711,root,system) %dir /var/lib/sudo
%attr(0711,root,system) %dir /var/lib/sudo/lectured
%attr(0700,root,system) %dir /var/run/sudo

%attr(4111,root,system) %{_bindir}/sudo*
%attr(4111,root,system) %{_bindir}/sudoreplay*
%attr(4111,root,system) %{_bindir}/sudoedit*
%attr(0111,root,system) %{_sbindir}/visudo*

# %{_bindir}/sudo*
# %{_bindir}/sudoreplay*
# %{_bindir}/sudoedit*
# %{_sbindir}/visudo*

%{_libdir}/sudo
%{_libdir64}/sudo

/etc/rc.d/init.d/*
/etc/rc.d/rc2.d/*

%{_mandir}/man5/*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%{_includedir}/*


%changelog
* Mon Feb 08 2021 Tony Reix <tony.reix@atos.net> - 1.9.5p2-1
- Merge of Bullfreeware 1.8.31-1 and AIX Toolbox 1.9.5p2-1
- Fix export symbols when -fvisibility=hidden is detected
- Update requirements
- Add /etc/sudo.conf

* Wed Jan 27 2021 Ayappan P <ayappap2@in.ibm.com> - 1.9.5p2-1
- Update to 1.9.5p2 version (contains fix for CVE-2021-3156)

* Mon Sep 07 2020 BaanuTumma  <btumma15@in.ibm.com> - 1.8.31p1-2
- Rebuid to ship files from /opt/freeware/libexec64 directory
- no longer shipping files from /usr/include directory

* Mon May 04 2020 Baanu Tumma <btumma15@in.ibm.com> - 1.8.31p1
- Updated to version 1.8.31p1

* Tue Feb 04 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.8.31-1
- New version 1.8.31
- Bullfreeware OpenSSL removal
- No more provide .so and .la
- No link from /usr
- Build 32 and 64 bit version
- No more use brtl

* Wed Dec 04 2019 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.28-1
- Update to 1.8.28 which includes CVE fix CVE-2019-14287.

* Thu Sep 12 2019 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.27-3
- Rebuild to use newer AIX authentication API.
- Newer API's saves the state information and works better than
- the older API's.

* Fri Jun 07 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.8.27-2
- Rebuild with pam support
- Rebuilt to fix expired login credentials issue 

* Mon Mar 18 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.8.27-1
- Updated to 1.8.27

* Tue Nov 14 2017 Ayappan P <ayappap2@in.ibm.com> 1.8.20p2-4
- Fix rpm_share error messages due to improper symlinks

* Fri Jul 14 2017 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.20p2-3
- Update to include CVE fixes.
- Build with -fstack-check & maxdata.

* Sat Jul 02 2016 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.15-2
- Rebuild with ldap support.

* Thu Mar 17 2016 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.15-1
- Update to 1.8.15

* Tue Apr 7 2015 Sangamesh Mallayya <smallayy@in.ibm.com> 1.8.13-1
- Update to 1.8.13

* Fri Nov 11 2011 Sangamesh Mallayya <smallayy@in.ibm.com> 1.6.9p23
- Update to 1.6.9p23

* Fri Aug 22 2008 Garrick Trowsdale <garrick.trowsdale@telus.com>
- Move BuildRequires: openldap-devel inside conditional block

* Tue Jul 29 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-2noldap
- Create a non-LDAP enabled release.  Build with --define 'noldap 1'.

* Wed Jul  2 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-2
- Change the order of the libpath encoded in the sudo binary.  

* Fri May  2 2008 Reza Arbab <arbab@austin.ibm.com> 1.6.9p15-1
- Update to 1.6.9p15.
- Configure with-ldap and with-noexec.  Require openldap.

* Tue Apr 27 2004 David Clissold <cliss@austin.ibm.com> 1.6.7p5-2
- Make sure /etc/sudoers installs with 0440 permissions.
- Thanks to Leigh Brown (leigh@solinno.co.uk) for pointing this out.

* Wed May 21 2003 David Clissold <cliss@austin.ibm.com> 1.6.7p5-1
- New version, 1.6.7p5.  (Includes earlier security fix; separate
-  patch no longer required).

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Wed Jul 17 2002 David Clissold <cliss@austin.ibm.com>
- New version, 1.6.5p2.  Security patch still required.

* Thu Apr 25 2002 David Clissold <cliss@austin.ibm.com>
- Security patch announced today; added.

* Fri Feb 08 2002 Marc Stephenson <marc@austin.ibm.com>
- New version

* Tue Oct 23 2001 David Clissold <cliss@austin.ibm.com>
- No functional change.  Remove unneccessary libtool use.

* Thu Oct 11 2001 Marc Stephenson <marc@austin.ibm.com>
- Use configure with-authenticate

* Fri Apr 20 2001 Marc Stephenson <marc@austin.ibm.com>
- Build for AIX Toolbox for Linux Distributions

* Mon Mar 5 2001 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.3p7

* Thu Feb 22 2001 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.3p6

* Sat Dec 30 2000 Roger Luethi <rluethi@turbolinux.com>
- 1.6.3p5-2: libtoolized build

* Thu Sep 21 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>
- rewrite spec file for FHS 2.1
- updated to 1.6.3p5
  o Fixed a case where a string was used after it had been freed.
  o Fixed a bug that prevented the -H option from working.
  o Fixed targetpw, rootpw, and runaspw options when used with non-passwd
    file authentication (PAM, etc).
  o When the targetpw flag is set, use the target username as part
    of the timestamp path.
  o The listpw and verifypw options had no effect.

* Mon Jul 17 2000 SL Baur  <steve@turbolinux.co.jp>
- alpha port

* Mon Mar 27 2000 Takeshi Aihana <aihana@turbolinux.co.jp>
- updated to 1.6.3
- patch pathname of libpam

* Sat Mar 25 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>
- update to 1.6.2p3

* Fri Feb 4 2000 Hirofumi Takeda <takepin@turbolinux.co.jp>
- Repackaged for TurboLinux Workstation 6.0J

* Sun Jan 9 2000 Takaaki Tabuchi <tab@kondara.org>
- be able to rebuild non-root user.

* Sun Dec 19 1999 Taichi Nakamura <pdf30044@biglobe.ne.jp>
- update to 1.6.1

* Tue Dec 14 1999 Tenkou N. Hattori <tnh@kondara.org>
- change /etc/sudoers to noreplace.

* Tue Nov 30 1999 Tenkou N. Hattori <tnh@kondara.org>
- updated to 1.6
- be a NoSrc :-P

* Thu Jul 22 1999 Tim Powers <timp@redhat.com>
- updated to 1.5.9p2 for Powertools 6.1

* Wed May 12 1999 Bill Nottingham <notting@redhat.com>
- sudo is configured with pam. There's no pam.d file. Oops.

* Mon Apr 26 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.59p1 for powertools 6.0

* Tue Oct 27 1998 Preston Brown <pbrown@redhat.com>
- fixed so it doesn't find /usr/bin/vi first, but instead /bin/vi (always installed)

* Thu Oct 08 1998 Michael Maher <mike@redhat.com>
- built package for 5.2 

* Mon May 18 1998 Michael Maher	<mike@redhat.com>
- updated SPEC file. 

* Thu Jan 29 1998 Otto Hammersmith <otto@redhat.com>
- updated to 1.5.4

* Tue Nov 18 1997 Otto Hammersmith <otto@redhat.com>
- built for glibc, no problems

* Fri Apr 25 1997 Michael Fulbright <msf@redhat.com>
- Fixed for 4.2 PowerTools 
- Still need to be pamified
- Still need to move stmp file to /var/log

* Mon Feb 17 1997 Michael Fulbright <msf@redhat.com>
- First version for PowerCD.
