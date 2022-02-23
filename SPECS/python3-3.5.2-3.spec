%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 64}
%{!?dotests: %define dotests 1}
%{!?include_tkinter: %define include_tkinter 1}
#define gcc_compiler 0
#define gcc_compiler 1

%if %{gcc_compiler} != 1
%define sub_release xlc
%define compiler_msg This version has been compiled with XLC.
%else
%define compiler_msg This version has been compiled with GCC.
%endif


%define WITH_WITHOUT_MALLOC	--with-pymalloc
%define with_pmalloc 1

%if %{gcc_compiler} == 1
%define WITH_WITHOUT_GOTOS	--with-computed-gotos 
%else
%define WITH_WITHOUT_GOTOS	--without-computed-gotos 
%endif


#########################
#  User-modifiable configs
##########################
#  Build tkinter?
#WARNING: Commenting out doesn t work.  Last line is what s used.
%define config_tkinter no
%define config_tkinter yes

#################################
#  End of user-modifiable configs
#################################
%define name python3
%define version 3.5.2
%define MAJOR_VERSION 3
%define BASE_VERSION 3.5
%define SHORT_VERSION 35

# Change VERSION_SUFFIX to empty when compiling without pymalloc
# ATTENTION: code may not work if VERSION_SUFFIX is empty
%if %{with_pmalloc} == 1
%define VERSION_SUFFIX m
%else
%define VERSION_SUFFIX ""
%endif


%define release 3%{?sub_release}
%define doc_version 3.5.0a3

# include_tkinter is now defined with --define command_line
#  kludge to get around rpm <percent>define weirdness
#define include_tkinter %(if [ "%{config_tkinter}" = yes ]; then echo 1; else echo 0; fi)

%define _libdir64     %{_prefix}/lib64
%define pylibdir      %{_libdir}/python%{BASE_VERSION}
%define dynload_dir   %{pylibdir}/lib-dynload
%define pylibdir64    %{_libdir64}/python%{BASE_VERSION}
%define dynload_dir64 %{pylibdir64}/lib-dynload

%define ABIFLAGS_optimized %{VERSION_SUFFIX}
%define ABIFLAGS_debug     dm

%define LDVERSION_optimized %{BASE_VERSION}%{ABIFLAGS_optimized}
%define LDVERSION_debug     %{BASE_VERSION}%{ABIFLAGS_debug}

#################################
#  Header
#################################
Summary: An interpreted, interactive, object-oriented programming language.
Name: %{name}
Version: %{version}
Release: %{release}
License: Modified CNRI Open Source License
Group: Development/Languages
URL: http://www.python.org/

Source0: http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1: pyconfig.h
Source2: http://www.python.org/ftp/python/doc/%{version}/Python-%{doc_version}-docs-text.tar.bz2
Source3: %{name}-%{version}-%{release}.build.log
# Patch 7 & 12 are still required
Patch7: Python-%{version}-fileio.patch
Patch12: Python-%{version}-compat.patch

# 64 bits only : this patch ensures dynamic Python libs are loaded from lib64, not lib
Patch0: Python-%{version}-64bit.patch

# Other patchs seems no more usefull with Python3, kept here just in case...
Patch2: Python-%{version}-aixsetup.patch
Patch3: Python-%{version}-termios.patch
# http://bugs.python.org/issue11215
# New version for Python 2.7.10
Patch10: Python-%{version}-linkso.patch
Patch11: Python-%{version}-ldshared.patch
Patch13: Python-%{version}-Lib.ctypes.160309.patch


Provides: python-abi = %{BASE_VERSION}
Provides: python(abi) = %{BASE_VERSION}
Provides: python3 = %{version}

# new module include in 2.7
Provides: python-argparse
Provides: python-unittest2
Provides: python-importlib
Provides: python-ordereddict

