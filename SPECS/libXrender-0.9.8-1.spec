# Version with/without AIX X11
%{!?aixX11:%define AIXX11 0}
%{?aixX11:%define AIXX11 1}

%{!?dotests:%define DO_TESTS 0}
%{?dotests:%define DO_TESTS 1}

%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

Summary:	X.Org X11 libXrender runtime library
Name: 		libXrender
Version: 	0.9.8
Release: 	1%{RELEASE_SUFFIX}
License: 	MIT
Group: 		System Environment/Libraries
URL: 		http://www.x.org
Source0: 	ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: 	%{name}.so.0-aix32
Source2: 	%{name}.so.0-aix64
Patch0: 	%{name}-%{version}-aix.patch
BuildRoot: 	/var/tmp/%{name}-%{version}-%{release}-root

Provides: xrender

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
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

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
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
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

%define LINKS lib/libXrender.a
%define LINKS_DEVEL lib/libXrender.la include/X11/extensions/Xrender.h

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

# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/X11/extensions
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
# mkdir -p /usr/include/X11/extensions
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
# mkdir -ignore-fail-on-non-empty /usr/include/X11/extensions

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog
%{_prefix}/lib/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%dir %{_prefix}/include/X11
%dir %{_prefix}/include/X11/extensions
%{_prefix}/include/X11/extensions/Xrender.h
%{_prefix}/lib/*.la
%{_prefix}/lib/pkgconfig/xrender.pc
/usr/lib/*.la
/usr/include/X11/extensions/Xrender.h

%changelog
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

* Tue Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-1
- Initial porting on platform Aix5.3 

