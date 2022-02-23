# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, tests are prevented from overusing resources like disk space and memory.
%bcond_with doalltests

%global version     3.10.0
%global pybasever   3.10
%global pyshortver  310
%global pyb         3.10

%global pkgname             python%{pybasever}

%global _libdir64           %{_libdir}64

%global pylibdir            %{_libdir}/python%{pybasever}
%global pylibdir64          %{_libdir64}/python%{pybasever}

%global dynload_dir         %{pylibdir}/lib-dynload
%global dynload_dir64       %{pylibdir64}/lib-dynload 

%global SOABI               cpython-%{pyshortver}

Summary: Version %{pybasever} of the Python interpreter
Name: %{pkgname}
Version: 3.10.1
Release: 1
License: Modified CNRI Open Source License
Group: Development/Languages
URL: http://www.python.org/
Source0: https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1: pyconfig.h
Source1000: %{name}-%{version}-%{release}.build.log

# _LARGE_FILES should not be defined for 64bit build
Patch0: python3.9-no-largefiles-64bit.patch

# Pass "-C" to nm to suppress demangling of C++ names
#Patch1: python3.9-demangling-aix.patch

# Use 64bit version of major, minor & makedev for 64bit AIX build
Patch2: python3.9-makedev-64bit.patch

# nextafter patch for AIX, See https://bugs.python.org/issue42323
#Patch3: python3.9-nextafter-aix.patch

# build with ncurses instead of AIX curses
Patch4: python3.9-enable-ncurses-aix.patch

Provides: python%{pybasever}(abi) = %{pybasever}

BuildRequires: make, sed
BuildRequires: pkg-config
BuildRequires: bzip2-devel >= 1.0.8
BuildRequires: expat-devel >= 2.2.9
BuildRequires: gettext-devel >= 0.20.2
BuildRequires: gdbm-devel >= 1.19
BuildRequires: libffi-devel >= 3.2.1
BuildRequires: ncurses-devel >= 6.3-2
BuildRequires: readline-devel >= 8.0-2
BuildRequires: sqlite-devel >= 3.34
BuildRequires: tcl-devel >= 8.6.10
BuildRequires: tk-devel >= 8.6.10
BuildRequires: xz-devel >= 5.2.5
BuildRequires: zlib-devel >= 1.2.11

Requires: bzip2 >= 1.0.8
Requires: expat >= 2.2.9
Requires: gdbm >= 1.19
Requires: libffi >= 3.2.1
Requires: ncurses >= 6.3-2
Requires: readline >= 8.0-2
Requires: sqlite >= 3.34
Requires: zlib >= 1.2.11
Requires: gettext >= 0.20.2
Requires: libgcc >= 8.3.0
Requires: xz-libs >= 5.2.5

%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%define osplat aix7
%endif

%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%define osplat aix7
%endif

%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The %{pkgname} package provides the python%{pybasever} executable: the reference
interpreter for the Python language, version 3 and majority of its standard library.
The remaining parts of the Python standard library are broken out into the
%{pkgname}-tkinter and %{pkgname}-test packages, which may need to be installed
separately.

IDLE for Python %{pybasever} is provided in the %{pkgname}-idle package and
development files are provided through %{pkgname}-devel package


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains 2to3 tool, an automatic source converter from Python 2.X.


%package idle
Summary: A basic graphical development environment for Python
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}

%description idle
IDLE is Python's Integrated Development and Learning Environment.

IDLE has the following features: Python shell window (interactive
interpreter) with colorizing of code input, output, and error messages;
multi-window text editor with multiple undo, Python colorizing,
smart indent, call tips, auto completion, and other features;
search within any window, replace within editor windows, and
search through multiple files (grep); debugger with persistent
breakpoints, stepping, and viewing of global and local namespaces;
configuration, browsers, and other dialogs.


%package tkinter
Summary: A GUI toolkit for Python
Requires: %{name} = %{version}-%{release}

Requires: tcl >= 8.6.10
Requires: tk >= 8.6.10

%description tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package test
Summary: The self-test suite for the main python3 package
Requires: %{name} = %{version}-%{release}

%description test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{pkgname}, or a library such as
pytest.


#################################
#  Prep
#################################
%prep
# need tar from /opt/freeware to extract tar.xz archives
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
# Extract python
%setup -q -n Python-%{version}
#%%patch1 -p1 -b .demangling
#%%patch3 -p1 -b .nextafter
%patch4 -p1 -b .ncurses

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit

