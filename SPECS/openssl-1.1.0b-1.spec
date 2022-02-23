# Tests are done by default
# SSLv2 is  done by default

# 0: GCC - 1: XLC
%define gcc_compiler 0
%define gcc_compiler 1

%if %{gcc_compiler} == 0
%define sub_release xlc
%endif


# rpm -ba --define 'dotests 0' openssl...spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

# Version with/without SSLv2
# rpm -ba --define 'nosslv2 0' openssl...spec
%{!?nosslv2:%define SSLV2 1}
%{?nosslv2:%define SSLV2 0}


%define opensslversion 1.1.0

%define openssldir   /var/ssl
%define openssldir64 /var/ssl/64

Summary: Secure Sockets Layer and cryptography libraries and tools
Name: openssl
Version: %{opensslversion}b
Release: 1%{!?nosslv2:withsslv2}%{?sub_release}

Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}.tar.gz.asc
#  File:	%{name}-%{version}.tar.gz.md5  is no more provided by OpenSSL project
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

# Taken from 1.0.1u :
Source17:	libcrypto.so.1.0.1-aix32
Source18:	libcrypto.so.1.0.1-aix64
Source19:	libssl.so.1.0.1-aix32
Source20:	libssl.so.1.0.1-aix64

# Taken from 1.0.2j-1withsslv2 :
Source21:	libcrypto.so.1.0.2-aix32
Source22:	libcrypto.so.1.0.2-aix64
Source23:	libssl.so.1.0.2-aix32
Source24:	libssl.so.1.0.2-aix64

Source100:	%{name}-%{version}-%{release}.build.log

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


# No more useful
#Patch0: %{name}-%{version}-Configure.patch
#Patch1: %{name}-%{version}-aix.patch

# No more useful. Integrated into OpenSSL sources.
#Patch2: %{name}-%{version}-chacha-ppc.patch


License: OpenSSL License
Group: System Environment/Libraries
Provides: SSL
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
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

# Fixed now by means of openssl-1.1.0-chacha-ppc.patch patch
# GCC versions 6.1.0 and 6.2.0 behaves badly for ppccap.c and -O
#BuildRequires: gcc < 6

Requires: perl >= 5.10.0


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

EGD is built by default.

The library is available as 32-bit and 64-bit.

%if %{SSLV2} == 1
Note: this version is compiled with SSLv2 support.
However, it is only aimed to help when linking with tools that need SSLv2 at build time.
Do not use it !
%else
Note: this version is compiled without SSLv2 support.
%endif

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
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

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif
If you are compiling a 64-bit program, you have to compile and link your
application with "gcc -maix64" or "xlc -q64".

%if %{SSLV2} == 1
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


%prep
%setup -q
#%patch0
#%patch1
# No more useful. Integrated into OpenSSL sources.
#%patch2

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

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

echo "C/C++ compiler: "
%if %{gcc_compiler} == 1
export CC__="gcc"
$CC__ --version
%else
export CC__="xlc_r"
$CC__ -qversion
%endif

# -lpthread required for: GCC/32bit & test/threadstest.o
LDFLAGS="-L. -lpthread"

# Does nothing. Change CFLAG in Makefile
CFLAGS="-O2"

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

%if %{SSLV2} == 1
        SSLV2_=enable-ssl2
%endif


# Issue with 1.0.2f:    no-symlinks  !
# first build the 64-bit version
# 1.0.2g : config says:     no-ssl2         [default]  OPENSSL_NO_SSL2 (skip dir)



