# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

Summary: A utility for determining file types
Name: file
Version: 5.39
Release: 1
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/

Source10: %{name}-%{version}-%{release}.build.log

# Prevent rpmbuild to hang sometimes when building some RPMs
Patch0: %{name}-5.38-rpmbuild-hang-fix.patch
Patch1: %{name}-5.39-strip.patch

# Avoid a malloc(0) in some cases.
Patch2: %{name}-5.39-avoid-coalesce_entries-when-there-is-no-entries.patch

# Use reimplementation of strndup to avoid memory corruption
Patch3: %{name}-5.39-fix-strndup-for-aix.patch


BuildRequires: zlib-devel

%define _libdir64 %{_prefix}/lib64

Requires: %{name}-libs = %{version}-%{release}

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package libs
Summary: Libraries for applications using libmagic
Group:   Applications/File
BuildRequires: libgcc >= 8
Requires: libgcc >= 8
Requires: zlib >= 1.2.11-2
Requires: bzip2 >= 1.0.8-2
Requires: xz-libs >= 5.2.4-1

%description libs

Libraries for applications using libmagic.
The library is available as 32-bit and 64-bit.

%package devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: %{name} = %{version}-%{release}

%description devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.

%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q

%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

export CFLAGS_BASE="-D_FILE_OFFSET_BITS=64 -g"

%if %{with gcc_compiler}
export __CC="gcc"
export __CXX="g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="xlc_r"
export __CXX="xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"
%endif

build_file() {
    ./configure --prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=$1 \
		--enable-fsect-man5 \
		--disable-silent-rules
    gmake
}

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64

export CC="$__CC $FLAG64"
export CXX="$__CXX $FLAG64"
export CFLAGS="$CFLAGS_BASE"
export CXXFLAGS="$CFLAGS_BASE"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_file %{_libdir64}



# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32

export CC="$__CC $FLAG32"
export CXX="$__CXX $FLAG32"
export CFLAGS="$CFLAGS_BASE -D_LARGEFILE_SOURCE"
export CXXFLAGS="$CFLAGS_BASE -D_LARGEFILE_SOURCE"

export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_file %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

# install 64-bit version
cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/misc/magic
ln -s misc/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/%{name}/magic

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

(
    # Extract .so from 64bit .a libraries and create links from /lib64 to /lib
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for f in lib*.a ; do
	${AR} -x ${f}
	rm -f ${f}
	ln -sf ../lib/${f} ${f}
    done
)

(
    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q libmagic.a ${RPM_BUILD_ROOT}%{_libdir64}/libmagic.so.1
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libmagic.so.1
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
%doc 32bit/COPYING 32bit/ChangeLog 32bit/README
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,system,-)
%{_libdir}/*.a
%{_libdir64}/*.a
%{_datadir}/magic*
%{_mandir}/man5/*
%{_datadir}/%{name}
%{_datadir}/misc/*

%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_mandir}/man3/*


%changelog
* Fri Nov 13 2020 Clement Chigot <clement.chigot@atos.net> 5.39-1
- BullFreeware Compatibility Improvements
- Update to 5.39
- Fix a crash linked to malloc(0)
- Fix memory corruption linked to strndup

* Thu Dec 13 2018 Tony Reix <tony.reix@atos.net> 5.32-2
- Fix the issue with the rpmbuild hangs

* Fri Dec 08 2017 Michael Wilson <Michael.A.Wilson@atos.net> 5.32-1
-  update to version 5.32 on Aix 6.1

* Wed Dec 14 2016 Michael Wilson <Michael.A.Wilson@atos.net> 5.29-1
-  update to version 5.29 on Aix 6.1

* Thu Jul 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.12-2
-  update to version 5.12. on Aix5.3

* Tue Feb 12 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.12-1
- update to version 5.12. This version is mandatory for rpm manager 4.9.1.3

* Thu Mar 29 2012 Patricia Cugny <patricia.cugny@bull.net>  5.11-1
- update to version 5.11

* Fri Mar 13 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 5.00-1
- port to AIX

