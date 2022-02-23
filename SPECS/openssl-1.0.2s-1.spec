# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# Version with/without SSLv2
# By default, SSLv2 is added
# No tests: rpmbuild -ba --without sslv2 *.spec
%bcond_without sslv2

%define opensslversion 1.0.2

%define openssldir   /var/ssl
%define openssldir64 /var/ssl/64

Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl
Version: %{opensslversion}s
%define baserelease 1
Release: %{baserelease}%{?with_sslv2:withsslv2}

Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc
Source3:	%{name}-%{version}.tar.gz.sha1
Source4:	%{name}-%{version}.tar.gz.sha256
Source5:	libcrypto.so.0.9.7-aix32
Source6:	libcrypto.so.0.9.7-aix64
Source7:	libssl.so.0.9.7-aix32
Source8:	libssl.so.0.9.7-aix64
Source9:	libcrypto.so.0.9.8-aix32
Source10:	libcrypto.so.0.9.8-aix64
Source11:	libssl.so.0.9.8-aix32
Source12:	libssl.so.0.9.8-aix64
Source13:	libcrypto.so.1.0.0-aix32
Source14:	libcrypto.so.1.0.0-aix64
Source15:	libssl.so.1.0.0-aix32
Source16:	libssl.so.1.0.0-aix64


# baserelease instead of release
# Required, because *.build.log file is built by brpm before the .spec file
Source100:	%{name}-%{version}-%{baserelease}.build.log
# $SOURCES/openssl-1.0.2m-1withsslv2.build.log
# $SOURCES/openssl-1.0.2m-1.build.log


# Taken from 1.0.1u :
Source17: libcrypto.so.1.0.1-aix32
Source18: libcrypto.so.1.0.1-aix64
Source19: libssl.so.1.0.1-aix32
Source20: libssl.so.1.0.1-aix64
#
# Use script:
#	RPMPATH=/opt/freeware/src/packages/RPMS/ppc/openssl-1.0.1t-1.aix6.1.ppc.rpm
#	SOURCES=/opt/freeware/src/packages/SOURCES
#	cd /tmp
#	for bits in lib lib64
#	do
#	  for lib in crypto ssl
#	  do
#	        rpm2cpio $RPMPATH | /opt/freeware/bin/cpio -idv opt/freeware/$bits/lib$lib.so.1.0.1
#	  done
#	done
#	  for lib in crypto ssl
#	  do
#	        cp opt/freeware/lib/lib$lib.so.1.0.1   $SOURCES/lib$lib.so.1.0.1-aix32
#	        cp opt/freeware/lib64/lib$lib.so.1.0.1 $SOURCES/lib$lib.so.1.0.1-aix64
#	  done


Patch0: %{name}-%{version}-Configure-xlc.patch
Patch1: %{name}-%{version}-Configure-LIBPATH-with-opt-freeware.patch

License: OpenSSL License
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/
Obsoletes: openssl64


# This IS for compatibility for version 0.9.7 of libssl.so which searches for
# libcrypto.so.0.9.7 in libcrypto.a in PATH:/opt/freeware/64/lib:/usr/lib :
# INDEX  PATH                          BASE                MEMBER              
# 0      /opt/freeware/64/lib:/usr/lib                                         
# 1                                    libcrypto.a         libcrypto.so.0.9.7  
%define _prefix64 %{_prefix}/64
# Now, only a link is required:
#	/opt/freeware/64/lib/libcrypto.a -> ../../lib/libcrypto.a


%define _libdir64 %{_prefix}/lib64

BuildRequires: make
BuildRequires: perl


%description
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A. Young
and Tim J. Hudson.  OpenSSL is licensed under the OpenSSL License, included in
this package.

This package contains the base OpenSSL cryptography and SSL/TLS libraries and
tools.

You should also install a pseudo-random number generator such as EGD or prngd
if you do not have a /dev/urandom and /dev/random.

The library is available as 32-bit and 64-bit.

%if %{with sslv2}
Note: this version is compiled with SSLv2 support.
However, it is only aimed to help when linking with tools that need SSLv2 at build time.
Do not use it !
%else
Note: this version is compiled without SSLv2 support.
%endif


%package devel
Summary: Secure Sockets Layer and cryptography static libraries and headers
Group: Development/Libraries
Requires: %{name} = %{version}
Obsoletes: openssl64-devel

%description devel
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A. Young
and Tim J. Hudson.  OpenSSL is licensed under the OpenSSL License, included in
this package.

This package contains the the OpenSSL cryptography and SSL/TLS static libraries
and header files required when developing applications.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".

