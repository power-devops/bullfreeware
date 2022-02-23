
%define _libdir64 %{_prefix}/lib64
%define cmake      /usr/bin/cmake
%define pkg_name   mariadb
# No tests for this package.
%bcond_without dotests
%bcond_with    debug

Patch1:     mariadb-connector-odbc-3.1.2-export.patch
Patch2:     mariadb-connector-odbc-3.1.2-strstr.patch

Name:       mariadb-connector-odbc
%define     so_mariadb 3
Version:    %{so_mariadb}.1.2
Release:    1
Summary:    The MariaDB Native Client library (ODBC driver)
Group:      Servers
License:    LGPLv2+
Source:     https://downloads.mariadb.org/f/connector-odbc-%{version}/%{name}-%{version}-ga-src.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log
Url:        http://mariadb.org/

BuildRequires: cmake >= 3.14
BuildRequires: cmake <  3.15
BuildRequires: unixODBC-devel gcc-c++
BuildRequires: mariadb-connector-c-devel >= 3.1.2

Requires:      unixODBC
Requires:      mariadb-connector-c >= 3.1.2

%description
MariaDB Connector/ODBC is a standardized, LGPL licensed database driver using
the industry standard Open Database Connectivity (ODBC) API. It supports ODBC
Standard 3.5, can be used as a drop-in replacement for MySQL Connector/ODBC,
and it supports both Unicode and ANSI modes.


%prep
%setup -q -n %{name}-%{version}-ga-src

%patch1 -p1 -b .export 
%patch2 -p1 -b .strstr

# Remove unsused parts
rm -r wininstall osxinstall

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
env | sort

export PATH=/opt/freeware/bin:/usr/bin

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"

export FLAG32="-maix32"
export FLAG64="-maix64"

COMMON_C_FLAGS="-D_GNU_SOURCE -D_LARGEFILE_SOURCE -pthread -mcmodel=large -I/opt/freeware/include/mysql"
%if %{with debug}
COMMON_C_FLAGS="$COMMON_C_FLAGS -O0"
%endif

echo "GCC Version:"
$CC --version

# Force cmake to user AIX ar command
export AR=/usr/bin/ar
export NM=/usr/bin/nm

export MAKE="gmake --trace -j8"

run_compile()
{
%cmake . -L \
         -DCMAKE_BUILD_TYPE=%{?with_debug:DEBUG}%{!?with_debug:RELEASE} \
         -DMARIADB_LINK_DYNAMIC="%{_lib}$OBJECT_MODE_LIB/libmariadb.a" \
         -DBUILD_SHARED_LIBS="ON" \
         -DCMAKE_POLICY_DEFAULT_CMP0065=NEW \
         -DCMAKE_INSTALL_RPATH=$PATH_MODE \
         -DCMAKE_BUILD_RPATH=$PATH_MODE \
         -DLOG_LOCATION="%{logfile}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_LIBDIR="%{_lib}$OBJECT_MODE_LIB" \
         -DENABLED_LOCAL_INFILE=ON \
         -DSECURITY_HARDENED=ON \
         -DICONV_LIBRARIES=/opt/freeware/lib/libiconv.a
$MAKE
}


############################### 64-bit BEGIN ##############################
# first build the 64-bit version

cd 64bit
export OBJECT_MODE=64
export OBJECT_MODE_LIB=64
export PATH_MODE="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib"

export CFLAGS="${COMMON_C_FLAGS} ${FLAG64} -D_FILE_OFFSET_BITS=64"
export LDFLAGS="-pthread"
export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

export CXXFLAGS="$CFLAGS"

run_compile

############################### 32-bit BEGIN ##############################

cd ../32bit

export OBJECT_MODE=32
export OBJECT_MODE_LIB=""
export PATH_MODE="/opt/freeware/lib/pthread:/opt/freeware/lib"

export CFLAGS="${COMMON_C_FLAGS} ${CFLAG32}"
export LDFLAGS="-pthread -Wl,-bmaxdata:0x80000000"
export LIBPATH="/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"

export CXXFLAGS="$CFLAGS"

run_compile

########################### END 32-bit #####################################


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%check
%if %{with dotests}
# No tests!
%endif


%install

export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export MAKE="gmake --trace -j8"
export AR="/usr/bin/ar"

echo ${RPM_BUILD_ROOT}

cd 32bit
export OBJECT_MODE=32
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

cd ../64bit
export OBJECT_MODE=64
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

cd ${RPM_BUILD_ROOT}%{_libdir}
# TODO: clean when CMake 3.16 will be released
$AR -x -X32 libmaodbc.a
mv libmaodbc.so          libmaodbc.so.%{so_mariadb}
rm libmaodbc.a
$AR -qc -X32 libmaodbc.a libmaodbc.so.%{so_mariadb}
/usr/bin/strip -e -X32   libmaodbc.so.%{so_mariadb}

cd ../lib64
$AR -x -X64 libmaodbc.a
mv libmaodbc.so                 libmaodbc.so.%{so_mariadb}
$AR -qc -X64 ../lib/libmaodbc.a libmaodbc.so.%{so_mariadb}
/usr/bin/strip -e -X64          libmaodbc.so.%{so_mariadb}

rm libmaodbc.a
ln -s ../lib/libmaodbc.a libmaodbc.a


%files
%{_libdir64}/*
%{_libdir}/*

%doc 32bit/README 32bit/COPYING

%changelog
* Wed Jul 31 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.2-1
- First port on AIX
