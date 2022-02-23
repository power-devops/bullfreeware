# Tests by default. No tests: rpm -ba --define 'dotests 0' gcc*.spec

%ifos aix7.1 aix7.2
%{!?with_go: %define with_go 1}
%else
%define with_go 0
%endif

%{!?dotests: %define dotests 1}
%{!?do_default: %define do_default 1}

%{!?do_prep: %define do_prep %{do_default}}
%{!?do_build: %define do_build %{do_default}}
%{!?do_clean_build: %define do_clean_build %{do_default}}
%{!?do_install: %define do_install %{do_default}}

%global do_prep 1
%global do_build 1
%global do_clean_build 1
%global dotests 0
# dotest = 1 for:
#   libgo tests
# dotest = 2 for:
#   compilers tests ???
# dotest = 3 for: (about 20 hours...)
#   for DIR in ppc64 pthread pthread/ppc64; do
#        for LIB in libatomic libgomp libstdc++-v3; do
%global do_install 1

%define DO_OBJC 0
%define gcc_version 8.3.0
%define gcc_version_directory 8.3.0
%define rpm_version 8.3.0

Summary: GNU Compiler Collection
Name: gcc
Version: %{rpm_version}
Release: 1
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/

Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{gcc_version_directory}.tar.xz
# Used for snapshots:
#Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{gcc_version_directory}-%{release}.tar.xz

Source1: %{name}-BSum.1.0.sh
Source2: %{name}-BCmp.1.0.sh
Source3: %{name}-BCmpErr.1.0.sh
Source4: %{name}-ParseLibgo.sh

# Source code of the AIX objcopy: copycsect
# To be built with binutils package sources
# See copycsect.c for how to build it
# See: OBJCOPY for replacement
# Deprecated. Now, package binutils-gccgov1 provides it.
#   (However, keep it here for safety)
Source10: copycsect.c
Source11: copycsect
Source12: copycsectall.c
Source13: copycsectall

Source100: %{name}-%{version}-%{release}.build.log
Source101: %{name}-%{version}-%{release}.testslogs.tar.gz


# configure OBJCOPY: Patch to submit ??
Patch10060: gcc-8.1.0-configure_OBJCOPY-a.patch
Patch10061: gcc-8.1.0-configure_OBJCOPY-c.patch

# net.Interface() workaround: Patches supplementary. Ready to submit ???
Patch1007: gcc-8.1.0-net-interface-workaround-c.patch

# gotest: Required for AIX. However, should be improved before submit it
# +GL="${GL} -Wl,-bernotok -static-libgo -Wl,-bbigtoc"   !!!!!!!!!!!!
Patch1010: gcc-8.2.0-gotest-min.patch

# gotest trace: Some hints about how to trace gotest. Do not submit.
Patch10111: gcc-8.1.0-gotest-trace.patch
# For: net/http : -mcmodel=large in 64bit
Patch10112: gcc-8.2.0-gotest-nethttp.patch
# For: $BUILD/gcc-build-8.0.1/./gcc/ppc64/libgcc_s.a(shr.o) could not be loaded.
Patch10113: gcc-8.1.0-gotest-ppc64-go1.patch
# For: suppress duplicated tests (mainly in ppc64)
Patch10114: gcc-8.1.0-gotest-nodup.patch
# For: manage aix/ppc64 case vs linux/ppc64
# Change done
#Patch10115: gcc-8.1.0-gotest-text-ppc64.patch

# Add management of AIX and submit
# No more useful. Done already by gcc-8.2.0-gotest-min.patch
#Patch1012: gcc-8.1.0-no-section-anchors-b.patch

# Skip test on AIX. Submit ??
Patch1015: gcc-8.1.0-user_TestGroupIds.patch

# Already submitted as 44952 . Not merged yet. However, Ian does not like it...
#Part A Already merged ??
Patch10191: gcc-8.1.0-traceback_gccgo-New.patch

# Experimental
Patch1020: gcc-8.2.0-HasGoBuild.patch

# Ready to submit ? I think so. However, useful ??
# David : The reversion of config to oslevel is not acceptable.
#         Please remove that patch completely and find another solution if that truly is necessary.
# Study this !!
Patch1022: gcc-8.1.0-oslevel.patch

