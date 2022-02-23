%define freetype_version 2.0.9

%{!?dotests:%define DO_TESTS 0}
%{?dotests:%define DO_TESTS 1}

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.11.95
Release:	1
License:	MIT
Group:		System Environment/Libraries
Source:		https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.gz
URL:		http://fontconfig.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
PreReq:		freetype2 >= %{freetype_version}
BuildRequires:	freetype2-devel >= %{freetype_version}

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.

The library is available as 32-bit and 64-bit.

%package devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	freetype2-devel >= %{freetype_version}

%description devel
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.
Install fontconfig-devel if you want to develop programs which will use
fontconfig.

%prep
echo "DO_TESTS=%{DO_TESTS}"
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
export CC32="/usr/vac/bin/xlc"
export CC64="$CC32 -q64"

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

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

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true ) 
    /usr/sbin/slibclean
fi

%define LINKS lib/libfontconfig.a bin/fc*
%define LINKS_DEVEL lib/libfontconfig.la include/fontconfig/*.h

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
/usr/bin/ar -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/libfontconfig.a  libfontconfig.so.1

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
/usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/libfontconfig.a  libfontconfig.so.1

# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/fontconfig
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
#         ln -sf /opt/freeware/$LINK /usr/$LINK
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
# mkdir /usr/include/fontconfig
# LINKS=`cd /opt/freeware ; ls -1 %{LINKS_DEVEL}`
# # Add symbolic links in /usr if files not already exists
# for LINK in $LINKS; do
#     if [ ! -f /usr/$LINK ]; then
#         ln -sf /opt/freeware/$LINK /usr/$LINK
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
# rmdir --ignore-fail-on-non-empty /usr/include/fontconfig

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/README 32bit/AUTHORS 32bit/COPYING
%{_prefix}/etc/fonts/*
%{_bindir}/fc*
%{_libdir}/libfontconfig.a
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
/usr/lib/*.a
/usr/bin/*


%files devel
%defattr(-,root,system)
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig/*.h
%{_datadir}/doc/fontconfig*
%{_datadir}/man/man3/*
/usr/lib/*.la
/usr/include/fontconfig

%changelog
* Mon Apr 25 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>  2.11.95 - 1
- Update to version 2.11.95

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.8.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo àbull.net> 2.8.0-2
 - Compiling on 3é and 64 bits

*  Wed Nov 26 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.8.0-1
 - Update to version 2.8.0

*  Wed Nov 15 2006  BULL
 - Release 7 
 - gnome 2.16.1

*  Tue Sep 19 2006  BULL
 - Release 6
 - support 64 bit
*  Fri Dec 23 2005  BULL
 - Release 5
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  4
*  Mon May 30 2005  BULL
 - Release  3
 - .o removed from lib
*  Fri Sep 24 2004  BULL
 - Release  2
 - Package the directories /opt/freeware/etc/fonts, /opt/freeware/include/fontconfig and /usr/include/fontconfig along with their contents