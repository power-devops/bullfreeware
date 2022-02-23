%{!?dotests:%define DO_TESTS 0}
%{?dotests:%define DO_TESTS 1}

Summary: Library of functions for manipulating TIFF format image files
Name: libtiff
Version: 4.0.6
Release: 1
License: BSD
Group: System Environment/Libraries
URL: http://www.libtiff.org/

Source0: ftp://ftp.remotesensing.org/pub/%{name}/tiff-%{version}.tar.gz
Source1: tiffconf.h
Source2: %{name}.so.3-aix32
Source3: %{name}.so.3-aix64
Source4: %{name}xx.so.3-aix32
Source5: %{name}xx.so.3-aix64
Patch0: tiff-%{version}-aix.patch

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
echo "DO_TESTS=%{DO_TESTS}"
%setup -q -n tiff-%{version}
%patch0 -p1 -b .aix

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/usr/vac/bin/xlc_r"
export CC64="$CC32 -q64"
export CXX32="/usr/vacpp/bin/xlC_r"
export CXX64="$CXX32 -q64"
export CXXFLAGS="-I/usr/vacpp/include"
export LDFLAGS=""

# first build the 64-bit version
cd 64bit
export CC=$CC64
export CXX=$CXX64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

cp libtiff/tiffconf.h ../tiffconf-ppc64.h
cd ..

# now build the 32-bit version
cd 32bit
export CC=$CC32
export CXX=$CXX32
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

cp libtiff/tiffconf.h ../tiffconf-ppc32.h
cd ..

%define LINKS bin/*tiff bin/tiff* bin/fax2ps bin/pal2rgb bin/rgb2ycbcr bin/thumbnail lib/libtiff*.a
%define LINKS_DEVEL include/tiff*.h lib/libtiff*.la

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# Extract the 64 bit object from the lib
/usr/bin/ar -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.5
/usr/bin/ar -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/%{name}xx.a %{name}xx.so.5

# Rename executables
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects

/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.5
# add AIX Toolbox compatibility members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
mv %{name}.so.5 shr.o
/usr/bin/strip -X64 -e shr.o
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr.o

/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}xx.a %{name}xx.so.5
# add AIX Toolbox compatibility members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
mv %{name}xx.so.5 shr.o
/usr/bin/strip -X64 -e shr.o
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}xx.a shr.o

# Add the older version 3 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
for SOURCE in %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5}; do
    BITS=`echo $SOURCE | sed -e "s/.*-aix\([0-9]*\)\$/\1/"`
    SO_NAME=`basename $SOURCE | sed -e "s/-aix\([0-9]*\)\$//"`
    ARCHIVE_NAME=`echo $SO_NAME | sed -e "s/so.[0-9]*\$/a/"`
    cp ${SOURCE} ${SO_NAME}
    /usr/bin/strip -X${BITS} -e ${SO_NAME}
    /usr/bin/ar -X${BITS} -q ${RPM_BUILD_ROOT}%{_libdir}/${ARCHIVE_NAME}.a ${SO_NAME}
done

# add AIX Toolbox compatibility members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
/usr/bin/ar -X32 xv ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.5
mv %{name}.so.5 shr.o
/usr/bin/strip -X32 -e shr.o
/usr/bin/ar -q -X32 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr.o

/usr/bin/ar -X32 xv ${RPM_BUILD_ROOT}%{_libdir}/%{name}xx.a %{name}xx.so.5
mv %{name}xx.so.5 shr.o
/usr/bin/strip -X32 -e shr.o
/usr/bin/ar -q -X32 ${RPM_BUILD_ROOT}%{_libdir}/%{name}xx.a shr.o

cp tiffconf-ppc??.h $RPM_BUILD_ROOT%{_includedir}/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/
chmod 644 $RPM_BUILD_ROOT%{_includedir}/*.h

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/*

# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir usr/include
LINKS=`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 %{LINKS} %{LINKS_DEVEL}`
for LINK in $LINKS; do
    if [ ! -f /usr/$LINK -o "ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'" != "" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    fi
done

# Uncomment this when using RPM > 4.4
#
# %posttrans
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS}`
# # Add symbolic links in /usr if files not already exists
# for LINK in $LINKS; do
#     if [ ! -f /usr/$LINK ]; then
#         ln -s /opt/freeware/$LINK /usr/$LINK
#     fi
# done
#     
# %preun
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS}`
# # Remove the symbolic link from /usr
# for LINK in $LINKS; do
#     if [ -L /usr/$LINK ]; then
#         if [ "`ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'`" != "" ]; then
# 	    rm /usr/$LINK
#         fi
#     fi
# done
# 
# %posttrans devel
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS_DEVEL}`
# # Add symbolic links in /usr if files not already exists
# for LINK in $LINKS; do
#     if [ ! -f /usr/$LINK ]; then
#         ln -s /opt/freeware/$LINK /usr/$LINK
#     fi
# done
#     
# %preun devel
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS_DEVEL}`
# # Remove the symbolic link from /usr
# for LINK in $LINKS; do
#     if [ -L /usr/$LINK ]; then
#         if [ "`ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'`" != "" ]; then
# 	    rm /usr/$LINK
#         fi
#     fi
# done

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/COPYRIGHT 32bit/README 32bit/RELEASE-DATE 32bit/VERSION
%{_datadir}/doc/tiff-%{version}/ChangeLog
%{_datadir}/doc/tiff-%{version}/COPYRIGHT
%{_datadir}/doc/tiff-%{version}/README
%{_datadir}/doc/tiff-%{version}/README.vms
%{_datadir}/doc/tiff-%{version}/RELEASE-DATE
%{_datadir}/doc/tiff-%{version}/TODO
%{_datadir}/doc/tiff-%{version}/VERSION
%{_datadir}/doc/tiff-%{version}/html
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man1/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/TODO 32bit/ChangeLog 32bit/html
%{_includedir}/*
%{_libdir}/*.la
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Tue Apr 26 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 4.0.6-1
- Update to version 4.0.6

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 4.0.1
- Update to version 4.0.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 3.9.5-1
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 3.9.5-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Mon Sep 12 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 3.9.5-1
- Initial port on Aix5.3 
