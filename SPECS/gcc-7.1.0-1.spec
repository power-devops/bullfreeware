# Tests by default. No tests: rpm -ba --define 'dotests 0' gcc*.spec
%{!?with_go: %define with_go 1}

%{!?dotests: %define dotests 1}
%{!?do_default: %define do_default 1}
%{!?do_prep: %define do_prep %{do_default}}
%{!?do_build: %define do_build %{do_default}}
%{!?do_clean_build: %define do_clean_build %{do_default}}
%{!?do_install: %define do_install %{do_default}}

%define DO_OBJC 0
%define gcc_version 7.1.0
%define gcc_version_directory 7.1.0
%define rpm_version 7.1.0

Summary: GNU Compiler Collection
Name: gcc
Version: %{rpm_version}
Release: 1
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-%{gcc_version_directory}.tar.bz2
Source1: %{name}-BSum.1.0.sh
Source2: %{name}-BCmp.1.0.sh
Source3: %{name}-BCmpErr.1.0.sh

Source4: %{name}-%{version}-%{release}.build.log

# This file is not included in the snapshots, and the generation fails.
# As the .l file used for generation is the same on GCC 6.2.0, we use
# the c file for GCC 6.2.0 release.
# no more needed with /opt/freeware/bin/m4
#Source5: gcc-6.2.0-gengtype-lex.c

# Patches already merged into gccgo sources
Patch0: gcc-7.0.0-go-merged-20170323.patch
Patch1: gcc-7.0.0-go-1ccb22b.diff
Patch2: gcc-7.0.0-go-27db481.diff
Patch3: gcc-7.0.0-go-c93babb.diff
Patch4: gcc-7.0.0-go-c0b00f0.diff
Patch5: gcc-7.0.0-go-0dc369f.diff
Patch6: gcc-7.0.0-go-c3db34f.diff
Patch7: gcc-7.0.0-go-66926ca.diff
Patch8: gcc-7.0.0-go-43101e5.diff
Patch9: gcc-7.0.0-go-be4a751.diff
Patch10: gcc-7.0.0-go-46a669c.diff
Patch11: gcc-7.0.0-go-53b0e80.diff
Patch12: gcc-7.0.0-go-f8d5ebd.diff
Patch13: gcc-7.0.0-go-ef56097.diff
Patch14: gcc-7.0.0-go-fc3d6af.diff

# Other Google-part patches, not yet merged
Patch21: gcc-7.0.0-go-configure.patch
Patch23: gcc-7.0.0-go-dollars1.patch
Patch24: gcc-7.0.0-go-dollars2.patch
Patch25: gcc-7.0.0-go-dollars4.patch
Patch26: gcc-7.0.0-go-dollars-gotest.patch
Patch30: gcc-7.0.0-go-no-section-anchors.patch
Patch33: gcc-7.0.0-go-socktest_sys_unix_aix.patch
Patch34: gcc-7.0.0-go-stat_timespec.patch
Patch35: gcc-7.0.0-go-test-hostname.patch
Patch36: gcc-7.0.0-go-uintptr_go_symbol_value.patch
Patch38: gcc-7.0.0-go-user_TestGroupIds.patch
Patch40: gcc-7.0.0-go-dollars5.patch
Patch43: gcc-7.0.0-go-lfstack_64bit.patch
#Patch44: gcc-7.0.0-go-nil_panic_C.patch
#Patch45: gcc-7.0.0-go-nil_panic_Go.patch
Patch47: gcc-7.0.0-go-panic_pc.patch
Patch48: gcc-7.0.0-go-whole-archive.patch
Patch49: gcc-7.0.0-go-lgo-brtllib-v5.patch

