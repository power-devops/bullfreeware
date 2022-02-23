
%define opensslversion 1.0.2

%define openssldir   /var/ssl
%define openssldir64 /var/ssl/64

Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl
Version: %{opensslversion}g
Release: 1

Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{version}.tar.gz.asc
#  File: %{name}-%{version}.tar.gz.md5  is no more provided by OpenSSL project
Source3: %{name}-%{version}.tar.gz.sha1
Source4: %{name}-%{version}.tar.gz.sha256
Source5: libcrypto.so.0.9.7-aix32
Source6: libcrypto.so.0.9.7-aix64
Source7: libssl.so.0.9.7-aix32
Source8: libssl.so.0.9.7-aix64
Source9: libcrypto.so.0.9.8-aix32
Source10: libcrypto.so.0.9.8-aix64
Source11: libssl.so.0.9.8-aix32
Source12: libssl.so.0.9.8-aix64
Source13: libcrypto.so.1.0.0-aix32
Source14: libcrypto.so.1.0.0-aix64
Source15: libssl.so.1.0.0-aix32
Source16: libssl.so.1.0.0-aix64
# Taken from 1.0.1s :
Source17: libcrypto.so.1.0.1-aix32
Source18: libcrypto.so.1.0.1-aix64
Source19: libssl.so.1.0.1-aix32
Source20: libssl.so.1.0.1-aix64

Patch0: %{name}-%{version}-Configure.patch
Patch1: %{name}-%{version}-aix.patch

License: OpenSSL License
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: openssl64
%define _prefix64 %{_prefix}/64

%define _libdir64 %{_prefix}/lib64

BuildRequires: make

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


%prep
%setup -q
%patch0
%patch1


%build 
/usr/bin/perl util/perlpath.pl /usr/bin/perl

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r"
LDFLAGS="-L."

# What Fedora does (from openssl-1.0.2d-2.fc23.src.rpm):
#       # ia64, x86_64, ppc are OK by default
#       # Configure the build tree.  Override OpenSSL defaults with known-good defaults
#       # usable on all platforms.  The Configure script already knows to use -fPIC and
#       # RPM_OPT_FLAGS, so we can skip specifiying them here.
#       ./Configure \
#               --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
#               --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
#               zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
#               enable-cms enable-md2 no-mdc2 no-rc5 no-ec2m no-gost no-srp \
#               --with-krb5-flavor=MIT --enginesdir=%{_libdir}/openssl/engines \
#               --with-krb5-dir=/usr shared  ${sslarch} %{?!nofips:fips}

# Issue with 1.0.2f:    no-symlinks  !
# first build the 64-bit version
export OBJECT_MODE=64
./Configure \
    no-idea no-mdc2 no-rc5 \
    -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir64} \
    aix64-xlc_r
gmake depend
gmake build_libs

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libcrypto.a
${CC} -qmkshrobj *.o -o ../libcrypto.so.%{opensslversion} -bexpall -bernotok
cd ..
rm -rf libcrypto.a .tmplibdir
/usr/bin/ar -rv libcrypto.a libcrypto.so.%{opensslversion}

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libssl.a
${CC} -qmkshrobj *.o -o ../libssl.so.%{opensslversion} -bexpall -bernotok -L.. -lcrypto -blibpath:/opt/freeware/lib:/usr/lib:/lib 
cd ..
rm -rf libssl.a .tmplibdir
/usr/bin/ar -rv libssl.a libssl.so.%{opensslversion}

gmake


# Without the "export LIBPATH=...", "gmake test" makes the zlib test to fail with:
# 1152921504606846944:error:25066067:DSO support routines:DLFCN_LOAD:could not load the shared library:dso_dlfcn.c:187:filename(libz.so): Could not load module /usr/lib/libz.so.
#      System error: Exec format error
# in 64bits ONLY !!
# Replacing /opt/freeware/lib/libz.so.1 by /opt/freeware/lib64/libz.so.1 shows that the test loads the32bit libz.so.1 instead of the 64bits.
OLDLIBPATH=$LIBPATH
export LIBPATH=/opt/freeware/lib64/
gmake test
export LIBPATH=$OLDLIBPATH


mkdir -p 64
mv libcrypto.so.%{opensslversion} libssl.so.%{opensslversion} 64/
gmake clean


