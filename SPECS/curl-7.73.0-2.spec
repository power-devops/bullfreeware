# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# By default, curl is built with SSL support
# To disable SSL, rpmbuild --without SSL *.spec
%bcond_without SSL

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL


%define		_libdir64 %{_prefix}/lib64

Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name:    curl
Version: 7.73.0
Release: 2
License: MIT
Group:   Applications/Internet
Source0: https://curl.haxx.se/download/%{name}-%{version}.tar.gz
Source2: %{name}-%{version}-%{release}.build.log

# Patch1:    %{name}-7.72.0-aix-poll.patch@

URL: https://curl.haxx.se/

%if %{with SSL} && %{without ibm_SSL}
BuildRequires: openssl-devel >= 1.0.2g
%endif

# BuildRequires: ca-certificates >= 2016.10.7
BuildRequires: libssh2-devel >= 1.2.7
BuildRequires: pkg-config, libidn-devel >= 1.24
BuildRequires: openldap-devel >= 2.4.24
BuildRequires: krb5-libs >= 1.16.1-2
BuildRequires: krb5-devel >= 1.16.1-2

Requires: libcurl = %{version}-%{release}

# Workaround to use AIX libssl.A and libcrypto.a needs OpenSource sed
BuildRequires: sed


%description
CURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

The library is available as 32-bit and 64-bit.

%if %{with SSL} == 1
%if %{with ibm_SSL} == 1
Note: this version is compiled with IBM SSL support.
%else
Note: this version is compiled with BullFreeware SSL support.
%endif
%else
Note: this version is compiled without SSL support.
%endif


%package -n libcurl
Summary: A library for getting files from web servers
Requires: zlib, libssh2 >= 1.2.7
%if %{with SSL} == 1 && %{without ibm_SSL}
Requires: openssl >= 1.0.2g
%endif
Obsoletes: curl < 7.72.0

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%if %{with SSL} == 1
%if %{with ibm_SSL} == 1
Note: this version is compiled with IBM SSL support.
%else
Note: this version is compiled with BullFreeware SSL support.
%endif
%else
Note: this version is compiled without SSL support.
%endif


%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries

Requires: libcurl = %{version}-%{release}
Requires: libssh2-devel
%if %{with SSL} && %{without ibm_SSL}
Requires: openssl-devel >= 1.0.2g
%endif
Provides: curl-devel = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}


%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.


%prep
%setup -q 

# %patch1 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build

PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
CONFIG_SHELL=/usr/bin/ksh
CONFIGURE_ENV_CONFIG_OPTIONS=/usr/bin/ksh
# export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"



# Choose GCC or XLC
%if %{with gcc_compiler}

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


build_curl()
{
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=$1 \
	--enable-shared --enable-static \
	--enable-manual \
	--enable-ldap \
	--with-libssh2 \
        --without-nghttp2 \
%if %{with SSL}
	--with-ssl=/usr \
	--with-ca-path=/var/ssl/certs/ \
	--with-ca-bundle=/var/ssl/cert.pem \
%else
	--without-ssl \
%endif

# Workaround in order to remove -L/opt/freeware/lib. Otherwize, the build will be done
# with the laready installed libcurl.a
sed -i  "s|-L/opt/freeware/lib||g" src/Makefile

# # # Deactivate Workaround
# # %if %{with SSL} && %{with ibm_SSL}
# # # Workaround to use AIX OpenSSL
# # find . -name "Makefile" | xargs /opt/freeware/bin/sed -i "s|-lssl -lcrypto|/usr/lib/libssl.a /usr/lib/libcrypto.a|g"
# # %endif

# # liblber is also required when building with LDAP support
# %if %{LDAP} == 1
# mv lib/Makefile lib/Makefile.orig
# cat lib/Makefile.orig | sed -e "s/-lldap/-lldap -llber/" > lib/Makefile
# %endif

gmake %{?_smp_mflags}
}


# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC=" ${CC}  ${FLAG64}"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
# export LDFLAGS=" -L`pwd`/lib/.libs"

build_curl %{_libdir64}


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC=" ${CC}  ${FLAG32}"

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
# export LDFLAGS=" -L`pwd`/lib/.libs"

