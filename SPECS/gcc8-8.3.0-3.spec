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

# By default, objectif-C isn't made
# To build objectif-c: rpmbuild -ba --with objc *.spec
%bcond_with objc

%global do_clean_build 0

# By default, binaries and libraries are built on %default_arch bits.
%define default_arch 32

%define gcc_version 8.3.0
%define gcc_major 8

%define base_name gcc

# The build is made in another fodler under BUILD
%define build_dir /opt/freeware/src/packages/BUILD/gcc-build-%{gcc_version}

Summary: GNU Compiler Collection
Name:    %{base_name}%{gcc_major}
Version: %{gcc_version}
Release: 3
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/

Source0: ftp://ftp.gnu.org/gnu/%{base_name}/%{base_name}-%{version}/%{base_name}-%{gcc_version}.tar.xz
# Used for snapshots:
#Source0: ftp://ftp.gnu.org/gnu/%{base_name}/%{base_name}-%{version}/%{base_name}-%{gcc_version}-%{release}.tar.xz

Source1: %{base_name}-BSum.1.0.sh
Source2: %{base_name}-BCmp.1.0.sh
Source3: %{base_name}-BCmpErr.1.0.sh
Source4: %{base_name}-ParseLibgo.sh

Source100: %{name}-%{version}-%{release}.build.log
Source101: %{name}-%{version}-%{release}.testslogs.tar.gz

# GCC PATCHES

# Ready to submit ? I think so. However, useful ??
# David : The reversion of config to oslevel is not acceptable.
#         Please remove that patch completely and find another solution if that truly is necessary.
# Study this !!
Patch1:   gcc-8.1.0-oslevel.patch

# Add /opt/freeware/lib in default LIBPATH
Patch2:  gcc-8.3.0-gcc-config-force-opt-freeware-lib-in-AIX-LIBPATH.patch

# Fix linking with shared libraries
Patch9:   gcc-9.1.0-configure-fix-shrext-for-AIX.patch
Patch10:  gcc-9.1.0-configure-fix-disable-rpath-for-AIX.patch

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

# Skip test on AIX. Submit ??
Patch1015: gcc-8.1.0-user_TestGroupIds.patch

# Already submitted as 44952 . Not merged yet. However, Ian does not like it...
#Part A Already merged ??
Patch10191: gcc-8.1.0-traceback_gccgo-New.patch

# Experimental
Patch1020: gcc-8.2.0-HasGoBuild.patch

# Crashes the link of gotools if no GCC-Go (libgo.a) installed on machine...
# VERY TOUCHY !!! RE-ANALYZE IT !!!
# v8: add /opt/freeware/lib/gcc/8
# Important !!!!!!!!!
Patch1023: gcc-8.3.0-lgo-brtllib-v8.patch

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

# runtime : os_aix.go : semsleep: 32bit issue due to Google using 2^64-1
Patch1044: gcc-8.1.0-runtime_semasleep.patch

# Improvement of the loading time dealing with XCOFF
Patch1047: gcc-8.1.0-20180731-go-speedup-XCOFF.patch

# Complete rewriting of netpoll for AIX
# Edge-triggered instead of level-triggered.
# No more use of the pollset API which is not designed for edge-triggered.
# Use poll instead.
Patch1048: gcc-8.1.0-20180731-go-netpoll-NoMorePollSet.patch

# Add SockaddrDataLink for golang.org/x/net
# TO BE MERGED
Patch1049: gcc-8.3.0-libgo-go-syscall-add-sockaddrdatalink-for-aix-20190404.patch

# Add SO_REUSEPORT when multicast
# ALREADY MERGED
Patch1050: gcc-8.3.0-libgo-go-net-add-SO-REUSEPORT-on-socket-20190404.patch

BuildRequires: bash, sed, make, tar, gcc >= 6
# Version 6.7-1 has a bug with makeinfo_32
BuildRequires: texinfo >= 6.7-2
BuildRequires: automake = 1.11.6, autoconf = 2.64
# Not sure this version 8.5 of tcl is really required...
#BuildRequires: tcl >= 8.5, tcl < 8.6
BuildRequires: tcl >= 8.5
BuildRequires: gmp-devel >= 4.3.2, mpfr-devel >= 2.4.2, libmpc-devel >= 0.8.1, m4 = 1.4.17
BuildRequires: zlib-devel >= 1.2.3-3

