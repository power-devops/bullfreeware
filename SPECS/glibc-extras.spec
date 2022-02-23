%define glibcsrcdir  glibc-extras-2.21
%define glibcversion 2.21
%define glibcrelease 5%{?dist}
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
%define glibc_release_url http://ftp.gnu.org/gnu/glibc/
##############################################################################
# If run_glibc_tests is zero then tests are not run for the build.
# You must always set run_glibc_tests to one for production builds.
%define run_glibc_tests 1
# Run valgrind test to ensure compatibility.
%ifarch %{ix86} x86_64 ppc ppc64le s390x armv7hl aarch64
%define run_valgrind_tests 1
%endif
# Disable -Werror in builds for these architectures
%ifarch s390x
%define disable_werror 1
%endif
# Disable -Werror if we're bootstrapping
%{!?_with_bootstrap: %global disable_werror 1}

##############################################################################
# Auxiliary arches are those arches that can be built in addition
# to the core supported arches. You either install an auxarch or
# you install the base arch, not both. You would do this in order
# to provide a more optimized version of the package for your arch.
%define auxarches athlon alphaev6
##############################################################################
# Enable lock elision support for these architectures
#
# At the moment lock elision is disabled on x86_64 until there's a CPU that
# would actually benefit from enabling it.  Intel released a microcode update
# to disable HLE and RTM at boot and the Fedora kernel now applies it early
# enough that keeping lock elision enabled should be harmless, but we have
# disabled it anyway as a conservative measure.
%define lock_elision_arches s390 s390x
##############################################################################
# We build a special package for Xen that includes TLS support with
# no negative segment offsets for use with Xen guests. This is
# purely an optimization for increased performance on those arches.
%define xenarches i686 athlon
%ifarch %{xenarches}
%define buildxen 1
%define xenpackage 0
%else
%define buildxen 0
%define xenpackage 0
%endif
##############################################################################
# For Power we actually support alternate runtimes in the same base package.
# If we build for Power or Power64 we additionally build a power6 runtime that
# is enabled by AT_HWCAPS selection and an alternate runtime directory.
%ifarch ppc ppc64
%define buildpower6 1
%else
%define buildpower6 0
%endif
##############################################################################
# We build librtkaio for all rtkaioarches. The library is installed into
# a distinct subdirectory in the lib dir. This define enables the rtkaio
# add-on during the build. Upstream does not have rtkaio and it is provided
# strictly as part of our builds.
%define rtkaioarches %{ix86} x86_64 ppc %{power64} s390 s390x
##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%define biarcharches %{ix86} x86_64 ppc %{power64} s390 s390x
##############################################################################
# If the debug information is split into two packages, the core debuginfo
# pacakge and the common debuginfo package then the arch should be listed
# here. If the arch is not listed here then a single core debuginfo package
# will be created for the architecture.
%define debuginfocommonarches %{biarcharches} alpha alphaev6
##############################################################################
# If the architecture has multiarch support in glibc then it should be listed
# here to enable support in the build. Multiarch support is a single library
# with implementations of certain functions for multiple architectures. The
# most optimal function is selected at runtime based on the hardware that is
# detected by glibc. The underlying support for function selection and
# execution is provided by STT_GNU_IFUNC.
%define multiarcharches ppc %{power64} %{ix86} x86_64 %{sparc}
##############################################################################
# Add -s for a less verbose build output.
%define silentrules PARALLELMFLAGS=
##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc-extras
Version: %{glibcversion}
Release: %{glibcrelease}
# GPLv2+ is used in a bunch of programs, LGPLv2+ is used for libraries.
# Things that are linked directly into dynamically linked programs
# and shared libraries (e.g. crt files, lib*_nonshared.a) have an additional
# exception which allows linking it into any kind of programs or shared
# libraries without restrictions.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: System Environment/Libraries
URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.gz
#Source1: build-locale-archive.c
#Source2: glibc_post_upgrade.c
#Source3: libc-lock.h
#Source4: nscd.conf
#Source7: nsswitch.conf
#Source8: power6emul.c

##############################################################################
# Start of glibc patches
##############################################################################
# 0000-0999 for patches which are unlikely to ever go upstream or which
# have not been analyzed to see if they ought to go upstream yet.
#
# 1000-2000 for patches that are already upstream.
#
# 2000-3000 for patches that are awaiting upstream approval
#
# Yes, I realize this means some gratutious changes as patches to from
# one bucket to another, but I find this scheme makes it easier to track
# the upstream divergence and patches needing approval.
#
# Note that we can still apply the patches in any order we see fit, so
# the changes from one bucket to another won't necessarily result in needing
# to twiddle the patch because of dependencies on prior patches and the like.


##############################################################################
#
# Patches that are unlikely to go upstream or not yet analyzed.
#
##############################################################################

# Configuration twiddle, not sure there's a good case to get upstream to
# change this.
#Patch0001: %{name}-fedora-nscd.patch
#
#Patch0003: %{name}-fedora-ldd.patch
#
#Patch0004: %{name}-fedora-ppc-unwind.patch
#
## Build info files in the source tree, then move to the build
## tree so that they're identical for multilib builds
#Patch0005: %{name}-rh825061.patch
#
## Horrible hack, never to be upstreamed.  Can go away once the world
## has been rebuilt to use the new ld.so path.
#Patch0006: %{name}-arm-hardfloat-3.patch
#
## Needs to be sent upstream
#Patch0009: %{name}-fedora-include-bits-ldbl.patch
#
## All these were from the glibc-fedora.patch mega-patch and need another
## round of reviewing.  Ideally they'll either be submitted upstream or
## dropped.
#Patch0012: %{name}-fedora-linux-tcsetattr.patch
#Patch0014: %{name}-fedora-nptl-linklibc.patch
#Patch0015: %{name}-fedora-localedef.patch
#Patch0016: %{name}-fedora-i386-tls-direct-seg-refs.patch
#Patch0019: %{name}-fedora-nis-rh188246.patch
#Patch0020: %{name}-fedora-manual-dircategory.patch
#Patch0024: %{name}-fedora-locarchive.patch
#Patch0025: %{name}-fedora-streams-rh436349.patch
#Patch0028: %{name}-fedora-localedata-rh61908.patch
#Patch0030: %{name}-fedora-uname-getrlimit.patch
#Patch0031: %{name}-fedora-__libc_multiple_libcs.patch
#Patch0033: %{name}-fedora-elf-ORIGIN.patch
#Patch0034: %{name}-fedora-elf-init-hidden_undef.patch
#
## Needs to be sent upstream.
## Support mangling and demangling null pointers.
#Patch0037: %{name}-rh952799.patch
#
## rtkaio and c_stubs.  Note that despite the numbering, these are always
## applied first.
#Patch0038: %{name}-rtkaio.patch
#Patch0039: %{name}-c_stubs.patch
#
## Remove non-ELF support in rtkaio
#Patch0040: %{name}-rh731833-rtkaio.patch
#Patch0041: %{name}-rh731833-rtkaio-2.patch
#Patch0042: %{name}-rh970865.patch
#
## ARM: Accept that some objects marked hard ABI are now not because of a
##      binutils bug.
#Patch0044: %{name}-rh1009145.patch
#
## Allow applications to call pthread_atfork without libpthread.so.
#Patch0046: %{name}-rh1013801.patch
#
#Patch0047: %{name}-nscd-sysconfig.patch
#
## Allow up to 32 libraries to use static TLS. Should go upstream after
## more testing.
#Patch0050: %{name}-rh1124987.patch
#
## Disable rwlock elision if --enable-lock-elision is not used.
#Patch0052: %{name}-disable-rwlock-elision.patch
#
## confstr _CS_PATH should only return /usr/bin on Fedora since /bin is just a
## symlink to it.
#Patch0053: %{name}-cs-path.patch
#
## Remove the clock_* functions and use the ones in libc like librt does.
#Patch0054: %{name}-rtkaio-clock.patch
#
###############################################################################
##
## Patches from upstream
##
###############################################################################
## BZ #17949 - Fix __memcpy_chk on non-SSE2 CPUs.
#Patch1000: glibc-swbz17949.patch
#
##Unicode 7.0.0 update.
#Patch1001: glibc-rh1191059.patch
#
###############################################################################
##
## Patches submitted, but not yet approved upstream.
##
###############################################################################
##
## Each should be associated with a BZ.
## Obviously we're not there right now, but that's the goal
##
#
## http://sourceware.org/ml/libc-alpha/2012-12/msg00103.html
#Patch2007: %{name}-rh697421.patch
#
#Patch2011: %{name}-rh757881.patch
#
#Patch2013: %{name}-rh741105.patch
#
## Upstream BZ 14247
#Patch2023: %{name}-rh827510.patch
#
## Upstream BZ 13028
#Patch2026: %{name}-rh841787.patch
#
## Upstream BZ 14185
#Patch2027: %{name}-rh819430.patch
#
#Patch2031: %{name}-rh1070416.patch
#
#Patch2033: %{name}-aarch64-tls-fixes.patch
#Patch2034: %{name}-aarch64-workaround-nzcv-clobber-in-tlsdesc.patch

