# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

%define _defaultdocdir %{_prefix}/doc

%define _libdir64 %{_prefix}/lib64

%global _smp_mflags -j4

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.10
Release: 1
License: MIT
Group:		Development/Libraries
URL:		http://xmlsoft.org/
Source0:	ftp://xmlsoft.org/%{name}-%{version}.tar.gz
# See http://www.w3.org/XML/Test/ for downloading last version of Conformance Test Suites
# OLD	Source1:        libxml2-xmlts20080827.tar.gz
Source1:        libxml2-xmlts20130923.tar.gz
Source1000:	%{name}-%{version}-%{release}.build.log

Patch0: %{name}-%{version}-continue-tests-after-error.aix.patch
# Patches used by hand
Source2: %{name}-%{version}-python-64bit.patch
Source3: %{name}-%{version}-python-32bit.patch

BuildRequires: libiconv >= 1.14-1
BuildRequires: python-devel >= 2.7.15
BuildRequires: xz-devel >= 5.2.2-1
BuildRequires: zlib-devel >= 1.2.11-1
Requires: libiconv >= 1.14-1
Requires: xz-libs >= 5.2.2-1
Requires: zlib >= 1.2.11-1
Requires: libgcc >= 6.3.0-1

Prefix:         %{_prefix}
Docdir:         %{_docdir}


%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: xz-devel >= 5.2.2-1
Requires: pkg-config

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%package python
Summary: Python bindings for the libxml2 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python >= 2.7.15
Requires: libffi >= 3.2.1-2
Requires: libgcc >= 6.3.0-1
Requires: ncurses >= 6.1-1
Requires: xz-libs >= 5.2.3-1
Requires: sqlite >= 3.27.1
Requires: expat >= 2.2.6

%description python
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.


%prep
%setup -q
%patch0 -p1 -b .test
tar xf %{SOURCE1}

# Hummmmmmmmmm That was used with 2.9.4 but... it generates an issue with 2.9.9 .
#	perl -pi -e "s|--ldflags|--libs|g;" configure

# Duplicate source for 32 & 64 bits
rm -rf ../%{name}-%{version}-32bit
mkdir  ../%{name}-%{version}-32bit
mv *   ../%{name}-%{version}-32bit
mkdir 32bit
mv     ../%{name}-%{version}-32bit/* 32bit
rm -rf ../%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -B"

export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

export CC="gcc"
export CXX="g++"

export _CFLAGS="-D_LARGE_FILES=1"

export GMAKE_TRACE="--trace"
export GMAKE_TRACE=""

build_libxml2() {
set -x
	LIBPATH=$1 \
	./configure \
		--prefix=%{_prefix} \
		--libdir=$2 \
		--mandir=%{_mandir} \
		--enable-shared \
		--disable-static \
		--with-python=%{_bindir}/$3 \
	    --with-lzma=/opt/freeware

	/opt/freeware/bin/patch -p0 < $4

	gmake $GMAKE_TRACE %{?_smp_mflags}
}


cd 64bit
# first build the 64-bit version
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "
export OBJECT_MODE=64
export CFLAGS="$_CFLAGS -maix64"

#build_libxml2 "%{_prefix}/lib64:%{_libdir}:/usr/lib64:/usr/lib" %{_libdir64} python2_64 %{SOURCE2}
build_libxml2 "" %{_libdir64} python2_64 %{SOURCE2}

/usr/sbin/slibclean
cd ..

# build the 32-bit version
cd 32bit
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
export CFLAGS="$_CFLAGS -maix32"

#build_libxml2 "%{_libdir}:/usr/lib" %{_libdir} python2_32 %{SOURCE3}
build_libxml2 "" %{_libdir} python2_32 %{SOURCE3}

/usr/sbin/slibclean
gzip --best ChangeLog


%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && ${RM} ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

BINFILES="xmlcatalog xmllint"

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in $BINFILES
  do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in $BINFILES
  do
    mv ${f} ${f}_32
  done
)

# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in $BINFILES
  do
    ln -sf ${f}_64 ${f}
  done
)

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

(
  cd ${RPM_BUILD_ROOT}%{_libdir}/python*/site-packages
  /usr/bin/ar -X32 -x libxml2mod.a

  cd ${RPM_BUILD_ROOT}%{_libdir64}/python*/site-packages
  /usr/bin/ar -X64 -x libxml2mod.a
)

(pwd ; cd doc/examples ; make clean ; rm -rf .deps)
# doc/libxml2-api.xml is compressed for %file stage
# But it is required for 32&64bit tests
rm -f doc/examples/index.py
cp          doc/%{name}-api.xml      doc/%{name}-api.xml.save
gzip --best doc/%{name}-api.xml
mv          doc/%{name}-api.xml.save doc/%{name}-api.xml

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -sf ../lib/%{name}.a .
)

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
# Do not change /usr/lib/libxml2.a (symlink to: /usr/ccs/lib/libxml2.a) !
    for f in ../..%{_prefix}/${dir}/*
    do
      b=`/usr/bin/basename $f`
      if [ ! \( "$dir" == "lib" -a "$b" == "libxml2.a" \) ]
      then
        ln -sf $f .
      fi
    done
    cd -
  done

  mkdir -p usr/include/libxml2/libxml
  cd usr/include/libxml2/libxml
  ln -sf ../../../..%{_prefix}/include/libxml2/libxml/* .
)

# No more .la in .rpm files
rm ${RPM_BUILD_ROOT}%{_libdir}/python*/site-packages/libxml2mod.la
rm ${RPM_BUILD_ROOT}%{_libdir64}/python*/site-packages/libxml2mod.la

