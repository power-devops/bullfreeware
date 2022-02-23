# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# Previous version of freetype2 installed on build machine was too old
# %%define freetype_version 2.4.4

# Fedora has following, but symbol FT_Done_MM_Var not in old AIX freetype2
# freetype2 version 2.9.1  cooresponds to libtool version 22.1.16 & .so 6.16.1
#
# ifdef'd in source code but runtime dep will be made for FT_Done_MM_Var symbol in freetype-2.9.1
# so update the build deps as well to keep deps consistency between runtime and build time.
%global freetype_version 2.9.1

%define _libdir64 %{_libdir}64

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.13.92
Release:	2
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
License:	MIT and Public Domain and UCD
Group:		System Environment/Libraries
URL:		http://fontconfig.org/
Source0:	https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.xz

# TBC Source1:	fontconfig-25-no-bitmap-fedora.conf
Source2:	fontconfig-fc-cache
Source3:	fontconfig-FcConfigGetFilename.3

Source10: %{name}-%{version}-%{release}.build.log

# BuildRoot:      %{_tmppath}/%{name}-%{version}-root

# Fedora patches
# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:		%{name}-sleep-less.patch
Patch1:		%{name}-required-freetype-version.patch
Patch2:		%{name}-score-hint-on-match.patch
Patch3:		%{name}-fix-1744377.patch
Patch4:		%{name}-drop-lang-from-pkgkit-format.patch
Patch5:		%{name}-sysroot.patch
Patch6:		%{name}-read-latest-cache.patch
Patch7:		%{name}-mt.patch
Patch8:		%{name}-fix-test.patch
Patch9:		%{name}-fix-assertion.patch
Patch10:	%{name}-fix-dtd.patch
Patch11:	%{name}-fix-dtd-id.patch


# Following requires new freetype2 installed - info in libfreetype.pc
BuildRequires:  freetype2-devel >= %{freetype_version}
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  autoconf automake
BuildRequires:  zlib-devel
BuildRequires:  gperf
Requires:	freetype2 >= %{freetype_version}
# Requires:       expat
Requires:       libxml2

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.

The library is available as 32-bit and 64-bit.

%package devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype2-devel >= %{freetype_version}
Requires:	freetype2-devel
# Requires:  	expat-devel

%description devel
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.
Install fontconfig-devel if you want to develop programs which will use
fontconfig.

%prep

echo "dotests=%{dotests}"

# Script brpm & checks in autobuild required patches to be applied explicitly
%autosetup -p1

# %setup -q

# %patch0 -p1 -b .sleep-less
# %patch1 -p1 -b .freetype-req
# %patch2 -p1 -b .hint
# %patch3 -p1 -b .fix-1744377
# %patch4 -p1 -b .drop-lang
# %patch5 -p1 -b .sysroot
# %patch6 -p1 -b .cache
# %patch7 -p1 -b .mt
# %patch8 -p1 -b .test
# %patch9 -p1 -b .assertion
# %patch10 -p1 -b .dtd
# %patch11 -p1 -b .dtd-id

# autobuild.sh/mv do not like patch created files with mode 000
# chmod 644 ./test/test-crbug1004254.c.mt
# chmod 644 ./test/test-bz1744377.c.fix-1744377

cp %{SOURCE3} $RPM_BUILD_DIR/%{name}-%{version}/doc/FcConfigGetFilename.3

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

# Do not rebuild the docs, just install the included docs
export SOURCE_DATE_EPOCH=0
export HASDOCBOOK=no

export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS="-Wl,-blibpath:%{_libdir64}:%{_libdir}:/usr/lib:/lib"
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

autoreconf

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static \
    --enable-libxml2 \
    --with-cache-dir=/opt/freeware/lib/fontconfig/cache

gmake %{?_smp_mflags}


# now build the 32-bit version
cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
export CFLAGS=-D_LARGE_FILES
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

autoreconf

./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --enable-libxml2 \
    --with-cache-dir=/opt/freeware/lib/fontconfig/cache

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

# Move installed doc files to build directory for correct packaging
# mv $RPM_BUILD_ROOT%{_datadir}/doc/fontconfig/* .
# rmdir $RPM_BUILD_ROOT%{_datadir}/doc/fontconfig/

# rename fc-cache binary
mv $RPM_BUILD_ROOT%{_bindir}/fc-cache $RPM_BUILD_ROOT%{_bindir}/fc-cache_32

install -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fc-cache

# create link to man page
echo ".so man1/fc-cache.1" > $RPM_BUILD_ROOT%{_datadir}/man/man1/fc-cache_32.1


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

export SOURCE_DATE_EPOCH=0

cd 64bit
export CC=$CC64
export OBJECT_MODE=64

(VERBOSE=1 gmake -k check || true )
/usr/sbin/slibclean

cd ../32bit
export CC=$CC32
export OBJECT_MODE=32
(VERBOSE=1 gmake -k check || true )
/usr/sbin/slibclean


%post
umask 0022

mkdir -p /opt/freeware/lib/fontconfig/cache



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/README 32bit/AUTHORS
%doc 32bit/doc/fontconfig-user.txt 32bit/doc/fontconfig-user.html
%doc 32bit/conf.d/README
%license 32bit/COPYING
%{_prefix}/etc/fonts/*
# %{_bindir}/fc*
%{_bindir}/fc-cache*
%{_bindir}/fc-cat*
%{_bindir}/fc-conflist*
%{_bindir}/fc-list*
%{_bindir}/fc-match*
%{_bindir}/fc-pattern*
%{_bindir}/fc-query*
%{_bindir}/fc-scan*
%{_bindir}/fc-validate*
%{_libdir}/*.a
# %{_libdir}/*so*
# %{_libdir64}/*so*
%dir /opt/freeware/lib/fontconfig/cache
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
# /usr/lib/*.a
/usr/bin/*


%files devel
%defattr(-,root,system)
# %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig/*.h
%{_datadir}/doc/fontconfig*
%{_datadir}/man/man3/*
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc
# /usr/lib/*.la
/usr/include/fontconfig
# %doc 32bit/fontconfig-devel.txt 32bit/fontconfig-devel


%changelog
* Tue May 26 2020 Michael Wilson <michael.a.wilson@atos.net> 2.13.92-2
- Include Requires libxml2 to avoid missing symbols by loading AIX LPP libxml

* Wed Apr 15 2020 Michael Wilson <michael.a.wilson@atos.net> 2.13.92-1
- Update to version 2.13.92
- Based on Fedora 33
- Build requires new freetype2 (test of version in pkgconfig/freetype2.pc)
- http://git.savannah.gnu.org/cgit/freetype/freetype2.git/tree/docs/VERSIONS.TXT
-    freetype2 .pc tested >= 20.0.14 corresponds to version 2.8.0 & .so 6.14.0
-    freetype_version 2.9.1 corresponds to libtool .pc 22.1.16  & .so 6.16.1
-    latest freetype2 2.10.1 corresponds to libtool .pc 23.1.17 & .so 6.17.1
-    previous AIX freetype2 2.4.4 corresponds to libtool .pc 12.2.6 & .so 6.6.2

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
