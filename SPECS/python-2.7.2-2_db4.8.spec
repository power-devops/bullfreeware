#########################
#  User-modifiable configs
##########################
#  Build tkinter?
#WARNING: Commenting out doesn't work.  Last line is what's used.
%define config_tkinter no
%define config_tkinter yes

#################################
#  End of user-modifiable configs
#################################
%define name python
%define version 2.7.2
%define BASE_VERSION 2.7
%define release 2

#  kludge to get around rpm <percent>define weirdness
%define include_tkinter %(if [ "%{config_tkinter}" = yes ]; then echo 1; else echo 0; fi)

%define BASE_VERSION 2.7

%define libdir64 %{_prefix}/lib64

Summary: An interpreted, interactive, object-oriented programming language.
Name: %{name}
Version: %{version}
Release: %{release}
License: Modified CNRI Open Source License
Group: Development/Languages
URL: http://www.python.org/
Source0: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.bz2
Source1: http://www.python.org/ftp/python/doc/%{version}/%{name}-%{version}-docs-html.tar.bz2
Source2: pyconfig.h
Patch0: Python-%{version}-aix.patch
Patch1: Python-%{version}-aixsetup.patch
Patch2: Python-%{version}-termios.patch
Patch3: Python-%{version}-64bit.patch


Provides: python-abi = %{BASE_VERSION}
Provides: python(abi) = %{BASE_VERSION}
Provides: python2 = %{version}

BuildRequires: readline-devel >= 5.2, openssl-devel >= 0.9.8, gmp-devel
BuildRequires: gdbm-devel, zlib-devel, expat-devel
BuildRequires: tcl tcl-devel tk tk-devel bzip2-devel pkg-config
BuildRequires: sqlite-devel db-devel >= 4.7

BuildRequires: make
Requires: readline >= 5.2, openssl >= 0.9.8, gmp
Requires: gdbm, zlib, expat >= 2.0.0
Requires: bzip2, sqlite, db >= 4.6.0

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%define osplat aix5
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif


%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface. This package contains most of the standard
Python modules, as well as modules for interfacing to the Tix widget
set for Tk and RPM.

Note that documentation for Python is provided in the python-docs
package.


#%package libs
#Summary: The libraries for python runtime
#Group: Applications/System
#Requires: %{name} = %{version}-%{release}

#%description libs
#The python interpreter can be embedded into applications wanting to 
#use python as an embedded scripting language.  The python-libs package 
#provides the libraries needed for this.


%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Conflicts: %{name} < %{version}-%{release}

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.


%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: tkinter = %{version}-%{release}

%description tools
The Python package includes several development tools that are used
to build python programs.

%if %{include_tkinter}
%package -n tkinter
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
BuildRequires: tcl-devel, tk-devel
Requires: tcl, tk
Requires: %{name} = %{version}-%{release}

%description -n tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.
%endif


%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.


%prep
%setup -q -n Python-%{version}
%patch0 -p1 -b .aix
%patch1 -p1 -b .aixsetup
%patch2 -p1 -b .termios

mkdir ../32bit
mv * ../32bit
mv .hg* ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/
cd 64bit
%patch3 -p1 -b .64bit

# A couple of one-liner patches, on the fly.
perl -pi -e "s|yperr_string|(const char*)yperr_string|g;" \
  Modules/nismodule.c

%setup -q -D -T -a 1 -n Python-%{version} -q

%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# build 64-bit version
export CC="/usr/vac/bin/xlc -q64"
export CXX='/usr/vacpp/bin/xlC_r -q64'
export CONFIG_SHELL=%{_prefix}/bin/bash
export CONFIGURE_ENV_ARGS=%{_prefix}/bin/bash
export CPPFLAGS="-I/usr/include"
export OBJECT_MODE=64
export LDFLAGS="-L%{libdir64} -L%{_libdir}"
export LIBS="-lbsd -lsqlite3 -lncurses -lexpat -lffi"
cd 64bit
LIBPATH="`pwd`:/usr/lib/threads:%{_prefix}/lib64:%{_libdir}:/usr/lib:/usr/lib64" \
CPPFLAGS="-I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses" \
LDFLAGS="-L. -L%{libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{libdir64} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir} \
    --with-gcc="/usr/vac/bin/xlc_r -ma -q64 -qmaxmem=16384 -DAIX_GENUINE_CPLUSCPLUS -Wl,-brtl -lbsd" \
    --with-cxx-main="/usr/vacpp/bin/xlC_r -ma -q64 -qmaxmem=16384 -DAIX_GENUINE_CPLUSCPLUS -Wl,-brtl -lbsd" \
    --enable-shared \
    --disable-ipv6 \
    --with-threads \
    --with-system-ffi \
    --with-system-expat \
    OPT="-O"

