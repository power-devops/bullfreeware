%define libgcrypt_version 20
%define libgcrypt_fullversion 20.2.3

Name: libgcrypt
Version: 1.8.3
Release: 1
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
Source4: libgcrypt-1.8.1-ecc-curves.c
Source5: libgcrypt-1.8.1-curves.c
Source6: libgcrypt-1.8.3-t-mpi-point.c

# Source4: ecc-curves.c
# Source5: curves.c
# Source6: t-mpi-point.c

Source7: random.conf

Source10: %{name}-%{version}-%{release}.build.log

Source11:       libgcrypt.so.11-1.5.4-aix32
Source12:       libgcrypt.so.11-1.5.4-aix64

%define _libdir64 %{_prefix}/lib64
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}


# make FIPS hmac compatible with fipscheck - non upstreamable
# update on soname bump
Patch2: libgcrypt-1.8.1-use-fipscheck.patch
# fix tests in the FIPS mode, allow CAVS testing of DSA keygen
Patch5: libgcrypt-1.8.0-tests.patch
# update the CAVS tests
Patch7: libgcrypt-1.7.3-fips-cavs.patch
# use poll instead of select when gathering randomness
Patch11: libgcrypt-1.8.0-use-poll.patch
# slight optimalization of mpicoder.c to silence Valgrind (#968288)
Patch13: libgcrypt-1.6.1-mpicoder-gccopt.patch
# fix tests to work with approved ECC
Patch14: libgcrypt-1.7.3-ecc-test-fix.patch
# Run the FIPS mode initialization in the shared library constructor
Patch18: libgcrypt-1.8.3-fips-ctor.patch
# Block some operations if in FIPS non-operational state
Patch22: libgcrypt-1.7.3-fips-reqs.patch
# Do not try to open /dev/urandom if getrandom() works
Patch24: libgcrypt-1.8.3-getrandom.patch

%define gcrylibdir %{_libdir}
%define gcrylibdir64 %{_libdir64}

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gcc
BuildRequires: gawk, libgpg-error-devel >= 1.11, pkgconfig

# RPM fipscheck not yet ported
# BuildRequires: fipscheck
# This is needed only when patching the .texi doc.
BuildRequires: texinfo
Group: System Environment/Libraries

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Group: Development/Libraries
# Requires(pre): /sbin/install-info
# Requires(post): /sbin/install-info
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}

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
%setup -q
%{SOURCE3}
%patch2 -p1 -b .use-fipscheck
%patch5 -p1 -b .tests
%patch7 -p1 -b .cavs
%patch11 -p1 -b .use-poll
%patch13 -p1 -b .gccopt
%patch14 -p1 -b .eccfix
%patch18 -p1 -b .fips-ctor
%patch22 -p1 -b .fips-reqs
%patch24 -p1 -b .getrandom

cp %{SOURCE4} cipher/ecc-curves.c
cp %{SOURCE5} tests/curves.c
cp %{SOURCE6} tests/t-mpi-point.c


%build

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
# pb compiling .S code (32 bit ?)
export CC="gcc -maix64"
# export CC="gcc "

# Pbs compiling src/fips.c due to Dl_info and dladdr() not in AIX dlfcn.h
#     --enable-hmac-binary-check

%configure --disable-static \
     --enable-noexecstack \
     --enable-pubkey-ciphers='dsa elgamal rsa ecc' \
     --disable-O-flag-munging \
     --disable-asm

sed -i -e '/^sys_lib_dlsearch_path_spec/s,/lib /usr/lib,/usr/lib /lib64 /usr/lib64 /lib,g' libtool

gmake %{?_smp_mflags}

# %check is not recogized by RPM 3.0.5
# %check

# RPM fipscheck not yet ported
# fipshmac src/.libs/libgcrypt.so.??

(gmake check || true)

# Add generation of HMAC checksums of the final stripped binaries 
# (%)define __spec_install_post \
#     %{?__debug_package:%{__debug_install_post}} \
#     %{__arch_install_post} \
#     %{__os_install_post} \
#     fipshmac $RPM_BUILD_ROOT%{gcrylibdir}/*.so.?? \
# %{nil}


# Previous version was libgcrypt.so.11, may have to archive in libgcrypt.a
cp src/.libs/%{name}.so.%{libgcrypt_version} .
gmake distclean
slibclean

