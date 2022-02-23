%bcond_without dotests
# Unactivate to use libtool
%bcond_without cmake_build

%define        _libdir64 %{_libdir}64

Patch1:        pcre-8.44_cmake.patch

Name:          pcre
Version:       8.44
Release:       1
Summary:       Perl-compatible regular expression library
URL:           http://www.pcre.org/
Source0:       ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz
Source1:       ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz.sig
Source2:       libpcre.so.0.aix32
Source3:       libpcre.so.0.aix64
Source4:       pcre-config_32
Source5:       pcre-config_64
Source1000:    %{name}-%{version}-%{release}.build.log
License:       BSD
Group:         System Environment/Libraries
BuildRequires: sed bzip2-devel >= 1.0.2, zlib-devel >= 1.2.3, readline-devel >= 5.2
%if %{with cmake_build}
BuildRequires: cmake >= 3.16
%endif
Requires:      bzip2 >= 1.0.2, zlib >= 1.2.3, readline >= 5.2

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for %{name}.


%prep
%setup -q

%patch1 -p1 -b .cmake

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
rm -rf   /tmp/%{name}-%{version}-32bit
cp -rp 32bit 64bit

#Ensure libpcre.so.0-aix(32|64) are present
ls %{SOURCE2}
ls %{SOURCE3}

%build
export PATH="/opt/freeware/bin:$PATH"

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export OPT="-O2"
export CFLAGS="-fPIC -pthread -D_LARGE_FILES"
export CXXFLAGS=$CFLAGS


export CC="gcc"
export CXX="g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
# export CC="/usr/vac/bin/xlc_r"
# export CXX="/usr/vacpp/bin/xlC_r"
# export FLAG32="-q32"
# export FLAG64="-q64"

export CC32="${CC} ${FLAG32}"
export CXX32="${CXX} ${FLAG32}"
export CC64="${CC} ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"

build_pcre() {
  set -x
%if %{with cmake_build}
  mkdir build_cmake ; cd build_cmake
  echo "Building ${OBJECT_MODE} bit with cmake"
  cmake -L \
    -DCMAKE_BUILD_TYPE=RELEASE \
    -DNON_STANDARD_LIB_SUFFIX=YES \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DPCRE_BUILD_PCRE16=ON \
    -DPCRE_BUILD_PCRE32=ON \
    -DPCRE_SUPPORT_UTF=ON \
    -DPCRE_SUPPORT_UNICODE_PROPERTIES=ON \
    -DPCRE_NO_RECURSE=ON \
    -DPCRE_SUPPORT_PCREGREP_JIT=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DPCRE_SUPPORT_LIBZ=ON -DPCRE_SUPPORT_LIBBZ2=ON -DPCRE_SUPPORT_LIBREADLINE=ON \
    -DCMAKE_INSTALL_RPATH=$PATH_MODE \
    -DCMAKE_BUILD_RPATH=$PATH_MODE \
    ..
    
    #    -DCMAKE_INSTALL_LIBDIR=$1 is ignored...
    
    gmake VERBOSE=1  %{?_smp_mflags}
  cd ..
%else
  mkdir build_configure ; cd build_configure
  echo "Building ${OBJECT_MODE} bit with libtool"
  ../configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir} \
    --libdir=$1 \
    --enable-utf \
    --enable-unicode-properties \
    --enable-pcregrep-libz \
    --enable-pcregrep-libbz2 \
    --enable-pcretest-libreadline \
    --disable-static \
    --with-pic

## --enable-pcre16
## --enable-pcre32
## --enable-utf
## --enable-pcre8

  gmake --trace %{?_smp_mflags}
  cd ..
%endif
}

# build 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC=${CC64}
export CXX=${CXX64}
%if %{with cmake_build}
export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export PATH_MODE="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib"
%else
export LIBPATH="./.libs:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L./.libs -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export CFLAGS="$CFLAGS $OPT"
export CXXFLAGS="$CXXFLAGS $OPT"
%endif
build_pcre %{_libdir64}
cd ..

# build 32-bit version
cd 32bit
export CC=${CC32}
export CXX=${CXX32}
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
%if %{with cmake_build}
export LIBPATH="/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="$LDFLAGS -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export PATH_MODE="/opt/freeware/lib/pthread:/opt/freeware/lib"
%else
export LIBPATH="./.libs:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="$LDFLAGS -L./.libs -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export CFLAGS="$CFLAGS $OPT"
export CXXFLAGS="$CXXFLAGS $OPT"
%endif
build_pcre %{_libdir}
cd ..

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export STRIP="/usr/bin/strip -X32_64"

# install 64-bit version
cd 64bit
%if %{with cmake_build}
  cd build_cmake
%else
  cd build_configure
%endif

export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ../..

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  mv pcregrep    pcregrep_64
  mv pcretest    pcretest_64
  # mv pcre-config pcre-config_64
  # libdir is ignored...
  cd ${RPM_BUILD_ROOT}
  mv ${RPM_BUILD_ROOT}%{_libdir} ${RPM_BUILD_ROOT}%{_libdir64}
  
  # Extract the 64 bit object from the libs
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  $AR xv libpcre.a      libpcre.so.1
  $AR xv libpcrecpp.a   libpcrecpp.so.0
  $AR xv libpcreposix.a libpcreposix.so.0
  $AR xv libpcre16.a    libpcre16.so.0
  $AR xv libpcre32.a    libpcre32.so.0
)

