# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# compiler default gcc
# To use xlc : --define 'gcc_compiler=x'
%{!?gcc_compiler: %define gcc_compiler 1}

Summary: A library of functions for manipulating PNG image format files
Name: libpng
Version: 1.6.37
%define libpngversion 16
Release: 1
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

Source0: https://github.com/glennrp/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: libpng.so.3-aix32
Source2: libpng.so.3-aix64
Source3: libpng12.so.0-aix32
Source4: libpng12.so.0-aix64
Source5: libpng14.so.14-aix32
Source6: libpng14.so.14-aix64
# Include CVE-2016-10087 corrected  1.5.28
Source7: libpng15.so.15-aix32
Source8: libpng15.so.15-aix64

Source9: libpng-pngusr.dfa

Source10: %{name}-%{version}-%{release}.build.log

Patch0:  %{name}-1.6.27-xlc-issue.patch

# From Fedora
Patch1:  libpng-multilib.patch
Patch2:  libpng-fix-arm-neon.patch


# BuildRoot: /var/tmp/%{name}-%{version}-buildroot

%define _libdir64 %{_prefix}/lib64


BuildRequires: zlib-devel
# Requires: zlib

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

The library is available as 32-bit and 64-bit.
The library contains older versions.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif 


%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel pkg-config

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif 


%prep

echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"

%setup -q
%if %{gcc_compiler} != 1
%patch0 -p1 -b .xlc-issue
%endif

# Provide pngusr.dfa for build (from Fedora)
# cp -p %{SOURCE1} ./pngusr.dfa         - TBC
#
%patch1 -p1
%patch2 -p1 -b .arm


# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh


# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

export CFLAGS=" -O2"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export CFLAGS=" -O2"

export CC__="xlc_r"
export CXX__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__
type $CXX__


export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"



# First build the 64-bit version
export OBJECT_MODE=64
cd 64bit

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LDFLAGS="-L./.libs -L%{_libdir64} -L%{_libdir} -Wl,-blibpath:%{_libdir64}:%{_libdir}:/usr/lib:/lib"

# LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static

# Fedora TBC  gmake  DFA_XTRA=pngusr.dfa
gmake

# make check has to launched after make install which compiles tools in tests

# now build the 32-bit version
export OBJECT_MODE=32
cd ../32bit

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LDFLAGS="-Wl,-bmaxdata:0x80000000 -L./.libs -L%{_libdir} -Wl,-blibpath:%{_libdir}:/usr/lib"

# LIBPATH="%{_libdir}:/usr/lib" \

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static

# Fedora TBC  gmake  DFA_XTRA=pngusr.dfa
gmake




# make check has to launched after make install which compiles tools in tests
%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

for testdir in 64bit  32bit
do
    cd $testdir
    ( gmake -k check || true )
    /usr/sbin/slibclean
    cd ..
done




%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


# install 64-bit version

export OBJECT_MODE=64
cd 64bit

gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install


# install 32-bit version

export OBJECT_MODE=32
cd ../32bit

gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install



# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
cd                  ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libpng.a                                              libpng%{libpngversion}.so.%{libpngversion}
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng%{libpngversion}.a  ${RPM_BUILD_ROOT}%{_libdir64}/libpng%{libpngversion}.so.%{libpngversion}


# Add the older v1.2.xx shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} libpng.so.3
/usr/bin/strip -X32 -e libpng.so.3
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng.so.3

cp %{SOURCE2} libpng.so.3
/usr/bin/strip -X64 -e libpng.so.3
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng.so.3

# # copy the old libpng12.a library for compatibility reasons
# cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/
# chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/*.a

# Add the older v1.2.x shared members for compatibility with older apps
cp %{SOURCE3} libpng12.so.0
/usr/bin/strip -X32 -e libpng12.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng12.so.0

cp %{SOURCE4} libpng12.so.0
/usr/bin/strip -X64 -e libpng12.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng12.so.0

# Add the older v1.4.x shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE5} libpng14.so.14
/usr/bin/strip -X32 -e libpng14.so.14
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng14.so.14

cp %{SOURCE6} libpng14.so.14
/usr/bin/strip -X64 -e libpng14.so.14
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng14.so.14

# Add the older v1.5.x shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE7} libpng15.so.15
/usr/bin/strip -X32 -e libpng15.so.15
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng15.so.15

cp %{SOURCE8} libpng15.so.15
/usr/bin/strip -X64 -e libpng15.so.15
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpng.a libpng15.so.15



# add compatibility symlink for "libpng14.a"
(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  %{__ln_s} libpng.a libpng12.a 
  %{__ln_s} libpng.a libpng14.a
  %{__ln_s} libpng.a libpng15.a
)


# Moved in %posttrans and %preun WITH RPM >= v4.4 !!
(
  cd ${RPM_BUILD_ROOT}
  mkdir -p %{_libdir64}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

# Create symlink to lib/libpng.a where 64 bit .so files have been archived
rm -f $RPM_BUILD_ROOT/%{_libdir64}/libpng.a
rm -f $RPM_BUILD_ROOT/%{_libdir64}/libpng16.a
ln -s  ../lib/libpng.a  $RPM_BUILD_ROOT/%{_libdir64}/libpng.a
ln -s  ../lib/libpng16.a  $RPM_BUILD_ROOT/%{_libdir64}/libpng16.a



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/*.txt 32bit/example.c 32bit/README 32bit/TODO 32bit/CHANGES 32bit/LICENSE
%{_libdir}/*.a
%{_libdir64}/*.a
%{_mandir}/man5/*
/usr/lib/*.a
/usr/lib64/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
# %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
/usr/bin/*
/usr/include/*
# /usr/lib/*.la


%changelog
* Tue Mar 31 2020 Michael Wilson <Michael.A.Wilson@atos.net> - 1.6.37-3
- Update to version 1.6.37

* Tue Mar 31 2020 Michael Wilson <Michael.A.Wilson@atos.net> - 1.6.27-3
- Rebuild on laurel2 with brpm
- Add symlink lib64/libpng.a to ../lib

* Thu Jan 12 2017 Michael Wilson <Michael.A.Wilson@atos.net> - 1.6.27-2
- Compile using GCC (default) or XLC

* Mon Jan 02 2017 Michael Wilson <Michael.A.Wilson@atos.net> - 1.6.27-1
- Update to version 1.6.27
- Correction for CVE-2016-10087
- Move make check to after make install, where test tools are built
- Add build log

* Tue Apr 26 2016 Tony Reix <tony.reix@bull.net> - 1.6.21-1
- Update to version 1.6.21

* Mon Apr 25 2016 Tony Reix <tony.reix@bull.net> - 1.5.26-1
- Update to version 1.5.26 plus fixes to .spec file

* Fri Jun 22 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.10-1
- Update to version 1.5.10

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-3
- Initial port on Aix6.1

* Wed Nov 23 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-2
- Add omitted symbolic link libpng12.a

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.4-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.5.4-1
- Update to version 1.5.4-1

* Tue Nov 30 2010 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.2.44-1
 - Update to version 1.2.44

*  Wed Oct 18 2006  BULL
 - Release  5

*  Mon Sep 18 2006  BULL
 - Release  4
 - support 64 bits

*  Fri Jan 06 2006  BULL
 - Release  3
 - added compatmember= shr.o

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit

*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.2.8