# Specific patch for 64 bit
cd 64bit
%patch0 -p1 -b .large_file
%patch2 -p1 -b .makedev


#################################
#  Build
#################################
%build

# setup common configuration for 32-bit and 64-bit builds
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export CFLAGS="-I/opt/freeware/include -I/usr/include -DAIX_GENUINE_CPLUSCPLUS -D_ALL_SOURCE -D_LINUX_SOURCE_COMPAT"
export CPPFLAGS="$CFLAGS"
export CXXFLAGS="$CFLAGS"

# build 64-bit version
cd 64bit

/opt/freeware/bin/sed -i "s|#! /usr/local/bin/python|#! /opt/freeware/bin/python%{pybasever}|g" Lib/cgi.py

export OBJECT_MODE=64
export CC="gcc -maix64 -fPIC -pthread -O2"
export CXX="g++ -maix64 -fPIC -pthread -O2"
export LDFLAGS="-L/opt/freeware/lib/pthread/ppc64 -L/opt/freeware/lib64 -L/opt/freeware/lib -L/usr/lib -Wl,-brtl -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export PKG_CONFIG_PATH=/opt/freeware/lib64/pkgconfig:/opt/freeware/lib/pkgconfig

./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir64} \
        --with-platlibdir=lib64 \
        --mandir=%{_mandir} \
        --enable-shared \
        --enable-ipv6 \
        --with-system-ffi \
        --with-system-expat \
        --with-tcltk-includes="-I/opt/freeware/include" \
        --with-tcltk-libs="-L/opt/freeware/lib -ltcl -ltk" \
        --with-computed-gotos

gmake -j8


# build 32-bit version
cd ../32bit

/opt/freeware/bin/sed -i "s|#! /usr/local/bin/python|#! /opt/freeware/libexec/python%{pybasever}_32|g" Lib/cgi.py

export OBJECT_MODE=32
export CC="gcc -fPIC -pthread -O2 -D_LARGE_FILES"
export CXX="g++ -fPIC -pthread -O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib/pthread -L/opt/freeware/lib -L/usr/lib -Wl,-brtl -Wl,-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib -Wl,-bmaxdata:0x80000000"
export PKG_CONFIG_PATH=/opt/freeware/lib/pkgconfig

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --enable-shared \
        --enable-ipv6 \
        --with-system-ffi \
        --with-system-expat \
        --with-tcltk-includes="-I/opt/freeware/include" \
        --with-tcltk-libs="-L/opt/freeware/lib -ltcl -ltk" \
        --with-computed-gotos

gmake -j8

#################################
#  Install
#################################
%install

