# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: A tool for determining compilation options
Name: pkg-config
Version: 0.29.2
Release: 1
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Source0:  https://pkgconfig.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

# https://bugs.freedesktop.org/show_bug.cgi?id=16095
# Patch3: pkg-config-lib64-excludes.patch
# workaround for breakage with autoconf 2.66
# https://bugzilla.redhat.com/show_bug.cgi?id=611781
# Patch4: pkg-config-dnl.patch

Obsoletes: pkgconfig < %{version}
Provides:  pkgconfig = %{version}


%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
# %patch3 -p0
# %patch4 -p1 -R

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export AR="/usr/bin/ar -X32_64"

build_pkgconfig () {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--mandir=%{_mandir} \
	--enable-shared --disable-static \
	--with-pc-path=${1}/pkgconfig \
	--with-internal-glib

    make %{?_smp_mflags} 
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_pkgconfig %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_pkgconfig %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)
cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 32bit binaries' name and make default link towards 64bit
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _32 -e _64)
    do
	mv ${f} ${f}_32
	ln -sf ${f}_64 ${f}
    done
)

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig

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
%doc 32bit/AUTHORS 32bit/README 32bit/NEWS 32bit/COPYING
%{_bindir}/*
%{_libdir}/pkgconfig
%{_libdir64}/pkgconfig
%{_datadir}/aclocal/*
%{_mandir}/man?/*


%changelog
* Mon May 31 2021 Clement Chigot <clement.chigot@atos.net> - 0.29.2-1
- Update to version 0.29.2
- BullFreeware Compatibility Improvements

* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.25-3
- Initial port on Aix6.1

* Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.25-2
- Porting on Aix5.3

