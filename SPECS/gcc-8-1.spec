# GCC package is now a metapackage only using requirements towards a
# specific gcc version (eg gcc9 RPMS).

# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default on aix 7.1 and 7.2, gccgo is built.
# No gccgo: rpmbuild -ba --without build_go *.spec
%ifos aix7.1 aix7.2
%bcond_without build_go
%endif

# By default, objectif-C isn't made
# To build objectif-c: rpmbuild -ba --with objc *.spec
%bcond_with build_objc

%define _libdir64 %{_prefix}/lib64

%define gcc_major 8

Summary: GNU Compiler Collection
Name: gcc
Version: %{gcc_major}
Release: 1
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source1000: %{name}-%{version}-%{release}.build.log

# BullFreeware has already a gcc-9. But we are moving back
# to gcc 8 by default as gcc9 package is now available.
Epoch: 1

%define full_version %{epoch}:%{version}-%{release}

Requires: libgcc = %{full_version}
Requires: gcc-cpp = %{full_version}
Requires: gcc%{gcc_major}
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


%description
The gcc package contains the GNU Compiler Collection version %{gcc_major}.
You will need this package in order to compile C code.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: %{name} = %{full_version}
Requires: gcc%{gcc_major}-c++
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
Requires: gcc%{gcc_major}-cpp
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
Summary: GCC version %{gcc_major} shared support library
Group: Development/Libraries
Requires: libgcc%{gcc_major}
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
Requires: libgcc = %{full_version}
Requires: libstdc++%{gcc_major}
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
Requires: libstdc++ = %{full_version}
Requires: libstdc++%{gcc_major}-devel
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
Requires: %{name} = %{full_version}
Requires: gcc%{gcc_major}-gfortran
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
Requires: %{name} = %{full_version}
Requires: libgomp%{gcc_major}
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


%if %{with build_objc}

# TODO: port not yet done

%package objc
Summary: Objective-C support for GCC
Group: Development/Languages
Requires: %{name} = %{full_version}
Requires: libobjc = %{full_version}
Requires: gcc%{gcc_major}-objc
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
Requires: gcc-c++  = %{full_version}
Requires: gcc-objc = %{full_version}
Requires: gcc%{gcc_major}-objc++
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
Requires: libobjc%{gcc_major}
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

%endif

%if %{with build_go}

%package go
Summary: Go support
Group: Development/Languages
Requires: gcc = %{full_version}
Requires: libgo = %{full_version}
Requires: libgo-devel = %{full_version}
Requires: gcc%{gcc_major}-go


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

%package -n libgo
Summary: Go runtime
Group: System Environment/Libraries
Requires: libgo%{gcc_major}

%description -n libgo
Objects (.o), shared-objects (.so), and archives (.a) built from .go code
should be rebuilt when a new version of GCC Go is available.

This package contains a Go shared library which is needed to run
Go dynamically linked programs.


%package -n libgo-devel
Summary: Go development libraries
Group: Development/Languages
Requires: libgo = %{full_version}
Requires: libgo%{gcc_major}-devel

%description -n libgo-devel
This package includes libraries and support files for compiling Go programs.

# Also on AIX ?????
#	%package -n libgo-static
#	Summary: Static Go libraries
#	Group: Development/Libraries
#	Requires: libgo = %{full_version}
#	Requires: gcc = %{full_version}
#	
#	%description -n libgo-static
#	This package contains static Go libraries.


%endif


%prep
# NOTHING TO DO

%build
# NOTHING TO DO

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_infodir}

# create links for binaries
(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in c++ \
             cpp \
             g++ \
             gcc \
             gcc-ar \
             gcc-nm \
             gcc-ranlib \
%if %{with build_go}
             gccgo \
             go.gcc \
             gofmt.gcc \
%endif
             gcov \
			 gcov-tool \
			 gcov-dump \
             gfortran \
             %{buildhost}-c++ \
             %{buildhost}-g++ \
             %{buildhost}-gcc \
             %{buildhost}-gfortran \
             %{buildhost}-gcc-ar \
             %{buildhost}-gcc-nm \
             %{buildhost}-gcc-ranlib ; do
        ln -sf ${f}-%{gcc_major} ${f}
    done
)

# Link man pages
(
	mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
	cd $RPM_BUILD_ROOT%{_mandir}/man1
	for man1 in gcc \
				gcov \
				gcov-dump \
				gcov-tool \
				g++ \
				cpp \
				gfortran \
%if %{with build_go}
				go \
				gofmt \
				gccgo \
%endif
				;do
		ln -sf $man1-%{gcc_major}.1 $man1.1
	done

)

# Link info
(
	cd $RPM_BUILD_ROOT%{_infodir}
	for info in gcc \
				gccinstall \
				gccint \
				libgomp \
				cpp \
				cppinternals \
				gfortran \
%if %{with build_go}
				gccgo \
%endif
				;do
		ln -sf $info-%{gcc_major}.info.gz $info.info.gz
	done

)


