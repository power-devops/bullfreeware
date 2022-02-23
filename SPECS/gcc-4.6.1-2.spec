Summary: GNU Compiler Collection
Name: gcc
Version: 4.6.1
Release: 2
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-core-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-g++-%{version}.tar.bz2
Patch1: gcc-4.6.1-aix.patch

# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: bash, sed, automake, autoconf, texinfo, make, tar
BuildRequires: gmp-devel >= 4.3.2, mpfr-devel >= 2.4.2, libmpc-devel >= 0.8.1
Requires: info
Prereq: /sbin/install-info
Requires: libgcc = %{version}-%{release}
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
Requires: gmp >= 4.3.2, mpfr >= 2.4.2, libmpc >= 0.8.1
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

%prep
%setup -q -b 1
%patch1 -p1 -b .aix

%build
# Boost configure speed by a factor of 10:
# ksh creates all pipes, redirections, etc in /tmp
# whereas bash uses memory
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export LIBPATH="/opt/freeware/lib:/usr/lib/$LIBPATH"

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"

# use maximum amount of memory (heap) available to 32-bit programs
export LDR_CNTRL=MAXDATA=0x80000000

rm -rf objdir
mkdir objdir
cd objdir

CC="/usr/vac/bin/cc" \
BOOT_CFLAGS='-O2 -I/opt/freeware/include' \
CFLAGS='-O2 -I/opt/freeware/include' \
CXXFLAGS='-O2 -I/opt/freeware/include' \
LIBCFLAGS='-O2 -I/opt/freeware/include' \
LIBCXXFLAGS='-O2 -I/opt/freeware/include -fno-implicit-templates' \
LDFLAGS="-L/opt/freeware/lib -Wl,-bbigtoc -Wl,-blibpath:/opt/freeware/lib/gcc/%{buildhost}/%{version}:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000" \
../configure \
--with-as=/usr/bin/as \
--with-ld=/usr/bin/ld \
--enable-languages=c,c++ \
--prefix=%{_prefix} \
--infodir=%{_infodir} \
--mandir=%{_mandir} \
--enable-threads \
--enable-version-specific-runtime-libs \
--build=%{buildhost} \
--host=%{buildhost} \
--target=%{buildhost} 

ulimit -d unlimited
ulimit -s unlimited


gmake  \
    BOOT_CFLAGS='-O2 -I/opt/freeware/include' \
    CFLAGS='-O2 -I/opt/freeware/include' \
    CXXFLAGS='-O2 -I/opt/freeware/include' \
    LIBCFLAGS='-O2 -I/opt/freeware/include' \
    LIBCXXFLAGS='-O2 -I/opt/freeware/include -fno-implicit-templates' \
    LDFLAGS="-L/opt/freeware/lib -Wl,-bbigtoc -Wl,-blibpath:/opt/freeware/lib/gcc/%{buildhost}/%{version}:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000" \
    bootstrap-lean



%install
# Boost configure speed by a factor of 10:
# ksh creates all pipes, redirections, etc in /tmp
# whereas bash uses memory
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash


[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd objdir
gmake install DESTDIR=${RPM_BUILD_ROOT}

# Strip compiler binaries
strip ${RPM_BUILD_ROOT}%{_bindir}/* 2>/dev/null || :
for file in cc1 cc1plus collect2 lto-wrapper; do
  strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/$file 2>/dev/null || :
done

# Strip utilities
strip ${RPM_BUILD_ROOT}%{gcclibexecdir}/install-tools/fixincl 2>/dev/null || :

# remove libiberty.a library which is not used directly by gcc
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty.a
for dir in power powerpc ppc64 pthread; do
    rm -rf ${RPM_BUILD_ROOT}%{_libdir}/$dir
done

# remove empty include directory
rmdir ${RPM_BUILD_ROOT}%{_includedir} || :

# Gzip info pages
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info

# Create links in /usr/bin
(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/bin
    cd usr/bin
    for fname in c++ g++ gcc gcov \
	%{buildhost}-c++ %{buildhost}-g++ \
 	%{buildhost}-gcc %{buildhost}-gcc-%{version}; do
        ln -sf ../..%{_bindir}/$fname .
    done
)


(
    cd ${RPM_BUILD_ROOT}
    mkdir -p usr/linux/bin
    cd usr/linux/bin
    ln -sf ../..%{_prefix}/bin/cpp .
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
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -sf gcc/%{buildhost}/%{version}/libgcc_s.a .
    ln -sf gcc/%{buildhost}/%{version}/libgomp.a .
    ln -sf gcc/%{buildhost}/%{version}/libstdc++.a .
    ln -sf gcc/%{buildhost}/%{version}/libsupc++.a .
)  


%post
/sbin/install-info %{_infodir}/cpp.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/cppinternals.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gcc.info.gz %{_infodir}/dir  || :
/sbin/install-info %{_infodir}/gccint.info.gz %{_infodir}/dir  || :
/sbin/install-info %{_infodir}/gccinstall.info.gz %{_infodir}/dir  || :

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

%preun -n libgomp
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libgomp.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_bindir}/gcc
%{_bindir}/gcov
%{_bindir}/%{buildhost}-gcc
%{_bindir}/%{buildhost}-gcc-%{version}
/usr/bin/gcc
/usr/bin/gcov
/usr/bin/%{buildhost}-gcc
/usr/bin/%{buildhost}-gcc-%{version}
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcov.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_eh.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcov.a

%{_libexecdir}/gcc/%{buildhost}/%{version}/collect2
%{_libexecdir}/gcc/%{buildhost}/%{version}/lto-wrapper

%dir %{_libdir}/gcc/%{buildhost}/%{version}/include
%{_libdir}/gcc/%{buildhost}/%{version}/include/[^c++]*
%{_libdir}/gcc/%{buildhost}/%{version}/include-fixed/*.h
%{_libdir}/gcc/%{buildhost}/%{version}/include-fixed/README
%dir %{_libdir}/gcc/%{buildhost}/%{version}/install-tools

%{_infodir}/gcc*

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1

%doc gcc/COPYING* MAINTAINERS gcc/README*

# The "cpp" files
%{_bindir}/cpp
/usr/linux/bin/cpp
%{gcclibexecdir}/cc1
%{_mandir}/man1/cpp.1
%{_infodir}/cpp*

%files locale
%defattr(-,root,system)
%{_prefix}/share/locale/*

%files -n libgomp
%defattr(-,root,system)
%{gcclibdir}/libgomp.a
%{gcclibdir}/libgomp.la
%{gcclibdir}/libgomp.spec
%{gcclibdir}/ppc64/libgomp.a
%{gcclibdir}/ppc64/libgomp.la
%{gcclibdir}/ppc64/libgomp.spec
%{gcclibdir}/pthread/libgomp.a
%{gcclibdir}/pthread/libgomp.la
%{gcclibdir}/pthread/libgomp.spec
%{gcclibdir}/pthread/ppc64/libgomp.a
%{gcclibdir}/pthread/ppc64/libgomp.la
%{gcclibdir}/pthread/ppc64/libgomp.spec
%{_libdir}/libgomp.a 
%{gcclibdir}/include/omp.h
%{_infodir}/libgomp*

%files c++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64

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
%dir %{_libexecdir}/gcc/%{buildhost}/%{version}
%{_libexecdir}/gcc/%{buildhost}/%{version}/cc1plus
%{_mandir}/man1/g++.1
%doc gcc/COPYING*

%files -n libgcc
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libgcc_s.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_s.a
%{_libdir}/libgcc_s.a
%doc gcc/COPYING*

%files -n libstdc++
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libstdc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.a
%{_libdir}/libstdc++.a
%doc gcc/COPYING*

%files -n libstdc++-devel
%defattr(-,root,system)
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{buildhost}
%dir %{_libdir}/gcc/%{buildhost}/%{version}
%dir %{_libdir}/gcc/%{buildhost}/%{version}/ppc64
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread
%dir %{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64
%{_libdir}/gcc/%{buildhost}/%{version}/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libsupc++.a
%{_libdir}/gcc/%{buildhost}/%{version}/pthread/ppc64/libsupc++.la
%{_libdir}/gcc/%{buildhost}/%{version}/include/c++
%{_libdir}/libsupc++.a
%doc gcc/COPYING*

%changelog
* Tue Oct 15 2013 BULL Gerard Visiedo <gerard.visiedo@bull.net>  4.6.1-2
- Rebuilt with XLC V12

* Thu Oct 13 2011 BULL Patricia Cugny <patricia.cugny@bull.net>  4.6.1-1
- Update to version 4.6.1 - languages C and C++

* Tue Apr 19 2011 BULL Patricia Cugny <patricia.cugny@bull.net> 4.5.2-1
- Update to version 4.5.2

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
