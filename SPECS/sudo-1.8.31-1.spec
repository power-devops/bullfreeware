# enable tests by default
%bcond_without dotests

# LDAP is enabled by default. 
%define LDAP 1

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

%define _libdir64 %{_libdir}64

Summary:     Allows restricted root access for specified users.
Name:        sudo
Version:     1.8.31
Release:     1
Group:       Applications/System
License:     ISC-style
Source:      http://www.sudo.ws/sudo/dist/sudo-%{version}.tar.gz
Source100:   %{name}-%{version}-%{release}.build.log
URL:         http://www.sudo.ws

%if %{LDAP} == 1
Requires:    openldap >= 2.4.48-3
Requires:    gettext >= 0.19.7-1
BuildRequires: openldap-devel >= 2.4.48-3
BuildRequires: sed
BuildRequires: coreutils
BuildRequires: libtool >= 2.4.6-3
%endif

Patch1:     sudo-1.8.28-exppasswd2-aix.patch

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

%if %{without ibm_SSL}
###############################################
# for linking with openssl archive (not soname)
###############################################
if [ -f %{_libdir}/libcrypto.so ]; then
    mv %{_libdir}/libcrypto.so /tmp/libcrypto.so.32
fi
if [ -f %{_libdir}/libssl.so ]; then
    mv %{_libdir}/libssl.so /tmp/libssl.so.32
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{libdir64}/libcrypto.so /tmp/libcrypto.so.64
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{libdir64}/libssl.so /tmp/libssl.so.64
fi
%endif

export AR=/usr/bin/ar

export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:.
# # Strangely, build does not work when $RM is set to /usr/bin/rm
# # (which is set when using /usr/bin/rpm), but works fine when RM
# # is not set and /usr/bin is first in the PATH
# unset RM
# # Use the default compiler for this platform - gcc otherwise
# if [[ -z "$CC" ]]
# then
#     if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
#        export CC=%{DEFCC}
#     else 
#        export CC=gcc
#     fi
# fi
# if [[ "$CC" != "gcc" ]]
# then
#        export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
# fi

build_sudo () {
set -ex
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc/ \
    --libexecdir=$1 \
    --with-logging=syslog \
    --with-logfac=auth \
    --without-pam \
    --with-env-editor \
    --with-ignore-dot \
    --with-authenticate \
    --with-tty-tickets \
    --with-libtool=/opt/freeware/bin/libtool.gcc.$2 \
%if %{LDAP} == 1
    --with-ldap=/opt/freeware \
    --with-ldap-conf-file=/opt/freeware/etc/openldap/ldap.conf \
    --with-ldap-secret-file=/opt/freeware/etc/openldap/slapd.conf
%endif
# libexec contains libraries with .a and .so.
# We cannot easily install both 32 and 64 bits version in this case.
# We install all libraries on lib and lib64.

# Clean brtl flag
find . -name Makefile | xargs sed -i 's|-Wl,-brtl||g' 

gmake

#They have put /opt/freeware/lib at the back of the libpath.  Bad.
#perl -pi -e 's|-Wl,-blibpath:/usr/lib:/lib:/opt/freeware/lib|-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib|g' Makefile

}

cd 64bit
export CC="gcc -maix64"
export OBJECT_MODE=64
export CFLAGS="-O2 -fstack-check"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/libexec/sudo:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
build_sudo %{_libdir64} 64

cd ../32bit
export CC="gcc -maix32"
export OBJECT_MODE=32
export CFLAGS="-O2 -fstack-check"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/libexec/sudo:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
build_sudo %{_libdir} 32


%if %{without ibm_SSL}
##################################################################
# revert previous move - linking with openssl archive (not soname)
##################################################################

if [ -f /tmp/libcrypto.so.32 ]; then
    mv /tmp/libcrypto.so.32 %{_libdir}/libcrypto.so
fi
if [ -f /tmp/libssl.so.32 ]; then
    mv /tmp/libssl.so.32 %{_libdir}/libssl.so
fi
if [ -f /tmp/libcrypto.so.64 ]; then
    mv /tmp/libcrypto.so.64 %{libdir64}/libcrypto.so
