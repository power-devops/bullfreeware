# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, all targets (compiler, ppc, ppc64, pthread) are tested
# To test only compiler: rpmbuild -ba --without longtests *.spec
%bcond_without longtests

# By default on aix 7.1 and 7.2, gccgo is built.
# No gccgo: rpmbuild -ba --without build_go *.spec
%ifos aix7.1 aix7.2
%bcond_without build_go
%endif

# By default, objectif-C isn't made.
# To build objectif-c: rpmbuild -ba --with objc *.spec
%bcond_with build_objc

# Create macros for AIX version requirements
%ifos aix6.1
%global buildhost powerpc-ibm-aix6.1.0.0
%global AIX_requirements \
Requires: AIX-rpm >= 6.1.0.0 \
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
%global buildhost powerpc-ibm-aix7.1.0.0
%global AIX_requirements \
Requires: AIX-rpm >= 7.1.0.0 \
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
%global buildhost powerpc-ibm-aix7.2.0.0
%global AIX_requirements \
Requires: AIX-rpm >= 7.2.0.0 \
Requires: AIX-rpm <  7.3.0.0
%endif

%define _libdir64 %{_prefix}/lib64

%global do_clean_build 1

# By default, binaries and libraries are built on %default_arch bits.
%define default_arch 32

%define gcc_version 9.3.0
%define gcc_major 9

%define base_name gcc

# The build is made in another folder under BUILD
%define build_dir /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version}

Summary: GNU Compiler Collection
Name:    %{base_name}%{gcc_major}
Version: %{gcc_version}
Release: 7
Group:   Development/Tools
License: GPL
URL:     http://gcc.gnu.org/

Source0: ftp://ftp.gnu.org/gnu/%{base_name}/%{base_name}-%{version}/%{base_name}-%{gcc_version}.tar.xz
# Used for snapshots:
#Source0: ftp://ftp.gnu.org/gnu/%{base_name}/%{base_name}-%{version}/%{base_name}-%{gcc_version}-%{release}.tar.xz

Source100: %{name}-%{version}-%{release}.build.log
Source101: %{name}-%{version}-%{release}.testslogs.tar.gz

# Older .so files for gfortran
# Only add 6.1 versions for now. They should be compatible across versions.
Source200: libgfortran.so.3_61_aix32
Source201: libgfortran.so.3_61_aix64
Source202: libgfortran.so.3_61_pthread_aix32
Source203: libgfortran.so.3_61_pthread_aix64

# GCC PATCHES

# Ready to submit ? I think so. However, useful ??
# David : The reversion of config to oslevel is not acceptable.
#         Please remove that patch completely and find another solution if that truly is necessary.
# Study this !!
Patch1:   gcc-9.3.0-oslevel.patch

# ADDITIONAL_LANGUAGES=",go" on AIX !!
# To be submitted as the last patch, so that go is compiled within AIX
Patch2:  gcc-9.1.0-contrib-config-list-add-go-for-aix.patch

Patch3:  gcc-9.3.0-gotools-fix-Makefile-v3.patch
Patch4:  gcc-9.1.0-gotools-64bits-commands.patch

# Crashes the link of gotools if no GCC-Go (libgo.a) installed on machine...
# VERY TOUCHY !!! RE-ANALYZE IT !!!
# v7: Version without -brtllib
# Important !!!!!!!!!
# Patch3: gcc-8.1.0-lgo-brtllib-v7.patch

# Fix long names for gcbits symbols
# Merged
Patch5:  gcc-9.1.0-gccgo-use-SHA-1-hash-for-symname.patch

# Fix libbacktrace tests
# Merged
Patch6:  gcc-9.1.0-libbacktrace-split-elf_test-into-32-and-64-bits.patch

# Speedup libbacktrace for Go tracebacks
Patch7:  gcc-9.1.0-libbacktrace-speed-up-XCOFF.patch
# Use /proc/pid/object/a.out before /proc/self/exe
# Fix panic failures.
# Don't submit
Patch8:  gcc-9.1.0-libbacktrace-open-with-pid-first.patch

# Fix linking with shared libraries
Patch9:   gcc-8.4.0-configure-fix-shrext-for-AIX.patch
Patch10:  gcc-8.4.0-configure-fix-disable-rpath-for-AIX.patch

# Add /opt/freeware/lib in default LIBPATH
# TODO: pthread and ppc64 also ?
Patch11:  gcc-8.3.0-gcc-config-force-opt-freeware-lib-in-AIX-LIBPATH.patch

# Fix long double builtins
Patch12:  gcc-8.4.0-gcc-config-rs6000-fix-long-double-builtins-for-AIX-V2.patch

# Link with libc128.a when -mlong-double-128 is provided
Patch13:  gcc-8.4.0-gcc-config-rs6000-add-link-with-libc128-with-mlong-d.patch

# Use the correct behavior for -mcmodel=large
Patch14:  gcc-8.4.0-Correct-logic-to-disable-NO_SUM_IN_TOC-and-NO.patch

# Workaround for a TLS bug dealing with TOC values being precomputed
Patch15:  gcc-8.4.0-gcc-WORKAROUND-TLS-TOC-constants.patch

# Set correct AR for libcpp and lib
Patch16:  gcc-8.4.0-libcpp-libdecnumber-configure-and-substitute-AR.patch

# Fix collect2 when -fvisibility=hidden is given
Patch17: gcc-8.4.0-aix-collect2-visibility.patch

# Fix fixincludes for "sys/socket.h" after AIX7.2 TL4
Patch18: gcc-8.4.0-aix-apply-socket.h-extern-C-more-narrowly.patch

# Fix fixincludes for "malloc.h" after AIX7.2 TL4
Patch19: gcc-8.4.0-aix-apply-aix_malloc-more-narrowly.patch

# Always enable STDC format macros in GCC "sys/inttypes.h"
Patch20: gcc-9.3.0-aix-Fix-_STDC_FORMAT_MACROS-in-inttypes.h.patch

# Add libstdc++ locale support
Patch21: gcc-9.3.0-libstdc-implement-locale-support-for-XPG7.patch