# What Fedora does (from openssl-1.0.2d-2.fc23.src.rpm):
#       # ia64, x86_64, ppc are OK by default
#       # Configure the build tree.  Override OpenSSL defaults with known-good defaults
#       # usable on all platforms.  The Configure script already knows to use -fPIC and
#       # RPM_OPT_FLAGS, so we can skip specifiying them here.
#       ./Configure \
#               --prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
#               --system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
#               zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
#               enable-cms enable-md2 no-mdc2 no-rc5 no-ec2m no-gost no-srp \
#               --with-krb5-flavor=MIT --enginesdir=%{_libdir}/openssl/engines \
#               --with-krb5-dir=/usr shared  ${sslarch} %{?!nofips:fips}

# now build the 32-bit version
export OBJECT_MODE=32
./Configure \
    no-idea no-mdc2 no-rc5 \
    -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir} \
    aix-xlc_r

gmake depend
gmake build_libs

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libcrypto.a
${CC} -qmkshrobj *.o -o ../libcrypto.so.%{opensslversion} -bexpall -bernotok
cd ..
rm -rf libcrypto.a .tmplibdir
/usr/bin/ar -rv libcrypto.a libcrypto.so.%{opensslversion}

mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libssl.a
${CC} -qmkshrobj *.o -o ../libssl.so.%{opensslversion} -bexpall -bernotok -L.. -lcrypto -blibpath:/opt/freeware/lib:/usr/lib:/lib
cd ..
rm -rf libssl.a .tmplibdir
/usr/bin/ar -rv libssl.a libssl.so.%{opensslversion}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q libcrypto.a 64/libcrypto.so.%{opensslversion}
/usr/bin/ar -X64 -q libssl.a 64/libssl.so.%{opensslversion}

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

# apps/openssl still has the wrong shared library paths, we have to relink it
rm -f apps/openssl
gmake LDFLAGS="-L. -L.. $LDFLAGS" LIBSSL=" -L/opt/freeware/lib -lssl" LIBCRYPTO="-L/opt/freeware/lib -lcrypto"

gmake test


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake INSTALL_PREFIX=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install

strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Make backwards-compatibility symlink to ssleay
ln -s %{_bindir}/openssl ${RPM_BUILD_ROOT}%{_bindir}/ssleay

# add 32-bit run-time-linker libraries
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -X32 -x libcrypto.a
/usr/bin/ar -X32 -x libssl.a
ln -s libcrypto.so.%{opensslversion} libcrypto.so
ln -s libssl.so.%{opensslversion} libssl.so

# add 64-bit run-time-linker libraries
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 -x ../lib/libcrypto.a
/usr/bin/ar -X64 -x ../lib/libssl.a
ln -s libcrypto.so.%{opensslversion} libcrypto.so
ln -s libssl.so.%{opensslversion} libssl.so

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib lib64 include
  do
    mkdir -p usr/linux/${dir}
    cd usr/linux/${dir}
    ln -sf ../../..%{_prefix}/${dir}/* .
    cd -
  done

# change these to be full-path links
  cd usr/linux/lib
  rm ./libcrypto.* ./libssl.*
  ln -sf %{_libdir}/libcrypto.a .
  ln -sf %{_libdir}/libcrypto.so .
  ln -sf %{_libdir}/libcrypto.so.%{opensslversion} .
  ln -sf %{_libdir}/libssl.a .
  ln -sf %{_libdir}/libssl.so .
  ln -sf %{_libdir}/libssl.so.%{opensslversion} .

  cd ../lib64
  rm ./libcrypto.* ./libssl.*
  ln -sf %{_libdir64}/libcrypto.so .
  ln -sf %{_libdir64}/libcrypto.so.%{opensslversion} .
  ln -sf %{_libdir64}/libssl.so .
  ln -sf %{_libdir64}/libssl.so.%{opensslversion} .

  cd -
)

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


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README FAQ
%config %attr(0644,root,system) %{openssldir}/openssl.cnf 
%dir %attr(0755,root,system) %{openssldir}/certs
%dir %attr(0755,root,system) %{openssldir}/misc
%dir %attr(0750,root,system) %{openssldir}/private
%{openssldir}/misc/*
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%dir %attr(755,bin,bin) %{_prefix64}
%dir %attr(755,bin,bin) %{_prefix64}/lib
%{_prefix64}/lib/*.a
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
/usr/linux/bin/*
/usr/linux/lib/*.a
/usr/linux/lib/*.so*
/usr/linux/lib64/*.so*


%files devel
%defattr(-,root,system)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%{_includedir}/*
%{_libdir}/pkgconfig/*
/usr/linux/include/*


%files doc
%defattr(-,root,system)
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
%doc doc
%{_mandir}/man3/*


%changelog
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
