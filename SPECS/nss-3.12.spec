Summary:	Network Security Services
Name:		nss
Version:	3.12
Release:        2
License:	MPL/GPL/LGPL
URL:		http://www.mozilla.org/projects/security/pki/nss/
Group:		System Environment/Libraries
Requires:	nspr >=	4.7 
BuildRoot:	/var/tmp/%{name}-root
Prefix:		%{_prefix}
Source:		https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_3_12_RTM/src/%{name}-%{version}.tar.gz
Patch0: 	%{name}-%{version}-aixconf.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package tools
Summary:          Tools for the Network Security Services
Group:            System Environment/Base
Requires:         zlib

%description tools
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

Install the nss-tools package if you need command-line tools to
manipulate the NSS certificate and key database.


%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries

%description devel
Header and Library files for doing development with Network Security Services.

%prep
%setup -q
%patch0 -p1 -b .aixconf

%build
cd  ./mozilla/security/coreconf
make
cd ../dbm
make
cd ../nss
make

cd ../../dist/*.OBJ/lib
for solibfile in libnss3 libnssutil3 libnssdbm3 libssl3 libsqlite3 \
	       libsmime3 libsoftokn3 libnssckbi libfreebl3
do
	/usr/bin/ar -qv $solibfile.a $solibfile.so
done

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

echo $RPM_BUILD_ROOT%{_bindir}
echo $RPM_BUILD_ROOT%{_libdir}
echo $RPM_BUILD_ROOT%{_includedir}

# No make install target so we do it manually
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/nss3
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT%{_includedir}/nss3

for binfile in certutil cmsutil crlutil modutil pk12util \
	     atob btoa derdump ocspclnt pp selfserv shlibsign \
	     strsclnt symkeyutil tstclnt vfyserv vfychain
do
	cp mozilla/dist/*.OBJ/bin/$binfile $RPM_BUILD_ROOT%{_bindir}
	chmod 755 $RPM_BUILD_ROOT%{_bindir}/$binfile
	cd $RPM_BUILD_ROOT/usr/bin
	ln -sf ../..%{_bindir}/$binfile $binfile
	cd -
done

for libfile in libnss3.* libnssutil3.* libnssdbm3.* libssl3.* libsqlite3.* \
	       libsmime3.* libsoftokn3.* libnssckbi.* libfreebl3.*
do
	cp mozilla/dist/*.OBJ/lib/$libfile $RPM_BUILD_ROOT%{_libdir}
	chmod 755 $RPM_BUILD_ROOT%{_libdir}/$libfile
done

for files in libcrmf.a libnssb.a libnssckfw.a libnss.a libjar.a \
	     libnssutil.a libsmime.a libssl.a libnssdev.a libzlib.a
do
	cp mozilla/dist/*.OBJ/lib/$files $RPM_BUILD_ROOT%{_libdir}/nss3
	chmod 644 $RPM_BUILD_ROOT%{_libdir}/nss3/$files
done

cp mozilla/dist/*.OBJ/lib/*.chk  $RPM_BUILD_ROOT%{_libdir}
chmod 644 $RPM_BUILD_ROOT%{_libdir}/*.chk

cp mozilla/dist/public/nss/*.h $RPM_BUILD_ROOT%{_includedir}
chmod 644 $RPM_BUILD_ROOT%{_includedir}/*.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/libnss3.a
%{_libdir}/libnssutil3.a
%{_libdir}/libnssdbm3.a
%{_libdir}/libssl3.a
%{_libdir}/libsmime3.a 
%{_libdir}/libsoftokn3.a
%{_libdir}/libnssckbi.a
%{_libdir}/libfreebl3.a
%{_libdir}/libsqlite3.a
%ghost %{_libdir}/libsoftokn3.chk
%ghost %{_libdir}/libfreebl3.chk

%{_bindir}/certutil
%{_bindir}/cmsutil
%{_bindir}/crlutil
%{_bindir}/modutil
%{_bindir}/pk12util
/usr/bin/certutil
/usr/bin/cmsutil
/usr/bin/crlutil
/usr/bin/modutil
/usr/bin/pk12util
%{_bindir}/atob
%{_bindir}/btoa
%{_bindir}/derdump
%{_bindir}/ocspclnt
%{_bindir}/pp
%{_bindir}/selfserv
%{_bindir}/strsclnt
%{_bindir}/symkeyutil
%{_bindir}/tstclnt
%{_bindir}/vfyserv
%{_bindir}/vfychain

%files devel
%defattr(-,root,root)
%{_libdir}/nss3/*.a
%{_libdir}/*.so

%{_includedir}/*.h

%changelog
* Wed Feb 25 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.12-2
- ship libsqlite3
- add .so file in -devel rpm
- .spec simplification

* Wed Feb 25 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.12-1
- Initial port for AIX
