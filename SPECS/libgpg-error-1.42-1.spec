# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

%define _smp_mflags -j4

# Still version 0 on Fedora
%define libgpg_error_version 0
%define libgpg_error_fullversion 0.28.0
# The full version is significant as each new version may add symbols

%define name libgpg-error
%define version 1.42
%define release 1

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        A library defining common error values used by GnuPG components
Group:          System Environment/Libraries

License:        LGPLv2+
URL:            https://www.gnupg.org/related_software/libgpg-error/
Source0:        https://www.gnupg.org/ftp/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2
Source1:        https://www.gnupg.org/ftp/gcrypt/libgpg-error/%{name}-%{version}.tar.bz2.sig

# RPM 3.0.5 does not recognize or initialise  %{buildroot} without following
# BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

Source10: %{name}-%{version}-%{release}.build.log

Patch1: libgpg-error-1.29-multilib.patch
Patch2: libgpg-error-1.42-coverity.patch
# Manage $HOME = / on AIX
Patch3: libgpg-error-1.42-aix-home.patch

BuildRequires: gcc
BuildRequires: gettext, gettext-devel
BuildRequires: diffutils sed
# BuildRequires: texinfo
# BuildRequires: gettext-autopoint


%description
Libgpg-error is a library that defines common error values for all GnuPG
components. Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
Libksba, DirMngr, Pinentry, SCdaemon (SmartCard Daemon) and possibly more
in the future.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary:  Development files for the %{name} package
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}


%description devel
Libgpg-error is a library that defines common error values for all GnuPG
components. Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
Libksba, DirMngr, Pinentry, SCdaemon (SmartCard Daemon) and possibly more
in the future.
This package contains files for application development using libgpg-error.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep

%setup -q
%patch1 -p1 -b .multilib
%patch2 -p1 -b .coverity
%patch3 -p1 -b .aix-home

# Fedora .spec file does strange things about config:
#	gpg-error-config.in
#	gpg-error-config-test.sh.in
#	configure

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

/usr/bin/env | /usr/bin/sort

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"
export AWK="/usr/bin/awk"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/usr/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CFLAGS="-D_LARGE_FILES"

export CC32=" ${CC__}  ${FLAG32} $CFLAGS"
export CC64=" ${CC__}  ${FLAG64} $CFLAGS"

# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

./configure -v --prefix=%{_prefix} \
               --infodir=%{_infodir} \
               --localedir=%{_datadir}/locale \
               --mandir=%{_mandir} \
               --disable-static \
               --disable-rpath \
               --disable-languages

gmake %{?_smp_mflags}

# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure -v --prefix=%{_prefix} \
               --infodir=%{_infodir} \
               --localedir=%{_datadir}/locale \
               --mandir=%{_mandir} \
               --disable-static \
               --disable-rpath \
               --disable-languages

gmake %{?_smp_mflags}

# Archive 64 bit shared object in 32 bit shared library

slibclean
${AR} -q src/.libs/libgpg-error.a ../64bit/src/.libs/libgpg-error.so.%{libgpg_error_version}

slibclean

strip -e -X32_64 src/.libs/libgpg-error.so.%{libgpg_error_version} ../64bit/src/.libs/libgpg-error.so.%{libgpg_error_version}


%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"
# export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64

gmake install DESTDIR="$RPM_BUILD_ROOT"

