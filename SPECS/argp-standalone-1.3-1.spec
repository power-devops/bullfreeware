# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64
%define libname libargp

Name: argp-standalone
Version: 1.3
Release: 1
Group: System Environment/Libraries
Summary: Argp standalone library
License: GPLv2+
Source0: http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

%description
Standalone version of arguments parsing functions from GLIBC

%package devel
Group: Development/Libraries
Summary: Argp standalone library - development files
Requires: %{name} = %{version}-%{release}
%description devel
Development files for programs using libargp.

%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_COMMON="-O0"

build_libargp(){
    set -x
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir}

    gmake %{?_smp_mflags}

    # Only the static library is created.
    # Create the correct shared library ourself.
    # The export file creation command is based on libtool.
    $NM %{libname}.a | awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) && (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } else { print $ 1 } } }' | sort -u > %{libname}.exp
    $CC $CFLAGS $LDFLAGS -shared %{libname}.a -o %{libname}.so.1 -Wl,-bE:%{libname}.exp
    rm %{libname}.a
    $AR cru %{libname}.a %{libname}.so.1
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_libargp %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_libargp %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
# Make install does nothing for now. But keep it anyway.
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
install -m644 libargp.a ${RPM_BUILD_ROOT}%{_libdir64}

cd ../32bit
export OBJECT_MODE=32
# Make install does nothing for now. But keep it anyway.
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
install -m644 libargp.a ${RPM_BUILD_ROOT}%{_libdir}
install -m644 argp.h ${RPM_BUILD_ROOT}%{_includedir}
cd ..

(
    %define libsoversion 1

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{libname}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{libname}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.%{libsoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{libname}.a
    ln -sf ../lib/%{libname}.a %{libname}.a
)

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%{_libdir}/*.a
%{_libdir64}/*.a

%files devel
%defattr(-,root,system,-)
%{_includedir}/*.h


%changelog
* Thu Aug 12 2021 Clement Chigot <clement.chigot@atos.net> - 1.3-1
- First port for AIX