%if %{with sslv2}
Note: this version is compiled with SSLv2 support.
However, it is only aimed to help when linking with tools that need SSLv2 at build time.
Do not use it !
%else
Note: this version is compiled without SSLv2 support.
%endif


%package doc
Summary: OpenSSL miscellaneous files
Group: Documentation
Requires: %{name} = %{version}
Obsoletes: openssl64-doc

%description doc
The OpenSSL Project is a collaborative effort to develop a robust,
commercial-grade, fully featured, and Open Source toolkit implementing the
Secure Sockets Layer (SSL v2/v3) and Transport Layer Security (TLS v1)
protocols as well as a full-strength general purpose cryptography library.
The project is managed by a worldwide community of volunteers that use the
Internet to communicate, plan, and develop the OpenSSL tookit and its related
documentation.

OpenSSL is based on the excellent SSLeay library developed from Eric A. Young
and Tim J. Hudson.  OpenSSL is licensed under the OpenSSL License, included in
this package.

This package contains the the OpenSSL cryptography and SSL/TLS extra
documentation and POD files from which the man pages were produced.


%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name} = %{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q
%patch0
%patch1

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build

export AR="/usr/bin/ar"
%if %{with gcc_compiler}
export CC="/opt/freeware/bin/gcc"
%else
export CC="/opt/IBM/xlC/13.1.3/bin/xlc"
%endif
LDFLAGS="-L."

# SSLv2 !
# Fedora 23 1.0.2g spec file
#       http://pkgs.fedoraproject.org/cgit/rpms/openssl.git/tree/openssl.spec
#       http://pkgs.fedoraproject.org/cgit/rpms/openssl.git/tree/openssl-1.0.2g-disable-sslv2v3.patch
#	http://www.theregister.co.uk/2016/03/01/drown_crypto_flaw_analysis/
#
#       # ia64, x86_64, ppc are OK by default
#       # Configure the build tree.  Override OpenSSL defaults with known-good defaults
#       # usable on all platforms.  The Configure script already knows to use -fPIC and
#       # RPM_OPT_FLAGS, so we can skip specifiying them here.
#       ./Configure \
#               --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
#               --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
#               zlib sctp enable-camellia enable-seed enable-tlsext enable-rfc3779 \
#               enable-cms enable-md2 enable-ssl2 \
#               no-mdc2 no-rc5 no-ec2m no-gost no-srp \
#               --with-krb5-flavor=MIT --enginesdir=%{_libdir}/openssl/engines \
#               --with-krb5-dir=/usr shared  ${sslarch} %{?!nofips:fips}

%if %{with sslv2}
        SSLV2_=enable-ssl2
%endif


# Issue with 1.0.2f:    no-symlinks  !
# first build the 64-bit version
# 1.0.2g : config says:     no-ssl2         [default]  OPENSSL_NO_SSL2 (skip dir)


# first build the 64-bit version
cd 64bit
/usr/bin/perl util/perlpath.pl /usr/bin/perl

export OBJECT_MODE=64
./Configure \
    no-idea no-mdc2 no-rc5 \
    -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir64} \
    $SSLV2_ \
%if %{with gcc_compiler}
    aix64-gcc
%else
    aix64-xlc_r
%endif

gmake depend

gmake build_libs


# We can't simply remove no-shared from Configure and build .a libraries with the .so
# automatically built, because libcrypto.so (and not libcrypto.a) will be imported
# by libssl.so
mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libcrypto.a
%if %{with gcc_compiler}
${CC} -maix64 -shared *.o -o ../libcrypto.so.%{opensslversion} -Wl,-bexpall -Wl,-bernotok -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%else
${CC} -qmkshrobj *.o -o ../libcrypto.so.%{opensslversion} -bexpall -bernotok -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%endif
cd ..
rm -rf libcrypto.a .tmplibdir
/usr/bin/ar -rv libcrypto.a libcrypto.so.%{opensslversion}

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libssl.a
%if %{with gcc_compiler}
${CC} -maix64 -shared *.o -o ../libssl.so.%{opensslversion} -Wl,-bexpall -Wl,-bernotok -L.. -lcrypto -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%else
${CC} -qmkshrobj *.o -o ../libssl.so.%{opensslversion} -bexpall -bernotok -L.. -lcrypto -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%endif
cd ..
rm -rf libssl.a .tmplibdir
/usr/bin/ar -rv libssl.a libssl.so.%{opensslversion}

gmake