##############################################################################
# End of glibc patches.
##############################################################################

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes: glibc-profile < 2.4
Obsoletes: nss_db
Provides: ldconfig

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# This is a short term need until everything is rebuilt in the ARM world
# to use the new dynamic linker path
%ifarch armv7hl armv7hnl
Provides: ld-linux.so.3
Provides: ld-linux.so.3(GLIBC_2.4)
%endif

#Requires: glibc-common = %{version}-%{release}

# Require libgcc in case some program calls pthread_cancel in its %%post
#Requires(pre): basesystem, libgcc

# This is for building auxiliary programs like memusage, nscd
# For initial glibc bootstraps it can be commented out
#BuildRequires: gd-devel libpng-devel zlib-devel texinfo, libselinux-devel >= 1.33.4-3
#BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext, nss-devel
#BuildRequires: /bin/ps, /bin/kill, /bin/awk
#BuildRequires: systemtap-sdt-devel
BuildRequires: findutils >= 4.4.2

%if 0%{?run_valgrind_tests}
#BuildRequires: /usr/bin/valgrind
%endif

# We use systemd rpm macros for nscd
#BuildRequires: systemd

# This is to ensure that __frame_state_for is exported by glibc
# will be compatible with egcs 1.x.y
BuildRequires: gcc >= 3.2
#%define enablekernel 2.6.32
#Conflicts: kernel < %{enablekernel}
%define target powerpc-ibm-aix-7.1.0.0

%ifarch %{multiarcharches}
# Need STT_IFUNC support
%ifarch ppc %{power64}
#BuildRequires: binutils >= 2.20.51.0.2
#Conflicts: binutils < 2.20.51.0.2
%else
%ifarch s390 s390x
# Needed for STT_GNU_IFUNC support for s390/390x
BuildRequires: binutils >= 2.23.52.0.1-8
Conflicts: binutils < 2.23.52.0.1-8
%else
# Default to this version
BuildRequires: binutils >= 2.19.51.0.10
Conflicts: binutils < 2.19.51.0.10
%endif
%endif
# Earlier releases have broken support for IRELATIVE relocations
#Conflicts: prelink < 0.4.2
%else
# Need AS_NEEDED directive
# Need --hash-style=* support
#BuildRequires: binutils >= 2.17.50.0.2-5
%endif

BuildRequires: gcc >= 3.2.1-5
%ifarch ppc s390 s390x
BuildRequires: gcc >= 4.1.0-0.17
%endif
%if 0%{?_enable_debug_packages}
#BuildRequires: elfutils >= 0.72
#BuildRequires: rpm >= 4.2-0.56
%endif

# The testsuite builds static C++ binaries that require a static
# C++ runtime from libstdc++-static.
#BuildRequires: libstdc++-static

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1

%description
The glibc-extras package contains functions of the GNU libC that are not present
in AIX. It currently contains the io/fts submodule.

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Group: Development/Libraries
#Requires(pre): /sbin/install-info
#Requires(pre): %{name}-headers
Requires: %{name}-headers = %{version}-%{release}
Requires: %{name} = %{version}-%{release}

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "headers" sub-package
##############################################################################
%package headers
Summary: Header files for development using standard C libraries.
Group: Development/Libraries
Provides: %{name}-headers(%{_target_cpu})
%ifarch x86_64
# If both -m32 and -m64 is to be supported on AMD64, x86_64 glibc-headers
# have to be installed, not i586 ones.
Obsoletes: %{name}-headers(i586)
Obsoletes: %{name}-headers(i686)
%endif
#Requires(pre): kernel-headers
#Requires: kernel-headers >= 2.2.1, %{name} = %{version}-%{release}
#BuildRequires: kernel-headers >= 2.6.22

%description headers
The glibc-headers package contains the header files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard header files available in order to create the
executables.

Install glibc-headers if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc core "debuginfo" sub-package
##############################################################################
%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%global __debug_package 1

%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
AutoReqProv: no
%ifarch %{debuginfocommonarches}
Requires: glibc-debuginfo-common = %{version}-%{release}
%else
%ifarch %{ix86} %{sparc}
Obsoletes: glibc-debuginfo-common
%endif
%endif

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

This package also contains static standard C libraries with
debugging information.  You need this only if you want to step into
C library routines during debugging programs statically linked against
one or more of the standard C libraries.
To use this debugging information, you need to link binaries
with -static -L%{_prefix}/lib/debug%{_libdir} compiler options.
%endif
##############################################################################
# Prepare for the build.
##############################################################################
%prep
%setup -q -n %{glibcsrcdir}

# Patch order is important as some patches depend on other patches and
# therefore the order must not be changed.  First two are rtkaio and c_stubs;
# we maintain this only in Fedora.
#%patch0038 -p1
#%patch0039 -p1
#%patch0001 -p1
#%patch0003 -p1
#%patch0004 -p1
#%patch0005 -p1
#%patch0006 -p1
#%patch2007 -p1
#%patch0009 -p1
#%patch2011 -p1
#%patch0012 -p1
#%patch2013 -p1
#%patch0014 -p1
#%patch0015 -p1
#%patch0016 -p1
#%patch0019 -p1
#%patch0020 -p1
#%patch2023 -p1
#%patch0024 -p1
#%patch0025 -p1
#%patch2026 -p1
#%patch2027 -p1
#%patch0028 -p1
#%patch0030 -p1
#%patch0031 -p1
#%patch0033 -p1
#%patch0034 -p1
#%patch0037 -p1
#%patch0040 -p1
#%patch0041 -p1
#%patch0042 -p1
#%patch0044 -p1
#%patch0046 -p1
#%patch2031 -p1
#%patch0047 -p1
#%patch2033 -p1
#%patch2034 -p1
#%patch0050 -p1
#%patch0052 -p1
#%patch0053 -p1
#%patch0054 -p1
#%patch1000 -p1
#%patch1001 -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################

# XXX: This sounds entirely out of date, particularly in light of the fact
#      that we want to be building newer Power support. We should review this
#      and potentially remove this workaround. However it will require
#      determining which arches we support building for on our distributions.
# ~~~
# On powerpc32, hp timing is only available in power4/power6
# libs, not in base, so pre-power4 dynamic linker is incompatible
# with power6 libs.
# ~~~
%if "%{buildpower6}" == "1"
rm -f sysdeps/powerpc/powerpc32/power4/hp-timing.[ch]
%endif