BuildRequires: bzip2-devel
BuildRequires: db-devel >= 4.7
BuildRequires: expat-devel >= 2.0.0
BuildRequires: gdbm-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel >= 1.0.2
BuildRequires: readline-devel >= 5.2
BuildRequires: sqlite-devel >= 3
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: zlib-devel
BuildRequires: gettext-devel
BuildRequires: make
BuildRequires: ncurses
BuildRequires: pkg-config
BuildRequires: tcl
BuildRequires: tk
BuildRequires: xz-devel

Requires: bzip2
Requires: db >= 4.8
Requires: expat >= 2.0.0
Requires: gdbm
Requires: gmp
Requires: libffi
Requires: ncurses
Requires: openssl >= 1.0.2
Requires: readline >= 5.2
Requires: sqlite >= 3
Requires: zlib
Requires: gettext

BuildRoot: %{_tmppath}/python-%{version}-%{release}-root

Prefix: %{_prefix}

%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%define osplat aix7
%endif

%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%define osplat aix7
%endif

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%define osplat aix5
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

%{compiler_msg}


%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Conflicts: %{name} < %{version}-%{release}

%description devel
The Python programming language s interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You ll probably also
want to install the python-docs package, which contains Python
documentation.

%{compiler_msg}


%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}

%description tools
The Python package includes several development tools that are used
to build python programs.


%if %{include_tkinter} == 1
%package tkinter
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
BuildRequires: tcl-devel
BuildRequires: tk-devel
Requires: tcl
Requires: tk
Requires: %{name} = %{version}-%{release}

%description tkinter
The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you d like to use a graphical
user interface for Python programming.

%{compiler_msg}
%endif


%package test
Summary: The test modules from the main python package
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description test
The test modules from the main python package: python
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you re developing python
code that uses more than just unittest and/or test_support.py.

%{compiler_msg}


%package docs
Summary: Documentation for the Python programming language
Group: %{name}
Requires: %{name} = %{version}-%{release}

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.

Install the python-docs package if you d like to use the documentation
for the Python language.


#################################
#  Prep
#################################
%prep
echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
echo "include_tkinter=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif
# need tar from /opt/freeware to extract tar.xz archives
export PATH=/opt/freeware/bin:$PATH
# Extract python
%setup -q -n Python-%{version}

# Then patch it
# Only patch 7 and 12 are still required
%patch7 -p1 -b .fileio
%patch12 -p1 -b .compat

# Patch 2 no more useful with Python 3.5.2
#%patch2 -p1 -b .aixsetup
#%patch3 -p1 -b .termios
#%patch10 -p1 -b .linkso
#%patch11 -p1 -b .ldshared
#%patch13 -p1 -b .Lib.ctypes.160309

# Patch on the fly
perl -pi -e "s|yperr_string|(const char*)yperr_string|g;" \
Modules/nismodule.c

# Should autoreconf for coherent configures installed and generated version
#autoreconf


# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit


# Specific patch for 64 bit
cd 64bit
%patch0 -p1 -b .64bit
sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_64|" Lib/cgi.py > tmpfile.tmp
mv tmpfile.tmp Lib/cgi.py
if [ ! -f /opt/freeware/bin/python3_64 ]; then
    echo "WARNING : python3_64 not found. You will have to rebuild the package after installing the first build !"
    sleep 30
