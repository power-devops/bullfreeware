# PYTHON3 WITH XLC for AIX !!!!

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, xlc is used.
#%%bcond_with gcc_compiler
# By default, gcc is used.
%bcond_without gcc_compiler
# Choose GCC: rpmbuild -ba --with gcc_compiler *.spec

# Needed for patch Python-3.8.3-64bit_lib64.patch
#	file Modules/getpath.c
#	Hunk #2 
%global _default_patch_fuzz 2

%define __bzip2 /opt/freeware/bin/bzip2

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

%if %{with gcc_compiler}
%define compiler_msg This version has been compiled with GCC.
%else
%define sub_release xlc
%define compiler_msg This version has been compiled with XLC.
%endif

#By default, 64bit mode
%define default_bits 64


%define WITH_WITHOUT_MALLOC	--with-pymalloc
%define with_pmalloc 0

%if %{with gcc_compiler}
%define WITH_WITHOUT_GOTOS	--with-computed-gotos
%else
%define WITH_WITHOUT_GOTOS	--without-computed-gotos
%endif



#################################
#  End of user-modifiable configs
#################################
%define name python3
%define version 3.8.5
%define MAJOR_VERSION 3
%define BASE_VERSION 3.8
%define SHORT_VERSION 38

# Change VERSION_SUFFIX to empty when compiling without pymalloc
%if %{with_pmalloc} == 1
%define VERSION_SUFFIX m
%define ABIFLAGS_optimized %{VERSION_SUFFIX}
%define ABIFLAGS_debug     dm

%define LDVERSION_optimized %{BASE_VERSION}%{ABIFLAGS_optimized}
%define LDVERSION_debug     %{BASE_VERSION}%{ABIFLAGS_debug}

%define VERSION_LIB         %{BASE_VERSION}%{VERSION_SUFFIX}
%else
%define VERSION_SUFFIX ""

%define LDVERSION_optimized %{BASE_VERSION}
%define LDVERSION_debug     %{BASE_VERSION}d

%define VERSION_LIB         %{BASE_VERSION}
%endif

%define base_release 3
%define release %{base_release}%{?sub_release}%{?without_ibm_SSL:opensourcessl}
%define doc_version %{version}

# include_tkinter is now defined with --define command_line
#  kludge to get around rpm <percent>define weirdness
%define include_tkinter 1

%define _libdir64      %{_prefix}/lib64
%define pylibdir       %{_libdir}/python%{BASE_VERSION}
%define dynload_dir    %{pylibdir}/lib-dynload
%define pylibdir64     %{_libdir64}/python%{BASE_VERSION}
%define dynload_dir64  %{pylibdir64}/lib-dynload
%define pyscriptdir    %{_libdir}/python%{MAJOR_VERSION}
%define pylibdir_major %{_libdir}/python%{MAJOR_VERSION}


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

Source0: http://www.python.org/ftp/python/%{version}/Python-%{version}.tgz
Source1: pyconfig.h
Source2: http://www.python.org/ftp/python/doc/%{version}/python-%{doc_version}-docs-text.tar.bz2
Source3: %{name}-%{version}-%{base_release}.build.log

Source4: ChangePythonPrimaryVersion.sh

# 64 bits only : this patch ensures dynamic Python libs are loaded from lib64, not lib
Patch0: Python-%{version}-64bit_lib64.patch
# 32bit mirror patch to have script installed on python3/lib
Patch5: Python-%{version}-32bit_lib.patch
# Build is not generating the 64 bit config-xx/Makefile and other config files
Patch1: Python-%{version}-64bit_LIBPL.patch
# _LARGE_FILES should not be defined for 64bit build
Patch2: Python-%{version}-LFS_no_64bit-aix.patch

# # get_python_lib() to show lib64 for 64bit Python
# Patch3: Python-%{version}-libpath_fix-aix.patch

# Don't demangle C++ symbols hen using nm
Patch4: Python-%{version}-demangle-aix.patch

# kept here just in case...
# Patch 2, 3 10, 11, 13 no more useful with Python 3.5.2
#Patch2: Python-%{version}-aixsetup.patch
#Patch3: Python-%{version}-termios.patch
# http://bugs.python.org/issue11215
#Patch10: Python-%{version}-linkso.patch
#Patch11: Python-%{version}-ldshared.patch
#Patch13: Python-%{version}-Lib.ctypes.160309.patch
# Patch 7, 12 no more useful with Python 3.6.1
#Patch7: Python-%{version}-fileio.patch Python Issue28016  ~patch comitted 2016-11
#Patch12: Python-%{version}-compat.patch Python Issue28000 patch comitted 2016-11

Patch13: Python-%{version}-decimal-ExternStaticInlineMESS.patch

# %if %{with ibm_SSL}
# # Workaround to remvoe dependency over OpenSource OpenSSL
# Patch17: Python-%{version}-workaround-openssl.patch
# %endif