# Crashes the link of gotools if no GCC-Go (libgo.a) installed on machine...
# VERY TOUCHY !!! RE-ANALYZE IT !!!
# v7: Version without -brtllib
# Important !!!!!!!!!
Patch1023: gcc-8.1.0-lgo-brtllib-v7.patch

# Part of our solution for running tests on AIX with libgo packages duplicated
# -static-libgo -Wl,-bbigtoc
# VERY TOUCHY !!! RE-ANALYZE IT !!!
# No more useful. Done already by gcc-8.2.0-gotest-min.patch
#Patch1026: gcc-8.1.0-static-libgo-for-tests.patch

%ifos aix7.1 aix7.2
# NO Go on AIX 6.1
# ADDITIONAL_LANGUAGES=",go" on AIX !!
# To be submitted as the last patch, so that go is compiled within AIX
Patch1031: gcc-8.1.0-config-list.mk.patch
%endif

# Experimental
# Patch for suppressing the check of XO type for go_export CSect
#   Still useful ?????
#Patch1041: gcc-8.1.0-xcoff-go_export-noXOtest.patch

# Patch for suppressing the ar rcD and the -zdefs from gccgo
# Change done
#Patch1042: gcc-8.1.0-gccgo-aix.patch
# Change wrongly done... Here is the FIX:
# Merged in gcc go trunk
#Patch1043: gcc-8.1.0-go-20180504-gccgo-aix-FIX.patch

# runtime : os_aix.go : semsleep: 32bit issue due to Google using 2^64-1
Patch1044: gcc-8.1.0-runtime_semasleep.patch

# Fix for the -static-libgcc and -static-libgo issue
# Merged in GCC
#Patch1045: gcc-8.1.0-20180615-static-link-collect2.patch
# ChangeLog: gcc-8.1.0-20180615-static-link-collect2-changelog.patch is not patched

# Fix an issue with netpoll_aix
# Deprecated. Replaced by: gcc-8.1.0-20180731-go-netpoll-NoMorePollSet.patch
#Patch1046: gcc-8.1.0-20180601-go-netpoll-new-improvedVersion.patch


# Improvement of the loading time dealing with XCOFF
Patch1047: gcc-8.1.0-20180731-go-speedup-XCOFF.patch

# Complete rewriting of netpoll for AIX
# Edge-triggered instead of level-triggered.
# No more use of the pollset API which is not designed for edge-triggered.
# Use poll instead.
Patch1048: gcc-8.1.0-20180731-go-netpoll-NoMorePollSet.patch



# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: /opt/tmp/%{name}-%{gcc_version}-root

BuildRequires: bash, sed, texinfo, make, tar, gcc >= 6
BuildRequires: automake = 1.11.6, autoconf = 2.64
# Not sure this version 8.5 of tcl is really required...
#BuildRequires: tcl >= 8.5, tcl < 8.6
BuildRequires: tcl >= 8.5
BuildRequires: gmp-devel >= 4.3.2, mpfr-devel >= 2.4.2, libmpc-devel >= 0.8.1, m4 = 1.4.17
BuildRequires: zlib-devel >= 1.2.3-3
#BuildRequires: binutils, binutils-gccgov1
BuildRequires: binutils-gccgov1
# For: runtest
BuildRequires: dejagnu
%if %{dotests} >= 1
BuildRequires: autogen, autogen-libopts
%endif
Requires: info
Prereq: /sbin/install-info
Requires: libgcc = %{version}-%{release}
Requires: gcc-cpp = %{version}-%{release}
Conflicts: g++ <= 2.9.aix51.020209-4

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif


%define _libdir64 %{_prefix}/lib64
%define gcclibdir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%define gcclibexecdir %{_libexecdir}/gcc/%{buildhost}/%{gcc_version}

%description
The gcc package contains the GNU Compiler Collection version %{gcc_version}.
You'll need this package in order to compile C code.


Summary of tests results:
 # BSum.sh $SPECS/gcc-8...
 EP: Expected Passes
 UF: Unexpected Failures
 EF: Expected Failures
 US: Unexpected Successes
 UC: Unresolved TestCases
 UT: Unsupported Tests


%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
Requires: zlib >= 1.2.3-3
Obsoletes: g++
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.


%package cpp
Summary: The C Preprocessor
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
Requires: zlib >= 1.2.3-3
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

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