build_curl %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar -X32_64"

# install_curl()
# {
#     cd ${1}bit
#     export OBJECT_MODE=${1}
#     make DESTDIR=${RPM_BUILD_ROOT} install
#     # strip and rename binary
#     /usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/curl
#     mv ${RPM_BUILD_ROOT}%{_bindir}/curl ${RPM_BUILD_ROOT}%{_bindir}/curl_${1}
# # The file curl/curlbuild.h no longer exists
# # It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
# #    mv ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild-ppc${1}.h
#     cd ..
# }

# install on 64bit mode
cd 64bit
export OBJECT_MODE=64
make DESTDIR=%{buildroot} install-strip

(
cd  ${RPM_BUILD_ROOT}/%{_bindir}
for fic in $(ls -1| grep -v -e _32 -e _64)
do
	mv $fic "$fic"_64
done
)

# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
make DESTDIR=%{buildroot} install-strip

(
cd  ${RPM_BUILD_ROOT}/%{_bindir}
for fic in $(ls -1| grep -v -e _32 -e _64)
do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
done
)

# merge 32 and 64 bits into a single archive
${AR} -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libcurl.a libcurl.so.4
${AR} -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/libcurl.a libcurl.so.4
ln -sf %{_libdir}/libcurl.a ${RPM_BUILD_ROOT}%{_libdir64}/libcurl.a

# The file curl/curlbuild.h no longer exists
# It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
# cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/README* 32bit/COPYING
%doc 32bit/docs/BUGS* 32bit/docs/FAQ* 32bit/docs/FEATURES*
%doc 32bit/docs/TheArtOfHttpScripting*
%doc 32bit/docs/TODO*
%{_bindir}/curl*
%{_mandir}/man1/curl.1
%if %{with SSL}
%doc 32bit/docs/SSLCERTS.md
%endif

%files -n libcurl
%defattr(-,root,system)
%doc 32bit/COPYING
%{_libdir}/*.a

%files -n libcurl-devel
%defattr(-,root,system)
%doc 32bit/docs/examples/*.c 32bit/docs/examples/Makefile.example
%doc 32bit/docs/INTERNALS.md
%doc 32bit/docs/CONTRIBUTE.md 32bit/docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/%{name}
# %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1
%{_mandir}/man3/*


%changelog
* Tue Dec 08 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 7.73.0-2
- Correct certificate location.

* Tue Oct 27 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 7.73.0-1
- Update to 7.73.0
- Docs files have changed

* Thu Oct 08 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 7.72.0-2
- Update to 7.72.0

* Fri Oct 02 2020 Étienne Guesnet etienne.guesnet.external@atos.net> - 7.72.0-1
- Update to 7.72.0
- Add libcurl subpackage

* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 7.68.0-1
- New version 7.68.0
- Bullfreeware OpenSSL removal

* Fri Dec 13 2019 Clément Chigot <clement.chigot@atos.net> - 7.67.0-1
- BullFreeware Compatibility Improvements
- Update to version 7.67.0
- Built with IBM SSL by default
- Remove BuildRoot
- Built with GSS-Negotiate Support
- Remove /usr links
- Remove libidn dependency
   Only libidn2 is supported now, but we do not have at the moment.

* Tue Dec 05 2017 Michael Wilson <michael.a.wilson@atos.net> - 7.64.0-1
- Update to version 7.64.0
- rpmbuild/brpm/rpm -ba must include  "--define 'ibm_SSL 0'"
- Build in src for curl-tool requires    LDFLAGS=" -L../lib/.libs"
-                                        export LDFLAGS=" -L`pwd`/lib/.libs"
- The file curl/curlbuild.h no longer exists
-    It is replaced by curl/system.h which tests for __LP64__ __ppc__ __ppc64__
- Based on changes in Fedora 31

* Mon Nov 07 2016 Tony Reix <tony.reix@atos.net> - 7.51.0-2
- Remove no more useful patch.

* Fri Nov 04 2016 Tony Reix <tony.reix@atos.net> - 7.51.0-1
- Update version to 7.51.0 .

* Thu Oct 13 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.50.3-1
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

