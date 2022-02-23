%{!?gcc_compiler: %define gcc_compiler 1} # Switch to GCC build
%{!?default_bits: %define default_bits 64}
%{!?dotests: %define dotests 1}

%global nss_major_version 3
%global nss_minor_version 43
%global nss_patch_version 0

%global nss_release_tag NSS_3_43_RTM
%global nss_archive_version %{nss_major_version}.%{nss_minor_version}

%global nspr_version 4.21
Summary:	Network Security Services
Name:		nss
Version:	%{nss_major_version}.%{nss_minor_version}.%{nss_patch_version}
Release:	3
License:	MPLv2.0
URL:		https://www.mozilla.org/projects/security/pki/nss/
Group:		System Environment/Libraries

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:		%{_prefix}

# Source0:	%{name}-%{version}-with-nspr-%{nspr_version}.tar.gz

# Source0:	https://ftp.mozilla.org/pub/security/nss/releases/%{nss_release_tag}/src/%{name}-%{nss_archive_version}.tar.gz

Source0:	https://ftp.mozilla.org/pub/security/nss/releases/%{nss_release_tag}/src/%{name}-%{nss_archive_version}-with-nspr-%{nspr_version}.tar.gz

Source1:	nss-config.in

Source20:    %{name}-%{version}-%{release}.build.log

Patch0: 	nss-3.43.0-aixbuild.patch
# Patch1: 	nss-3.27.1-namemax.patch
Patch1: 	nss-3.43.0-aixDl_info.patch
Patch2: 	nss-3.43.0-aixXLCbuild.patch

# Patches from Fedora
Patch10:	nss-539183.patch
Patch11:	nss-iquote.patch


Requires:       nspr >= %{nspr_version}
# Only needed if building from NSS tar file without NSPR or to find NSPR headers
BuildRequires:  nspr-devel >= %{nspr_version}

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509
v3 certificates, and other security standards.

%package devel
Summary:          Development libraries for Network Security Services
Group:            Development/Libraries
Requires:         nspr-devel = %{nspr_version}
# Only needed if building from NSS tar file without NSPR or to find NSPR headers
BuildRequires:    nspr-devel = %{nspr_version}

%description devel
Header and Library files for doing development with Network Security Services.

%prep
if [ "%{dotests}" == 1 ]; then
    if [ "${DOMSUF}" == "" ]; then
        echo "You need to set the DOMSUF environnment variable in order to run the tests."
        echo "It should be set so that ping \$HOST.\$DOMSUF works."
        exit 1
    fi
fi

%setup -q -n %{name}-%{nss_archive_version}

%patch0 -p1 -b .aixbuild
%patch1 -p1 -b .aixDl_info
%if %{gcc_compiler} == 0
%patch2 -p1 -b .aixXLCbuild
%endif

%patch10 -p1 -b .httpserv

# Following includes GCC -iquote option, may need adapted version for XLC
%if %{gcc_compiler} != 0
%patch11 -p1 -b .iquote
%endif

mkdir 32bit
cp -rp nspr nss 32bit
cp -rp 32bit 64bit


%build


# Environment variables from Fedora version 3.43

export FREEBL_NO_DEPEND=1

# Must export FREEBL_LOWHASH=1 for nsslowhash.h so that it gets
# copied to dist and the rpm install phase can find it
# This due of the upstream changes to fix
# https://bugzilla.mozilla.org/show_bug.cgi?id=717906
export FREEBL_LOWHASH=1

# uncomment if the iquote patch is activated
export IN_TREE_FREEBL_HEADERS_FIRST=1

# Following leads to  code requiring Dl_info
# export NSS_FORCE_FIPS=1

# Enable compiler optimizations and disable debugging code
export BUILD_OPT=1

# Uncomment to disable optimizations
#RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-O2/-O0/g'`
#export RPM_OPT_FLAGS

export NSS_ALLOW_SSLKEYLOGFILE=1

