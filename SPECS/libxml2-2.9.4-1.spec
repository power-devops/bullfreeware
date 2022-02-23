%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.4
Release: 1
License: MIT
Group:		Development/Libraries
URL:		http://xmlsoft.org/
Source0:	ftp://xmlsoft.org/%{name}-%{version}.tar.gz
# http://www.w3.org/XML/Test/xmlts20080827.tar.gz
Source1:        libxml2-xmlts20080827.tar.gz
Patch0:         %{name}-%{version}-continue-tests-after-error.aix.patch
BuildRoot:	/var/tmp/%{name}-%{version}-%{release}-root
BuildRequires:	zlib-devel
BuildRequires:	python-devel >= 2.7
Requires:	zlib
Requires:       libiconv

Prefix:         %{_prefix}
Docdir:         %{_docdir}
%define _libdir64 %{_prefix}/lib64

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
Requires: zlib-devel
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
Requires: python >= 2.7

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
perl -pi -e "s|--ldflags|--libs|g;" configure

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -B"

export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

export CC32="/usr/vac/bin/xlc_r"
export CXX32="/usr/vacpp/bin/xlC_r"
export CC64="$CC32 -q64"
export CXX64="$CXX32 -q64"

export CFLAGS="-D_LARGE_FILES=1"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="$CC64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/lib"
LIBPATH="%{_prefix}/lib64:%{_libdir}:/usr/lib/lib64:/usr/lib" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir64} \
	--mandir=%{_mandir} \
	--enable-shared \
	--disable-static \
	--with-python=%{_bindir}/python_64

gmake %{?_smp_mflags}
if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi
/usr/sbin/slibclean
cd ..

# build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CC="$CC32"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--enable-shared \
	--disable-static \
        --with-python=%{_bindir}/python

gmake %{?_smp_mflags}
if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi
/usr/sbin/slibclean
gzip --best ChangeLog
cd ..


%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && ${RM} ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}

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

(cd doc/examples ; make clean ; rm -rf .deps)
rm -f doc/examples/index.py
gzip --best doc/%{name}-api.xml

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p usr/include/libxml2/libxml
  cd usr/include/libxml2/libxml
  ln -sf ../../../..%{_prefix}/include/libxml2/libxml/* .
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%postun
ln -sf /usr/ccs/lib/libxml2.a /usr/lib/libxml2.a


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog.gz 32bit/NEWS
%doc 32bit/README 32bit/Copyright 32bit/TODO
%{_bindir}/xmlcatalog*
%{_bindir}/xmllint*
%{_libdir}/lib*.a
%{_libdir}/lib*.so*
%{_libdir64}/lib*.so*
%{_mandir}/man1/xmllint.1
%{_mandir}/man1/xmlcatalog.1
/usr/bin/xmlcatalog*
/usr/bin/xmllint*
/usr/lib/lib*.a
/usr/lib/lib*.so*
/usr/lib64/lib*.so*


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
%{_libdir}/lib*.la
%{_libdir64}/lib*.la
%{_libdir}/*.sh
%{_libdir64}/*.sh
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_mandir}/man1/xml2-config.1
%{_mandir}/man3/libxml.3
%{_datadir}/aclocal/libxml.m4
/usr/bin/xml2-config*
/usr/include/*
/usr/lib/lib*.la
/usr/lib64/lib*.la
/usr/lib/*.sh
/usr/lib64/*.sh


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

*  Fri Jul 11 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.7.8-1
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