%package -n libgcc
Summary: GCC version %{gcc_version} shared support library
Group: Development/Libraries
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.


%package -n libstdc++
Summary: GNU Standard C++ Library
Group: Development/Libraries
Requires: libgcc = %{version}-%{release}
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.


%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++ = %{version}-%{release}
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes a rewritten implementation of STL.


%package gfortran
Summary: Fortran 95 support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
Requires: zlib >= 1.2.3-3
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description gfortran
The gcc-gfortran package provides support for compiling Fortran 95
programs with the GNU Compiler Collection.


%package -n libgomp
Summary: GCC OpenMP 2.5 shared support library
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.


if [ "%{DO_OBJC}" == 1 ]
then

Work in Progress

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: gcc-c++  = %{version}-%{release}
Requires: gcc-objc = %{version}-%{release}
Autoreq: true
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Group: System Environment/Libraries
Autoreq: true
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

fi


%if %{with_go}

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}

%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm <  7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
Requires: AIX-rpm <  7.3.0.0
%endif

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

This is GCC Go for AIX. With Go version 1.10 .
There are still only 5 failures in the Go compiler tests out of 7388 tests.
GCC Go on AIX appears in 4 flavors: 32bit, pthread, ppc64, pthread/ppc64.

This GCC Go compiler for AIX is being used for compiling/testing several large Go applications:
  - Filebeat
  - Hyperledeger
  - Kubelet (and other parts of Kubernetes)
  - parts of Docker
  - GRPC-Go
More improvements are required, mainly about golang.org/x packages, which do not know AIX.

Summary of remaining tests failures for 32bit:
# ParseLibgo.sh $SPECS/gcc-8

Your objects (.o), shared-objects (.so), and archives (.a) built from .go code 
should be rebuilt when a new stable version of GCC Go is available.
I mean to say that you'll probably not be able to mix .o, .so or .a files
compiled with different versions of GCC Go for AIX.

Full cgo feature of Go works only on AIX 7.2 since it is the first AIX version providing
sufficient DWARF support in XCOFF (and probably too on some recent TLs of AIX 7.1).

go command is 32bit by default.
Go 32bit has a limited memory for threads and data.
In order to run go command in 64bit, do:
	GOARCH=ppc64 go 
or (for big & complex application):
	GOARCH=ppc64 CGO_ENABLED=1 go build -gccgoflags='-Wl,-bbigtoc'

Feel free to contact me whenever you are facing issues.
Tony Reix tony.reix@atos.net


%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries

%description -n libgo
Objects (.o), shared-objects (.so), and archives (.a) built from .go code
should be rebuilt when a new version of GCC Go is available.

This package contains a Go shared library which is needed to run
Go dynamically linked programs.


%package -n libgo-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo = %{version}-%{release}

%description -n libgo-devel
This package includes libraries and support files for compiling Go programs.

# Also on AIX ?????
#	%package -n libgo-static
#	Summary: Static Go libraries
#	Group: Development/Libraries
#	Requires: libgo = %{version}-%{release}
#	Requires: gcc = %{version}-%{release}
#	
#	%description -n libgo-static
#	This package contains static Go libraries.


%endif


%prep
export PATH=/opt/freeware/bin:$PATH

if [ %{dotests} -ge 1 ]; then
  if /usr/bin/file `which autogen` | grep -q "64-bit"; then
    echo "ERROR: autogen command needs to be the 32 bit version to run the tests."
    exit 1
  fi
fi
if [ "%{do_prep}" == "1" ]; then

%setup -q -n gcc-%{gcc_version_directory}

%patch10060 -p1
%patch10061 -p1
%patch1007 -p1
%patch1010 -p1
%patch10111 -p1
%patch10112 -p1
%patch10113 -p1
%patch10114 -p1
#%patch1012 -p1
%patch1015 -p1
%patch10191 -p1
%patch1020 -p1
%patch1022 -p1
%patch1023 -p1
#%patch1026 -p1
%ifos aix7.1 aix7.2
%patch1031 -p1
%endif
#%patch1043 -p1
%patch1044 -p1
#%patch1045 -p1
#%patch1046 -p1
%patch1047 -p1
%patch1048 -p1


cd libgo

#automake --version
#autoconf --version

#(automake -v || true)
#(autoconf -v || true)

autoconf --version
autoreconf

else
echo "Prep skipped !"
fi


