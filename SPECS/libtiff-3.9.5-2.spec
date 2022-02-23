Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 3.9.5
Release: 2
License: BSD
Group: System Environment/Libraries
URL: http://www.libtiff.org/

Source0: ftp://ftp.remotesensing.org/pub/%{name}/tiff-%{version}.tar.gz
Source1: tiffconf.h
Patch0: %{name}-%{version}-aix.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: make, libjpeg-devel, zlib-devel, jbigkit-devel
Requires: libjpeg, zlib, jbigkit-libs

%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development tools for programs which will use the libtiff library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: jbigkit-devel

%description devel
This package contains the header files and documentation necessary for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n tiff-%{version}
%patch0


%build
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export CXXFLAGS="-I/usr/vacpp/include"

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make

cp libtiff/.libs/libtiff.so.3 .
cp libtiff/.libs/libtiffxx.so.3 .
cp libtiff/tiffconf.h tiffconf-ppc64.h
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static
make

cp libtiff/tiffconf.h tiffconf-ppc32.h


%install
export AR="ar -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# Due to an inexpected rebuild of the librairy, we force to copy into the
# BUIL_ROOT directory, the library whith the objects with 32 and 64 bit.
#
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q libtiff/.libs/libtiff.a ./libtiff.so.3
${AR} -q libtiff/.libs/libtiffxx.a ./libtiffxx.so.3

# add AIX Toolbox compatibility members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
mv libtiff.so.3 shr.o
/usr/bin/strip -X64 -e shr.o
${AR} -q libtiff/.libs/libtiff.a ./shr.o
cp libtiff/.libs/libtiff.so.3 shr.o
/usr/bin/strip -X32 -e shr.o
${AR} -q libtiff/.libs/libtiff.a ./shr.o
cp libtiff/.libs/libtiff.a libtiff/.libs/libtiffxx.a  ${RPM_BUILD_ROOT}%{_libdir}

cp tiffconf-ppc??.h $RPM_BUILD_ROOT%{_includedir}/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/
chmod 644 $RPM_BUILD_ROOT%{_includedir}/*.h

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
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
%doc COPYRIGHT README RELEASE-DATE VERSION
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man1/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc TODO ChangeLog html
%{_includedir}/*
%{_libdir}/*.la
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Mon Sep 12 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 3.9.5-1
- Initial port on Aix5.3 
