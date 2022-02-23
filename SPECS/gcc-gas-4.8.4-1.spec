Summary: GNU Compiler Collection
Name: gcc-gas
Version: 4.8.4
Release: 1
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source0: ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2.sig

%define _prefix /opt/freeware/gcc-gas

# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: /opt/tmp/%{name}-%{version}-root

BuildRequires: bash, sed, automake, autoconf, texinfo, make, tar, gcc
BuildRequires: gmp-devel >= 4.3.2, mpfr-devel >= 2.4.2, libmpc-devel >= 0.8.1
BuildRequires: zlib-devel >= 1.2.3-3
Requires: info
Prereq: /sbin/install-info
Requires: libgcc = %{version}-%{release}
Requires: gcc-cpp = %{version}-%{release}
Conflicts: g++ <= 2.9.aix51.020209-4

%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%define _libdir64 %{_prefix}/lib64
%define gcclibdir %{_libdir}/gcc/%{buildhost}/%{version}
%define gcclibexecdir %{_libexecdir}/gcc/%{buildhost}/%{version}

%description
The gcc-gas package is a new GCC with Gnu Assembler Support. It contains the GNU Compiler
Collection version %{version}.

Using this GCC you will be able to compile source code with in line assembler code (C code
 that generate GNU Assembler code).

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
Requires: zlib >= 1.2.3-3
Obsoletes: g++
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
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
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
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


%package -n libgcc-gas
Summary: GCC version %{version} shared support library
Group: Development/Libraries
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description -n libgcc-gas
This package contains GCC shared support library which is needed
e.g. for exception handling support.


%package -n libstdc++-gas
Summary: GNU Standard C++ Library
Group: Development/Libraries
Requires: libgcc
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description -n libstdc++-gas
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.


%package -n libstdc++-gas-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
Requires: libstdc++-gas
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description -n libstdc++-gas-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes a rewritten implementation of STL.


%package gfortran
Summary: Fortran 95 support
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
Requires: zlib >= 1.2.3-3
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description gfortran
The gcc-gfortran package provides support for compiling Fortran 95
programs with the GNU Compiler Collection.


%package -n libgomp-gas
Summary: GCC OpenMP 2.5 shared support library
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description -n libgomp-gas
This package contains GCC shared support library which is needed
for OpenMP 2.5 support.


%prep
#export PATH=/opt/freeware/bin:$PATH
%setup -q -n gcc-%{version}
%ifos aix5.1
%patch1
%endif
%ifos aix5.2
%patch2
%endif


%build
# speed up the configure processes...
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"

# use maximum amount of memory (heap) available to 32-bit programs 
# seems not to be taken into account though
export LDR_CNTRL=MAXDATA=0x80000000


cd ..
rm -rf gcc-gas-build-%{version}
mkdir gcc-gas-build-%{version}
cd gcc-gas-build-%{version}
CC="/opt/hamza/build.gcc.4.8.4/bin/gcc -std=gnu99" \
CXX="/opt/hamza/build.gcc.4.8.4/bin/g++" \
BOOT_CFLAGS='-O2 -I/opt/freeware/include' \
CFLAGS='-O2 -mpowerpc -mno-mfcrf -mtune=power6 -I/opt/freeware/include' \
CXXFLAGS='-O2 -mpowerpc -mno-mfcrf -mtune=power6 -I/opt/freeware/include' \
LIBCFLAGS='-O2 -I/opt/freeware/include' \
LIBCXXFLAGS='-O2 -I/opt/freeware/include -fno-implicit-templates' \
LDFLAGS="-L/opt/freeware/lib -Wl,-bbigtoc -Wl,-blibpath:/opt/freeware/lib/gcc/%{buildhost}/%{version}:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000" \
../gcc-%{version}/configure \
--with-as=/opt/damien/apps/bin/as  \
--enable-languages="c,c++" \
--prefix=%{_prefix} \
--mandir=%{_mandir} \
--infodir=%{_infodir} \
--enable-version-specific-runtime-libs \
--disable-nls \
--enable-decimal-float=dpd \
--host=%{buildhost}