[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT 

install_python(){

   cd ${OBJECT_MODE}bit

   gmake DESTDIR=${RPM_BUILD_ROOT} install

   # pyconfig.h header file is arch specific (32bit vs 64bit)
   cp ${RPM_BUILD_ROOT}%{_includedir}/python%{pybasever}/pyconfig.h ${RPM_BUILD_ROOT}%{_includedir}/python%{pybasever}/pyconfig-ppc${OBJECT_MODE}.h

   (
     if [ ${OBJECT_MODE} -eq 64 ]
     then
       cd ${RPM_BUILD_ROOT}%{_bindir}
     else
       cd ${RPM_BUILD_ROOT}%{_libexecdir}
     fi
     rm 2to3 idle3 pydoc3 python3 python3-config
   )

   # We do not want to provide pip and setuptools
   rm -rf ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/pip*
   rm -rf ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/setuptools*
   rm -rf ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/distutils*
   rm -rf ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/pkg_resources
   rm -rf ${RPM_BUILD_ROOT}%{pylibdir}/site-packages/_distutils_hack
   cd ..
}

#install 32bit version

export OBJECT_MODE=32

install_python

#install 64bit version

export OBJECT_MODE=64

install_python

# Add "_32" prefix to 32bit binaries
(
  cd ${RPM_BUILD_ROOT}%{_libexecdir}
  for f in 2to3-%{pyb} idle%{pyb} pydoc%{pyb} python%{pyb} python%{pyb}-config ; do
    mv ${f} ${f}_32
  done

  for f in 2to3-%{pyb} idle%{pyb} pydoc%{pyb} ; do
    /opt/freeware/bin/sed -i "s|/opt/freeware/libexec/python%{pybasever}|/opt/freeware/libexec/python%{pybasever}_32|g" ${f}_32
  done
)

# Replace the pyconfig.h with the Source1 "pyconfig.h" file
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/python%{pybasever}/pyconfig.h

/opt/freeware/bin/sed -i "s|/opt/freeware/libexec/python%{pybasever}|/opt/freeware/libexec/python%{pybasever}_32|g" ${RPM_BUILD_ROOT}%{pylibdir}/config-%{pybasever}/python-config.py

# Create archive file for library
ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libpython%{pybasever}.a ${RPM_BUILD_ROOT}%{_libdir}/libpython%{pybasever}.so
ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libpython%{pybasever}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{pybasever}.so
ln -sf ../lib/libpython%{pybasever}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{pybasever}.a

# Create config directory from version specific config directory
(
  cd ${RPM_BUILD_ROOT}%{pylibdir64}
  ln -s config-%{pybasever} config

  cd ${RPM_BUILD_ROOT}%{pylibdir}
  ln -s config-%{pybasever} config
)

# Create files list for main & sub rpms

# main package
find ${RPM_BUILD_ROOT}%{pylibdir}   -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" > main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir}   -type f                                    >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type f                                    >> main-pkg-files.tmp
cat main-pkg-files.tmp | \
  grep -v "_ctypes_test.%{SOABI}.so" | \
  grep -v "_testbuffer.%{SOABI}.so" | \
  grep -v "_testcapi.%{SOABI}.so" | \
  grep -v "_testimportmultiple.%{SOABI}.so" | \
  grep -v "_testinternalcapi.%{SOABI}.so" | \
  grep -v "_testmultiphase.%{SOABI}.so" | \
  grep -v "_xxtestfuzz.%{SOABI}.so" | \
  grep -v "/test/" | \
  grep -v "ctypes/test" |\
  grep -v "distutils/test" |\
  grep -v "lib2to3/test" | \
  grep -v "sqlite3/test" |\
  grep -v "unittest/test" | \
  grep -v "tkinter" | \
  grep -v "turtle" | \
  grep -v "config-%{pybasever}" | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |"  >> main-pkg-files


cat main-pkg-files.tmp | grep "_ctypes_test.%{SOABI}.so"         > test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testbuffer.%{SOABI}.so"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testcapi.%{SOABI}.so"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testimportmultiple.%{SOABI}.so" >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testinternalcapi.%{SOABI}.so"   >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testmultiphase.%{SOABI}.so"     >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_xxtestfuzz.%{SOABI}.so"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "/test/"                          >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "ctypes/test"                     >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "distutils/test"                  >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "lib2to3/test"                    >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "sqlite3/test"                    >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "tkinter/test"                    >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "unittest/test"                   >> test-pkg-files.tmp

cat test-pkg-files.tmp | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |" | sort -u > test-pkg-files

# devel package
find ${RPM_BUILD_ROOT}%{pylibdir}/config-%{pybasever}   -type f | grep -v "Makefile" > devel-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64}/config-%{pybasever} -type f | grep -v "Makefile" >> devel-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{_includedir}/python%{pybasever}/* -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> devel-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{_includedir}/python%{pybasever} -type f | grep "\.h$"        >> devel-pkg-files.tmp
cat devel-pkg-files.tmp | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |"  >> devel-pkg-files

#################################
# Check
#################################
%check
%if %{with dotests}
ulimit -d unlimited
ulimit -m unlimited
ulimit -n 20000

# test_urllib2net spend 120 minutes due to timeout of 20 minutes x2 (32, 64 bits) x2 (rerun due to fail)
# Some tests hang when running the whole test_suite, so we need to ignore them first and run them separately later
cd 64bit
export OBJECT_MODE=64
%if %{with doalltests}
(gmake -k testall TESTOPTS="-x test_urllib2net -x test_multiprocessing_fork -x test_multiprocessing_forkserver -x test_interrupted_read_retry_buffered -x test_concurrent_futures" || true)
(gmake -k testall TESTOPTS="                      test_multiprocessing_fork    test_multiprocessing_forkserver    test_interrupted_read_retry_buffered    test_concurrent_futures" || true)
%else
(gmake -k test TESTOPTS="-x test_urllib2net -x test_multiprocessing_fork -x test_multiprocessing_forkserver -x test_interrupted_read_retry_buffered -x test_concurrent_futures" || true)
(gmake -k test TESTOPTS="                      test_multiprocessing_fork    test_multiprocessing_forkserver    test_interrupted_read_retry_buffered    test_concurrent_futures" || true)
%endif
slibclean

cd ../32bit
export OBJECT_MODE=32
%if %{with doalltests}
(gmake -k testall TESTOPTS="-x test_urllib2net -x test_multiprocessing_fork -x test_multiprocessing_forkserver -x test_interrupted_read_retry_buffered -x test_concurrent_futures" || true)
(gmake -k testall TESTOPTS="                      test_multiprocessing_fork    test_multiprocessing_forkserver    test_interrupted_read_retry_buffered    test_concurrent_futures" || true)
%else
(gmake -k test TESTOPTS="-x test_urllib2net -x test_multiprocessing_fork -x test_multiprocessing_forkserver -x test_interrupted_read_retry_buffered -x test_concurrent_futures" || true)
(gmake -k test TESTOPTS="                      test_multiprocessing_fork    test_multiprocessing_forkserver    test_interrupted_read_retry_buffered    test_concurrent_futures" || true)
%endif
slibclean
%endif

#################################
# Clean
#################################
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#################################
#  File
#################################
%files -f main-pkg-files
%defattr(-,root,system,-)
%doc 32bit/README.rst
%{_bindir}/python%{pybasever}
%{_bindir}/pydoc%{pybasever}
%{_libexecdir}/python%{pybasever}_32
%{_libexecdir}/pydoc%{pybasever}_32
%{_mandir}/man1/python%{pybasever}.1

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config-%{pybasever}/
%{pylibdir}/config-%{pybasever}/Makefile
%dir %{pylibdir64}/config-%{pybasever}/
%{pylibdir64}/config-%{pybasever}/Makefile
%{pylibdir}/config
%{pylibdir64}/config
%dir %{_includedir}/python%{pybasever}/
%{_includedir}/python%{pybasever}/pyconfig.h
%{_includedir}/python%{pybasever}/pyconfig-ppc32.h
%{_includedir}/python%{pybasever}/pyconfig-ppc64.h

%{_libdir}/libpython%{pybasever}.so
%{_libdir}/libpython%{pybasever}.a
%{_libdir64}/libpython%{pybasever}.so
%{_libdir64}/libpython%{pybasever}.a


%files devel -f devel-pkg-files
%defattr(-,root,system,-)
%doc 32bit/Misc/README.valgrind 32bit/Misc/valgrind-python.supp
%doc 32bit/Misc/gdbinit
%{_bindir}/2to3-%{pybasever}
%{_bindir}/python%{pybasever}-config
%{_libexecdir}/2to3-%{pybasever}_32
%{_libexecdir}/python%{pybasever}-config_32

%{_libdir}/pkgconfig/python-%{pybasever}*.pc
%{_libdir64}/pkgconfig/python-%{pybasever}*.pc

# Exclude the header files already shipped with main rpm
%exclude %{_includedir}/python%{pybasever}/pyconfig.h
%exclude %{_includedir}/python%{pybasever}/pyconfig-ppc32.h
%exclude %{_includedir}/python%{pybasever}/pyconfig-ppc64.h


%files idle
%defattr(-,root,system,-)
%{_bindir}/idle%{pybasever}
%{_libexecdir}/idle%{pybasever}_32
%{pylibdir}/idlelib
%{pylibdir64}/idlelib


%files tkinter
%defattr(-,root,system,-)
%{pylibdir}/tkinter
%exclude %{pylibdir}/tkinter/test
%{pylibdir64}/tkinter
%exclude %{pylibdir64}/tkinter/test
%{dynload_dir}/_tkinter.%{SOABI}.so
%{dynload_dir64}/_tkinter.%{SOABI}.so

%{pylibdir}/turtle.py
%{pylibdir64}/turtle.py
%{pylibdir}/__pycache__/turtle*
%{pylibdir64}/__pycache__/turtle*
%{pylibdir}/turtledemo
%{pylibdir64}/turtledemo


%files test -f test-pkg-files
%defattr(-,root,system,-)


%changelog
* Sun Dec 12 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 3.10.1-1
- Update to 3.10.1

* Mon Nov 22 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 3.10.0-1
- New version 3.10.0

* Mon Nov 22 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 3.9.9-1
- New version 3.9.9
- First version published on Bullfreeware

* Mon Sep 27 2021 Ayappan P <ayappap2@in.ibm.com> - 3.9.6-1
- python 3.9.6 build for AIX Toolbox