# install 32-bit version
cd 32bit
%if %{with cmake_build}
  cd build_cmake
%else
  cd build_configure
%endif

export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ../..

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  mv pcregrep    pcregrep_32
  mv pcretest    pcretest_32
  # mv pcre-config pcre-config_32
  
  # Extract the 64 bit object from the libs
  cd ${RPM_BUILD_ROOT}%{_libdir}
  $AR xv libpcre.a      libpcre.so.1
  $AR xv libpcrecpp.a   libpcrecpp.so.0
  $AR xv libpcreposix.a libpcreposix.so.0
  $AR xv libpcre16.a    libpcre16.so.0
  $AR xv libpcre32.a    libpcre32.so.0
  # And strip -e it
  $STRIP -e libpcre.so.1
  $STRIP -e libpcrecpp.so.0
  $STRIP -e libpcreposix.so.0
  $STRIP -e libpcre16.so.0
  $STRIP -e libpcre32.so.0
)

# add the shared object from older version for compatibility
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/libpcre.so.0
$STRIP -e ${RPM_BUILD_ROOT}%{_libdir}/libpcre.so.0
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir64}/libpcre.so.0
$STRIP -e ${RPM_BUILD_ROOT}%{_libdir64}/libpcre.so.0

# Add 64 bit version
cd ${RPM_BUILD_ROOT}%{_libdir}
$AR q libpcre.a      libpcre.so.0
$AR q libpcre.a      ../lib64/libpcre.so.0
$AR q libpcre.a      ../lib64/libpcre.so.1

$AR q libpcrecpp.a   ../lib64/libpcrecpp.so.0
$AR q libpcreposix.a ../lib64/libpcreposix.so.0
$AR q libpcre16.a    ../lib64/libpcre16.so.0
$AR q libpcre32.a    ../lib64/libpcre32.so.0

# Strip -e 64 .so files
$STRIP -e ../lib64/libpcre.so.0
$STRIP -e ../lib64/libpcre.so.1
$STRIP -e ../lib64/libpcrecpp.so.0
$STRIP -e ../lib64/libpcreposix.so.0
$STRIP -e ../lib64/libpcre16.so.0
$STRIP -e ../lib64/libpcre32.so.0

# replace archives in lib64 with links to archives in lib
cd ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf ../lib/libpcre.a      libpcre.a
ln -sf ../lib/libpcrecpp.a   libpcrecpp.a
ln -sf ../lib/libpcreposix.a libpcreposix.a
ln -sf ../lib/libpcre16.a    libpcre16.a
ln -sf ../lib/libpcre32.a    libpcre32.a

# Link binary files to 64 bit version
cd ${RPM_BUILD_ROOT}%{_bindir}
ln -s pcregrep_64    pcregrep
ln -s pcretest_64    pcretest
# ln -s pcre-config_64 pcre-config

%if %{with cmake_build}
# Add pcre-config
cd ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE4} .
cp %{SOURCE5} .
ln -sf pcre-config_64 pcre-config
%endif


%check
%if %{with dotests}

test_pcre() {
  set -ex
  %if %{with cmake_build}
    cd build_cmake
  %else
    cd build_configure
  %endif
  LIBPATH="${RPM_BUILD_ROOT}%{_libdir}:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
  echo "Testing ${OBJECT_MODE} bit build"
  echo "LIBPATH: $LIBPATH"
  find . -name "pcretest" | xargs dump -X32_64 -Hv
  %if %{with cmake_build}
    ( gmake test    || true )
  %else
    ( gmake -k check || true )
  %endif
  /usr/sbin/slibclean
  cd ..
}

# build 64-bit version
cd 64bit
test_pcre
cd ..

# build 32-bit version
cd 32bit
test_pcre
cd ..
%endif # dotests


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/LICENCE 32bit/README
%{_bindir}/pcregrep*
%{_bindir}/pcretest*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_mandir}/man1/pcregrep.1
%{_mandir}/man1/pcretest.1


%files devel
%defattr(-,root,system)
%{_includedir}/*.h
%{_bindir}/pcre-config*
%{_mandir}/man3/*
%{_mandir}/man1/pcre-config.1
# libtool only
# %{_libdir}/pkgconfig/*



%changelog
* Tue Sep 08 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 8.44-1
- New version 8.44

* Fri Feb 14 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 8.43-2
- Add pcre-config even if build with cmake

* Wed Oct 09 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 8.43-1
- Update to version 8.43
- Use GCC
- Can use CMake or libtool
- No more provide link to /usr
- No more provide *.la, pkgconfig, pcre-config or .so
- Correct link from /opt/freeware/lib64/libpcre.a to ../lib/libpcre.a
- Add UTF-{16,32} libraries

* Wed Jun 29 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 8.39-1
- Update to version 8.39

* Fri Mar 14 2014 Gerard Visiedo <gerard.visiedo@bull.net> -8.34-1
- Update to version 8.34

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> -8.12-3
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 8.12-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Mar 17 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.12-1
- Update to version 8.12

* Thu Oct 14 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 8.10-1
- Update to version 8.10.

* Thu Feb 16 2006 Reza Arbab <arbab@austin.ibm.com>
- Add patch for CAN-2005-2491.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.