Provides: python-abi = %{BASE_VERSION}
Provides: python(abi) = %{BASE_VERSION}
Provides: python3 = %{version}-%{release}

# As python, pydoc is now a link created in %post, it must be declared as provided
Provides: /opt/freeware/bin/python
Provides: /opt/freeware/bin/pydoc

# new module include in 2.7
Provides: python3-argparse
Provides: python-unittest2
Provides: python-importlib
Provides: python-ordereddict

BuildRequires: bzip2-devel
BuildRequires: expat-devel >= 2.2.9
BuildRequires: gdbm-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: readline-devel >= 5.2
BuildRequires: sqlite-devel >= 3.30
BuildRequires: zlib-devel
BuildRequires: gettext-devel
BuildRequires: make
BuildRequires: ncurses
BuildRequires: pkg-config
BuildRequires: tcl
BuildRequires: tk
BuildRequires: xz-devel
BuildRequires: libgcc >= 8.3.0
BuildRequires: libstdc++ >= 8.3.0

Requires: bzip2
Requires: expat >= 2.2.9
Requires: gdbm >= 1.18.1-3
Requires: gmp
Requires: libffi >= 3.2.1
Requires: ncurses
Requires: readline >= 5.2
Requires: sqlite >= 3.30
Requires: zlib
Requires: gettext
Requires: libgcc >= 8.3.0
Requires: libstdc++ >= 8.3.0

%if %{without ibm_SSL}
# BullFreeware Openssl
BuildRequires: openssl-devel >= 1.0.2
Requires: openssl >= 1.0.2
%endif

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

# As python-config is now a link created in %post, it must be declared as provided
Provides: /opt/freeware/bin/python-config

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
# Requires: %{name}-tkinter = %{version}-%{release}

# As python-config is now a link created in %post, it must be declared as provided
Provides: /opt/freeware/bin/idle

%description tools
The Python package includes several development tools that are used
to build python programs.


%if %{include_tkinter} == 1
%package tkinter
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
BuildRequires: tcl-devel
BuildRequires: tk-devel
Requires: tcl > 8.6.6
Requires: tk > 8.6.6
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
# need tar from /opt/freeware to extract tar.xz archives
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# Extract python
%setup -q -n Python-%{version}

# Patch on the fly
perl -pi -e "s|yperr_string|(const char*)yperr_string|g;" \
Modules/nismodule.c

# Should autoreconf for coherent configures installed and generated version
#autoreconf

# %if %{with ibm_SSL}
# %patch17 -p1
# %endif

%patch13 -p1 -b .decimal-ExternStaticInlineMESS

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit

# Specific patches for 64 bit
cd 64bit
%patch0 -p1 -b .64bit_lib64
%patch1 -p1 -b .64bit_LIBPL
%patch2 -p1 -b .no_LFS
%patch4 -p1 -b .demangle

sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_64|" Lib/cgi.py > tmpfile.tmp
mv tmpfile.tmp Lib/cgi.py
if [ ! -f /opt/freeware/bin/python3_64 ]; then
    echo "WARNING : python3_64 not found. You will have to rebuild the package after installing the first build !"
    sleep 30
else
	for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1 | uniq`; do
		# inplace agnostic sed
		sed "s|\/usr\/bin\/env python3|\/usr\/bin\/env python3_64|" ${f} > tmpfile.tmp
		sed "s|\/usr\/bin\/env python\([^3]\)|\/usr\/bin\/env python_64\\1|" tmpfile.tmp > tmpfile.tmp2
		sed "s|\/usr\/bin\/env python$|\/usr\/bin\/env python_64|" tmpfile.tmp2 > tmpfile.tmp
		cp -f tmpfile.tmp ${f}
	done
fi
cd ..

cd 32bit
%patch5 -p1 -b .32bit_lib
sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_32|" Lib/cgi.py > tmpfile.tmp
mv tmpfile.tmp Lib/cgi.py
if [ ! -f /opt/freeware/bin/python3_32 ]; then
    echo "WARNING : python3_32 not found. You will have to rebuild the package after installing the first build !"
    sleep 30
else
	for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1 | uniq`; do
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

echo "WITH_WITHOUT_MALLOC: %{WITH_WITHOUT_MALLOC}"
echo "WITH_WITHOUT_GOTOS:  %{WITH_WITHOUT_GOTOS}"
echo "with_pmalloc:      : %{with_pmalloc}"
echo "VERSION_SUFFIX     : %{VERSION_SUFFIX}"

%if %{without ibm_SSL}
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
if [ -f %{_libdir64}/libssl.so ]; then
    mv %{_libdir64}/libssl.so /tmp/libssl.so.64
fi
%endif

