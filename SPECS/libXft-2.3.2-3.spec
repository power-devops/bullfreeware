%bcond_without AIXX11

%bcond_without dotests

%define _libdir64 %{_libdir}64

%if %{with AIXX11}
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif


Summary: 	X.Org X11 libXft runtime library
Name: 		libXft
Version: 	2.3.2
Release: 	3
License: 	MIT
Group: 		System Environment/Libraries
URL: 		http://www.x.org
Source0: 	ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: 	%{name}.so.0-aix32
Source2: 	%{name}.so.0-aix64
Source1000:     %{name}-%{version}-%{release}.build.log

Provides:      xft = %{version}-%{release}

BuildRequires: libXrender-devel >= 0.9.5
BuildRequires: freetype2-devel >= 2.3.5
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: expat-devel >= 2.1.0
BuildRequires: pkg-config
BuildRequires: autoconf automake libtool

Requires: libXrender >= 0.9.5
Requires: freetype2 >= 2.3.5
Requires: fontconfig >= 2.5.0
%if %{with AIXX11}
BuildRequires: aix-x11-pc
%else
BuildRequires: libX11-devel >= 1.5

Requires: libX11 >= 1.5
%endif


%description
X.Org X11 libXft runtime library

The library is available as 32-bit and 64-bit.
%if %{with AIXX11}
This package requires AIX X11.
%else
This package requires Bull Freeware X11.
%endif


%package devel
Summary: X.Org X11 libXft development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXft development package

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q

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
export CC32="gcc -maix32"
export CC64="gcc -maix64"
export LIBS="-lXrender"
export CFLAGS="-I/usr/include/X11"

export XRENDER_LIBS="-lXrender -lX11"
export XRENDER_CFLAGS="-I/opt/freeware/include"
export FREETYPE_LIBS="-lfreetype -lz"
export FREETYPE_CFLAGS="-I/opt/freeware/include/freetype2"
export FONTCONFIG_LIBS="-lfontconfig"
export FONTCONFIG_CFLAGS="-I/opt/freeware/include"

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
./configure \
    --libdir=%{_libdir64} \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}


# now build the 32-bit version
cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}


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

# extract 64-bit shared object file from 64 bit lib
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 xv %{name}.a  %{name}.so.2
cd -

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects and extract the 32-bit shared objects
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -q -X64 %{name}.a  ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.2
/usr/bin/ar -X32 xv %{name}.a  %{name}.so.2
cd -

# Add the older shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} %{name}.so.0
/usr/bin/strip -X32 -e %{name}.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0
cp %{SOURCE2} %{name}.so.0
/usr/bin/strip -X64 -e %{name}.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/X11/Xft
LINKS="`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 include/X11/Xft/*.h`
lib/libXft.a
lib/libXft.la"
for LINK in $LINKS; do
    if [ ! -e /usr/$LINK ] || [ x`ls -l /usr/$LINK | grep -v "/opt/freeware/$LINK"` == "x" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    else
	echo "Warning: /usr/$LINK already exists and is not a link to /opt/freeware/$LINK"
    fi
done

%check
%if %{with dotests}
cd 32bit
( gmake -k check || true )
/usr/sbin/slibclean
cd ../64bit
( gmake -k check || true )
/usr/sbin/slibclean
%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/README 32bit/ChangeLog
%{_libdir}/libXft.a

%files devel
%defattr(-,root,system,-)
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/pkgconfig/xft.pc
%{_mandir}/man3/Xft.3

%changelog
* Tue Nov 30 2021 Etienne Guesnet <etienne.guesnet@atos.net>  2.3.2-3
- Rebuild on RPMv4

* Mon Apr 18 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>  2.3.2-2
- Added option to build against AIX X11 or Bull Freeware X11
- Improved 32/64 bits build

* Tue Apr 12 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>  2.3.2-1
- Updated to version 2.3.2
- Fixed libraries references to use /opt/freeware/lib/libXrender.a instead of /usr/lib/libXrender.a

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  2.2.0-3
- Initial port on Aix6.1

* Mon Sep 26 2011 Patricia Cugny <patricia.cugny@bull.net> 2.2.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2