# Remove all files generated from patching.
/opt/freeware/bin/find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `/opt/freeware/bin/find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
#touch locale/programs/*-kw.h

##############################################################################
# Build glibc...
##############################################################################
%build

# We build using the native system compilers.
GCC=/opt/freeware/bin/gcc
GXX=/opt/freeware/bin/g++

##############################################################################
# %%build - x86 options.
##############################################################################
# On x86 we build for the specific target cpu rpm is using.
%ifarch %{ix86}
BuildFlags="-march=%{_target_cpu} -mtune=generic"
%endif
# We don't support building for i386. The generic i386 architecture lacks the
# atomic primitives required for NPTL support. However, when a user asks to
# build for i386 we interpret that as "for whatever works on x86" and we
# select i686. Thus we treat i386 as an alias for i686.
%ifarch i386 i686
BuildFlags="-march=i686 -mtune=generic"
%endif
%ifarch i486 i586
%endif
%ifarch x86_64
BuildFlags="-mtune=generic"
%endif

##############################################################################
# %%build - SPARC options.
##############################################################################
%ifarch sparc
BuildFlags="-fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparcv9
BuildFlags="-mcpu=ultrasparc -fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparcv9v
BuildFlags="-mcpu=niagara -fcall-used-g6"
GCC="gcc -m32"
GXX="g++ -m32"
%endif
%ifarch sparc64
BuildFlags="-mcpu=ultrasparc -mvis -fcall-used-g6"
GCC="gcc -m64"
GXX="g++ -m64"
%endif
%ifarch sparc64v
BuildFlags="-mcpu=niagara -mvis -fcall-used-g6"
GCC="gcc -m64"
GXX="g++ -m64"
%endif
%ifarch %{power64}
BuildFlags=""
GCC="gcc -m64"
GXX="g++ -m64"
%endif

##############################################################################
# %%build - Generic options.
##############################################################################
BuildFlags="$BuildFlags -fasynchronous-unwind-tables"
# Add -DNDEBUG unless using a prerelease
case %{version} in
  *.*.9[0-9]*) ;;
  *)
     BuildFlags="$BuildFlags -DNDEBUG"
     ;;
esac
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc
AddOns=`echo */configure | sed -e 's!/configure!!g;s!\(linuxthreads\|nptl\|rtkaio\|powerpc-cpu\)\( \|$\)!!g;s! \+$!!;s! !,!g;s!^!,!;/^,\*$/d'`
%ifarch %{rtkaioarches}
AddOns=,rtkaio$AddOns
%endif

##############################################################################
# build()
#	Build glibc in `build-%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, add-ons, kernel
#	version, multiarch support, system tap support, etc.
##############################################################################
build()
{
	builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
    mkdir -p ${builddir}/linkobj
    mkdir -p ${builddir}/elf
	cd $builddir
	build_CFLAGS="$BuildFlags -g -O3 $*"
	# Some configure checks can spuriously fail for some architectures if
	# unwind info is present
	configure_CFLAGS="$build_CFLAGS -fno-asynchronous-unwind-tables -maix64"
    configure_ARFLAGS="-X 64"
    export OBJECT_MODE=64
	../configure CC="$GCC" CXX="$GXX" CFLAGS="$configure_CFLAGS" ARFLAGS="$configure_ARFLAGS" \
		--prefix=%{_prefix} \
%ifarch ppc64p7
		--with-cpu=power7 \
%endif
     || { cat config.log; false; }

	/opt/freeware/bin/make -d %{?_smp_mflags} -r CFLAGS="$build_CFLAGS" %{silentrules}
	cd -
}

##############################################################################
# Build glibc for the default set of options.
##############################################################################
build

##############################################################################
# Build glibc for xen:
# If we support xen build glibc again for xen support.
##############################################################################
%if "%{buildxen}"
%endif

##############################################################################
# Build glibc for power6:
# If we support building a power6 alternate runtime then built glibc again for
# power6.
# XXX: We build in a sub-shell for no apparent reason.
##############################################################################
%if "%{buildpower6}"
#(
#	platform=`LD_SHOW_AUXV=1 /bin/true | sed -n 's/^AT_PLATFORM:[[:blank:]]*//p'`
#	if [ "$platform" != power6 ]; then
#		mkdir -p power6emul/{lib,lib64}
#		$GCC -shared -O2 -fpic -o power6emul/%{_lib}/power6emul.so %{SOURCE8} -Wl,-z,initfirst
#%ifarch ppc
#		gcc -shared -nostdlib -O2 -fpic -m64 -o power6emul/lib64/power6emul.so -xc - </dev/null
#%endif
#%ifarch ppc64
#		gcc -shared -nostdlib -O2 -fpic -m32 -o power6emul/lib/power6emul.so -xc - < /dev/null
#%endif
#		export LD_PRELOAD=`pwd`/power6emul/\$LIB/power6emul.so
#	fi
#	AddOns="$AddOns --with-cpu=power6"
#	GCC="$GCC -mcpu=power6"
#	GXX="$GXX -mcpu=power6"
#	build power6
#)
%endif # %{buildpower6}

##############################################################################
# Build the glibc post-upgrade program:
# We only build one of these with the default set of options. This program
# must be able to run on all hardware for the lowest common denomintor since
# we only build it once.
##############################################################################
#pushd build-%{target}
#$GCC -static -L. -Os -g %{SOURCE2} \
#	-o glibc_post_upgrade.%{_target_cpu} \
#	'-DLIBTLS="/%{_lib}/tls/"' \
#	'-DGCONV_MODULES_DIR="%{_libdir}/gconv"' \
#	'-DLD_SO_CONF="/etc/ld.so.conf"' \
#	'-DICONVCONFIG="%{_sbindir}/iconvconfig.%{_target_cpu}"'
#popd

##############################################################################
# Install glibc...
##############################################################################
%install

# Ensure the permissions of errlist.c do not change.  When the file is
# regenerated the Makefile sets the permissions to 444. We set it to 644
# to match what comes out of git. The tarball of the git archive won't have
# correct permissions because git doesn't track all of the permissions
# accurately (see git-cache-meta if you need that). We also set it to 644 to
# match pre-existing rpms. We do this *after* the build because the build
# might regenerate the file and set the permissions to 444.
chmod 644 sysdeps/gnu/errlist.c

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

# Cleanup any previous installs...
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
/opt/freeware/bin/make -j1 install_root=$RPM_BUILD_ROOT \
	install -C build-%{target} %{silentrules}

# If we are not building an auxiliary arch then install all of the supported
# locales.
#%ifnarch %{auxarches}
#cd build-%{target}
#/opt/freeware/bin/make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT \
#	install-locales -C ../localedata objdir=`pwd`
#cd -
#%endif

