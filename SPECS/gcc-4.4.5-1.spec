%define gcc_version 4.4.5
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%define gcc_release 1

%define libjavatoolversion 10

Summary: GNU Compiler Collection
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-core-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-g++-%{version}.tar.bz2
Source2: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-java-%{version}.tar.bz2
Source3: ftp://sourceware.org/pub/java/ecj-latest.jar
Patch1: gcc-4.4.5-aixos.patch
Patch2: gcc-4.4.5-java.patch
Patch3: gcc-4.4.5-sup_debug.patch
Patch4: gcc-4.4.5-libffi.patch
Patch5: gcc-4.4.5-libjava.patch

# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: bash, sed, automake, autoconf, texinfo, make, tar
BuildRequires: gmp-devel, mpfr-devel
# libjava
Requires: info
Prereq: /sbin/install-info
Conflicts: g++ <= 2.9.aix51.020209-4

%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%define gcclibdir %{_libdir}/gcc/%{buildhost}/%{version}
%define gcclibexecdir %{_libexecdir}/gcc/%{buildhost}/%{version}
%define gxxinclude %{gcclibdir}/include/c++

%description
The gcc package contains the GNU Compiler Collection version %{version}
in order to compile C code.
The gcc package contains also the cpp, the GNU C-Compatible Compiler Preprocessor.

%package locale
Summary: Locale data for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description locale
Locale data for GCC to display error message in locale language.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Obsoletes: g++
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description c++
The gcc-c++ package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.
The static standard C++ library and C++ header files are included.

%package -n libgcc
Summary: GCC version %{version} shared support library
Group: Development/Libraries
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description -n libgcc
This package is required at runtime for programs dynamically linked with GCC.

%package -n libgomp
Summary: GCC OpenMP 2.5 shared support library
Group: Development/Languages
Requires: gcc = %{version}-%{release}
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.

%package -n libstdc++
Summary:  GNU Standard C++ Library
Group: Development/Libraries
Requires: libgcc
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
%endif

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development.

%package java
Summary: The GNU Java compiler
Group: Development/Tools
Requires: gcc = %{version}-%{release}

%description java
The java package includes the gcj GNU compiler for compiling Java code.

%package -n libgcj
Summary: The GNU Java Runtime Library
Group: Development/Libraries
Requires: gcc = %{version}-%{release}

%description -n libgcj
This library is needed by the GNU Java compiler.

%package -n libgcj-devel
Summary: Include Files and Libraries for libgcj
Group: Development/Libraries
Requires: gcc = %{version}-%{release}
Requires: libstdc++-devel = %{version}
Requires: libgcj = %{version}-%{release}
Requires: zlib-devel

%description -n libgcj-devel
This library is needed by the GNU Java compiler.

%package gij
Summary: GCC Java Bytecode Interpreter
Group: Development/Tools
Requires: libgcj >= %{version}-%{release}

%description gij
This package contains the Java Bytecode interpreter.

%package -n libffi
Summary: Foreign Function Interface library
Group: System/Libraries

%description -n libffi
This library all-ows one language to call function written in another language.

%package -n libffi-devel
Summary: Foreign Function Interface library development files
Group: System/Libraries

%description -n libffi-devel
This library all-ows one language to call function written in another language.

%prep
%setup -q -b 1 -b 2
%patch1 -p1 -b .aixos
%patch2 -p1 -b .java
%patch3 -p1 -b .sup_debug
%patch4 -p1 -b .libffi
%patch5 -p1 -b .libjava
cp %{SOURCE3} ecj.jar

%build
# Boost configure speed by a factor of 10:
# ksh creates all pipes, redirections, etc in /tmp
# whereas bash uses memory
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"

# use maximum amount of memory (heap) available to 32-bit programs
export LDR_CNTRL=MAXDATA=0x80000000

rm -rf objdir
mkdir objdir
cd objdir

GCJFLAGS="" \
CFLAGS="-O2" \
CXXFLAGS="-O2" \
LIBCFLAGS="-O2" \
LIBCXXFLAGS="-O2 -fno-implicit-templates" \
../configure \
--with-as=/usr/bin/as \
--with-ld=/usr/bin/ld \
--enable-languages=c,c++,java \
--prefix=%{_prefix} \
--infodir=%{_infodir} \
--mandir=%{_mandir} \
--enable-threads \
--enable-version-specific-runtime-libs \
--host=%{buildhost} \
--target=%{buildhost} \
--build=%{buildhost} \
--disable-libjava-multilib 

ulimit -d unlimited
ulimit -s unlimited


# gcj crashes with -O2 in some cases (too many classes)
GCJFLAGS="" gmake bootstrap-lean