# Fix 64bit inodes with stat
Patch22: gcc-9.3.0-aix-handle-64bit-inodes-for-include-directories.patch

# Fix collect2 with archvies containing text files
Patch23: gcc-8.5.0-aix-collect2-text-files-in-archive.patch

# LIBGO PATCHES

# Remove -fno-section-anchors: No longer needed
# TO SUBMIT
Patch100:   gcc-9.1.0-libgo-configure-remove-fno-section-anchors-on-AIX.patch

# configure OBJCOPY: Patch to submit ??
Patch101:   gcc-9.1.0-libgo-configure-use-copycsect-instead-of-objcopy.patch

# Enable gotest for AIX. Must be improved.
# Add flags -Wl,-bbigtoc, -Wl,-bernotok, -static-libgo
# Unset LD_LIBRARY_PATH for ppc64
Patch102:   gcc-9.1.0-libgo-testsuite-fix-gotest-for-AIX.patch

# Fix duplications of libgo tests
Patch103:   gcc-9.1.0-libgo-testsuite-only-retrieve-T-symbols-on-AIX.patch

# Fix libgo tests.
Patch105:   gcc-9.1.0-libgo-syscall-fix-TestForeground-for-AIX.patch
Patch106:   gcc-9.1.0-libgo-syscall-remove-ptrace-syscall-on-ppc64.patch
Patch107:   gcc-9.1.0-libgo-testsuite-add-mcmodel-large-for-net-http-tests.patch
Patch108:   gcc-9.1.0-libgo-runtime-fix-TestPhysPageSize-on-AIX.patch

# Equivalent of go test -vet=off
# Do not merged
Patch109:   gcc-9.1.0-libgo-cmd-go-disable-vet-in-tests.patch

# Remove "ar: 0707-101 D is not a valid flag." error
Patch110:   gcc-9.1.0-libgo-cmd-go-silence-ar-with-D-flags.patch


BuildRequires: bash, sed, make, tar, gcc >= 6
# Version 6.7-1 has a bug with makeinfo_32
BuildRequires: texinfo >= 6.7-2
# 8.31-1 adds _32/_64 binaries
BuildRequires: coreutils >= 8.31-1
# 5.0.1-1 adds _32/_64 binaries
BuildRequires: gawk >= 5.0.1-1

# autoconf and automake aren't needed as long as the patches
# are correctly made. ie if configure.ac needs to be modified, configure
# should also be modified in the patch.
# However, always keep this line to know which versions need to be used
# when creating patches.
# BuildRequires: automake = 1.15.1, autoconf = 2.69, m4 = 1.4.17

# Not sure this version 8.5 of tcl is really required...
#BuildRequires: tcl >= 8.5, tcl < 8.6
BuildRequires: tcl >= 8.5
BuildRequires: gmp-devel >= 6.2.1, mpfr-devel >= 4.1.0, libmpc-devel >= 1.2.1

# GCC is now compiled with a GCC zlib. Thus, the minimal version is 1.2.11-2
BuildRequires: zlib-devel >= 1.2.11-2

%if %{with build_go}
# objcopy must be replaced by copycsect
#BuildRequires: binutils, binutils-gccgov1
BuildRequires: binutils-gccgov1
%endif
# For: runtest
BuildRequires: dejagnu
%if %{with dotests}
BuildRequires: autogen, autogen-libopts
%endif

Requires: info
Requires: /sbin/install-info
Requires: libgcc%{gcc_major} = %{version}-%{release}
Requires: gcc%{gcc_major}-cpp = %{version}-%{release}

Conflicts: g++ <= 2.9.aix51.020209-4

# As gcc is configure with /opt/freeware/bin/sed, fixinc.sh in %post
# will try to call it.
Requires(post): sed

# Conflicts gcc without multi-gcc support
Conflicts: gcc <= 9.1.0
%{AIX_requirements}

%define gcclibdir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%define gcclibexecdir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}


%description
The gcc package contains the GNU Compiler Collection version %{gcc_version}.
You will need this package in order to compile C code.


%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libstdc++%{gcc_major}-devel = %{version}-%{release}
Requires: zlib >= 1.2.11-2
Obsoletes: g++
%{AIX_requirements}

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.


%package cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gmp >= 6.2.1, mpfr >= 4.1.0, libmpc >= 1.2.1
Requires: zlib >= 1.2.11-2
%{AIX_requirements}

%description cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.


%package -n libgcc%{gcc_major}
Summary: GCC version %{gcc_version} shared support library
Group: Development/Libraries
%{AIX_requirements}

# Conflicts libgcc without multi-gcc support
Conflicts: libgcc <= 9.1.0

%description -n libgcc%{gcc_major}
This package contains GCC shared support library which is needed
e.g. for exception handling support.


%package -n libstdc++%{gcc_major}
Summary: GNU Standard C++ Library
Group: Development/Libraries
Requires: libgcc%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description -n libstdc++%{gcc_major}
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.
Support for std::locale is still in beta version.


%package -n libstdc++%{gcc_major}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description -n libstdc++%{gcc_major}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes a rewritten implementation of STL.


%package gfortran
Summary: Fortran 95 support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libgfortran%{gcc_major} = %{version}-%{release}
Requires: zlib >= 1.2.11-2
%{AIX_requirements}

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran%{gcc_major}
Summary: Fortran runtime
Group: Development/Languages
Requires: libgcc%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description -n libgfortran%{gcc_major}
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp%{gcc_major}
Summary: GCC OpenMP 2.5 shared support library
Group: Development/Languages
Requires: libgcc%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description -n libgomp%{gcc_major}
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.

%if %{with build_objc}

# TODO: port not yet done

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libobjc%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description objc
%{name}-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: %{name}-c++  = %{version}-%{release}
Requires: %{name}-objc = %{version}-%{release}
Autoreq: true
%{AIX_requirements}

%description objc++
%{name}-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc%{gcc_major}
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true
%{AIX_requirements}

%description -n libobjc%{gcc_major}
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%endif

