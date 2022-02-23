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

# Dependencies versions, last updated for pango 1.40.1
%define glib2_version 2.33.12
%define harfbuzz_version 0.9.30
%define fontconfig_version 2.10.91
%define freetype_version 2.1.5
%define xft_version 2.0.0
%define cairo_version 1.12.10

Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.40.1
Release: 1%{RELEASE_SUFFIX}
License: GNU GPL
Url: 	 http://www.pango.org
Source0: http://ftp.gnome.org/pub/GNOME/sources/pango/1.40/%{name}-%{version}.tar.xz
Group:   System Environment/Libraries
Buildroot: /var/tmp/%{name}-root
Prefix:  %{_prefix}

BuildRequires: pkg-config
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libXrender-devel
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: freetype2-devel >= %{freetype_version}
BuildRequires: harfbuzz-devel >= %{harfbuzz_version}
BuildRequires: libXft-devel >= %{xft_version}
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: libX11-devel

Requires: libX11
%endif
Requires: glib2 >= %{glib2_version}
Requires: libXrender
Requires: cairo >= %{cairo_version}
Requires: fontconfig >= %{fontconfig_version}
Requires: freetype2 >= %{freetype_version}
Requires: harfbuzz >= %{harfbuzz_version}
Requires: libXft >= %{xft_version}

%description 
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

The library is available as 32-bit and 64-bit

%package devel
Summary: System for layout and rendering of internationalized text
Group: Development/Libraries
Requires: pango = %{version}-%{release}

%description devel
The pango-devel package includes the header files and developer docs
for the pango package.

%prep
echo "AIXX11=%{AIXX11}"
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
# /opt/freeware/bin needs to be first in the PATH to make the tests work (tests
# not compatible with AIX diff -u command behavior)
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
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
./configure  \
	--prefix=%{prefix} \
	--mandir=%{_mandir} \
	--disable-silent-rules \
	--enable-shared  --disable-static

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
    --enable-shared  --disable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true ) 
    /usr/sbin/slibclean
fi

%define LINKS bin/pango* lib/libpango*.a
%define LINKS_DEVEL include/pango-1.0/pango/*.h lib/libpango*.la

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake install DESTDIR=$RPM_BUILD_ROOT
cd ..

# extract 64-bit shared object files from 64 bit libs
LISTLIB=`ls -1 ${RPM_BUILD_ROOT}%{_libdir}/*.a | sed -e "s/.a\$//" | sed -e "s-.*/--g"`
for lib in ${LISTLIB}
do
    /usr/bin/ar -X64 xv ${RPM_BUILD_ROOT}%{_libdir}/${lib}.a  ${lib}.so.0
done

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
for lib in ${LISTLIB}
do
    /usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${lib}.a  ${lib}.so.0
done


# Comment this when using RPM > 4.4
#
# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/pango-1.0/pango
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
# mkdir -p /usr/include/pango-1.0/pango
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
# rmdir -p --ignore-fail-on-non-empty /usr/include/pango-1.0/pango

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/README 32bit/AUTHORS 32bit/COPYING 32bit/NEWS
%{_mandir}/man1/*
%{_bindir}/pango*
%{_libdir}/libpango*.a
/usr/bin/*
/usr/lib/*.a

%files devel
%defattr(-,root,system)
#%doc %{_datadir}/gtk-doc/html/pango/*
%{_includedir}/pango-1.0/pango/*.h
%{_libdir}/libpango*.la
%{_libdir}/pkgconfig/pango*.pc
/usr/lib/*.la
/usr/include/pango-1.0

%changelog
* Mon Apr 25 2016 Matthieu Sarter <matthieu.sarter@atos.net> - 1.40.1-1
- Update to version 1.40.1

* Mon Oct 07 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.30.1-2
- Rebuild due to libX11 issue

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.30.1-1
- Update to version 1.30.1

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.28.3-4
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.28.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 8 2011 Gerard Visiedo <gerard.visiedo@bull.fnet> 1.28.3-2
- Add libraries 64-bit

* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.28.3-1
- update to version 1.28.3

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.10.0

*  Wed Aug 10 2005  BULL
 - Release  3

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 1.8.1
 - Fix Xscreensaver-demo core at initialisation on AIX

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 1.6.0

*  Wed Jul 28 2004  BULL
 - Release  2
 - fix bug causing the generation of a core file
