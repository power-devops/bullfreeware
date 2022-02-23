# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# Revert to UCS2 when building with gcc for python.exp compatibility
# Fedora specifies ucs4, but for AIX this creates incompatibility with all
# previous versions of python.exp and _sysconfigdata.py, used to build
# Python modules, leading to impossibilty to load for "import <module>"
%global unicode ucs2

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

#By default, 64bit mode
%define default_bits 64

#########################
#  User-modifiable configs
##########################
#  Build tkinter?
#WARNING: Commenting out doesn t work.  Last line is what s used.
%define config_tkinter yes

#################################
#  End of user-modifiable configs
#################################
%define name python
%define version 2.7.17
%define MAJOR_VERSION 2
%define BASE_VERSION 2.7
%define base_release 2
%define release %{base_release}%{?without_ibm_SSL:opensourcessl}

# When the build stops in the middle, files are not put back at their original place
# Run:
# ln -s /opt/freeware/lib64/libssl.so.1.0.2 /opt/freeware/lib64/libssl.so ; ln -s /opt/freeware/lib64/libcrypto.so.1.0.2 /opt/freeware/lib64/libcrypto.so ; ln -s /opt/freeware/lib/libssl.so.1.0.2 /opt/freeware/lib/libssl.so ; ln -s /opt/freeware/lib/libcrypto.so.1.0.2 /opt/freeware/lib/libcrypto.so

#  kludge to get around rpm <percent>define weirdness
%define include_tkinter %(if [ "%{config_tkinter}" = yes ]; then echo 1; else echo 0; fi)

%define _libdir64 %{_prefix}/lib64

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
Source2: http://www.python.org/ftp/python/doc/%{version}/python-%{version}-docs-text.tar.bz2

Source3: %{name}-%{version}-%{base_release}.build.log

# 64 bits only: use lib64 instead of lib !
Patch0: Python-%{version}-64bit.patch
Patch16: Python-%{version}-no_LFS_64bit.patch

# Common patches
Patch1: Python-%{version}-aix.patch
Patch2: Python-%{version}-aixsetup.patch
Patch3: Python-%{version}-termios.patch
Patch4: Python-%{version}-test.patch
Patch9: Python-%{version}-README.AIX.patch

Patch10: Python-%{version}-linkso.patch
Patch11: Python-%{version}-ldshared.patch
Patch13: Python-%{version}-pthread-stack-size.patch

# Fixes the "lack of support" for cdll/find_library - Michael Felt
Patch14: Python-%{version}-Lib.ctypes.160309.patch

Patch15: Python-%{version}-xxsubtype.patch

# %if %{with ibm_SSL}
# # Workaround to remvoe dependency over OpenSource OpenSSL
# Patch17: Python-%{version}-workaround-openssl.patch
# %endif

Provides: python-abi = %{BASE_VERSION}
Provides: python(abi) = %{BASE_VERSION}
Provides: python2 = %{version}

# As python, pydoc is now a link created in %post, it must be declared as provided
Provides: /opt/freeware/bin/python
Provides: /opt/freeware/bin/pydoc

# new module include in 2.7
Provides: python-argparse
Provides: python-unittest2
Provides: python-importlib
Provides: python-ordereddict

BuildRequires: bzip2-devel
BuildRequires: bzip2
# BuildRequires: db-devel >= 4.7
# BuildRequires: expat-devel >= 2.1.0
BuildRequires: expat-devel >= 2.2.4
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
BuildRequires: libgcc >= 8.3.0
BuildRequires: libstdc++ >= 8.3.0

Requires: bzip2
# Requires: db >= 4.8
# Requires: expat >= 2.1.0
Requires: expat >= 2.2.4
Requires: gdbm
Requires: libffi
Requires: ncurses
Requires: readline >= 5.2
Requires: sqlite >= 3.30
Requires: zlib
Requires: gettext >= 0.19.7
Requires: libgcc >= 8.3.0
Requires: libstdc++ >= 8.3.0


%if %{without ibm_SSL}
# BullFreeware Openssl
BuildRequires: openssl-devel >= 1.0.2s
Requires: openssl >= 1.0.2s
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

Python executables and library are available as 32-bit and 64-bit.

%if %{with gcc_compiler}
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


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

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: %{name} = %{version}-%{release}

# As python-config is now a link created in %post, it must be declared as provided
Provides: /opt/freeware/bin/idle

%description tools
The Python package includes several development tools that are used
to build python programs.

%if %{include_tkinter}
%package tkinter
Summary: A graphical user interface for the Python scripting language.
Group: Development/Languages
Provides: tkinter = %{version}-%{release}
Obsoletes: tkinter
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
%endif

%package test
Summary: The test modules from the main python package
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description test
The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you re developing python
code that uses more than just unittest and/or test_support.py.

%package docs
Summary: Documentation for the Python programming language
Group: Documentation
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

# Extract python
%setup -q -n Python-%{version}