%if %{with build_go}

%package go
Summary: Go support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libgo%{gcc_major} = %{version}-%{release}
Requires: libgo%{gcc_major}-devel = %{version}-%{release}
%{AIX_requirements}

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

This is GCC Go for AIX. With Go version 1.12.
GCC Go on AIX appears in 4 flavors: 32bit, pthread, ppc64, pthread/ppc64.

Summary of remaining tests failures for 32bit:
# ParseLibgo.sh $SPECS/gcc-8

Your objects (.o), shared-objects (.so), and archives (.a) built from .go code
should be rebuilt when a new stable version of GCC Go is available.
I mean to say that you will probably not be able to mix .o, .so or .a files
compiled with different versions of GCC Go for AIX.

Full cgo feature of Go works only on AIX 7.2 since it is the first AIX version providing
sufficient DWARF support in XCOFF (and probably too on some recent TLs of AIX 7.1).

go command is 64bit by default.
In order to create go programs in 32bit, do:
	GOARCH=ppc go
or (for big & complex application):
	GOARCH=ppc64 CGO_ENABLED=1 go build -gccgoflags='-Wl,-bbigtoc'

Feel free to contact us whenever you are facing issues.
Tony Reix tony.reix@atos.net
Clement Chigot clement.chigot@atos.net


%package -n libgo%{gcc_major}
Summary: Go runtime
Group: System Environment/Libraries
Requires: libgcc%{gcc_major} = %{version}-%{release}
%{AIX_requirements}

%description -n libgo%{gcc_major}
Objects (.o), shared-objects (.so), and archives (.a) built from .go code
should be rebuilt when a new version of GCC Go is available.

This package contains a Go shared library which is needed to run
Go dynamically linked programs.


%package -n libgo%{gcc_major}-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo%{gcc_major} = %{version}-%{release}

%description -n libgo%{gcc_major}-devel
This package includes libraries and support files for compiling Go programs.

%endif


%prep
export PATH=/opt/freeware/bin:$PATH

# Ensure that all the locales needed for libstdc++ tests
# are available.
%if %{with dotests}
locales=`locale -a`
minimal_local="
de_DE.8859-15
de_DE.UTF-8
en_HK.8859-15
en_US.ISO8859-1
en_US.UTF-8
es_ES.8859-15
fr_FR.8859-15
is_IS.ISO8859-1"
for loc in $minimal_local; do
    echo "checking $loc"
    if ! echo $locales | grep -q $loc; then
	echo "Missing locales for tests: $loc"
	echo "Please check at least these locales are installed: $minimal_local"
	exit 1
    fi
done
%endif

%if !%{do_clean_build}
echo "Skipping %prep"
exit 0
%endif

%setup -q -n gcc-%{gcc_version}
%patch1 -p1
%ifos aix7.1 aix7.2
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1

# Always make sure testlogs are present.
touch %{SOURCE101}

# cd libgo
# autoconf --version
# autoreconf

%build
echo "Build start time:"
date

echo "GCC version:"
gcc --version

export PATH=/usr/bin:/usr/sbin:/sbin:/opt/freeware/bin

# GCC is setting LD_LIBRARY_PATH when calling "make". This new libpath
# will find the newly created libgcc_s before the /opt/freeware/lib one.
# However, this new libgcc_s doesn't have both 32 and 64 bit shared objects but
# only the %default_arch version.
# Setting LIBPATH seems to fix it without impacted the binaries and libraries
# built.
export LIBPATH=/opt/freeware/lib:/usr/lib:/lib

# speed up the configure processes...
export CONFIG_SHELL=/opt/freeware/bin/bash_%{default_arch}
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash_%{default_arch}


# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
# export SED="/opt/freeware/bin/sed_%{default_arch}"
export SED="/opt/freeware/bin/sed"
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar "
export M4="/opt/freeware/bin/m4"

%if %{default_arch} == 32
# use maximum amount of memory (heap) available to 32-bit programs
# seems not to be taken into account though
export LDR_CNTRL=MAXDATA=0x80000000
%endif

%if %{do_clean_build}
cd ..
if [ -d %{build_dir} ]; then
	rm -rf %{build_dir}
fi
mkdir %{build_dir}
cd %{build_dir}

/opt/freeware/bin/gcc --version

LANGUAGES="c,c++,fortran"
%if %{with build_go}
LANGUAGES="${LANGUAGES},go"
%endif
%if %{with build_objc}
LANGUAGES="${LANGUAGES},objc,obj-c++"
%endif

echo "Start of configure/build"
date

echo "GCC will be built with support for following languages: ${LANGUAGES}"

CC=/opt/freeware/bin/gcc					\
CXX=/opt/freeware/bin/g++					\
../%{base_name}-%{gcc_version}/configure 			\
	--prefix=%{_prefix}					\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
	--with-local-prefix=/opt/freeware			\
	--with-as=/usr/bin/as					\
	--with-ld=/usr/bin/ld					\
	--enable-languages="${LANGUAGES}"			\
	--enable-version-specific-runtime-libs			\
	--disable-nls 						\
	--disable-libstdcxx-pch					\
	--disable-werror					\
	--enable-libstdcxx-filesystem-ts			\
	--with-gcc-major-version-only				\
	--program-suffix=-%{gcc_major}				\
	--disable-rpath						\
	--host=%{buildhost}

%else # do_clean_build = 0
cd %{build_dir}
%endif # do_clean_build


export CC=/opt/freeware/bin/gcc
export CXX=/opt/freeware/bin/g++

ulimit -a
ulimit -d unlimited
ulimit -s unlimited
ulimit -m unlimited
ulimit -a


# configure/build takes about 100mn on AIX 7.2 with 4 CPU x 4 execution threads

export OPT_FLAG="-O2 -D_LARGE_FILES"

export	BOOT_CFLAGS="${OPT_FLAG}"
export	  LT_CFLAGS="${OPT_FLAG}"
export	     CFLAGS="${OPT_FLAG}"
export	   CXXFLAGS="${OPT_FLAG}"
export	  LIBCFLAGS="${OPT_FLAG}"
export	LIBCXXFLAGS="${OPT_FLAG} -fno-implicit-templates"