# objcopy must be replaced by copycsect
#BuildRequires: binutils, binutils-gccgov1
BuildRequires: binutils-gccgov1
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

# Conflicts gcc without multi-gcc support
Conflicts: gcc <= 9.1.0

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
You will need this package in order to compile C code.


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
Requires: libstdc++%{gcc_major}-devel = %{version}-%{release}
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


%package -n libgcc%{gcc_major}
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

# Conflicts libgcc without multi-gcc support
Conflicts: libgcc <= 9.1.0

%description -n libgcc%{gcc_major}
This package contains GCC shared support library which is needed
e.g. for exception handling support.


%package -n libstdc++%{gcc_major}
Summary: GNU Standard C++ Library
Group: Development/Libraries
Requires: libgcc%{gcc_major} = %{version}-%{release}
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

%description -n libstdc++%{gcc_major}
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.


%package -n libstdc++%{gcc_major}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++%{gcc_major} = %{version}-%{release}
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

%description -n libstdc++%{gcc_major}-devel
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


%package -n libgomp%{gcc_major}
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

%description -n libgomp%{gcc_major}
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.

	
%if %{with objc}
%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libobjc%{gcc_major} = %{version}-%{release}
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
%{name}-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Group: Development/Languages
Requires: %{name}-c++  = %{version}-%{release}
Requires: %{name}-objc = %{version}-%{release}
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
%{name}-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc%{gcc_major}
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

This is GCC Go for AIX, with Go version 1.10.

This version of GCC Go is not supported anymore. Please move to GCC 9 or higher.
The main reason behind that is that the code made for the Golang toolchain was
integrated only as of GCC 9. Thus, a lot of improvement were made at the
same time.

%package -n libgo%{gcc_major}
Summary: Go runtime
Group: System Environment/Libraries

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

# %if %{with dotests}
# if /usr/bin/file `which autogen` | grep -q "64-bit"; then
#     echo "ERROR: autogen command needs to be the 32 bit version to run the tests."
#     exit 1
# fi
# %endif


%setup -q -n gcc-%{gcc_version}

%patch1 -p1
%patch2 -p1
%patch9 -p1
%patch10 -p1
%patch10060 -p1
%patch10061 -p1
%patch1007 -p1
%patch1010 -p1
%patch10111 -p1
%patch10112 -p1
%patch10113 -p1
%patch10114 -p1
%patch1015 -p1
%patch10191 -p1
%patch1020 -p1
%patch1023 -p1
%ifos aix7.1 aix7.2
%patch1031 -p1
%endif
%patch1044 -p1
%patch1047 -p1
%patch1048 -p1
%patch1049 -p1
%patch1050 -p1

cd libgo

autoconf --version
autoreconf


%build

# LIBPATH=/opt/freeware/lib breaks libffi tests
# since it looks at /opt/freeware/lib/libffi.a
# which contains an older version of libffi.so.
unset LIBPATH
unset OBJECT_MODE


echo "BUILD: $BUILD"
echo "LIBPATH: $LIBPATH"

echo "Build start time:"
date

echo "GCC version:"
gcc --version

export PATH=/usr/bin:/usr/sbin:/sbin:/opt/freeware/bin

# GCC is setting LD_LIBRARY_PATH when calling "make". This new libpath
# will find the newly created libgcc_s before the /opt/freeware/lib one.
# However, this new libgcc_s doesn't have both 32 and 64 bit shared objects but
# only the %default_arch version.
# Therefore, the binaries called inside "make" must have the same archiecture than
# the default one.
export MAKEINFO=/opt/freeware/bin/makeinfo_%{default_arch}

# speed up the configure processes...
export CONFIG_SHELL=/opt/freeware/bin/bash_%{default_arch}
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash_%{default_arch}

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export SED="/opt/freeware/bin/sed_%{default_arch}"
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