build_openssl()
{
echo "--prefix     = %{_prefix}"
echo "--openssldir =$1"

# EGD is no more required by Python team

./Configure \
    no-egd \
    no-idea no-mdc2 no-rc5 \
    -DSSL_ALLOW_ADH \
    threads \
    no-shared \
    zlib-dynamic \
    --prefix=%{_prefix} \
    --openssldir=$1 \
    $SSLV2_ \
    $CONFIGURE_TARGET

echo "# gmake depend"
gmake depend

echo "# gmake build_libs"
gmake build_libs


# Fixed now with openssl-1.1.0-chacha-ppc.patch patch
# test_evp issue with -O
# Appears with XLC v12 & v13 only for 64bits
# Appears with GCC 6.1.0 & 6.2.0, not for GCC 4.8.4, 4.8.5, 5.4.0
# No more useful when using GCC < 6.*
#	See: BuildRequires: gcc < 6
#	%if %{gcc_compiler} == 0
#	if [ "$OBJECT_MODE" == "64" ]
#	then
#	# Work-around about the -O issue with ppccap.o and test_evp .
#	echo "-O issue with crypto/ppccap.o"
#	ls -l crypto/ppccap.o
#	rm  crypto/ppccap.o
#	rm -rf libcrypto.a
#	cp  Makefile                         Makefile.O
#	cat Makefile | sed "s/ -O / -O0 /" > Makefile.O0
#	cp  Makefile.O0                      Makefile
#	gmake crypto/ppccap.o
#	cp  Makefile.O                       Makefile
#	gmake build_libs
#	ls -l crypto/ppccap.o
#	fi
#	%endif

# Test 40-test_rehash.t fails due to being root
# Run it as non-root and it all runs fine


mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libcrypto.a
%if %{gcc_compiler} == 1
    # GCC
    ${CC} -shared    *.o -o ../libcrypto.so.%{opensslversion}                    -lpthread
%else
    # xlc
    ${CC} -qmkshrobj *.o -o ../libcrypto.so.%{opensslversion} -bexpall -bernotok
%endif
cd ..
rm -rf libcrypto.a .tmplibdir
/usr/bin/ar -rv libcrypto.a libcrypto.so.%{opensslversion}


mkdir .tmplibdir
cd .tmplibdir
/usr/bin/ar -x ../libssl.a
%if %{gcc_compiler} == 1
    # GCC
    ${CC} -shared    *.o -o ../libssl.so.%{opensslversion}                       -L.. -lcrypto                                           -lpthread
%else
    # xlc
    ${CC} -qmkshrobj *.o -o ../libssl.so.%{opensslversion}    -bexpall -bernotok -L.. -lcrypto -blibpath:/opt/freeware/lib:/usr/lib:/lib 
%endif
cd ..
rm -rf libssl.a .tmplibdir
/usr/bin/ar -rv libssl.a libssl.so.%{opensslversion}


echo "# gmake all"
# WHY different in 32 compared to 64 ???????????????????
if [ "$OBJECT_MODE" == "64" ]
then
	gmake
else
	# apps/openssl still has the wrong shared library paths, we have to relink it
	rm -f apps/openssl
	gmake LDFLAGS="-L. -L.. $LDFLAGS" LIBSSL=" -L/opt/freeware/lib -lssl" LIBCRYPTO="-L/opt/freeware/lib -lcrypto -lpthread"
fi


if [ "%{DO_TESTS}" == 1 ]
then

echo "# gmake -k test"
echo "LIBPATH: $LIBPATH"

if [ "$OBJECT_MODE" == "64" ]
then
# -Versions 1.0.1* and 1.0.2Ã* :
#   Without the "export LIBPATH=...", "gmake test" makes the zlib test to fail with:
#   1152921504606846944:error:25066067:DSO support routines:DLFCN_LOAD:could not load the shared library:dso_dlfcn.c:187:filename(libz.so): Could not load module /usr/lib/libz.so.
#        System error: Exec format error
#   in 64bits ONLY !!
#   Replacing /opt/freeware/lib/libz.so.1 by /opt/freeware/lib64/libz.so.1 shows that the test loads the 32bit libz.so.1 instead of the 64bits.

# -Version 1.1.0 :
#   The tests:
#       20-test_enc.t (Failed test 'zlib base64')
#       80-test_cms.t (Failed test 'compressed content test streaming PEM format')
#   also fail due to some LIBPATH issue.
#   Below LIBPATH does fix the issue.
#   Use:
#      export LIBPATH=/opt/freeware/src/packages/BUILD/openssl-1.1.0/64bit:/opt/freeware/lib64/
#   when testing by hand.

OLDLIBPATH=$LIBPATH
export LIBPATH="`pwd`:/opt/freeware/lib64/"
echo "LIBPATH: $LIBPATH"
	(gmake -k test || true)
export LIBPATH=$OLDLIBPATH
else
	(gmake -k test || true)
fi

for t in test_evp
do
    echo
    echo "#---- test of: $t"
    for n in 1 2 3 4 5
    do
       	( cd test; SRCTOP=../. BLDTOP=../. PERL="perl" EXE_EXT= OPENSSL_ENGINES=.././engines perl .././test/run_tests.pl $t || true )
    done
done

/usr/sbin/slibclean
fi

}