# Set the policy file location
# if set NSS will always check for the policy file and load if it exists
export POLICY_FILE="nss.config"
# location of the policy file
export POLICY_PATH="/opt/freeware/etc/crypto-policies/back-ends"



# Environment variables from previous version

# Ask to NOT build the libsqlite3.so !! (conflict !!)
export NSS_USE_SYSTEM_SQLITE=1

%if %{gcc_compiler} == 0
    export NS_AIX_XLC=1
%endif

export NSS_DISABLE_GTESTS=1

# Following only works if NSPR is built/installed beforehand
# The combined tar file has NSPR headers in ./nspr/lib/ds
export NSPR_INCLUDE_DIR=/opt/freeware/include/nspr4

export NSS_INCLUDES="-I/opt/freeware/include/nspr4 -I../../../dist/AIX6.1_64_OPT.OBJ/include -I../../../dist/public/nss -I../../../dist/private/nss"

build_nss() {
    set -x
    cd ${OBJECT_MODE}bit/nss
    echo `date +%Y%m%d_%H%M%S`" : Starting ${OBJECT_MODE}bit build"
    #NSS_INCLUDES=
    #for HEADER_DIR in `(for HEADER in \`find .. -name *.h\`; do dirname ${HEADER}; done) | sort -u`; do
    #    ABS_DIR=`pwd`/${HEADER_DIR}
    #    NSS_INCLUDES="-I ${ABS_DIR} ${NSS_INCLUDES}"
    #done
    #NSS_INCLUDES="-I `pwd`/../dist/AIX6.1_DBG.OBJ/include ${NSS_INCLUDES}"
    #export NSS_INCLUDES=${NSS_INCLUDES}
    
    gmake
    echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit build completed"
    
    if [ "%{dotests}" == 1 ]; then
        echo `date +%Y%m%d_%H%M%S`" : Starting ${OBJECT_MODE}bit tests"
        export LIBPATH=`pwd`/../dist/AIX6.1_DBG.OBJ/lib
        echo "HOST=${HOST} ; DOMSUF=${DOMSUF}"
        cd tests
        ./all.sh || true
        cd ..
        unset LIBPATH
        echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit tests completed"
    fi
    cd ../..
}

# first build the 64-bit version
export NSPR_LIB_DIR=/opt/freeware/lib64
export OBJECT_MODE=64
export USE_64=1
export LDFLAGS=" -L/usr/lib64 -lnspr4 "
build_nss

# now build the 32-bit version
export NSPR_LIB_DIR=/opt/freeware/lib
export OBJECT_MODE=32
unset USE_64
export LDFLAGS=" -L/usr/lib -lnspr4 "
build_nss

mkdir -p 32bit/dist/pkgconfig
cat %{SOURCE1} | sed -e "s,@libdir@,${_libdir},g" \
                     -e "s,@prefix@,%{_prefix},g" \
                     -e "s,@exec_prefix@,%{_prefix},g" \
                     -e "s,@includedir@,%{_includedir}/nss3,g" \
                     -e "s,@MOD_MAJOR_VERSION@,%{nss_major_version},g" \
                     -e "s,@MOD_MINOR_VERSION@,%{nss_minor_version},g" \
                     -e "s,@MOD_PATCH_VERSION@,%{nss_patch_version},g" \
                     > 32bit/dist/pkgconfig/nss-config

chmod 755 32bit/dist/pkgconfig/nss-config

%install
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar"

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

# process shared libraries (libsqlite3 removed from list)
# NSS libnssckbi has already been obsoleted by p11-kit-trust (removed from list)

