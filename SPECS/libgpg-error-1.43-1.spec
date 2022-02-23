# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

%define _smp_mflags -j4

# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}

Name:           libgpg-error
Version: 1.43
Release: 1
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
# Manage $HOME = / on AIX
Patch3: libgpg-error-1.42-aix-home.patch
# Use -pthread when multi-threading
Patch4: libgpg-error-1.43-configure-force-pthread-in-MT_CFLAGS-for-AIX.patch

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
%patch1 -p1
%patch3 -p1
%patch4 -p1

# Fedora .spec file does strange things about config:
#	gpg-error-config.in
#	gpg-error-config-test.sh.in
#	configure

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

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
%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"
%endif

build_libgpgerror() {
    ./configure -v --prefix=%{_prefix} \
		--infodir=%{_infodir} \
		--localedir=%{_datadir}/locale \
		--mandir=%{_mandir} \
		--libdir=$1 \
		--disable-static \
		--disable-rpath \
		--disable-languages

    gmake %{?_smp_mflags}
}

# -pthread is required for multi-threading (tests thread1)
# tls-model is required for Python tests
COMMON_CFLAGS="-ftls-model=global-dynamic -pthread"

# First build the 64-bit version
cd 64bit
export CFLAGS="$COMMON_CFLAGS"
export CC64=" ${CC__}  ${FLAG64} $CFLAGS"
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_libgpgerror %{_libdir64}

# Build the 32-bit version
cd ../32bit
export CFLAGS="$COMMON_CFLAGS -D_LARGE_FILES"
export CC32=" ${CC__}  ${FLAG32} $CFLAGS"
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_libgpgerror %{_libdir}

%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake install DESTDIR="$RPM_BUILD_ROOT"

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)

cd ../32bit
export OBJECT_MODE=32
gmake install DESTDIR="$RPM_BUILD_ROOT"

(
    # Change 32bit binaries' name and make default link towards 64bit
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _32 -e _64)
    do
	mv ${f} ${f}_32
	ln -sf ${f}_64 ${f}
    done
)


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


(
    %define libsoversion 0

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.%{libsoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
)

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

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
%{_libdir64}/libgpg-error.a
%{_datadir}/libgpg-error
%{_datadir}/locale


%files devel
%defattr(-,root,system,-)
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m*
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_datadir}/aclocal/gpg-error.m4
%{_datadir}/aclocal/gpgrt.m4
%{_infodir}/gpgrt.info*
%{_mandir}/man1/gpgrt-config.*


%changelog
* Mon Nov 08 2021 Clément Chigot <clement.chigot@atos.net> - 1.43-1
- Update to 1.43
- BullFreeware Compatibility Improvements

* Tue Jun 15 2021 Tony Reix <tony.reix@atos.com> - 1.42-2
- Use -pthread rather than -D_THREAD_SAFE on AIX

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

