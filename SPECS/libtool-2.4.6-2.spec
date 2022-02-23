%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 2.4.6
Release: 2
License: GPLv2+ and LGPLv2+ and GFDL
Group: Development/Tools
#Source: ftp://alpha.gnu.org/gnu/libtool-%{version}.tar.gz
Source0:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz
Source1:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz.sig
Source2:  libtool-gcc-xlc-wrapper
Source3:  %{name}-%{version}-%{release}.build.log
Patch1:   libtool-2.4.6-remove-build-rpath.patch
Patch2:   libtool-2.4.6-tests-echo-backslash-n.patch
URL: http://www.gnu.org/software/libtool
Prefix: %{_prefix}
PreReq: /sbin/install-info autoconf automake m4
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: bash, sed, grep
BuildRequires: gcc
Requires: autoconf >= 2.58, automake >= 1.9.2
Requires: info, /sbin/install-info
Requires: bash, sed, grep

%define _libdir64 %{_prefix}/lib64

%description
GNU Libtool is a set of shell scripts which automatically configure UNIX and
UNIX-like systems to generically build shared libraries. Libtool provides a
consistent, portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, but do not use
the rest of the GNU Autotools (such as GNU Autoconf and GNU Automake), you
should install the libtool package.

The libtool package also includes all files needed to integrate the GNU
Portable Library Tool (libtool) and the GNU Libtool Dynamic Module Loader
(ltdl) into a package built using the GNU Autotools (including GNU Autoconf
and GNU Automake).

This package includes a modification from the original GNU Libtool to allow
support for multi-architecture systems, such as the AMD64 Opteron and the Intel
64-bit Xeon and is available in 32-bit and 64-bit.

%package ltdl
Summary:  Runtime libraries for GNU Libtool Dynamic Module Loader
Group:    System Environment/Libraries
Provides: %{name}-libs = %{version}-%{release}
Obsoletes: %{name}-libs < 1.5.20
License:  LGPLv2+
Requires: info

%description ltdl
The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a
library that provides a consistent, portable interface which simplifies the
process of using dynamic modules.

These runtime libraries are needed by programs that link directly to the
system-installed ltdl libraries; they are not needed by software built using the
rest of the GNU Autotools (including GNU Autoconf and GNU Automake).

%package ltdl-devel
Summary:  Tools needed for development using the GNU Libtool Dynamic Module Loader
Group:    Development/Libraries
Requires: %{name}-ltdl = %{version}-%{release}
License:  LGPLv2+

%description ltdl-devel
Static libraries and header files for development with ltdl.

%prep
env
%setup -q
%patch1 -p1
%patch2 -p1

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit
# Need an additionnal source tree to build the libtool script for xlc
cp -rp 32bit xlc

%build
export PATH=/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export ECHO=/usr/bin/echo
export AR="/usr/bin/ar -X32_64"
export CONFIG_SHELL=/usr/bin/sh
export RM="/usr/bin/rm -f"
export EGREP="/opt/freeware/bin/egrep"

# We use the AIX nm with the -B option to display the symbols in the BSD format
# for compatibility with the GNU nm
export NM="/usr/bin/nm -X32_64 -B"

# libtool script is compiler dependant, so we need to build the script for 
# gcc and for xlc
# At runtime, a wrapper script will choose which version to run depending
# on the values of $CC, $CXX and $LT_GCC
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export LDFLAGS="-Wl,-brtl"
export CFLAGS=""

cd xlc
./configure --prefix=%{_prefix}
gmake
cd ..

# Now build with GCC
export PATH=/opt/freeware/bin:$PATH
# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
# Note 1 : build process does not properly recognize g++ if the full path is used instead of just g++
# Note 2 : build process does not properly recognize gcc if the -maix64 is in CLAGS instead of CC
export CC="gcc -maix64"
export CXX="g++ -maix64"
export F77="gfortran -maix64"
export FC="gfortran -maix64"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir64} \
            --infodir=%{_infodir} \
            --enable-shared --enable-static
gmake
if [ "%{DO_TESTS}" == 1 ]; then
    export LIBTOOL=`pwd`/libtool
    ( gmake -k check || true )
    unset LIBTOOL
fi
cd ..

# now build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CC="gcc"
export CXX="g++"
export F77="gfortran"
export FC="gfortran"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --infodir=%{_infodir} \
            --enable-shared --enable-static
gmake
if [ "%{DO_TESTS}" == 1 ]; then
    export LIBTOOL=`pwd`/libtool
    ( gmake -k check || true )
    unset LIBTOOL