%build

# LIBPATH=/opt/freeware/lib breaks libffi tests
# since it looks at /opt/freeware/lib/libffi.a
# which contains an older version of libffi.so.
unset LIBPATH
unset OBJECT_MODE


echo "BUILD: $BUILD"
echo "LIBPATH: $LIBPATH"

if [ "%{do_build}" == 1 ]; then

echo "Build start time:"
date

echo "RPM packages installed on the system:"
/usr/bin/rpm -qa | /usr/bin/sort

echo "GCC version:"
gcc --version

export PATH=/usr/bin:/usr/sbin:/sbin:/opt/freeware/bin

# speed up the configure processes...
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

# objcopy for AIX: copycsect
# Deprecated. Now, package binutils-gccgov1 provides it.
#	export OBJCOPY=/opt/freeware/bin/copycsect
#	cp %{SOURCE11} ${OBJCOPY}

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export SED="/opt/freeware/bin/sed"
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar "
export M4="/opt/freeware/bin/m4"

# use maximum amount of memory (heap) available to 32-bit programs
# seems not to be taken into account though
export LDR_CNTRL=MAXDATA=0x80000000


if [ "%{do_clean_build}" == 1 ]; then
cd ..
rm -rf gcc-build-%{gcc_version_directory}
mkdir gcc-build-%{gcc_version_directory}
cd gcc-build-%{gcc_version_directory}

/opt/freeware/bin/gcc --version

LANGUAGES="c,c++,fortran,objc,obj-c++"
%if %{with_go}
    LANGUAGES="${LANGUAGES},go"
%endif

echo "Start of configure/build"
date

echo "GCC will be built with support for following languages: ${LANGUAGES}"

CC=/opt/freeware/bin/gcc					\
CXX=/opt/freeware/bin/g++					\
../%{name}-%{gcc_version_directory}/configure 			\
	--prefix=%{_prefix}					\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
	--with-local-prefix=/opt/freeware			\
	--with-as=/usr/bin/as					\
	--with-ld=/usr/bin/ld					\
	--enable-languages="${LANGUAGES}"			\
	--enable-version-specific-runtime-libs			\
	--disable-nls 						\
	--enable-decimal-float=dpd				\
	--with-cloog=no						\
	--with-ppl=no						\
	--disable-libstdcxx-pch					\
	--enable-__cxa_atexit					\
	--disable-werror					\
	--host=%{buildhost}

else # do_clean_build = 0
    cd ../gcc-build-%{gcc_version_directory}
fi # do_clean_build


export CC=/opt/freeware/bin/gcc
export CXX=/opt/freeware/bin/g++

ulimit -a
ulimit -d unlimited
ulimit -s unlimited
ulimit -m unlimited
ulimit -a


# configure/build takes about 100mn on AIX 7.2 with 4 CPU x 4 execution threads

export OPT_FLAG="-O2 -D_LARGE_FILES"
export OPT_FLAG="-O2"

export	BOOT_CFLAGS="${OPT_FLAG}"
export	  LT_CFLAGS="${OPT_FLAG}"
export	     CFLAGS="${OPT_FLAG}"
export	   CXXFLAGS="${OPT_FLAG}"
export	  LIBCFLAGS="${OPT_FLAG}"
export	LIBCXXFLAGS="${OPT_FLAG} -fno-implicit-templates"

echo "BUILD ENVIRONMENT:"
/usr/bin/env | /usr/bin/sort

%if %{with_go}
if [ ! -f /opt/freeware/lib/libgo.a ]; then
    ln -sf ${BUILD}/gcc-build-%{gcc_version_directory}/%{buildhost}/libgo/.libs/libgo.a /opt/freeware/lib/libgo.a
fi
%endif

#gmake --trace -d -j 8
gmake -j 8

echo "End of configure/build"
date

else
echo "Build skipped !"
fi