echo "BUILD ENVIRONMENT:"
/usr/bin/env | /usr/bin/sort

%if %{with build_go}
# Add a link to simulate that libgo.a is installed.
# This is needed because of patch "gcc-8.3.0-lgo-brtllib-v8.patch" for gotools.
if [ ! -f %{gcclibdir}/libgo.a ]; then
	mkdir -p %{_libdir}/gcc/%{buildhost}/%{gcc_major}
    ln -sf ${BUILD}/gcc-build-%{gcc_version}/%{buildhost}/libgo/.libs/libgo.a %{gcclibdir}/libgo.a
fi
%endif

#gmake --trace -d -j 8
gmake -j8

echo "Build end time : "
date


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar "


cd %{build_dir}
gmake install DESTDIR=${RPM_BUILD_ROOT}

# strip compiler binaries
strip ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :
for file in cc1 cc1plus collect2 f951 lto-wrapper ; do
    strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/$file 2>/dev/null || :
done

# strip utilities
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/fixincl 2>/dev/null || :
strip ${RPM_BUILD_ROOT}%{gcclibdir}/install-tools/fixincl 2>/dev/null || :

# remove unrelated man pages
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man7

# remove libiberty.a library which is not used directly by gcc
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty.a

# Do not remove ppc64 & pthread directories since they contain useful stuff for Go
#for dir in power powerpc ppc64 pthread ; do
for dir in power powerpc ; do
    rm -rf ${RPM_BUILD_ROOT}%{_libdir}/$dir
done

# remove empty include directory
rmdir ${RPM_BUILD_ROOT}%{_includedir} || :

# rename with gcc version and gzip info pages
(
	cd ${RPM_BUILD_ROOT}%{_infodir}
	for f in `find . -name "*.info"`; do
		mv $f ${f%.*}-%{gcc_major}.${f##*.}
	done
	gzip --best *.info
)

# patch 32-bit binaries to use the maximum number of 8 x 256MB data segments
# as the "export LDR_CNTRL=MAXDATA=0x80000000" setting seems not to be taken
# into account though
cd ${RPM_BUILD_ROOT}%{_bindir}
for f in `ls -1 | grep -v "^go*"` ; do
    if [[ "`/usr/bin/file ${f} | awk '{ print $2 }'`" = "executable" ]] ; then
        /usr/bin/echo '\0200\0\0\0' | /usr/bin/dd of=${f} bs=4 count=1 seek=19 conv=notrunc
    fi
done
cd -

# Change name of Go binaries to allow both golang and gccgo on the same machine
%if %{with build_go}
   cd ${RPM_BUILD_ROOT}/%{_bindir}
   mv go-%{gcc_major} go.gcc-%{gcc_major}
   mv gofmt-%{gcc_major} gofmt.gcc-%{gcc_major}
%endif

# Create link between the full version and the major version.
# This isn't needed but explains which full version is currently used.
(
	cd ${RPM_BUILD_ROOT}/%{_libdir}/gcc/%{buildhost}
	ln -sf %{gcc_major} %{gcc_version}
)

# strip debugging information of all libraries as the settings specified
# while bootstrapping do not seem to be taken into account
# Note 1: this does NOT strip the lib*.so files contained by the lib*.a files !!
(
    cd ${RPM_BUILD_ROOT}

    for f in `find . -name "*.a"` ; do
        if [ -f ${f} ] ; then
            /usr/bin/strip -X32_64 ${f}
        fi
    done
)

# Add the older gfortran .so library to new archive.
# Make sure they are set for "LOADONLY" with strip -e
cp %{SOURCE200} libgfortran.so.3
/usr/bin/strip -X32 -e libgfortran.so.3
$AR    -X32 -q ${RPM_BUILD_ROOT}%{gcclibdir}/libgfortran.a libgfortran.so.3
cp %{SOURCE201} libgfortran.so.3
/usr/bin/strip -X64 -e libgfortran.so.3
$AR    -X64 -q ${RPM_BUILD_ROOT}%{gcclibdir}/libgfortran.a libgfortran.so.3
cp %{SOURCE202} libgfortran.so.3
/usr/bin/strip -X32 -e libgfortran.so.3
$AR    -X32 -q ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/libgfortran.a libgfortran.so.3
cp %{SOURCE203} libgfortran.so.3
/usr/bin/strip -X64 -e libgfortran.so.3
$AR    -X64 -q ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/libgfortran.a libgfortran.so.3

# Add 64bit .so from 64bit libX.a to 32bit libX.a
# For X = atomic gcc_s stdc++ supc++ gomp gfortran caf_single
mkdir /tmp/gcc-$$
(
    cd    /tmp/gcc-$$

	# Static libraries don't need to have both 32 and 64bit objects.
	# Except for gccgo ones as long as the gotools are in 64bit instead of
	# the default 32 bit.
%if %{with build_go}
    for lib in atomic gcc_s stdc++ gomp gfortran go gobegin golibbegin
%else
    for lib in atomic gcc_s stdc++ gomp gfortran
%endif
    do
        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{gcclibdir}/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{gcclibdir}/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{gcclibdir}/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{gcclibdir}/ppc64
          ln -s                      %{gcclibdir}/lib$lib.a .
		)

        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/ppc64
          ln -s                      %{gcclibdir}/pthread/lib$lib.a .
        )
    done
)
rm -rf /tmp/gcc-$$


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

ulimit -a
ulimit -d unlimited
ulimit -s unlimited
ulimit -m unlimited
ulimit -a

# Set GOROOT to any value expect the default one which is "/opt/freeware".
# The reason is "/opt/freeware" has a "src" subdirectory. Thus TestDependencies
# will think every subdirectories under "src" is a go package and then raise
# a ton of errors.
export GOROOT=`pwd`

# Compiler tests + all libgo tests
# Default way for gcc to do its tests.
echo "Tests 1) Compiler + libgo tests"
date