else
  for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1`; do
	# inplace agnostic sed
    sed "s|\/usr\/bin\/env python3|\/usr\/bin\/env python3_64|" ${f} > tmpfile.tmp
    sed "s|\/usr\/bin\/env python\([^3]\)|\/usr\/bin\/env python_64\\1|" tmpfile.tmp > tmpfile.tmp2
    sed "s|\/usr\/bin\/env python$|\/usr\/bin\/env python_64|" tmpfile.tmp2 > tmpfile.tmp
    cp -f tmpfile.tmp ${f}
  done 
fi
cd ..

cd 32bit
sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_32|" Lib/cgi.py > tmpfile.tmp
mv tmpfile.tmp Lib/cgi.py
if [ ! -f /opt/freeware/bin/python3_32 ]; then
    echo "WARNING : python3_32 not found. You will have to rebuild the package after installing the first build !"
    sleep 30
else
  for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1`; do
	# inplace agnostic sed
    sed "s|\/usr\/bin\/env python3|\/usr\/bin\/env python3_32|" ${f} > tmpfile.tmp
    sed "s|\/usr\/bin\/env python\([^3]\)|\/usr\/bin\/env python_32\\1|" tmpfile.tmp > tmpfile.tmp2
    sed "s|\/usr\/bin\/env python$|\/usr\/bin\/env python_32|" tmpfile.tmp2 > tmpfile.tmp
    cp -f tmpfile.tmp ${f}
  done 
fi
cd ..

# Extract documentation
%setup -q -D -T -a 2 -n Python-%{version}


#################################
#  Build
#################################
# from python tracker: issue 7657, set qbitfields=signed for ctypes bitfield
# from python: Misc/README.AIX, You can allow up to 2GB of memory for Python by using the value 0x80000000 for maxdata.
# from python: Misc/README.AIX, It is a good idea to add the '-qmaxmem=70000' option, otherwise the compiler considers various files too complex to optimize.
# from man tzset: Do not use the tzset subroutine when linking with both libc.a and libbsd.a.
# hotshot without D_LINUX_SOURCE_COMPAT failed due to AIX malloc
# enable LARGE_FILES support for 32bits
#################################

%build
###############################################
# for linking with openssl archive (not soname)
###############################################
if [ -f %{_libdir}/libcrypto.so ]; then
    mv %{_libdir}/libcrypto.so /tmp/libcrypto.so.32
fi
if [ -f %{_libdir}/libssl.so ]; then
    mv %{_libdir}/libssl.so /tmp/libssl.so.32
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{_libdir64}/libcrypto.so /tmp/libcrypto.so.64
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{_libdir64}/libssl.so /tmp/libssl.so.64
fi

echo "WITH_WITHOUT_MALLOC: %{WITH_WITHOUT_MALLOC}"
echo "WITH_WITHOUT_GOTOS:  %{WITH_WITHOUT_GOTOS}"
echo "with_pmalloc:      : %{with_pmalloc}"
echo "VERSION_SUFFIX     : %{VERSION_SUFFIX}"

# setup commun for 32-bit and 64-bit builds
export CONFIG_SHELL=%{_prefix}/bin/bash
export CONFIGURE_ENV_ARGS=%{_prefix}/bin/bash

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64 -B"
export RM="/usr/bin/rm -f"

export LDFLAGS=""
export LIBS="-lXext -lexpat -lffi -lncurses -lsqlite3"

export CFLAGS="  -I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -Wl,-brtl"
export CPPFLAGS="-I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses"

export OPT="-g -O0"
export OPT="-g -O2"
export OPT="   -O2"


# Choose GCC or XLC
%if %{gcc_compiler} == 1

export CC="gcc"
export CXX="gcc"

export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC --version

%else

export OPT="$OPT -qmaxmem=70000"
export CFLAGS="$CFLAGS -qbitfields=signed -qalloca"

export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC -qversion

%endif

export CXXFLAGS="${CFLAGS}"

type $CC
type $CXX


export CC32=" ${CC}  ${FLAG32}"
export CXX32="${CXX} ${FLAG32}"
export CC64=" ${CC}  ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"


