# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64
%define  realver 3300100
%define  docrealver 3300100

Summary: Library that implements an embeddable SQL database engine
Name: 	 sqlite
Version: 3.30.1
Release: 1
License: Public Domain
Group: 	 Applications/Databases
URL: 	 http://www.sqlite.org/
Source0: http://www.sqlite.org/%{name}-src-%{realver}.zip
Source1: http://www.sqlite.org/%{name}-doc-%{docrealver}.zip
Source1000:	%{name}-%{version}-%{release}.build.log

# Support a system-wide lemon template
Patch1:  %{name}-%{version}-lemon-system-template.patch
# Shut up stupid tests depending on system settings of allowed open fd's
# Patch2:  sqlite-%{version}-stupid-openfiles-test.patch
# Patch4:  sqlite-%{version}-aix.patch

# Lemon won't have the correct LIBPATH if we do not add LDFLAGS when it's built.
Patch2:  %{name}-%{version}-Makefile-add-LDFLAGS-for-lemon.patch

Obsoletes: sqlite3 sqlite3-devel

BuildRequires: gcc
BuildRequires: make
BuildRequires: unzip
BuildRequires: zlib-devel
BuildRequires: readline-devel >= 5.2
BuildRequires: tcl >= 8.6.8-1
# Needed by configure for -e option
BuildRequires: sed


Requires: readline >= 5.2
Requires: libgcc >= 6.3.0
Requires: ncurses >= 6.1
Requires: zlib
Requires: %{name}-libs = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1


%description
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process. The distribution comes with a
standalone command-line access program (sqlite) that can be used to
administer an SQLite database and which serves as an example of how to
use the SQLite library.


%package devel
Summary: Header files and libraries for developing apps which will use sqlite.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
The sqlite-devel package contains the header files and libraries needed
to develop programs that use the sqlite database library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".

%package libs
Summary: Shared library for the sqlite3 embeddable SQL database engine.

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description libs
This package contains the shared library for %{name}.


%package doc
Summary: Documentation for sqlite
Group: Documentation

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package -n lemon
Summary: A parser generator
Group: Development/Tools

%description -n lemon
Lemon is an LALR(1) parser generator for C or C++. It does the same
job as bison and yacc. But lemon is not another bison or yacc
clone. It uses a different grammar syntax which is designed to reduce
the number of coding errors. Lemon also uses a more sophisticated
parsing engine that is faster than yacc and bison and which is both
reentrant and thread-safe. Furthermore, Lemon implements features
that can be used to eliminate resource leaks, making is suitable for
use in long-running programs such as graphical user interfaces or
embedded controllers.


%prep
%setup -q -a1 -n %{name}-src-%{realver}

export PATH=/opt/freeware/bin:$PATH

%patch1 -p1 -b .lemon-system-template
%patch2 -p1
# %patch4 -p1 -b .aix

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

# Needed by configure for -e option
export SED=/opt/freeware/bin/sed

build_sqlite(){
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--enable-shared --enable-static \
		--enable-threadsafe \
		--enable-cross-thread-connections \
		--enable-load-extension \
		--disable-tcl \


	# "correct" Makefile
	cat Makefile | sed -e "s|THREADLIB|LIBPTHREAD|" > Makefile.tmp
	mv Makefile.tmp Makefile

	gmake %{?_smp_mflags}
}


cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"


build_sqlite %{_libdir64}


# now build the 32-bit version
cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_sqlite %{_libdir}



%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"


cd 64bit
#Install 64bit version of binaries and libraries
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
cp lemon ${RPM_BUILD_ROOT}%{_bindir}/lemon
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/lemon

/usr/bin/strip -X64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
	cd  ${RPM_BUILD_ROOT}/%{_bindir}
	for fic in $(ls -1| grep -v -e _32 -e _64)
	do
             mv $fic "$fic"_64
        done
)

cd ../32bit

#install 32bit version version of binaries and libraries

export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cp lemon ${RPM_BUILD_ROOT}%{_bindir}/lemon
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/lemon

/usr/bin/strip -X32 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)

(
	# Extract .so from 64bit .a libraries and create links from /lib64 to /lib
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x libsqlite3.a
	rm -f libsqlite3.a
	ln -sf ../lib/libsqlite3.a libsqlite3.a
)


(
	# Extract and create .so files for compatibility purpose
	# TODO: remove one day
	cd ${RPM_BUILD_ROOT}%{_libdir}
	${AR} -X32 -x libsqlite3.a
	ln -sf libsqlite3.so.0 libsqlite3.so

	# 64 bit .so file already extracted
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	ln -sf libsqlite3.so.0 libsqlite3.so

)

(
	# add the 64-bit shared objects to the shared library containing already the
	# 32-bit shared objects
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libsqlite3.a  libsqlite3.so.0
)


mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
cp sqlite3.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
chmod 644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lemon
chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/lemon
cp tool/lempar.c ${RPM_BUILD_ROOT}%{_datadir}/lemon/lempar.c
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/lemon/lempar.c

# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin include lib lib64
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export SED=/opt/freeware/bin/sed

cd 64bit
$SED -i "s/^LIBTCL = $/LIBTCL = -ltcl/g" Makefile
(gmake -k test || true)

cd ../32bit
$SED -i "s/^LIBTCL = $/LIBTCL = -ltcl/g" Makefile
(gmake -k test || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/sqlite3*
%{_mandir}/man?/*
# /usr/bin/sqlite3

%files libs
%defattr(-,root,system)
%doc 32bit/README.md
%{_libdir}/*.a
%{_libdir64}/*.a
# Keep .so files for older Python versions
%{_libdir}/*.so*
%{_libdir64}/*.so*
# /usr/lib/*.a
# /usr/lib/*.so*
# /usr/lib64/*.a
# /usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_includedir}/*
# %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
# /usr/include/*
# /usr/lib/*.la


%files doc
%defattr(-,root,system)
%doc 32bit/doc/*


%files -n lemon
%defattr(-,root,system)
%{_bindir}/lemon*
%{_datadir}/lemon
# /usr/bin/lemon

%changelog
* Wed Jul 31 2019 Clément Chigot <clement.chigot@atos.net> - 3.30.1-1
- BullFreeware Compatibility Improvements
- Fix setup in %prep
- Move tests to %check
- Add symlinks between lib64 and lib
- Add sqlite-libs package
- Remove .la files
- Remove /usr links
- Add zlib-devel dependency
- Remove patch BuildRequires

* Thu May 23 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.28.0-1
- Updating to 3.28.0 to fix following CVE's
- CVE-2019-5018 CVE-2018-20346 CVE-2019-9937  CVE-2019-9936

* Thu Feb 21 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.27.1-1
- Updated to 3.27.1
- Built with gcc
- Built both 32 and 64bit binaries making 64bit default
- Created patch for renaming thread_wait function as 
- it is predifined in AIX

* Tue Apr 10 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.23.0-1
- Updated to 3.23.0-1 For security vulnerability fix. 

* Fri Dec 16 2016 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.15.2-1
- Build requires tcl >= 8.5
- Updated to 3.15.2 

* Tue Feb 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 3.715.2-2
- Add lemon package

* Fri Feb 22 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 3.715.2-1
- Update to version 3.7.15.2-1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 3.7.6.3-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 3.7.6.3-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 22 2011 Gerard Visiedo <gerard.visiedo@bull.net> 3.7.6.3-1
- Update to 3.7.6.3 

* Tue Jan 19 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.6.22-1
- Initial port for AIX