# setup commun for 32-bit and 64-bit builds
export CONFIG_SHELL=%{_prefix}/bin/bash
export CONFIGURE_ENV_ARGS=%{_prefix}/bin/bash

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64 -B"
export RM="/usr/bin/rm -f"

export LIBFFI_INCLUDEDIR="/opt/freeware/include"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-brtl"

export LIBS="-lXext -lexpat -lffi -lncurses -lsqlite3"

export CFLAGS="  -I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -Wl,-brtl"
export CPPFLAGS="-I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses"

#export OPT="-g -O2"
# GCC -g -O0 entails: TOC overflow. TOC size: 65936       Maximum size: 65536
export OPT="-g -O0"
export OPT="   -O2"

# Used by both XLC and GCC (CreateExportList)
#export XLCCPATH="/opt/IBM/xlc/13.1.7/bin"
#export XLCXXPATH="/opt/IBM/xlC/13.1.7/bin"
export XLCCPATH="/opt/IBM/xlc/13.1.3/bin"
export XLCXXPATH="/opt/IBM/xlC/13.1.3/bin"

# Choose GCC or XLC
%if %{with gcc_compiler}

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

CFLAGS="$CFLAGS -fPIC -pthread"

echo "CC Version:"
$CC__ --version

%else

export CC__="$XLCCPATH/xlc_r"
export CXX__="$XLCXXPATH/xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"

export OPT="$OPT -qmaxmem=70000"
export CFLAGS="$CFLAGS -qbitfields=signed -qalloca"

echo "CC Version:"
$CC__ -qversion

%endif

export CFLAGS__="$CFLAGS $OPT"
export CXXFLAGS__="${CFLAGS}"

type $CC__
type $CXX__


build_python()
{
    set -x

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
        --with-system-expat \
	%{WITH_WITHOUT_MALLOC} \
        %{WITH_WITHOUT_GOTOS}

    # /usr/sbin/slibclean
    
    gmake --trace %{?_smp_mflags} libpython%{VERSION_LIB}.a
    
    $XLCCPATH/CreateExportList -X${OBJECT_MODE} libpython.exp libpython%{VERSION_LIB}.a
%if %{with gcc_compiler}
    # GCC
    ${CC} ${CFLAGS} -shared    libpython%{VERSION_LIB}.a -o libpython%{VERSION_LIB}.so -Wl,-bE:libpython.exp -lm -lpthreads          -lintl -Wl,-blibpath:$1:/opt/freeware/lib:/usr/lib:/lib
%else
    # xlc
    ${CC} ${CFLAGS} -qmkshrobj libpython%{VERSION_LIB}.a -o libpython%{VERSION_LIB}.so     -bE:libpython.exp -lm -L/opt/freeware/lib -lintl     -blibpath:$1:/opt/freeware/lib:/usr/lib:/lib
%endif
    rm -f libpython.exp
    mv -f libpython%{VERSION_LIB}.a libpython%{VERSION_LIB}.a.old
    ${AR} -r libpython%{VERSION_LIB}.a libpython%{VERSION_LIB}.so

    gmake --trace %{?_smp_mflags}
}


# build 64-bit version
export OBJECT_MODE=64
export CC=${CC__}
export CXX=${CXX__}

export CFLAGS="${CFLAGS__} ${FLAG64}"
export CXXFLAGS="${CXXFLAGS__} ${FLAG64}"

export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"
%if %{with gcc_compiler}
  export LDFLAGS="$LDFLAGS -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib ${FLAG64} -pthread"
  export CFLAGS="${CFLAGS} -pthread"
  export CXXFLAGS="${CXXFLAGS} -pthread"
%else
  # libgcc_s.a is used by dependencies. Thus it must be "pthread" !
  export LDFLAGS="$LDFLAGS     -blibpath:/opt/freeware/lib/pthread/ppc64:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib ${FLAG64}"
%endif

cd 64bit
export LIBPATH=`pwd`
build_python %{_libdir64}
cd ..


# build 32-bit version
export OBJECT_MODE=32
export CC=${CC__}
export CXX=${CXX__}

export CFLAGS="${CFLAGS__} ${FLAG32} -D_LARGE_FILES"
export CXXFLAGS="${CXXFLAGS__} ${FLAG32} -D_LARGE_FILES"

export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir} -L/usr/lib -Wl,-brtl"
%if %{with gcc_compiler}
  export LDFLAGS="$LDFLAGS -Wl,-blibpath:/opt/freeware/lib/pthread:%{_libdir}:/usr/lib -Wl,-bmaxdata:0x80000000 ${FLAG32} -pthread"
  export CFLAGS="${CFLAGS} -pthread"
  export CXXFLAGS="${CXXFLAGS} -pthread"
%else
  export LDFLAGS="$LDFLAGS     -blibpath:/opt/freeware/lib/pthread:%{_libdir}:/usr/lib ${FLAG32}"
