# There are two parts to this package
# The first is based on the initial Bull packaging with a collection of
# single CA certification files named <CAname>.crt
#
# The second is based on the Fedora packaging which includes
# formats/files for a classic ca-bundle, an openssl format trust bundle,
# a P11 format bundle, a legacy default bundle, a legacy disable bundle
# and a Java bundle
#
# The EDK2 format has not been extracted from the certificate bundle as it
# may not be useful on an AIX platform.
# File edku2/cacerts.bin is a CA certificate bundle for TLS server
# authentication containing a sequence in EFI_SIGNATURE_LIST format as
# defined in the UEFI-2.7 specification and EFI_CERT_X509_GUID. 
#
# If required, it can be generated after installing ca-cetificates using the
# command p11-kit >= 0.23.11 :
#      /usr/bin/p11-kit extract --format=edk2-cacerts --filter=ca-anchors
#                     --overwrite --purpose=server-auth $DEST/edk2/cacerts.bin



%define pkidir %{_sysconfdir}/pki
# %define catrustdir %{_sysconfdir}/pki/ca-trust
%define classic_tls_bundle ca-bundle.crt
%define openssl_format_trust_bundle ca-bundle.trust.crt
%define p11_format_bundle ca-bundle.trust.p11-kit
# %define legacy_default_bundle ca-bundle.legacy.default.crt
# %define legacy_disable_bundle ca-bundle.legacy.disable.crt
%define java_bundle java/cacerts


# The package version number is <year>.<NSS version>
# The previous version number was incorrectly based on the date of
# nssckbi.h 26.3.2018
#
# The <NSS version> is specfied by symbol NSS_BUILTINS_LIBRARY_VERSION
# in file nss/lib/ckfw/builtins/nssckbi.h
# This version corresponds to the collection of certificates in
# file nss/lib/ckfw/builtins/certdata.txt.


Summary: The Mozilla CA root certificate bundle
Name: ca-certificates
Version: 2019.2.30
Release: 1
License: Public Domain
BuildRoot:	/var/tmp/%{name}-%{version}-root
Group: System Environment/Base

# Please always update both certdata.txt and nssckbi.h
# They should be taken from a released version of NSS, as published
# at https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/
#
# The versions that are used by the latest released version of 
# Mozilla Firefox should be available from (raw-file or file) :
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/nssckbi.h
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt
#
# The most recent development versions of the files can be found at
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/nssckbi.h
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/certdata.txt
# (but these files might have not yet been released).


# certdata2pem.py comes from Debian
#        https://sources.debian.net/data/main/c/ca-certificates/20190110/mozilla/certdata2pem.py
# with some minor changes to handle characters encoding issues on AIX
# Directory 20160104 no longer exists - latest are  20190110 and 20180409

# The source files certdata.txt and nssckbi.h MUST be updated together
Source0: certdata.txt
Source1: nssckbi.h
Source2: certdata2pem.py
Source3: certdata2pem-fc28-2018.2.22.py
Source4: certdata2pem-fc30-2018.2.26.Python3

Source9: %{name}-%{version}-%{release}.build.log

BuildRequires: python
Requires: p11-kit >= 0.23.10


%description
This package contains the set of CA certificates chosen by the
Mozilla Foundation for use with the Internet PKI.

%prep
rm -rf %{name}
mkdir %{name}
mkdir %{name}/certs
mkdir %{name}/certs_fc28
mkdir %{name}/certs_fc28/legacy-default
mkdir %{name}/certs_fc28/legacy-disable
mkdir %{name}/java

%build
export LIBPATH=/opt/freeware/lib
cd %{name}/certs
cp %{SOURCE0} .
echo "Extracting certificates from certdata.txt"
python2 %{SOURCE2} 2>&1

echo "Extraction OK"


# Build using Fedora certdata2pem.py - more complete solution than our original

cd ../../%{name}/certs_fc28
cp %{SOURCE0} .
echo "Extracting certificates from certdata.txt"
python2 %{SOURCE3} 2>&1


