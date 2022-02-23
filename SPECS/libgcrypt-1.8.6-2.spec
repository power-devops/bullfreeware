# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define libgcrypt_version 20
%define libgcrypt_fullversion 20.2.6

Name: libgcrypt
Version: 1.8.6
Release: 2
URL: http://www.gnupg.org/

Source0: libgcrypt-%{version}-hobbled.tar.xz

# The original libgcrypt sources now contain potentially patented ECC
# cipher support (in ecc-curves.c, curves.c, t-mpi-point.c).
# Fedora removes it from the tarball shipped with the hobble-libgcrypt
# script.
# The replacement is an RH approved ECC in Source4-5
#
# See  https://en.wikipedia.org/wiki/ECC_patents
#
#Source0: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{version}.tar.bz2
#Source1: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-{version}.tar.bz2.sig

Source2: wk@g10code.com
Source3: hobble-libgcrypt

# Approved ECC support
Source4: libgcrypt-1.8.6-ecc-curves.c
Source5: libgcrypt-1.8.1-curves.c
Source6: libgcrypt-1.8.6-t-mpi-point.c

# Source4: ecc-curves.c
# Source5: curves.c
# Source6: t-mpi-point.c

Source7: random.conf

Source10: %{name}-%{version}-%{release}.build.log

Source11:       libgcrypt.so.11-1.5.4-aix32
Source12:       libgcrypt.so.11-1.5.4-aix64

%define _libdir64 %{_prefix}/lib64
# BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}


# make FIPS hmac compatible with fipscheck - non upstreamable
# update on soname bump
Patch2: libgcrypt-1.8.5-use-fipscheck.patch
# modify FIPS RSA and DSA keygen to comply with requirements
Patch5: libgcrypt-1.8.4-fips-keygen.patch
# fix the tests to work correctly in the FIPS mode
Patch6: libgcrypt-1.8.4-tests-fipsmode.patch
# update the CAVS tests
Patch7: libgcrypt-1.7.3-fips-cavs.patch
# use poll instead of select when gathering randomness
Patch11: libgcrypt-1.8.4-use-poll.patch
# slight optimalization of mpicoder.c to silence Valgrind (#968288)
Patch13: libgcrypt-1.6.1-mpicoder-gccopt.patch
# fix tests to work with approved ECC
Patch14: libgcrypt-1.7.3-ecc-test-fix.patch
# Run the FIPS mode initialization in the shared library constructor
Patch18: libgcrypt-1.8.6-fips-ctor.patch
# Block some operations if in FIPS non-operational state
Patch22: libgcrypt-1.7.3-fips-reqs.patch
# Do not try to open /dev/urandom if getrandom() works
Patch24: libgcrypt-1.8.5-getrandom.patch
# CMAC selftest for FIPS POST
Patch25: libgcrypt-1.8.3-cmac-selftest.patch
# Continuous FIPS entropy test
Patch26: libgcrypt-1.8.3-fips-enttest.patch 
# Disable non-approved FIPS hashes in the enforced FIPS mode
Patch27: libgcrypt-1.8.3-md-fips-enforce.patch
# Intel CET support, in upstream master
Patch28: libgcrypt-1.8.5-intel-cet.patch
# FIPS module is redefined a little bit (implicit by kernel FIPS mode)
Patch30: libgcrypt-1.8.5-fips-module.patch
# Backported AES performance improvements
Patch31: libgcrypt-1.8.5-aes-perf.patch


%global gcrysoname libgcrypt.so.20
%global hmackey orboDeJITITejsirpADONivirpUkvarP

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library
Group: System Environment/Libraries

BuildRequires: gcc
BuildRequires: gawk, pkgconfig
BuildRequires: sed
BuildRequires: libgpg-error-devel >= 1.11
BuildRequires: autoconf, automake
# TBC BuildRequires: libtool

# This is needed only when patching the .texi doc.
BuildRequires: texinfo

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Group: Development/Libraries
# Requires(pre): /sbin/install-info
# Requires(post): /sbin/install-info
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}
# TBC Requires: pkgconfig

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