# Add libgpg-error.so.0 and libgpg-error.so & .so.0.28.0 - they may be required
mkdir    ${RPM_BUILD_ROOT}%{_libdir64}
install -p src/.libs/libgpg-error.so.%{libgpg_error_version} ${RPM_BUILD_ROOT}%{_libdir64}/libgpg-error.so.%{libgpg_error_version}
ln -sf  libgpg-error.so.%{libgpg_error_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpg-error.so
ln -sf  libgpg-error.so.%{libgpg_error_version}     ${RPM_BUILD_ROOT}%{_libdir64}/libgpg-error.so.%{libgpg_error_fullversion}

# Following not required, as lib64/libgpg-error.a is symlink to lib/libgpg-error.a
# mv ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpg-error.a

rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

# Move lib to lib64
mv  ${RPM_BUILD_ROOT}/%{_libdir}  ${RPM_BUILD_ROOT}/%{_libdir64}
# Move 64 bit yat2m
mv  ${RPM_BUILD_ROOT}/%{_bindir}/yat2m  ${RPM_BUILD_ROOT}/%{_bindir}/yat2m_64

cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR="$RPM_BUILD_ROOT"

# Header file is 32 / 64 bit dependent - need to inject following in
# gpg-error.h / gpgrt.h (header file copied during build)
#
# The build does  ./gen-posix-lock-obj >lock-obj-pub.native.h
# which is included in gpg-error.h 32/64 bit headers
#
# But need following in common header file
# (alternative is to copy the entirety of both into a common header)
#
# #ifndef __64BIT__
# #define GPGRT_LOCK_INITIALIZER {1,{{0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,2}}}
# #else
# #define GPGRT_LOCK_INITIALIZER {1,{{0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,2}}}
# #endif /* __64BIT__ */
#
#
# Using the merge option "--ifdef=__64BIT__" or "-D" of diff command produces
# following which does not compile
#
# #define GPGRT_LOCK_INITIALIZER {1,{{0,0,0,0,0,0,0,0, \
# #ifdef __64BIT__
#                                     0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,0, \
#                                     0,0,0,0,0,0,0,0, \
# #endif /* __64BIT__ */
#
# So add a space to the 2 lines of 32 bit version before diff command (hack!)

# if diff --ifdef=__64BIT__  ./src/gpg-error.h  ../64bit/src/gpg-error.h > src/gpg-error.h.32_64

if cat ./src/gpg-error.h | sed '/define GPGRT_LOCK_INITIALIZER/,+1s/$/ /' | diff --ifdef=__64BIT__ --  -   ../64bit/src/gpg-error.h > src/gpg-error.h.32_64
then
  echo No diff in 32 / 64 bit gpg-error.h is unexpected
else
  sed -i '/define GPGRT_LOCK_INITIALIZER/s/ $//' src/gpg-error.h.32_64
  cp src/gpg-error.h.32_64 src/gpgrt.h.32_64
fi

/opt/freeware/bin/install -c -m 644 src/gpg-error.h.32_64 ${RPM_BUILD_ROOT}%{_includedir}/gpg-error.h
# If no diff found, next command will fail
/opt/freeware/bin/install -c -m 644 src/gpgrt.h.32_64 ${RPM_BUILD_ROOT}%{_includedir}/gpgrt.h

# For %%check the tests need to be rebuilt using the common header

mv ./src/gpg-error.h ./src/gpg-error.h.32
mv ./src/gpgrt.h ./src/gpgrt.h.32
cp ./src/gpg-error.h.32_64 ./src/gpg-error.h
cp ./src/gpgrt.h.32_64 ./src/gpgrt.h

mv ../64bit/src/gpg-error.h ../64bit/src/gpg-error.h.64
mv ../64bit/src/gpgrt.h ../64bit/src/gpgrt.h.64
cp ./src/gpg-error.h.32_64 ../64bit/src/gpg-error.h
cp ./src/gpgrt.h.32_64 ../64bit/src/gpgrt.h

# Add libgpg-error.so.0 and libgpg-error.so & .so.0.28.0 - they may be required
install -p src/.libs/libgpg-error.so.%{libgpg_error_version} ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.so.%{libgpg_error_version}
ln -sf  libgpg-error.so.%{libgpg_error_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.so
ln -sf  libgpg-error.so.%{libgpg_error_version}     ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.so.%{libgpg_error_fullversion}

# Following is done in case a future version is incompatible
mv    ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.a ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error-%{libgpg_error_fullversion}.a
ln -s libgpg-error-%{libgpg_error_fullversion}.a ${RPM_BUILD_ROOT}%{_libdir}/libgpg-error.a
ln -s ../lib/libgpg-error.a ${RPM_BUILD_ROOT}%{_libdir64}/libgpg-error.a

# rm "$RPM_BUILD_ROOT%{_libdir}"/*.la

# No more used
#	(
#	  cd ${RPM_BUILD_ROOT}
#	  for dir in bin include lib
#	  do
#	    mkdir -p usr/${dir}
#	    cd usr/${dir}
#	    ln -sf ../..%{_prefix}/${dir}/* .
#	    cd -
#	  done
#	)

# Compress this .info file
gzip ${RPM_BUILD_ROOT}%{_infodir}/gpgrt.info


%check

# Running "gmake test" requires an X display 
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Currently there are 8 tests

TRACE="--trace VERBOSE=1"
TRACE=""

# Test the 64 bit version
cd 64bit
export OBJECT_MODE=64
(gmake check $TRACE || true)

# Test the 32 bit version
cd ../32bit
export OBJECT_MODE=32
(gmake check $TRACE || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/COPYING 32bit/COPYING.LIB
%doc 32bit/AUTHORS 32bit/README 32bit/NEWS 32bit/ChangeLog
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.a
%{_libdir}/libgpg-error-%{libgpg_error_fullversion}.a
%{_libdir64}/libgpg-error.a
#	%{_libdir}/libgpg-error.so.0*
#	%{_libdir64}/libgpg-error.so.0*
%{_datadir}/libgpg-error
%{_datadir}/locale


%files devel
%defattr(-,root,system,-)
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m*
#	%{_libdir}/libgpg-error.so
#	%{_libdir64}/libgpg-error.so
#	%{_libdir}/*.la
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpg-error.m4
%{_datadir}/aclocal/gpgrt.m4
%{_infodir}/gpgrt.info*
%{_mandir}/man1/gpgrt-config.*


%changelog
* Wed Jun 09 2021 Tony Reix <tony.reix@atos.com> - 1.42-1
- Update to new version 1.42
- Update with Fedora 1.42-2.fc35 .spec file
- Do some cleaning

* Wed Aug 26 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.37-2
- Exclude the lib*.so files

* Thu Aug 06 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.37-1
- Update to version 1.37

* Fri Jul 31 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.31-2
- Adaptions for rebuild on laurel2 with RPM 4
- Correction to gpg-error.h / gpgrt.h to merge 32 & 64 bit initialiser

* Thu Sep 27 2018 Michael Wilson <michael.a.wilson@atos.com> - 1.31-1
- Update to version 1.31 inspired by Fedora

* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 1.27-1
- Re-port
-
- Based on Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.27-1

* Tue Jul 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-3
- Initial port on Aix6.1

* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net>  1.10-1
- Initial port on Aix5.3

