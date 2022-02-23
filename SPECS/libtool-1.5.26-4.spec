%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.5.26
Release: 4
License: GPL
Group: Development/Tools
Source: ftp://alpha.gnu.org/gnu/libtool-%{version}.tar.gz
Source1: libtool-gcc-xlc-wrapper
Patch1:   libtool-1.5.24-multilib.patch
# don't  read .la file in current working directory, root might get tricked'
# into running a prepared binary in that directory:
Patch2:   libtool-1.5.26-relativepath.patch
Patch3:   libtool-1.5.26-remove-build-rpath.patch
URL: http://www.gnu.org/software/libtool
Prefix: %{_prefix}
PreReq: /sbin/install-info autoconf automake m4
BuildRoot: /var/tmp/%{name}-root
BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: bash, sed, grep
Requires: autoconf >= 2.58, automake >= 1.9.2
Requires: info, /sbin/install-info
Requires: bash, sed, grep

%define _libdir64 %{_prefix}/lib64

%description
The libtool package contains the GNU libtool, a set of shell scripts which
automatically configure UNIX and UNIX-like architectures to generically build
shared libraries.  Libtool provides a consistent, portable interface which
simplifies the process of using shared libraries.

If you are developing programs which will use shared libraries, you should
install libtool.

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
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p0

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
# */
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/
# */
mkdir gcc
cp -rp 32bit/* gcc/
# */

%build
export PATH=/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export NM=/usr/bin/nm
export ECHO=/usr/bin/echo

# libtool script is compiler dependant, so we need to build the script for 
# gcc and for xlc
# At runtime, a wrapper script will choose which version to run depending
# on the values of $CC, $CXX and $LT_GCC
export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"
cd gcc
./configure --prefix=%{_prefix}
make
cd ..

# Now build with xlc
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export LDFLAGS="-Wl,-brtl"
# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CFLAGS="-q64"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir64} \
            --infodir=%{_infodir} \
            --enable-shared --enable-static
gmake
if [ "%{DO_TESTS}" == 1 ]; then
    ( gmake -k check || true )
fi
cd ..

# now build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CFLAGS=""
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --infodir=%{_infodir} \
            --enable-shared --enable-static
gmake
if [ "%{DO_TESTS}" == 1 ]; then
    ( gmake -k check || true )
fi
cd ..

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
#first install the 64-bit version
cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# Extract 64bit object from archive
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libltdl.a ltdl.o

#first install the 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# Add 64bit object to the archive
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libltdl.a ltdl.o

# Add scripts for both compilers
cp gcc/libtool ${RPM_BUILD_ROOT}%{_bindir}/libtool.gcc
cp 32bit/libtool ${RPM_BUILD_ROOT}%{_bindir}/libtool.xlc
cp %SOURCE1 ${RPM_BUILD_ROOT}%{_bindir}/libtool

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS 32bit/README 32bit/THANKS 32bit/TODO 32bit/ChangeLog
%{_bindir}/*
%{_infodir}/%{name}.info
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
* Thu Aug 04 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.5.26-4
- Update to version 1.5.26
- GCC/xlc compatibility

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
