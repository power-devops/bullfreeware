# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary:	The zlib compression and decompression library
Name:		zlib
Version:	1.2.11
Release:	3
Group:		System Environment/Libraries
Source0:	http://www.zlib.net/%{name}-%{version}.tar.xz
Patch0:		%{name}-%{version}-aix-mandir.patch
Patch1:		%{name}-%{version}-aix-configure-gcc.patch
URL:		http://www.gzip.org/zlib/
License:	zlib

Source1000:	%{name}-%{version}-%{release}.build.log

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Header files and libraries for Zlib development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
echo %{_bindir} %{_mandir} %{_prefix} %{_infodir} %{_datadir} %_libexecdir
export PATH="/opt/freeware/bin:$PATH"
%setup -q
%patch0
%patch1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC="gcc"

# first build the 64-bit version
cd 64bit

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
	--64

gmake %{?_smp_mflags}

# Remove the static library and replace it with a shared one.
rm libz.a
${AR} -q libz.a libz.so.1

# add AIX Toolbox compatibility member for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e').
cp libz.so.1 shr_64.o
/usr/bin/strip -X64 -e shr_64.o
${AR} -q libz.a ./shr_64.o



# now build the 32-bit version
cd ../32bit
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \

gmake %{?_smp_mflags}

# Remove the static library and replace it with a shared one.
rm libz.a
${AR} -q libz.a libz.so.1

# add AIX Toolbox compatibility member for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e').
cp libz.so.1 shr.o
/usr/bin/strip -X32 -e shr.o
${AR} -q libz.a ./shr.o


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..


(
	# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x ${RPM_BUILD_ROOT}%{_libdir64}/libz.a	libz.so.1
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libz.a		${RPM_BUILD_ROOT}%{_libdir64}/libz.so.1
	${AR} -x ${RPM_BUILD_ROOT}%{_libdir64}/libz.a	shr_64.o
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libz.a		${RPM_BUILD_ROOT}%{_libdir64}/shr_64.o
	rm ${RPM_BUILD_ROOT}%{_libdir64}/shr_64.o
)

(
	# Add a sym link from 64bit to 32bit libz.a
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	rm libz.a
	ln -s ../lib/libz.a .
)

# Create links for /usr/lib/libz.a because, ssh in AIX 6.1 needs it...
(
	mkdir -p ${RPM_BUILD_ROOT}/usr/lib
	cd ${RPM_BUILD_ROOT}/usr/lib
	ln -sf ../..%{_libdir}/libz.a .
)


# strip shared object
/usr/bin/strip -X64 -e ${RPM_BUILD_ROOT}%{_libdir64}/libz.so.1
/usr/bin/strip -X32 -e ${RPM_BUILD_ROOT}%{_libdir}/libz.so.1

%check
%if %{with dotests}
cd 64bit
( gmake -k check || true )
cd ../32bit
( gmake -k check || true )
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/README 32bit/ChangeLog 32bit/FAQ
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/README 32bit/doc/algorithm.txt 32bit/test/minigzip.c 32bit/test/example.c
%{_libdir}/pkgconfig/zlib.pc
%{_includedir}/*
%{_mandir}/man3/*


%changelog
* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net> - 1.2.11-3
- BullFreeware Compatibility Improvements
- Remove BuildRoot
- Remove /usr links except /usr/lib/zlib.a (needed by ssh)

* Fri Jul 19 2019 Clément Chigot <clement.chigot@atos.net> - 1.2.11-2
- Build with gcc rather than XLC
- Strip .so

* Wed Apr 11 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.2.11-1
- New version 1.2.11
- Add sym link of 32bit libz.a to 64bit libz.a

* Mon May 09 2016 Tony Reix <tony.reix@bull.net> - 1.2.8-3
- Looks like .so files are useful... at least by openssl tests

* Wed Apr 27 2016 Tony Reix <tony.reix@bull.net> - 1.2.8-2
- Fix issues in .spec file (no more deliver .so files)
- Change 32-64 bits management

* Fri Sep 11 2015 Tony Reix <tony.reix@bull.net> - 1.2.8-1
- New version 1.2.8

* Wed Jul 24 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-6
- Confusion between libraries 32 et 64bit

* Tue Jul 16 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-5
- Add librairies .so 

* Wed Jun 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-4
- Add zlib.pc into devel package

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.5-3
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 1.2.5-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jul 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.2.5
- Initial port on Aix 5.3
