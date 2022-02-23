Name: gnupg2
Summary: A GNU utility for secure communication and data storage.
Version: 2.0.30
Release: 1
License: GPL
Group: Productivity/Security
Source0: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-%{version}.tar.bz2.sig
Patch0: %{name}-%{version}-aix.patch
Patch1:  gnupg-2.0.20-insttools.patch
Patch3:  gnupg-2.0.20-secmem.patch

URL: http://www.gnupg.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: patch, make
BuildRequires: libgcrypt-devel, libksba-devel, libassuan >= 2.0.0
BuildRequires: libgpg-error-devel >= 1.11
BuildRequires: libiconv >= 1.14-2
BuildRequires: pth-devel, gettext, bzip2, zlib-devel
BuildRequires: curl-devel >= 7.17.1, readline-devel >= 5.2
BuildRequires: openldap-devel >= 2.4.23

Requires: libgcrypt, libksba, libassuan >= 2.0.0
Requires: libgpg-error >= 1.11
Requires: libiconv >= 1.14-2
Requires: pth, gettext, bzip2, zlib
Requires: curl >= 7.17.1, readline >= 5.2
Requires: openldap >= 2.4.23
Requires: /sbin/install-info, info

Provides: gpg, openpgp

%description
GnuPG is GNU's tool for secure communication and data storage.  It can
be used to encrypt data and to create digital signatures.  It includes
an advanced key management facility and is compliant with the proposed
OpenPGP Internet standard as described in RFC2440 and the S/MIME
standard as described by several RFCs.

GnuPG 2.0 is the stable version of GnuPG integrating support for
OpenPGP and S/MIME.  It does not conflict with an installed 1.x
OpenPGP-only version.

GnuPG 2.0 is a newer version of GnuPG with additional support for
S/MIME.  It has a different design philosophy that splits
functionality up into several modules.  Both versions may be installed
simultaneously without any conflict (gpg is called gpg2 in GnuPG 2).
In fact, the gpg version from GnuPG 1.x is able to make use of the
gpg-agent as included in GnuPG 2 and allows for seamless passphrase
caching.  The advantage of GnupG 1.x is its smaller size and no
dependency on other modules at run and build time.


%prep
%setup -q -n gnupg-%{version}
export PATH=/opt/freeware/bin:$PATH
%patch0
%patch1 -p1 -b .insttools
%patch3 -p1 -b .secmem


%build
export RM="/usr/bin/rm -f"
export CC="xlc_r"
export CC="gcc -maix32"
export CFLAGS="-O2"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --disable-scdaemon \
    --with-zlib \
    --with-bzip2 \
    --with-libcurl	\
    --with-libiconv-prefix=/opt/freeware	\
    --with-libintl-prefix=/opt/freeware	

gmake %{?_smp_mflags}

gmake check

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
* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 2.0.30-1
- Updated to version 2.0.30

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.26-1
- updated to version 2.0.26

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.25-1
- updated to version 2.0.25

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.24-1
- updated to version 2.0.24

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.0.23-1
- updated to version 2.0.23

* Mon Oct 07 2013 Michael Perzl <michael@perzl.org> - 2.0.22-1
- updated to version 2.0.22

* Fri Sep 13 2013 Michael Perzl <michael@perzl.org> - 2.0.21-1
- updated to version 2.0.21

* Mon Jul 22 2013 Michael Perzl <michael@perzl.org> - 2.0.20-1
- updated to version 2.0.20

* Fri Apr 26 2013 Michael Perzl <michael@perzl.org> - 2.0.19-1
- updated to version 2.0.19

* Wed Aug 17 2011 Michael Perzl <michael@perzl.org> - 2.0.18-1
- updated to version 2.0.18

* Fri Jan 21 2011 Michael Perzl <michael@perzl.org> - 2.0.17-1
- updated to version 2.0.17

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 2.0.16-1
- updated to version 2.0.16

* Tue Jul 06 2010 Michael Perzl <michael@perzl.org> - 2.0.15-2
- removed dependency on gettext >= 0.17

* Wed Mar 10 2010 Michael Perzl <michael@perzl.org> - 2.0.15-1
- updated to version 2.0.15

* Tue Dec 22 2009 Michael Perzl <michael@perzl.org> - 2.0.14-1
- updated to version 2.0.14

* Mon Sep 07 2009 Michael Perzl <michael@perzl.org> - 2.0.13-1
- updated to version 2.0.13

* Wed Aug 26 2009 Michael Perzl <michael@perzl.org> - 2.0.12-1
- updated to version 2.0.12

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 2.0.11-1
- updated to version 2.0.11

* Mon Mar 31 2008 Michael Perzl <michael@perzl.org> - 2.0.9-1
- updated to version 2.0.9

* Mon Jan 07 2008 Michael Perzl <michael@perzl.org> - 2.0.8-1
- updated to version 2.0.8

* Mon Oct 08 2007 Michael Perzl <michael@perzl.org> - 2.0.7-1
- first version for AIX V5.1 and higher
