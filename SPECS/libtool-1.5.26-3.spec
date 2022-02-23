Summary:  The GNU Portable Library Tool
Name:     libtool
Version:  1.5.26
Release:  3
License:  GPLv2+ and LGPLv2+ and GFDL
Group:    Development/Tools
Source0:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz
Source1:  http://ftp.gnu.org/gnu/libtool/%{name}-%{version}.tar.gz.sig
Patch1:   libtool-1.5.24-multilib.patch
# don't  read .la file in current working directory, root might get tricked
# into running a prepared binary in that directory:
Patch2:   libtool-1.5.24-relativepath.patch
URL:      http://www.gnu.org/software/libtool/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: autoconf >= 2.59, automake >= 1.9.2
BuildRequires: bash, sed, grep
BuildRequires: patch
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
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch1 -p1
%patch2 -p1
mkdir -p ../64bit
cp -r * ../64bit
mv ../64bit .


%build
# first build the 64-bit version
cd 64bit
export CC="/home/gnu/gcc482/bin/gcc -maix64"
export LDFLAGS="-Wl,-brtl"
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static
# build not smp safe:
make
cd ..

# now build the 32-bit version
export CC="/home/gnu/gcc482/bin/gcc"
export LDFLAGS="-Wl,-brtl"
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static
# build not smp safe:
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  /usr/bin/ar -X64 -x libltdl.a
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libltdl.a ${RPM_BUILD_ROOT}%{_libdir64}/ltdl.o

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


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


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
* Mon Feb 16 2015 BULL Hamza Sellami <hamza.sellami@bull.com>
- Rebuild/BoosTrapped with the new GCC Compiler 4.8.3

* Tue Sep 18 2012 Michael Perzl <michael@perzl.org> - 1.5.26-2
- added missing shared member to "proper" AIX shared library

* Fri Oct 10 2008 Michael Perzl <michael@perzl.org> - 1.5.26-1
- first version for AIX V5.1 and higher