build_python()
{

    ./configure \
        --srcdir="`pwd`" \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
        --prefix=%{_prefix} \
        --libdir=$1 \
        --includedir=%{_includedir} \
        --mandir=%{_mandir} \
        --enable-shared \
        --enable-ipv6 \
        --with-threads \
        --with-system-ffi \
        --without-computed-gotos  \
        --with-system-expat \
	%{WITH_WITHOUT_MALLOC} %{WITH_WITHOUT_GOTOS}

    /usr/sbin/slibclean
    
    gmake --trace %{?_smp_mflags} libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
    
    /usr/vac/bin/CreateExportList -X${OBJECT_MODE} libpython.exp libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
%if %{gcc_compiler} == 1
    # GCC
    ${CC} -shared    libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a -o libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so -Wl,-bE:libpython.exp -lm -lpthreads             -lintl
%else
    # xlc
    ${CC} -qmkshrobj libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a -o libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so     -bE:libpython.exp -lm             -L/usr/lib -lintl
%endif
    rm -f libpython.exp
    mv -f libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a.old
    ${AR} -r libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so

    gmake %{?_smp_mflags}
    
    /usr/sbin/slibclean
    
    if [ "%{dotests}" == 1 ]
    then
	echo "Testing ${OBJECT_MODE} bit build"
        export PYTHONPATH=`pwd`/Modules
        # Some tests hang when running the whole test_suite, so we need to ignore them first and run them separately later
        #( ./python Lib/test/regrtest.py -x test_io -x test_signal -x test_socket -x test_subprocess -x test_poplib || true )
        #( ./python Lib/test/regrtest.py test_io test_signal test_socket test_subprocess test_poplib || true )
        #( gmake -k test || true )
        ( gmake -k testall || true )
        /usr/sbin/slibclean
	unset PYTHONPATH
    fi
}


# build 64-bit version
export OBJECT_MODE=64
export CC=${CC64}
export CXX=${CXX64}

export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib"
%if %{gcc_compiler} == 0
export LDFLAGS="$LDFLAGS -blibpath:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib -bmaxdata:0x06FFFFFFFFFFFFF8"
%endif


cd 64bit
export LIBPATH=`pwd`
build_python %{_libdir64}
cd ..


# build 32-bit version
export OBJECT_MODE=32
export CC=${CC32}
export CXX=${CXX32}

export LDFLAGS="-L. -L/usr/lib/threads                -L%{_libdir}              -L/usr/lib"
%if %{gcc_compiler} == 0
export LDFLAGS="$LDFLAGS -blibpath:/usr/lib/threads:%{_libdir}:/usr/lib -bmaxdata:0x80000000"
%endif


cd 32bit
export LIBPATH=`pwd`
build_python %{_libdir}
cd ..


##################################################################
# revert previous move - linking with openssl archive (not soname)
##################################################################

if [ -f /tmp/libcrypto.so.32 ]; then
    mv /tmp/libcrypto.so.32 %{_libdir}/libcrypto.so
fi
if [ -f /tmp/libssl.so.32 ]; then
    mv /tmp/libssl.so.32 %{_libdir}/libssl.so
fi
if [ -f /tmp/libcrypto.so.64 ]; then
    mv /tmp/libcrypto.so.64 %{_libdir64}/libcrypto.so
fi
if [ -f /tmp/libssl.so.64 ]; then
    mv /tmp/libssl.so.64 %{_libdir64}/libssl.so
fi


#################################
#  Install
#################################
%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# install 64-bit version

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

