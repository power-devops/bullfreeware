%global nspr_version 4.9.5
Summary:	Network Security Services
Name:		nss
Version:	3.14.3
Release:        1
License:	MPL/GPL/LGPL
URL:		http://www.mozilla.org/projects/security/pki/nss/
Group:		System Environment/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:		%{_prefix}
Source:		https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_3_13_2_RTM/src/%{name}-%{version}.tar.gz
Source1:	nss-config.in
BuildRequires:    nspr-devel >= %{nspr_version}
Requires:         nspr >= %{nspr_version}
Patch0: 	%{name}-%{version}-aixconf.patch
Patch1: 	%{name}-%{version}-int64.patch
Patch2: 	%{name}-%{version}-ocspsig.patch

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         nspr-devel >= %{nspr_version}

%description devel
Header and Library files for doing development with Network Security Services.

%prep
%setup -q
%patch0 -p1 -b .aixconf
%patch1 -p1 -b .int64
%patch2 -p1 -b .ocspsig

mkdir mozilla-64
mv mozilla mozilla-32
cd mozilla-32
cp -r * ../mozilla-64
cd ..

%build
# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=64
export USE_64=1
export NSPR_INCLUDE_DIR=/opt/freeware/include/nspr4
export NSPR_LIB_DIR=/opt/freeware/lib64
gmake -C mozilla-64/security/coreconf
gmake -C mozilla-64/security/dbm
gmake -C mozilla-64/security/nss
gmake -C mozilla-64/security/nss/lib/sysinit

mkdir -p mozilla-64/dist/pkgconfig
cat %{SOURCE1} | sed -e "s,@libdir@,%{_libdir64},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,3,g" \
                          -e "s,@MOD_MINOR_VERSION@,13,g" \
                          -e "s,@MOD_PATCH_VERSION@,2,g" \
                          > ./mozilla-64/dist/pkgconfig/nss-config

chmod 755 mozilla-64/dist/pkgconfig/nss-config

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=32
export USE_64=
export NSPR_INCLUDE_DIR=/opt/freeware/include/nspr4
export NSPR_LIB_DIR=/opt/freeware/lib
gmake -C mozilla-32/security/coreconf
gmake -C mozilla-32/security/dbm
gmake -C mozilla-32/security/nss
gmake -C mozilla-32/security/nss/lib/sysinit

mkdir -p mozilla-32/dist/pkgconfig
cat %{SOURCE1} | sed -e "s,@libdir@,%{_libdir},g" \
                          -e "s,@prefix@,%{_prefix},g" \
                          -e "s,@exec_prefix@,%{_prefix},g" \
                          -e "s,@includedir@,%{_includedir}/nss3,g" \
                          -e "s,@MOD_MAJOR_VERSION@,3,g" \
                          -e "s,@MOD_MINOR_VERSION@,13,g" \
                          -e "s,@MOD_PATCH_VERSION@,2,g" \
                          > ./mozilla-32/dist/pkgconfig/nss-config

chmod 755 mozilla-32/dist/pkgconfig/nss-config

%install
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar -X32_64"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# There is no make install target so we do it manually

# No make install target so we do it manually
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/nss3
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64/nss3
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/nss3/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64/nss3/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/nss3
mkdir -p ${RPM_BUILD_ROOT}/usr/bin

# process shared libraries
for solibfile in libfreebl3 libnssckbi libnssutil3 \
	libsoftokn3 libssl3 libnss3 libnssdbm3 \
	libsmime3 libsqlite3