%install
# Boost configure speed by a factor of 10:
# ksh creates all pipes, redirections, etc in /tmp
# whereas bash uses memory
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash


[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd objdir
gmake install DESTDIR=${RPM_BUILD_ROOT}

# Remove unneeded links in bin/
rm -f ${RPM_BUILD_ROOT}%{_bindir}/c++*
rm -f ${RPM_BUILD_ROOT}%{_bindir}/powerpc*

# Don't need to ship gccbug
rm -f ${RPM_BUILD_ROOT}%{_bindir}/gccbug

# Strip compiler binaries
strip ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :
for file in cc1 cc1plus collect2 jc1 jvgenmain ecj1; do
  strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/$file 2>/dev/null || :
done

# Strip utilities
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/fixincl 2>/dev/null || :
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/mkheaders 2>/dev/null || :

# Remove unrelated man pages
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man7

# Remove libiberty.a library which is not used directly by gcc.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty.a
for dir in power powerpc ppc64 pthread; do
  rm -rf ${RPM_BUILD_ROOT}%{_libdir}/$dir
done

# Remove libtool files
for arch in . power powerpc ppc64; do
  rm -f ${RPM_BUILD_ROOT}%{gcclibdir}/$arch/*.la
  rm -f ${RPM_BUILD_ROOT}%{gcclibdir}/pthread/$arch/*.la
done

# Remove zutil.h which is not installed by default on AIX systems
rm -f ${RPM_BUILD_ROOT}%{gcclibdir}/include/zutil.h

# Remove empty include directory
rmdir ${RPM_BUILD_ROOT}%{_includedir} || :

# Gzip info pages
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info

# Create links in /usr/bin
(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/bin
    cd usr/bin
    for fname in aot-compile g++ gappletviewer gc-analyze gcc gcj gcj-dbtool gcjh gcov gij gjar gjarsigner gjavah gkeytool gnative2ascii gorbd grmic grmid grmiregistry gserialver gtnameserv jcf-dump jv-convert rebuild-gcj-db; do
        ln -sf ../..%{_bindir}/$fname .
    done
)

(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    ln -sf ../..%{_prefix}/bin/cpp .
)

%post
/sbin/install-info %{_infodir}/cpp.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/cppinternals.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/gccint.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/gccinstall.info.gz %{_infodir}/dir

%post java
/sbin/install-info %{_infodir}/cp-tools.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gcj.info.gz %{_infodir}/dir || :

%post -n libgomp
/sbin/install-info %{_infodir}/libgomp.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpp.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/cppinternals.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gcc.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccint.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gccinstall.info.gz %{_infodir}/dir || :
fi

%preun java
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cp-tools.info.gz %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gcj.info.gz %{_infodir}/dir || :
fi

%preun -n libgomp
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libgomp.info.gz %{_infodir}/dir || :
fi


%files
%defattr(-,root,system)
%{_bindir}/gcc
%{_bindir}/gcov
/usr/bin/gcc
/usr/bin/gcov
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/include
%dir %{_libdir}/gcc/%{buildhost}/%{version}/include-fixed
%dir %{_libdir}/gcc/%{buildhost}/%{version}/install-tools
%dir %{_libdir}/gcc/%{buildhost}/%{version}/install-tools/include
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64

%dir %{gcclibexecdir}/install-tools

%{gcclibdir}/libgcc.a
%{gcclibdir}/ppc64/libgcc.a
%{gcclibdir}/pthread/libgcc.a
%{gcclibdir}/pthread/ppc64/libgcc.a
%{gcclibdir}/libgcc_eh.a
%{gcclibdir}/ppc64/libgcc_eh.a
%{gcclibdir}/pthread/libgcc_eh.a
%{gcclibdir}/pthread/ppc64/libgcc_eh.a
%{gcclibdir}/libgcov.a
%{gcclibdir}/ppc64/libgcov.a
%{gcclibdir}/pthread/libgcov.a
%{gcclibdir}/pthread/ppc64/libgcov.a
%{gcclibexecdir}/collect2


%{gcclibdir}/include/*.h

%{gcclibdir}/libgcc_s.a
%{gcclibdir}/ppc64/libgcc_s.a
%{gcclibdir}/pthread/libgcc_s.a
%{gcclibdir}/pthread/ppc64/libgcc_s.a
%{gcclibdir}/include-fixed/*.h
%{gcclibdir}/include-fixed/README
%{gcclibdir}/install-tools/gsyslimits.h
%{gcclibdir}/install-tools/mkheaders.conf
%{gcclibdir}/install-tools/include/README
%{gcclibdir}/install-tools/include/limits.h
%{gcclibexecdir}/install-tools/fixinc.sh
%{gcclibexecdir}/install-tools/fixincl
%{gcclibexecdir}/install-tools/mkheaders
%{gcclibexecdir}/install-tools/mkinstalldirs

%{_infodir}/gcc*
%{_infodir}/cp-*

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1

%doc ABOUT-NLS COPYING* ChangeLog* INSTALL LAST_UPDATED MAINTAINERS MD5SUMS
%doc NEWS README gcc/ABOUT-GCC-NLS gcc/BASE-VER gcc/README* gcc/COPYING*
%doc gcc/ChangeLog*

# The "cpp" files
%{_mandir}/man1/cpp.1
%{_infodir}/cpp*
%{_prefix}/bin/cpp
/usr/linux/bin/cpp
%{gcclibexecdir}/cc1

%files locale
%defattr(-,root,system)
%{_prefix}/share/locale/*

%files -n libgomp
%defattr(-,root,system)
%{gcclibdir}/libgomp.a
%{gcclibdir}/libgomp.spec
%{gcclibdir}/ppc64/libgomp.a
%{gcclibdir}/ppc64/libgomp.spec
%{gcclibdir}/pthread/libgomp.a
%{gcclibdir}/pthread/libgomp.spec
%{gcclibdir}/pthread/ppc64/libgomp.a
%{gcclibdir}/pthread/ppc64/libgomp.spec
%{gcclibdir}/include/omp.h

%{_infodir}/libgomp*

%files c++
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/libexec
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{buildhost}
%dir %{_prefix}/libexec/gcc/%{buildhost}/%{version}

%{_prefix}/bin/g++
/usr/bin/g++
%{gcclibexecdir}/cc1plus
%{_mandir}/man1/g++.1
%doc COPYING*

%files -n libgcc
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%{_prefix}/lib/gcc/%{buildhost}/%{version}/libgcc_s*.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_s*.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/libgcc_s*.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64/libgcc_s*.a
%doc COPYING.LIB

%files -n libstdc++
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64
%{gcclibdir}/libstdc++.a
%{gcclibdir}/ppc64/libstdc++.a
%{gcclibdir}/pthread/libstdc++.a
%{gcclibdir}/pthread/ppc64/libstdc++.a
%doc COPYING.LIB


%files -n libstdc++-devel
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64
%{gcclibdir}/libsupc++.a
%{gcclibdir}/ppc64/libsupc++.a
%{gcclibdir}/pthread/libsupc++.a
%{gcclibdir}/pthread/ppc64/libsupc++.a
%{gcclibdir}/include/c++
%doc COPYING*

%files java
%defattr(-,root,system)
/usr/bin/gcj
/usr/bin/gcjh
/usr/bin/jcf-dump
%{_prefix}/bin/gcj
%{_prefix}/bin/gcjh

%{_prefix}/bin/aot-compile
%{_prefix}/bin/gc-analyze
%{_prefix}/share/python/aotcompile.py
%{_prefix}/share/python/classfile.py

%{_prefix}/bin/jcf-dump
%{_mandir}/man1/gcj-dbtool.1
%{_mandir}/man1/gcj.1
%{_mandir}/man1/gcjh.1
%{_mandir}/man1/gij.1

%{_mandir}/man1/grmic.1
%{_mandir}/man1/grmiregistry.1
%{_mandir}/man1/jcf-dump.1
%{_mandir}/man1/jv-convert.1
%{_mandir}/man1/aot-compile.1
%{_mandir}/man1/gc-analyze.1

%{gcclibexecdir}/jc1
%{gcclibexecdir}/jvgenmain
%{gcclibexecdir}/ecj1

%{_infodir}/cp-tools*
%{_infodir}/gcj*


%files -n libgcj
%defattr(-,root,system)
%{_prefix}/share/java/libgcj-%{version}.jar
%{_prefix}/share/java/libgcj-tools-%{version}.jar
%{_prefix}/share/java/ecj.jar
%{gcclibdir}/libgcj-tools.a
%{gcclibdir}/libgcj.a
%{gcclibdir}/libgcj.spec
%{gcclibdir}/libgij.a

%{gcclibdir}/libgcj_bc.a
%{gcclibdir}/ppc64/libgcj_bc.a
%{gcclibdir}/pthread/libgcj_bc.a
%{gcclibdir}/pthread/ppc64/libgcj_bc.a

%{_libdir}/gcj-%{version}-%{libjavatoolversion}/libjvm.a
%{_libdir}/gcj-%{version}-%{libjavatoolversion}/libjavamath.a
%{_libdir}/gcj-%{version}-%{libjavatoolversion}/classmap.db

%{_libdir}/logging.properties
%{_libdir}/security/classpath.security

%files -n libgcj-devel
%defattr(-,root,system)

%{_libdir}/pkgconfig/libgcj-4.4.pc

%{gxxinclude}/gcj
%{gxxinclude}/gnu
%{gxxinclude}/java
%{gxxinclude}/javax
%{gxxinclude}/org
%{gcclibdir}/include/gcj
%{gcclibdir}/include/jawt.h
%{gcclibdir}/include/jawt_md.h
%{gcclibdir}/include/jni.h
%{gcclibdir}/include/jni_md.h
%{gcclibdir}/include/jvmpi.h

%files gij
%defattr(-,root,system)
/usr/bin/gappletviewer
/usr/bin/gjarsigner
/usr/bin/gkeytool
/usr/bin/grmic
/usr/bin/grmiregistry
/usr/bin/jv-convert
/usr/bin/gcj-dbtool
/usr/bin/gij
/usr/bin/gjar
/usr/bin/gjavah
/usr/bin/gnative2ascii
/usr/bin/grmid
/usr/bin/gorbd
/usr/bin/gserialver
/usr/bin/gtnameserv
/usr/bin/rebuild-gcj-db

%{_bindir}/gjar
%{_bindir}/gjavah
%{_bindir}/gnative2ascii
%{_bindir}/grmid
%{_bindir}/gorbd
%{_bindir}/gserialver
%{_bindir}/gtnameserv
%{_bindir}/rebuild-gcj-db
%{_bindir}/gappletviewer
%{_bindir}/gjarsigner
%{_bindir}/gkeytool
%{_bindir}/grmic
%{_bindir}/grmiregistry
%{_bindir}/jv-convert
%{_bindir}/gcj-dbtool
%{_bindir}/gij

%{_mandir}/man1/gappletviewer.1
%{_mandir}/man1/gjar.1
%{_mandir}/man1/gjarsigner.1
%{_mandir}/man1/gjavah.1
%{_mandir}/man1/gjdoc.1
%{_mandir}/man1/gkeytool.1
%{_mandir}/man1/gnative2ascii.1
%{_mandir}/man1/gorbd.1
%{_mandir}/man1/grmid.1
%{_mandir}/man1/gserialver.1
%{_mandir}/man1/gtnameserv.1
%{_mandir}/man1/rebuild-gcj-db.1

%files -n libffi
%defattr(-,root,system)
%{_libdir}/libffi.a

%files -n libffi-devel
%defattr(-,root,system)
%{gcclibdir}/include/ffi.h
%{gcclibdir}/include/ffitarget.h

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Tue Apr 12 2011 BULL Patricia Cugny <patricia.cugny@bull.net> 4.4.5-1
- Update to version 4.4.5
- add Eclipse Java compiler as source file (see contrib/download_ecj script)

* Fri Jul 24 2009 BULL <jean-noel.cordenner@bull.net> 4.4.0-1
- Update to version 4.4.0

* Sat Mar  1 2008 BULL 4.2.0-3
- Add libgcj, gij, libffi

* Fri Feb 15 2008 BULL 4.2.0-2
- Add locale package
- Add a separate package for libgomp
- Add gcj

* Thu Feb 14 2008 BULL 4.2.0-1
- Update to version 4.2.0

* Thu Oct 13 2005 Reza Arbab <arbab@austin.ibm.com> 4.0.0-1
- Update to version 4.0.0.

* Thu Feb 10 2005 David Clissold <cliss@austin.ibm.com> 3.3.2-5
- Get rid of --disable-shared.  Split libgcc, libstdc++, libstdc++-devel
- into separate packages, like on Linux.

* Tue Oct 26 2004 David Clissold <cliss@austin.ibm.com> 3.3.2-4
- Change gcc-c++ so that it "Obsoletes" g++.  Will allow direct update
- from the GNUPro gcc and g++ to the newer gcc and gcc-c++.
- Rebuild with newer binutils installed (using AIX's ranlib).

* Tue Sep 21 2004 David Clissold <cliss@austin.ibm.com> 3.3.2-3
- Update the OS-level if statements to include aix5.3.
- Build using bash, to make it faster (build takes a long time).

* Wed Nov 19 2003 Philip K. Warren <pkw@us.ibm.com> 3.3.2-2
- Update file list to include all directories.
- Added patch to build libgcc.a without debugging symbols.
- Add conflict with older GNUPro images.
- Add links in /usr/bin.

* Tue Nov 18 2003 Philip K. Warren <pkw@us.ibm.com> 3.3.2-1
- Initial release of GCC 3.3.2 for AIX.