##############################################################################
# Install rtkaio libraries.
##############################################################################
#%ifarch %{rtkaioarches}
#librtso=`basename $RPM_BUILD_ROOT/%{_lib}/librt.so.*`
#rm -f $RPM_BUILD_ROOT{,%{_prefix}}/%{_lib}/librtkaio.*
#rm -f $RPM_BUILD_ROOT%{_libdir}/librt.so.*
#mkdir -p $RPM_BUILD_ROOT/%{_lib}/rtkaio
#mv $RPM_BUILD_ROOT/%{_lib}/librtkaio-*.so $RPM_BUILD_ROOT/%{_lib}/rtkaio/
#rm -f $RPM_BUILD_ROOT/%{_lib}/$librtso
#ln -sf `basename $RPM_BUILD_ROOT/%{_lib}/librt-*.so` $RPM_BUILD_ROOT/%{_lib}/$librtso
#ln -sf `basename $RPM_BUILD_ROOT/%{_lib}/rtkaio/librtkaio-*.so` $RPM_BUILD_ROOT/%{_lib}/rtkaio/$librtso
#%endif

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
%ifarch %{rtkaioarches}
	local rtkdestdir="$RPM_BUILD_ROOT/%{_lib}/rtkaio/$subdir"
	local librtso=`basename $RPM_BUILD_ROOT/%{_lib}/librt.so.*`
	mkdir -p $rtkdestdir
	librtkaioso=$(basename $RPM_BUILD_ROOT/%{_lib}/librt-*.so | sed s/librt-/librtkaio-/)
	if cmp -s rtkaio/librtkaio.so ../build-%{target}/rtkaio/librtkaio.so; then
		ln -s %{nosegneg_subdir_up}/$librtkaioso $rtkdestdir/$librtkaioso
	else
		cp -a rtkaio/librtkaio.so $rtkdestdir/$librtkaioso
	fi
	ln -sf $librtkaioso $rtkdestdir/$librtso
%endif
}

##############################################################################
# Install the xen build files.
##############################################################################
#%if "%{buildxen}"
#%define nosegneg_subdir_base i686
#%define nosegneg_subdir i686/nosegneg
#%define nosegneg_subdir_up ../..
#cd build-%{target}-nosegneg
#destdir=$RPM_BUILD_ROOT/%{_lib}
#install_different "$destdir" "%{nosegneg_subdir}" "%{nosegneg_subdir_up}"
#cd -
#%endif # %{buildxen}

##############################################################################
# Install the power6 build files.
##############################################################################
#%if "%{buildpower6}"
#%define power6_subdir power6
#%define power6_subdir_up ..
#%define power6_legacy power6x
#%define power6_legacy_up ..
#cd build-%{target}-power6
#destdir=$RPM_BUILD_ROOT/%{_lib}
#install_different "$destdir" "%{power6_subdir}" "%{power6_subdir_up}"
## Make a legacy /usr/lib[64]/power6x directory that is a symlink to the
## power6 runtime.
## XXX: When can we remove this? What is the history behind this?
#mkdir -p ${destdir}/%{power6_legacy}
#cd -
#cd build-%{target}-power6/${destdir}/%{power6_legacy}
#ln -sf %{power6_legacy_up}/%{power6_subdir}/*.so .
#cp -a %{power6_legacy_up}/%{power6_subdir}/*.so.* .
#cd -
#%ifarch %{rtkaioarches}
#destdir=${destdir}/rtkaio
#mkdir -p ${destdir}/%{power6_legacy}
#cd build-%{target}-power6/${destdir}/%{power6_legacy}
#ln -sf ../power6/*.so .
#cp -a ../power6/*.so.* .
#cd -
#%endif
#%endif # %{buildpower6}

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f $RPM_BUILD_ROOT%{_libdir}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*

# rquota.x and rquota.h are now provided by quota
rm -f $RPM_BUILD_ROOT%{_prefix}/include/rpcsvc/rquota.[hx]

# In F7+ this is provided by rpcbind rpm
rm -f $RPM_BUILD_ROOT%{_sbindir}/rpcinfo

# Remove the old nss modules.
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss1-*
rm -f ${RPM_BUILD_ROOT}/%{_lib}/libnss-*.so.1

##############################################################################
# Install info files
##############################################################################

## Move the info files if glibc installed them into the wrong location.
#if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
#  mkdir -p $RPM_BUILD_ROOT%{_infodir}
#  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
#  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
#fi
#
## Compress all of the info files.
#gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

##############################################################################
# Install locale files
##############################################################################

# Create archive of locale files
#%ifnarch %{auxarches}
#olddir=`pwd`
#cd ${RPM_BUILD_ROOT}%{_prefix}/lib/locale
#rm -f locale-archive
## Intentionally we do not pass --alias-file=, aliases will be added
## by build-locale-archive.
#$olddir/build-%{target}/elf/ld.so \
#	--library-path $olddir/build-%{target}/ \
#	$olddir/build-%{target}/locale/localedef \
#	--prefix ${RPM_BUILD_ROOT} --add-to-archive \
#	*_*
#rm -rf *_*
#mv locale-archive{,.tmpl}
#cd -
#%endif

##############################################################################
# Install configuration files for services
##############################################################################

#install -p -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/nsswitch.conf
#
#%ifnarch %{auxarches}
#mkdir -p $RPM_BUILD_ROOT/etc/default
#install -p -m 644 nis/nss $RPM_BUILD_ROOT/etc/default/nss
#
## This is for ncsd - in glibc 2.2
#install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc
#mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
#install -m 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}
#mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
#install -m 644 nscd/nscd.service nscd/nscd.socket $RPM_BUILD_ROOT/lib/systemd/system
#%endif
#
## Include ld.so.conf
#echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
#truncate -s 0 $RPM_BUILD_ROOT/etc/ld.so.cache
#chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
#mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
#%ifnarch %{auxarches}
#mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
#truncate -s 0 $RPM_BUILD_ROOT/etc/sysconfig/nscd
#truncate -s 0 $RPM_BUILD_ROOT/etc/gai.conf
#%endif
#
## Include %{_libdir}/gconv/gconv-modules.cache
#truncate -s 0 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
#chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

##############################################################################
# Misc...
##############################################################################

# NPTL <bits/stdio-lock.h> is not usable outside of glibc, so include
# the generic one (#162634)
#cp -a bits/stdio-lock.h $RPM_BUILD_ROOT%{_prefix}/include/bits/stdio-lock.h
# And <bits/libc-lock.h> needs sanitizing as well.
#cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/include/bits/libc-lock.h

# XXX: What is this for?
#ln -sf libbsd-compat.a $RPM_BUILD_ROOT%{_libdir}/libbsd.a

# Install the upgrade program
#install -m 700 build-%{target}/glibc_post_upgrade.%{_target_cpu} \
#  $RPM_BUILD_ROOT%{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

# Strip all of the installed object files.
#strip -g $RPM_BUILD_ROOT%{_libdir}/*.o

# XXX: Ugly hack for buggy rpm. What bug? BZ? Is this fixed?
#ln -f ${RPM_BUILD_ROOT}%{_sbindir}/iconvconfig{,.%{_target_cpu}}

##############################################################################
# Install debug copies of unstripped static libraries
# - This step must be last in order to capture any additional static
#   archives we might have added.
##############################################################################

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if "0%{?_enable_debug_packages}"
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}
cp -dR $RPM_BUILD_ROOT%{_libdir}/*.a \
	$RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/*_p.a
%endif

mv $RPM_BUILD_ROOT/opt/freeware/lib/libcextrasextras.a $RPM_BUILD_ROOT/opt/freeware/lib/libcextras.a
rm -f $RPM_BUILD_ROOT/opt/freeware/lib/libcextrasextras_nonshared.a
rm -f $RPM_BUILD_ROOT/opt/freeware/lib/libcextras.so
mv $RPM_BUILD_ROOT/opt/freeware/lib/libcextras-2.21.90.so $RPM_BUILD_ROOT/opt/freeware/lib/libcextras.so

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are 11 file lists:
# * rpm.fileslist
#	- Master file list. Eventually, after removing files from this list
#	  we are left with the list of files for the glibc package.
# * common.filelist
#	- Contains the list of flies for the common subpackage.
# * utils.filelist
#	- Contains the list of files for the utils subpackage.
# * nscd.filelist
#	- Contains the list of files for the nscd subpackage.
# * devel.filelist
#	- Contains the list of files for the devel subpackage.
# * headers.filelist
#	- Contains the list of files for the headers subpackage.
# * static.filelist
#	- Contains the list of files for the static subpackage.
# * nosegneg.filelist
#	- Contains the list of files for the xen subpackage.
# * debuginfo.filelist
#	- Contains the list of files for the glibc debuginfo package.
# * debuginfocommon.filelist
#	- Contains the list of files for the glibc common debuginfo package.
#

{
  /opt/freeware/bin/find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  # Print all directories with a %%dir prefix.  We omit the info directory and
  # all directories in (and including) /usr/share/locale.
  /opt/freeware/bin/find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' ! -path '*%{_infodir}' -o \
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {

  # primary filelist

  # Add %%lang entries for language-specific locale files.  This allows users
  # to set %%_install_lang and not install the unnecessary locale files.
  I18N_LANG='s|.*/share/i18n/locales/\([a-z]\{2\}[a-z]\?\)_[A-Z]\{2\}.*|%lang(\1) &|'
  # Remove the *.mo entries.  We will add that using %%find_lang
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e "$I18N_LANG" \
      -e '\,/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,/%{_lib}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > rpm.filelist

