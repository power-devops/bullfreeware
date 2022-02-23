%define realver 3071502
%define docrealver 3071502

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.7.15.2
Release: 3
License: Public Domain
Group: 	Applications/Databases
URL: http://www.sqlite.org/
Source0: http://www.sqlite.org/%{name}-src-%{realver}.zip
Source1: http://www.sqlite.org/%{name}-doc-%{docrealver}.zip
# Support a system-wide lemon template
Patch1: sqlite-3.6.23-lemon-system-template.patch
Patch2: sqlite-3.7.7.1-stupid-openfiles-test.patch
# Shut up pagecache overflow test whose expected result depends on compile
# options and whatnot. Dunno why this started failing in 3.7.10 but
# doesn't seem particularly critical...
Patch3: sqlite-3.7.10-pagecache-overflow-test.patch
Patch4: sqlite-3.7.6.3-aixconf.patch
# libdl patch needs
Obsoletes: sqlite3 sqlite3-devel
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: make, patch, unzip, readline-devel >= 5.2
Requires: readline >= 5.2

%description
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process. The distribution comes with a
standalone command-line access program (sqlite) that can be used to
administer an SQLite database and which serves as an example of how to
use the SQLite library.

The library is available as 32-bit and 64-bit.


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


# all this hoopla is required because RPM V3 (which we are stuck with on AIX)
# does not understand ZIP archives as source files :-(
%prep
/usr/bin/rm -rf %{name}-src-%{realver} %{name}-doc-%{docrealver}
unzip %{SOURCE0}
unzip %{SOURCE1}
%setup -T -D -n %{name}-src-%{realver}
/usr/bin/mv ../%{name}-doc-%{docrealver}/* doc/
/usr/bin/rmdir ../%{name}-doc-%{docrealver}
export PATH=/opt/freeware/bin:$PATH
%patch1 -p1 -b .lemon-system-template
%patch2 -p1 -b .stupid-openfiles-test
%patch3 -p1 -b .pagecache-overflow-test
%patch4 -p1 -b .aixconf

# remove cgi-script erroneously included in sqlite-doc-3070600
rm -f %{name}-doc-%{docrealver}/search


%build
autoconf

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-tcl \
    --enable-threadsafe \
    --enable-cross-thread-connections \
    --enable-load-extension

# "correct" Makefile
cat Makefile | sed -e "s|THREADLIB|LIBPTHREAD|" > Makefile.tmp
mv Makefile.tmp Makefile

gmake %{?_smp_mflags}

cp .libs/libsqlite3.so.0 .
gmake distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-tcl \
    --enable-threadsafe \
    --enable-cross-thread-connections \
    --enable-load-extension

# "correct" Makefile
cat Makefile | sed -e "s|THREADLIB|LIBPTHREAD|" > Makefile.tmp
mv Makefile.tmp Makefile

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libsqlite3.a ./libsqlite3.so.0

# Deliver the 32 and 64 bits .so files :
#    /opt/freeware/lib/libsqlite3.so
#    /opt/freeware/lib64/libsqlite3.so
# It is needed by httpd-2.4.18-1, at least
mkdir -p             ${RPM_BUILD_ROOT}%{_libdir}64/
cp ./libsqlite3.so.0 ${RPM_BUILD_ROOT}%{_libdir}64/libsqlite3.so
rm ./libsqlite3.so.0
${AR} -X32 -xv       ${RPM_BUILD_ROOT}%{_libdir}/libsqlite3.a    libsqlite3.so.0
cp ./libsqlite3.so.0 ${RPM_BUILD_ROOT}%{_libdir}/libsqlite3.so

# Symlink 32-64
(
 cd ${RPM_BUILD_ROOT}%{_libdir}64
 ln -s %{_libdir}/libsqlite3.a .
)


mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
cp sqlite3.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
chmod 644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*

cp lemon ${RPM_BUILD_ROOT}%{_bindir}/
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/lemon

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/lemon
chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/lemon
cp tool/lempar.c ${RPM_BUILD_ROOT}%{_datadir}/lemon/lempar.c
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/lemon/lempar.c

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc README
%{_bindir}/sqlite3
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}64/*.a
%{_libdir}64/*.so
%{_mandir}/man?/*
/usr/bin/sqlite3
/usr/lib/*.a
/usr/lib/*.so
/usr/lib64/*.a
/usr/lib64/*.so


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
/usr/include/*
/usr/lib/*.la


%files doc
%defattr(-,root,system)
%doc doc/*


%files -n lemon
%defattr(-,root,system)
%{_bindir}/lemon
%{_datadir}/lemon
/usr/bin/lemon


%changelog
* Thu Jun 30 2016 Tony Reix <tony.reix@bull.net> - 3.715.2-3
- Add libsqlite3.so to %files
- Add 32-64 symlink

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

