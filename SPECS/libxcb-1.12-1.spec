# Version with/without AIX X11
%{!?aixX11:%define AIXX11 0}
%{?aixX11:%define AIXX11 1}

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

%define _libdir64 %{_libdir}64

Summary:	X.Org xcb library
Name: 		libxcb
Version: 	1.12
Release: 	1%{RELEASE_SUFFIX}
License: 	MIT
Group: 		System/Libraries
URL: 		http://www.x.org
Source0: 	ftp://ftp.x.org/pub/individual/xcb/%{name}-%{version}.tar.gz
Patch0: 	%{name}-%{version}-aix.patch
BuildRoot: 	/var/tmp/%{name}-%{version}-%{release}-root

Provides: xcb

BuildRequires: autoconf automake libtool
BuildRequires: pkg-config
BuildRequires: libpng-devel
BuildRequires: libxslt
BuildRequires: check-devel
BuildRequires: xcb-proto = 1.12
BuildRequires: libpthread-stubs-devel
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: libXdmcp-devel
BuildRequires: libXau-devel
%endif
Requires: xcb-proto = 1.12

%description
X.Org xcb library

The library is available as 32-bit and 64-bit.
%if %{AIXX11} == 1
This package requires AIX X11.
%else
This package requires Bull Freeware X11.
%endif

%package devel
Summary: X.Org xcb library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org xcb library.

This package contains static libraries and header files need for development.


%prep
echo "AIXX11=%{AIXX11}"
echo "DO_TESTS=%{DO_TESTS}"
%setup -q
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
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/usr/vac/bin/xlc"
export CC64="$CC32 -q64"

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
export LIBS="-lpthread"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static \
    --enable-xkb \
    --enable-xevie \
    --enable-xinput \
    --enable-xprint
    
# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

# now build the 32-bit version
cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
export LIBS="-lpthread"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --enable-static \
    --enable-xkb \
    --enable-xevie \
    --enable-xinput \
    --enable-xprint

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}
if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true ) 
    /usr/sbin/slibclean
fi

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# extract 64-bit shared object files from 64 bit libs
LISTLIB=`cd ${RPM_BUILD_ROOT}%{_libdir64} ; ls -1 *.a | cut -d . -f 1`
cd ${RPM_BUILD_ROOT}%{_libdir64}
for lib in ${LISTLIB}
do
    SO=0
    if [ ${lib} = "libxcb" -o ${lib} = "libxcb-xkb" -o ${lib} = "libxcb-sync" ]
    then
        SO=1
    fi
    /usr/bin/ar -X64 xv ${lib}.a  ${lib}.so.${SO}
done
cd -

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects and extract the 32-bit shared objects
cd ${RPM_BUILD_ROOT}%{_libdir}
for lib in ${LISTLIB}
do
    SO=0
    if [ ${lib} = "libxcb" -o ${lib} = "libxcb-xkb" -o ${lib} = "libxcb-sync" ]
    then
        SO=1
    fi
    /usr/bin/ar -q -X64 ${lib}.a  ${RPM_BUILD_ROOT}%{_libdir64}/${lib}.so.${SO}
    /usr/bin/ar -X32 xv ${lib}.a  ${lib}.so.${SO}
done
cd -

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/xcb
LINKS=`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 lib/libxcb*.a lib/libxcb*.la include/xcb/*.h`
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
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%doc 32bit/INSTALL 32bit/NEWS 32bit/COPYING 32bit/README
/usr/lib/*.a

%files devel
%defattr(-,root,system)
%{_libdir}/libxcb*.la
%{_includedir}/xcb/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/libxcb
/usr/lib/*.la
/usr/include/xcb

%changelog
* Fri May 20 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.12-1
- Updated to version 1.12

* Tue Apr 19 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.11-1
- Updated to version 1.11
- Added options to build agains AIX X11 or Bull X11 

* Wed May 15 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.9-1
- Initial port on Aix6.1

* Thu Sep 01 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.7-1
- Inital port on Aix 5.3