ulimit -d unlimited
ulimit -s unlimited
gmake -j 4 \
    BOOT_CFLAGS='-O2 -I/opt/freeware/include' \
    CFLAGS='-O2 -mpowerpc -mno-mfcrf -mtune=power6 -I/opt/freeware/include' \
    CXXFLAGS='-O2 -mpowerpc -mno-mfcrf -mtune=power6 -I/opt/freeware/include' \
    LIBCFLAGS='-O2 -I/opt/freeware/include' \
    LIBCXXFLAGS='-O2 -I/opt/freeware/include -fno-implicit-templates' \
    LDFLAGS="-L/opt/freeware/lib -Wl,-bbigtoc -Wl,-blibpath:/opt/freeware/lib/gcc/%{buildhost}/%{version}:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000" \
    bootstrap-lean

# remove the "-print-multi-os-directory" flag...
sed -e "s/MULTIOSDIR = \`\$(CC) \$(LIBCFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
mv -f Makefile.tmp libiberty/Makefile


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd ../gcc-gas-build-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

# strip compiler binaries
strip ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :
for file in cc1 cc1plus collect2 f951 lto-wrapper ; do
    strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/$file 2>/dev/null || :
done

# strip utilities
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/fixincl 2>/dev/null || :
strip ${RPM_BUILD_ROOT}%{_libdir}/gcc/%{buildhost}/%{version}/install-tools/fixincl 2>/dev/null || :

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
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    if [[ "`/usr/bin/file ${f} | awk '{ print $2 }'`" = "executable" ]] ; then
        /usr/bin/echo '\0200\0\0\0' | /usr/bin/dd of=${f} bs=4 count=1 seek=19 conv=notrunc
    fi
done

