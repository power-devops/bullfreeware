%bcond_without dotests

# By default, compiler is gcc.
#To compile with xlc : --define 'gcc_compiler=0'
#%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler: %define gcc_compiler 1}

# Current .so version is 5
# See SET_TARGET_PROPERTIES(... SOVERSION 5) in lib/CMakeLists.txt
%define soversion 5

%if %{gcc_compiler} == 1
%define compiler_msg This version has been compiled with GCC.
%else
%define compiler_msg This version has been compiled with XLC.
%endif

#default optimize is 2 ; may be 0
%{!?optimize:%define optimize 2}

%define _libdir64     %{_prefix}/lib64


Name:    libzip
Version: 1.7.3
Release: 1
Summary: C library for reading, creating, and modifying zip archives

License: BSD
Group:   Applications/File
URL:     https://libzip.org/
Source0: https://libzip.org/download/libzip-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

BuildRequires: gcc >= 8.4.0
BuildRequires: compat-getopt-devel
BuildRequires: bzip2-devel >= 1.0.8
BuildRequires: gnutls-devel
BuildRequires: nettle-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

BuildRequires: cmake >= 3.16.0
BuildRequires: sed

# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
# find regress/ -type f | /usr/lib/rpm/perl.prov
BuildRequires:  perl(perl)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

Requires: gcc >= 8.4.0
Requires: compat-getopt
Requires: bzip2 >= 1.0.8
Requires: gnutls
Requires: nettle
Requires: xz
Requires: zlib


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%{compiler_msg}


%package devel
Summary:   Development files for %{name}
Requires: %{name} = %{version}-%{release}
Group:    Applications/File
Requires: compat-getopt-devel
Requires: bzip2-devel >= 1.0.8
Requires: gnutls-devel
Requires: nettle-devel
Requires: xz-devel
Requires: zlib-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:  Command line tools from %{name}
Requires: %{name} = %{version}-%{release}
Group:    Applications/File

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- zipcmp
- zipmerge
- ziptool


%prep

export TAR=/usr/bin/tar
export PATH=/opt/freeware/bin:$PATH

%setup -q

# unwanted in package documentation
rm INSTALL.md

# drop skipped test which make test suite fails (cmake issue ?)
sed -e '/clone-fs-/d' \
    -i regress/CMakeLists.txt

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar"

### default make is gmake
export MAKE="/opt/freeware/bin/gmake"

export CFLAGS="-I/usr/include -I/opt/freeware/include"
export CFLAGS="${CFLAGS} -D_LARGE_FILES -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
export CFLAGS="${CFLAGS} -fPIC"

#Add -g to CFLAGS for debug
export CFLAGS="${CFLAGS} -O%{optimize}"


# Choose GCC or XLC
%if %{gcc_compiler} == 1

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"
###use full path for gcc except for ... which requires a string beginning with gcc:  export CC="gcc"
export CFLAGS32="-maix32"
export CFLAGS64="-maix64"

echo "GCC version=`$CC --version | head -1`"

%else

export CC="/usr/vac/bin/xlc_r"
export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"
export CFLAGS32="-q32 -qcpluscmt"
export CFLAGS64="-q64 -qcpluscmt"
echo "XLC Version=`$CC -qversion`"

export RPM_OPT_FLAGS=`echo ${RPM_OPT_FLAGS} | sed 's:-fsigned-char::'`
export CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"

%endif

build_libzip()
{
set -x

echo "CC=" ${CC}
echo "CFLAGS=" ${CFLAGS}
echo "LDFLAGS=" ${LDFLAGS}
echo "AR=" ${AR}

rm -f CMakeCache.txt

#cmake .  --trace --debug-trycompile --debug-output -G"Unix Makefiles"
cmake -L . \
    -G"Unix Makefiles" \
    -DCMAKE_SYSTEM_NAME="AIX"  \
    -DCMAKE_C_COMPILER="${CC}"  \
    -DCMAKE_C_FLAGS="${CFLAGS}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=$1 \
    -DCMAKE_INSTALL_MANDIR="%{_mandir}" \
    -DBUILD_SHARED_LIBS=ON  \
    -DBUILD_STATIC_LIBS=OFF \
    -DCMAKE_AR="${AR}" \
    -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE
#    -DCMAKE_INSTALL_RPATH=$PATH_MODE \
#    -DCMAKE_BUILD_RPATH=$PATH_MODE \

$MAKE VERBOSE=1 --print-directory %{?_smp_mflags} -j16

/usr/sbin/slibclean

} #end build_libzip()