# Other FSF-part patches
Patch50: gcc-6.2.0-go-backend.patch
Patch51: gcc-6.2.0-go-configure.patch
Patch52: gcc-6.2.0-go-simple-object-xcoff.patch
Patch53: gcc-6.2.0-oslevel.patch
Patch54: gcc-7.0.0-enable-ffi.patch
Patch55: gcc-7.0.0-go-config-list.mk.patch
Patch56: gcc-7.0.0-libbacktrace-aix.patch
Patch58: gcc-7.0.0-libffi.patch
Patch59: gcc-6.2.0-go-system.h.patch
Patch60: gcc-7.0.0-aix-unwind.patch
Patch61: gcc-7.1.0-go-gotools-blibpath.patch

%ifos aix6.1
# Required for AIX 6.1, not 7.2. Must be applied last AFTER os_build_aix.patch
Patch100: %{name}-7.0.0-go-os_stat_atime.patch
%endif

# Patches that should not be submitted !
# proc.c from git repo don't uses hz anymore, but is not yet included in GCC snapshots
Patch200: gcc-7.0.0-go-runtime-hz2.patch

# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: /opt/tmp/%{name}-%{gcc_version}-root

BuildRequires: bash, sed, automake = 1.11.6, autoconf = 2.64, texinfo, make, tar, gcc >= 6, tcl >= 8.5, tcl < 8.6
BuildRequires: gmp-devel >= 4.3.2, mpfr-devel >= 2.4.2, libmpc-devel >= 0.8.1
BuildRequires: zlib-devel >= 1.2.3-3
BuildRequires: binutils-gccgov1
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

if [ "%{with_go}" == 1 ]
then

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}

%description go
WARNING: This is a pre-release package.
It is aimed at experimenting gccgo in an AIX environment and should NOT be used
for production.

The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries

%description -n libgo
WARNING: This is a pre-release package.
It is aimed at experimenting gccgo in an AIX environment and should NOT be used
for production.

This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo = %{version}-%{release}

%description -n libgo-devel
WARNING: This is a pre-release package.
It is aimed at experimenting gccgo in an AIX environment and should NOT be used
for production.

This package includes libraries and support files for compiling
Go programs.

fi

%prep
if [ "%{dotests}" == "1" ]; then
  if file -L `which autogen` | grep -q "64-bit"; then
    echo "ERROR: autogen command needs to be the 32 bit version to run the tests."
    exit 1
  fi
fi
if [ "%{do_prep}" == "1" ]; then

%setup -q -n gcc-%{gcc_version_directory}
export PATH=/opt/freeware/bin:$PATH

%patch0 -p1
%patch1 -p1
%patch2 -p1
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

%patch21 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
#%patch29 -p1
%patch30 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch40 -p1
%patch43 -p1
#%patch44 -p1
#%patch45 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1

%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
#%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1

%ifos aix6.1
%patch100 -p1
%endif

%patch200 -p1

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
if [ "%{do_build}" == 1 ]; then

echo "Build start time:"
date

echo "RPM packages installed on the system:"
/usr/bin/rpm -qa

echo "GCC version:"
gcc --version

export PATH=/usr/bin:/usr/sbin:/sbin:/opt/freeware/bin

# speed up the configure processes...
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export OBJCOPY=/opt/freeware/bin/copycsect

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
if [ "%{with_go}" == "1" ]; then
    LANGUAGES="${LANGUAGES},go"
fi

echo "GCC will be built with support for following languages: ${LANGUAGES}"

CC=/opt/freeware/bin/gcc					\
CXX=/opt/freeware/bin/g++					\
../%{name}-%{gcc_version_directory}/configure 				\
	--prefix=%{_prefix}					\
	--mandir=%{_mandir}					\
	--infodir=%{_infodir}					\
	--with-local-prefix=/opt/freeware			\
	--with-as=/usr/bin/as					\
	--with-ld=/usr/bin/ld					\
	--enable-languages="${LANGUAGES}"				\
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

ulimit -d unlimited
ulimit -s unlimited


# Takes about 82mn on AIX 7.2 with 2 CPUs

export NO_DOLLAR_IN_LABEL_FOR_GO=
export NO_DOLLAR_IN_LABEL_FOR_GO="-DNO_DOLLAR_IN_LABEL_FOR_GO"

export OPT_FLAG="-O2 -D_LARGE_FILES"
export OPT_FLAG="-O2"