# Replace /usr/bin/python by ... in doc/libxml2-python-2.9.10/*.py files.
pwd
find . -name "*.py" | xargs /opt/freeware/bin/sed -i "s|/usr/bin/python|/usr/bin/env python2|"


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# LDFLAGS (for link) and LIBPATH (for execution) are changed
#   in order to use the new libxml2 libraries instead of the installed ones

cd 64bit
export LDFLAGS_="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "
(gmake --trace -k check LDFLAGS="-L%{_builddir}/%{name}-%{version}/64bit/.libs -L%{_builddir}/%{name}-%{version}/64bit/python/.libs $LDFLAGS_" LIBPATH="%{_builddir}/%{name}-%{version}/64bit/.libs:%{_builddir}/%{name}-%{version}/64bit/python/.libs" || true)
(pwd ; cd doc/examples ; make clean ; rm -rf .deps)

cd ../32bit
export LDFLAGS_="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
(gmake --trace -k check LDFLAGS="-L%{_builddir}/%{name}-%{version}/32bit/.libs -L%{_builddir}/%{name}-%{version}/32bit/python/.libs $LDFLAGS_" LIBPATH="%{_builddir}/%{name}-%{version}/32bit/.libs::%{_builddir}/%{name}-%{version}/32bit/python/.libs" || true)
(pwd ; cd doc/examples ; make clean ; rm -rf .deps)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog.gz 32bit/NEWS
%doc 32bit/README 32bit/Copyright 32bit/TODO
%{_bindir}/xmlcatalog*
%{_bindir}/xmllint*
%{_libdir}/lib*.a
%{_libdir64}/lib*.a
%{_mandir}/man1/xmllint.1
%{_mandir}/man1/xmlcatalog.1


%files devel
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog.gz 32bit/NEWS
%doc 32bit/README 32bit/Copyright 32bit/TODO
%doc 32bit/doc/*.html 32bit/doc/html 32bit/doc/*.gif 32bit/doc/*.png
%doc 32bit/doc/tutorial 32bit/doc/%{name}-api.xml.gz
%doc 32bit/doc/examples
%doc %{_datadir}/gtk-doc/html/%{name}/*.devhelp
%doc %{_datadir}/gtk-doc/html/%{name}/*.html
%doc %{_datadir}/gtk-doc/html/%{name}/*.png
%doc %{_datadir}/gtk-doc/html/%{name}/*.css
%{_bindir}/xml2-config*
%{_includedir}/*
%{_libdir}/*.sh
%{_libdir64}/*.sh
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_mandir}/man1/xml2-config.1
%{_mandir}/man3/libxml.3
%{_datadir}/aclocal/libxml.m4


%files python
%defattr(-,root,system)
%doc 32bit/python/TODO
%doc 32bit/python/libxml2class.txt
%doc 32bit/python/tests/*.py
%doc 32bit/doc/*.py
%doc 32bit/doc/python.html
%{_libdir}/python*/site-packages/libxml2.py*
%{_libdir64}/python*/site-packages/libxml2.py*
%{_libdir}/python*/site-packages/drv_libxml2.py*
%{_libdir64}/python*/site-packages/drv_libxml2.py*
%{_libdir}/python*/site-packages/libxml2mod.*
%{_libdir64}/python*/site-packages/libxml2mod.*


%changelog
* Tue Jan 07 2020 Tony Reix <tony.reix@atos.net> - 2.9.10-1
- Update to 2.9.10
- Fix tests issues (use of installed libxml2.a instead of new one)
- Add build.log file
- Move tests in %check
- Clean  doc/example after testing
- Add build_libxml2() routine
- Move from python to python2
- Use version 20130923 of XML W3C Conformance Test Suite
  from: https://www.w3.org/XML/Test/

* Tue Jan 07 2020 Tony Reix <tony.reix@atos.net> - 2.9.9-1
- Update to 2.9.9
- Merge with AIX ToolBox changes 

* Thu Oct 20 2016 Tony Reix <tony.reix@atos.net> - 2.9.4-2
- No more create /usr/lib/libxml2.a which is already a symlink to /usr/ccs/lib/libxml2.a
  created by LPP bos.rte.control

* Fri Jun 17 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.9.4-1
- Update to 2.9.4

* Wed Jun 19 2013  Gerard Visiedo <gerard.visiedo@bull.net> - 2.9.1-1
- Update to 2.9.1

* Fri Jul 27 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.8.0-1
- Update to 2.8.0-1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.7.8-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.7.8-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Mon Jul 11 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.7.8-1
-  Update to 2.7.8-1

*  Wed Nov 17 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.7.7-2
-  changes on the packaging

*  Wed Sep 22 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.7.7-1
-  Updated to release 2.7.7

*  Tue Aug 04 2009 BULL 2.7.3-1
-  Updated to release 2.7.3

*  Wed Nov 15 2006  BULL
 - Release  1
 - New version  version: 2.6.26

*  Mon Sep 18 2006  BULL
 - Release  3
 - New version  version: 2.6.23
 - support 64 bits

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 2.6.21

*  Wed Aug 10 2005  BULL
 - Release  3
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
 - correct libxml2.a member to libxml2.so.2

*  Wed May 11 2005  BULL
 - Release  1
 - New version  version: 2.6.17