# now build the 32-bit version
cd ../32bit
/usr/bin/perl util/perlpath.pl /usr/bin/perl

export OBJECT_MODE=32
./Configure \
    no-idea no-mdc2 no-rc5 \
    -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir} \
    $SSLV2_ \
%if %{with gcc_compiler}
    aix-gcc
%else
    aix-xlc_r
%endif

gmake depend

gmake build_libs



# We can't simply remove no-shared from Configure and build .a libraries with the .so
# automatically built, because libcrypto.so (and not libcrypto.a) will be imported
# by libssl.so
mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libcrypto.a
%if %{with gcc_compiler}
${CC} -shared *.o -o ../libcrypto.so.%{opensslversion} -Wl,-bexpall -Wl,-bernotok -Wl,-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib:/lib
%else
${CC} -qmkshrobj *.o -o ../libcrypto.so.%{opensslversion} -bexpall -bernotok -blibpath:/opt/freeware/lib:/usr/lib:/lib
%endif
cd ..
rm -rf libcrypto.a .tmplibdir
/usr/bin/ar -rv libcrypto.a libcrypto.so.%{opensslversion}

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libssl.a
%if %{with gcc_compiler}
${CC} -shared *.o -o ../libssl.so.%{opensslversion} -Wl,-bexpall -Wl,-bernotok -L.. -lcrypto -Wl,-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib:/lib
%else
${CC} -qmkshrobj *.o -o ../libssl.so.%{opensslversion} -bexpall -bernotok -L.. -lcrypto -blibpath:/opt/freeware/lib:/usr/lib:/lib
%endif
cd ..
rm -rf libssl.a .tmplibdir
/usr/bin/ar -rv libssl.a libssl.so.%{opensslversion}

gmake
/usr/sbin/slibclean

# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
/usr/bin/ar -X64 -q libcrypto.a ../64bit/libcrypto.so.%{opensslversion}
/usr/bin/ar -X64 -q libssl.a    ../64bit/libssl.so.%{opensslversion}


# Add the older 0.9.7l, 0.9.8x, 1.0.0j, and 1.0.1r shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')

# crypto 32bits
cp %{SOURCE5} libcrypto.so.0.9.7
/usr/bin/strip -X32 -e libcrypto.so.0.9.7
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE9} libcrypto.so.0.9.8
/usr/bin/strip -X32 -e libcrypto.so.0.9.8
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.0.9.8
cp %{SOURCE13} libcrypto.so.1.0.0
/usr/bin/strip -X32 -e libcrypto.so.1.0.0
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.1.0.0
cp %{SOURCE17} libcrypto.so.1.0.1
/usr/bin/strip -X32 -e libcrypto.so.1.0.1
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.1.0.1

# crypto 64bits
cp %{SOURCE6} libcrypto.so.0.9.7
/usr/bin/strip -X64 -e libcrypto.so.0.9.7
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE10} libcrypto.so.0.9.8
/usr/bin/strip -X64 -e libcrypto.so.0.9.8
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.0.9.8
cp %{SOURCE14} libcrypto.so.1.0.0
/usr/bin/strip -X64 -e libcrypto.so.1.0.0
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.1.0.0
cp %{SOURCE18} libcrypto.so.1.0.1
/usr/bin/strip -X64 -e libcrypto.so.1.0.1
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.1.0.1

# ssl 32bits
cp %{SOURCE7} libssl.so.0.9.7
/usr/bin/strip -X32 -e libssl.so.0.9.7
/usr/bin/ar -X32 -q libssl.a libssl.so.0.9.7
cp %{SOURCE11} libssl.so.0.9.8
/usr/bin/strip -X32 -e libssl.so.0.9.8
/usr/bin/ar -X32 -q libssl.a libssl.so.0.9.8
cp %{SOURCE15} libssl.so.1.0.0
/usr/bin/strip -X32 -e libssl.so.1.0.0
/usr/bin/ar -X32 -q libssl.a libssl.so.1.0.0
cp %{SOURCE19} libssl.so.1.0.1
/usr/bin/strip -X32 -e libssl.so.1.0.1
/usr/bin/ar -X32 -q libssl.a libssl.so.1.0.1