# create links in /usr/bin
(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/bin/gcc-gas
    cd usr/bin/gcc-gas
    for f in c++ \
             cpp \
             g++ \
             gcc \
             gcov \
             gfortran \
             %{buildhost}-c++ \
             %{buildhost}-g++ \
             %{buildhost}-gcc \
             %{buildhost}-gcc-%{version} \
             %{buildhost}-gfortran \
             %{buildhost}-gcc-ar \
             %{buildhost}-gcc-nm \
             %{buildhost}-gcc-ranlib ; do
        ln -sf ../../..%{_bindir}/$f .
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

# add compatibility symbolic links
(
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -sf gcc/%{buildhost}/%{version}/libatomic.a .
    ln -sf gcc/%{buildhost}/%{version}/libgcc_s.a .
    ln -sf gcc/%{buildhost}/%{version}/libgfortran.a .
    ln -sf gcc/%{buildhost}/%{version}/libgomp.a .
    ln -sf gcc/%{buildhost}/%{version}/libstdc++.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/gcc/%{buildhost}/%{version}/ppc64/libatomic.a .
    ln -sf ../lib/gcc/%{buildhost}/%{version}/ppc64/libgcc_s.a .
    ln -sf ../lib/gcc/%{buildhost}/%{version}/ppc64/libgfortran.a .
    ln -sf ../lib/gcc/%{buildhost}/%{version}/ppc64/libgomp.a .
    ln -sf ../lib/gcc/%{buildhost}/%{version}/ppc64/libstdc++.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread
    ln -sf ../gcc/%{buildhost}/%{version}/pthread/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{version}/pthread/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{version}/pthread/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{version}/pthread/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{version}/pthread/libstdc++.a .

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/ppc64/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/ppc64/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.a .

%ifos aix5.1
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/power
    cd ${RPM_BUILD_ROOT}%{_libdir}/power
    ln -sf ../gcc/%{buildhost}/%{version}/power/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{version}/power/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{version}/power/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{version}/power/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{version}/power/libstdc++.a .
    
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/powerpc
    cd ${RPM_BUILD_ROOT}%{_libdir}/powerpc
    ln -sf ../gcc/%{buildhost}/%{version}/powerpc/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{version}/powerpc/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{version}/powerpc/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{version}/powerpc/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{version}/powerpc/libstdc++.a .
    
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/power
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/power
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/power/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/power/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/power/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/power/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/power/libstdc++.a .
    
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/powerpc
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/powerpc
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/powerpc/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/powerpc/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{version}/pthread/powerpc/libstdc++.a .
%endif
)


%post 
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccinstall.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gccint.info.gz %{_infodir}/dir || :

%post -n libgomp-gas
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

%preun -n libgomp-gas
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
%{_bindir}/%{buildhost}-gcc-%{version}
%{_bindir}/%{buildhost}-gcc-ar
%{_bindir}/%{buildhost}-gcc-nm
%{_bindir}/%{buildhost}-gcc-ranlib
/usr/bin/gcc-gas/gcc
/usr/bin/gcc-gas/gcov
/usr/bin/gcc-gas/%{buildhost}-gcc
/usr/bin/gcc-gas/%{buildhost}-gcc-%{version}
/usr/bin/gcc-gas/%{buildhost}-gcc-ar
/usr/bin/gcc-gas/%{buildhost}-gcc-nm
/usr/bin/gcc-gas/%{buildhost}-gcc-ranlib
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/libgcov.a
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgcov.a
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcov.a
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcov.a
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/crtcxa*o
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcov.a

%{_libexecdir}/gcc/%{buildhost}/%{version}/collect2
%{_libexecdir}/gcc/%{buildhost}/%{version}/lto-wrapper

%dir %{_libdir}/gcc/%{buildhost}/%{version}/include
%{_libdir}/gcc/%{buildhost}/%{version}/include/[^c++]*
%{_libdir}/gcc/%{buildhost}/%{version}/include-fixed

%{_libdir}/gcc/%{buildhost}/%{version}/install-tools

%{_infodir}/gcc*

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1
%doc gcc/COPYING* MAINTAINERS gcc/README* 


%files cpp 
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{version}
%{_bindir}/cpp
/usr/bin/gcc-gas/cpp
%{_libexecdir}/gcc/%{buildhost}/%{version}/cc1
%{_mandir}/man1/cpp.1
%{_infodir}/cpp*


%files -n libgomp-gas
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/libgomp.spec
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgomp.spec
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgomp.spec
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgomp.spec
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgomp.spec
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgomp.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgomp.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgomp.spec
%{_libdir}/libgomp.a
%{_libdir64}/libgomp.a
%{_libdir}/pthread/libgomp.a
%{_libdir}/pthread/ppc64/libgomp.a
%ifos aix5.1
%{_libdir}/power/libgomp.a
%{_libdir}/powerpc/libgomp.a
%{_libdir}/pthread/power/libgomp.a
%{_libdir}/pthread/powerpc/libgomp.a
%endif
%{_infodir}/libgomp*


%files c++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_bindir}/c++
%{_bindir}/g++
%{_bindir}/%{buildhost}-c++
%{_bindir}/%{buildhost}-g++
/usr/bin/gcc-gas/c++
/usr/bin/gcc-gas/g++
/usr/bin/gcc-gas/%{buildhost}-c++
/usr/bin/gcc-gas/%{buildhost}-g++
%dir %{_libexecdir}/gcc
%dir %{_libexecdir}/gcc/%{buildhost}
%dir %{_libexecdir}/gcc/%{buildhost}/%{version}
%{_libexecdir}/gcc/%{buildhost}/%{version}/cc1plus
%{_mandir}/man1/g++.1
%doc gcc/COPYING*


