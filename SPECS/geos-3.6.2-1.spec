%define _libdir64 %{_prefix}/lib64

Name:		geos
Version:	3.6.2
Release:	1
Summary:	GEOS is a C++ port of the Java Topology Suite

Group:		Applications/Engineering
License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

Patch01:        %{name}-%{version}-aix.patch

BuildRequires:	doxygen autoconf

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Development files for GEOS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}


%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology 
Suite (JTS). As such, it aims to contain the complete functionality of 
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial 
predicate functions and spatial operators, as well as specific JTS topology 
functions such as IsValid()

This package contains the development files to build applications that 
use GEOS.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep

export PATH=/opt/freeware/bin:$PATH

%setup -q


# Duplicate source for 32 & 64 bits

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
# This line (use for tracing) sometimes generates the issue: "--trace:  not found" during tests
export MAKE="gmake "

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


cd 64bit

# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

export GLOBAL_CC_OPTIONS="-O2"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"
export CC="${CC64}  $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

echo $CXX

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --with-aix-soname=aix \
    --disable-static \
    --disable-dependency-tracking \
    --enable-shared



#/usr/bin/cp include/geos/platform.h ~/platform.h.SAV
#/usr/bin/cp ~/platform.h include/geos/platform.h

#%patch01
/opt/freeware/bin/patch -p1 < $SOURCES/%{name}-%{version}-aix.patch


$MAKE %{?_smp_mflags} -j 10  

$MAKE check || true 


cd ..

cd 32bit
# now build the 32-bit version


export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"

export GLOBAL_CC_OPTIONS="-O2"
export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC="${CC32}  $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --with-aix-soname=aix \
    --disable-static \
    --disable-dependency-tracking \
    --enable-shared


$MAKE %{?_smp_mflags} -j 10

$MAKE check || true

# make doxygen documentation files
cd doc
make doxygen-html


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
    rm ${f}
    ln -s /opt/freeware/lib/${f} ${f}

  done

#  cd ${RPM_BUILD_ROOT}%{_libdir}
#  for f in *.a ; do
#    /usr/bin/ar -X32 -x ${f}
#  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-*.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-*.so*
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}_c.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}_c.so*

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
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS 32bit/README 32bit/TODO
%{_libdir}/*.a
#%{_libdir}/*.so*
%{_libdir64}/*.a
#%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib64/*.a
#/usr/lib/*.so*
#/usr/lib64/*.so*

%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/doxygen_docs
%{_bindir}/geos-config*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_includedir}/*
/usr/bin/geos-config*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Wed Feb  7 2018 Pascal Oliva <pascal.oliva@atos.net> - 3.6.2-1
- updated to version 3.6.2

* Sat Jan 04 2014 Michael Perzl <michael@perzl.org> - 3.4.2-1
- updated to version 3.4.2

* Sat Jan 04 2014 Michael Perzl <michael@perzl.org> - 3.3.9-1
- updated to version 3.3.9

* Mon Mar 04 2013 Michael Perzl <michael@perzl.org> - 3.3.8-1
- updated to version 3.3.8

* Tue Jan 29 2013 Michael Perzl <michael@perzl.org> - 3.3.7-1
- updated to version 3.3.7

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 3.3.6-1
- updated to version 3.3.6

* Tue Jul 10 2012 Michael Perzl <michael@perzl.org> - 3.3.5-1
- updated to version 3.3.5

* Mon Jul 09 2012 Michael Perzl <michael@perzl.org> - 3.2.3-1
- first version for AIX V5.1 and higher