%endif

cd 32bit
export LIBPATH=`pwd`
build_python %{_libdir}
cd ..


%if %{without ibm_SSL}
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
%endif


#################################
#  Install
#################################
%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# install 64-bit version

export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

install_python() {
    set -ex
    cd ${OBJECT_MODE}bit
    gmake DESTDIR=${RPM_BUILD_ROOT} install

    cp ${RPM_BUILD_ROOT}%{_includedir}/python%{VERSION_LIB}/pyconfig.h ${RPM_BUILD_ROOT}%{_includedir}/python%{VERSION_LIB}/pyconfig-ppc${OBJECT_MODE}.h

    (
      cd ${RPM_BUILD_ROOT}%{_bindir}

	  # Add the architecture suffix to binaries' name and
	  # add links between base_version, major_version, etc
      for f in 2to3; do
        mv ${f}-%{BASE_VERSION} ${f}-%{BASE_VERSION}_${OBJECT_MODE} ;
        ln -sf ${f}-%{BASE_VERSION}_64 ${f}_${OBJECT_MODE}
      done

      for f in idle pydoc python ; do
        mv     ${f}%{BASE_VERSION}                ${f}%{BASE_VERSION}_${OBJECT_MODE}
        ln -sf ${f}%{BASE_VERSION}_${OBJECT_MODE} ${f}_${OBJECT_MODE}
        ln -sf ${f}%{BASE_VERSION}_${OBJECT_MODE} ${f}%{MAJOR_VERSION}_${OBJECT_MODE}
      done

      
      %if %{with_pmalloc} == 1
      mv     python%{VERSION_LIB}                         python%{VERSION_LIB}_${OBJECT_MODE}
      ln -sf python%{VERSION_LIB}_${OBJECT_MODE}          python%{BASE_VERSION}_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}_${OBJECT_MODE}         python%{MAJOR_VERSION}_${OBJECT_MODE}
      %else
      ln -sf python%{VERSION_LIB}_${OBJECT_MODE}          python%{MAJOR_VERSION}_${OBJECT_MODE}
      %endif
      ln -sf python%{MAJOR_VERSION}_${OBJECT_MODE}        python_${OBJECT_MODE}
      
      %if %{with_pmalloc} == 1
      mv     python%{VERSION_LIB}-config                  python%{VERSION_LIB}-config_${OBJECT_MODE}
      ln -sf python%{VERSION_LIB}-config_${OBJECT_MODE}   python%{BASE_VERSION}-config_${OBJECT_MODE}
      ln -sf python%{BASE_VERSION}-config_${OBJECT_MODE}  python%{MAJOR_VERSION}-config_${OBJECT_MODE}
      %else
      mv     python%{VERSION_LIB}-config                  python%{VERSION_LIB}-config_${OBJECT_MODE}
      ln -sf python%{VERSION_LIB}-config_${OBJECT_MODE}   python%{MAJOR_VERSION}-config_${OBJECT_MODE}
      %endif
      ln -sf python%{MAJOR_VERSION}-config_${OBJECT_MODE} python-config_${OBJECT_MODE}

      # Change python name in scripts
      for f in 2to3 pyvenv idle pydoc python%{LDVERSION_optimized}-config; do
        if [ -f ${f}_${OBJECT_MODE} ]; then
          cat ${f}_${OBJECT_MODE} | sed "s|\/opt\/freeware\/bin\/python%{BASE_VERSION}|\/opt\/freeware\/bin\/python%{BASE_VERSION}_${OBJECT_MODE}|" > tmpfile.tmp
          mv -f tmpfile.tmp ${f}_${OBJECT_MODE}
		  chmod +x ${f}_${OBJECT_MODE}
        fi
      done

	  # Same for smtpd.py
	  cat smtpd_${OBJECT_MODE}.py  | sed "s|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}_${OBJECT_MODE}|" > tmpfile.tmp
	  mv -f tmpfile.tmp smtpd_${OBJECT_MODE}.py
	  chmod +x smtpd_${OBJECT_MODE}.py

	  rm -f tmpfile.tmp
      cd ..

      # if [  ${OBJECT_MODE} == 64 ]
      # then
	  # 	  cd ${RPM_BUILD_ROOT}%{_libdir}
	  # 	  mv python%{BASE_VERSION}/config-%{VERSION_LIB} ${RPM_BUILD_ROOT}/%{_libdir64}/python%{BASE_VERSION}/config-%{VERSION_LIB}
	  # 	  cd ..
      # fi
    )
    cd ..
}

# install 64-bit version
export OBJECT_MODE=64

export LIBPATH="`pwd`:/opt/freeware/lib/pthread/ppc64:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib"
%if %{with gcc_compiler}
  export LDFLAGS="-Wl,-blibpath:$LIBPATH -Wl,-brtl"
  export LDFLAGS="$LDFLAGS -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib"