make lib%{name}%{BASE_VERSION}.a

/usr/vac/bin/CreateExportList -X64 lib%{name}.exp lib%{name}%{BASE_VERSION}.a
/usr/vac/bin/xlc_r -q64 -qmkshrobj lib%{name}%{BASE_VERSION}.a \
	-o lib%{name}%{BASE_VERSION}.so -bE:lib%{name}.exp -lm
rm -f lib%{name}.exp lib%{name}%{BASE_VERSION}.a
${AR} -rv lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.so

LIBPATH="`pwd`:/usr/lib/threads:%{_libdir}:/usr/lib" \
LIBS=$LIBS \
LDFLAGS="$LDFLAGS -blibpath:%{_prefix}/lib64:%{_prefix}/lib:/usr/lib/threads:/usr/lib64:/usr/lib" \
make \
LIBPATH="`pwd`:/usr/lib/threads:%{_libdir}:/usr/lib"

# build 32-bit version
export CC="/usr/vac/bin/xlc"
export CXX='/usr/vacpp/bin/xlC_r'
export OBJECT_MODE=32
export LDFLAGS="-L/usr/lib -L%{_libdir}"
cd ../32bit
LIBS="-lbsd -lsqlite3 -lncurses -lexpat -lffi" \
LIBPATH="`pwd`:/usr/lib/threads:%{_prefix}/lib:/usr/lib" \
CPPFLAGS="-I/usr/include -I%{_prefix}/include/ncurses" \
LDFLAGS="-L. -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --includedir=%{_includedir} \
    --with-gcc="/usr/vac/bin/xlc_r -ma -qmaxmem=16384 -DAIX_GENUINE_CPLUSCPLUS -Wl,-brtl -lbsd" \
    --with-cxx-main="/usr/vacpp/bin/xlC_r -ma -qmaxmem=16384 -DAIX_GENUINE_CPLUSCPLUS -Wl,-brtl -lbsd" \
    --enable-shared \
    --disable-ipv6 \
    --with-threads \
    --with-system-ffi \
    --with-system-expat \
    OPT="-O"

make lib%{name}%{BASE_VERSION}.a

/usr/vac/bin/CreateExportList -X32 lib%{name}.exp lib%{name}%{BASE_VERSION}.a
/usr/vac/bin/xlc_r -q32 -qmkshrobj lib%{name}%{BASE_VERSION}.a \
	-o lib%{name}%{BASE_VERSION}.so -bE:lib%{name}.exp -lm
rm -f lib%{name}.exp lib%{name}%{BASE_VERSION}.a
${AR} -rv lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.so ../64bit/lib%{name}%{BASE_VERSION}.so

LIBPATH="`pwd`:/usr/lib/threads:%{_prefix}/lib:/usr/lib" \
LIBS=$LIBS \
LDFLAGS="$LDFLAGS -blibpath:%{_prefix}/lib:/usr/lib/threads:/usr/lib" \
make


%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export LIBS="-lbsd -lsqlite3 -lncurses -lexpat -lffi -lXext"
export LDFLAGS="-L%{libdir64} -L%{_libdir} -L/usr/lib/lib64 -L/usr/lib"

cd 64bit
export OBJECT_MODE=64
LIBPATH="`pwd`:/usr/lib/threads:%{_libdir}:%{_prefix}/lib64:/usr/lib:/usr/lib64" \
LDFLAGS="$LDFLAGS -blibpath:%{_prefix}/lib64:%{_prefix}/lib:/usr/lib/threads:/usr/lib64:/usr/lib" \
LIBS=$LIBS \
make DESTDIR=${RPM_BUILD_ROOT} install