# Our *.mo files.  Put them in glibc-common.
#%find_lang libc
#mv libc.lang common.filelist

mkdir -p $RPM_BUILD_ROOT%{_libdir}
#mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so $RPM_BUILD_ROOT%{_libdir}

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
#for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
#  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
#      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
#      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
#      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
#      -i $i
#done

# Put the info files into the devel file list.
touch devel.filelist
#grep '%{_infodir}' < rpm.filelist | grep -v '%{_infodir}/dir' > devel.filelist

# Put the stub headers into the devel file list.
#grep '%{_prefix}/include/gnu/stubs-[^.]\+\.h' < rpm.filelist >> devel.filelist || :

# Put the include files into headers file list.
grep '%{_prefix}/include' < rpm.filelist |
	egrep -v '%{_prefix}/include/(linuxthreads|gnu/stubs-[^.]+\.h)' \
	> headers.filelist

# Remove partial (lib*_p.a) static libraries, include files, and info files from
# the core glibc package.
sed -i -e '\|%{_libdir}/lib.*_p.a|d' \
       -e '\|%{_prefix}/include|d' \
       -e '\|%{_infodir}|d' rpm.filelist

# Put some static files into the devel package.
#grep '%{_libdir}/lib.*\.a' < rpm.filelist \
#  | grep '/lib\(\(cextras\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
#  >> devel.filelist

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < rpm.filelist \
  | grep -v '/lib\(\(cextras\|pthread\|nldbl\)_nonshared\|bsd\(\|-compat\)\|g\|ieee\|mcheck\|rpcsvc\)\.a$' \
  > static.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
#grep '%{_libdir}/.*\.o' < rpm.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < rpm.filelist >> devel.filelist

# Remove all of the static, object, unversioned DSOs, old linuxthreads stuff,
# and nscd from the core glibc package.
sed -i -e '\|%{_libdir}/lib.*\.a|d' \
       -e '\|%{_libdir}/.*\.o|d' \
       -e '\|%{_libdir}/lib.*\.so|d' \
       -e '\|%{_libdir}/linuxthreads|d' \
       -e '\|nscd|d' rpm.filelist

# All of the bin and certain sbin files go into the common package.
# We explicitly exclude certain sbin files that need to go into
# the core glibc package for use during upgrades.
#grep '%{_prefix}/bin' < rpm.filelist >> common.filelist
#grep '%{_prefix}/sbin/[^gi]' < rpm.filelist >> common.filelist
# All of the files under share go into the common package since
# they should be multilib-independent.
#grep '%{_prefix}/share' < rpm.filelist | \
#  grep -v -e '%{_prefix}/share/zoneinfo' -e '%%dir %{prefix}/share' \
#       >> common.filelist

# Remove the bin, locale, some sbin, and share from the
# core glibc package. We cheat a bit and use the slightly dangerous
# /usr/sbin/[^gi] to match the inverse of the search that put the
# files into common.filelist. It's dangerous in that additional files
# that start with g, or i would get put into common.filelist and
# rpm.filelist.
sed -i -e '\|%{_prefix}/bin|d' \
       -e '\|%{_prefix}/lib/locale|d' \
       -e '\|%{_prefix}/sbin/[^gi]|d' \
       -e '\|%{_prefix}/share|d' rpm.filelist

##############################################################################
# Build the xen package file list (nosegneg.filelist)
##############################################################################
##truncate -s 0 nosegneg.filelist
##%if "%{xenpackage}"
##grep '/%{_lib}/%{nosegneg_subdir}' < rpm.filelist >> nosegneg.filelist
##sed -i -e '\|/%{_lib}/%{nosegneg_subdir}|d' rpm.filelist
### TODO: There are files in the nosegneg list which should be in the devel
###	pacakge, but we leave them instead in the xen subpackage. We may
###	wish to clean that up at some point.
##%endif
##
### Add the binary to build localse to the common subpackage.
##echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist
##
### The nscd binary must go into the nscd subpackage.
##echo '%{_prefix}/sbin/nscd' > nscd.filelist
##
### The memusage and pcprofile libraries are put back into the core
### glibc package even though they are only used by utils package
### scripts..
##cat >> rpm.filelist <<EOF
##%{_libdir}/libmemusage.so
##%{_libdir}/libpcprofile.so
##EOF
##
### Add the utils scripts and programs to the utils subpackage.
##cat > utils.filelist <<EOF
##%{_prefix}/bin/memusage
##%{_prefix}/bin/memusagestat
##%{_prefix}/bin/mtrace
##%{_prefix}/bin/pcprofiledump
##%{_prefix}/bin/xtrace
##EOF

# Remove the zoneinfo files
# XXX: Why isn't this don't earlier when we are removing files?
#      Won't this impact what is shipped?
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent.  The choice of using
# glibc_post_upgrade.c is arbitrary.
#touch -r %{SOURCE2} $RPM_BUILD_ROOT/etc/ld.so.conf
#touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc

# We allow undefined symbols in shared libraries because the libraries
# referenced at link time here, particularly ld.so, may be different than
# the one used at runtime.  This is really only needed during the ARM
# transition from ld-linux.so.3 to ld-linux-armhf.so.3.
#cd build-%{target}
#$GCC -Os -g -static -o build-locale-archive %{SOURCE1} \
#	../build-%{target}/locale/locarchive.o \
#	../build-%{target}/locale/md5.o \
#	-I. -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
#	-L../build-%{target} \
#	-Wl,--allow-shlib-undefined \
#	-B../build-%{target}/csu/ -lc -lc_nonshared
#install -m 700 build-locale-archive $RPM_BUILD_ROOT%{_prefix}/sbin/build-locale-archive
#cd -

# Lastly copy some additional documentation for the packages.
#rm -rf documentation
#mkdir documentation
#cp crypt/README.ufc-crypt documentation/README.ufc-crypt
#cp timezone/README documentation/README.timezone
#cp posix/gai.conf documentation/

%ifarch s390x
# Compatibility symlink
mkdir -p $RPM_BUILD_ROOT/lib
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/lib/ld64.so.1
%endif

# Leave a compatibility symlink for the dynamic loader on armhfp targets,
# at least until the world gets rebuilt
%ifarch armv7hl armv7hnl
ln -sf /lib/ld-linux-armhf.so.3 $RPM_BUILD_ROOT/lib/ld-linux.so.3
%endif