%else
  export LDFLAGS="    -blibpath:$LIBPATH -Wl,-brtl"
  # libgcc_s.a is used by dependencies. Thus it must be "pthred" !
  export LDFLAGS="$LDFLAGS     -blibpath:/opt/freeware/lib/pthread/ppc64:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib"
%endif
install_python

# Move /opt/freeware/lib/python3.6/config-3.6m/* to /opt/freeware/lib64/python3.6/config-3.6m/*

mkdir -p  ${RPM_BUILD_ROOT}%{pylibdir64}/config-%{LDVERSION_optimized}
mv  ${RPM_BUILD_ROOT}%{pylibdir}/config-%{LDVERSION_optimized}/*  ${RPM_BUILD_ROOT}%{pylibdir64}/config-%{LDVERSION_optimized}
rm -f  ${RPM_BUILD_ROOT}%{pylibdir64}/config-%{LDVERSION_optimized}/libpython%{VERSION_LIB}.a


# install 32-bit version
export OBJECT_MODE=32

export LIBPATH="`pwd`:/opt/freeware/lib/pthread:/usr/lib/threads:%{_libdir}:/usr/lib"
%if %{with gcc_compiler}
  export LDFLAGS="-Wl,-blibpath:$LIBPATH -Wl,-brtl"
  export LDFLAGS="$LDFLAGS -Wl,-blibpath:/opt/freeware/lib/pthread:%{_libdir}:/usr/lib -Wl,-bmaxdata:0x80000000"
%else
  export LDFLAGS="    -blibpath:$LIBPATH -Wl,-brtl"
  export LDFLAGS="$LDFLAGS     -blibpath:/opt/freeware/lib/pthread:%{_libdir}:/usr/lib"
%endif
install_python


# python header
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/python%{VERSION_LIB}/pyconfig.h

cp %{_builddir}/Python-%{version}/32bit/libpython%{VERSION_LIB}.a ${RPM_BUILD_ROOT}%{_libdir}/libpython%{VERSION_LIB}.a
#cp %{_builddir}/Python-%{version}/64bit/libpython%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{BASE_VERSION}.a
ln -sf ../lib/libpython%{VERSION_LIB}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{VERSION_LIB}.a

# Add the 64 bit shared object to the 32/64 bits archive
${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libpython%{VERSION_LIB}.a ${RPM_BUILD_ROOT}%{_libdir64}/libpython%{VERSION_LIB}.so

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

  ln -sf smtpd_${DEFAULT_BITS}.py smtpd.py

  cd ..
)


# Why NOT ??
echo "Why NOT strip ????????????????????????????????????????????????????????????????????????????"
#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
#*/
(
  cd ${RPM_BUILD_ROOT}
  # Only make link for include dir
  # for dir in bin include lib lib64
  for dir in include
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
ln -sf ../../libpython%{VERSION_LIB}.a ${RPM_BUILD_ROOT}%{_libdir}/python%{BASE_VERSION}/config-%{VERSION_LIB}/libpython%{VERSION_LIB}.a
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/python%{BASE_VERSION}/config-%{VERSION_LIB}
ln -sf ../../libpython%{VERSION_LIB}.a ${RPM_BUILD_ROOT}%{_libdir64}/python%{BASE_VERSION}/config-%{VERSION_LIB}/libpython%{VERSION_LIB}.a

(
  cd ${RPM_BUILD_ROOT}%{pylibdir64} 
  ln -s config-%{LDVERSION_optimized} config 
)

(
  cd ${RPM_BUILD_ROOT}%{pylibdir}
  ln -s config-%{LDVERSION_optimized} config
)

(
  mkdir -p ${RPM_BUILD_ROOT}%{pylibdir_major}
  cd ${RPM_BUILD_ROOT}%{pylibdir_major}
  ln -s ../python%{BASE_VERSION}/config-%{LDVERSION_optimized} config
)

# Create files list for the different packages

# main package
rm -rf main-pkg-files
find ${RPM_BUILD_ROOT}%{pylibdir}   -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" > main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir}   -type f                                    >> main-pkg-files.tmp
find ${RPM_BUILD_ROOT}%{pylibdir64} -type f                                    >> main-pkg-files.tmp
cat main-pkg-files.tmp | \
  grep -v "_ctypes_test.so" | \
  grep -v "_testbuffer.so" | \
  grep -v "_testcapi.so" | \
  grep -v "_testimportmultiple.so" | \
  grep -v "_testmultiphase.so" | \
  grep -v "/test/" | \
  grep -v "ctypes/test" |\
  grep -v "distutils/test" |\
  grep -v "lib2to3/test" | \
  grep -v "sqlite3/test" |\
  grep -v "unittest/test" | \
  grep -v "tkinter" | \
  grep -v "_tkinter.so" | \
  grep -v "turtle" | \
  grep -v "config-%{LDVERSION_optimized}" | \
  sed -e "s|${RPM_BUILD_ROOT}||" | \
  sed -e "s|\ |*|" | \
  sed -e "s|%dir\*|%dir |"  >> main-pkg-files


# test package
cat main-pkg-files.tmp | grep "_ctypes_test.so"         > test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testbuffer.so"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testcapi.so"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testimportmultiple.so" >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "_testmultiphase.so"     >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "/test/"                 >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "ctypes/test"            >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "distutils/test"         >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "lib2to3/test"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "sqlite3/test"           >> test-pkg-files.tmp
cat main-pkg-files.tmp | grep "tkinter/test"           >> test-pkg-files.tmp
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

# Install the Change Python Primary Version shell script
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_bindir}/