cd %{build_dir}
(gmake -k check || true)

date

%if %{with longtests}
# Tests on others AIX target (ppc64, pthread)
echo "Tests 2) ppc64, pthread, pthread/ppc64 tests"
date

LIBS="libatomic libbacktrace libgomp libstdc++-v3 libgfortran"

cd %{buildhost}
for DIR in ppc64 pthread pthread/ppc64 ; do
    for LIB in $LIBS ; do
        echo $DIR $LIB
        cd $DIR/$LIB
        (gmake -k check || true)
        cd -
    done
done
cd ..

date
%endif

cd %{build_dir}
find . -name "*.log" | grep -v config.log | xargs /opt/freeware/bin/tar zcf  %{SOURCE101}
cd -


%post
/sbin/install-info %{_infodir}/gcc-%{gcc_major}.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccinstall-%{gcc_major}.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccint-%{gcc_major}.info.gz %{_infodir}/dir || :

# Regen include-fixed directory to avoid getting wrong headers being used.
# Export LIBPATH for sed
export LIBPATH=/opt/freeware/lib:/usr/lib:/lib
/%{gcclibexecdir}/install-tools/mkheaders

%post -n libgomp%{gcc_major}
/sbin/install-info %{_infodir}/libgomp-%{gcc_major}.info.gz %{_infodir}/dir || :

%post cpp
/sbin/install-info %{_infodir}/cpp-%{gcc_major}.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/cppinternals-%{gcc_major}.info.gz %{_infodir}/dir || :

%post gfortran
/sbin/install-info %{_infodir}/gfortran-%{gcc_major}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcc-%{gcc_major}.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccinstall-%{gcc_major}.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccint-%{gcc_major}.info.gz %{_infodir}/dir || :
fi
echo "Warnings dealing with include-fixed directory can be ignored."

%postun
# Make sure that all the headers in include-fixed are removed, as some
# may have been generated only for this machine and thus aren't listed by
# gcc RPMs.
if [ "$1" = 0 ]; then
		[[ -e %{gcclibdir}/include-fixed/ ]] && rm -r %{gcclibdir}/include-fixed/
fi

%preun -n libgomp%{gcc_major}
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libgomp-%{gcc_major}.info.gz %{_infodir}/dir || :
fi

%preun cpp
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpp-%{gcc_major}.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/cppinternals-%{gcc_major}.info.gz %{_infodir}/dir || :
fi

%preun gfortran
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gfortran-%{gcc_major}.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/gcc-%{gcc_major}
%{_bindir}/gcc-ar-%{gcc_major}
%{_bindir}/gcc-nm-%{gcc_major}
%{_bindir}/gcc-ranlib-%{gcc_major}
%{_bindir}/gcov-%{gcc_major}
%{_bindir}/gcov-tool-%{gcc_major}
%{_bindir}/gcov-dump-%{gcc_major}
%{_bindir}/%{buildhost}-gcc-%{gcc_major}
%{_bindir}/%{buildhost}-gcc-ar-%{gcc_major}
%{_bindir}/%{buildhost}-gcc-nm-%{gcc_major}
%{_bindir}/%{buildhost}-gcc-ranlib-%{gcc_major}
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/crtcxa*o
%{gcclibdir}/crtdbase.o
%{gcclibdir}/libgcc.a
%{gcclibdir}/libgcc_eh.a
%{gcclibdir}/libgcov.a
%{gcclibdir}/ppc64/crtcxa*o
%{gcclibdir}/ppc64/crtdbase.o
%{gcclibdir}/ppc64/libgcc.a
%{gcclibdir}/ppc64/libgcc_eh.a
%{gcclibdir}/ppc64/libgcov.a
%{gcclibdir}/pthread/crtcxa*o
%{gcclibdir}/pthread/crtdbase.o
%{gcclibdir}/pthread/libgcc.a
%{gcclibdir}/pthread/libgcc_eh.a
%{gcclibdir}/pthread/libgcov.a
%{gcclibdir}/pthread/ppc64/crtcxa*o
%{gcclibdir}/pthread/ppc64/crtdbase.o
%{gcclibdir}/pthread/ppc64/libgcc.a
%{gcclibdir}/pthread/ppc64/libgcc_eh.a
%{gcclibdir}/pthread/ppc64/libgcov.a

%dir %{gcclibdir}/include
%{gcclibdir}/include/[^c++]*
%{gcclibdir}/include-fixed

%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{gcclibexecdir}
%{gcclibexecdir}/collect2
%{gcclibexecdir}/lto-wrapper
%{gcclibexecdir}/install-tools

%{gcclibdir}/install-tools

%{_infodir}/gcc*

%{_mandir}/man1/gcc-%{gcc_major}.1
%{_mandir}/man1/gcov-%{gcc_major}.1
%doc gcc/COPYING* MAINTAINERS gcc/README*


%files cpp
%defattr(-,root,system)
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{gcclibexecdir}
%{_bindir}/cpp-%{gcc_major}
%{gcclibexecdir}/cc1
%{_mandir}/man1/cpp-%{gcc_major}.1
%{_infodir}/cpp*



%files c++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{_bindir}/c++-%{gcc_major}
%{_bindir}/g++-%{gcc_major}
%{_bindir}/%{buildhost}-c++-%{gcc_major}
%{_bindir}/%{buildhost}-g++-%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{gcclibexecdir}
%{gcclibexecdir}/cc1plus
%{_mandir}/man1/g++-%{gcc_major}.1


%files -n libgcc%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/libgcc_s.a
%{gcclibdir}/libatomic.a
%{gcclibdir}/ppc64/libgcc_s.a
%{gcclibdir}/ppc64/libatomic.a
%{gcclibdir}/pthread/libgcc_s.a
%{gcclibdir}/pthread/libatomic.a
%{gcclibdir}/pthread/ppc64/libgcc_s.a
%{gcclibdir}/pthread/ppc64/libatomic.a
# Full version link
%{_libdir}/gcc/%{buildhost}/%{gcc_version}
%doc gcc/COPYING*