# ssl 64bits
cp %{SOURCE8} libssl.so.0.9.7
/usr/bin/strip -X64 -e libssl.so.0.9.7
/usr/bin/ar -X64 -q libssl.a libssl.so.0.9.7
cp %{SOURCE12} libssl.so.0.9.8
/usr/bin/strip -X64 -e libssl.so.0.9.8
/usr/bin/ar -X64 -q libssl.a libssl.so.0.9.8
cp %{SOURCE16} libssl.so.1.0.0
/usr/bin/strip -X64 -e libssl.so.1.0.0
/usr/bin/ar -X64 -q libssl.a libssl.so.1.0.0
cp %{SOURCE20} libssl.so.1.0.1
/usr/bin/strip -X64 -e libssl.so.1.0.1
/usr/bin/ar -X64 -q libssl.a libssl.so.1.0.1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export OBJECT_MODE=64
cd 64bit
gmake INSTALL_PREFIX=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install

export OBJECT_MODE=32
cd ../32bit
gmake INSTALL_PREFIX=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install


strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
# Warning about c_rehash, which is a shell script. Not an issue.

# Move runable perl scripts to bindir and remove 64bit version
mv $RPM_BUILD_ROOT%{openssldir}/misc/*.pl $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{openssldir}/misc/tsget $RPM_BUILD_ROOT%{_bindir}
rm $RPM_BUILD_ROOT%{openssldir64}/misc/*.pl
rm $RPM_BUILD_ROOT%{openssldir64}/misc/tsget


# Make backwards-compatibility symlink to ssleay
ln -s openssl ${RPM_BUILD_ROOT}%{_bindir}/ssleay


# add 32-bit run-time-linker libraries
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -X32 -x libcrypto.a
/usr/bin/ar -X32 -x libssl.a
ln -s libcrypto.so.%{opensslversion} libcrypto.so
ln -s libssl.so.%{opensslversion} libssl.so


# add 64-bit run-time-linker libraries
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/
cd       ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 -x ../lib/libcrypto.a
/usr/bin/ar -X64 -x ../lib/libssl.a
ln -s libcrypto.so.%{opensslversion} libcrypto.so
ln -s libssl.so.%{opensslversion} libssl.so


# Add link from 64bit libraries to 32bit libraries
cd       ${RPM_BUILD_ROOT}%{_libdir64}
rm -f libcrypto.a
rm -f libssl.a
ln -s ../lib/libcrypto.a libcrypto.a
ln -s ../lib/libssl.a    libssl.a

# Don't make /usr/linux anymore.
# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin lib lib64 include
#   do
#     mkdir -p usr/linux/${dir}
#     cd usr/linux/${dir}
#     ln -sf ../../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )


# Compatibility with libssl.so.0.9.7
# add links for 64-bit library members
(
  mkdir -p ${RPM_BUILD_ROOT}%{_prefix64}/lib
  cd ${RPM_BUILD_ROOT}%{_prefix64}/lib
  ln -s ../../lib/*.a .
)


# rename ${RPM_BUILD_ROOT}%{_mandir}/man3/threads.3 as it might conflict with
# man3/threads.3 from perl
cd ${RPM_BUILD_ROOT}%{_mandir}/man3
mv -f threads.3 threads.3ssl


# strip -e ALL .so files but the libssl.so.1.0.2 in libssl.a & libcrypto.a !!
# The goal is to deliver only ONE .so... file un-stripped-e :
#	ONLY libssl.so.1.0.2 in libssl.a !!!
# so that dependent packages build dependency on libssl.so.1.0.2 ONLY !
# (dependency on libssl.so leads to confusion with versions 1.0 and 1.1 !!)
strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/libssl.so*
strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/libcrypto.so*
strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/libssl.so*
strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/libcrypto.so*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Without the "export LIBPATH=...", "gmake test" makes the zlib test to fail with:
# 1152921504606846944:error:25066067:DSO support routines:DLFCN_LOAD:could not load the shared library:dso_dlfcn.c:187:filename(libz.so): Could not load module /usr/lib/libz.so.
#      System error: Exec format error
# in 64bits ONLY !!
# Replacing /opt/freeware/lib/libz.so.1 by /opt/freeware/lib64/libz.so.1 shows that the test loads the32bit libz.so.1 instead of the 64bits.
# OLDLIBPATH=$LIBPATH
# export LIBPATH=/opt/freeware/lib64/
cd 64bit
(gmake -k test || true)
# export LIBPATH=$OLDLIBPATH
/usr/sbin/slibclean

cd ../32bit
(gmake -k test || true)
/usr/sbin/slibclean

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/CHANGES.SSLeay 32bit/LICENSE 32bit/NEWS 32bit/README 32bit/FAQ
%config %attr(0644,root,system) %{openssldir}/openssl.cnf
%dir %attr(0755,root,system) %{openssldir}/certs
%dir %attr(0755,root,system) %{openssldir}/misc
%dir %attr(0750,root,system) %{openssldir}/private
%{openssldir}/misc/*
%{_bindir}/*
%exclude %{_bindir}/c_rehash
%exclude %{_bindir}/*.pl
%exclude %{_bindir}/tsget
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
# Compatibility with libssl.so.0.9.7 with %{_prefix64}/lib
%dir %attr(755,bin,bin) %{_prefix64}
%dir %attr(755,bin,bin) %{_prefix64}/lib
%{_prefix64}/lib/*.a
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%exclude %{_mandir}/man1*/*.pl*
%exclude %{_mandir}/man1*/c_rehash*
%exclude %{_mandir}/man1*/tsget*
%exclude %{_mandir}/man1*/openssl-tsget*