# strip -t the libgo.so* files contained by libgo.a files
# Goal: reduce symbols to only useful symbols. For faster start of Go processes.
# This is done BEFORE libgo tests are run.
# Note: due to a bug in "strip" command, "strip -t" fails on 64bit files.
# IMPOSSIBLE: libgo tests are made with -static-libgo, which is NOT compatible with stripped libgo.so.* 
# SOLUTION: strip -t the libgo tests a.out files in gotest script
#	mkdir /tmp/libgo$$
#	(
#	    cd    /tmp/libgo$$
#	    LIBGO_BASE=/opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version_directory}/%{buildhost}
#	    for LIB in libgo pthread/libgo ppc64/libgo pthread/ppc64/libgo ; do
#		ar -X32_64 -x ${LIBGO_BASE}/${LIB}/.libs/libgo.a
#		(strip -X32_64 -t libgo.so* || true)
#		ar -X32_64 -q libgo.a libgo.so*
#		mv    libgo.a ${LIBGO_BASE}/${LIB}/.libs/libgo.a
#		rm libgo.so*
#	    done
#	    cd -
#	)
#	rm -rf /tmp/libgo$$


# dotests==3 ==> ~23 hours on P8 2CPUs

# First : libgo !!
#
if [ "%{dotests}" -ge 1 ]
then

echo "Tests 1) libgo tests"
date

%if %{with_go}

    # LDR_CNTRL messes up the go compiler tests (timeouts)
    unset LDR_CNTRL

    cd /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version_directory}
    cd %{buildhost}


# This should be changed now by using -static-libgo since now it works !!
# Done by default already in gotest
    # Libgo tests require to change the entry point name in libgo to prevent
    # collect2 to find it when using -static-libgo
    # The original libgo will be restored after the tests
#	    for LIB in libgo pthread/libgo ppc64/libgo pthread/ppc64/libgo ; do
#	        cp -p ${LIB}/.libs/libgo.a ${LIB}/.libs/libgo.a.ORIGIN
#	        perl -pi -e 's/_GLOBAL__AIXI_libgo_so/_GOLBAL__AIXI_libgo_so/g' ${LIB}/.libs/libgo.a
#	    done

# Still useful now with changes applied to 7.2.0-5 ??
# No . See: libgo/Makefile.in
#	    # testenv.gox is not generated during build, but is required for tests
#	    for DIR in libgo pthread/libgo ppc64/libgo pthread/ppc64/libgo ; do
#	      cd $DIR
#	      (gmake internal/testenv.gox || true)
#	      (gmake net/internal/socktest.gox || true)
#	      cd -
#	    done

    cd libgo
      (gmake -k check || true)
    cd ..

#	    # Restore original libgo
#	    for LIB in libgo pthread/libgo ppc64/libgo pthread/ppc64/libgo ; do
#	        rm -f ${LIB}/.libs/libgo.a
#	        mv ${LIB}/.libs/libgo.a.ORIGIN ${LIB}/.libs/libgo.a
#	    done

# Tests of cgo
    cd /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version_directory}/gotools 
    (gmake check-cgo-test || true)

date

%endif

fi


if [ "%{dotests}" -ge "2" ]
then

echo "Tests 2) Basic tests"
date

    cd /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version_directory}

    (gmake -k check || true)

date

if [ "%{dotests}" -ge "3" ]
then

echo "Tests 3) ppc64, pthread, pthread/ppc64 tests"
date

    cd %{buildhost}
    
      for DIR in ppc64 pthread pthread/ppc64 ; do
        for LIB in libatomic libgomp libstdc++-v3 ; do
          echo $DIR $LIB
          cd $DIR/$LIB
          (gmake -k check || true)
          cd -
        done
      done
      
    cd ..

date

fi

/usr/sbin/slibclean


GCCTOOLS=/tmp/gcc-tools
echo "Tools for analyzing Tests results are available at $GCCTOOLS: BSum; BComp, BCompErr"
echo "  BSum    <rpm/rpmbuild -ba output file>"
echo "          It builds a Summary of the tests from the output of gmake check"
echo "  BCmp    <rpm/rpmbuild -ba output file ONE> <rpm/rpmbuild -ba output file TWO>"
echo "          It compares the results of 2 outputs of gmake check"
echo "  BCmpErr <rpm/rpmbuild -ba output file ONE> <rpm/rpmbuild -ba output file TWO>"
echo "          It compares the errors  of 2 outputs of gmake check"
echo "  You should use BSum on the output of these tests !!"
mkdir -p $GCCTOOLS
cp %{SOURCE1} $GCCTOOLS
cp %{SOURCE2} $GCCTOOLS
cp %{SOURCE3} $GCCTOOLS
cp %{SOURCE4} $GCCTOOLS