%files -n libstdc++%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/libstdc++.a
%{gcclibdir}/ppc64/libstdc++.a
%{gcclibdir}/pthread/libstdc++.a
%{gcclibdir}/pthread/ppc64/libstdc++.a
%{gcclibdir}/libstdc++.a-gdb.py
%{gcclibdir}/ppc64/libstdc++.a-gdb.py
%{gcclibdir}/pthread/libstdc++.a-gdb.py
%{gcclibdir}/pthread/ppc64/libstdc++.a-gdb.py
%dir %{_datadir}/gcc-%{gcc_major}
%dir %{_datadir}/gcc-%{gcc_major}/python
%{_datadir}/gcc-%{gcc_major}/python/libstdcxx


%files -n libstdc++%{gcc_major}-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/libsupc++.a
%{gcclibdir}/ppc64/libsupc++.a
%{gcclibdir}/pthread/libsupc++.a
%{gcclibdir}/pthread/ppc64/libsupc++.a
%{gcclibdir}/libstdc++fs.a
%{gcclibdir}/ppc64/libstdc++fs.a
%{gcclibdir}/pthread/libstdc++fs.a
%{gcclibdir}/pthread/ppc64/libstdc++fs.a
%{gcclibdir}/include/c++


%files -n libgomp%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/libgomp.a
%{gcclibdir}/libgomp.spec
%{gcclibdir}/ppc64/libgomp.a
%{gcclibdir}/ppc64/libgomp.spec
%{gcclibdir}/pthread/libgomp.a
%{gcclibdir}/pthread/libgomp.spec
%{gcclibdir}/pthread/ppc64/libgomp.a
%{gcclibdir}/pthread/ppc64/libgomp.spec
%{_infodir}/libgomp*


%files gfortran
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{_bindir}/gfortran-%{gcc_major}
%{_bindir}/%{buildhost}-gfortran-%{gcc_major}
%{gcclibdir}/finclude
%{gcclibdir}/libgfortran.spec
%{gcclibdir}/libcaf_single.a
%{gcclibdir}/ppc64/libgfortran.spec
%{gcclibdir}/ppc64/libcaf_single.a
%{gcclibdir}/pthread/libgfortran.spec
%{gcclibdir}/pthread/libcaf_single.a
%{gcclibdir}/pthread/ppc64/libgfortran.spec
%{gcclibdir}/pthread/ppc64/libcaf_single.a
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{gcclibexecdir}
%{gcclibexecdir}/f951
%{_infodir}/gfortran-%{gcc_major}.info.gz
%{_mandir}/man1/gfortran-%{gcc_major}.1

%files -n libgfortran%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{gcclibdir}/ppc64
%dir %{gcclibdir}/pthread
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/libgfortran.a
%{gcclibdir}/ppc64/libgfortran.a
%{gcclibdir}/pthread/libgfortran.a
%{gcclibdir}/pthread/ppc64/libgfortran.a

%if %{with build_objc}
%files objc
%defattr(-,root,system)
%{gcclibdir}/include/objc
%{gcclibdir}/include/objc/objc-decls.h
%{gcclibdir}/include/objc/objc-exception.h
%{gcclibdir}/include/objc/objc-sync.h
%{gcclibdir}/include/objc/objc.h
%{gcclibdir}/libobjc.a
%{gcclibdir}/ppc64/libobjc.a
%{gcclibdir}/pthread/libobjc.a
%{gcclibdir}/pthread/ppc64/libobjc.a

%endif

%if %{with build_go}

%files go
%defattr(-,root,system)
%{_bindir}/go.gcc-%{gcc_major}
%{_bindir}/gccgo-%{gcc_major}
%{_bindir}/gofmt.gcc-%{gcc_major}
%{_mandir}/man1/gccgo-%{gcc_major}.1
%{_mandir}/man1/go-%{gcc_major}.1
%{_mandir}/man1/gofmt-%{gcc_major}.1
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{gcclibexecdir}
%{gcclibexecdir}/go1
%{gcclibexecdir}/cgo
%{gcclibexecdir}/buildid
%{gcclibexecdir}/test2json
%{gcclibexecdir}/vet

%files -n libgo%{gcc_major}
%defattr(-,root,system)
%{gcclibdir}/libgo.a
%{gcclibdir}/pthread/libgo.a
%{gcclibdir}/ppc64/libgo.a
%{gcclibdir}/pthread/ppc64/libgo.a

%files -n libgo%{gcc_major}-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{gcclibdir}
%{gcclibdir}/libgobegin.a
%{gcclibdir}/libgolibbegin.a
%dir %{gcclibdir}/pthread
%{gcclibdir}/pthread/libgobegin.a
%{gcclibdir}/pthread/libgolibbegin.a
%dir %{gcclibdir}/ppc64
%{gcclibdir}/ppc64/libgobegin.a
%{gcclibdir}/ppc64/libgolibbegin.a
%dir %{gcclibdir}/pthread/ppc64
%{gcclibdir}/pthread/ppc64/libgobegin.a
%{gcclibdir}/pthread/ppc64/libgolibbegin.a
# .gox files
%{_libdir}/go/%{gcc_major}/%{buildhost}
%{_libdir}/pthread/go/%{gcc_major}/%{buildhost}
%{_libdir}/ppc64/go/%{gcc_major}/%{buildhost}
%{_libdir}/pthread/ppc64/go/%{gcc_major}/%{buildhost}

%endif


%changelog
* Wed May 05 2021 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-7
- Handle 64bit inodes for include directories.
- Improvement version requirements
- Add libgfortran subpackage
- Add libgcc dependency for libgo
- Improves %post regeneration of includes by calling mkheaders directly
- Remove configure option --with-cloog=no, --with-ppl=no,
  --enable-decimal-float=dpd and --enable__cxa_atexit
- Fix collect2 with archives containing text files

* Tue Jan 05 2021 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-6
- Fix %post and %postun with *info files
- Remove gcc as a dependency of libgomp
- Add beta version for locale support on libstdc++
- Update minimal version for libmpg, mpfr, gmp

