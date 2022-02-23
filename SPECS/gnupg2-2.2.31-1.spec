# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


%define __bzip2 /opt/freeware/bin/bzip2

%define _smp_mflags -j4

Name: gnupg2
Summary: A GNU utility for secure communication and data storage.
Version: 2.2.31
Release: 1
License: GPLv3+
Group:   Productivity/Security
Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2.sig
Source1000: %{name}-%{version}-%{release}.build.log 

Patch0: %{name}-2.2.19-aix.patch

# From Fedora (v2.2.27, different from v2.2.23)
Patch1:  gnupg-2.2.23-insttools-v2.patch

# exponential backoff when waiting on gpg-agent and dirmngr to save time
# Patch2:  gnupg-2.1.19-exponential.patch

# needed for compatibility with system FIPS mode
Patch3:  gnupg-2.1.10-secmem.patch

# non-upstreamable patch adding file-is-digest option needed for Copr
# TBC Patch4:  gnupg-2.2.20-file-is-digest.patch

# fix handling of missing key usage on ocsp replies - upstream T1333
Patch5:  gnupg-2.2.16-ocsp-keyusage.patch

Patch6:  gnupg-2.1.1-fips-algo.patch

# allow 8192 bit RSA keys in keygen UI with large RSA
Patch9:  gnupg-2.2.23-large-rsa.patch

# From Fedora 33 gnupg2 2.2.18 / 19 / 20
# fix missing uid on refresh from keys.openpgp.org
# https://salsa.debian.org/debian/gnupg2/commit/f292beac1171c6c77faf41d1f88c2e0942ed4437
Patch20: gnupg-2.2.18-tests-add-test-cases-for-import-without-uid.patch
Patch21: gnupg-2.2.18-gpg-allow-import-of-previously-known-keys-even-without-UI.patch
Patch22: gnupg-2.2.18-gpg-accept-subkeys-with-a-good-revocation-but-no-self-sig.patch

# Fixes for issues found in Coverity scan - reported upstream
# From Fedora (v2.2.27, different from v2.2.23)
Patch30: gnupg-2.2.21-coverity-v2.patch

Patch40: %{name}-2.2.9-g10-t-stutter-sync.patch
Patch41: %{name}-2.2.19-aix-thread-init.patch

# New patches appearing within 2.2.27-4.fc34 Fedora version
# 1) non-upstreamable patch adding file-is-digest option needed for Copr
#    (Fedora/Copr is an easy-to-use automatic build system providing a package repository as its output)
#  That seems specific to Fedora. Probably we should not use it.
#	Patch42: gnupg-2.2.20-file-is-digest.patch
# 2) Do not require exclusive access to the pcsc (pc/sc)
#    (The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
#     in a very small form factor for communicating to smartcards and
#     readers.  PC/SC Lite uses the same winscard API as used under Windows.)
#  Hummm The Patch mainly adds a possibility option. Maybe useful.
# 2.2.28 : patch seems to have been integrated. No more needed (and my 2.2.28 version seems wrong...)
#	Patch43: gnupg-2.2.28-shared.patch

# The following is needed for 32 bit build
Patch44: %{name}-2.2.9-aix-do-open64.patch

URL:     https://www.gnupg.org

# BuildRequires: patch, make
BuildRequires: automake
BuildRequires: bzip2, bzip2-devel
BuildRequires: curl-devel >= 7.68.0
BuildRequires: gettext
BuildRequires: gettext-devel
BuildRequires: libassuan-devel >= 2.1.0
BuildRequires: libgcrypt-devel >= 1.7.0
buildRequires: libgpg-error-devel >= 1.38
BuildRequires: libksba-devel >= 1.3.0
# BuildRequires: libiconv >= 1.14-2
BuildRequires: openldap-devel >= 2.4.48-3
BuildRequires: ncurses-devel
BuildRequires: npth-devel
BuildRequires: readline-devel >= 7.0
BuildRequires: zlib-devel
# Following in Fedora
# BuildRequires: libusb-devel
# BuildRequires: pcsc-lite-libs
# BuildRequires: gnutls-devel
# BuildRequires: fuse
BuildRequires: pkg-config
# Useful for -n hexadecimal option
BuildRequires: gawk
# Required for TOFU/Tofu/tofu test
BuildRequires: sqlite-devel

# Requires: libgcrypt, libksba, libassuan >= 2.0.0
Requires: libgcrypt >= 1.7.0
Requires: libgpg-error >= 1.38
Requires: libiconv >= 1.14-2
Requires: npth, gettext, bzip2, zlib
Requires: curl >= 7.17.1, readline >= 5.2
Requires: openldap >= 2.4.23
Requires: /sbin/install-info, info

