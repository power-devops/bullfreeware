# This specfile is building the libraries needed by other RPMs
# Currently:
#  - libsmartcols

# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

### Header
Summary: A collection of basic system utilities
Name: util-linux
Version: 2.36.2
Release: 1
License: GPLv2 and GPLv2+ and LGPLv2+ and BSD with advertising and Public Domain

### Macros
%define upstream_version %{version}
%define upstream_major %(eval echo %{version} | %{__sed} -e 's/\([[:digit:]]*\)\.\([[:digit:]]*\)\.[[:digit:]]*$/\1.\2/')

Source0: https://ftp.kernel.org/pub/linux/utils/util-linux/v%{upstream_major}/util-linux-%{upstream_version}.tar.xz

Source100: %{name}-%{version}-%{release}.build.log

Patch0: util-linux-2.36-include-add-support-for-asprintf-and-vasprintf.patch
Patch1: util-linux-2.36-include-remove-VDISCARD-and-VWERASE-if-not-available.patch
Patch2: util-linux-2.36-include-rename-errmsg-to-errmsgf.patch
Patch3: util-linux-2.36-lib-remove-err.h-if-not-available.patch

%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, Util-linux contains the fdisk configuration tool and the login
program.

This RPM is empty on AIX.


%package -n libsmartcols
Summary: Formatting library for ls-like programs.
License: LGPLv2+

%description -n libsmartcols
This is library for ls-like terminal programs, part of util-linux.


%package -n libsmartcols-devel
Summary: Formatting library for ls-like programs.
License: LGPLv2+
Requires: libsmartcols = %{version}-%{release}
Requires: pkgconfig

%description -n libsmartcols-devel
This is development library and headers for ls-like terminal programs,
part of util-linux.

# Remove PaxHeaders
%define __tar /opt/freeware/bin/tar

%prep
%autosetup -p1 -n %{name}-%{upstream_version}

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

export CFLAGS_COMMON="-O2"

build_util_linux(){
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \
	--disable-all-programs \
	--enable-libsmartcols

	gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_util_linux %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_util_linux %{_libdir}

%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

(
    %define libsoversion 1

    for l in libsmartcols; do
	# Extract .so from 64bit .a libraries
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x ${l}.a

	# Create 32 bits libraries with 32/64bit members
	cd ${RPM_BUILD_ROOT}%{_libdir}
	${AR} -q ${l}.a ${RPM_BUILD_ROOT}%{_libdir64}/${l}.so.%{libsoversion}
	rm ${RPM_BUILD_ROOT}%{_libdir64}/${l}.so.%{libsoversion}

	# Create links for 64 bits libraries
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	rm -f ${l}.a
	ln -sf ../lib/${l}.a ${l}.a
    done
)

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm ${RPM_BUILD_ROOT}%{_libdir64}/*.la


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# make check will try to launch everything.
# libsmartcols have been tested manually with the samples provides.
# cd 64bit
# (gmake -k check || true)

# cd ../32bit
# (gmake -k check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 64bit/AUTHORS 64bit/NEWS 64bit/README


%files -n libsmartcols
%defattr(-,root,system,-)
%doc 64bit/Documentation/licenses/COPYING.LGPL-2.1-or-later 64bit/libsmartcols/COPYING
%{_libdir}/libsmartcols.a

%files -n libsmartcols-devel
%defattr(-,root,system,-)
%{_includedir}/libsmartcols



%changelog
* Wed Sep 15 2021 Clément Chigot <clement.chigot@atos.net> - 2.36.2-1
- Adapt to provide libsmartcols to AIX