The library is available as 32-bit and 64-bit.

This version has been compiled with GCC.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".




%prep

echo "dotests=%{dotests}"

%setup -q
%{SOURCE3}
%patch2 -p1 -b .use-fipscheck
%patch5 -p1 -b .tests
%patch6 -p1 -b .tests-fipsmode
%patch7 -p1 -b .cavs
%patch11 -p1 -b .use-poll
%patch13 -p1 -b .gccopt
%patch14 -p1 -b .eccfix
%patch18 -p1 -b .fips-ctor
%patch22 -p1 -b .fips-reqs
%patch24 -p1 -b .getrandom
%patch25 -p1 -b .cmac-selftest
%patch26 -p1 -b .fips-enttest
%patch27 -p1 -b .fips-enforce
%patch28 -p1 -b .intel-cet
%patch30 -p1 -b .fips-module
%patch31 -p1 -b .aes-perf

# New files created without read permissions
chmod +r cipher/rijndael-ppc-common.h.aes-perf
chmod +r cipher/rijndael-ppc-functions.h.aes-perf
chmod +r cipher/rijndael-ppc.c.aes-perf
chmod +r cipher/rijndael-ppc9le.c.aes-perf
chmod +r src/hwf-ppc.c.aes-perf

cp %{SOURCE4} cipher/ecc-curves.c
cp %{SOURCE5} tests/curves.c
cp %{SOURCE6} tests/t-mpi-point.c

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

# configure tests try to compile code containing ASMs to a .o file
# In an LTO world, that always works as compilation does not happen until
# link time.  As a result we get the wrong results from configure.
# Disable LTO.
# TBC %%define _lto_cflags %{nil}
# TBC and remove --disable-asm

%define _lto_cflags %{nil}


# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
cd 64bit

# pb compiling .S code (32 bit ?)
export CC="gcc -maix64"
# export CC="gcc "

autoreconf -f

# Pbs compiling src/fips.c due to Dl_info and dladdr() not in AIX dlfcn.h
#     --enable-hmac-binary-check

%configure --disable-static \
     --enable-noexecstack \
     --enable-pubkey-ciphers='dsa elgamal rsa ecc' \
     --disable-O-flag-munging \
     --disable-asm

/opt/freeware/bin/sed -i -e '/^sys_lib_dlsearch_path_spec/s,/lib /usr/lib,/usr/lib /lib64 /usr/lib64 /lib,g' libtool

gmake %{?_smp_mflags}


# Previous version was libgcrypt.so.11, may have to archive in libgcrypt.a
cp src/.libs/%{name}.so.%{libgcrypt_version} .
# gmake distclean
slibclean

# now build the 32-bit version
cd ../32bit

export CC="gcc -maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

autoreconf -f

%configure --disable-static \
     --enable-noexecstack \
     --enable-pubkey-ciphers='dsa elgamal rsa ecc' \
     --disable-O-flag-munging

/opt/freeware/bin/sed -i -e '/^sys_lib_dlsearch_path_spec/s,/lib /usr/lib,/usr/lib /lib64 /usr/lib64 /lib,g' libtool

gmake %{?_smp_mflags}

slibclean

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ../64bit/%{name}.so.%{libgcrypt_version}


# Add the older .so.11 shared members for compatibility with previous
# RPMs and applications
# They are set LOADONLY by running the command 'strip -e'

# libgcrypt 32bits
cp %{SOURCE11} libgcrypt.so.11
/usr/bin/strip -X32 -e libgcrypt.so.11
${AR} -X32 -q src/.libs/%{name}.a libgcrypt.so.11

# libgcrypt 64bits
cp %{SOURCE12} libgcrypt.so.11
/usr/bin/strip -X64 -e libgcrypt.so.11
${AR} -X64 -q src/.libs/%{name}.a libgcrypt.so.11



%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# first the 64 bit install
cd 64bit
export OBJECT_MODE=64

gmake install DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}%{_libdir} ${RPM_BUILD_ROOT}%{_libdir64}