# first build the 64-bit version
cd 64bit
#/usr/bin/perl util/perlpath.pl /usr/bin/perl

export OBJECT_MODE=64

%if %{gcc_compiler} == 1
export CC="$CC__ -maix64"
export CONFIGURE_TARGET="aix64-gcc"
%else
export CC="$CC__ -q64"
export CONFIGURE_TARGET="aix64-cc"
%endif

build_openssl %{openssldir64}


# now build the 32-bit version
cd ../32bit
#/usr/bin/perl util/perlpath.pl /usr/bin/perl

export OBJECT_MODE=32

%if %{gcc_compiler} == 1
export CC="$CC__ -maix32"
export CONFIGURE_TARGET="aix-gcc"
%else
export CC="$CC__ -q32"
export CONFIGURE_TARGET="aix-cc"
%endif

build_openssl %{openssldir}


# Required here even if no tests were done previously
/usr/sbin/slibclean


# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
/usr/bin/ar -X64 -q libcrypto.a ../64bit/libcrypto.so.%{opensslversion}
/usr/bin/ar -X64 -q libssl.a    ../64bit/libssl.so.%{opensslversion}


# Add the older 0.9.7l, 0.9.8x, 1.0.0j, and 1.0.1r shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')

# crypto 32bits
cp %{SOURCE5}                      libcrypto.so.0.9.7
/usr/bin/strip -X32 -e             libcrypto.so.0.9.7
/usr/bin/ar    -X32 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE9}                      libcrypto.so.0.9.8
/usr/bin/strip -X32 -e             libcrypto.so.0.9.8
/usr/bin/ar    -X32 -q libcrypto.a libcrypto.so.0.9.8
cp %{SOURCE13}                     libcrypto.so.1.0.0
/usr/bin/strip -X32 -e             libcrypto.so.1.0.0
/usr/bin/ar    -X32 -q libcrypto.a libcrypto.so.1.0.0
cp %{SOURCE17}                     libcrypto.so.1.0.1
/usr/bin/strip -X32 -e             libcrypto.so.1.0.1
/usr/bin/ar    -X32 -q libcrypto.a libcrypto.so.1.0.1
cp %{SOURCE21}                     libcrypto.so.1.0.2
/usr/bin/strip -X32 -e             libcrypto.so.1.0.2
/usr/bin/ar    -X32 -q libcrypto.a libcrypto.so.1.0.2

# crypto 64bits
cp %{SOURCE6}                      libcrypto.so.0.9.7
/usr/bin/strip -X64 -e             libcrypto.so.0.9.7
/usr/bin/ar    -X64 -q libcrypto.a libcrypto.so.0.9.7
cp %{SOURCE10}                     libcrypto.so.0.9.8
/usr/bin/strip -X64 -e             libcrypto.so.0.9.8
/usr/bin/ar    -X64 -q libcrypto.a libcrypto.so.0.9.8
cp %{SOURCE14}                     libcrypto.so.1.0.0
/usr/bin/strip -X64 -e             libcrypto.so.1.0.0
/usr/bin/ar    -X64 -q libcrypto.a libcrypto.so.1.0.0
cp %{SOURCE18}                     libcrypto.so.1.0.1
/usr/bin/strip -X64 -e             libcrypto.so.1.0.1
/usr/bin/ar    -X64 -q libcrypto.a libcrypto.so.1.0.1
cp %{SOURCE22}                     libcrypto.so.1.0.2
/usr/bin/strip -X64 -e             libcrypto.so.1.0.2
/usr/bin/ar    -X64 -q libcrypto.a libcrypto.so.1.0.2

# ssl 32bits
cp %{SOURCE7}                      libssl.so.0.9.7
/usr/bin/strip -X32 -e             libssl.so.0.9.7
/usr/bin/ar    -X32 -q libssl.a    libssl.so.0.9.7
cp %{SOURCE11}                     libssl.so.0.9.8
/usr/bin/strip -X32 -e             libssl.so.0.9.8
/usr/bin/ar    -X32 -q libssl.a    libssl.so.0.9.8
cp %{SOURCE15}                     libssl.so.1.0.0
/usr/bin/strip -X32 -e             libssl.so.1.0.0
/usr/bin/ar    -X32 -q libssl.a    libssl.so.1.0.0
cp %{SOURCE19}                     libssl.so.1.0.1
/usr/bin/strip -X32 -e             libssl.so.1.0.1
/usr/bin/ar    -X32 -q libssl.a    libssl.so.1.0.1
cp %{SOURCE23}                     libssl.so.1.0.2
/usr/bin/strip -X32 -e             libssl.so.1.0.2
/usr/bin/ar    -X32 -q libssl.a    libssl.so.1.0.2