* Thu Sep 17 2020 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-5
- Fix fixincludes for "sys/socket.h" and "malloc.h" after AIX7.2 TL4
- Always enable STDC format macros in "sys/inttypes.h"
- Fix collect2 when -fvisibility is provided
- Clean %check and remove parsing scripts

* Mon Aug 10 2020 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-4
- Revert the merging of 32/64bit in static libraries used by gccgo

* Thu Jul 16 2020 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-3
- Backported patch in order to use correct AR is libdecnumber
- Add older libgfortran for backward compatibility
- Add C++ filesystem support
- Regen include-fixed directory in %post
- Remove the merging of 32/64bit in static libraries

* Tue Apr 21 2020 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-2
- Improve long double support
    fix frexpl, ldexpl, modfl and fmodl with 64-bit long double
    add link with libc128.a with -mlong-double-128
- Fix where TLS variables had a wrong value

* Tue Mar 17 2020 Clement Chigot <clement.chigot@atos.net> - gcc9-9.3.0-1
- Update to version 9.3.0
- BullFreeware Compatibility Improvements
- Add multi gcc support and rename package gcc9
- Add gcov-dump and gcov-tool
- Remove .la files
- Always add /opt/freeware/lib in LIBPATH
- Add tests for libbacktrace and libgfortran
- Remove dependency over autoconf and automake

* Fri May 17 2019 Clement Chigot <clement.chigot@atos.net> - 9.1.0-1
- Update to version 9.1.0
- Change go commands to 64 bits (GOARCH=ppc64 by default)

* Thu Apr 04 2019 Clement Chigot <clement.chigot@atos.net> - 8.3.0-2
- Add missing features in net and syscall to enable golang.org/x/net

* Mon Feb 25 2019 Tony Reix <tony.reix@atos.net> - 8.3.0-1
- Move to GCC v8.3
- Rename go binaries to have both golang and gccgo available

* Thu Oct 18 2018 Tony Reix <tony.reix@atos.net> - 8.2.0-2
- Built on AIX 7.2 TL2 SP2 on Power9 in order to have pwr9 tuning.
- Fix several missing BuildRequires

* Tue Jul 31 2018 Tony Reix <tony.reix@atos.net> - 8.2.0-1
- Move to GCC v8.2
- Update the patch list with already merged patches

* Tue Jun 26 2018 Tony Reix <tony.reix@atos.net> - 8.1.0-3
- Suppress GLOBAL/GOLBAL now that -static-libgo works fine
- Add 2 patches for XCOFF speed improvement and for netpoll

* Wed May 23 2018 Tony Reix <tony.reix@atos.net> - 8.1.0-2
- New patches
- Fix the semsleep:32bit/64bit issue
- Fix the -static-libgcc and -static-libgo issue
- Fix the netpoll issue with high CPU consumption

* Wed May 02 2018 Tony Reix <tony.reix@atos.net> - 8.1.0-1
- Official version 8.1.0
- Adaptations for AIX 6.1

* Mon Mar 05 2018 Tony Reix <tony.reix@atos.net> - 8.0.1-4
- Move to snapshot 20180305
- Add missing gotools to list: buildid, gofmt, test2json, vet.

* Thu Mar 01 2018 Tony Reix <tony.reix@atos.net> - 8.0.1-3
- Fix "address space conflict" error. 20180301-mallocinit-v4.patch

* Tue Jan 30 2018 Tony Reix <tony.reix@atos.net> - 8.0.1-2
- Go v1.10 rc1.
- Go: "$" replaced by "..". No more need of Dollar patch
- Changes in gotest

* Tue Jan 23 2018 Tony Reix <tony.reix@atos.net> - 8.0.1-1
- First version of 8.0.1, with Go v1.10 beta2

* Mon Jan 15 2018 Tony Reix <tony.reix@atos.net> - 8.0.0-7
- "strip -t" the gotest a.out files.

* Fri Jan 12 2018 Tony Reix <tony.reix@atos.net> - 8.0.0-6
- "strip -t" the libgo.so.* files of libgo.a files. Abandonned.

* Tue Jan 09 2018 Tony Reix <tony.reix@atos.net> - 8.0.0-5
- Add *.gox files from pthread, ppc64, pthread/ppc64

* Tue Dec 05 2017 Tony Reix <tony.reix@atos.net> - 8.0.0-4
- Move to GCC svn-trunk of 2017/12/05
- Comment already-merged patches from 20171122 list

* Wed Nov 22 2017 Tony Reix <tony.reix@atos.net> - 8.0.0-3
- Move to GCC svn-trunk of 2017/11/22
- Comment already-merged patches from 20171003 list
- Add cgo tests

* Tue Oct 24 2017 Tony Reix <tony.reix@atos.net> - 8.0.0-2
- Fix issue with "ar rcD" in go command when:
     GOARCH=ppc64 (OBJECT_MODE=64 was required)

* Tue Oct 03 2017 Tony Reix <tony.reix@atos.net> - 8.0.0-1
- From 7.2.0-6
- New list of patches Patch10XY: gcc-8.0.0-go-trunk-20171003-*

* Fri Sep 29 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-6
- Change description of RPM
- Add some forgotten patches (cgo, -maix64 for ppc64/aix)

* Thu Sep 21 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-5
- Add new patches ("net", gox issue)

* Tue Aug 29 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-3
- Add new patches for cleanup of libgo and libiberty

* Fri Aug 18 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-2
- Add new patches for cgo
- Copy xcoff/testdata exec files

* Wed Aug 16 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-1
- Derived from experimental 7.1.0-8

* Mon Aug 07 2017 Tony Reix <tony.reix@atos.net> - 7.1.0-8
- Manages cgo
- Add Ian's patch for compiling Kubernetes

* Fri Jun 16 2017 Tony Reix <tony.reix@atos.net> - 7.1.0-7
- Unset LIBPATH

* Wed Jun 14 2017 Tony Reix <tony.reix@atos.net> - 7.1.0-6
- New experimental version of gccgo.
  4 failures out of 7358 Go compiler tests.
  12 failed tests out of 145 libgo tests (only few failed sub-tests).