fi
if [ -f /tmp/libssl.so.64 ]; then
    mv /tmp/libssl.so.64 %{libdir64}/libssl.so
fi
%endif


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export PATH=/opt/freeware/bin:/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export AR="/usr/bin/ar -X32_64"

# # Strangely, build does not work when $RM is set to /usr/bin/rm
# # (which is set when using /usr/bin/rpm), but works fine when RM
# # is not set and /usr/bin is first in the PATH
# unset RM
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

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
gmake DESTDIR=${RPM_BUILD_ROOT} install

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
install_sudo 64

cd ../32bit
install_sudo 32

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

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/* 

#install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo
/opt/freeware/bin/install -d -m 700 $RPM_BUILD_ROOT/var/run/sudo
rm $RPM_BUILD_ROOT/opt/freeware/lib*/sudo/*.la

(
  cd ${RPM_BUILD_ROOT}/%{_libdir}/sudo
  for fic in `find . -name "*.a"`
  do
    # libsudo_util.a contains libsudo_util.so.0,
    # sudo_noexec.a contains libsudo_noexec.so,
    # other contain NAME.so
    ( $AR -x  ../../lib64/sudo/${fic} `basename ${fic} .a`.so    || true )
    ( $AR -x  ../../lib64/sudo/${fic} `basename ${fic} .a`.so.0  || true )
    ( $AR -x  ../../lib64/sudo/${fic} lib`basename ${fic} .a`.so || true )
      $AR -qc                  ${fic} *`basename ${fic} .a`.so*
  done
  
  cd ../../lib64/sudo
  for fic in `find . -name "*.a"`
  do
    rm ${fic}
    ln -sf    ../../lib/sudo/${fic}   ${fic}
  done
)

# sudoers.so is loaded during execution, so it is needed.
(
  cd ${RPM_BUILD_ROOT}%{_libdir}/sudo
  /usr/bin/ar -X32 -x sudoers.a sudoers.so
  cd ../../lib64/sudo
  /usr/bin/ar -X64 -x sudoers.a sudoers.so
)


%check
# export LIBPATH=/opt/freeware/lib:/usr/lib
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
( make -k check || true )
cd ../32bit
export OBJECT_MODE=32
( make -k check || true )
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/INSTALL 32bit/NEWS 32bit/doc/HISTORY 32bit/doc/LICENSE 32bit/README 32bit/README.LDAP 32bit/doc/TROUBLESHOOTING 32bit/doc/UPGRADE
%config(noreplace) %attr(0440,root,root) /etc/sudoers
%attr(0750,root,system) %dir /etc/sudoers.d
%attr(0711,root,system) %dir /var/lib/sudo
%attr(0711,root,system) %dir /var/lib/sudo/lectured
%attr(0700,root,system) %dir /var/run/sudo

%attr(4111,root,system) %{_bindir}/sudo_*
%attr(4111,root,system) %{_bindir}/sudoreplay_*
%attr(0111,root,system) %{_sbindir}/visudo_*
%{_bindir}/sudo
%{_bindir}/sudoreplay
%{_sbindir}/visudo

%{_bindir}/sudoedit*
%{_libdir}/sudo
%{_libdir64}/sudo
/etc/rc.d/init.d/*
#/etc/rc.d/rc2.d/*
#%{_datadir}/locale/*/LC_MESSAGES/*
%{_mandir}/man5/*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%{_includedir}/*


%changelog
* Tue Feb 04 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.8.31-1 
- New version 1.8.31
- Bullfreeware OpenSSL removal
- No more provide .so and .la
- No link from /usr
- Build 32 and 64 bit version
- No more use brtl

* Mon Jun 19 2017 Tony Reix <tony.reix@atos.net> 1.8.20p2-2
- Fix the dependency to libcrypto.so and libssl.so .

* Fri Jun 02 2017 Tony Reix <tony.reix@atos.net> 1.8.20p2-1
- New (security) version

* Tue Feb 07 2017 Tony Reix <tony.reix@atos.net> 1.8.17p1-2
- Rebuild for removing libssl.so alone.

* Mon Jul 11 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.8.17o1-1
- Update to 1.8.17p1

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

* Mon May 18 1998 Michael Maher    <mike@redhat.com>
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
