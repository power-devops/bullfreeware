# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary:	Library for handling page faults in user mode
Name:		libsigsegv
Version: 2.14
Release: 1
Group:		System Environment/Libraries
License:	GPLv2+
URL:		http://libsigsegv.sourceforge.net/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

%description
This is a library for handling page faults in user mode. A page fault
occurs when a program tries to access to a region of memory that is
currently not available. Catching and handling a page fault is a useful
technique for implementing:
  - pageable virtual memory
  - memory-mapped access to persistent databases
  - generational garbage collectors
  - stack overflow handlers
  - distributed shared memory


%package devel
Summary:	Development libraries and header files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs to handle
page faults in user mode.

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

build_libsigsegv(){
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


build_libsigsegv %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_libsigsegv %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
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
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2

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

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 64bit/AUTHORS 64bit/ChangeLog 64bit/NEWS 64bit/README
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*


%changelog
* Sat Jan 08 2022 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.14-1
- Update to 2.14

* Fri May 21 2021 Clement Chigot <clement.chigot@atos.net> - 2.13-1
- Update to version 2.13
- BullFreeware Compatibility Improvements
- Rebuild in RPM v4


* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.10-2
- Initial port on Aix6.1

* Mon Oct 03 2011 Patricia Cugny <patricia.cugny@bull.net> - 2.10-1
- initial port of version 2.10 on AIX 5.3

