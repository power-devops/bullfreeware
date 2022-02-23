Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 2.4.3
Release: 1
License: GPLv2+ and LGPLv2+ and GFDL
Group: Development/Tools
#Source: ftp://alpha.gnu.org/gnu/libtool-%{version}.tar.gz
Source0:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz
Source1:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz.sig
URL: http://www.gnu.org/software/libtool
Prefix: %{_prefix}
PreReq: /sbin/install-info autoconf automake m4
BuildRoot: /var/tmp/%{name}-%{version}-root
# avoid unnecessary dependency on the GNU sed
#  (can just deinstall sed and reinstall after build)
BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: bash, sed, grep
BuildRequires: patch
Requires: autoconf >= 2.58, automake >= 1.9.2
Requires: info, /sbin/install-info
Requires: bash, sed, grep

## BuildConflicts: sed
%define DEFCC cc
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
export PATH=/opt/freeware/bin:$PATH

%setup -q

## mkdir ../32bit
## mv * ../32bit
## mv ../32bit .
## mkdir 64bit
## cp -r 32bit/* 64bit/

mkdir -p ../64bit
cp -r * ../64bit
mv ../64bit .

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/sh
export RM="/usr/bin/rm -f"

# We use the AIX nm with the -B option to display the symbols in the BSD format
# for compatibilit√y with the GNU nm
export NM="/usr/bin/nm -X32_64 -B"

# first build the 64-bit version
cd 64bit
export CC="/usr/vac/bin/xlc_r -q64"
export LDFLAGS="-Wl,-brtl"
export OBJECT_MODE=64

## ./configure --enable-ltdl-install --prefix=%{_prefix}
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static

# build not smp safe:
make

## cp ./libltdl/.libs/libltdl.so.7 .

# now build the 32-bit version
cd ..
export CC="/usr/vac/bin/xlc_r"
export OBJECT_MODE=32

## ./configure --enable-ltdl-install --prefix=%{_prefix}

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static
# build not smp safe:
make

## # add the 64-bit shared objects to the shared library containing already the
## # 32-bit shared objects
## rm -f libltdl/.libs/libltdl.a
## /usr/bin/ar -X32_64  -r libltdl/.libs/libltdl.a libltdl/.libs/libltdl.so.7 ../64bit/libltdl.so.7

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ..
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  /usr/bin/ar -X64 -x libltdl.a
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
(
  for f in ${RPM_BUILD_ROOT}%{_libdir64}/*.o
  do
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libltdl.a ${f}
  done
)

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
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog
%{_bindir}/*
%{_infodir}/%{name}.info.gz
%{_datadir}/aclocal/*.m4
%{_datadir}/%{name}
/usr/bin/*


%files ltdl
%defattr(-,root,system)
%doc libltdl/COPYING.LIB libltdl/README
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
