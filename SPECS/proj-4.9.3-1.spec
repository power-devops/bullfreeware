%define _libdir64 %{_prefix}/lib64

Name:		proj
Version:	4.9.3
Release:	4%{?dist}
Summary:	Cartographic projection software (PROJ.4)

Group:		Applications/Engineering
License:	MIT
URL:		https://proj4.org
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:	http://download.osgeo.org/%{name}/%{name}-datumgrid-1.6.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Patch01:        proj-aix.patch

BuildRequires:	libtool

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.

library is available as 32-bit and 64-bit.

%package devel
Summary:	Development files for PROJ.4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.


%package static
Summary:	Development files for PROJ.4
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
This package contains libproj static library.

%package nad
Summary:	US and Canadian datum shift grids for PROJ.4
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description nad
This package contains additional US and Canadian datum shift grids.

%package epsg
Summary:	EPSG dataset for PROJ.4
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description epsg
This package contains additional EPSG dataset.

%prep

export PATH=/opt/freeware/bin:$PATH

%setup -q

# setup nad
cd nad
unzip %{SOURCE1}
cd ..

%patch01

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
    --mandir=%{_mandir} \
    --disable-static \
    --enable-shared

$MAKE %{?_smp_mflags} 

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
    --mandir=%{_mandir} \
    --disable-static \
    --enable-shared


$MAKE %{?_smp_mflags} 

$MAKE check || true

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install


strip ${RPM_BUILD_ROOT}%{_bindir}/* ||

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp nad/pj_out27.dist ${RPM_BUILD_ROOT}%{_datadir}/%{name} 
cp nad/pj_out83.dist ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp nad/td_out.dist ${RPM_BUILD_ROOT}%{_datadir}/%{name}

chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/%{name}/*.dist
cp nad/test27 ${RPM_BUILD_ROOT}%{_datadir}/%{name}
cp nad/test83 ${RPM_BUILD_ROOT}%{_datadir}/%{name} 
cp nad/testvarious ${RPM_BUILD_ROOT}%{_datadir}/%{name}
chmod 0755 ${RPM_BUILD_ROOT}%{_datadir}/%{name}/test*

cp src/projects.h %{buildroot}%{_includedir}/


(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)


cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

strip ${RPM_BUILD_ROOT}%{_bindir}/* ||

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
    rm ${f}
    ln -s /opt/freeware/lib/${f} ${f}

 done
)


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}*.so*

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
%defattr(-,root,system)
%doc 32bit/NEWS 32bit/AUTHORS 32bit/COPYING 32bit/README 32bit/ChangeLog
%{_bindir}/*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_mandir}/man1/*.1*
/usr/lib/*.a
/usr/lib64/*.a

%files devel
%defattr(-,root,system,-)
%{_includedir}/*.h
%{_libdir}/libproj.la
%{_libdir64}/libproj.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la

%files nad
%defattr(-,root,root,-)
%doc 32bit/nad/README
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}


%files epsg
%defattr(-,root,system,-)
%doc 32bit/nad/README
%attr(0644,root,system) %{_datadir}/%{name}/epsg

%changelog
* Mon Feb 12 2018 Pascal Oliva <pascal.oliva@atos.net> - 4.9.3-1
- updated to version 4.9.3

* Mon Apr 30 2012 Michael Perzl <michael@perzl.org> - 4.8.0-1
- updated to version 4.8.0
- updated proj-datumgrid to version 1.6RC1

* Wed Apr 13 2011 Michael Perzl <michael@perzl.org> - 4.7.0-2
- updated proj-datumgrid to version 1.5

* Thu Oct 08 2009 Michael Perzl <michael@perzl.org> - 4.7.0-1
- updated to version 4.7.0

* Thu May 15 2008 Michael Perzl <michael@perzl.org> - 4.6.0-1
- first version for AIX V5.1 and higher