# Compose P11 format bundle
 (
   cat <<EOF
# This is a bundle of X.509 certificates of public Certificate
# Authorities.  It was generated from the Mozilla root CA list.
# These certificates and trust/distrust attributes use the file format accepted
# by the p11-kit-trust module.
#
# Source: nss/lib/ckfw/builtins/certdata.txt
# Source: nss/lib/ckfw/builtins/nssckbi.h
#
# Generated from:
EOF
   cat %{SOURCE1}  |grep -w NSS_BUILTINS_LIBRARY_VERSION | awk '{print "# " $2 " " $3}';
   echo '#';
 ) > %{p11_format_bundle}

 P11FILES=`find . -name \*.tmp-p11-kit | wc -l`
 if [ $P11FILES -ne 0 ]; then
   for p in *.tmp-p11-kit; do
     cat "$p" >> %{p11_format_bundle}
   done
 fi


# Omit legacy_default_bundle and legacy_disable_bundle for now

touch %{legacy_default_bundle}
touch %{legacy_disable_bundle}



echo "Extraction OK"




%install

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs
mkdir -p $RPM_BUILD_ROOT/var/ssl/certs
mkdir -p $RPM_BUILD_ROOT%{_bindir}

mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/pem
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/openssl
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/java
mkdir -p -m 755 $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/

mkdir -p $RPM_BUILD_ROOT/var/pki/ca-trust-source
mkdir -p $RPM_BUILD_ROOT/var/pki/certs/java
mkdir -p $RPM_BUILD_ROOT/var/pki/certs/openssl
mkdir -p $RPM_BUILD_ROOT/var/pki/certs/pem


# Initially for OpenSSL, AIX chose single CA certificates per file in
#    /opt/freeware/etc/ssl/certs
# and symbolic plus hashed links from  /var/ssl/certs  to these files

cd %{name}/certs/

for CRT in `ls -1 *.crt`; do
  install -p -m 644 ${CRT} $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs
  ln -s %{_sysconfdir}/ssl/certs/${CRT} $RPM_BUILD_ROOT/var/ssl/certs/${CRT}
done

# 64bit openssl searches for certs in /var/ssl/64/certs
mkdir -p $RPM_BUILD_ROOT/var/ssl/64
ln -s ../certs $RPM_BUILD_ROOT/var/ssl/64/certs


# For different applications, bundles of CA certificates are required
# These bundles are extracted on the machine being installed from the
# ca-cetificates master bundle %{p11_format_bundle} using p11-kit extract

cd ../../%{name}/certs_fc28/

install -p -m 644 %{p11_format_bundle} $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/%{p11_format_bundle}
install -p -m 644 %{p11_format_bundle} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}

touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/%{p11_format_bundle}
touch -r %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}

# Touch files created/extracted dynamically via command p11-kit extract
touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/pem/tls-ca-bundle.pem
touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/pem/email-ca-bundle.pem
touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/pem/objsign-ca-bundle.pem
touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/openssl/%{openssl_format_trust_bundle}
touch $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs/extracted/%{java_bundle}


# AIX chose links from /var/ssl/certs (Fedora chose /etc/pki/tls/certs)

# Symbolic link to CA certificate bundle for Python
ln -s %{_sysconfdir}/ssl/certs/extracted/pem/tls-ca-bundle.pem $RPM_BUILD_ROOT/var/ssl/certs/%{classic_tls_bundle}

# Symbolic links to CA certificate bundles for OpenSSL, email, code sign
ln -s %{_sysconfdir}/ssl/certs/extracted/pem/tls-ca-bundle.pem $RPM_BUILD_ROOT/var/ssl/certs/tls-ca-bundle.pem
ln -s %{_sysconfdir}/ssl/certs/extracted/pem/email-ca-bundle.pem $RPM_BUILD_ROOT/var/ssl/certs/email-ca-bundle.pem
ln -s %{_sysconfdir}/ssl/certs/extracted/pem/objsign-ca-bundle.pem $RPM_BUILD_ROOT/var/ssl/certs/objsign-ca-bundle.pem

# Symbolic link to CA certificate bundle for OpenSSL
ln -s %{_sysconfdir}/ssl/certs/extracted/openssl/%{openssl_format_trust_bundle} $RPM_BUILD_ROOT/var/ssl/certs/%{openssl_format_trust_bundle}

# Symbolic link to CA certificate bundle for java
ln -s %{_sysconfdir}/ssl/certs/extracted/%{java_bundle} $RPM_BUILD_ROOT/var/ssl/certs/cacerts


# Create update-ca-bundles script to create/update the bundles (p11-kit extract)

cat   << __EOF__   > $RPM_BUILD_ROOT%{_bindir}/update-ca-bundles
#!/bin/sh

DEST=/opt/freeware/etc/ssl/certs/extracted

# Prevent p11-kit from reading user configuration files.
export P11_KIT_NO_USER_CONFIG=1