# now build the 32-bit version
export CC="gcc -maix32"

%configure --disable-static \
     --enable-noexecstack \
     --enable-pubkey-ciphers='dsa elgamal rsa ecc' \
     --disable-O-flag-munging

sed -i -e '/^sys_lib_dlsearch_path_spec/s,/lib /usr/lib,/usr/lib /lib64 /usr/lib64 /lib,g' libtool

gmake %{?_smp_mflags}

(gmake check || true)

slibclean

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.%{libgcrypt_version}


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

gmake install DESTDIR=$RPM_BUILD_ROOT

# Add libgcrypt.so.20 and libgcrypt.so & .so.20.2.3 - they may be required
install -p src/.libs/libgcrypt.so.%{libgcrypt_version} ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so.%{libgcrypt_version}
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgcrypt.so.%{libgcrypt_fullversion}

mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}

# Add 64 bit version of libgcrypt.so.20 and libgcrypt.so & .so.20.2.3
install -p ./%{name}.so.%{libgcrypt_version} ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so.%{libgcrypt_version}
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so
ln -sf  libgcrypt.so.%{libgcrypt_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgcrypt.so.%{libgcrypt_fullversion}



# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
# Also replace my_host with none.
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config
sed -i -e 's,^my_host=".*"$,my_host="none",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
# /sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

%if "%{gcrylibdir}" != "%{_libdir}"
# Relocate the shared libraries to %{gcrylibdir}.
mkdir -p $RPM_BUILD_ROOT%{gcrylibdir}
for shlib in $RPM_BUILD_ROOT%{_libdir}/*.so* ; do
	if test -L "$shlib" ; then
		rm "$shlib"
	else
		mv "$shlib" $RPM_BUILD_ROOT%{gcrylibdir}/
	fi
done

# Add soname symlink.
# /sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/

%endif

# Overwrite development symlinks.
# pushd $RPM_BUILD_ROOT/%{gcrylibdir}
pwd
cd $RPM_BUILD_ROOT/%{gcrylibdir}
for shlib in lib*.so.?? ; do
	target=$RPM_BUILD_ROOT/%{_libdir}/`echo "$shlib" | sed -e 's,\.so.*,,g'`.so
%if "%{gcrylibdir}" != "%{_libdir}"
	shlib=%{gcrylibdir}/$shlib
%endif
	ln -sf $shlib $target
done
# popd
pwd
cd $OLDPWD

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/gcrypt
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/gcrypt/random.conf


/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

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


# %post -p /sbin/ldconfig

# %postun -p /sbin/ldconfig

%post devel
[ -f %{_infodir}/gcrypt.info.gz ] && \
    /sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir
exit 0

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gcrypt.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi
exit 0



%files
%dir /etc/gcrypt
%config(noreplace) /etc/gcrypt/random.conf
%{_libdir}/*.a
/usr/lib/*.a
%{gcrylibdir}/libgcrypt.so.*
%{gcrylibdir64}/libgcrypt.so.*
# The fips check sums files are not produced
# %{gcrylibdir}/.libgcrypt.so.*.hmac
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%doc AUTHORS NEWS THANKS

%files devel
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
/usr/bin/%{name}-config
/usr/bin/dumpsexp
/usr/bin/hmac256
/usr/bin/mpicalc
%{_includedir}/*
/usr/include/*
%{_libdir}/*.so
%{_libdir64}/*.so
/usr/lib/*.so
/usr/lib64/*.so
%{_datadir}/aclocal/*
%{_mandir}/man1/*

%{_infodir}/gcrypt.info*
%{!?_licensedir:%global license %%doc}
%license COPYING

%changelog
* Tue Oct 16 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.8.3-1
- Updated to version 1.8.3
- Based on Fedora 29
- Include 32/64 bit members of libgcrypt.so.11 in libgcrypt.a for compatibility

* Thu Jul 12 2018 Tomáš Mráz <tmraz@redhat.com> 1.8.3-2
- make only_urandom a default in non-presence of configuration file
- run the full FIPS selftests only when the library is called from
  application

* Wed Nov 09 2017 Tony Reix <tony.reix@atos.net> - 1.8.1-1
- port on AIX

* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 1.5.4-1
- port on AIX 6.1
- Based on Perzl 1.5.4-1


