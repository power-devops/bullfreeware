# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:           zstd
Version:        1.5.0
Release:        1
Summary:        Zstd compression library

License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

Patch0: %{name}-1.5.0-Makefile-add-AIX-support.patch
Patch1: %{name}-1.5.0-lib-avoid-weak-attribute-on-AIX.patch
Patch2: %{name}-1.5.0-test-avoid-dev-full-on-AIX.patch

# For testing
BuildRequires: diffutils

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%package -n lib%{name}
Summary:        Zstd shared library

%description -n lib%{name}
Zstandard compression shared library.

%package -n lib%{name}-devel
Summary:        Header files for Zstd library
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstd library.


%prep
%setup -q
%patch0 -p1
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

export CFLAGS_COMMON="-O2"

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

gmake prefix=%{prefix} libdir=%{_libdir64} mandir=%{_mandir}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

gmake prefix=%{prefix} libdir=%{_libdir} mandir=%{_mandir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit

# Export same variable than in %build because there isn't any configure
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "
make DESTDIR=${RPM_BUILD_ROOT} install prefix=%{_prefix} libdir=%{_libdir64} mandir=%{_mandir}

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)

cd ../32bit
# Export same variable than in %build because there isn't any configure
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir}
cd ..

# Only provide 64bit version for commands.
(
    # Replace 32bit command by 64bit version
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _64)
    do
	mv ${f}_64 ${f}
    done
)

(
    %define libsoversion 1

    # Remove static lib
    rm ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.a
    rm ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q lib%{name}.a lib%{name}.so.%{libsoversion}
    ${AR} -q lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so*
    rm ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so*

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/lib%{name}.a lib%{name}.a
)

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
# Export same variable than in %build because there isn't any configure
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

# Some RoundTripTests will failed without this ulimit
ulimit -d unlimited

(
    cd tests
    gmake -k check && echo "ZSTD TESTS: 64BIT OK" || true
)

cd ../32bit
# Export same variable than in %build because there isn't any configure
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "
export OBJECT_MODE=32
(
    cd tests
    gmake -k check && echo "ZSTD TESTS: 32BIT OK" || true
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 64bit/CHANGELOG 64bit/README.md
%{_bindir}/*
%{_mandir}/man1/*
%license 64bit/COPYING 64bit/LICENSE

%files -n lib%{name}
%defattr(-,root,system,-)
%{_libdir}/libzstd.a
%{_libdir64}/libzstd.a
%license 64bit/COPYING 64bit/LICENSE

%files -n lib%{name}-devel
%defattr(-,root,system,-)
%{_includedir}/*.h


%changelog
* Mon Aug 02 2021 Clément Chigot <clement.chigot@atos.net> - 1.5.0-1
- Port to version 1.5.0
- BullFreeware Compatibility Improvements

* Mon Jan 13 2020 sangamesh Mallayya <smallayy@in.ibm.com> 1.4.3dev-1
- Initial port to AIX.

* Wed Jul 31 2019 Pádraig Brady <P@draigBrady.com> - 1.4.2-1
- Latest upstream

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Pádraig Brady <P@draigBrady.com> - 1.4.0-1
- Latest upstream

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 31 2018 Pádraig Brady <P@draigBrady.com> - 1.3.8-1
- Latest upstream

* Mon Oct 08 2018 Pádraig Brady <P@draigBrady.com> - 1.3.6-1
- Latest upstream

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Pádraig Brady <P@draigBrady.com> - 1.3.5.1
- Latest upstream

* Wed Mar 28 2018 Pádraig Brady <P@draigBrady.com> - 1.3.4-1
- Latest upstream

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.3-2
- Switch to %%ldconfig_scriptlets

* Thu Dec 21 2017 Pádraig Brady <P@draigBrady.com> - 1.3.3-1
- Latest upstream

* Fri Nov 10 2017 Pádraig Brady <P@draigBrady.com> - 1.3.2-1
- Latest upstream

* Mon Aug 21 2017 Pádraig Brady <P@draigBrady.com> - 1.3.1-1
- Latest upstream

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 16 2017 Pádraig Brady <P@draigBrady.com> - 1.3.0-1
- Latest upstream

* Mon May 08 2017 Pádraig Brady <P@draigBrady.com> - 1.2.0-1
- Latest upstream

* Mon Mar 06 2017 Pádraig Brady <P@draigBrady.com> - 1.1.3-1
- Latest upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 02 2016 Pádraig Brady <pbrady@redhat.com> - 1.1.1-1
- Latest upstream

* Thu Oct 6  2016 Pádraig Brady <pbrady@fb.com> 1.1.0-2
- Add pzstd(1)

* Thu Sep 29 2016 Pádraig Brady <pbrady@fb.com> 1.1.0-1
- New upstream release
- Remove examples and static lib

* Mon Sep 12 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-2
- Adjust various upstream links
- Parameterize various items in spec file

* Mon Sep 5 2016 Pádraig Brady <pbrady@fb.com> 1.0.0-1
- Initial release