DA=/opt/freeware/src/packages/BUILD
DB=$DA/gcc-build-%{gcc_version_directory}
DC=$DB/gcc/testsuite
DD=$DB/%{buildhost}
DE=$DB/%{buildhost}/ppc64
DF=$DB/%{buildhost}/pthread
DG=$DB/%{buildhost}/pthread/ppc64

#/opt/freeware/src/packages/BUILD/gcc-build-6.1.0/gcc/testsuite/objc/objc.log
#/opt/freeware/src/packages/BUILD/gcc-build-6.1.0/powerpc-ibm-aix7.2.0.0/libatomic/testsuite/libatomic.log
#/opt/freeware/src/packages/BUILD/gcc-build-6.1.0/powerpc-ibm-aix7.2.0.0/ppc64/libatomic/testsuite/libatomic.log
#/opt/freeware/src/packages/BUILD//gcc-build-6.1.0/powerpc-ibm-aix7.2.0.0/pthread/libatomic/testsuite/libatomic.log
#/opt/freeware/src/packages/BUILD//gcc-build-6.1.0/powerpc-ibm-aix7.2.0.0/pthread/ppc64/libstdc++-v3/testsuite/libstdc++.log

echo "Tests logs are available at: /tmp/%{name}-%{gcc_version}.testslogs.tar.gz"
cd $DB
find . -name "*.log" | grep -v config.log | xargs /opt/freeware/bin/tar zcf  %{SOURCE101}
cd -