fi
cd ..


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#first install the 64-bit version
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# Extract 64bit objects from archive
mkdir 64obj
cd 64obj
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libltdl.a
cd ..

#now install the 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# Add 64bit objects to the archive
for f in 64obj/*.o; do
# */
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libltdl.a ${f}
done

# Add scripts for both compilers
cp xlc/libtool ${RPM_BUILD_ROOT}%{_bindir}/libtool.xlc
cp 32bit/libtool ${RPM_BUILD_ROOT}%{_bindir}/libtool.gcc
cp %SOURCE2 ${RPM_BUILD_ROOT}%{_bindir}/libtool

# Temp hack : on our build machine, /opt/freeware is a link to /home2/freeware, but
# we don't want any reference to /home2/freeware in libtool !
sed -e "s/\/home2\/freeware/\/opt\/freeware/g" -i ${RPM_BUILD_ROOT}%{_bindir}/libtool.gcc
sed -e "s/\/home2\/freeware/\/opt\/freeware/g" -i ${RPM_BUILD_ROOT}%{_bindir}/libtool.xlc

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    # */
    cd -
  done
)

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_prefix}/info/libtool.info.gz %{_prefix}/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/libtool.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS 32bit/README 32bit/THANKS 32bit/TODO 32bit/ChangeLog
%{_bindir}/*
%{_infodir}/%{name}.info.gz
%{_datadir}/aclocal/*.m4
%{_datadir}/%{name}
/usr/bin/*


%files ltdl
%defattr(-,root,system)
%doc 32bit/libltdl/COPYING.LIB 32bit/libltdl/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files ltdl-devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la

%changelog
* Mon Aug 08 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.4.6-2
- GCC/xlc compatibility for libtool script
- ltldl now built with GCC

* Wed Feb 17 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.4.6-1
- Update to version 2.4.6

* Thu Nov 13 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.3-1
- Update to version 2.4.3

* Thu Jul 19 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.7b-2
- Build libraries on 32bit and 64bit

* Tue Jan 31 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.2.7b-1
- Initial port on Aix6.1

* Tue Aug 31 2010 Jean Noel Cordennet <jean-noel.cordenner@bull.net> 2.2.6b-2
- bug fixes

* Fri Apr 23 2010 Jean Noel Cordennet <jean-noel.cordenner@bull.net> 2.2.6b-1
- Update to version 2.2.6b

* Thu Apr 12 2007 Christophe Belle <christophe.belle@bull.net> 1.5.22-1
- Update to version 1.5.22

* Thu Aug 19 2004 David Clissold <cliss@austin.ibm.com>  1.5.8-1
- Update to 1.5.8

* Thu May 27 2004 David Clissold <cliss@austin.ibm.com>  1.5-2
- Avoid forced dependency on GNU sed; ok to use AIX sed.

* Wed Apr 30 2003 David Clissold <cliss@austin.ibm.com>
- Update to level 1.5

* Thu Sep 27 2001 David Clissold <cliss@austin.ibm.com>
- Update to level 1.4.2

* Fri May 25 2001 David Clissold <cliss@austin.ibm.com>
- Fix to patch for ia64 -- add no_undefined_flag="-zdefs"

* Sun Mar 25 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix library dependency code for ia64

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Hardcode noentry flag

* Tue Mar 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Add code to handle non-gcc compilers

* Sun Mar 04 2001 Marc Stephenson <marc@austin.ibm.com>
- Update to 1.3.5a

* Thu Mar 01 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Update needed for the the IA64 aix patch

* Fri Feb 16 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Fri Mar  3 2000 Jeff Johnson <jbj@redhat.com>
- add prereqs for m4 and perl inorder to run autoconf/automake.

* Mon Feb 28 2000 Jeff Johnson <jbj@redhat.com>
- functional /usr/doc/libtool-*/demo by end-user %post procedure (#9719).

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.4.

* Mon Dec  6 1999 Jeff Johnson <jbj@redhat.com>
- change from noarch to per-arch in order to package libltdl.a (#7493).

* Thu Jul 15 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.3.

* Mon Jun 14 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.2.

* Tue May 11 1999 Jeff Johnson <jbj@redhat.com>
- explicitly disable per-arch libraries (#2210)
- undo hard links and remove zero length file (#2689)

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- disable the --cache-file passing to ltconfig; this breaks the older
  ltconfig scripts found around.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.2f

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- completed arm patch
- added patch to make it more arm-friendly
- upgrade to version 1.2d

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- fixed busted group

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- Update to 1.0h
- added install-info support

* Tue Nov 25 1997 Elliot Lee <sopwith@redhat.com>
- Update to 1.0f
- BuildRoot it
- Make it a noarch package