install_python() {
    cd ${OBJECT_MODE}bit
    gmake DESTDIR=${RPM_BUILD_ROOT} install

    cp ${RPM_BUILD_ROOT}%{_includedir}/python%{BASE_VERSION}%{VERSION_SUFFIX}/pyconfig.h ${RPM_BUILD_ROOT}%{_includedir}/python%{BASE_VERSION}%{VERSION_SUFFIX}/pyconfig-ppc${OBJECT_MODE}.h

    (
      cd ${RPM_BUILD_ROOT}%{_bindir}

      for f in 2to3 pyvenv; do
        mv ${f}-%{BASE_VERSION} ${f}-%{BASE_VERSION}_${OBJECT_MODE} ;
        ln -sf ${f}-%{BASE_VERSION}_64 ${f}_${OBJECT_MODE}
      done

      for f in idle pydoc python ; do
        mv     ${f}%{BASE_VERSION}                ${f}%{BASE_VERSION}_${OBJECT_MODE}
        ln -sf ${f}%{BASE_VERSION}_${OBJECT_MODE} ${f}_${OBJECT_MODE}
        ln -sf ${f}%{BASE_VERSION}_${OBJECT_MODE} ${f}%{MAJOR_VERSION}_${OBJECT_MODE}
      done

      mv     python%{BASE_VERSION}%{VERSION_SUFFIX}                        python%{BASE_VERSION}%{VERSION_SUFFIX}_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}%{VERSION_SUFFIX}_${OBJECT_MODE}         python%{BASE_VERSION}_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}_${OBJECT_MODE}                          python%{MAJOR_VERSION}_${OBJECT_MODE}
      ln -sf python%{MAJOR_VERSION}_${OBJECT_MODE}                         python_${OBJECT_MODE}
      
      mv     python%{BASE_VERSION}%{VERSION_SUFFIX}-config                 python%{BASE_VERSION}%{VERSION_SUFFIX}-config_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}%{VERSION_SUFFIX}-config_${OBJECT_MODE}  python%{BASE_VERSION}-config_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}-config_${OBJECT_MODE}                   python%{MAJOR_VERSION}-config_${OBJECT_MODE}
      ln -sf python%{MAJOR_VERSION}-config_${OBJECT_MODE}                  python-config_${OBJECT_MODE}
      
      for f in 2to3 pyvenv idle pydoc python-config; do
        if [ -f ${f}_${OBJECT_MODE} ]; then
          cat ${f}_${OBJECT_MODE} | sed "s|\/opt\/freeware\/bin\/python%{BASE_VERSION}|\/opt\/freeware\/bin\/python%{BASE_VERSION}_${OBJECT_MODE}|" > tmpfile.tmp
          mv -f tmpfile.tmp ${f}_${OBJECT_MODE}
        fi
      done
      cd ..
    )
    cd ..
}

# install 64-bit version
export OBJECT_MODE=64

LIBPATH="`pwd`:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib" \
LDFLAGS="-blibpath:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib" \

install_python

# install 32-bit version
export OBJECT_MODE=32

LIBPATH="`pwd`:/usr/lib/threads:%{_libdir}:/usr/lib" \
LDFLAGS="-blibpath:/usr/lib/threads:%{_libdir}:/usr/lib" \

install_python

# python header
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/python%{BASE_VERSION}%{VERSION_SUFFIX}/pyconfig.h

cp %{_builddir}/Python-%{version}/32bit/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a ${RPM_BUILD_ROOT}%{_libdir}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
#cp %{_builddir}/Python-%{version}/64bit/libpython%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{BASE_VERSION}.a
ln -sf ../lib/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a

