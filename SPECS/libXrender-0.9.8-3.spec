# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# Version with/without AIX X11
%define AIXX11 1


%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

%define baserelease 3

Summary:	X.Org X11 libXrender runtime library
Name: 		libXrender
Version: 	0.9.8
Release: 	%{baserelease}%{?RELEASE_SUFFIX}
License: 	MIT
Group: 		System Environment/Libraries
URL: 		http://www.x.org
Source0: 	ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: 	%{name}.so.0-aix32
Source2: 	%{name}.so.0-aix64
Source3:    %{name}-%{version}-%{baserelease}.build.log
Patch0: 	%{name}-%{version}-aix.patch

Provides: libXrender
Obsoletes: xrender, xrender-devel

BuildRequires: autoconf automake libtool
BuildRequires: pkg-config
BuildRequires: renderproto >= 0.11.1
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: xorg-x11-util-macros
BuildRequires: libX11-devel
Requires: libX11
%endif

%description
X.Org X11 libXrender runtime library

The library is available as 32-bit and 64-bit.
%if %{AIXX11} == 1
This package requires AIX X11.
%else
This package requires Bull Freeware X11.
%endif

%package devel
Summary: X.Org X11 libXrender development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config
Requires: renderproto >= 0.11.1

%description devel
X.Org X11 libXrender development package

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
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
export SHELL=/opt/freeware/bin/bash
export CONFIG_ENV_ARGS=/opt/freeware/bin/bash
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export PKG_CONFIG_PATH="/opt/freeware/lib/pkgconfig"

# /opt/freeware/lib is needed for libgcc_s
export LDFLAGS32="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS64="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

%if %{with gcc_compiler}
export CC__="/opt/freeware/bin/gcc"
export CC32="${CC__} -maix32"
export CC64="${CC__} -maix64"
%else
export CC__="/opt/IBM/xlC/13.1.3/bin/xlc"
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
export CC32="${CC__} -q32"
export CC64="${CC__} -q64"
%endif


# first build the 64-bit version
cd 64bit
export CC=$CC64
export LDFLAGS=$LDFLAGS64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}

# now build the 32-bit version
cd ../32bit
export CC=$CC32
export LDFLAGS=$LDFLAGS32
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

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
/usr/bin/ar -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a  %{name}.so.1

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a  %{name}.so.1

# Add the older shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} %{name}.so.0
/usr/bin/strip -X32 -e %{name}.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0
cp %{SOURCE2} %{name}.so.0
/usr/bin/strip -X64 -e %{name}.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
gmake -k check
/usr/sbin/slibclean
cd ..

cd 32bit
gmake -k check
/usr/sbin/slibclean
cd ..

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog
%{_prefix}/lib/*.a


%files devel
%defattr(-,root,system,-)
%dir %{_prefix}/include/X11
%dir %{_prefix}/include/X11/extensions
%{_prefix}/include/X11/extensions/Xrender.h
%{_prefix}/lib/*.la
%{_prefix}/lib/pkgconfig/xrender.pc

%changelog
* Tue Sep 3 2019 Clément Chigot <clement.chigot@atos.net> - 0.9.8-3
- Add %check
- Rebuild with AIX libX11

* Tue May 29 2018 Nitish K Mishra <nitismis@in.ibm.com> - 0.9.8-2
- Rebuild to obsolete xrender
 
* Mon Apr 18 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 0.9.8-1
- Updated to 0.9.8
- Added option to build against AIX X11 or Bull Freeware X11

* Thu Apr 07 2016 Tony Reix <tony.reix@bull.net> - 0.9.6-6
- Rebuild due to libX11 issue (shr4.o)

* Wed Sep 25 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-5
- Rebuild due to libX11 issue

* Mon Mar 05 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-4
- Must preserve inital include and library of Aix

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-3
- Initial port on Aix6.1

* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Jun 07 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-1
- Initial porting on platform Aix5.3 

