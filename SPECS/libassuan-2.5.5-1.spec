# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

%define _libdir64 %{_prefix}/lib64

Name:    libassuan
Summary: GnuPG IPC library
Group:   System Environment/Base
Version: 2.5.5
Release: 1

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
Source0: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
URL:     https://gnupg.org/software/libassuan/index.html

Source10: %{name}-%{version}-%{release}.build.log

Patch1:  libassuan-2.5.2-multilib.patch
Patch2:  libassuan-2.5.5-coverity.patch

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.36-1
Requires: libgcc >= 8, libgpg-error >= 1.36-1

%description
This is the IPC library used by GnuPG 2, GPGME and a few other packages.


%package devel 
Summary: GnuPG IPC library 
Group: System Environment/Base
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other packages.

This package contains files needed to develop applications using %{name}.


%prep
%setup -q

%patch1 -p1
%patch2 -p1

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
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{with gcc_compiler}
export CC__="gcc"
export FLAG32=" -O2 -maix32"
export FLAG64=" -O2 -maix64"

%else
export CC__="xlc_r"
export FLAG32="-q32"
export FLAG64="-q64"

%endif

build_libassuan () {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--includedir=%{_includedir}/libassuan2

    gmake %{?_smp_mflags}
}
export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"



# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC__} ${FLAG64}"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

build_libassuan %{_libdir64}


# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC__} ${FLAG32}"
export CFLAGS="-D_LARGE_FILES"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_libassuan %{_libdir}

# # Archive 64 bit shared object in 32 bit shared library

# slibclean
# ${AR} -q src/.libs/libassuan.a ../64bit/src/.libs/libassuan.so.%{libassuan_version}

# slibclean

# strip -e -X32_64     src/.libs/libassuan.so.%{libassuan_version} ../64bit/src/.libs/libassuan.so.%{libassuan_version}




%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.0
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.0

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
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


%post devel
/sbin/install-info %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :

%preun devel
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/assuan.info %{_infodir}/dir &>/dev/null || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
#%license COPYING COPYING.LIB
%doc 32bit/COPYING 32bit/COPYING.LIB
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/NEWS 32bit/README
%doc 32bit/THANKS 32bit/TODO
%{_libdir}/libassuan.a
%{_libdir64}/libassuan.a


%files devel
%{_bindir}/libassuan-config
%defattr(-,root,system,-)
%{_includedir}/libassuan2/
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Wed Jun 02 2021 Clement Chigot <clement.chigot@atos.net> - 2.5.5-1
- Update to version 2.5.5
- BullFreeware Compatibility Improvements

* Wed Oct 10 2018 Michael Wilson <michael.a.wilson@atos.com> - 2.5.1-1
- Add 64 bit library (required for 64 bit gpgme)
- Removed Fedora changelog as the notes contained no useful information

* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 2.4.3-1
- Port on AIX