* Wed May 17 2017 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.1.0-1
- Update to version 7.1.0 (gccgo still experimental)

* Mon Apr 24 2017 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.20170323-alpha
- Experimental build for testing Go.

* Tue Sep 27 2016 Tony Reix <tony.reix@bull.net> - 6.2.0-4
- Build go language too.
- Add patches for Go.

* Fri Sep 02 2016 Tony Reix <tony.reix@bull.net> - 6.2.0-2
- Rebuild now that autogen works fine for testing

* Tue Aug 23 2016 Tony Reix <tony.reix@bull.net> - 6.2.0-1
- Initial port on AIX 6.1

* Thu Jun 09 2016 Tony Reix <tony.reix@bull.net> - 6.1.0-5
- Remove everything dealing with AIX 5.*
- Put all 32bit & 64bit .so files in ..../libX.a file for X=
     atomic gcc_s stdc++ supc++ gomp gfortran caf_single
- Replace 64bits libs by link to 32bits lib
- Port on AIX 6.1

* Mon May 30 2016 Tony Reix <tony.reix@bull.net> - 6.1.0-4
- Fix issues with Requires for libstdc++ and libstdc++-devel

* Wed May 25 2016 Tony Reix <tony.reix@bull.net> - 6.1.0-3
- Improve tests: tools and logs analysis

* Mon May 23 2016 Tony Reix <tony.reix@bull.net> - 6.1.0-2
- Initial port on AIX 7.2

* Thu Nov 05 2015 Tony Reix <tony.reix@bull.net> - 5.2.0-1
- Updated to version 5.2.0

* Tue Mar 10 2015 Gerard Visiedo <gerard.visiedo@bull.net> - 4.8.4-2
- Change gcc and g++ binairies paths to standard bindir

* Fri Feb 27 2015 Hamza Sellami BULL <hamzasell@gmail.com> - 4.8.4-1
- Porting GCC 4.8.4 to fixe some issues

* Fri May 23 2014 Michael Perzl <michael@perzl.org> - 4.8.3-1
- Updated to version 4.8.3.

* Thu Oct 17 2013 Michael Perzl <michael@perzl.org> - 4.8.2-1
- Updated to version 4.8.2.

* Fri May 31 2013 Michael Perzl <michael@perzl.org> - 4.8.1-1
- Updated to version 4.8.1.

* Tue Apr 30 2013 Michael Perzl <michael@perzl.org> - 4.8.0-2
- Added missing files/libraries introduced with version 4.8.0.
- Added libstdc++ Python support files.

* Sun Mar 24 2013 Michael Perzl <michael@perzl.org> - 4.8.0-1
- Updated to version 4.8.0.

* Wed Dec 05 2012 Michael Perzl <michael@perzl.org> - 4.7.2-2
- Fixed wrong gcc shared libraries compatibility symbolic links.

* Fri Sep 21 2012 Michael Perzl <michael@perzl.org> - 4.7.2-1
- Updated to version 4.7.2.
- Added the -fPIC patch from David Edelsohn <edelsohn@us.ibm.com>.

* Tue Aug 21 2012 Michael Perzl <michael@perzl.org> - 4.7.1-3
- Added the "AIX libgcc.map missing" patch from
  http://gcc.gnu.org/ml/gcc-patches/2012-08/msg01120.html.

* Thu Jun 14 2012 Michael Perzl <michael@perzl.org> - 4.7.1-2
- Added the libstdc++ patch for GCC bug 52887.
- Reorganized gcc shared libraries compatibility symbolic links.

* Thu Jun 14 2012 Michael Perzl <michael@perzl.org> - 4.7.1-1
- Updated to version 4.7.1.

* Thu Mar 22 2012 Michael Perzl <michael@perzl.org> - 4.7.0-1
- Updated to version 4.7.0.

* Tue Mar 13 2012 Michael Perzl <michael@perzl.org> - 4.6.3-2
- Added missing dependency on gcc-cpp for 'gcc'.

* Thu Mar 01 2012 Michael Perzl <michael@perzl.org> - 4.6.3-1
- Updated to version 4.6.3.

* Thu Oct 27 2011 Michael Perzl <michael@perzl.org> - 4.6.2-1
- Updated to version 4.6.2.

* Wed Jul 13 2011 Michael Perzl <michael@perzl.org> - 4.6.1-1
- Updated to version 4.6.1.

* Wed Jul 13 2011 Michael Perzl <michael@perzl.org> - 4.6.0-2
- Fixed dependencies on gmp, mpfr and libmpc for gcc-c++ and gcc-cpp packages.

* Sat Mar 26 2011 Michael Perzl <michael@perzl.org> - 4.6.0-1
- Updated to version 4.6.0.

* Sat Mar 26 2011 Michael Perzl <michael@perzl.org> - 4.5.2-2
- Fixed some small RPM SPEC file errors.

* Thu Mar 10 2011 Michael Perzl <michael@perzl.org> - 4.5.2-1
- Updated to version 4.5.2.

* Thu Nov 04 2010 Michael Perzl <michael@perzl.org> - 4.4.5-1
- Updated to version 4.4.5.

* Tue Jun 22 2010 Michael Perzl <michael@perzl.org> - 4.3.5-1
- Updated to version 4.3.5.

* Wed Mar 24 2010 Michael Perzl <michael@perzl.org> - 4.3.4-1
- Updated to version 4.3.4.

* Fri Dec 11 2009 Michael Perzl <michael@perzl.org> - 4.2.4-2
- fixed some spec file and portability issues.

* Sat May 31 2008 Michael Perzl <michael@perzl.org> - 4.2.4-1
- Updated to version 4.2.4.

* Tue Feb 19 2008 Michael Perzl <michael@perzl.org> - 4.2.3-1
- Updated to version 4.2.3.

* Thu Nov 29 2007 Michael Perzl <michael@perzl.org> - 4.2.2-1
- First version for AIX, slightly based on the original SPEC file from IBM.