# Add compatibility symbolic links
(
    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ln -sf gcc/%{buildhost}/%{gcc_major}/libatomic.a .
    ln -sf gcc/%{buildhost}/%{gcc_major}/libgcc_s.a .
    ln -sf gcc/%{buildhost}/%{gcc_major}/libgfortran.a .
    ln -sf gcc/%{buildhost}/%{gcc_major}/libgomp.a .
    ln -sf gcc/%{buildhost}/%{gcc_major}/libstdc++.a .
%if %{with build_go}
    ln -sf gcc/%{buildhost}/%{gcc_major}/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libatomic.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libgcc_s.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libgfortran.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libgomp.a .
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libstdc++.a .
%if %{with build_go}
    ln -sf ../lib/gcc/%{buildhost}/%{gcc_major}/ppc64/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libatomic.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libgcc_s.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libgfortran.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libgomp.a .
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libstdc++.a .
%if %{with build_go}
    ln -sf ../gcc/%{buildhost}/%{gcc_major}/pthread/libgo.a .
%endif

    mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    cd ${RPM_BUILD_ROOT}%{_libdir}/pthread/ppc64
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libatomic.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgcc_s.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgfortran.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgomp.a .
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libstdc++.a .
%if %{with build_go}
    ln -sf ../../gcc/%{buildhost}/%{gcc_major}/pthread/ppc64/libgo.a .
%endif
)


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


%if %{with build_go}

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

%if %{with build_go}

%preun go
# Remove links to binaries if they're pointing to this RPM binaries
if ls -l %{_bindir}/go 2>/dev/null | grep -q '.gcc'; then
	rm %{_bindir}/go
fi
if ls -l %{_bindir}/gofmt 2>/dev/null | grep -q '.gcc'; then
	rm %{_bindir}/gofmt
fi

%endif

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# No tests at the moment.

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/gcc
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/gcov
%{_bindir}/gcov-tool
%{_bindir}/gcov-dump
%{_bindir}/%{buildhost}-gcc
%{_bindir}/%{buildhost}-gcc-ar
%{_bindir}/%{buildhost}-gcc-nm
%{_bindir}/%{buildhost}-gcc-ranlib
%{_infodir}/gcc*

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1


%files cpp
%defattr(-,root,system)
%{_bindir}/cpp
%{_mandir}/man1/cpp.1
%{_infodir}/cpp*


%files c++
%defattr(-,root,system)
%{_bindir}/c++
%{_bindir}/g++
%{_bindir}/%{buildhost}-c++
%{_bindir}/%{buildhost}-g++
%{_mandir}/man1/g++.1


%files -n libgcc
%defattr(-,root,system)
%{_libdir}/libgcc_s.a
%{_libdir}/libatomic.a
%{_libdir64}/libgcc_s.a
%{_libdir64}/libatomic.a
%{_libdir}/pthread/libgcc_s.a
%{_libdir}/pthread/libatomic.a
%{_libdir}/pthread/ppc64/libgcc_s.a
%{_libdir}/pthread/ppc64/libatomic.a


%files -n libstdc++
%defattr(-,root,system)
%{_libdir}/libstdc++.a
%{_libdir64}/libstdc++.a
%{_libdir}/pthread/libstdc++.a
%{_libdir}/pthread/ppc64/libstdc++.a


%files -n libstdc++-devel
# Empty


%files -n libgomp
%defattr(-,root,system)
%{_libdir}/libgomp.a
%{_libdir64}/libgomp.a
%{_libdir}/pthread/libgomp.a
%{_libdir}/pthread/ppc64/libgomp.a
%{_infodir}/libgomp*


%files gfortran
%defattr(-,root,system)
%{_bindir}/gfortran
%{_bindir}/%{buildhost}-gfortran
%{_libdir}/libgfortran.a
%{_libdir64}/libgfortran.a
%{_libdir}/pthread/libgfortran.a
%{_libdir}/pthread/ppc64/libgfortran.a
%{_infodir}/gfortran.info.gz
%{_mandir}/man1/gfortran.1


%if %{with build_objc}
%files objc
%defattr(-,root,system)
%{_libdir}/libobjc.a
%{_libdir64}/libobjc.a
%{_libdir}/pthread/libobjc.a
%{_libdir}/pthread/ppc64/libobjc.a
%endif

%if %{with build_go}

%files go
%defattr(-,root,system)
%{_bindir}/go.gcc
%{_bindir}/gccgo
%{_bindir}/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*

%files -n libgo
%defattr(-,root,system)
%{_libdir}/libgo.a

%files -n libgo-devel
%defattr(-,root,system)
# Empty

%endif


%changelog
* Wed Mar 11 2020 Clément Chigot <clement.chigot@atos.net> - 8-1
- Rework gcc default package to handle multi-gcc support.
  Gcc is now a metapackage having requirements over gccX RPMS,
  with X the current major version (currently 8).
  The version of this package is only the major version of gcc,
  which is becoming the default one on AIX.
  Minor versions are handled by gccX packages.

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