# For testing - weak dependency because not required for public-key operations
Recommends: pinentry

# Provides: gpg, openpgp
Provides: gpg = %{version}-%{release}
Provides: gnupg = %{version}-%{release}
Provides: dirmngr = %{version}-%{release}
Provides: opengpg = %{version}-%{release}


%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.

GnuPG2 is a newer version of GnuPG with additional support for
S/MIME.  It has a different design philosophy that splits
functionality up into several modules.

This package includes support for smart cards and S/MIME encryption
and signing.


# From version 2.0.13-3 Fedora separated gpgsm components to form gnupg2-smime

# %package smime
# Summary: CMS encryption and signing tool and smart card support for GnuPG
# Requires: gnupg2 = %{version}-%{release}
# Group: Applications/Internet
# 
# %description smime
# GnuPG is GNU's tool for secure communication and data storage. This
# package adds support for smart cards and S/MIME encryption and signing
# to the base GnuPG package


%prep

%setup -q -n gnupg-%{version}

export PATH=/opt/freeware/bin:$PATH
%patch0
%patch1 -p1 -b .insttools
# %patch2 -p1 -b .exponential
%patch3 -p1 -b .secmem
# TBC %patch4 -p1 -b .file-is-digest
%patch5 -p1 -b .keyusage
%patch6 -p1 -b .fips
%patch9 -p1 -b .large-rsa

%patch20 -p1 -b .test_missing_uid
%patch21 -p1 -b .prev_known_key
%patch22 -p1 -b .good_revoc

%patch30 -p1 -b .coverity

%patch40 -p1 -b .g10-t-stutter-sync
%patch41 -p1 -b .aix-thread-init

#	%patch42 -p1 -b .file-is-digest
#	%patch43 -p1 -b .shared

# The following is needed for 32 bit build
# %patch44 -p1 -b .aix-do-open64