do
	# copy shared objects
	install -p -m 755 mozilla-32/dist/*.OBJ/lib/${solibfile}.so ${RPM_BUILD_ROOT}%{_libdir}
	install -p -m 755 mozilla-64/dist/*.OBJ/lib/${solibfile}.so ${RPM_BUILD_ROOT}%{_libdir}64
	# build AIX shared libraries
	${AR} -rv ${RPM_BUILD_ROOT}%{_libdir}/${solibfile}.a mozilla-32/dist/*.OBJ/lib/${solibfile}.so
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/${solibfile}.a mozilla-64/dist/*.OBJ/lib/${solibfile}.so
	
done

# process binaries files
for binfile in certutil cmsutil crlutil modutil pk12util \
	     atob btoa derdump ocspclnt pp selfserv shlibsign \
	     strsclnt symkeyutil tstclnt vfyserv vfychain \
	     signtool signver ssltap
do
	install -p -m 755 mozilla-32/dist/*.OBJ/bin/${binfile} ${RPM_BUILD_ROOT}%{_bindir}
	install -p -m 755 mozilla-64/dist/*.OBJ/bin/${binfile} ${RPM_BUILD_ROOT}%{_bindir}/${binfile}_64
done


# copy some other libraries
for file in libcrmf.a libnssb.a libnssckfw.a libnss.a libjar.a \
	     libnssutil.a libsmime.a libssl.a libnssdev.a libzlib.a
do
	install -p -m 644 mozilla-32/dist/*.OBJ/lib/${file} ${RPM_BUILD_ROOT}%{_libdir}/nss3
	install -p -m 644 mozilla-64/dist/*.OBJ/lib/${file} ${RPM_BUILD_ROOT}%{_libdir}64/nss3
done

# copy the include files
for file in mozilla-32/dist/public/nss/*.h 
do
	install -p -m 644 ${file} ${RPM_BUILD_ROOT}%{_includedir}/nss3
done

# copy the package configuration files
install -p -m 755 mozilla-32/dist/pkgconfig/nss-config ${RPM_BUILD_ROOT}%{_bindir}/nss-config
install -p -m 755 mozilla-64/dist/pkgconfig/nss-config ${RPM_BUILD_ROOT}%{_bindir}/nss-config_64

# strip binaries                 
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# make symbolic links            
(                   
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do                             
    mkdir -p usr/${dir}          
    cd usr/${dir}     
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -                         
  done                           
)      
     

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_libdir}/libnss3.a
%{_libdir}/libnss3.so
%{_libdir}64/libnss3.so
%{_libdir}/libnssutil3.a
%{_libdir}/libnssutil3.so
%{_libdir}64/libnssutil3.so
%{_libdir}/libnssdbm3.a
%{_libdir}/libnssdbm3.so
%{_libdir}64/libnssdbm3.so
%{_libdir}/libssl3.a
%{_libdir}/libssl3.so
%{_libdir}64/libssl3.so
%{_libdir}/libsmime3.a 
%{_libdir}/libsmime3.so 
%{_libdir}64/libsmime3.so 
%{_libdir}/libsoftokn3.a
%{_libdir}/libsoftokn3.so
%{_libdir}64/libsoftokn3.so
%{_libdir}/libnssckbi.a
%{_libdir}/libnssckbi.so
%{_libdir}64/libnssckbi.so
%{_libdir}/libfreebl3.a
%{_libdir}/libfreebl3.so
%{_libdir}64/libfreebl3.so
##%{_libdir}/libsqlite3.a
%{_libdir}/libsqlite3.so
%{_libdir}64/libsqlite3.so
/usr/lib/libnss3.a
/usr/lib/libnss3.so
/usr/lib64/libnss3.so
/usr/lib/libnssutil3.a
/usr/lib/libnssutil3.so
/usr/lib64/libnssutil3.so
/usr/lib/libnssdbm3.a
/usr/lib/libnssdbm3.so
/usr/lib64/libnssdbm3.so
/usr/lib/libssl3.a
/usr/lib/libssl3.so
/usr/lib64/libssl3.so
/usr/lib/libsmime3.a 
/usr/lib/libsmime3.so 
/usr/lib64/libsmime3.so 
/usr/lib/libsoftokn3.a
/usr/lib/libsoftokn3.so
/usr/lib64/libsoftokn3.so
/usr/lib/libnssckbi.a
/usr/lib/libnssckbi.so
/usr/lib64/libnssckbi.so
/usr/lib/libfreebl3.a
/usr/lib/libfreebl3.so
/usr/lib64/libfreebl3.so
## /usr/lib/libsqlite3.a
/usr/lib/libsqlite3.so
/usr/lib64/libsqlite3.so
%{_bindir}/certutil
%{_bindir}/cmsutil
%{_bindir}/crlutil
%{_bindir}/modutil
%{_bindir}/pk12util
%{_bindir}/signtool
%{_bindir}/signver
%{_bindir}/ssltap
/usr/bin/certutil
/usr/bin/cmsutil
/usr/bin/crlutil
/usr/bin/modutil
/usr/bin/pk12util
/usr/bin/signtool
/usr/bin/signver
/usr/bin/ssltap
%{_bindir}/atob
%{_bindir}/btoa
%{_bindir}/derdump
%{_bindir}/ocspclnt
%{_bindir}/pp
%{_bindir}/selfserv
%{_bindir}/shlibsign
%{_bindir}/strsclnt
%{_bindir}/symkeyutil
%{_bindir}/tstclnt
%{_bindir}/vfyserv
%{_bindir}/vfychain

%files devel
%defattr(-,root,system)
%{_bindir}/nss-config*
%{_libdir}/nss3/*.a
%{_libdir}64/nss3/*.a
%{_includedir}/*
/usr/include/*
/usr/bin/nss-config*
/usr/lib/nss3/*.a
/usr/lib64/nss3/*.a


%changelog
* Mon Feb 25 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.14.3-1
- update to  3.14.3. Due to conflit with sqlite package, the library libsqlite3.a is not copied.

* Mon Mar 26 2012 Patricia Cugny <patricia.cugny@bull.net> 3.13.2-1
- update to  3.13.2

- .spec simplification
* Wed Feb 25 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.12-2
- ship libsqlite3
- add .so file in -devel rpm
- .spec simplification

* Wed Feb 25 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.12-1
- Initial port for AIX
