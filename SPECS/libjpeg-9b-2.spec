%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define _libdir64 %{_libdir}64

Summary:       A library for manipulating JPEG image format files
Name:          libjpeg
Version:       9b
Release:       2
License:       IJG
Group:         System Environment/Libraries
URL:           http://www.ijg.org/
Source0:       http://www.ijg.org/files/jpegsrc.v%{version}.tar.gz
Source1:       %{name}.so.62-aix32
Source2:       %{name}.so.62-aix64
Source3:       %{name}.so.7-aix32
Source4:       %{name}.so.7-aix64
Source5:       %{name}.so.8-aix32
Source6:       %{name}.so.8-aix64
#Patch0:        %{name}-%{version}-aix.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

The library is available as 32-bit and 64-bit.


%package devel
Summary:  Development tools for programs which will use the libjpeg library
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
echo "DO_TESTS=%{DO_TESTS}"
%setup -q -n jpeg-%{version}
#%patch0

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

# first build the 64-bit version
cd 64bit
export CC=$CC64
export CXX=$CXX64
export OBJECT_MODE=64
#LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi
cd ..

# now build the 32-bit version
cd 32bit
export CC=$CC32
export CXX=$CXX32
export OBJECT_MODE=32
#LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi
cd ..

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
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 xv %{name}.a %{name}.so.9
cd -

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
# 32-bit shared objects and extract the 32 bit shared objets
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.9
/usr/bin/ar -X32 xv %{name}.a %{name}.so.9
cd -

# Add the older version 6b/7/8 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
for SOURCE in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}; do
    BITS=`echo $SOURCE | sed -e "s/.*-aix\([0-9]*\)\$/\1/"`
    SO_NAME=`basename $SOURCE | sed -e "s/-aix\([0-9]*\)\$//"`
    cp ${SOURCE} ${SO_NAME}
    /usr/bin/strip -X${BITS} -e ${SO_NAME}
    /usr/bin/ar -X${BITS} -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${SO_NAME}
    if [ ${BITS} == "64" ]; then
        cp ${SO_NAME} ${RPM_BUILD_ROOT}%{_libdir64}
    else
        cp ${SO_NAME} ${RPM_BUILD_ROOT}%{_libdir}
    fi
done

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/*

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir usr/include
LINKS=`cd ${RPM_BUILD_ROOT}%{_prefix} ; ls -1 lib/*.a lib/*.la bin/* include/*.h`
for LINK in $LINKS; do
    if [ ! -e /usr/$LINK ] || [ x`ls -l /usr/$LINK | grep -v "/opt/freeware/$LINK"` == "x" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    else
	echo "Warning: /usr/$LINK already exists and is not a link to /opt/freeware/$LINK"
    fi
done

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/README 32bit/usage.txt
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man?/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc 32bit/example.c 32bit/%{name}.txt 32bit/structure.txt
%{_includedir}/*
%{_libdir}/*.la
/usr/lib/*.la
/usr/include/*

%changelog
* Thu Jun 9 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 9b-2
- Added the .so files

* Tue Apr 26 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 9b
- Update to version 9b

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 8d-1
- Update to version 8d

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 8c-2
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 8c-1
- Initial port on Aix5.3