# Create an empty folder for scripts
mkdir -p ${RPM_BUILD_ROOT}%{pyscriptdir}
mkdir -p ${RPM_BUILD_ROOT}%{pyscriptdir}/site-packages

#################################
#  Check
#################################
%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

test_python() {
    set -ex
    echo "Testing ${OBJECT_MODE} bit build"
    # For some test, including lzma (-d) and io (-f)
    ulimit -d 4000000
    # ulimit -f unlimited # Not OK on user
    ulimit -m 4000000
    export LIBPATH=`pwd`:/opt/freeware/lib:/usr/lib
    export PYTHONPATH=`pwd`/Modules
    # Some tests hang when running the whole test_suite, so we need to ignore them first and run them separately later
    #( ./python Lib/test/regrtest.py -x test_io -x test_signal -x test_socket -x test_subprocess -x test_poplib || true )
    #( ./python Lib/test/regrtest.py test_io test_signal test_socket test_subprocess test_poplib || true )
    #( gmake -k test || true )
    ( ./python Lib/test/regrtest.py -x test_multiprocessing_fork -x test_interrupted_read_retry_buffered -x test_concurrent_futures || true )
    ( ./python Lib/test/regrtest.py    test_multiprocessing_fork    test_interrupted_read_retry_buffered    test_concurrent_futures || true ) 
    # ( gmake -k testall || true )
    /usr/sbin/slibclean
    unset PYTHONPATH
}


cd 64bit
# test 64-bit version
export OBJECT_MODE=64
test_python
cd ..

cd 32bit
# tests 32-bit version
export OBJECT_MODE=32
test_python
cd ..


#################################
#  Clean
#################################
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#################################
#  Pre/Post
#################################
%post
# Python3 is default. Don't change links.
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

cd %{_bindir}

ln -sf python3    python
ln -sf python3_32 python_32
ln -sf python3_64 python_64
ln -sf pydoc3     pydoc
ln -sf pydoc3_32  pydoc_32
ln -sf pydoc3_64  pydoc_64

# Python3 is default. Don't change links.
%postun
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

# Python 3 exists. Choose by default.
if [[ -e %{_bindir}/python2 ]]; then
	cd %{_bindir}
	ln -sf python2    python
	ln -sf python2_32 python_32
	ln -sf python2_64 python_64
	ln -sf pydoc2     pydoc
	ln -sf pydoc2_32  pydoc_32
	ln -sf pydoc2_64  pydoc_64
else
	# Remove links
	unlink %{_bindir}/python
	unlink %{_bindir}/python_32
	unlink %{_bindir}/python_64
	unlink %{_bindir}/pydoc
	unlink %{_bindir}/pydoc_32
	unlink %{_bindir}/pydoc_64
fi

%post devel
# Python3 is default. Don't change links.
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

cd %{_bindir}
ln -sf python3-config    python-config
ln -sf python3-config_32 python-config_32
ln -sf python3-config_64 python-config_64

%postun devel
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

if [[ -e %{_bindir}/python2-config ]]; then
	cd %{_bindir}
	ln -sf python2-config    python-config
	ln -sf python2-config_32 python-config_32
	ln -sf python2-config_64 python-config_64
else
	unlink %{_bindir}/python-config
	unlink %{_bindir}/python-config_32
	unlink %{_bindir}/python-config_64
fi

%post tools
# Python3 is default. Don't change links.
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

cd %{_bindir}
ln -sf idle3    idle
ln -sf idle3_32 idle_32
ln -sf idle3_64 idle_64

%postun tools
if %{_bindir}/python --version 2>&1 | grep -q "Python 2"; then
	exit 0
fi

if [[ -e %{_bindir}/idle2 ]]; then
	cd %{_bindir}
	ln -sf idle2    idle
	ln -sf idle3_32 idle_32
	ln -sf idle2_64 idle_64
else
	unlink %{_bindir}/idle
	unlink %{_bindir}/idle_32
	unlink %{_bindir}/idle_64
fi