###############################################################################
# Rebuild libpthread.a using --whole-archive to ensure all of libpthread
# is included in a static link. This prevents any problems when linking
# statically, using parts of libpthread, and other necessary parts not
# being included. Upstream has decided that this is the wrong approach to
# this problem and that the full set of dependencies should be resolved
# such that static linking works and produces the most minimally sized
# static application possible.
###############################################################################
#cd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
#$GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
#rm libpthread.a
#ar rcs libpthread.a libpthread.o
#rm libpthread.o
#cd -
###############################################################################

%if "0%{?_enable_debug_packages}"

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
#cd locale
#ln -s programs/*.gperf .
#cd -
#cd iconv
#ln -s ../locale/programs/charmap-kw.gperf .
#cd -

# Print some diagnostic information in the builds about the
# getconf binaries.
# XXX: Why do we do this?
#ls -l $RPM_BUILD_ROOT%{_prefix}/bin/getconf
#ls -l $RPM_BUILD_ROOT%{_prefix}/libexec/getconf
#eu-readelf -hS $RPM_BUILD_ROOT%{_prefix}/bin/getconf \
#	$RPM_BUILD_ROOT%{_prefix}/libexec/getconf/*
#
#find_debuginfo_args='--strict-build-id -g'
#%ifarch %{debuginfocommonarches}
#find_debuginfo_args="$find_debuginfo_args \
#	-l common.filelist \
#	-l utils.filelist \
#	-l nscd.filelist \
#	-p '.*/(sbin|libexec)/.*' \
#	-o debuginfocommon.filelist \
#	-l rpm.filelist \
#	-l nosegneg.filelist"
#%endif
#eval /usr/lib/rpm/find-debuginfo.sh \
#	"$find_debuginfo_args" \
#	-o debuginfo.filelist

# List all of the *.a archives in the debug directory.
list_debug_archives()
{
	local dir=%{_prefix}/lib/debug%{_libdir}
	/opt/freeware/bin/find $RPM_BUILD_ROOT$dir -name "*.a" -printf "$dir/%%P\n"
}

%ifarch %{debuginfocommonarches}

# Remove the source files from the common package debuginfo.
#sed -i '\#^%{_prefix}/src/debug/#d' debuginfocommon.filelist
#
## Create a list of all of the source files we copied to the debug directory.
#/opt/freeware/bin/find $RPM_BUILD_ROOT%{_prefix}/src/debug \
#     \( -type d -printf '%%%%dir ' \) , \
#     -printf '%{_prefix}/src/debug/%%P\n' > debuginfocommon.sources
#
#%ifarch %{biarcharches}
#
## Add the source files to the core debuginfo package.
#cat debuginfocommon.sources >> debuginfo.filelist
#
#%else
#
#%ifarch %{ix86}
#%define basearch i686
#%endif
#%ifarch sparc sparcv9
#%define basearch sparc
#%endif
#
## The auxarches get only these few source files.
#auxarches_debugsources=\
#'/(generic|linux|%{basearch}|nptl(_db)?)/|/%{glibcsrcdir}/build|/dl-osinfo\.h'
#
## Place the source files into the core debuginfo pakcage.
#egrep "$auxarches_debugsources" debuginfocommon.sources >> debuginfo.filelist
#
## Remove the source files from the common debuginfo package.
#egrep -v "$auxarches_debugsources" \
#  debuginfocommon.sources >> debuginfocommon.filelist
#
#%endif # %{biarcharches}

# Add the list of *.a archives in the debug directory to
# the common debuginfo package.
#list_debug_archives >> debuginfocommon.filelist
#
## It happens that find-debuginfo.sh produces duplicate entries even
## though the inputs are unique. Therefore we sort and unique the
## entries in the debug file lists. This avoids the following warnings:
## ~~~
## Processing files: glibc-debuginfo-common-2.17.90-10.fc20.x86_64
## warning: File listed twice: /usr/lib/debug/usr/sbin/build-locale-archive.debug
## warning: File listed twice: /usr/lib/debug/usr/sbin/nscd.debug
## warning: File listed twice: /usr/lib/debug/usr/sbin/zdump.debug
## warning: File listed twice: /usr/lib/debug/usr/sbin/zic.debug
## ~~~
#sort -u debuginfocommon.filelist > debuginfocommon2.filelist
#mv debuginfocommon2.filelist debuginfocommon.filelist
#
%endif # %{debuginfocommonarches}
#
## Remove any duplicates output by a buggy find-debuginfo.sh.
#sort -u debuginfo.filelist > debuginfo2.filelist
#mv debuginfo2.filelist debuginfo.filelist

# Remove some common directories from the common package debuginfo so that we
# don't end up owning them.
exclude_common_dirs()
{
	exclude_dirs="%{_prefix}/src/debug"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug{,/%{_lib},/bin,/sbin})"
	exclude_dirs="$exclude_dirs $(echo %{_prefix}/lib/debug%{_prefix}{,/%{_lib},/libexec,/bin,/sbin})"

	for d in $(echo $exclude_dirs | sed 's/ /\n/g'); do
		sed -i "\|^%%dir $d/\?$|d" $1
	done
}

#%ifarch %{debuginfocommonarches}
#exclude_common_dirs debuginfocommon.filelist
#%endif
#exclude_common_dirs debuginfo.filelist
#
%endif # 0%{?_enable_debug_packages}

# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%ifarch %{auxarches}

# Delete files that we do not intended to ship with the auxarch.
echo Cutting down the list of unpackaged files
sed -e '/%%dir/d;/%%config/d;/%%verify/d;s/%%lang([^)]*) //;s#^/*##' \
	common.filelist devel.filelist static.filelist headers.filelist \
	utils.filelist nscd.filelist \
#%ifarch %{debuginfocommonarches}
#	debuginfocommon.filelist \
#%endif
	| (cd $RPM_BUILD_ROOT; xargs --no-run-if-empty rm -f 2> /dev/null || :)

%else

#mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
#touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
#touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}
#
%endif # %{auxarches}
#
#%ifnarch %{auxarches}
#truncate -s 0 $RPM_BUILD_ROOT/%{_prefix}/lib/locale/locale-archive
#%endif
#
#mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
#truncate -s 0 $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

