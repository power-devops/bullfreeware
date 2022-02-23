%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define _libdir64 %{_libdir}64

Name: pcre
Version: 8.39
Release: 1
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz.sig
Source2: libpcre.so.0.aix32
Source3: libpcre.so.0.aix64
License: BSD
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildPrereq: sed
BuildRequires: bzip2 >= 1.0.2, zlib-devel >= 1.2.3, readline-devel >= 5.2
Requires: bzip2 >= 1.0.2, zlib >= 1.2.3, readline >= 5.2

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

The library is available as 32-bit and 64-bit.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for %{name}.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=

export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64 -B"

export CFLAGS=""
export CXXFLAGS=""
export CPPFLAGS=""
export LDFLAGS=""
export OPT="-g -O2"

#export CC="gcc"
#export CXX="gcc"
#export FLAG32="-maix32"
#export FLAG64="-maix64"
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"

export CC32="${CC} ${FLAG32}"
export CXX32="${CXX} ${FLAG32}"
export CC64="${CC} ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"

build_pcre() {
  echo "Building ${OBJECT_MODE} bit"
  ./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir} \
    --libdir=$1 \
    --enable-utf8 \
    --enable-unicode-properties \
    --enable-pcregrep-libz \
    --enable-pcregrep-libbz2 \
    --enable-pcretest-libreadline
  gmake %{?_smp_mflags}

  if [ "%{DO_TESTS}" == 1 ]
  then
    echo "Testing ${OBJECT_MODE} bit build"
    ( gmake -k check || true )
    /usr/sbin/slibclean
  fi
}

# build 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC=${CC64}
export CXX=${CXX64}
export LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib"
build_pcre %{_libdir64}
cd ..

# build 32-bit version
cd 32bit
export CC=${CC32}
export CXX=${CXX32}
export OBJECT_MODE=32
export LIBPATH="%{_libdir}:/usr/lib"
build_pcre %{_libdir}
cd ..

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"

# install 64-bit version
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

cd ${RPM_BUILD_ROOT}%{_bindir}
mv pcregrep pcregrep_64
mv pcretest pcretest_64
cd -

# Extract the 64 bit object from the libs
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 xv libpcre.a libpcre.so.1
/usr/bin/ar -X64 xv libpcrecpp.a libpcrecpp.so.0
/usr/bin/ar -X64 xv libpcreposix.a libpcreposix.so.0
cd -

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# add the shared object from older version for compatibility
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/libpcre.so.0
strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/libpcre.so.0
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir64}/libpcre.so.0
strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/libpcre.so.0

cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -X32 q libpcre.a libpcre.so.0
# Extract the 32 bit object from the libs
/usr/bin/ar -X32 xv libpcre.a libpcre.so.1
/usr/bin/ar -X32 xv libpcrecpp.a libpcrecpp.so.0
/usr/bin/ar -X32 xv libpcreposix.a libpcreposix.so.0
cd -

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpcre.a libpcre.so.0
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpcre.a libpcre.so.1
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpcrecpp.a libpcrecpp.so.0
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpcreposix.a libpcreposix.so.0
cd -

# replace archives in lib64 with links to archives in lib
cd ${RPM_BUILD_ROOT}%{_libdir64}
ln -sf ../lib/libprce.a libpcre.a
ln -sf ../lib/libpcrecpp.a libpcrecpp.a
ln -sf ../lib/libpcreposix.a libpcreposix.a
cd -

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/LICENCE 32bit/README
%{_bindir}/pcregrep*
%{_bindir}/pcretest*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
%{_mandir}/man1/pcregrep.1
%{_mandir}/man1/pcretest.1
/usr/bin/pcregrep
/usr/bin/pcretest
/usr/lib/*.a
/usr/lib/*.so*


%files devel
%defattr(-,root,system)
%{_bindir}/pcre-config
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_mandir}/man1/pcre-config.1
%{_mandir}/man3/*
/usr/bin/pcre-config
/usr/include/*
/usr/lib/*.la


%changelog
* Wed Jun 29 2016  Matthieu Sarter <matthieu.sarter.external@atos.net> -8.39-1
- Update to version 8.39

* Fri Mar 14 2014  Gerard Visiedo <gerard.visiedo@bull.net> -8.34-1
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