#################################
#  File
#################################
%files -f main-pkg-files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/README.rst
%dir %{pyscriptdir}
%dir %{pyscriptdir}/site-packages
%{_bindir}/pydoc%{MAJOR_VERSION}
%{_bindir}/pydoc%{MAJOR_VERSION}_32
%{_bindir}/pydoc%{MAJOR_VERSION}_64
%{_bindir}/pydoc%{BASE_VERSION}
%{_bindir}/pydoc%{BASE_VERSION}_32
%{_bindir}/pydoc%{BASE_VERSION}_64
%{_bindir}/python%{MAJOR_VERSION}
%{_bindir}/python%{MAJOR_VERSION}_32
%{_bindir}/python%{MAJOR_VERSION}_64
%{_bindir}/python%{BASE_VERSION}
%{_bindir}/python%{BASE_VERSION}_32
%{_bindir}/python%{BASE_VERSION}_64
%if "%{LDVERSION_optimized}" != "%{BASE_VERSION}"
%{_bindir}/python%{LDVERSION_optimized}
%{_bindir}/python%{LDVERSION_optimized}_32
%{_bindir}/python%{LDVERSION_optimized}_64
%endif
# pyvenv is no more provided by python; use python -m venv
#%{_bindir}/pyvenv
#%{_bindir}/pyvenv_32
#%{_bindir}/pyvenv_64
#%{_bindir}/pyvenv-%{BASE_VERSION}
#%{_bindir}/pyvenv-%{BASE_VERSION}_32
#%{_bindir}/pyvenv-%{BASE_VERSION}_64
%{_bindir}/ChangePythonPrimaryVersion.sh
%{_mandir}/*/*
# /usr/bin/python
# /usr/bin/python%{MAJOR_VERSION}
# /usr/bin/python%{BASE_VERSION}
# /usr/bin/python%{BASE_VERSION}m
# /usr/bin/pyvenv
# /usr/bin/pyvenv-%{BASE_VERSION}
# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%{pylibdir}/config-%{LDVERSION_optimized}
%{pylibdir64}/config-%{LDVERSION_optimized}
%{pylibdir}/config
%{pylibdir64}/config
%{pylibdir_major}/config
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/pyconfig.h
%{_includedir}/python%{LDVERSION_optimized}/pyconfig-ppc32.h
%{_includedir}/python%{LDVERSION_optimized}/pyconfig-ppc64.h
# /usr links
# /usr/include/python%{LDVERSION_optimized}

%{_libdir}/libpython%{VERSION_LIB}.a
%{_libdir}/libpython%{VERSION_LIB}.so
%{_libdir64}/libpython%{VERSION_LIB}.a
%{_libdir64}/libpython%{VERSION_LIB}.so


%files devel -f devel-pkg-files
%defattr(-,root,system,-)
%doc 32bit/Misc/README.valgrind 32bit/Misc/valgrind-python.supp
%doc 32bit/Misc/gdbinit
%{_bindir}/python%{MAJOR_VERSION}-config
%{_bindir}/python%{MAJOR_VERSION}-config_32
%{_bindir}/python%{MAJOR_VERSION}-config_64
%{_bindir}/python%{BASE_VERSION}-config
%{_bindir}/python%{BASE_VERSION}-config_32
%{_bindir}/python%{BASE_VERSION}-config_64
%if "%{LDVERSION_optimized}" != "%{BASE_VERSION}"
%{_bindir}/python%{LDVERSION_optimized}-config
%{_bindir}/python%{LDVERSION_optimized}-config_32
%{_bindir}/python%{LDVERSION_optimized}-config_64
%endif
#*/
# /usr/bin/python3*config*
# 32 bit files
%{_libdir}/pkgconfig/python-%{BASE_VERSION}.pc
%{_libdir}/pkgconfig/python3.pc

# 64 bit files
%{_libdir64}/pkgconfig/python-%{BASE_VERSION}.pc
%{_libdir64}/pkgconfig/python3.pc

%if "%{LDVERSION_optimized}" != "%{BASE_VERSION}"
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir64}/pkgconfig/python-%{LDVERSION_optimized}.pc
%endif

%files tools
%defattr(-,root,system,-)
%{_bindir}/2to3
%{_bindir}/2to3_32
%{_bindir}/2to3_64
%{_bindir}/2to3-%{BASE_VERSION}
%{_bindir}/2to3-%{BASE_VERSION}_32
%{_bindir}/2to3-%{BASE_VERSION}_64
%{_bindir}/idle%{MAJOR_VERSION}
%{_bindir}/idle%{MAJOR_VERSION}_32
%{_bindir}/idle%{MAJOR_VERSION}_64
%{_bindir}/idle%{BASE_VERSION}
%{_bindir}/idle%{BASE_VERSION}_32
%{_bindir}/idle%{BASE_VERSION}_64
# /usr/bin/2to3*
# /usr/bin/idle3*

