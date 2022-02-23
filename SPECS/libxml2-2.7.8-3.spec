%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.7.8
Release: 3
License: MIT
Group: 		Development/Libraries
URL: 		http://xmlsoft.org/
Source0: 	ftp://xmlsoft.org/%{name}-%{version}.tar.gz
BuildRoot: 	/var/tmp/%{name}-%{version}-%{release}-root
BuildRequires:	python python-devel
Requires: 	zlib
BuildRequires:	zlib-devel
Prefix:		%{_prefix}
Docdir:		%{_docdir}

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
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	zlib-devel
Requires:	pkg-config

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
Requires: libxml2 = %{version}
Requires: python

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

%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
export OBJECT_MODE=64

perl -pi -e "s|--ldflags|--libs|g;" configure

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib:/usr/lib64" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make 
cp .libs/%{name}.so.2 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
export OBJECT_MODE=32

LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make 

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/%{name}.a ./%{name}.so.2

gzip -9 ChangeLog


%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(cd doc/examples ; make clean ; rm -rf .deps)
rm -f doc/examples/index.py
gzip -9 doc/%{name}-api.xml

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  [ -d usr/include/libxml2/libxml ] || mkdir -p usr/include/libxml2/libxml
  cd usr/include/libxml2/libxml
  ln -sf ../../../..%{_prefix}/include/libxml2/libxml/* .
  cd -
  [ -d usr/share ] || mkdir -p usr/share
  cd usr/share
  for dir in include aclocal doc gtk-doc man
  do
        case $dir in
         aclocal|doc) mkdir $dir
                      cd $dir
                      ln -sf ../../..%{_prefix}/share/${dir}/* .
                      cd -
                      ;;
            gtk-doc)  mkdir -p gtk-doc/html/libxml2
                      cd gtk-doc/html/libxml2
                      ln -sf ../../../../..%{_prefix}/share/gtk-doc/html/libxml2/* .
                      cd -
                      ;;
                man)   mkdir -p man/man1 man/man3
                      cd man/man1
                      ln -sf ../../../..%{_prefix}/share/man/man1/* .
                      cd ../man3
                      ln -sf ../../../..%{_prefix}/share/man/man3/* .
                      cd ../../
                      ;;
        esac
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%postun
ln -sf /usr/ccs/lib/libxml2.a /usr/lib/libxml2.a


%files
%defattr(-,root,system)
%doc AUTHORS ChangeLog.gz NEWS README Copyright TODO
%{_libdir}/lib*.a
%{_mandir}/man1/xmllint.1
%{_mandir}/man1/xmlcatalog.1
%{_bindir}/xmlcatalog
%{_bindir}/xmllint
/usr/bin/xmlcatalog
/usr/bin/xmllint


%files devel
%defattr(-,root,system)
%doc AUTHORS ChangeLog.gz NEWS README Copyright TODO
%doc doc/*.html doc/html doc/*.gif doc/*.png
%doc doc/tutorial doc/%{name}-api.xml.gz
%doc doc/examples
%doc %{_datadir}/gtk-doc/html/%{name}/*.devhelp
%doc %{_datadir}/gtk-doc/html/%{name}/*.html
%doc %{_datadir}/gtk-doc/html/%{name}/*.png
%doc %{_datadir}/gtk-doc/html/%{name}/*.css
%{_bindir}/xml2-config
/usr/bin/xml2-config
%{_includedir}/libxml2/libxml/*
%{_libdir}/lib*.la
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_mandir}/man1/xml2-config.1
%{_mandir}/man3/libxml.3
%{_datadir}/aclocal/libxml.m4
/usr/include/libxml2/libxml/*
/usr/lib/*.sh

%files python
%defattr(-, root, system)
%doc AUTHORS ChangeLog.gz NEWS README Copyright
%{_libdir}/python*/site-packages/libxml2.py*
%{_libdir}/python*/site-packages/libxml2mod*
%{_libdir}/python*/site-packages/drv_libxml2.py*
%{_datadir}/doc/%{name}-python-%{version}/examples/*
%doc python/TODO
%doc python/libxml2class.txt
%doc python/tests/*.py
%doc doc/*.py
%doc doc/python.html


%changelog
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