# ssl 64bits
cp %{SOURCE8}                      libssl.so.0.9.7
/usr/bin/strip -X64 -e             libssl.so.0.9.7
/usr/bin/ar    -X64 -q libssl.a    libssl.so.0.9.7
cp %{SOURCE12}                     libssl.so.0.9.8
/usr/bin/strip -X64 -e             libssl.so.0.9.8
/usr/bin/ar    -X64 -q libssl.a    libssl.so.0.9.8
cp %{SOURCE16}                     libssl.so.1.0.0
/usr/bin/strip -X64 -e             libssl.so.1.0.0
/usr/bin/ar    -X64 -q libssl.a    libssl.so.1.0.0
cp %{SOURCE20}                     libssl.so.1.0.1
/usr/bin/strip -X64 -e             libssl.so.1.0.1
/usr/bin/ar    -X64 -q libssl.a    libssl.so.1.0.1
cp %{SOURCE24}                     libssl.so.1.0.2
/usr/bin/strip -X64 -e             libssl.so.1.0.2
/usr/bin/ar    -X64 -q libssl.a    libssl.so.1.0.2


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install

export OBJECT_MODE=32
cd ../32bit
gmake DESTDIR=${RPM_BUILD_ROOT} MANDIR=%{_mandir} install


echo "RPM_BUILD_ROOT: ${RPM_BUILD_ROOT}"
ls -l ${RPM_BUILD_ROOT}


strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
# Warning about c_rehash, which is a shell script. Not an issue.


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


# Compatibility with libssl.so.0.9.7
# add links for 64-bit library members
(
  mkdir -p ${RPM_BUILD_ROOT}%{_prefix64}/lib
  cd ${RPM_BUILD_ROOT}%{_prefix64}/lib
  ln -s ../../lib/*.a .
)


# rename ${RPM_BUILD_ROOT}%{_mandir}/man3/threads.3 as it might conflict with
# man3/threads.3 from perl
#cd ${RPM_BUILD_ROOT}%{_mandir}/man3
#mv -f threads.3 threads.3ssl


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NEWS 32bit/README 32bit/FAQ
%config %attr(0644,root,system) %{openssldir}/openssl.cnf 
%dir %attr(0755,root,system) %{openssldir}/certs
%dir %attr(0755,root,system) %{openssldir}/misc
%dir %attr(0750,root,system) %{openssldir}/private
%{openssldir}/misc/*
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
# Compatibility with libssl.so.0.9.7 with %{_prefix64}/lib
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
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NEWS 32bit/README
%{_includedir}/*
%{_libdir}/pkgconfig/*
/usr/linux/include/*


%files doc
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NEWS 32bit/README
%doc 32bit/doc
%{_mandir}/man3/*


%changelog
* Thu Sep 26 2016 Tony Reix <tony.reix@atos.net> - 1.1.0b-1
- Version 1.1.0a MUST be replaced by 1.1.0b !

* Thu Sep 22 2016 Tony Reix <tony.reix@atos.net> - 1.1.0a-1
- Update to version 1.1.0a on AIX 6.1

* Tue Sep 06 2016 Tony Reix <tony.reix@atos.net> - 1.1.0-4
- Add openssl-1.1.0-chacha-ppc.patch which fixed issue with -02 .
- Suppress suport of EGD since Python people will manage without it.

* Thu Sep 01 2016 Tony Reix <tony.reix@atos.net> - 1.1.0-3
- Add EGD for python
- Add BuildRequires for GCC version < 6.* for ppccap.c & -O

* Tue Aug 30 2016 Tony Reix <tony.reix@atos.net> - 1.1.0-2
- Manage both xlc & gcc.
- Fix changes (patches, DESTDIR, ...)
- Add compatibility with 1.0.2
- Handle -O issue with ppccap.o and test_evp.

* Mon Aug 29 2016 Tony Reix <tony.reix@atos.net> - 1.1.0-1
- Update to version 1.1.0 on AIX 6.1

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