##############################################################################
# Run the glibc testsuite
##############################################################################
#%check
#%if "%{run_glibc_tests}"
#
## Run the glibc tests. If any tests fail to build we exit %check with an error
## of 1, otherwise we print the test failure list and the failed test output
## and exit with 0. In the future we want to compare against a baseline and
## exit with 1 if the results deviate from the baseline.
#run_tests () {
#	truncate -s 0 check.log
#	tail -f check.log &
#	tailpid=$!
#	# Run the make a sub-shell (to avoid %check failing if make fails)
#	# but capture the status for use later. We use the normal sub-shell
#	# trick of printing the status. The actual result of the sub-shell
#	# is the successful execution of the echo.
#	status=$(set +e
#		 /opt/freeware/bin/make %{?_smp_mflags} check %{silentrules} > check.log 2>&1
#		 status=$?
#		 echo $status)
#	# Wait for the tail to catch up with the output and then kill it.
#	sleep 10
#	kill $tailpid
#	# Print the header, so we can find it, but skip the error printing
#	# if there aren't any failrues.
#	echo ===================FAILED TESTS=====================
#	if [ $status -ne 0 ]; then
#		# We are not running with `-k`, therefore a test build failure
#		# terminates the test run and that terminates %check with an
#		# error which terminates the build. We want this behaviour to
#		# ensure that all tests build, and all tests run.
#		# If the test result summary is not present it means one of
#		# tests failed to build.
#		if ! grep 'Summary of test results:' check.log; then
#			echo "FAIL: Some glibc tests failed to build."
#			exit 1
#		fi
#
#		# Print out information about all of the failed tests.
#		grep -e ^FAIL -e ^ERROR tests.sum \
#			| awk '{print $2}' \
#			| while read testcase;
#		do
#			echo "$testcase"
#			cat $testcase.out
#			echo -------------------------
#		done
#	fi
#}
#
## Increase timeouts
#export TIMEOUTFACTOR=16
#parent=$$
#echo ====================TESTING=========================
###############################################################################
## - Test the default runtime.
###############################################################################
#cd build-%{target}
#run_tests
#cd -
#
###############################################################################
## - Test the xen runtimes (nosegneg).
###############################################################################
#%if "%{buildxen}"
#echo ====================TESTING -mno-tls-direct-seg-refs=============
#cd build-%{target}-nosegneg
#run_tests
#cd -
#%endif
#
###############################################################################
## - Test the power6 runtimes.
###############################################################################
#%if "%{buildpower6}"
#echo ====================TESTING -mcpu=power6=============
#cd build-%{target}-power6
#if [ -d ../power6emul ]; then
#    export LD_PRELOAD=`cd ../power6emul; pwd`/\$LIB/power6emul.so
#fi
#run_tests
#cd -
#%endif
#echo ====================TESTING DETAILS=================
#for i in `sed -n 's|^.*\*\*\* \[\([^]]*\.out\)\].*$|\1|p' build-*-linux*/check.log`; do
#  echo =====$i=====
#  cat $i || :
#  echo ============
#done
#echo ====================TESTING END=====================
#PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
#echo ====================PLT RELOCS LD.SO================
#readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
#echo ====================PLT RELOCS LIBC.SO==============
#readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
#echo ====================PLT RELOCS END==================
#
#%if "0%{?run_valgrind_tests}"
## Finally, check if valgrind runs with the new glibc.
## We want to fail building if valgrind is not able to run with this glibc so
## that we can then coordinate with valgrind to get it fixed before we update
## glibc.
#cd build-%{target}
#elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/valgrind \
#	elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/true
#cd -
#%endif
#
#%endif # %{run_glibc_tests}


#%pre -p <lua>
#-- Check that the running kernel is new enough
#required = '%{enablekernel}'
#rel = posix.uname("%r")
#if rpm.vercmp(rel, required) < 0 then
#  error("FATAL: kernel too old", 0)
#end

#%post -p %{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

#%postun -p /sbin/ldconfig

#%triggerin common -p <lua> -- glibc
#if posix.stat("%{_prefix}/lib/locale/locale-archive.tmpl", "size") > 0 then
#  pid = posix.fork()
#  if pid == 0 then
#    posix.exec("%{_prefix}/sbin/build-locale-archive")
#  elseif pid > 0 then
#    posix.wait(pid)
#  end
#end
#
#%post common -p <lua>
#if posix.access("/etc/ld.so.cache") then
#  if posix.stat("%{_prefix}/lib/locale/locale-archive.tmpl", "size") > 0 then
#    pid = posix.fork()
#    if pid == 0 then
#      posix.exec("%{_prefix}/sbin/build-locale-archive")
#    elseif pid > 0 then
#      posix.wait(pid)
#    end
#  end
#end

%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :

%pre headers
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi

#%post utils -p /sbin/ldconfig
#
#%postun utils -p /sbin/ldconfig

#%pre -n nscd
#getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
#getent passwd nscd >/dev/null ||
#  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
#		    -c "NSCD Daemon" -u 28 -g nscd nscd
#
#%post -n nscd
#%systemd_post nscd.service
#
#%preun -n nscd
#%systemd_preun nscd.service
#
#%postun -n nscd
#if test $1 = 0; then
#  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
#fi
#%systemd_postun_with_restart nscd.service

#%if "%{xenpackage}"
#%post xen -p /sbin/ldconfig
#%postun xen -p /sbin/ldconfig
#%endif

%clean
rm -rf "$RPM_BUILD_ROOT"
rm -f *.filelist*

%files -f rpm.filelist
%defattr(-,root,root)
%if "%{buildpower6}"
#%dir /%{_lib}/power6
#%dir /%{_lib}/power6x
%endif
%ifarch s390x
/lib/ld64.so.1
%endif
%ifarch armv7hl armv7hnl
/lib/ld-linux.so.3
%endif
#%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
#%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
#%verify(not md5 size mtime) %config(noreplace) /etc/rpc
#%dir /etc/ld.so.conf.d
#%dir %{_prefix}/libexec/getconf
#%dir %{_libdir}/gconv
#%dir %attr(0700,root,root) /var/cache/ldconfig
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
#%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
#%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
#%doc README NEWS INSTALL BUGS PROJECTS CONFORMANCE elf/rtld-debugger-interface.txt
%{!?_licensedir:%global license %%doc}
#%license COPYING COPYING.LIB LICENSES localedata/unicode-gen/unicode-license.txt
#%doc hesiod/README.hesiod

%if "%{xenpackage}"
#%files -f nosegneg.filelist xen
#%defattr(-,root,root)
#%dir /%{_lib}/%{nosegneg_subdir_base}
#%dir /%{_lib}/%{nosegneg_subdir}
%endif

%ifnarch %{auxarches}
#%files -f common.filelist common
#%defattr(-,root,root)
#%dir %{_prefix}/lib/locale
#%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/lib/locale/locale-archive.tmpl
#%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive
#%dir %attr(755,root,root) /etc/default
#%verify(not md5 size mtime) %config(noreplace) /etc/default/nss
#%doc documentation/*

%files -f devel.filelist devel
%defattr(-,root,root)

%files -f static.filelist static
%defattr(-,root,root)

%files -f headers.filelist headers
%defattr(-,root,root)

#%files -f utils.filelist utils
#%defattr(-,root,root)

#%files -f nscd.filelist -n nscd
#%defattr(-,root,root)
#%config(noreplace) /etc/nscd.conf
#%dir %attr(0755,root,root) /var/run/nscd
#%dir %attr(0755,root,root) /var/db/nscd
#/lib/systemd/system/nscd.service
#/lib/systemd/system/nscd.socket
#%{_tmpfilesdir}/nscd.conf
#%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
#%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
#%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
#%ghost %config(missingok,noreplace) /etc/sysconfig/nscd
%endif

#%if "0%{?_enable_debug_packages}"
#%files debuginfo -f debuginfo.filelist
#%defattr(-,root,root)
#%ifarch %{debuginfocommonarches}
#%ifnarch %{auxarches}
#%files debuginfo-common -f debuginfocommon.filelist
#%defattr(-,root,root)
#%endif
#%endif
#%endif

%changelog
* Mon Feb 23 2015 Alexandre Oliva <aoliva@redhat.com> - 2.21-5
- Update __STDC_ISO_10646__ following Unicode 7.0.0 update.

