# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: X.509 library
Name:    libksba
Version: 1.6.0
Release: 1

# The library is licensed under LGPLv3+ or GPLv2+,
# the rest of the package under GPLv3+
License: (LGPLv3+ or GPLv2+) and GPLv3+
Group:   System Environment/Libraries
URL:     http://www.gnupg.org/
Source0: https://www.gnupg.org/ftp/gcrypt/libksba/libksba-%{version}.tar.bz2

Source10: %{name}-%{version}-%{release}.build.log

Patch1: libksba-1.3.0-multilib.patch

BuildRequires: libgpg-error-devel >= 1.36
BuildRequires: libgcrypt-devel >= 1.8.5
Requires: libgpg-error >= 1.36
Requires: libgcrypt >= 1.8.5
Requires: libgcc >= 8

%description
KSBA (pronounced Kasbah) is a library to make X.509 certificates as
well as the CMS easily accessible by other applications.  Both
specifications are building blocks of S/MIME and TLS.

%package devel
Summary: Development headers and libraries for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: info
Requires: /sbin/install-info

%description devel
%{summary}.



%prep
%setup -q
%patch1 -p1

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

export CFLAGS="-O3"

build_libksba(){
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \
	--enable-shared --disable-static \

	gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "


build_libksba %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_libksba %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

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
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.8
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.8

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
)

# Gzip info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

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


%post devel
install-info %{_infodir}/ksba.info.gz %{_infodir}/dir


%postun devel
if [ $1 -eq 0 ]; then
    install-info --delete %{_infodir}/ksba.info.gz %{_infodir}/dir
fi


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/COPYING 32bit/NEWS
%doc 32bit/README* 32bit/THANKS 32bit/TODO
%{_libdir}/*.a


%files devel
%defattr(-,root,system,-)
%{_bindir}/ksba-config
%{_includedir}/*
%{_datadir}/aclocal/*
%{_infodir}/*info*


%changelog
* Mon Jun 14 2021 Clément Chigot <clement.chigot@atos.net> - 1.6.0-1
- Update to 1.6.0
- Remove .sig from sources

* Tue Jun 08 2021 Tony Reix <tony.reix@atos.net> - 1.5.1-2
- Remove %{_infodir}/dir and deliver only %{_infodir}/*info*

* Wed Jun 02 2021 Clement Chigot <clement.chigot@atos.net> - 1.5.1-1
- Update to version 1.5.1
- BullFreeware Compatibility Improvements

* Tue Nov 07 2017 Tony Reix <tony.reix@atos.net> - 1.3.5-1
- updated to version 1.3.5

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.3.0-1
- updated to version 1.3.0

* Tue Mar 29 2011 Michael Perzl <michael@perzl.org> - 1.2.0-1
- updated to version 1.2.0

* Wed Nov 17 2010 Michael Perzl <michael@perzl.org> - 1.1.0-1
- updated to version 1.1.0

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 1.0.8-1
- updated to version 1.0.8

* Tue Sep 08 2009 Michael Perzl <michael@perzl.org> - 1.0.7-1
- updated to version 1.0.7

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 1.0.5-1
- updated to version 1.0.5

* Fri Sep 26 2008 Michael Perzl <michael@perzl.org> - 1.0.4-1
- updated to version 1.0.4

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 1.0.3-1
- updated to version 1.0.3

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 1.0.2-2
- included both 32-bit and 64-bit shared objects

* Fri Oct 05 2007 Michael Perzl <michael@perzl.org> - 1.0.2-1
- first version for AIX V5.1 and higher
