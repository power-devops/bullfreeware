%{!?gcc_compiler: %define gcc_compiler 1}
%{!?dotests: %define dotests 1}
%{!?default_bits: %define default_bits 64}
# Use --define 'ibm_ssl 0' on the command line to use OpenSSL RPM instead of OpenSSL LPP
%{!?ibm_ssl: %define ibm_ssl 1}
# Use --define 'SSL 0' on the command line to disable SSL detection
%{!?SSL: %define SSL 1}
# Use --define 'LDAP 0' on the command line to disable LDAP
%{!?LDAP: %define LDAP 1}

%define release_number 1

# Building with ldaps requires a file named ldapssl.h that I did not find.
# configure : config.log : #include file <ldapssl.h> not found.
# Unsetting ldaps
# Use --define 'noldaps 1' on the command line to disable LDAPS
#%{!?noldaps:%define LDAPS 1}
#%{?noldaps:%define LDAPS 0}

Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name:    curl 
Version: 7.64.0
Release: %{release_number}%{!?noldap:ldap}%{!?nossl:ssl}
License: MIT
Group:   Applications/Internet
Source0: https://curl.haxx.se/download/%{name}-%{version}.tar.gz
# The file curl/curlbuild.h no longer exists
# It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
# Source1: curlbuild.h
Source2: %{name}-%{version}-%{release_number}.build.log

# No longer useful !
#Patch0:  %{name}-%{version}-events.patch

# Upstream patches provided by Fedora 31
# Fix zsh completion
Patch1:   0001-curl-7.64.0-zsh-completion.patch

# Fix NetworkManager file descriptor leaks (#1680198)
Patch2:   0002-curl-7.64.0-nm-fd-leak.patch


URL: https://curl.haxx.se/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

%if %{SSL} == 1
BuildRequires: openssl-devel >= 1.0.2g
%endif
BuildRequires: pkg-config, libidn-devel >= 1.24
BuildRequires: libssh2-devel >= 1.2.7, zlib-devel
BuildRequires: openldap-devel >= 2.4.24

%if %{SSL} == 1 && %{ibm_ssl} != 1
Requires: openssl >= 1.0.2g
%endif
Requires: libidn >= 1.24, zlib, libssh2 >= 1.2.7

%description
CURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

The library is available as 32-bit and 64-bit.

%if %{SSL} == 1
%if %{ibm_ssl} == 1
Note: this version is compiled with IBM SSL support.
%else
Note: this version is compiled with BullFreeware SSL support.
%endif
%else
Note: this version is compiled without SSL support.
%endif

%if %{LDAP} == 1
Note: this version is compiled with LDAP support.
%else
Note: this version is compiled without LDAP support.
%endif

%package devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries

Requires: %{name} = %{version}-%{release}
%if %{SSL} == 1 && %{ibm_ssl} != 1
Requires: openssl-devel >= 1.0.2g
%endif
Requires: libidn-devel, pkg-config, zlib-devel, libssh2-devel


%description devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The curl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.
libcurl is the core engine of curl; this packages contains all the
libs, headers, and manual pages to develop applications using libcurl.


%prep
%setup -q 
# No more useful !
#%patch0 -p1

# Upstream patches provided by Fedora 31
%patch1 -p1
%patch2 -p1


# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit

%build

PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
CONFIG_SHELL=/usr/bin/ksh
CONFIGURE_ENV_CONFIG_OPTIONS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar"

echo "SSL  : %{SSL}"
echo "LDAP : %{LDAP}"
echo "LDAPS: %{LDAPS}"
echo "ibm_ssl: %{ibm_ssl}"

	SSL_=--with-ssl
%if %{ibm_ssl} == 1
    SSL_=--with-ssl=/usr/lib
%endif
%if %{SSL} == 0
	SSL_=--without-ssl
%endif

%if %{LDAP} == 1 || %{LDAPS} == 1
 	LDAP_LIB=--with-ldap-lib=ldap
%endif

%if %{LDAP} == 1
	LDAP_=--enable-ldap
%else
	LDAP_=--disable-ldap
%endif

#%if %{LDAPS} == 1
#	LDAPS_=--enable-ldaps
#%else
#	LDAPS_=--disable-ldaps
#%endif

# Choose GCC or XLC
%if %{gcc_compiler} == 1

export CC="/opt/freeware/bin/gcc"

export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC --version

%else

export CC="/usr/vac/bin/xlc_r"

export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC -qversion

%endif

export CC32=" ${CC}  ${FLAG32}"
export CC64=" ${CC}  ${FLAG64}"

build_curl()
{
    cd ${OBJECT_MODE}bit
    ./configure \
        --prefix=%{_prefix} \
        --mandir=%{_prefix}/man \
        --libdir=$1 \
        --enable-shared --enable-static \
        --with-ca-path=/var/ssl/certs \
        $SSL_ \
        $LDAP_LIB $LDAP_ $LDAPS_

    %if %{SSL} == 1 && %{ibm_ssl} == 1
    mv lib/Makefile lib/Makefile.orig
    cat lib/Makefile.orig | sed -e "s/-lssl/\/usr\/lib\/libssl.a/" | sed -e "s/-lcrypto/\/usr\/lib\/libcrypto.a/" > lib/Makefile
    %endif

    # liblber is also required when building with LDAP support
    %if %{LDAP} == 1
    mv lib/Makefile lib/Makefile.orig
    cat lib/Makefile.orig | sed -e "s/-lldap/-lldap -llber/" > lib/Makefile
    %endif

    gmake %{?_smp_mflags}
    if [ "%{dotests}" == 1 ]; then
        (gmake -k check || true ; /usr/sbin/slibclean)
    fi
    cd ..
}


