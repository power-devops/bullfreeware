# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:		fswatch
Version:	1.15.0
Release:	1
Summary:	A cross-platform file change monitor
License:	GPLv3+
URL:		https://github.com/emcrisostomo/fswatch
Source0:	%{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

# BuildRequires: autoconf automake libtool
BuildRequires: gcc-c++ gcc gettext-devel
BuildRequires: texinfo sed grep

%description
%{name} is a cross-platform file change monitor.

%package devel
Summary:	Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and headers for lib%{name}.

%prep
%autosetup -n %{name}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# ./autogen.sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

export CFLAGS="-pthread"
export CXXFLAGS="-pthread"

build_fswatch() {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--enable-shared --disable-static \

	gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"
export CXX="g++ -maix64"

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

build_fswatch %{_libdir64}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc -maix32"
export CXX="g++ -maix32"
export CFLAGS="$CFLAGS -D_LARGE_FILES"
export CXXFLAGS="$CXXFLAGS -D_LARGE_FILES"

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_fswatch %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

mv ${RPM_BUILD_ROOT}/%{_bindir}/%{name} ${RPM_BUILD_ROOT}/%{_bindir}/%{name}_64

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

# Only distribute 64bit binaries for now
mv ${RPM_BUILD_ROOT}/%{_bindir}/%{name}_64 ${RPM_BUILD_ROOT}/%{_bindir}/%{name}

mkdir $RPM_BUILD_ROOT%{_mandir}/man1/
mv $RPM_BUILD_ROOT%{_mandir}/man7/%{name}.7 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

(
    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x lib%{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.11
    rm ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.11

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f lib%{name}.a
    ln -sf ../lib/lib%{name}.a lib%{name}.a
)

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(-,root,system,-)
%doc 64bit/README.md 64bit/AUTHORS 64bit/NEWS 64bit/CONTRIBUTING.md 64bit/ABOUT-NLS
%license 64bit/COPYING
%{_bindir}/%{name}
%{_libdir}/lib{%name}.a
%{_libdir64}/lib{%name}.a
%{_mandir}/man1/%{name}.1
%{_infodir}/*info*

%files devel
%defattr(-,root,system,-)
%doc 64bit/README.libfswatch.md 64bit/AUTHORS.libfswatch 64bit/NEWS.libfswatch
%doc %{_datadir}/doc/%{name}
%{_includedir}/lib%{name}/*

%changelog
* Thu Jan 07 2021 Clément Chigot <clement.chigot@atos.net> - 1.15.0-1
- First port to AIX 7.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Darryl T. Agostinelli <dagostinelli@gmail.com> 1.14.0-3
- Corrections made for package review process

* Sun May 03 2020 Darryl T. Agostinelli <dagostinelli@gmail.com> 1.14.0-2
- Corrections made for package review process

* Sat Apr 11 2020 Darryl T. Agostinelli <dagostinelli@gmail.com> 1.14.0-1
- Created the .spec file for version 1.14.0