# build 32bit mode
echo "build 32bit mode"

(
  cd 32bit
  export OBJECT_MODE=32
  export LIBS32="-L/opt/freeware/lib -L/usr/lib"

  export CFLAGS="${CFLAGS} ${CFLAGS32} ${LIBS32}"
  export CXXFLAGS="${CFLAGS} ${CFLAGS32} ${LIBS32}"

  export LDFLAGS32="-Wl,-bmaxdata:0x80000000 $LIBS32"
  export LDFLAGS="${LDFLAGS32}"

#  export PATH_MODE="/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"

  build_libzip lib

  cd ..

)

# build 64bit mode
(
  cd 64bit
  export OBJECT_MODE=64
  export LIBS64="-L/opt/freeware/lib64 -L/opt/freeware/lib -L/usr/lib"
  export CFLAGS="${CFLAGS} ${CFLAGS64} ${LIBS64}"
  export CXXFLAGS="${CFLAGS} ${CFLAGS64} ${LIBS64}"

  export LDFLAGS64=""
  export LDFLAGS="$LDFLAGS64 $LIBS64"

#  export PATH_MODE="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

  build_libzip lib64

  cd ..

)


%install
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar -X32_64"

export INSTALL="/opt/freeware/bin/install "

export LN="/usr/bin/ln -s"
export RM="/usr/bin/rm -f"
export MAKE="/opt/freeware/bin/gmake"