chmod +r tests/openpgp/import-incomplete/*.test_missing_uid
chmod +r tests/openpgp/import-incomplete.scm.test_missing_uid

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

cd 32bit
# The following is needed for 32 bit build
%patch44 -p1 -b .aix-do-open64


%build

export RM="/usr/bin/rm -f"
# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="gcc -maix64"
export CFLAGS="-O2"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LIBS="-liconv -lintl"

./configure  \
    --enable-gpg-is-gpg2 \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --libexecdir=%{_libexecdir}64 \
    --with-zlib \
    --with-bzip2 \
    --disable-gpgtar \
    --disable-rpath \
    --enable-g13 \
    --enable-large-secmem \
    --with-pinentry-pgm=/opt/freeware/bin/pinentry

# Previous options
#    --disable-scdaemon
#    --with-libcurl  - configure 2.2.19 warns that this is not a valid option
#    --with-libiconv-prefix=/opt/freeware  - hardcoded path in binaries
#    --with-libintl-prefix=/opt/freeware   - hardcoded path in binaries
#
# Following are in Fedora
#   --disable-gpgtar  --disable-rpath  --enable-g13  --enable-large-secmem
#
# May require  --disable-card-support

gmake %{?_smp_mflags}

# build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CC="gcc -maix32"
export CFLAGS="-O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LIBS="-liconv -lintl"
# Does not exist ? export GPG_ERROR_CONFIG=/opt/freeware/bin/gpg-error-config_32
# Does not exist ? export KSBA_CONFIG=/opt/freeware/bin/ksba-config_32
# Does not exist ? export LIBASSUAN_CONFIG=/opt/freeware/bin/libassuan-config_32
# Does not exist ? export LIBGCRYPT_CONFIG=/opt/freeware/bin/libgcrypt-config_32

export PTH_CONFIG='/opt/freeware/bin/pth-config_32'

./configure  \
    --enable-gpg-is-gpg2 \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --libexecdir=%{_libexecdir} \
    --disable-scdaemon \
    --with-zlib \
    --with-bzip2 \
    --with-pinentry-pgm=/usr/bin/pinentry

gmake %{?_smp_mflags}


%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#Install on 64bit mode
cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install docdir=%{_docdir}/%{name}-%{version}

cp tools/gpg-zip tools/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/

sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
cp lspgpot ${RPM_BUILD_ROOT}%{_bindir}/lspgpot
chmod 755  ${RPM_BUILD_ROOT}%{_bindir}/lspgpot

# rename files conflicting with gnupg-1.x
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/gpg2-split
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpg-zip  ${RPM_BUILD_ROOT}%{_bindir}/gpg2-zip

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

#Install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install docdir=%{_docdir}/%{name}-%{version}

cp tools/gpg-zip tools/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
cp lspgpot ${RPM_BUILD_ROOT}%{_bindir}/lspgpot
chmod 755  ${RPM_BUILD_ROOT}%{_bindir}/lspgpot

rm -f       ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gnupg*.info*

# gpgconf.conf
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/gnupg
touch    ${RPM_BUILD_ROOT}%{_sysconfdir}/gnupg/gpgconf.conf

# more docs
cp AUTHORS COPYING ChangeLog NEWS THANKS TODO \
  ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/

# drop the gpg scheme interpreter
rm -f %{buildroot}%{_bindir}/gpgscm

# rename files conflicting with gnupg-1.x
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/gpg2-split
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpg-zip  ${RPM_BUILD_ROOT}%{_bindir}/gpg2-zip
# No more in 2.0.30
#mv -f ${RPM_BUILD_ROOT}%{_mandir}/man1/gpg-zip.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/gpg2-zip.1

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

# compat symlinks
ln -sf gpg2    %{buildroot}%{_bindir}/gpg
ln -sf gpgv2   %{buildroot}%{_bindir}/gpgv
ln -sf gpg2.1   %{buildroot}%{_mandir}/man1/gpg.1
ln -sf gpgv2.1  %{buildroot}%{_mandir}/man1/gpgv.1
ln -sf gnupg2.7 %{buildroot}%{_mandir}/man7/gnupg.7


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# There is a t-stringhelp test which fails compare "//bar" with "/bar"
# if HOME=/
mkdir -p /tmp/.gnupg

cd 64bit
export OBJECT_MODE=64
(HOME=/tmp gmake -k check || true)

cd ../32bit
export OBJECT_MODE=32
(HOME=/tmp gmake -k check || true )


%post
if [ -f %{_infodir}/%{name}.info.gz ] ; then
    /sbin/install-info %{_infodir}/%{name}*.info.gz || :
fi


%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/%{name}.info.gz ] ; then
        /sbin/install-info --delete %{_infodir}/%{name}.info.gz || :
    fi
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# From version 2.0.13-3 Fedora separated gpgsm components to form gnupg2-smime
# containing _bindir/gpgsm*, _bindir/kbxutil, _mandir/man?/gpgsm*


%files
%defattr(-,root,system)
%{_docdir}/%{name}-%{version}/
%dir %{_sysconfdir}/gnupg
%ghost %config(noreplace) %{_sysconfdir}/gnupg/gpgconf.conf
%{_bindir}/*
%{_sbindir}/*
%{_libexecdir}/*
%{_libexecdir}64/*
%{_datadir}/gnupg/*
%{_datadir}/locale/*/*/*
%{_infodir}/*
%{_mandir}/man?/*


%changelog
* Sat Sep 18 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.2.31-1
- Update to 2.2.31

* Sat Aug 28 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.2.30-1
- Update to 2.2.30

* Tue Jul 20 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.2.29-1
- Update to 2.2.29

* Mon Jun 14 2021 Tony Reix <tony.reix@atos.com> - 2.2.28-1
- Move to version 2.2.28
- Add some BuildRequires: for autobuild (tofu test skipped otherwise)
- Bug on AIX & Fedora with test: t-sexputil

* Tue Jun 08 2021 Tony Reix <tony.reix@atos.com> - 2.2.27-1
- Move to version 2.2.27
- Use updated version (-v2) of: gnupg-2.2.21-coverity.patch,       gnupg-2.2.23-insttools.patch
- Use new patches:              gnupg-2.2.20-file-is-digest.patch, gnupg-2.2.27-shared.patch
- Update .spec file based on Fedora .spec file

* Mon Oct 12 2020 Michael Wilson <michael.a.wilson@atos.com> - 2.2.23-1
- Updated to version 2.2.23 based on Fedora 32 2.2.23-1
- This version fixes critical security bug CVE-2020-25125
- Define __bzip2 to W/A issue with symlinks in RPM LPP package

* Tue Aug 25 2020 Michael Wilson <michael.a.wilson@atos.com> - 2.2.21-1
- Updated to version 2.2.21
- Based on Fedora 33 2.2.21-4

* Mon Jul 27 2020 Michael Wilson <michael.a.wilson@atos.com> - 2.2.19-1
- Feb 18 2020 Etienne Guesnet Modifications for build under RPM 4 on laurel2
- Updated to version 2.2.19
- Based on Fedora 33 2.2.19 / 20

* Thu Oct 11 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.2.9-1
- Updated to version 2.2.9
- Removed Perzl changelog as the notes contained no useful information

* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 2.0.30-1
- Updated to version 2.0.30

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.26-1
- updated to version 2.0.26

