# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name: libunistring
Version: 0.9.10
Release: 2
Group: System Environment/Libraries
Summary: GNU Unicode string library
License: LGPLv3+
URL: http://www.gnu.org/software/libunistring/
Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz

# Keep for BullFreeware only
Source2: %{name}.so.0-0.9.3.-aix64
Source3: %{name}.so.0-0.9.3.-aix32

Source100: %{name}-%{version}-%{release}.build.log


# In order to create libunistring.info.gz
BuildRequires: gzip

Requires: info
Requires: libgcc >= 6.3.0-1

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

The library is available as 32-bit and 64-bit.


%package devel
Group: Development/Libraries
Summary: GNU Unicode string library - development files
Requires: %{name} = %{version}-%{release}
#Requires : libiconv >=  1.14-1
%description devel
Development files for programs using libunistring.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

export CFLAGS="-O3"

build_libunistring(){
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


build_libunistring %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_libunistring %{_libdir}


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
    ${AR} -q %{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2
	rm ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2

	# Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
	rm -f %{name}.a
	ln -sf ../lib/%{name}.a %{name}.a
)


# Add the previous versions for compatibility
cp %{SOURCE2}                                                %{name}.so.0
/usr/bin/strip -X64 -e                                       %{name}.so.0
${AR}          -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0
cp %{SOURCE3}                                                %{name}.so.0
/usr/bin/strip -X32 -e                                       %{name}.so.0
${AR}          -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0

rm   -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*
rm   -f $RPM_BUILD_ROOT/%{_libdir}/%{name}.la

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
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/NEWS 32bit/README
%{_libdir}/*.a

%files devel
%defattr(-,root,system,-)
%doc 32bit/HACKING 32bit/DEPENDENCIES 32bit/THANKS 32bit/ChangeLog
%doc %{_datadir}/doc/%{name}
%{_includedir}/unistring
%{_includedir}/*.h
%{_infodir}/*info*


%changelog
* Fri Sep 18 2020 Clement Chigot <clement.chigot@atos.net> - 0.9.10-2
- Remove --disable-rpath option from configure

* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net> - 0.9.10-1
- BullFreeware Compatibility Improvements
- Move tests to %check section
- Fix configure for AIX shared libraries
- Old shared object are kept for BullFreeware

* Mon Nov 19 2018 Harshita Jain <harjain9@in.ibm.com> -0.9.9-2
- Built with libiconv support

* Fri Jun 08 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 0.9.9-1
- Added build.log.
- Built with gcc-6.3.0
- Updated to 0.9.9 Removed compatibility as we
- dont have approval for older version

* Fri Apr 29 2016 Tony Reix <tony.reix@bull.net> - 0.9.6-2
- Initial port on AIX 6.1 - Add compatibility

* Fri Apr 29 2016 Tony Reix <tony.reix@bull.net> - 0.9.3-2
- Fix bug with 64bits : add -q64 for xlc

* Thu Nov 13 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.3-1
- First version for Aix6.1