%if %{include_tkinter} == 1
%files tkinter
%defattr(-,root,system,-)
%{pylibdir}/tkinter
%{dynload_dir}/_tkinter.so
%{dynload_dir64}/_tkinter.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*
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
* Mon Oct 19 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 3.8.5-3
- Remove db Requires

* Fri Jul 31 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.8.5-2
- Bit-flag are now on C(XX)FLAGS and not in CC/CXX,
    so they will be memorized by Python to compile Modules.

* Tue Jul 21 2020 Tony Reix <tony.reix@atos.net> 3.8.5-1
- New version 3.8.5

* Mon Jun 08 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.8.3-1
- Add a link from python3/config to python3.<version>/config-3.<version>
- New version 3.8.3

* Fri Feb 21 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.8.1-3
- Fix files distributed by python3 itself and python3-devel

* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.8.1-2
- Bullfreeware OpenSSL removal

* Fri Jan 24 2020 Étienne Guesnet <etienne.guesnet.extenal@atos.net> - 3.8.1-1
- Update to 3.8.1
- Fix scripts path

* Wed Dec 18 2019 Clément Chigot <clement.chigot@atos.net> - 3.7.4-5
- Remove OpenSources SSL dependency

* Mon Dec 02 2019 Clément Chigot <clement.chigot@atos.net> - 3.7.4-4
- Fix libpath of libpython3.Xm.a(libpython3.Xm.so)

* Thu Nov 07 2019 Ayappan P <ayappap2@in.ibm.com> - 3.7.4-3
- Fix demangling issue with C++ code compilation in AIX

* Tue Sep 17 2019 Clément Chigot <clement.chigot@atos.net> - 3.7.4-2
- Move tests to %check section
- Remove /usr links
- Remove BuildRoot
- Clean LIBPATH. /usr/lib/pthread does not exist
- Fix python2 and python3 conflict files:
    Links are now created during %post
	Merge both ChangePrimaryToPythonX.sh scripts to ChangePythnoPrimaryVersion.sh

* Mon Aug 05 2019 Ayappan P <ayappap2@in.ibm.com> - 3.7.4-1
- Update to 3.7.4 which has fixes for following CVEs
- CVE-2019-9948
- CVE-2019-9740

* Thu Apr 04 2019 Ayappan P <ayappap2@in.ibm.com> - 3.7.3-1
- Update to 3.7.3 which has fixes for following CVEs
- CVE 2019-5010
- CVE 2019-9636

* Fri Jan 11 2019 Ayappan P <ayappap2@in.ibm.com> - 3.7.1-1
- Update to 3.7.1 version

* Mon Dec 24 2018 Ayappan P <ayappap2@in.ibm.com> - 3.7.0-1
- Various fixes to make python3 robust

* Wed Nov 21 2018 Michael Wilson <michael.a.wilson@atos.net> 3.6.5-3
- Include 64 bit config files
- Include %pre and %postun to check/change primary python version
- Include migration shell scripts to change primary python version

* Thu Oct 25 2018 Tony Reix <tony.reix@atos.net> 3.6.5-2
- Fix the issue with libffi 20170516
- Fix the 64bit issue with Python-%{version}-64bit_lib64.patch !!

* Fri Sep 14 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.7.0-1
- Updated to 3.7.0.
- Created 64bit patch and applied. 
- Removed wrong dependencies added right dependencies.
- Removed unwanted patches.
- Shipping "idle" in python2 shipping only "idle3" with python3.
- Shipping 2to3 only with python3.
- Shipping python3-tkinter.

* Wed Jul 11 2018 Reshma V Kumar <reskumar@in.ibm.com> - 3.6.6-1
- Updated to 3.6.6 to fix security vulnerability

* Thu May 24 2018 Sena Apeke <sena.apeke.external@atos.net> 3.6.5-1
- Update to version 3.6.5

* Mon Mar 26 2018 Daniele Silvestre <daniele.silvestre@atos.net> - 3.6.4-1
- Update to version 3.6.4
- Fix _tkinter.so delivery for 64bit version
- tkinter package always built

* Wed Aug 2 2017 Daniele Silvestre <daniele.silvestre@atos.net> - 3.6.2-1
- Update to version 3.6.2

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

* Tue Sep 10 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-4
- constraint openssl branch 0.9.8 for python_64 -c "import _hashlib;_hashlib.openssl_md5()" coredump issue

* Tue Aug 20 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-3
- constraint on openssl for do not used openssl 1.0.1 branch
- large file support for 32bits

* Mon Jun 10 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-2
- Fix time, hotshot
- Installed pure in lib, and platform in lib/lib64

* Tue May 21 2013 Tristan Delhalle <tristan.delhalle@ext.bull.net> - 2.7.5-1
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