# Then patch it
%patch1 -p1 -b .aix
%patch2 -p1 -b .aixsetup
%patch3 -p1 -b .termios
%patch4 -p1 -b .test
%patch9 -p1 -b .README.AIX
%patch10 -p1 -b .linkso
%patch11 -p1 -b .ldshared
%patch13 -p1 -b .pthread-stack-size
%patch14 -p1 -b .Lib.ctypes.160309
%patch15 -p0

# %if %{with ibm_SSL}
# %patch17 -p1
# %endif

# Patch on the fly
perl -pi -e "s|yperr_string|(const char*)yperr_string|g;" \
Modules/nismodule.c

# Should autoreconf for coherent configures installed and generated version
#autoreconf

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# Specific patch for 32 bits
# Starting from python-2.7.16-2, python might be a link towards python_64.
# Therefore, /usr/bin/env python must be replaced by /usr/bin/env python_32
PY_VERSION=`python --version 2>&1 | awk '{print($2)}'`
NEED_32=False
if [[ "$PY_VERSION" > "2.7.16" ]]; then
	NEED_32=True
elif [[ "$PY_VERSION" == "2.7.16" ]]; then
	RELEASE=`rpm -qa | grep "^python-2" | awk -F- '{print($3)}' | awk -F. '{print($1)}'`
	if [[ "$RELEASE"  -ge "2" ]]; then
		NEED_32=True
	fi
