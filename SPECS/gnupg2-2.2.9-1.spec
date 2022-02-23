Name: gnupg2
Summary: A GNU utility for secure communication and data storage.
Version: 2.2.9
Release: 1
License: GPLv3+
Group:   Applications/System
URL:     https://www.gnupg.org

Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2.sig

# Patch0: %{name}-%{version}-aix.patch
Patch0: %{name}-2.2.9-aix.patch

Patch1:  gnupg-2.1.21-insttools.patch

# exponential backoff when waiting on gpg-agent and dirmngr to save time
Patch2:  gnupg-2.1.19-exponential.patch

# needed for compatibility with system FIPS mode
Patch3:  gnupg-2.1.10-secmem.patch

# non-upstreamable patch adding file-is-digest option needed for Copr
# TBC Patch4:  gnupg-2.2.8-file-is-digest.patch

Patch5:  gnupg-2.1.1-ocsp-keyusage.patch

Patch6:  gnupg-2.1.1-fips-algo.patch

# allow 8192 bit RSA keys in keygen UI with large RSA
Patch9:  gnupg-2.1.21-large-rsa.patch

Patch10: %{name}-2.2.9-g10-t-stutter-sync.patch
Patch11: %{name}-2.2.9-aix-thread-init.patch
Patch12: %{name}-2.2.9-aix-do-open64.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


# BuildRequires: patch, make
# BuildRequires: libgcrypt-devel, libksba-devel, libassuan >= 2.0.0
# BuildRequires: libgpg-error-devel >= 1.11
# BuildRequires: libiconv >= 1.14-2
# BuildRequires: pth-devel, gettext, bzip2, zlib-devel
# BuildRequires: curl-devel >= 7.17.1, readline-devel >= 5.2
# BuildRequires: openldap-devel >= 2.4.23
# 
# Requires: libgcrypt, libksba, libassuan >= 2.0.0
# Requires: libgpg-error >= 1.11
# Requires: libiconv >= 1.14-2
# Requires: pth, gettext, bzip2, zlib
# Requires: curl >= 7.17.1, readline >= 5.2
# Requires: openldap >= 2.4.23
# Requires: /sbin/install-info, info


# Current list of requires from Fedora
BuildRequires: bzip2-devel
BuildRequires: curl-devel
# BuildRequires: docbook-utils  Not on Bullfreeware
BuildRequires: gettext
BuildRequires: libassuan-devel >= 2.1.0
# BuildRequires: libgcrypt-devel >= 1.7.0  Only have 1.5.4 on Bullfreeware 
BuildRequires: libgcrypt-devel
BuildRequires: libgpg-error-devel >= 1.31
BuildRequires: libksba-devel >= 1.3.0
BuildRequires: openldap-devel
# BuildRequires: libusb-devel
# BuildRequires: pcsc-lite-libs
BuildRequires: npth-devel
BuildRequires: readline-devel ncurses-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: sqlite-devel
# BuildRequires: fuse
# Requires: libgcrypt >= 1.7.0
Requires: libgcrypt
Requires: libgpg-error >= 1.31
Requires: gnupg2 = %{version}-%{release}


# Provides: gpg, openpgp
Provides: gpg = %{version}-%{release}
Provides: gnupg = %{version}-%{release}
Provides: dirmngr = %{version}-%{release}





%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.

GnuPG 2.0 is a newer version of GnuPG with additional support for
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
%patch2 -p1 -b .exponential
%patch3 -p1 -b .secmem
# %patch4 -p1 -b .file-is-digest
%patch5 -p1 -b .keyusage
%patch6 -p1 -b .fips
%patch9 -p1 -b .large-rsa

%patch10 -p1 -b .g10-t-stutter-sync
%patch11 -p1 -b .aix-thread-init
%patch12 -p1 -b .aix-do-open64


%build
export RM="/usr/bin/rm -f"
export CC="xlc_r"
export CC="gcc -maix32"
export CFLAGS="-O2"

# Previous options
#    --disable-scdaemon
#    --with-zlib
#    --with-bzip2
#    --with-libcurl
#
# Following are in Fedora
#   --disable-gpgtar  --disable-rpath  --enable-g13  --enable-large-secmem
#
# May require  --disable-card-support


./configure -v \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --disable-gpgtar \
    --disable-rpath \
    --enable-g13 \
    --enable-large-secmem \
    --with-libiconv-prefix=/opt/freeware \
    --with-libintl-prefix=/opt/freeware

gmake %{?_smp_mflags}

# There is a t-stringhelp test which fails compare "//bar" with "/bar"
# if HOME=/
HOME=/tmp gmake check

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install docdir=%{_docdir}/%{name}-%{version}

cp tools/gpg-zip tools/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
cp lspgpot ${RPM_BUILD_ROOT}%{_bindir}/lspgpot
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/lspgpot

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gnupg*.info*

# gpgconf.conf
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/gnupg
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/gnupg/gpgconf.conf

# more docs
cp AUTHORS COPYING ChangeLog NEWS THANKS TODO \
  ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/

# rename files conflicting with gnupg-1.x
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpgsplit ${RPM_BUILD_ROOT}%{_bindir}/gpg2-split
mv -f ${RPM_BUILD_ROOT}%{_bindir}/gpg-zip ${RPM_BUILD_ROOT}%{_bindir}/gpg2-zip
# No more in 2.0.30
#mv -f ${RPM_BUILD_ROOT}%{_mandir}/man1/gpg-zip.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/gpg2-zip.1

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%post
if [ -f %{_infodir}/%{name}.info.gz ] ; then
    /sbin/install-info %{_infodir}/%{name}*.info.gz %{_infodir}/dir || :
fi


%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/%{name}.info.gz ] ; then
        /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
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
%{_datadir}/gnupg/*
%{_datadir}/locale/*/*/*
%{_infodir}/*
%{_mandir}/man?/*
/usr/bin/*
/usr/sbin/*


%changelog
* Thu Oct 11 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.2.9-1
- Updated to version 2.2.9
- Removed Perzl changelog as the notes contained no useful information

* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 2.0.30-1
- Updated to version 2.0.30

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.26-1
- updated to version 2.0.26