LANGUAGES="c,c++,fortran,objc,obj-c++"
%if %{with build_go}
    LANGUAGES="${LANGUAGES},go"
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
	--enable-decimal-float=dpd				\
	--with-cloog=no						\
	--with-ppl=no						\
	--disable-libstdcxx-pch					\
	--enable-__cxa_atexit					\
	--disable-werror					\
	--with-gcc-major-version-only  \
	--program-suffix=-%{gcc_major}					\
	--disable-rpath 			\
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
# export OPT_FLAG="-O2"

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
if [ ! -f %{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgo.a ]; then
	mkdir -p %{_libdir}/gcc/%{buildhost}/%{gcc_major}
    ln -sf ${BUILD}/gcc-build-%{gcc_version}/%{buildhost}/libgo/.libs/libgo.a %{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgo.a
fi
%endif

#gmake --trace -d -j 8
gmake -j8

echo "End of configure/build"
date

# remove the "-print-multi-os-directory" flag...
sed -e "s/MULTIOSDIR = \`\$(CC) \$(LIBCFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
mv -f Makefile.tmp libiberty/Makefile

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
strip ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/install-tools/fixincl 2>/dev/null || :

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
# (
# 	cd ${RPM_BUILD_ROOT}/%{_libdir}/gcc/%{buildhost}
# 	ln -sf %{gcc_major} %{gcc_version}
# )

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


# Add 64bit .so from 64bit libX.a to 32bit libX.a
# For X = atomic gcc_s stdc++ supc++ gomp gfortran caf_single
mkdir /tmp/gcc-$$
(
    cd    /tmp/gcc-$$

%if %{with build_go}
    for lib in atomic gcc_s stdc++ supc++ gomp gfortran caf_single go gobegin golibbegin
%else
    for lib in atomic gcc_s stdc++ supc++ gomp gfortran caf_single
%endif
    do
        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
          ln -s                      %{_libdir}/gcc/%{buildhost}/%{gcc_major}/lib$lib.a .
	)

        rm -f *
        $AR -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/lib$lib.a
        $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/lib$lib.a *
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/lib$lib.a
          cd        ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
          ln -s                      %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/lib$lib.a .
		)
    done
)
rm -rf /tmp/gcc-$$


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Compiler tests + all libgo tests
# Default way for gcc to do its tests.
echo "Tests 1) Compiler + libgo tests"
date

cd %{build_dir}
(gmake -k check || true)
(
	# CGO tests
	cd gotools
    (gmake check-cgo-test || true)
)

date

%if %{with longtests}
# Tests on others AIX target (ppc64, pthread)
echo "Tests 2) ppc64, pthread, pthread/ppc64 tests"
date

cd %{buildhost}
for DIR in ppc64 pthread pthread/ppc64 ; do
    for LIB in libatomic libgomp libstdc++-v3 libgo ; do
        echo $DIR $LIB
        cd $DIR/$LIB
        (gmake -k check || true)
        cd -
    done
done
cd ..

date
%endif


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

DIR_GCC=%{build_dir}/gcc/testsuite
DIR_PPC=%{build_dir}/%{buildhost}
DIR_PPC64=%{build_dir}/%{buildhost}/ppc64
DIR_PPC_PTHREAD=%{build_dir}/%{buildhost}/pthread
DIR_PPC64_PTHREAD=%{build_dir}/%{buildhost}/pthread/ppc64


echo "Tests logs are available at: /tmp/%{base_name}-%{gcc_version}.testslogs.tar.gz"
cd %{build_dir}
find . -name "*.log" | grep -v config.log | xargs /opt/freeware/bin/tar zcf  %{SOURCE101}
cd -