cp ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig-ppc64.h 

(
  cd ${RPM_BUILD_ROOT}%{_bindir}

  for f in * ; do
    mv ${f} ${f}_64
  done
  mv smtpd.py_64 smtpd_64.py
  mv %{name}%{BASE_VERSION}-config_64 %{name}%{BASE_VERSION}_64-config

  rm -f %{name}-config_64
  ln -sf %{name}%{BASE_VERSION}_64-config %{name}_64-config

  for f in 2to3_64 idle_64 pydoc_64 python%{BASE_VERSION}_64-config smtpd_64.py ; do
    cat ${f} | \
      sed 's|\/opt\/freeware\/bin\/python2.6|\/opt\/freeware\/bin\/python%{BASE_VERSION}_64|' \
      > tmpfile.tmp
    mv -f tmpfile.tmp ${f}
  done
  rm -f tmpfile.tmp
  cd ..
)

cd ../32bit
export OBJECT_MODE=32
LIBPATH="`pwd`:/usr/lib/threads:%{_prefix}/lib:/usr/lib" \
LIBS=$LIBS \
LDFLAGS="$LDFLAGS -blibpath:%{_prefix}/lib:/usr/lib/threads:/usr/lib" \
make DESTDIR=${RPM_BUILD_ROOT} install

cp ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig.h \
	${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig-ppc32.h 
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig.h 
cp %{_builddir}/Python-%{version}/32bit/lib%{name}%{BASE_VERSION}.a \
	${RPM_BUILD_ROOT}%{_libdir}/lib%{name}%{BASE_VERSION}.a
cp %{_builddir}/Python-%{version}/64bit/lib%{name}%{BASE_VERSION}.a \
	${RPM_BUILD_ROOT}%{libdir64}/lib%{name}%{BASE_VERSION}.a

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)

cd ..

find ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" > dynfiles
find ${RPM_BUILD_ROOT}%{libdir64}/%{name}%{BASE_VERSION}/lib-dynload -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> dynfiles
find ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload -type f | \
  grep -v "_tkinter.so$" | \
  grep -v "_ctypes_test.so$" | \
  grep -v "_testcapi.so$" | \
  sed "s|${RPM_BUILD_ROOT}||" >> dynfiles
find ${RPM_BUILD_ROOT}%{libdir64}/%{name}%{BASE_VERSION}/lib-dynload -type f | \
  grep -v "_tkinter.so$" | \
  grep -v "_ctypes_test.so$" | \
  grep -v "_testcapi.so$" | \
  sed "s|${RPM_BUILD_ROOT}||" >> dynfiles