* Mon Feb 23 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.21-4
- Unicode 7.0.0 update (#1191059).
- Add back x86 vDSO support.
- Fix rtkaio build to reference clock_* functions from libc.
- Fix missing clock_* IFUNCs in librtkaio.

* Tue Feb 17 2015 Carlos O'Donell <carlos@redhat.com> - 2.21-3
- Change patch file to avoid rpm bug 1193603 and rebuild with new NVR
  (#1190454).

* Tue Feb 17 2015 Carlos O'Donell <carlos@redhat.com> - 2.21-2
- Rebuild with new NVR.

* Wed Feb 11 2015 Carlos O'Donell <carlos@redhat.com> - 2.21-1
- Fix __memcpy_chk on non-SSE2 CPUs (Upstream BZ #17949)
- Rebase to upstream release 2.21 to provide ABI and API assurances.

* Wed Jan 21 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-20
- Sync with upstream master.
- Disable werror on s390x.
- Revert x86 vDSO support since it breaks i686 rtkaio build.

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.20.90-19
- Drop large ancient ChangeLogs (rhbz #1169546)

* Mon Jan 12 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-18
- Pass address of main_arena.mutex to mutex_lock/unlock.

* Thu Jan 08 2015 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-17
- Define a __tls_get_addr macro to avoid a conflicting declaration.

* Wed Jan 07 2015 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 2.20.90-16
- Disable -Werror for s390 as well.

* Wed Jan 07 2015 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 2.20.90-14
- Sync with upstream master.
- Disable -Werror on powerpc and armv7hl.
- Temporarily disable valgrind test on ppc64.

* Sun Dec 28 2014 Dan Horák <dan[at]danny.cz>
- valgrind available only on selected arches (missing on s390)

* Wed Dec 10 2014 Kyle McMartin <kmcmarti@redhat.com>
- aarch64: Drop strchrnul.S revert, apply fix from Richard Earnshaw.

* Fri Dec 05 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-13
- Fix permission of debuginfo source files to allow multiarch
  debuginfo packages to be installed and upgraded.

* Fri Dec 05 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-12
- Remove LIB_LANG since we don't install locales in /usr/lib/locale anymore.
- Don't own any directories in /usr/share/locale (#1167445).
- Use the %%find_lang macro to get the *.mo files (#1167445).
- Add %%lang tags to language locale files in /usr/share/i18n/locale (#1169044).

* Wed Dec 03 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.20.90-11
- aarch64: revert optimized strchrnul.S implementation (rhbz#1167501)
  until it can be debugged.

* Fri Nov 28 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-10
- Auto-sync with upstream master.

* Wed Nov 19 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-9
- Sync with upstream master.

* Wed Nov 05 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-8
- Make getconf return only /usr/bin (#1138835).
- Sync with upstream master.

* Tue Nov 04 2014 Arjun Shankar <arjun.is@lostca.se> - 2.20.90-7
- Add patch that modifies several tests to use test-skeleton.c.
  The patch is accepted but not yet committed upstream.
  https://sourceware.org/ml/libc-alpha/2014-10/msg00744.html

* Tue Sep 30 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-6
- Sync with upstream master.
- Disable more Intel TSX usage in rwlocks (#1146967).
- Enable lock elision again on s390 and s390x.
- Enable Systemtap SDT probes for all architectures (#985109).

* Fri Sep 26 2014 Carlos O'Donell <carlos@redhat.com> - 2.20.90-5
- Disable lock elision support for Intel hardware until microcode
  updates can be done in early bootup (#1146967).
- Fix building test tst-strtod-round for ARM.

* Tue Sep 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-4
- Sync with upstream master.
- Don't own the common debuginfo directories (#1144853).
- Run valgrind in the %%check section to ensure that it does not break.

* Tue Sep 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-3
- Sync with upstream master.
- Revert patch for #737223.

* Mon Sep 08 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-2
- Build build-locale-archive statically again.

* Mon Sep 08 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.20.90-1
- Sync with upstream master.

* Thu Sep  4 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-36
- Allow up to 32 dlopened modules to use static TLS (#1124987).
- Run glibc tests in %%check section of RPM spec file.
- Do not run tests with `-k` and fail if any test fails to build.

* Tue Aug 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-35
- Sync with upstream master.
- Use INTERNAL_SYSCALL in TLS_INIT_TP (#1133134).
- Remove gconv loadable module transliteration support (CVE-2014-5119, #1119128).

* Fri Aug 22 2014 Dennis Gilmore <dennis@ausil.us> - 2.19.90-34
- add back sss to nsswitch.conf we have added workarounds in the tools

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 2.19.90-33.1
- Rebuild for rpm bug 1131960

* Tue Aug 19 2014 Dennis Gilmore <dennis@ausil.us> - 2.19.90-33
- remove sss from default nsswitch.conf it causes issues with live image composing

* Wed Aug 13 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-32
- Auto-sync with upstream master.
- Revert to only defining __extern_always_inline for g++-4.3+.
- Fix build failure in compat-gcc-32 (#186410).

* Mon Jul 28 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-31
- Auto-sync with upstream master.

* Wed Jul 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-30
- Undo last master sync to fix up rawhide.

* Tue Jul 15 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-29
- Auto-sync with upstream master.

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.19.90-28
- fix license handling

* Mon Jul 07 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-27
- Auto-sync with upstream master.

* Fri Jul 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-26
- Sync with upstream roland/nptl branch.
- Improve testsuite failure outputs in build.log

* Thu Jul 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-25
- Sync with upstream roland/nptl branch.

* Wed Jul 02 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-24
- Sync with upstream master.

* Tue Jun 24 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-23
- Sync with upstream master.
- Add fix to unbreak i386 ABI breakage due to a change in scalbn.

* Fri Jun 20 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.19.90-22
- AArch64: Save & restore NZCV (flags) upon entry to _dl_tlsdesc_dynamic
  in order to work around GCC reordering compares across the TLS
  descriptor sequence (GCC PR61545.) Committing a (temporary) fix here
  allows us to avoid rebuilding the world with gcc 4.9.0-11.fc21.

* Mon Jun 16 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.19.90-21
- Auto-sync with upstream master.

* Thu Jun 12 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-20
- Auto-sync with upstream master.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.90-19.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-19
- Sync with upstream master.

* Mon May 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-18
- Sync with upstream master.
- Adjust rtkaio patches to build with upstream master.

* Wed May 21 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.19.90-17
- Backport some upstream-wards patches to fix TLS issues on AArch64.

* Wed May 21 2014 Kyle McMartin <kyle@fedoraproject.org> - 2.19.90-16
- AArch64: Fix handling of nocancel syscall failures (#1098327)

* Thu May 15 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-15
- Sync with upstream master.

* Wed May 14 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-14
- Add support for displaying all test results in build logs.

* Wed May 14 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-13
- Add initial support for ppc64le.

* Tue Apr 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-12
- Auto-sync with upstream master.
- Remove ports addon.

* Fri Apr 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-11
- Sync with upstream master.

* Thu Apr 10 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-10
- Sync with upstream master.

* Thu Apr 03 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-9
- Sync with upstream master.

* Wed Mar 26 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-8
- Sync with upstream master.

* Wed Mar 19 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-7
- Sync with upstream master.
- Fix offset computation for append+ mode on switching from read (#1078355).

* Wed Mar 12 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-6
- Sync with upstream master.
- Use cleaner upstream solution for -ftree-loop-distribute-patterns (#911307).

* Tue Mar 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-5
- Sync with upstream master.

* Thu Feb 27 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-4
- Use nscd service files from glibc sources.
- Make nscd service forking in systemd service file.

* Tue Feb 25 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-3
- Sync with upstream master.
- Separate ftell from fseek logic and avoid modifying FILE data (#1069559).

* Mon Feb 24 2014 Carlos O'Donell <carlos@redhat.com> - 2.19.90-2
- Fix build-locale-archive failure to open default template.

* Tue Feb 18 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.19.90-1
- Sync with upstream master.

* Tue Feb 04 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-27
- Sync with upstream master.

* Wed Jan 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-26
- Modify regular expressions to include powerpcle stubs-*.h (#1058258).

* Wed Jan 29 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-25
- Sync with upstream master.

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.18.90-24
- Own the %%{_prefix}/lib/locale dir.

* Thu Jan 23 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-23
- Sync with upstream master.

* Thu Jan 16 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-22
- Back out ftell test case (#1052846).

* Tue Jan 14 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-21
- Sync with upstream master.
- Fix infinite loop in ftell when writing wide char data (#1052846).

* Tue Jan  7 2014 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.18.90-20
- Sync with upstream master.
- Enable systemtap probes on Power and S/390.
