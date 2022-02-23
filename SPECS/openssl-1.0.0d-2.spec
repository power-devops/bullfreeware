
%define openssldir /var/ssl
%define openssldir64 /var/ssl/64

Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl
Version: 1.0.0d
Release: 2
Source0: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Source1: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz.asc
Source2: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz.md5
Source3: ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz.sha1
Source4: libcrypto.so.0.9.7-aix32
Source5: libcrypto.so.0.9.7-aix64
Source6: libssl.so.0.9.7-aix32
Source7: libssl.so.0.9.7-aix64
Source8: libcrypto.so.0.9.8-aix32
Source9: libcrypto.so.0.9.8-aix64
Source10: libssl.so.0.9.8-aix32
Source11: libssl.so.0.9.8-aix64
Patch0: %{name}-%{version}-Configure.patch
License: OpenSSL License
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
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


%build 
perl util/perlpath.pl /usr/bin/perl

export CC="/usr/vac/bin/xlc_r"

# first build the 64-bit version
export OBJECT_MODE=64
./Configure \
    no-idea no-mdc2 no-rc5 \
    no-symlinks -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir64} \
    aix64-xlc_r
gmake depend
gmake build_libs

/usr/vac/bin/CreateExportList libcrypto.exp libcrypto.a
echo "OPENSSL_cleanse" >> libcrypto.exp
${CC} -qmkshrobj libcrypto.a -o libcrypto.so.1.0.0 -bE:libcrypto.exp
rm -f libcrypto.exp libcrypto.a
/usr/bin/ar -rv libcrypto.a libcrypto.so.1.0.0

/usr/vac/bin/CreateExportList libssl.exp libssl.a
${CC} -qmkshrobj libssl.a -o libssl.so.1.0.0 -bE:libssl.exp -L. -lcrypto
rm -f libssl.exp libssl.a
/usr/bin/ar -rv libssl.a libssl.so.1.0.0

gmake

mkdir -p 64
mv libcrypto.so.1.0.0 libssl.so.1.0.0 64/
gmake clean

# now build the 32-bit version
export OBJECT_MODE=32
./Configure \
    no-idea no-mdc2 no-rc5 \
    no-symlinks -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=%{openssldir} \
    aix-xlc_r
gmake depend
gmake build_libs

/usr/vac/bin/CreateExportList libcrypto.exp libcrypto.a
echo "OPENSSL_cleanse" >> libcrypto.exp
${CC} -qmkshrobj libcrypto.a -o libcrypto.so.1.0.0 -bE:libcrypto.exp
rm -f libcrypto.exp libcrypto.a
/usr/bin/ar -rv libcrypto.a libcrypto.so.1.0.0

/usr/vac/bin/CreateExportList libssl.exp libssl.a
${CC} -qmkshrobj libssl.a -o libssl.so.1.0.0 -bE:libssl.exp -L. -lcrypto
rm -f libssl.exp libssl.a
/usr/bin/ar -rv libssl.a libssl.so.1.0.0

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q libcrypto.a 64/libcrypto.so.1.0.0
/usr/bin/ar -X64 -q libssl.a 64/libssl.so.1.0.0

# Add the older 0.9.7l and 0.9.8n shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE4} libcrypto.so.0.9.7
/usr/bin/strip -X32 -e libcrypto.so.0.9.7
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE8} libcrypto.so.0.9.8
/usr/bin/strip -X32 -e libcrypto.so.0.9.8
/usr/bin/ar -X32 -q libcrypto.a libcrypto.so.0.9.8

cp %{SOURCE5} libcrypto.so.0.9.7
/usr/bin/strip -X64 -e libcrypto.so.0.9.7
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE9} libcrypto.so.0.9.8
/usr/bin/strip -X64 -e libcrypto.so.0.9.8
/usr/bin/ar -X64 -q libcrypto.a libcrypto.so.0.9.8

cp %{SOURCE6} libssl.so.0.9.7
/usr/bin/strip -X32 -e libssl.so.0.9.7
/usr/bin/ar -X32 -q libssl.a libssl.so.0.9.7
cp %{SOURCE10} libssl.so.0.9.8
/usr/bin/strip -X32 -e libssl.so.0.9.8
/usr/bin/ar -X32 -q libssl.a libssl.so.0.9.8

cp %{SOURCE7} libssl.so.0.9.7
/usr/bin/strip -X64 -e libssl.so.0.9.7
/usr/bin/ar -X64 -q libssl.a libssl.so.0.9.7
cp %{SOURCE11} libssl.so.0.9.8
/usr/bin/strip -X64 -e libssl.so.0.9.8
/usr/bin/ar -X64 -q libssl.a libssl.so.0.9.8

# apps/openssl still has the wrong shared library paths, we have to relink it
rm -f apps/openssl
gmake LIBSSL="-L/opt/freeware/lib -lssl" LIBCRYPTO="-L/opt/freeware/lib -L/${RPM_BUILD_DIR}/%{name}-%{version} -lcrypto"


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
ln -s libcrypto.so.0.9.8 libcrypto.so
ln -s libssl.so.0.9.8 libssl.so

# add 64-bit run-time-linker libraries
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 -x ../lib/libcrypto.a
/usr/bin/ar -X64 -x ../lib/libssl.a
ln -s libcrypto.so.0.9.8 libcrypto.so
ln -s libssl.so.0.9.8 libssl.so

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
  ln -sf %{_libdir}/libcrypto.so.0.9.8 .
  ln -sf %{_libdir}/libssl.a .
  ln -sf %{_libdir}/libssl.so .
  ln -sf %{_libdir}/libssl.so.0.9.8 .

  cd ../lib64
  rm ./libcrypto.* ./libssl.*
  ln -sf %{_libdir64}/libcrypto.so .
  ln -sf %{_libdir64}/libcrypto.so.0.9.8 .
  ln -sf %{_libdir64}/libssl.so .
  ln -sf %{_libdir64}/libssl.so.0.9.8 .

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
%doc CHANGES CHANGES.SSLeay LICENSE NEWS README
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
* Wed Oct 05 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.0d-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Jun 10 2011 Gerard Visiedo <gerard.visiedo@bull.net>  1.0.0d-1
- Initial port on Aix5.3