# first build the 64-bit version

export OBJECT_MODE=64
export CC=$CC64

export LDFLAGS=" -L`pwd`/lib/.libs"

build_curl %{_libdir}64


# now build the 32-bit version

export OBJECT_MODE=32
export CC=$CC32

export LDFLAGS=" -L`pwd`/lib/.libs"

build_curl %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR=/usr/bin/ar

install_curl()
{
    cd ${1}bit
    export OBJECT_MODE=${1}
    make DESTDIR=${RPM_BUILD_ROOT} install
    # strip and rename binary
    /usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/curl
    mv ${RPM_BUILD_ROOT}%{_bindir}/curl ${RPM_BUILD_ROOT}%{_bindir}/curl_${1}
# The file curl/curlbuild.h no longer exists
# It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
#    mv ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild-ppc${1}.h
    cd ..
}

#first install the 64 bit version
install_curl 64

# now install the 32 bit version
install_curl 32

# merge 32 and 64 bits into a single archive
${AR} -X64 -x ${RPM_BUILD_ROOT}%{_libdir}64/libcurl.a libcurl.so.4
${AR} -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/libcurl.a libcurl.so.4
ln -sf %{_libdir}/libcurl.a ${RPM_BUILD_ROOT}%{_libdir}64/libcurl.a

# The file curl/curlbuild.h no longer exists
# It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
# cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h

# Add symlinks for command without _32/_64 suffix
DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi
ln -sf curl_${DEFAULT_BITS} ${RPM_BUILD_ROOT}%{_bindir}/curl

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/README* 32bit/COPYING
%doc 32bit/docs/BUGS 32bit/docs/FAQ 32bit/docs/FEATURES
%doc 32bit/docs/MANUAL 32bit/docs/RESOURCES
%doc 32bit/docs/TheArtOfHttpScripting 32bit/docs/TODO
%{_bindir}/curl*
%{_libdir}/*.a
%{_mandir}/man1/curl.1
/usr/bin/curl*
/usr/lib/*.a
%if %{SSL} == 1
%doc 32bit/docs/SSLCERTS.md
%endif


%files devel
%defattr(-,root,system)
%doc 32bit/docs/examples/*.c 32bit/docs/examples/Makefile.example
%doc 32bit/docs/INTERNALS.md
%doc 32bit/docs/CONTRIBUTE.md 32bit/docs/libcurl/ABI
%{_bindir}/curl-config*
%{_includedir}/%{name}
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1
%{_mandir}/man3/*
/usr/bin/curl-config*
/usr/include/*
/usr/lib/*.la


%changelog
* Tue Dec 05 2017 Michael Wilson <michael.a.wilson@atos.net> - 7.64.0-1
- Update to version 7.64.0
- rpmbuild/brpm/rpm -ba must include  "--define 'ibm_ssl 0'"
- Build in src for curl-tool requires    LDFLAGS=" -L../lib/.libs"
-                                        export LDFLAGS=" -L`pwd`/lib/.libs"
- The file curl/curlbuild.h no longer exists
-    It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
- Based on changes in Fedora 31

* Mon Nov 07 2016 Tony Reix <tony.reix@atos.net> - 7.51.0-2
- Remove no more useful patch.

* Fri Nov 04 2016 Tony Reix <tony.reix@atos.net> - 7.51.0-1
- Update version to 7.51.0 .

* Tue Oct 13 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.50.3-1
- Updated to version 7.50.3
- Fixed missing LDAP support
- Default SSL certs repository is now /var/ssl/certs
- Default curl command is now 64 bits
- Built with GCC instead of xlC
- General spec file improvements

* Tue Mar 22 2016 Tony Reix <tony.reix@atos.net> - 7.47.1-2
- Update version to 7.47.2 on 32 and 64 bit, with/without ssl

* Mon Mar 21 2016 Tony Reix <tony.reix@atos.net> - 7.47.1-1
- Update version to 7.47.1 on 32 and 64 bit

* Wed Jul 01 2015 Tony Reix <tony.reix@atos.net> - 7.43.0-1
- Update version to 7.43.0 on 32 and 64 bit

* Mon Oct 22 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.28.0-1
- update version to 7.28.0 on 32 and 64 bit

* Thu Mar 29 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.21.4-2
- Port on Aix6.1

* Fri Mar 04 2011 Patricia Cugny <patricia.cugny@bull.net> - 7.21.4-1
- updated to version 7.21.4
- remove option to flip on/off compile with SSL.

* Mon Oct 27 2003 David Clissold <cliss@austin.ibm.com>
- Add option to flip on/off compile with SSL.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Apr 30 2002 David Clissold <cliss@austin.ibm.com>
- First version for AIX Toolbox.