fi
if [[ "$NEED_32" == "True" ]]; then
	cd 32bit
	sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_32|" Lib/cgi.py > tmpfile.tmp
	mv tmpfile.tmp Lib/cgi.py
	for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1 | uniq` ; do
		# inplace agnostic sed
		sed "s|\/usr\/bin\/env python3|\/usr\/bin\/env python3_32|" ${f} > tmpfile.tmp
		sed "s|\/usr\/bin\/env python\([^3]\)|\/usr\/bin\/env python_32\\1|" tmpfile.tmp > tmpfile.tmp2
		sed "s|\/usr\/bin\/env python$|\/usr\/bin\/env python_32|" tmpfile.tmp2 > tmpfile.tmp
		cp -f tmpfile.tmp ${f}
	done
	cd ..
fi

# Specific patch for 64 bit
cd 64bit
%patch0 -p1 -b .64bit
%patch16 -p1 -b .no_LFS
sed "s|#! \/usr\/local\/bin\/python|#! \/opt\/freeware\/bin\/python_64|" Lib/cgi.py > tmpfile.tmp
mv tmpfile.tmp Lib/cgi.py
for f in `grep -R "/usr/bin/env python" * | cut -d ":" -f 1 | uniq`; do
	# inplace agnostic sed
    sed "s|\/usr\/bin\/env python3|\/usr\/bin\/env python3_64|" ${f} > tmpfile.tmp
    sed "s|\/usr\/bin\/env python\([^3]\)|\/usr\/bin\/env python_64\\1|" tmpfile.tmp > tmpfile.tmp2
    sed "s|\/usr\/bin\/env python$|\/usr\/bin\/env python_64|" tmpfile.tmp2 > tmpfile.tmp
    cp -f tmpfile.tmp ${f}
done
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
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{_libdir64}/libssl.so /tmp/libssl.so.64
fi
%endif

# setup commun for 32-bit and 64-bit builds
export CONFIG_SHELL=%{_prefix}/bin/bash
export CONFIGURE_ENV_ARGS=%{_prefix}/bin/bash

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export LIBS="-lXext -lexpat -lffi -lncurses -lsqlite3"

export CFLAGS="  -I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses"
export CPPFLAGS="-I/usr/include -I%{_prefix}/include -I%{_prefix}/include/ncurses"

# -qinfo=als generate a XLC internal error when compiling Objects/typeobject.c
#export OPT="-g -O0 -qinfo=als"
export OPT="-O2"

#export XLCCPATH="/usr/vac/bin"
#export XLCXXPATH="/usr/vac/bin"
export XLCCPATH="/opt/IBM/xlc/13.1.3/bin"
export XLCXXPATH="/opt/IBM/xlC/13.1.3/bin"


# Chose GCC or XLC
%if %{with gcc_compiler}

export CFLAGS="$CFLAGS  $RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fno-strict-aliasing -fwrapv -D_LINUX_SOURCE_COMPAT"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fno-strict-aliasing -fwrapv -D_LINUX_SOURCE_COMPAT"
export CPPFLAGS="$CPPFLAGS $(pkg-config --cflags-only-I libffi)"
export OPT="     $RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fno-strict-aliasing -fwrapv"
export LDFLAGS="$RPM_LD_FLAGS"
if pkg-config openssl ; then
  export CFLAGS=" $CFLAGS  $(pkg-config --cflags openssl)"
  export LDFLAGS="$LDFLAGS $(pkg-config --libs-only-L openssl)"
fi

export  CC="/usr/bin/gcc"
export CXX="/usr/bin/gcc"

# Use "-brtl" flag when building with gcc for ".so" / ".a" compatibility.
# Without "-brtl" flag there is a thread data/context issue while importing
# older python modules (e.g. python2.7/site-packages/rpm/_rpm.so) which
# were built using XLC and which resolve to libpython2.7.a(libpython2.7.so),
# whereas the GCC python deendency resolves to libpython2.7.so .
# This also impacts yum.

export FLAG32="-maix32 -Wl,-brtl"
export FLAG64="-maix64 -Wl,-brtl"

export  CC_FOR_CONFIGURE="$CC"
export CXX_FOR_CONFIGURE="$CXX"

echo "CC Version:"
$CC --version

%else

export CC="$XLCCPATH/xlc_r"
export CXX="$XLCXXPATH/xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"

export  CC_FOR_CONFIGURE=" $CC  -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -q64 -qbitfields=signed -qmaxmem=70000 -qalloca -bmaxdata:0x80000000 -Wl,-brtl"
export CXX_FOR_CONFIGURE=" $CXX -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -q64 -qbitfields=signed -qmaxmem=70000          -bmaxdata:0x80000000 -Wl,-brtl"

echo "CC Version:"
$CC -qversion

%endif


type $CC
type $CXX

export  CC32="${CC}  ${FLAG32} -D_LARGE_FILES"
export CXX32="${CXX} ${FLAG32} -D_LARGE_FILES"
export  CC64="${CC}  ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"

# build 64-bit version
export OBJECT_MODE=64
export CC=${CC64}
export CXX=${CXX64}
# export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir64} -L%{_libdir} -L/usr/lib/lib64 -L/usr/lib Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir64} -L%{_libdir} -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -Wl,-bnoipath"

PV=`python --version | awk '{print($2)}' | awk -F. '{print($1)}'`
if [ $PV -ne "2" ]
then
	echo "You have Python 3 installed. You need to change for Python 2"
	echo "Don't forget to also change python_32 and python_64"
	exit 1
fi

cd 64bit

#export LIBPATH="`pwd`:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib"
export LIBPATH="`pwd`"

./configure \
    --with-gcc="      $CC_FOR_CONFIGURE ${FLAG64}" \
    --with-cxx-main="$CXX_FOR_CONFIGURE ${FLAG64}" \
    --srcdir="`pwd`" \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --enable-shared \
    --enable-ipv6 \
    --with-threads=yes \
    --with-system-ffi \
    --with-system-expat \
%if %{with gcc_compiler}
  --enable-unicode=%{unicode} \
  --with-dbmliborder=gdbm:ndbm:bdb
%else
    --without-pymalloc
%endif


/usr/sbin/slibclean



%if %{without gcc_compiler}
# Due to ANSI-aliasing issue, build longobject.c without optimization
rm -f Objects/longobject.o lib%{name}%*
gmake OPT="$OPT -qalias=noansi" Objects/longobject.o
gmake %{?_smp_mflags} lib%{name}%{BASE_VERSION}.a
%else
gmake %{?_smp_mflags} lib%{name}%{BASE_VERSION}.a
%endif


$XLCCPATH/CreateExportList -X64 lib%{name}.exp lib%{name}%{BASE_VERSION}.a

%if %{with gcc_compiler}
# GCC
${CC} -shared    lib%{name}%{BASE_VERSION}.a -o lib%{name}%{BASE_VERSION}.so -Wl,-bE:lib%{name}.exp -lm -lpthreads -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%else
# xlc
${CC} -qmkshrobj lib%{name}%{BASE_VERSION}.a -o lib%{name}%{BASE_VERSION}.so -bE:lib%{name}.exp -lm -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
%endif

rm    -f lib%{name}.exp
mv    -f lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.a.old

${AR} -r lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.so

/usr/sbin/slibclean

gmake %{?_smp_mflags}

cd ..


# build 32-bit version
export CC=${CC32}
export CXX=${CXX32}
export OBJECT_MODE=32
export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir} -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bnoipath"
# export LDFLAGS="-L. -L/usr/lib/threads -L%{_libdir} -L/usr/lib"

cd 32bit

#export LIBPATH="`pwd`:/usr/lib/threads:%{_libdir}:/usr/lib"
export LIBPATH="`pwd`"

./configure \
    --with-gcc="      $CC_FOR_CONFIGURE ${FLAG32}" \
    --with-cxx-main="$CXX_FOR_CONFIGURE ${FLAG32}" \
    --srcdir="`pwd`" \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --enable-shared \
    --enable-ipv6 \
    --with-threads \
    --with-system-ffi \
    --with-system-expat \
%if %{with gcc_compiler}
  --enable-unicode=%{unicode} \
  --with-dbmliborder=gdbm:ndbm:bdb
%else
    --without-pymalloc
%endif

/usr/sbin/slibclean



%if %{without gcc_compiler}
# Due to ANSI-aliasing issue, build longobject.c without optimization
rm -f Objects/longobject.o lib%{name}%*
gmake OPT="$OPT -qalias=noansi" Objects/longobject.o
gmake %{?_smp_mflags} lib%{name}%{BASE_VERSION}.a
%else
gmake %{?_smp_mflags} lib%{name}%{BASE_VERSION}.a
%endif

$XLCCPATH/CreateExportList -X32 lib%{name}.exp lib%{name}%{BASE_VERSION}.a

%if %{with gcc_compiler}
# GCC
${CC} -shared    lib%{name}%{BASE_VERSION}.a -o lib%{name}%{BASE_VERSION}.so -Wl,-bE:lib%{name}.exp -lm -lpthreads -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib
%else
# xlc
${CC} -qmkshrobj lib%{name}%{BASE_VERSION}.a -o lib%{name}%{BASE_VERSION}.so -bE:lib%{name}.exp -lm -blibpath:/opt/freeware/lib:/usr/lib:/lib
%endif

rm    -f lib%{name}.exp

mv    -f lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.a.old

${AR} -r lib%{name}%{BASE_VERSION}.a lib%{name}%{BASE_VERSION}.so ../64bit/lib%{name}%{BASE_VERSION}.so

/usr/sbin/slibclean

gmake %{?_smp_mflags}

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

install_python() {
	set -x
	cd ${OBJECT_MODE}bit

	gmake DESTDIR=${RPM_BUILD_ROOT} install

	cp ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig-ppc${OBJECT_MODE}.h

	(
		cd ${RPM_BUILD_ROOT}%{_bindir}

		# Add the architecture suffix for binaries' name
		for f in pydoc idle 2to3 python%{BASE_VERSION} python%{BASE_VERSION}-config; do
			mv ${f} ${f}_${OBJECT_MODE};
		done
		mv smtpd.py smtpd_${OBJECT_MODE}.py

		# Create links between base and major version
		ln -sf python%{BASE_VERSION}_${OBJECT_MODE} python%{MAJOR_VERSION}_${OBJECT_MODE}
		ln -sf python%{BASE_VERSION}-config_${OBJECT_MODE} python%{MAJOR_VERSION}-config_${OBJECT_MODE}

		# Change python name in scripts
		for f in 2to3 idle pydoc python%{BASE_VERSION}-config  ; do
			cat ${f}_${OBJECT_MODE} | sed "s|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}_${OBJECT_MODE}|" > tmpfile.tmp
			mv -f tmpfile.tmp ${f}_${OBJECT_MODE}
			chmod +x ${f}_${OBJECT_MODE}
		done

		# Same for smtpd.py
		cat smtpd_${OBJECT_MODE}.py  | sed "s|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}|\/opt\/freeware\/bin\/%{name}%{BASE_VERSION}_${OBJECT_MODE}|" > tmpfile.tmp
		mv -f tmpfile.tmp smtpd_${OBJECT_MODE}.py
		chmod +x smtpd_${OBJECT_MODE}.py

		rm -f tmpfile.tmp
		cd ..


	)
	cd ..
}

# install 64-bit version

export OBJECT_MODE=64
LIBPATH="`pwd`:%{_libdir64}:%{_libdir}:/usr/lib:/lib" \
LDFLAGS="$LDFLAGS -blibpath:$LIBPATH -bnoipath" \
install_python

(
	# Generate application usable Python .exp without "_Py" internal symbols
	cd ${RPM_BUILD_ROOT}%{_libdir64}/%{name}%{BASE_VERSION}/config
	cat python.exp | sed -e '/^_Py/d' > App_python.exp
)

# install 32-bit version

export OBJECT_MODE=32
LIBPATH="`pwd`:%{_libdir}:/usr/lib:/lib" \
LDFLAGS="$LDFLAGS -blibpath:$LIBPATH -bnoipath" \
install_python

# python header
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/%{name}%{BASE_VERSION}/pyconfig.h
cp %{_builddir}/Python-%{version}/32bit/lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}%{BASE_VERSION}.a
ln -sf ../lib/lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}%{BASE_VERSION}.a

#/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Move pydoc to pydoc2
mv ${RPM_BUILD_ROOT}%{_bindir}/pydoc_32 ${RPM_BUILD_ROOT}%{_bindir}/pydoc%{MAJOR_VERSION}_32
mv ${RPM_BUILD_ROOT}%{_bindir}/pydoc_64 ${RPM_BUILD_ROOT}%{_bindir}/pydoc%{MAJOR_VERSION}_64

# Move idle to idle2
mv ${RPM_BUILD_ROOT}%{_bindir}/idle_32 ${RPM_BUILD_ROOT}%{_bindir}/idle%{MAJOR_VERSION}_32
mv ${RPM_BUILD_ROOT}%{_bindir}/idle_64 ${RPM_BUILD_ROOT}%{_bindir}/idle%{MAJOR_VERSION}_64

# Add symlinks for commands without _32/_64 suffix
DEFAULT_BITS=64
if [ "%{default_bits}" == "32" ]; then
    DEFAULT_BITS=32
fi
(
	cd ${RPM_BUILD_ROOT}%{_bindir}

	for f in `ls *_${DEFAULT_BITS}`; do
		ln -sf ${f} `echo ${f} | sed -e "s/_${DEFAULT_BITS}$//"`
	done

	ln -sf smtpd_${DEFAULT_BITS}.py smtpd.py
)

# For compatibility purpose, still add /usr/bin/python
# TODO: remove
(
	mkdir -p ${RPM_BUILD_ROOT}/usr/bin
	cd ${RPM_BUILD_ROOT}/usr/bin
	ln -sf ../..%{_prefix}/bin/python .
)

(
	cd ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/config

	# Generate application usable Python .exp without "_Py" internal symbols
	cat python.exp | sed -e '/^_Py/d' > App_python.exp

)

# dynfiles
find ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" > dynfiles
find ${RPM_BUILD_ROOT}%{_libdir64}/%{name}%{BASE_VERSION}/lib-dynload -type d | sed "s|${RPM_BUILD_ROOT}|%dir |" >> dynfiles
find ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload -type f | \
  grep -v "_tkinter.so" | \
  grep -v "_ctypes_test.so" | \
  grep -v "_testcapi.so" | \
  sed "s|${RPM_BUILD_ROOT}||" >> dynfiles
find ${RPM_BUILD_ROOT}%{_libdir64}/%{name}%{BASE_VERSION}/lib-dynload -type f | \
  grep -v "_tkinter.so" | \
  grep -v "_ctypes_test.so" | \
  grep -v "_testcapi.so" | \
  sed "s|${RPM_BUILD_ROOT}||" >> dynfiles

# symlink
ln -sf ../../lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir}/%{name}%{BASE_VERSION}/config/lib%{name}%{BASE_VERSION}.a
ln -sf ../../lib%{name}%{BASE_VERSION}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}%{BASE_VERSION}/config/lib%{name}%{BASE_VERSION}.a

#################################
#  Check
#################################
%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# Required for tests to not fail due to:
#	error: can't start new thread
#	Memory fault
ulimit -d unlimited
ulimit -m unlimited
# ulimit -f unlimited # Not OK on user
# ulimit -s unlimited
ulimit -a

test_python() {
    export PYTHONPATH=`pwd`/Modules
	export LIBPATH="`pwd`"
    # Some tests hang when running the whole test_suite, so we need to ignore them first and run them separately later
    ( ./python Lib/test/regrtest.py -x test_signal -x test_subprocess -x test_threading || true )
	( ./python Lib/test/regrtest.py  test_signal test_subprocess test_threading || true )
    #( LDFLAGS="$LDFLAGS -blibpath:/usr/lib/threads:%{_libdir}:/usr/lib" gmake -k test || true )
    #( LDFLAGS="$LDFLAGS -blibpath:/usr/lib/threads:%{_libdir64}:%{_libdir}:/usr/lib64:/usr/lib" gmake -k testall || true )
    # ( gmake -k testall || true )
    /usr/sbin/slibclean
}

cd 64bit
test_python 64
cd ..

cd 32bit
test_python 32
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
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

cd %{_bindir}
ln -sf python2    python
ln -sf python2_32 python_32
ln -sf python2_64 python_64
ln -sf pydoc2     pydoc
ln -sf pydoc2_32  pydoc_32
ln -sf pydoc2_64  pydoc_64

# Python3 is default. Don't change links.
%postun
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

# Python 3 exists. Choose by default.
if [[ -e %{_bindir}/python3 ]]; then
	cd %{_bindir}
	ln -sf python3    python
	ln -sf python3_32 python_32
	ln -sf python3_64 python_64
	ln -sf pydoc3     pydoc
	ln -sf pydoc3_32  pydoc_32
	ln -sf pydoc3_64  pydoc_64
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
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

cd %{_bindir}
ln -sf python2-config    python-config
ln -sf python2-config_32 python-config_32
ln -sf python2-config_64 python-config_64

%postun devel
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

if test -e %{_bindir}/python3-config; then
	cd %{_bindir}
	ln -sf python3-config    python-config
	ln -sf python3-config_32 python-config_32
	ln -sf python3-config_64 python-config_64
else
	unlink %{_bindir}/python-config
	unlink %{_bindir}/python-config_32
	unlink %{_bindir}/python-config_64
fi

%post tools
# Python3 is default. Don't change links.
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

cd %{_bindir}
ln -sf idle2    idle
ln -sf idle2_32 idle_32
ln -sf idle2_64 idle_64

%postun tools
if %{_bindir}/python --version 2>&1 | grep -q "Python 3"; then
	exit 0
fi

if test -e %{_bindir}/idle3; then
	cd %{_bindir}
	ln -sf idle3    idle
	ln -sf idle3_32 idle_32
	ln -sf idle3_64 idle_64
else
	unlink %{_bindir}/idle
	unlink %{_bindir}/idle_32
	unlink %{_bindir}/idle_64
fi


#################################
#  File
 #################################
%files -f dynfiles
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/README
%{_bindir}/python%{MAJOR_VERSION}
%{_bindir}/python%{MAJOR_VERSION}_32
%{_bindir}/python%{MAJOR_VERSION}_64
%{_bindir}/python%{BASE_VERSION}
%{_bindir}/python%{BASE_VERSION}_32
%{_bindir}/python%{BASE_VERSION}_64
%{_bindir}/pydoc%{MAJOR_VERSION}
%{_bindir}/pydoc%{MAJOR_VERSION}_32
%{_bindir}/pydoc%{MAJOR_VERSION}_64
%{_mandir}/*/*
# /usr links
# /usr/bin/python%{MAJOR_VERSION}
# /usr/bin/python%{MAJOR_VERSION}_32
# /usr/bin/python%{MAJOR_VERSION}_64
# /usr/bin/python%{BASE_VERSION}
# /usr/bin/python%{BASE_VERSION}_32
# /usr/bin/python%{BASE_VERSION}_64
# /usr/bin/pydoc%{MAJOR_VERSION}
# /usr/bin/pydoc%{MAJOR_VERSION}_32
# /usr/bin/pydoc%{MAJOR_VERSION}_64

%dir %{_libdir}/%{name}%{BASE_VERSION}
%dir %{_libdir}/%{name}%{BASE_VERSION}/bsddb
%dir %{_libdir}/%{name}%{BASE_VERSION}/ctypes
%dir %{_libdir}/%{name}%{BASE_VERSION}/distutils
%dir %{_libdir}/%{name}%{BASE_VERSION}/email
%dir %{_libdir}/%{name}%{BASE_VERSION}/json
%dir %{_libdir}/%{name}%{BASE_VERSION}/lib2to3
%dir %{_libdir}/%{name}%{BASE_VERSION}/site-packages
%dir %{_libdir}/%{name}%{BASE_VERSION}/sqlite3
%dir %{_libdir}/%{name}%{BASE_VERSION}/unittest
%dir %{_libdir}/%{name}%{BASE_VERSION}/xml
%{_libdir}/%{name}%{BASE_VERSION}/*.doc
%{_libdir}/%{name}%{BASE_VERSION}/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/LICENSE.txt
%{_libdir}/%{name}%{BASE_VERSION}/bsddb/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/compiler
%{_libdir}/%{name}%{BASE_VERSION}/config
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/macholib
%{_libdir}/%{name}%{BASE_VERSION}/curses
%{_libdir}/%{name}%{BASE_VERSION}/distutils/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/distutils/README
%{_libdir}/%{name}%{BASE_VERSION}/distutils/command
%{_libdir}/%{name}%{BASE_VERSION}/email/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/email/mime
%{_libdir}/%{name}%{BASE_VERSION}/encodings
%{_libdir}/%{name}%{BASE_VERSION}/hotshot
%{_libdir}/%{name}%{BASE_VERSION}/idlelib
%{_libdir}/%{name}%{BASE_VERSION}/importlib
%{_libdir}/%{name}%{BASE_VERSION}/json/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/Grammar*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/Pattern*
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/fixes
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/pgen2
%{_libdir}/%{name}%{BASE_VERSION}/logging
%{_libdir}/%{name}%{BASE_VERSION}/multiprocessing
%{_libdir}/%{name}%{BASE_VERSION}/plat-%{osplat}
%{_libdir}/%{name}%{BASE_VERSION}/pydoc_data
%{_libdir}/%{name}%{BASE_VERSION}/site-packages/README
%{_libdir}/%{name}%{BASE_VERSION}/sqlite3/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/unittest/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/wsgiref*
%{_libdir}/%{name}%{BASE_VERSION}/xml/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/xml/dom
%{_libdir}/%{name}%{BASE_VERSION}/xml/etree
%{_libdir}/%{name}%{BASE_VERSION}/xml/parsers
%{_libdir}/%{name}%{BASE_VERSION}/xml/sax
%{_libdir}/lib%{name}%{BASE_VERSION}.a
%{_libdir}/lib%{name}%{BASE_VERSION}.so
# /usr/lib/lib%{name}%{BASE_VERSION}.a
# /usr/lib/lib%{name}%{BASE_VERSION}.so

%dir %{_libdir64}/%{name}%{BASE_VERSION}
%dir %{_libdir64}/%{name}%{BASE_VERSION}/bsddb
%dir %{_libdir64}/%{name}%{BASE_VERSION}/ctypes
%dir %{_libdir64}/%{name}%{BASE_VERSION}/distutils
%dir %{_libdir64}/%{name}%{BASE_VERSION}/email
%dir %{_libdir64}/%{name}%{BASE_VERSION}/json
%dir %{_libdir64}/%{name}%{BASE_VERSION}/lib2to3
%dir %{_libdir64}/%{name}%{BASE_VERSION}/site-packages
%dir %{_libdir64}/%{name}%{BASE_VERSION}/sqlite3
%dir %{_libdir64}/%{name}%{BASE_VERSION}/unittest
%dir %{_libdir64}/%{name}%{BASE_VERSION}/xml
%{_libdir64}/%{name}%{BASE_VERSION}/*.doc
%{_libdir64}/%{name}%{BASE_VERSION}/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/LICENSE.txt
%{_libdir64}/%{name}%{BASE_VERSION}/bsddb/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/compiler
%{_libdir64}/%{name}%{BASE_VERSION}/config
%{_libdir64}/%{name}%{BASE_VERSION}/ctypes/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/ctypes/macholib
%{_libdir64}/%{name}%{BASE_VERSION}/curses
%{_libdir64}/%{name}%{BASE_VERSION}/distutils/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/distutils/README
%{_libdir64}/%{name}%{BASE_VERSION}/distutils/command
%{_libdir64}/%{name}%{BASE_VERSION}/email/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/email/mime
%{_libdir64}/%{name}%{BASE_VERSION}/encodings
%{_libdir64}/%{name}%{BASE_VERSION}/hotshot
%{_libdir64}/%{name}%{BASE_VERSION}/idlelib
%{_libdir64}/%{name}%{BASE_VERSION}/importlib
%{_libdir64}/%{name}%{BASE_VERSION}/json/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/Grammar*
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/Pattern*
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/fixes
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/pgen2
%{_libdir64}/%{name}%{BASE_VERSION}/logging
%{_libdir64}/%{name}%{BASE_VERSION}/multiprocessing
%{_libdir64}/%{name}%{BASE_VERSION}/plat-%{osplat}
%{_libdir64}/%{name}%{BASE_VERSION}/pydoc_data
%{_libdir64}/%{name}%{BASE_VERSION}/site-packages/README
%{_libdir64}/%{name}%{BASE_VERSION}/sqlite3/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/unittest/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/wsgiref*
%{_libdir64}/%{name}%{BASE_VERSION}/xml/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/xml/dom
%{_libdir64}/%{name}%{BASE_VERSION}/xml/etree
%{_libdir64}/%{name}%{BASE_VERSION}/xml/parsers
%{_libdir64}/%{name}%{BASE_VERSION}/xml/sax
%{_libdir64}/lib%{name}%{BASE_VERSION}.a
%{_libdir64}/lib%{name}%{BASE_VERSION}.so
# /usr/lib64/lib%{name}%{BASE_VERSION}.a
# /usr/lib64/lib%{name}%{BASE_VERSION}.so

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%{_libdir}/%{name}%{BASE_VERSION}/config
%{_libdir64}/%{name}%{BASE_VERSION}/config
%dir %{_includedir}/python%{BASE_VERSION}/
%{_includedir}/python%{BASE_VERSION}/pyconfig.h
%{_includedir}/python%{BASE_VERSION}/pyconfig-ppc32.h
%{_includedir}/python%{BASE_VERSION}/pyconfig-ppc64.h

# For compatibility purpose
/usr/bin/python

%files devel
%defattr(-,root,system,-)
%doc 32bit/Misc/README.valgrind 32bit/Misc/valgrind-python.supp
%doc 32bit/Misc/gdbinit
%{_bindir}/python%{MAJOR_VERSION}-config
%{_bindir}/python%{MAJOR_VERSION}-config_32
%{_bindir}/python%{MAJOR_VERSION}-config_64
%{_bindir}/python%{BASE_VERSION}-config
%{_bindir}/python%{BASE_VERSION}-config_32
%{_bindir}/python%{BASE_VERSION}-config_64
%exclude %{_includedir}/python%{BASE_VERSION}/pyconfig.h
%exclude %{_includedir}/python%{BASE_VERSION}/pyconfig-ppc32.h
%exclude %{_includedir}/python%{BASE_VERSION}/pyconfig-ppc64.h
%{_includedir}/python%{BASE_VERSION}/*.h

# /usr/bin/python*-config*

%files tools
%defattr(-,root,system,-)
%{_bindir}/idle%{MAJOR_VERSION}
%{_bindir}/idle%{MAJOR_VERSION}_32
%{_bindir}/idle%{MAJOR_VERSION}_64
%{_bindir}/smtpd.py
%{_bindir}/smtpd_32.py
%{_bindir}/smtpd_64.py
# /usr/bin/idle*
# /usr/bin/smtpd*.py*

%files tkinter
%defattr(-,root,system,-)

%dir %{_libdir}/%{name}%{BASE_VERSION}/lib-tk
%{_libdir}/%{name}%{BASE_VERSION}/lib-tk/*.py*
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_tkinter.so

%dir %{_libdir64}/%{name}%{BASE_VERSION}/lib-tk
%{_libdir64}/%{name}%{BASE_VERSION}/lib-tk/*.py*
%{_libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_tkinter.so

%files test
%defattr(-,root,system,-)

%{_libdir}/%{name}%{BASE_VERSION}/bsddb/test
%{_libdir}/%{name}%{BASE_VERSION}/ctypes/test
%{_libdir}/%{name}%{BASE_VERSION}/distutils/tests
%{_libdir}/%{name}%{BASE_VERSION}/email/test
%{_libdir}/%{name}%{BASE_VERSION}/json/tests
%{_libdir}/%{name}%{BASE_VERSION}/lib-tk/test
%{_libdir}/%{name}%{BASE_VERSION}/lib2to3/tests
%{_libdir}/%{name}%{BASE_VERSION}/sqlite3/test
%{_libdir}/%{name}%{BASE_VERSION}/test
%{_libdir}/%{name}%{BASE_VERSION}/unittest/test
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_ctypes_test.so
%{_libdir}/%{name}%{BASE_VERSION}/lib-dynload/_testcapi.so

%{_libdir64}/%{name}%{BASE_VERSION}/bsddb/test
%{_libdir64}/%{name}%{BASE_VERSION}/ctypes/test
%{_libdir64}/%{name}%{BASE_VERSION}/distutils/tests
%{_libdir64}/%{name}%{BASE_VERSION}/email/test
%{_libdir64}/%{name}%{BASE_VERSION}/json/tests
%{_libdir64}/%{name}%{BASE_VERSION}/lib-tk/test
%{_libdir64}/%{name}%{BASE_VERSION}/lib2to3/tests
%{_libdir64}/%{name}%{BASE_VERSION}/sqlite3/test
%{_libdir64}/%{name}%{BASE_VERSION}/test
%{_libdir64}/%{name}%{BASE_VERSION}/unittest/test
%{_libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_ctypes_test.so
%{_libdir64}/%{name}%{BASE_VERSION}/lib-dynload/_testcapi.so

%files docs
%defattr(-,root,system,-)
%doc python-%{version}-docs-text

#################################
#  Changelog
#################################
%changelog
* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.7.17-2
- Bullfreeware OpenSSL removal

* Fri Jan 10 2020 Clément Chigot <clement.chigot@atos.net> - 2.7.17-1
- Remove OpenSources SSL dependency

* Mon Dec 02 2019 Clément Chigot <clement.chigot@atos.net> - 2.7.16-6
- Improve libpath of libpython.a(libpython2.7.so)
- Fix man files
- Add /usr/bin/python for compatibility purpose

* Wed Nov 13 2019 Clément Chigot <clement.chigot@atos.net> - 2.7.16-5
- Rebuild to avoid dependency over libintl.so

* Fri Nov 8 2019 Clément Chigot <clement.chigot@atos.net> - 2.7.16-4
- Update openssl dependency to 1.0.2s

* Tue Oct 1 2019 Clément Chigot <clement.chigot@atos.net> - 2.7.16-3
- Fix missing .h files in python-devel

* Tue Sep 17 2019 Clément Chigot <clement.chigot@atos.net> - 2.7.16-2
- Move tests to %check section
- Remove /usr links
- No large file support needed for 64bit build
- Clean dependencies
- Fix python2 and python3 conflict files:
    idle and pydoc are now idle2 and pydoc2
    Links are now created during %post
	Add _32 files in order to match python3
- "2to3" removed from python-tools, now only in python3-tools

* Tue Mar 12 2019 Ayappan P <ayappap2@in.ibm.com> - 2.7.16-1
- Update to 2.7.16 (for CVE-2019-5010 fix)

* Wed Sep 19 2018 Michael Wilson <michael.a.wilson@atos.net> - 2.7.15-5
- Rebuild with expat 2.2.6 - symbol XML_SetHashSalt missing in libexpat 2.0

* Thu Sep 06 2018 Michael Wilson <michael.a.wilson@atos.net> - 2.7.15-4
- Revert to UCS2 when building with gcc for python.exp compatibility

* Tue Aug 28 2018 Michael Wilson <michael.a.wilson@atos.net> - 2.7.15-3
- Use "-brtl" flag when building with gcc for ".so" / ".a" compatibility.

* Thu Aug 02 2018 Michael Wilson <michael.a.wilson@atos.net> - 2.7.15-2
- Recover missing changes and history from version 2.7.12-*
- Generate application usable Python .exp filtering "_Py" internal symbols

* Thu May 17 2018 Sena Apeke <sena.apeke.external@atos.net> 2.7.15-1
- Update to version 2.7.15
- Fix issues with ncurses added with 2.7.12 .

* Thu Jun 22 2017 Tony Reix <tony.reix@atos.net> - 2.7.12-4
- Re-add the lost patch Lib.ctypes.160309

* Tue Jan 31 2017 Tony Reix <tony.reix@atos.net> - 2.7.12-3
- Rebuild it due to /opt/freeware --> /home2/freeware : mess

* Thu Aug 18 2016 Tony Reix <tony.reix@atos.net> - 2.7.12-2
- Use gcc compiler.

* Thu Aug 11 2016 Tony Reix <tony.reix@atos.net> - 2.7.11-6
- Fix issues with xlc -O2 and ANSI-aliasing
- Add gcc

* Tue Jul 26 2016 Tony Reix <tony.reix@atos.net> - 2.7.11-2
- Update to version 2.7.11

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