[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# ==========================
# Install the 64 bit version
# ==========================
cd 64bit

export OBJECT_MODE=64

$MAKE VERBOSE=1 DESTDIR=${RPM_BUILD_ROOT} install 

# Move the 64 bit utilities
(
  cd  ${RPM_BUILD_ROOT}%{_bindir}
  for f in $(ls -1| grep -v -e _32 -e _64)
    do
    mv ${f} ${f}_64
    /usr/bin/strip -X32_64 ${f}_64 || :
  done
)
cd ..


# ==========================
# Install the 32 bit version
# ==========================
cd 32bit

export OBJECT_MODE=32

$MAKE VERBOSE=1 DESTDIR=${RPM_BUILD_ROOT} install 

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.%{soversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.%{soversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
)

(
  cd  ${RPM_BUILD_ROOT}%{_bindir}
  for f in $(ls -1| grep -v -e _32 -e _64)
    do
    mv ${f} ${f}_32
    /usr/bin/strip -X32_64 ${f}_64 || :
    $LN ${f}_64 ${f}
  done
)
cd ..


%check
%if %{with dotests}
cd 64bit
( gmake --trace --print-directory -k check || true )
/usr/sbin/slibclean
cd ../32bit
( gmake --trace --print-directory -k check || true )
/usr/sbin/slibclean
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/LICENSE
%{_libdir}/libzip.a
%{_libdir64}/libzip.a

%files tools
%defattr(-,root,system)
%{_bindir}/zipcmp*
%{_bindir}/zipmerge*
%{_bindir}/ziptool*
%{_mandir}/man1/zip*

%files devel
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/THANKS* 32bit/*.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%{_libdir}/pkgconfig/libzip.pc
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*


%changelog
* Mon Nov 30 2020 Étienne Guesnet <etienne.guesnet@atos.net> 1.7.3-1
- New version 1.7.3

* Wed Feb 19 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.6.1-1
- New version 1.6.1
- BullFreeware Compatibility Improvements
- Bullfreeware OpenSSL removal

* Fri Dec 13 2019 Michael Wilson <michael.a.wilson@atos.net> 1.5.1-2
- Archive non-stripped 32 & 64 bit libzip.so.soversion in libzip.a
- Adaptation to new Cmake
- Adaptation to RPM version 4, brpm.OLD and build environment laurel2

* Fri Feb 15 2019 Daniele Silvestre <daniele.silvestre@atos.net> 1.5.1-1
- First delivery for AIX on bullfreeware

* Wed Apr 11 2018 Remi Collet <remi@remirepo.net> - 1.5.1-1
- update to 1.5.1
- drop dependency on zlib-devel and bzip2-devel no more
  referenced in libzip.pc
- drop rpath patch merged upstream
 
* Thu Mar 15 2018 Remi Collet <remi@remirepo.net> - 1.5.0-2
- add dependency on zlib-devel and bzip2-devel #1556068
 
* Mon Mar 12 2018 Remi Collet <remi@remirepo.net> - 1.5.0-1
- update to 1.5.0
- use openssl for cryptography instead of bundled custom AES implementation
 
* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.4.0-5
- missing BR on C compiler
- use ldconfig_scriptlets
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Fri Jan  5 2018 Remi Collet <remi@remirepo.net> - 1.4.0-3
- add upstream patch and drop multilib hack
 
* Tue Jan  2 2018 Remi Collet <remi@remirepo.net> - 1.4.0-2
- re-add multilib hack #1529886
 
* Sat Dec 30 2017 Remi Collet <remi@remirepo.net> - 1.4.0-1
- update to 1.4.0
- switch to cmake
- add upstream patch for lib64
 
* Mon Nov 20 2017 Remi Collet <remi@remirepo.net> - 1.3.2-1
- update to 1.3.2
- drop multilib header hack
- change URL to https://libzip.org/
- test suite now ok on all arch
 
* Wed Sep 06 2017 Pavel Raiskup <praiskup@redhat.com> - 1.3.0-2
- use multilib-rpm-config for multilib hacks
 
* Mon Sep  4 2017 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0
- add dependency on bzip2 library
- ignore 3 tests failing on 32-bit
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- soname bump to 5
 
* Tue Feb 28 2017 Remi Collet <remi@fedoraproject.org> - 1.2.0-0
- update to 1.2.0
- soname bump to 5
- temporarily keep libzip.so.4
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- update to 1.1.3
 
* Sat Feb 20 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2
- add BR on perl(Getopt::Long)
 
* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Thu Jan 28 2016 Remi Collet <remi@fedoraproject.org> - 1.1-1
- update to 1.1
- new ziptool command
- add fix for undefined optopt in ziptool.c (upstream)
 
* Fri Dec  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- fix libzip-tools summary #1288424
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- soname bump from .2 to .4
- drop ziptorrent
- create "tools" sub package
 
* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-5
- actually apply patch (using %%autosetup)
* Mon Mar 23 2015 Rex Dieter <rdieter@fedoraproject.org> 0.11.2-4
- CVE-2015-2331: integer overflow when processing ZIP archives (#1204676,#1204677)
 
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Thu Dec 19 2013 Remi Collet <remi@fedoraproject.org> - 0.11.2-1
- update to 0.11.2
- run test during build
 
* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-3
- replace php patch with upstream one
 
* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-2
- include API-CHANGES and LICENSE in package doc
 
* Wed Aug 21 2013 Remi Collet <remi@fedoraproject.org> - 0.11.1-1
- update to 0.11.1
 
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
 
* Mon Oct 15 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-5
- fix typo in multiarch (#866171)
 
* Wed Sep 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-4
- Warning about conflicting contexts for /usr/lib64/libzip/include/zipconf.h versus /usr/include/zipconf-64.h (#853954)
 
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
 
* Tue Jul 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.10.1-2
- spec cleanup, better multilib fix
 
* Wed Mar 21 2012 Remi Collet <remi@fedoraproject.org> - 0.10.1-1
- update to 0.10.1 (security fix only)
- fixes for CVE-2012-1162 and CVE-2012-1163
 
* Sun Mar 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-2
- try to fix ARM issue (#799684)
 
* Sat Feb 04 2012 Remi Collet <remi@fedoraproject.org> - 0.10-1
- update to 0.10
- apply patch with changes from php bundled lib (thanks spot)
- handle multiarch headers (ex from MySQL)
 
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
 
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-2
- Cleaned up pkgconfig deps which are now automatically handled by RPM.
 
* Thu Feb 04 2010 Kalev Lember <kalev@smartlink.ee> - 0.9.3-1
- Updated to libzip 0.9.3
 
* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.9-4
- Use bzipped upstream tarball.
 
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
 
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
 
* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- libzip-0.9
 
* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.8-5
- rebuild for new gcc-4.3
 
* Fri Jan 11 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.8-4
- use better workaround for removing rpaths
 
* Tue Nov 20 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-3
- require pkgconfig in devel subpkg
- move api description to devel subpkg
- keep timestamps in %%install
- avoid lib64 rpaths 
 
* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-2
- Change License to BSD
 
* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.8-1
- Initial version for Fedora