for solibfile in libfreebl3 libfreeblpriv3 libnssutil3 libsoftokn3 libssl3 libnss3 libnssdbm3 libsmime3
do
	# copy shared objects
	install -p -m 755 32bit/dist/*.OBJ/lib/${solibfile}.so ${RPM_BUILD_ROOT}%{_libdir}
	install -p -m 755 64bit/dist/*.OBJ/lib/${solibfile}.so ${RPM_BUILD_ROOT}%{_libdir}64
	# build AIX shared libraries
	${AR} -X32 -rv ${RPM_BUILD_ROOT}%{_libdir}/${solibfile}.a 32bit/dist/*.OBJ/lib/${solibfile}.so
	${AR} -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/${solibfile}.a 64bit/dist/*.OBJ/lib/${solibfile}.so
done

# Add symlinks from 32 ../lib to ../lib64 bits
(
  cd ${RPM_BUILD_ROOT}%{_libdir}64

# NSS libnssckbi has already been obsoleted by p11-kit-trust (removed from list)

  for solibfile in libfreebl3 libfreeblpriv3 libnssutil3 libsoftokn3 libssl3 libnss3 libnssdbm3 libsmime3
  do
    ln -s %{_libdir}/${solibfile}.a .
  done
)

DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi
# process binaries files
for binfile in certutil cmsutil crlutil modutil pk12util \
	     atob btoa derdump ocspclnt pp selfserv shlibsign \
	     strsclnt symkeyutil tstclnt vfyserv vfychain \
	     signtool signver ssltap
do
	install -p -m 755 32bit/dist/*.OBJ/bin/${binfile} ${RPM_BUILD_ROOT}%{_bindir}/${binfile}_32
	install -p -m 755 64bit/dist/*.OBJ/bin/${binfile} ${RPM_BUILD_ROOT}%{_bindir}/${binfile}_64
    ln -s %{_bindir}/${binfile}_${DEFAULT_BITS}  ${RPM_BUILD_ROOT}%{_bindir}/${binfile}
done


# copy some other libraries
for file in libcrmf.a libnssb.a libnssckfw.a libnss.a libjar.a \
	     libnssutil.a libsmime.a libssl.a libnssdev.a libzlib.a
do
	install -p -m 644 32bit/dist/*.OBJ/lib/${file} ${RPM_BUILD_ROOT}%{_libdir}/nss3
	install -p -m 644 64bit/dist/*.OBJ/lib/${file} ${RPM_BUILD_ROOT}%{_libdir}64/nss3
done

# copy the include files
for file in 32bit/dist/public/nss/*.h 
do
	install -p -m 644 ${file} ${RPM_BUILD_ROOT}%{_includedir}/nss3
done

# copy the package configuration files
install -p -m 755 32bit/dist/pkgconfig/nss-config ${RPM_BUILD_ROOT}%{_bindir}/nss-config

# strip binaries                 
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/*_32 ${RPM_BUILD_ROOT}%{_bindir}/*_64 || :

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
%{_libdir}64/libnss3.a
%{_libdir}64/libnss3.so
%{_libdir}/libnssutil3.a
%{_libdir}/libnssutil3.so
%{_libdir}64/libnssutil3.a
%{_libdir}64/libnssutil3.so
%{_libdir}/libnssdbm3.a
%{_libdir}/libnssdbm3.so
%{_libdir}64/libnssdbm3.a
%{_libdir}64/libnssdbm3.so
%{_libdir}/libssl3.a
%{_libdir}/libssl3.so
%{_libdir}64/libssl3.a
%{_libdir}64/libssl3.so
%{_libdir}/libsmime3.a 
%{_libdir}/libsmime3.so 
%{_libdir}64/libsmime3.a
%{_libdir}64/libsmime3.so 
%{_libdir}/libsoftokn3.a
%{_libdir}/libsoftokn3.so
%{_libdir}64/libsoftokn3.a
%{_libdir}64/libsoftokn3.so
# %{_libdir}/libnssckbi.a
# %{_libdir}/libnssckbi.so
# %{_libdir}64/libnssckbi.a
# %{_libdir}64/libnssckbi.so
%{_libdir}/libfreebl3.a
%{_libdir}/libfreebl3.so
%{_libdir}64/libfreebl3.a
%{_libdir}64/libfreebl3.so
%{_libdir}/libfreeblpriv3.a
%{_libdir}/libfreeblpriv3.so
%{_libdir}64/libfreeblpriv3.a
%{_libdir}64/libfreeblpriv3.so
##%{_libdir}/libsqlite3.a
##%{_libdir}/libsqlite3.so
##%{_libdir}64/libsqlite3.a
##%{_libdir}64/libsqlite3.so
/usr/lib/libnss3.a
/usr/lib/libnss3.so
/usr/lib64/libnss3.a
/usr/lib64/libnss3.so
/usr/lib/libnssutil3.a
/usr/lib/libnssutil3.so
/usr/lib64/libnssutil3.a
/usr/lib64/libnssutil3.so
/usr/lib/libnssdbm3.a
/usr/lib/libnssdbm3.so
/usr/lib64/libnssdbm3.a
/usr/lib64/libnssdbm3.so
/usr/lib/libssl3.a
/usr/lib/libssl3.so
/usr/lib64/libssl3.a
/usr/lib64/libssl3.so
/usr/lib/libsmime3.a 
/usr/lib/libsmime3.so 
/usr/lib64/libsmime3.a
/usr/lib64/libsmime3.so 
/usr/lib/libsoftokn3.a
/usr/lib/libsoftokn3.so
/usr/lib64/libsoftokn3.a
/usr/lib64/libsoftokn3.so
# /usr/lib/libnssckbi.a
# /usr/lib/libnssckbi.so
# /usr/lib64/libnssckbi.a
# /usr/lib64/libnssckbi.so
# New in 3.43 libdir/nss/unsupported  ?
# < %dir %{unsupported_tools_directory}
# %{unsupported_tools_directory}/bltest
# %{unsupported_tools_directory}/ecperf
# %{unsupported_tools_directory}/fbectest
# %{unsupported_tools_directory}/fipstest
# %{unsupported_tools_directory}/shlibsign
/usr/lib/libfreebl3.a
/usr/lib/libfreebl3.so
/usr/lib64/libfreebl3.a
/usr/lib64/libfreebl3.so
/usr/lib/libfreeblpriv3.a
/usr/lib/libfreeblpriv3.so
/usr/lib64/libfreeblpriv3.a
/usr/lib64/libfreeblpriv3.so
## /usr/lib/libsqlite3.a
##/usr/lib/libsqlite3.so
##/usr/lib64/libsqlite3.a
##/usr/lib64/libsqlite3.so
%{_bindir}/certutil*
%{_bindir}/cmsutil*
%{_bindir}/crlutil*
%{_bindir}/modutil*
%{_bindir}/pk12util*
%{_bindir}/signtool*
%{_bindir}/signver*
%{_bindir}/ssltap*
/usr/bin/certutil
/usr/bin/cmsutil
/usr/bin/crlutil
/usr/bin/modutil
/usr/bin/pk12util
/usr/bin/signtool
/usr/bin/signver
/usr/bin/ssltap
%{_bindir}/atob*
%{_bindir}/btoa*
%{_bindir}/derdump*
%{_bindir}/ocspclnt*
%{_bindir}/pp*
%{_bindir}/selfserv*
%{_bindir}/shlibsign*
%{_bindir}/strsclnt*
%{_bindir}/symkeyutil*
%{_bindir}/tstclnt*
%{_bindir}/vfyserv*
%{_bindir}/vfychain*

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
* Fri Oct 25 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.43.0-3
- Corrections to include missing _32 and _64 bit utilities

* Fri Jul 19 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.43.0-2
- Modifications to build using GCC

* Tue Apr 09 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.43.0-1
- Update to version 3.43.0

* Thu Oct 20 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 3.27.1-1
- Update to version 3.27.1

* Thu Jun 30 2016 Tony Reix <tony.reix@bull.net> 3.14.3-2
- Due to conflict with sqlite package (breaking subversion), all libsqlite3* files are not built.

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