mv ${RPM_BUILD_ROOT}%{_bindir}/dumpsexp ${RPM_BUILD_ROOT}%{_bindir}/dumpsexp_64
mv ${RPM_BUILD_ROOT}%{_bindir}/hmac256 ${RPM_BUILD_ROOT}%{_bindir}/hmac256_64
mv ${RPM_BUILD_ROOT}%{_bindir}/mpicalc ${RPM_BUILD_ROOT}%{_bindir}/mpicalc_64

# Add 64 bit version of libgcrypt.so.20, libgcrypt.so & .so.20.2.3 - if required
install -p ./%{name}.so.%{libgcrypt_version} ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so.%{libgcrypt_version}
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so.%{libgcrypt_fullversion}


# next the 32 bit install
cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR=$RPM_BUILD_ROOT

# Add libgcrypt.so.20 and libgcrypt.so & .so.20.2.3 - they may be required
install -p src/.libs/libgcrypt.so.%{libgcrypt_version} ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so.%{libgcrypt_version}
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so.%{libgcrypt_fullversion}




# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
# Also replace my_host with none.
/opt/freeware/bin/sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config
/opt/freeware/bin/sed -i -e 's,^my_host=".*"$,my_host="none",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
# /sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

# # Overwrite development symlinks.

# (
#     cd $RPM_BUILD_ROOT/%{gcrylibdir}
#     for shlib in lib*.so.?? ; do
# 	target=$RPM_BUILD_ROOT/%{_libdir}/`echo "$shlib" | sed -e 's,\.so.*,,g'`.so
# 	ln -sf $shlib $target
#     done
# )

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/gcrypt
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/gcrypt/random.conf

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

%check

# Running "gmake test" requires an X display
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Test the 64 bit version
cd 64bit
export OBJECT_MODE=64

src/hmac256 %{hmackey} src/.libs/%{gcrysoname} | cut -f1 -d ' ' >src/.libs/.%{gcrysoname}.hmac

(gmake check || true)

slibclean

# Test the 32 bit version
cd ../32bit
export OBJECT_MODE=32

src/hmac256 %{hmackey} src/.libs/%{gcrysoname} | cut -f1 -d ' ' >src/.libs/.%{gcrysoname}.hmac

(gmake check || true)



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,system,-)
%dir /etc/gcrypt
%config(noreplace) /etc/gcrypt/random.conf
%{_libdir}/*.a
# The fips check sums files are not produced due to Dl_info  TBC
# %{_libdir}/.libgcrypt.so.*.hmac          TBC
%{!?_licensedir:%global license %%doc}
%license 32bit/COPYING.LIB
%doc 32bit/AUTHORS 32bit/NEWS 32bit/THANKS

%files devel
%defattr(-,root,system,-)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp*
%{_bindir}/hmac256*
%{_bindir}/mpicalc*
%{_includedir}/*
%{_libdir}/pkgconfig/libgcrypt.pc
%{_libdir64}/pkgconfig/libgcrypt.pc
%{_datadir}/aclocal/*
%{_mandir}/man1/*

%{_infodir}/gcrypt.info*
%{!?_licensedir:%global license %%doc}
%license 32bit/COPYING

%changelog
* Thu Oct 22 2020 Clement Chigot <clement.chigot@atos.net> - 1.8.6-2
- Remove .so files

* Thu Aug 06 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.8.6-1
- Update to version 1.8.6 based on Fedora 33
- Add 64 bit versions of utilities

* Tue Aug 04 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.8.3-2
- Adaptions for rebuild on laurel2 with RPM 4 and to include
-    correction to gpg-error.h / gpgrt.h for 32 & 64 bit initialiser
- Reorganise 32 / 64 bit builds in separate directory trees

* Thu Jul 12 2018 Tomáš Mráz <tmraz@redhat.com> 1.8.3-2
- make only_urandom a default in non-presence of configuration file
- run the full FIPS selftests only when the library is called from
  application

* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 1.8.1-1
- port on AIX

* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 1.5.4-1
- port on AIX 6.1
- Based on Perzl 1.5.4-1