%files -n libgcc-gas
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/libatomic.*
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/power/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libatomic.*
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libatomic.*
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libatomic.*
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libatomic.*
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libatomic.*
%{_libdir}/libgcc_s.a
%{_libdir}/libatomic.a
%{_libdir64}/libgcc_s.a
%{_libdir64}/libatomic.a
%{_libdir}/pthread/libgcc_s.a
%{_libdir}/pthread/libatomic.a
%{_libdir}/pthread/ppc64/libgcc_s.a
%{_libdir}/pthread/ppc64/libatomic.a
%ifos aix5.1
%{_libdir}/power/libgcc_s.a
%{_libdir}/power/libatomic.a
%{_libdir}/powerpc/libgcc_s.a
%{_libdir}/powerpc/libatomic.a
%{_libdir}/pthread/power/libgcc_s.a
%{_libdir}/pthread/power/libatomic.a
%{_libdir}/pthread/powerpc/libgcc_s.a
%{_libdir}/pthread/powerpc/libatomic.a
%endif
%doc gcc/COPYING*


%files -n libstdc++-gas
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libstdc++.a
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libstdc++.a
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libstdc++.a
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libstdc++.a
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.a
%{_libdir}/libstdc++.a
%{_libdir64}/libstdc++.a
%{_libdir}/pthread/libstdc++.a
%{_libdir}/pthread/ppc64/libstdc++.a
%ifos aix5.1
%{_libdir}/power/libstdc++.a
%{_libdir}/powerpc/libstdc++.a
%{_libdir}/pthread/power/libstdc++.a
%{_libdir}/pthread/powerpc/libstdc++.a
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/libstdc++.a-gdb.py
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libstdc++.a-gdb.py
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libstdc++.a-gdb.py
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libstdc++.a-gdb.py
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libstdc++.a-gdb.py
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.a-gdb.py
%dir %{_datadir}/gcc-%{version}
%dir %{_datadir}/gcc-%{version}/python
%{_datadir}/gcc-%{version}/python/libstdcxx
%doc gcc/COPYING*


%files -n libstdc++-gas-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%ifos aix5.1
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
%endif
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/libsupc++.la
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/power/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/power/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/power/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libsupc++.la
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libsupc++.la
%ifos aix5.1
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libsupc++.la
%endif
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/include/c++
%doc gcc/COPYING*


#%files gfortran
#%defattr(-,root,system)
#%dir %{_libdir}/gcc
#%dir %{_libdir}/gcc/%{buildhost}
#%dir %{_libdir}/gcc/%{buildhost}/%{version}
#%ifos aix5.1
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/power
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/powerpc
#%endif
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
#%ifos aix5.1
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/power
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc
#%endif
#%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
#%{_bindir}/gfortran
#%{_bindir}/%{buildhost}-gfortran
#/usr/bin/gfortran
#/usr/bin/%{buildhost}-gfortran
#%{_libdir}/gcc/%{buildhost}/%{version}/finclude
#%{_libdir}/gcc/%{buildhost}/%{version}/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/libgfortranbegin.la
#%ifos aix5.1
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/power/libgfortranbegin.la
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/powerpc/libgfortranbegin.la
#%endif
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgfortranbegin.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgfortranbegin.la
#%ifos aix5.1
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/power/libgfortranbegin.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/powerpc/libgfortranbegin.la
#%endif
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortran.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortran.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortran.spec
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libcaf_single.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libcaf_single.la
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortranbegin.a
#%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgfortranbegin.la
#%{_libdir}/libgfortran.a
#%{_libdir64}/libgfortran.a
#%{_libdir}/pthread/libgfortran.a
#%{_libdir}/pthread/ppc64/libgfortran.a
#%ifos aix5.1
#%{_libdir}/power/libgfortran.a
#%{_libdir}/powerpc/libgfortran.a
#%{_libdir}/pthread/power/libgfortran.a
#%{_libdir}/pthread/powerpc/libgfortran.a
#%endif
#%{_libexecdir}/gcc/%{buildhost}/%{version}/f951
#%{_infodir}/gfortran.info.gz
#%{_mandir}/man1/gfortran.1
#%doc gcc/COPYING*


%changelog
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