%files devel
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/CHANGES.SSLeay 32bit/LICENSE 32bit/NEWS 32bit/README
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files doc
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/CHANGES.SSLeay 32bit/LICENSE 32bit/NEWS 32bit/README
%doc 32bit/doc
%{_mandir}/man3/*


%files perl
%{_bindir}/c_rehash
%{_bindir}/*.pl
%{_bindir}/tsget
%{_mandir}/man1*/*.pl*
%{_mandir}/man1*/c_rehash*
%{_mandir}/man1*/tsget*
%{_mandir}/man1*/openssl-tsget*

%changelog
* Fri Aug 02 2019 Clément Chigot <clement.chigot@atos.net> - 1.0.2s-1
- Update to version 1.0.2s
- Add openssl-perl package
- Change absolute path links to relative path
- Move from XLC to gcc
- Remove /usr/linux links

* Tue Nov 21 2017 Tony Reix <tony.reix@atos.net> - 1.0.2m-1
- Update to version 1.0.2m on AIX 6.1
- Add link from lib/lib*.a to lib64/lib*.a and deliver them.

* Tue May 30 2017 Tony Reix <tony.reix@atos.net> - 1.0.2l-1
- Update to version 1.0.2l on AIX 6.1

* Fri Jan 27 2017 Tony Reix <tony.reix@atos.net> - 1.0.2k-1
- Update to version 1.0.2k on AIX 6.1

* Thu Nov 24 2016 Tony Reix <tony.reix@atos.net> - 1.0.2j-2
- Big change:
  strip -e ALL .so files but the libssl.so.1.0.2 in libssl.a & libcrypto.a !!

* Mon Sep 26 2016 Tony Reix <tony.reix@atos.net> - 1.0.2j-1
- Version 1.0.2i  MUST be replaced by version 1.0.2j !

* Thu Sep 22 2016 Tony Reix <tony.reix@atos.net> - 1.0.2i-1
- Update to version 1.0.2i on AIX 6.1

* Tue May 10 2016 Tony Reix <tony.reix@atos.net> - 1.0.2h-2
- Change 32/64bits management

* Mon May 09 2016 Tony Reix <tony.reix@atos.net> - 1.0.2h-1
- Update to version 1.0.2h on AIX 6.1

* Thu Mar 24 2016 Tony Reix <tony.reix@atos.net> - 1.0.2g-3
- Add dependency of openssl RPM on Perl for: c_rehash.

* Wed Feb 03 2016 Tony Reix <tony.reix@atos.net> - 1.0.2f-2
- Fix issues with version of libraries (was 1.0.1 instead of 1.0.2)

* Tue Feb 02 2016 Tony Reix <tony.reix@atos.net> - 1.0.2f-1
- Update to version 1.0.2f on AIX 6.1

* Mon Aug 10 2015 Tony Reix <tony.reix@atos.net> - 1.0.2d-1
- Update to version 1.0.2d on Aix6.1

* Fri Aug 07 2015 Tony Reix <tony.reix@atos.net> - 1.0.1p-1
- Update to version 1.0.1p on Aix6.1

* Tue Apr 15 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.1g-1
- Update to version 1.0.1g on Aix6.1

* Thu Jul 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.1e-3
- Update to version 1.0.1e on Aix6.1

* Mon Mar 25 2013 Michael Perzl <michael@perzl.org> - 1.0.1e-2
- changed the way how the shared objects are generated as some functions
  where not exported otherwise

* Mon Feb 18 2013 Michael Perzl <michael@perzl.org> - 1.0.1e-1
- updated to version 1.0.1e

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  1.0.0d-2
- Initial port on Aix6.1

* Wed Oct 05 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.0d-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Jun 10 2011 Gerard Visiedo <gerard.visiedo@bull.net>  1.0.0d-1
- Initial port on Aix5.3