# Add the 64 bit shared object to the 32/64 bits archive
${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so

# Add symlinks for commands without _32/_64 suffix
DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi
(
  cd ${RPM_BUILD_ROOT}%{_bindir}

  for f in `ls *_${DEFAULT_BITS}`; do
    ln -sf ${f} `echo ${f} | sed -e "s/_${DEFAULT_BITS}$//"`
  done

  cd ..
)


# Why NOT ??
echo "Why NOT strip ????????????????????????????????????????????????????????????????????????????"
#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
#*/
(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    #*/
    cd -
  done
)

mkdir -p ${RPM_BUILD_ROOT}%{pylibdir64}/site-packages/__pycache__/


# symlink
ln -sf ../../libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a ${RPM_BUILD_ROOT}%{_libdir}/python%{BASE_VERSION}/config-%{BASE_VERSION}%{VERSION_SUFFIX}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/python%{BASE_VERSION}/config-%{BASE_VERSION}%{VERSION_SUFFIX}
ln -sf ../../libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a ${RPM_BUILD_ROOT}%{_libdir64}/python%{BASE_VERSION}/config-%{BASE_VERSION}%{VERSION_SUFFIX}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a


# Create files list for the differente packages

# main package
find ${RPM_BUILD_ROOT}%{pylibdir}   -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" > main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir}   -type f                                    >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type f                                    >> main-pkg-files.tmp
cat main-pkg-files.tmp | \
  grep -v "_tkinter.so" | \
  grep -v "_ctypes_test.so" | \
  grep -v "_testcapi.so" | \
  grep -v "_testbuffer.so" | \
  grep -v "_testimportmultiple.so" | \
  grep -v "_testmultiphase.so" | \
  grep -v "/test/" | \
  grep -v "ctypes/test" |\
  grep -v "distutils/test" |\
  grep -v "lib2to3/test" | \
  grep -v "sqlite3/test" |\
  grep -v "unittest/test" | \
  grep -v "turtle" | \
  grep -v "config-%{LDVERSION_optimized}" | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |"  >> main-pkg-files


cat main-pkg-files.tmp | grep "_ctypes_test.so"        > test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testcapi.so"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testbuffer.so"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testimportmultiple.so" >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testmultiphase.so"     >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "/test/"                 >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "ctypes/test"            >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "distutils/test"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "lib2to3/test"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "sqlite3/test"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "unittest/test"          >> test-pkg-files.tmp

cat test-pkg-files.tmp | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |" | sort -u > test-pkg-files


# devel package
find ${RPM_BUILD_ROOT}%{pylibdir}/config-%{LDVERSION_optimized}   -type f | grep -v "Makefile" > devel-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64}/config-%{LDVERSION_optimized} -type f                      >> devel-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{_includedir}/python%{LDVERSION_optimized} -type f | grep "\.h$"        >> devel-pkg-files.tmp
cat devel-pkg-files.tmp | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|"  > devel-pkg-files


#################################
#  Clean
#################################
#%clean
#[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


#################################
#  File
 #################################
%files -f main-pkg-files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/README
%{_bindir}/pydoc*
%{_bindir}/python
%{_bindir}/python_32
%{_bindir}/python_64
%{_bindir}/python%{MAJOR_VERSION}
%{_bindir}/python%{MAJOR_VERSION}_32
%{_bindir}/python%{MAJOR_VERSION}_64
%{_bindir}/python%{BASE_VERSION}
%{_bindir}/python%{BASE_VERSION}_32
%{_bindir}/python%{BASE_VERSION}_64
%{_bindir}/python%{BASE_VERSION}m
%{_bindir}/python%{BASE_VERSION}m_32
%{_bindir}/python%{BASE_VERSION}m_64
%{_bindir}/pyvenv
%{_bindir}/pyvenv_32
%{_bindir}/pyvenv_64
%{_bindir}/pyvenv-%{BASE_VERSION}
%{_bindir}/pyvenv-%{BASE_VERSION}_32
%{_bindir}/pyvenv-%{BASE_VERSION}_64
%{_mandir}/*/*
#*/
/usr/bin/pydoc*
/usr/bin/python
/usr/bin/python_32
/usr/bin/python_64
/usr/bin/python%{MAJOR_VERSION}
/usr/bin/python%{MAJOR_VERSION}_32
/usr/bin/python%{MAJOR_VERSION}_64
/usr/bin/python%{BASE_VERSION}
/usr/bin/python%{BASE_VERSION}_32
/usr/bin/python%{BASE_VERSION}_64
/usr/bin/python%{BASE_VERSION}m
/usr/bin/python%{BASE_VERSION}m_32
/usr/bin/python%{BASE_VERSION}m_64
/usr/bin/pyvenv
/usr/bin/pyvenv_32
/usr/bin/pyvenv_64
/usr/bin/pyvenv-%{BASE_VERSION}
/usr/bin/pyvenv-%{BASE_VERSION}_32
/usr/bin/pyvenv-%{BASE_VERSION}_64
/usr/include/*
#*/
# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%{pylibdir}/config-%{LDVERSION_optimized}/Makefile
%{_includedir}/python%{LDVERSION_optimized}/pyconfig.h
%{_includedir}/python%{LDVERSION_optimized}/pyconfig-ppc32.h
%{_includedir}/python%{LDVERSION_optimized}/pyconfig-ppc64.h