# OpenSSL PEM format bundle includes certificates with trust flag, i.e.
# (BEGIN TRUSTED CERTIFICATE)
/usr/bin/p11-kit extract --format=openssl-bundle --filter=certificates --overwrite --comment \$DEST/openssl/ca-bundle.trust.crt

# TLS, email and signature PEM format bundles
/usr/bin/p11-kit extract --format=pem-bundle --filter=ca-anchors --overwrite --comment --purpose server-auth \$DEST/pem/tls-ca-bundle.pem
/usr/bin/p11-kit extract --format=pem-bundle --filter=ca-anchors --overwrite --comment --purpose email \$DEST/pem/email-ca-bundle.pem
/usr/bin/p11-kit extract --format=pem-bundle --filter=ca-anchors --overwrite --comment --purpose code-signing \$DEST/pem/objsign-ca-bundle.pem

# Java format bundle
/usr/bin/p11-kit extract --format=java-cacerts --filter=ca-anchors --overwrite --purpose server-auth \$DEST/java/cacerts

__EOF__

chmod 755 $RPM_BUILD_ROOT%{_bindir}/update-ca-bundles



%postun
# if openssl RPM is installed, use it for the rehash
if [ -e /opt/freeware/bin/c_rehash ]; then
  LIBPATH=/opt/freeware/lib /opt/freeware/bin/c_rehash
else
  c_rehash
fi


%post
# if openssl RPM is installed, use it for the rehash
if [ -e /opt/freeware/bin/c_rehash ]; then
  LIBPATH=/opt/freeware/lib /opt/freeware/bin/c_rehash
else
  c_rehash /var/ssl/certs
  c_rehash /var/ssl/64/certs
fi
# Create/extract the CA certificate bundles
%{_bindir}/update-ca-bundles
# Symbolic link to CA certificate bundle for Python created here because
# c_rehash does not manage .crt files in /opt/freeware/etc/ssl/certs which
# are bundles
ln -sf /opt/freeware/etc/ssl/certs/extracted/pem/tls-ca-bundle.pem /opt/freeware/etc/ssl/certs/ca-bundle.crt



%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/ssl/certs/*.crt
/var/ssl/certs/*.crt
/var/ssl/64/certs
# Included in *.crt /var/ssl/certs/%{classic_tls_bundle}
# Included in *.crt /var/ssl/certs/%{openssl_format_trust_bundle}
/var/ssl/certs/*.pem
/var/ssl/certs/cacerts

# Master of extracted CA certificates in a bundle - ca-bundle.trust.p11-kit
%{_sysconfdir}/ssl/certs/extracted/%{p11_format_bundle}
%{_datadir}/pki/ca-trust-source/%{p11_format_bundle}
%{_bindir}/update-ca-bundles

%{_sysconfdir}/ssl/certs/extracted/pem/*.pem
%{_sysconfdir}/ssl/certs/extracted/openssl/%{openssl_format_trust_bundle}
%{_sysconfdir}/ssl/certs/extracted/%{java_bundle}

%changelog
* Fri Mar 15 2019 Michael Wilson <michael.a.wilson@atos.net> - 2019.2.30-1
- Update to latest Mozilla certdata.txt and nssckbi.h on March 15th 2019
-        corresponding to CKBI 2.30 from package   NSS 3.42.1
- Still using Python 2 script certdata2pem.py, but include Fedora 30 new
-        Python 3 version
- The previous version numbers were incorrectly based on the date of
-        nssckbi.h 26.3.2018 - they should have been CKBI 2.26 / 2018.2.26-2

* Mon May 07 2018 Michael Wilson <michael.a.wilson@atos.net> - 2018.3.26-2
- Include symbolic link to TLS/OpenSSL CA certificate bundle for Python

* Fri May 04 2018 Michael Wilson <michael.a.wilson@atos.net> - 2018.3.26-1
- Update to latest Mozilla certdata.txt and nssckbi.h on April 5th 2018
- 242 deleted certificates and 176 additions w.r.t. package 2016.12.12-1
- Update to latest Debian certdata2pem.py on April 5th 2018
- Include part of latest Fedora ca-certificates packaging
- The extracted CA certificates master bundle is used by p11-kit to produce
-                                    different formats - openssl, pem, java

* Mon Dec 12 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2016.12.12-1
- Initial release on AIX

* Fri Oct 7 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2016.10.7-1
- Initial release on AIX
