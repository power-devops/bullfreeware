Summary: GNU Compiler Collection
Name: gcc
Version: 4.2.0
Release: 1
Group: Development/Tools
License: GPL
URL: http://gcc.gnu.org/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-core-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}/%{name}-g++-%{version}.tar.bz2
Patch0: gcc-4.2.0.aix6.1.patch
# Unless you have a lot of space in /var/tmp, you will probably need to
# specify --buildroot on the command line to point to a larger filesystem.
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: sed, automake, libtool, autoconf, texinfo
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
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
Requires: AIX-rpm >= 6.1.0.0
%endif
%define gcclibdir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%define gcclibexecdir %{_prefix}/libexec/gcc/%{buildhost}/%{version}

%description
The gcc package includes the gcc GNU compiler for compiling C code.

%package c++
Summary: C++ support for GCC
Group: Development/Languages
Requires: gcc = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Obsoletes: g++
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%endif

%description c++
The gcc-c++ package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and exception
handling. The static standard C++ library and C++ header files are included.

%package -n libgcc
Summary: GCC compiler dynamic runtime library
Group: Development/Libraries
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%endif

%description -n libgcc
libgcc is required at runtime for programs dynamically linked with GCC.

%package -n libstdc++
Summary: G++ compiler dynamic runtime library
Group: Development/Libraries
Requires: libgcc
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%endif

%description -n libstdc++
libstdc++ is required at runtime for programs dynamically linked with G++.

%package -n libstdc++-devel
Summary: Include files and libraries required for G++ development.
Group: Development/Libraries
Requires: libstdc++
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%endif

%description -n libstdc++-devel
This package contains headers and libraries for the GNU G++ library.
Required for compiling G++ code.


%prep
%setup -q
%patch0

%build
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export SHELL=/opt/freeware/bin/bash

rm -rf objdir
mkdir objdir
cd objdir

CFLAGS="-g" LIBCFLAGS="-g" AR_FLAGS="-X32_64 cru" \
../configure --with-as=/usr/bin/as --with-ld=/usr/bin/ld --prefix=%{_prefix} --host=%{buildhost}

ulimit -d unlimited
ulimit -s unlimited
make

%install
# Seems to help build faster, using bash
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
cd objdir
gmake install DESTDIR=$RPM_BUILD_ROOT

# Remove unneeded links in bin/
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/c++*
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/powerpc*

# Don't need to ship gccbug
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/gccbug

# Strip compiler binaries
strip $RPM_BUILD_ROOT%{_prefix}/bin/* 2>/dev/null || :
for file in cc1 cc1plus collect2; do
  strip $RPM_BUILD_ROOT%{gcclibexecdir}/$file 2>/dev/null || :
done

# Strip utilities
strip $RPM_BUILD_ROOT%{gcclibdir}/install-tools/fix-header 2>/dev/null || :
strip $RPM_BUILD_ROOT%{gcclibdir}/install-tools/fixincl 2>/dev/null || :

# Remove unrelated man pages
rm -rf $RPM_BUILD_ROOT%{_prefix}/man/man7

# Remove libiberty.a library which is not used directly by gcc.
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/libiberty.a
for dir in power powerpc ppc64 pthread; do
  rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/$dir
done

# Remove libtool files
for arch in . power powerpc ppc64; do
  rm -f $RPM_BUILD_ROOT%{gcclibdir}/$arch/*.la
  rm -f $RPM_BUILD_ROOT%{gcclibdir}/pthread/$arch/*.la
done

# Remove zutil.h which is not installed by default on AIX systems
rm -f $RPM_BUILD_ROOT%{gcclibdir}/include/zutil.h

# Remove empty include directory
rmdir $RPM_BUILD_ROOT%{_prefix}/include || :

# Gzip info pages
gzip --best $RPM_BUILD_ROOT%{_prefix}/info/*.info

# Create links in /usr/bin
(
    cd $RPM_BUILD_ROOT
    mkdir -p usr/bin
    cd usr/bin
    for fname in cpp gcc gcov g++; do
        ln -sf ../..%{_prefix}/bin/$fname .
    done
)

%post
/sbin/install-info %{_prefix}/info/cpp.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/cppinternals.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/gcc.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/gccint.info.gz %{_prefix}/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/cpp.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/cppinternals.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/gcc.info.gz %{_prefix}/info/dir
    /sbin/install-info --delete %{_prefix}/info/gccint.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
/usr/bin/gcc
/usr/bin/gcov
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/include
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64
%ifos aix5.1
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc
%{_prefix}/lib/gcc/%{buildhost}/%{version}/power/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/power/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc/libgcc_eh.a
%endif
%{_prefix}/lib/gcc/%{buildhost}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/libgcc_eh.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64/libgcc_eh.a

%{_prefix}/libexec/gcc/%{buildhost}/%{version}/collect2

%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/README
%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/*.h
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/X11
%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/net
%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/netinet
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/root
%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/rpc
%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/sys
%{_prefix}/lib/gcc/%{buildhost}/%{version}/install-tools

%{_mandir}/man1/gcc.1
%{_mandir}/man1/gcov.1
%doc COPYING* BUGS FAQ MAINTAINERS gcc/README* 

# Below are files that are sometimes put into separately installed
# packages.  As they are almost always installed with gcc and are
# not much bigger, let's keep them within the "gcc" package.
#
# The "gcc-info" package
%{_infodir}/cpp*
%{_infodir}/gcc*
#
# The "cpp" package
%{_mandir}/man1/cpp.1
%{_prefix}/bin/cpp
/usr/bin/cpp
%{_prefix}/libexec/gcc/%{buildhost}/%{version}/cc1
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/specs


%files c++
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
#%{_prefix}/bin/g++
#/usr/bin/g++
#%{_prefix}/libexec/gcc/%{buildhost}/%{version}/cc1plus
#%{_mandir}/man1/g++.1
%doc COPYING*


%files -n libgcc
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/libgcc_s.a
%doc COPYING.LIB

%files -n libstdc++
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/libstdc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64/libstdc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/libstdc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64/libstdc++.a
%ifos aix5.1
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc
%{_prefix}/lib/gcc/%{buildhost}/%{version}/power/libstdc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc/libstdc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power/libstdc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc/libstdc++.a
%endif
%doc COPYING.LIB


%files -n libstdc++-devel
%defattr(-,root,system)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{buildhost}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64
%ifos aix5.1
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power
%dir %{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc
%{_prefix}/lib/gcc/%{buildhost}/%{version}/power/libsupc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/powerpc/libsupc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/power/libsupc++.a
%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/powerpc/libsupc++.a
%endif
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/libsupc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/ppc64/libsupc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/libsupc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/pthread/ppc64/libsupc++.a
#%{_prefix}/lib/gcc/%{buildhost}/%{version}/include/c++
%doc COPYING*


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Dec 14 2007 Christophe Belle <christophe.belle@bull.net> 4.2.0-1
- Update to version 4.2.0.

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