%{_libdir}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
%{_libdir}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so
%{_libdir64}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.a
%{_libdir64}/libpython%{BASE_VERSION}%{VERSION_SUFFIX}.so


%files devel -f devel-pkg-files
%defattr(-,root,system,-)
%doc 32bit/Misc/README.valgrind 32bit/Misc/valgrind-python.supp
%doc 32bit/Misc/gdbinit
%{_bindir}/*config*
#*/
/usr/bin/*config*
#*/
# 32 bit files
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{BASE_VERSION}.pc
%{_libdir}/pkgconfig/python3.pc

# 64 bit files
%{_libdir64}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir64}/pkgconfig/python-%{BASE_VERSION}.pc
%{_libdir64}/pkgconfig/python3.pc


%files tools
%defattr(-,root,system,-)
%{_bindir}/2to3*
%{_bindir}/idle*
/usr/bin/2to3*
/usr/bin/idle*

%if %{include_tkinter} == 1
%files tkinter
%defattr(-,root,system,-)
%{pylibdir}/tkinter
%{dynload_dir}/_tkinter.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
#*/
%{pylibdir}/turtledemo/*.cfg
#*/
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*
#*/
%endif


%files test -f test-pkg-files
%defattr(-,root,system,-)


%files docs
%defattr(-,root,system,-)
%doc python-%{doc_version}-docs-text


#################################
#  Changelog
#################################
%changelog
* Mon Sep 05 2016 Tony Reix <tony.reix@atos.net> & Matthieu Sarter <matthieu.sarter.external@atos.net> - 3.5.2-3
- Add --without-computed-gotos
- Default is %{release} : compiled with GCC
- default commands are now built in 64 bit

* Thu Aug 25 2016 Tony Reix <tony.reix@atos.net> - 3.5.2-2
- Add gcc/xlc

* Wed Aug 24 2016 Tony Reix <tony.reix@atos.net> - 3.5.2-1
- Update to version 3.5.2 .

* Thu Aug 11 2016  Matthieu Sarter <matthieu.sarter.external@atos.net> - 3.5.1-2
- Added some missing files

* Wed Jun 29 2016  Matthieu Sarter <matthieu.sarter.external@atos.net> - 3.5.1-1
- Update to version 3.5.1

* Tue Jun 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.7.10-3
- Improved test handling in spec file

* Thu Jun 16 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.7.10-2
- Fixed pyconfig.h for 32/64 bits

* Thu Aug 06 2015 Tony Reix <tony.reix@atos.net> - 2.7.10-1
- Update to version 2.7.10

* Tue Dec 24 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.6-1
- regen for 2.7.6

* Tue Sep 13 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-4
- constraint openssl branch 0.9.8 for python_64 -c "import _hashlib;_hashlib.openssl_md5()" coredump issue

* Tue Aug 21 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-3
- constraint on openssl for do not used openssl 1.0.1 branch
- large file support for 32bits

* Tue Jun 10 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-2
- Fix time, hotshot
- Installed pure in lib, and platform in lib/lib64

* Tue May 22 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-1
- Fix some AIX and distutils issue
- Fix 64bit version

* Tue Apr 30 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.4-1
- Update to version 2.7.4 with new patches

* Tue Feb 19 2013 Gerard Visiedo <gerard.visiedo@bull.net>  2.7.3-1
- Update to version 2.7.3

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  2.7.2-3
- Initial port on Aix6.1

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