%if %{with longtests}
ls -1 $DDR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log $DIR_PPC64/*/testsuite/*.log $DIR_PPC_PTHREAD/*/testsuite/*.log $DIR_PPC64_PTHREAD/*/testsuite/*.log
RP=`grep PASS: $DIR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log $DIR_PPC64/*/testsuite/*.log $DIR_PPC_PTHREAD/*/testsuite/*.log $DIR_PPC64_PTHREAD/*/testsuite/*.log | wc -l`
RF=`grep FAIL: $DIR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log $DIR_PPC64/*/testsuite/*.log $DIR_PPC_PTHREAD/*/testsuite/*.log $DIR_PPC64_PTHREAD/*/testsuite/*.log | grep -v XFAIL | wc -l`
%else
ls -1 $DIR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log
RP=`grep PASS: $DIR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log | wc -l`
RF=`grep FAIL: $DIR_GCC/*/*.log $DIR_PPC/*/testsuite/*.log | grep -v XFAIL | wc -l`
%endif
echo "PASS: $RP"
echo "FAIL: $RF"

# END of tests

%post
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccinstall.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccint.info.gz %{_infodir}/dir || :

%post -n libgomp%{gcc_major}
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

%preun -n libgomp%{gcc_major}
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
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/crtdbase.o
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgcov.a

%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/include
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/include/[^c++]*
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/include-fixed

%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/collect2
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/lto-wrapper
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/install-tools


%{_libdir}/gcc/%{buildhost}/%{gcc_major}/install-tools

%{_infodir}/gcc*

%{_mandir}/man1/gcc-%{gcc_major}.1
%{_mandir}/man1/gcov-%{gcc_major}.1
%doc gcc/COPYING* MAINTAINERS gcc/README*


%files cpp
%defattr(-,root,system)
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}
%{_bindir}/cpp-%{gcc_major}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/cc1
%{_mandir}/man1/cpp-%{gcc_major}.1
%{_infodir}/cpp*



%files c++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_bindir}/c++-%{gcc_major}
%{_bindir}/g++-%{gcc_major}
%{_bindir}/%{buildhost}-c++-%{gcc_major}
%{_bindir}/%{buildhost}-g++-%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/cc1plus
%{_mandir}/man1/g++-%{gcc_major}.1


%files -n libgcc%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libatomic.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libatomic.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libatomic.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libatomic.a
%doc gcc/COPYING*


%files -n libstdc++%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libstdc++.a-gdb.py
%dir %{_datadir}/gcc-%{gcc_major}
%dir %{_datadir}/gcc-%{gcc_major}/python
%{_datadir}/gcc-%{gcc_major}/python/libstdcxx


%files -n libstdc++%{gcc_major}-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/include/c++


%files -n libgomp%{gcc_major}
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgomp.spec
%{_infodir}/libgomp*


%files gfortran
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_bindir}/gfortran-%{gcc_major}
%{_bindir}/%{buildhost}-gfortran-%{gcc_major}
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/finclude
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libcaf_single.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgfortran.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgfortran.spec
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libcaf_single.a
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/f951
%{_infodir}/gfortran-%{gcc_major}.info.gz
%{_mandir}/man1/gfortran-%{gcc_major}.1


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
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{gcc_major}
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/go1
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/cgo
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/buildid
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/test2json
%{_libexecdir}/gcc/%{buildhost}/%{gcc_major}/vet

%files -n libgo%{gcc_major}
%defattr(-,root,system)
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgo.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgo.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgo.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgo.a

%files -n libgo%{gcc_major}-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgobegin.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/libgolibbegin.a
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgobegin.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/libgolibbegin.a
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgobegin.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/ppc64/libgolibbegin.a
%dir %{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgobegin.a
%{_libdir}/gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgolibbegin.a
# .gox files
%{_libdir}/go/%{gcc_major}/%{buildhost}
%{_libdir}/pthread/go/%{gcc_major}/%{buildhost}
%{_libdir}/ppc64/go/%{gcc_major}/%{buildhost}
%{_libdir}/pthread/ppc64/go/%{gcc_major}/%{buildhost}

%endif


%changelog
* Wed Feb 26 2020 Clément Chigot <clement.chigot@atos.net> - gcc8-8.3.0-3
- BullFreeware Compatibility Improvements
- Add multi gcc support and rename package gcc8
- Add gcov-dump and gcov-tool
- Remove .la files
- Always add /opt/freeware/lib in LIBPATH

* Thu Apr 04 2019 Clément Chigot <clement.chigot@atos.net> - 8.3.0-2
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
