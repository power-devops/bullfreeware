# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:       libyaml
Version:    0.2.5
Release:    1
Summary:    YAML 1.1 parser and emitter written in C
Group:      System Environment/Libraries
License:    MIT
URL:        https://pyyaml.org/
Source0:    https://pyyaml.org/download/libyaml/yaml-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.


%package devel
Summary:   Development files for LibYAML applications
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use LibYAML.


%prep
%setup -q -n yaml-%{version}

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

build_libyaml(){
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \

	gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_libyaml %{_libdir64}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_libyaml %{_libdir}


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

# Rename libyaml-0.a into libyaml.a
mv ${RPM_BUILD_ROOT}%{_libdir64}/libyaml-0.a ${RPM_BUILD_ROOT}%{_libdir64}/libyaml.a
mv ${RPM_BUILD_ROOT}%{_libdir}/libyaml-0.a ${RPM_BUILD_ROOT}%{_libdir}/libyaml.a

(
    %define libsoversion 2

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}-0.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}-0.so.%{libsoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
)

# Remove .la files
rm $RPM_BUILD_ROOT/%{_libdir}/%{name}.la
rm $RPM_BUILD_ROOT/%{_libdir64}/%{name}.la

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
%doc 32bit/License 32bit/ReadMe.md
%{_libdir}/*.a

%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/html
%{_includedir}/*


%changelog
* Fri Sep 03 2021 Clément Chigot <clement.chigot@atos.net> - 0.2.5-1
- Update to 0.2.5
- BullFreeware Compatibility Improvements

* Tue Feb 12 2013 Gerard Visiedo  <gerard.visiedo@bull.net> - 0.1.4-2
- Add omitted file yaml.pc

* Wed Jan 16 2013 Gerard Visiedo  <gerard.visiedo@bull.net> - 0.1.4-1
- Initial port on Aix6.1
