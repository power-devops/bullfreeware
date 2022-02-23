# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define freetype_version 2.0.9

%define _libdir64 %{_libdir}64

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.11.95
Release:	3
License:	MIT
Group:		System Environment/Libraries
URL:		http://fontconfig.org/
Source0:		https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:	freetype2 >= %{freetype_version}
Requires:       expat
BuildRequires:	freetype2-devel >= %{freetype_version}
BuildRequires:  expat-devel

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.

The library is available as 32-bit and 64-bit.

%package devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	freetype2-devel >= %{freetype_version}
Requires:  	expat-devel

%description devel
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.
Install fontconfig-devel if you want to develop programs which will use
fontconfig.

%prep
echo "dotests=%{dotests}"
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
#export CC32="/usr/vac/bin/xlc"
#export CC64="$CC32 -q64"
export CC32="/opt/freeware/bin/gcc -maix32"
export CC64="/opt/freeware/bin/gcc -maix64"

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}


# now build the 32-bit version
cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

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

# extract 64-bit shared object files from 64 bit libs
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 xv libfontconfig.a  libfontconfig.so.1
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
# 32-bit shared objects and extract the 32 bit share objects
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -q -X64 libfontconfig.a  ${RPM_BUILD_ROOT}%{_libdir64}/libfontconfig.so.1
/usr/bin/ar -X32 xv libfontconfig.a  libfontconfig.so.1

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir usr/include
LINKS="`cd ${RPM_BUILD_ROOT}/opt/freeware ; ls -1 bin/fc*`
lib/libfontconfig.a
lib/libfontconfig.la
include/fontconfig"
for LINK in $LINKS; do
    if [ ! -e /usr/$LINK ] || [ x`ls -l /usr/$LINK | grep -v "/opt/freeware/$LINK"` == "x" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    else
	echo "Warning: /usr/$LINK already exists and is not a link to /opt/freeware/$LINK"
    fi
done



%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export CC32="/opt/freeware/bin/gcc -maix32"
export CC64="/opt/freeware/bin/gcc -maix64"

cd 64bit
export CC=$CC64
export OBJECT_MODE=64

( gmake -k check || true )
/usr/sbin/slibclean

cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
( gmake -k check || true )
/usr/sbin/slibclean



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/README 32bit/AUTHORS 32bit/COPYING
%{_prefix}/etc/fonts/*
%{_bindir}/fc*
%{_libdir}/*.a
# %{_libdir}/*so*
# %{_libdir64}/*so*
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
/usr/lib/*.a
/usr/bin/*


%files devel
%defattr(-,root,system)
# %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig/*.h
%{_datadir}/doc/fontconfig*
%{_datadir}/man/man3/*
# /usr/lib/*.la
/usr/include/fontconfig

%changelog
* Thu Apr 09 2020 Michael Wilson <michael.a.wilson@atos.net> 2.11.95-3
- Rebuild on laurel2 to remove libfontconfig.la and dependency_libs
-           libfreetype.la, libexpat.la
- Gcc build only and tests moved to %%check phase

* Thu Jun 9 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.11.95-2
- Added the .so files

* Mon Apr 25 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>  2.11.95-1
- Update to version 2.11.95

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.8.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo àbull.net> 2.8.0-2
 - Compiling on 32 and 64 bits

*  Fri Nov 26 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.8.0-1
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
