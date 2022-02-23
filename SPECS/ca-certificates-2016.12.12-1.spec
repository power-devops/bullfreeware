Summary: The Mozilla CA root certificate bundle
Name: ca-certificates
Version: 2016.12.12
Release: 1
License: Public Domain
BuildRoot:	/var/tmp/%{name}-%{version}-root
Group: System Environment/Base

# Please always update both certdata.txt and nssckbi.h
# They should be taken from a released version of NSS, as published
# at https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/
#
# The versions that are used by the latest released version of 
# Mozilla Firefox should be available from:
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/nssckbi.h
# https://hg.mozilla.org/releases/mozilla-release/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt
#
# The most recent development versions of the files can be found at
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/nssckbi.h
# http://hg.mozilla.org/projects/nss/raw-file/default/lib/ckfw/builtins/certdata.txt
# (but these files might have not yet been released).


# certdata2pem.py comes from Debian ( https://sources.debian.net/data/main/c/ca-certificates/20160104/mozilla/certdata2pem.py ) with some minor changes to handle characters encoding issues on AIX
Source0: certdata.txt
Source1: nssckbi.h
Source2: certdata2pem.py
Source3: %{name}-%{version}-%{release}.build.log

BuildRequires: python

%description
This package contains the set of CA certificates chosen by the
Mozilla Foundation for use with the Internet PKI.

%prep
rm -rf %{name}
mkdir %{name}
mkdir %{name}/certs

%build
export LIBPATH=/opt/freeware/lib
cd %{name}/certs
cp %{SOURCE0} .
echo "Extracting certificates from certdata.txt"
python2 %{SOURCE2} 2>&1
echo "Extraction OK"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs
mkdir -p $RPM_BUILD_ROOT/var/ssl/certs


cd %{name}/certs/
for CRT in `ls -1 *.crt`; do
  install -p -m 644 ${CRT} $RPM_BUILD_ROOT%{_sysconfdir}/ssl/certs
  ln -s %{_sysconfdir}/ssl/certs/${CRT} $RPM_BUILD_ROOT/var/ssl/certs/${CRT}
done

# 64bit openssl searches for certs in /var/ssl/64/certs
mkdir -p $RPM_BUILD_ROOT/var/ssl/64
ln -s ../certs $RPM_BUILD_ROOT/var/ssl/64/certs

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

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/ssl/certs/*.crt
/var/ssl/certs/*.crt
/var/ssl/64/certs

%changelog
* Mon Dec 12 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2016.12.12-1
- Initial release on AIX

* Fri Oct 7 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2016.10.7-1
- Initial release on AIX