export	BOOT_CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"
export	  LT_CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"
export	     CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"
export	   CXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"
export	  LIBCFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"
export	LIBCXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO} -fno-implicit-templates"

echo "BUILD ENVIRONMENT:"
/usr/bin/env

( gmake -j 8								\
	BOOT_CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"				\
	     CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"				\
	   CXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"				\
	  LIBCFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"				\
	LIBCXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO} -fno-implicit-templates" || true )

cd %{buildhost}/libgo
gmake cmd/internal/browser.gox
cd -

gmake -j 8                                                              \
        BOOT_CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"                          \
             CFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"                          \
           CXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"                          \
          LIBCFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO}"                          \
        LIBCXXFLAGS="${OPT_FLAG} ${NO_DOLLAR_IN_LABEL_FOR_GO} -fno-implicit-templates"

# >= 600mn on P8 2CPUs

if [ "%{dotests}" == "1" ]
then
    # LDR_CNTRL messes up the go compiler tests (timeouts)
    unset LDR_CNTRL

    (gmake -k check || true)

    cd %{buildhost}
    
# Already done in previous gmake check ?!!
#      cd libatomic
#      (gmake -k check || true)
#      cd ..

#      cd libgomp
#      (gmake -k check || true)
#      cd ..

      # testenv.gox is not generated during build, but is required for tests
      for DIR in libgo pthread/libgo ppc64/libgo pthread/ppc64/libgo; do
        cd $DIR
        (gmake internal/testenv.gox || true)
        cd -
      done

      cd libgo
      (gmake -k check || true)
      cd ..

      for DIR in ppc64 pthread pthread/ppc64; do
        for LIB in libgo libatomic libgomp libstdc++-v3; do
          echo $DIR $LIB
          cd $DIR/$LIB
          (gmake -k check || true)
          cd -
        done
      done
      
    cd ..

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

ls -1 $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log

echo "Tests logs are available at: /tmp/%{name}-%{gcc_version}.testslogs.tar.gz"
cd $DB
find . -name "*.log" | grep -v config.log | xargs /opt/freeware/bin/tar zcf /tmp/%{name}-%{gcc_version}.testslogs.tar.gz
cd -

RP=`grep PASS: $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log | wc -l`
RF=`grep FAIL: $DC/*/*.log $DD/*/testsuite/*.log $DE/*/testsuite/*.log $DF/*/testsuite/*.log $DG/*/testsuite/*.log | grep -v XFAIL | wc -l`
echo "PASS: $RP"
echo "FAIL: $RF"

fi
# END of tests


# remove the "-print-multi-os-directory" flag...
sed -e "s/MULTIOSDIR = \`\$(CC) \$(LIBCFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
mv -f Makefile.tmp libiberty/Makefile

echo "RPM_BUILD_ROOT: " ${RPM_BUILD_ROOT}

echo "Build end time : "
date

else
echo "Build skipped !"
fi

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
for dir in power powerpc ppc64 pthread; do
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

# create links in /usr/bin
(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/bin
    cd usr/bin
    for f in c++ \
             cpp \
             g++ \
             gcc \
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

    for lib in atomic gcc_s stdc++ supc++ gomp gfortran caf_single go gobegin golibbegin
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
    ln -sf gcc/%{buildhost}/%{gcc_version}/libgo.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libatomic.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgcc_s.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgfortran.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgomp.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libstdc++.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgo.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libstdc++.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_version}/pthread/libgo.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libstdc++.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgo.a .
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
%{_prefix}/bin/go
%{_prefix}/bin/gccgo
%{_prefix}/bin/gofmt
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
%{_prefix}/lib/go/%{gcc_version}/%{buildhost}
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/ppc64/libgo.la
%{_prefix}/lib/gcc/%{buildhost}/%{gcc_version}/pthread/ppc64/libgo.la

%endif


%changelog
* Wed May 17 2017 Matthieu Sarter <matthieu.sarter.external@atos.net> - 7.1.0
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