ln -sf ../../lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/config/lib%{name}%{BASE_VERSION}.a
ln -sf ../../lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{libdir64}/%{name}%{BASE_VERSION}/config/lib%{name}%{BASE_VERSION}.a


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f dynfiles
%defattr(-,root,system)
%doc 32bit/LICENSE 32bit/README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_mandir}/man?/*
%dir %{_libdir}/%{name}%{BASE_VERSION}
%dir %{libdir64}/%{name}%{BASE_VERSION}
%{_libdir}/%{name}%{BASE_VERSION}/LICENSE.txt
%{libdir64}/%{name}%{BASE_VERSION}/LICENSE.txt
%dir %{_libdir}/%{name}%{BASE_VERSION}/site-packages
%dir %{libdir64}/%{name}%{BASE_VERSION}/site-packages
%{_libdir}/%{name}%{BASE_VERSION}/site-packages/README
%{libdir64}/%{name}%{BASE_VERSION}/site-packages/README
%{_libdir}/%{name}%{BASE_VERSION}/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/*.doc
%{libdir64}/%{name}%{BASE_VERSION}/*.doc
%dir %{_libdir}/%{name}%{BASE_VERSION}/bsddb
%dir %{libdir64}/%{name}%{BASE_VERSION}/bsddb
%{_libdir}/%{name}%{BASE_VERSION}/bsddb/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/bsddb/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/compiler
%{libdir64}/%{name}%{BASE_VERSION}/compiler
%dir %{_libdir}/%{name}%{BASE_VERSION}/ctypes
%dir %{libdir64}/%{name}%{BASE_VERSION}/ctypes
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/ctypes/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/macholib
%{libdir64}/%{name}%{BASE_VERSION}/ctypes/macholib
%{_libdir}/%{name}%{BASE_VERSION}/curses
%{libdir64}/%{name}%{BASE_VERSION}/curses
%dir %{_libdir}/%{name}%{BASE_VERSION}/distutils
%dir %{libdir64}/%{name}%{BASE_VERSION}/distutils
%{_libdir}/%{name}%{BASE_VERSION}/distutils/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/distutils/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/distutils/README
%{libdir64}/%{name}%{BASE_VERSION}/distutils/README
%{_libdir}/%{name}%{BASE_VERSION}/distutils/command
%{libdir64}/%{name}%{BASE_VERSION}/distutils/command
%dir %{_libdir}/%{name}%{BASE_VERSION}/email
%dir %{libdir64}/%{name}%{BASE_VERSION}/email
%{_libdir}/%{name}%{BASE_VERSION}/email/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/email/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/email/mime
%{libdir64}/%{name}%{BASE_VERSION}/email/mime
%{_libdir}/%{name}%{BASE_VERSION}/encodings
%{libdir64}/%{name}%{BASE_VERSION}/encodings
%{_libdir}/%{name}%{BASE_VERSION}/hotshot
%{libdir64}/%{name}%{BASE_VERSION}/hotshot
%{_libdir}/%{name}%{BASE_VERSION}/idlelib
%{libdir64}/%{name}%{BASE_VERSION}/idlelib
%dir %{_libdir}/%{name}%{BASE_VERSION}/json
%dir %{libdir64}/%{name}%{BASE_VERSION}/json
%{_libdir}/%{name}%{BASE_VERSION}/json/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/json/*.py*
%dir %{_libdir}/%{name}%{BASE_VERSION}/lib2to3
%dir %{libdir64}/%{name}%{BASE_VERSION}/lib2to3
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/Grammar*
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/Grammar*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/Pattern*
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/Pattern*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/fixes
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/fixes
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/pgen2
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/pgen2
%{_libdir}/%{name}%{BASE_VERSION}/logging
%{libdir64}/%{name}%{BASE_VERSION}/logging
%{_libdir}/%{name}%{BASE_VERSION}/multiprocessing
%{libdir64}/%{name}%{BASE_VERSION}/multiprocessing
%{_libdir}/%{name}%{BASE_VERSION}/plat-aix5
%{libdir64}/%{name}%{BASE_VERSION}/plat-aix5
%dir %{_libdir}/%{name}%{BASE_VERSION}/sqlite3
%dir %{libdir64}/%{name}%{BASE_VERSION}/sqlite3
%{_libdir}/%{name}%{BASE_VERSION}/sqlite3/*.py*
%{libdir64}/%{name}%{BASE_VERSION}/sqlite3/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/wsgiref*
%{libdir64}/%{name}%{BASE_VERSION}/wsgiref*
%{_libdir}/%{name}%{BASE_VERSION}/xml
%{libdir64}/%{name}%{BASE_VERSION}/xml
%{_libdir}/libpython%{BASE_VERSION}.a
%{_libdir}/libpython%{BASE_VERSION}.so
%{libdir64}/libpython%{BASE_VERSION}.a
%{libdir64}/libpython%{BASE_VERSION}.so
/usr/lib/libpython%{BASE_VERSION}.a
/usr/lib/libpython%{BASE_VERSION}.so
/usr/lib64/libpython%{BASE_VERSION}.a
/usr/lib64/libpython%{BASE_VERSION}.so
/usr/bin/pydoc*
/usr/bin/python*


#%files libs
#%defattr(-,root,system)
#%doc 32bit/LICENSE 32bit/README
#%{_libdir}/lib%{name}%{BASE_VERSION}.a
#%{libdir64}/lib%{name}%{BASE_VERSION}.a
#/usr/lib/lib%{name}%{BASE_VERSION}.a
#/usr/lib64/lib%{name}%{BASE_VERSION}.a


%files devel
%defattr(-,root,system)
%doc 32bit/Misc/README.valgrind 32bit/Misc/valgrind-python.supp
%doc 32bit/Misc/gdbinit
%{_includedir}/*
%{_libdir}/%{name}%{BASE_VERSION}/config
%{libdir64}/%{name}%{BASE_VERSION}/config
/usr/include/*


%files tools
%defattr(-,root,system,-)
%{_bindir}/2to3*
%{_bindir}/idle*
%{_bindir}/smtpd*.py*
/usr/bin/2to3*
/usr/bin/idle*
/usr/bin/smtpd*.py*


%files -n tkinter
%defattr(-,root,system,-)
%{_libdir}/%{name}%{BASE_VERSION}/lib-tk
%{libdir64}/%{name}%{BASE_VERSION}/lib-tk
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_tkinter.so
%{libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_tkinter.so


%files test
%defattr(-,root,system)
%{_libdir}/%{name}%{BASE_VERSION}/bsddb/test
%{libdir64}/%{name}%{BASE_VERSION}/bsddb/test
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/test
%{libdir64}/%{name}%{BASE_VERSION}/ctypes/test
%{_libdir}/%{name}%{BASE_VERSION}/distutils/tests
%{libdir64}/%{name}%{BASE_VERSION}/distutils/tests
%{_libdir}/%{name}%{BASE_VERSION}/email/test
%{libdir64}/%{name}%{BASE_VERSION}/email/test
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/tests
%{libdir64}/%{name}%{BASE_VERSION}/lib2to3/tests
%{_libdir}/%{name}%{BASE_VERSION}/json/tests
%{libdir64}/%{name}%{BASE_VERSION}/json/tests
%{_libdir}/%{name}%{BASE_VERSION}/sqlite3/test
%{libdir64}/%{name}%{BASE_VERSION}/sqlite3/test
%{_libdir}/%{name}%{BASE_VERSION}/test
%{libdir64}/%{name}%{BASE_VERSION}/test
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_ctypes_test.so
%{libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_ctypes_test.so
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_testcapi.so
%{libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_testcapi.so


%changelog
* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.7.1-4
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Mon Aug 01 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.7.1-3
- Compilation on 32 and 64 bit

* Mon Mar 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.7.1-2
- Adjust osplat for aix6

* Mon Mar 7 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.7.1
- Update to version 2.7.1

* Tue Feb 01 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.6-3
- Add patch for aix6.1

* Tue Jan 19 2010 <jean-noel.cordenner@bull.net> 2.6-2
- Update to version 2.6 compile with db-4.8.

* Wed Nov 5 2008 <jean-noel.cordenner@bull.net> 2.5.2
- Update to version 2.5.2.

* Thu Jul 13 2006 Reza Arbab <arbab@austin.ibm.com> 2.3.4-3
- Rebuild so tkinter can link to our latest libtk8.4.so.
* Mon Aug 08 2005 Philip K. Warren <pkw@us.ibm.com> 2.3.4-2
- Include patch for PSF-2005-001.
- Build with large files support.

* Thu Aug 05 2004 David Clissold <cliss@austin.ibm.com> 2.3.4-1
- Update to version 2.3.4.

* Wed Jul 28 2004 David Clissold <cliss@austin.ibm.com> 2.3.2-1
- Update to version 2.3.2. (but 2.3.4 is latest).

* Mon Feb 17 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM C++ compiler; --with-threads and --enable-shared
-  (as per tzy@us.ibm.com).  Also added BuildRequires.

* Fri Feb 15 2002 David Clissold <cliss@austin.ibm.com>
- Remove the old libpython2.1.a image.

* Thu Feb 14 2002 Marc Stephenson <marc@austin.ibm.com>
- Include compiler, email, and hotshot
- Move test to devel

* Sun Feb 10 2002 David Clissold <cliss@austin.ibm.com>
- Updated to version 2.2

* Tue Oct 09 2001 David Clissold <cliss@austin.ibm.com>
- Updated to version 2.1.1

* Wed Jun 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Adapted for AIX Toolbox