if [ "%{dotests}" -ge "3" ]
then
ls -1 $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log
RP=`grep PASS: $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log | wc -l`
RF=`grep FAIL: $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log | grep -v XFAIL | wc -l`
else
ls -1 $DC/*/*.log $DD/*/testsuite/*.log
RP=`grep PASS: $DC/*/*.log $DD/*/testsuite/*.log | wc -l`
RF=`grep FAIL: $DC/*/*.log $DD/*/testsuite/*.log | grep -v XFAIL | wc -l`
fi
echo "PASS: $RP"
echo "FAIL: $RF"

else
        echo "No test level 3 done." > %{SOURCE101}
fi

# END of tests


cd /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version_directory}

# remove the "-print-multi-os-directory" flag...
sed -e "s/MULTIOSDIR = \`\$(CC) \$(LIBCFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
mv -f Makefile.tmp libiberty/Makefile

echo "RPM_BUILD_ROOT: " ${RPM_BUILD_ROOT}

echo "Build end time : "
date


%install

if [ "%{do_install}" == "1" ]; then

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

export AR="/usr/bin/ar "


echo "RPM_BUILD_ROOT: " ${RPM_BUILD_ROOT}

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd ../gcc-build-%{gcc_version_directory}
gmake install DESTDIR=${RPM_BUILD_ROOT}

# strip compiler binaries
strip ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :
for file in cc1 cc1plus collect2 f951 lto-wrapper ; do
    strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/$file 2>/dev/null || :
done

# strip utilities
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/fixincl 2>/dev/null || :
strip ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/install-tools/fixincl 2>/dev/null || :

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

# gzip info pages
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info

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
%if %{with_go}
   cd ${RPM_BUILD_ROOT}/%{_bindir}
   mv go go.gcc
   mv gofmt gofmt.gcc
%endif

# create links in /usr/bin
(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/bin
    cd usr/bin
    for f in c++ \
             cpp \
             g++ \
             gcc \
%if %{with_go}
             gccgo \
             go.gcc \
             gofmt.gcc \
%endif
             gcov \
             gfortran \
             %{buildhost}-c++ \
             %{buildhost}-g++ \
             %{buildhost}-gcc \
             %{buildhost}-gcc-%{gcc_version} \
             %{buildhost}-gfortran \
             %{buildhost}-gcc-ar \
             %{buildhost}-gcc-nm \
             %{buildhost}-gcc-ranlib ; do
        ln -sf ../..%{_bindir}/$f .
    done
)

# strip debugging information of all libraries as the settings specified
# while bootstrapping do not seem to be taken into account
# Note 1: this does NOT strip the lib*.so files contained by the lib*.a files !!
# Note 2: this is done AFTER tests have been run !!
(
    cd ${RPM_BUILD_ROOT}

    for f in `find . -name "*.a"` ; do
        if [ -f ${f} ] ; then
            /usr/bin/strip -X32_64 ${f}
        fi
    done
)


# Add 64bit .so from 64bit libX.a to 32bit libX.a
# For X = atomic gcc_s stdc++ supc++ gomp gfortran caf_single
mkdir /tmp/gcc-$$
(
    cd    /tmp/gcc-$$

%if %{with_go}
    for lib in atomic gcc_s stdc++ supc++ gomp gfortran caf_single go gobegin golibbegin
%else
    for lib in atomic gcc_s stdc++ supc++ gomp gfortran caf_single
%endif
    do
        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
          ln -s                      %{_libdir}/gcc/%{buildhost}/%{gcc_version}/lib$lib.a .
	)

        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
          ln -s                      %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/lib$lib.a .
	)
    done
)
rm -rf /tmp/gcc-$$


# Add compatibility symbolic links
(
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -sf gcc/%{buildhost}/%{gcc_version}/libatomic.a .
    ln -sf gcc/%{buildhost}/%{gcc_version}/libgcc_s.a .
    ln -sf gcc/%{buildhost}/%{gcc_version}/libgfortran.a .
    ln -sf gcc/%{buildhost}/%{gcc_version}/libgomp.a .
    ln -sf gcc/%{buildhost}/%{gcc_version}/libstdc++.a .
%if %{with_go}
    ln -sf gcc/%{buildhost}/%{gcc_version}/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libatomic.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcc_s.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgfortran.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgomp.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libstdc++.a .
%if %{with_go}
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libstdc++.a .
%if %{with_go}
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libstdc++.a .
%if %{with_go}
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgo.a .
%endif
)

else
echo "Install skipped !"
fi


%post
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccinstall.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccint.info.gz %{_infodir}/dir || :

%post -n libgomp
/sbin/install-info %{_infodir}/libgomp.info.gz %{_infodir}/dir || :

%post cpp
/sbin/install-info %{_infodir}/cpp.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/cppinternals.info.gz %{_infodir}/dir || :

%post gfortran
/sbin/install-info %{_infodir}/gfortran.info.gz %{_infodir}/dir || :


%if %{with_go}

%post go
# Create links from default binaries to their .gcc name
ln -sf %{_bindir}/go.gcc %{_bindir}/go
ln -sf %{_bindir}/gofmt.gcc %{_bindir}/gofmt

%endif

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcc.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccinstall.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccint.info.gz %{_infodir}/dir || :
fi

%preun -n libgomp
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libgomp.info.gz %{_infodir}/dir || :
fi

%preun cpp
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpp.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/cppinternals.info.gz %{_infodir}/dir || :
fi

%preun gfortran
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gfortran.info.gz %{_infodir}/dir || :
fi

%if %{with_go}

%preun go
# Remove links to binaries if they're pointing to this RPM binaries
if ls -l %{_bindir}/go 2>/dev/null | grep -q '.gcc'; then
	rm %{_bindir}/go
fi
if ls -l %{_bindir}/gofmt 2>/dev/null | grep -q '.gcc'; then
	rm %{_bindir}/gofmt
fi

%endif



%clean
###[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/gcc
%{_bindir}/gcov
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/%{buildhost}-gcc
%{_bindir}/%{buildhost}-gcc-%{gcc_version}
%{_bindir}/%{buildhost}-gcc-ar
%{_bindir}/%{buildhost}-gcc-nm
%{_bindir}/%{buildhost}-gcc-ranlib
/usr/bin/gcc
/usr/bin/gcov
/usr/bin/%{buildhost}-gcc
/usr/bin/%{buildhost}-gcc-%{gcc_version}
/usr/bin/%{buildhost}-gcc-ar
/usr/bin/%{buildhost}-gcc-nm
/usr/bin/%{buildhost}-gcc-ranlib
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcov.a

%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/collect2
%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/lto-wrapper
%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/install-tools

%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/include
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/include/[^c++]*
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/include-fixed

%{_libdir}/gcc/%{buildhost}/%{gcc_version}/install-tools

%{_infodir}/gcc*

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1
%doc gcc/COPYING* MAINTAINERS gcc/README*


%files cpp
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_version}
%{_bindir}/cpp
/usr/bin/cpp
%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/cc1
%{_mandir}/man1/cpp.1
%{_infodir}/cpp*


%files -n libgomp
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgomp.spec
%{_libdir}/libgomp.a
%{_libdir64}/libgomp.a
%{_libdir}/pthread/libgomp.a
%{_libdir}/pthread/ppc64/libgomp.a
%{_infodir}/libgomp*


%files c++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_bindir}/c++
%{_bindir}/g++
%{_bindir}/%{buildhost}-c++
%{_bindir}/%{buildhost}-g++
/usr/bin/c++
/usr/bin/g++
/usr/bin/%{buildhost}-c++
/usr/bin/%{buildhost}-g++
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_version}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/cc1plus
%{_mandir}/man1/g++.1
%doc gcc/COPYING*


%files -n libgcc
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libatomic.*
%{_libdir}/libgcc_s.a
%{_libdir}/libatomic.a
%{_libdir64}/libgcc_s.a
%{_libdir64}/libatomic.a
%{_libdir}/pthread/libgcc_s.a
%{_libdir}/pthread/libatomic.a
%{_libdir}/pthread/ppc64/libgcc_s.a
%{_libdir}/pthread/ppc64/libatomic.a
%doc gcc/COPYING*


%files -n libstdc++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libstdc++.a
%{_libdir}/libstdc++.a
%{_libdir64}/libstdc++.a
%{_libdir}/pthread/libstdc++.a
%{_libdir}/pthread/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libstdc++.a-gdb.py
%dir %{_datadir}/gcc-%{gcc_version}
%dir %{_datadir}/gcc-%{gcc_version}/python
%{_datadir}/gcc-%{gcc_version}/python/libstdcxx
%doc gcc/COPYING*


%files -n libstdc++-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/include/c++
%doc gcc/COPYING*


%files gfortran
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_bindir}/gfortran
%{_bindir}/%{buildhost}-gfortran
/usr/bin/gfortran
/usr/bin/%{buildhost}-gfortran
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/finclude
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgfortran.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/libcaf_single.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgfortran.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/ppc64/libcaf_single.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgfortran.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libcaf_single.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgfortran.la
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libcaf_single.la
%{_libdir}/libgfortran.a
%{_libdir64}/libgfortran.a
%{_libdir}/pthread/libgfortran.a
%{_libdir}/pthread/ppc64/libgfortran.a
%{_libexecdir}/gcc/%{buildhost}/%{gcc_version}/f951
%{_infodir}/gfortran.info.gz
%{_mandir}/man1/gfortran.1
%doc gcc/COPYING*


#%if %{DO_OBJC}
#%files objc
#%defattr(-,root,system)
#./include/objc
#./include/objc/objc-decls.h
#./include/objc/objc-exception.h
#./include/objc/objc-sync.h
#./include/objc/objc.h
#./libobjc.a
#./libobjc.la
#./ppc64/libobjc.a
#./ppc64/libobjc.la
#./pthread/libobjc.a
#./pthread/libobjc.la
#./pthread/ppc64/libobjc.a
#./pthread/ppc64/libobjc.la
#%endif

%if %{with_go}

%files go
%{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{buildhost}
%dir %{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}
%{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}/go1
%{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}/cgo
%{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}/buildid
%{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}/test2json
%{_prefix}/libexec/gcc/%{buildhost}/%{gcc_version}/vet
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/libgobegin.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/libgolibbegin.a
%dir %{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/libgobegin.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/libgolibbegin.a
%dir %{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgobegin.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgolibbegin.a
%dir %{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgobegin.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgolibbegin.a

%files -n libgo
%{_prefix}/%{_lib}/libgo.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/libgo.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/libgo.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgo.a
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgo.a

%files -n libgo-devel
# .gox files
%{_prefix}/lib/go/%{gcc_version}/%{buildhost}
%{_prefix}/lib/pthread/go/%{gcc_version}/%{buildhost}
%{_prefix}/lib/ppc64/go/%{gcc_version}/%{buildhost}
%{_prefix}/lib/pthread/ppc64/go/%{gcc_version}/%{buildhost}
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgo.la

%endif


%changelog
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

* Tue Mar 01 2018 Tony Reix <tony.reix@atos.net> - 8.0.1-3
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

* Tue Sep 21 2017 Tony Reix <tony.reix@atos.net> - 7.2.0-5
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

* Tue Nov 05 2015 Tony Reix <tony.reix@bull.net> - 5.2.0-1
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
