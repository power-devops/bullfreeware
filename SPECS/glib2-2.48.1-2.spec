%{!?dotests: %define dotests 1}

Summary: A library of handy utility functions
Name: 	 glib2
Version: 2.48.1
Release: 2
License: LGPLv2+
Group: 	 System Environment/Libraries
URL: 	 http://www.gtk.org
Source0: http://download.gnome.org/sources/glib/2.33/glib-%{version}.tar.xz
# glib-2.48.0-xlc-W.sh is aimed to tell configure not using GCC -W options
%define  XLCW glib-2.48.1-xlc-W.sh
Source1: %{XLCW}
Patch0:  glib-%{version}-aix.patch
#Patch1:  glib-%{version}-constructor-aix.patch
Patch2:  glib-%{version}-glibconfig-aix.patch
Patch3:  glib-%{version}-configure.ac-aix.patch
Patch4:  glib-%{version}-constructorwrapper-aix.patch
BuildRoot: /var/tmp/%{name}-%{version}-buildroot

BuildRequires: pkg-config
BuildRequires: libffi-devel >= 3.0.10-1
BuildRequires: gettext-devel >= 0.17
BuildRequires: xml-common
BuildRequires: docbookx >= 4.1.2
BuildRequires: docbook-style-xsl
Requires: gettext >= 0.17
Requires: libffi >= 3.0.10-1

%define _libdir64 %{_prefix}/lib64

%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.


The library is available as 32-bit and 64-bit.

%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: pkg-config
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".

Please note that if you want to build a program with linked GRessources
with xlC, you need to compile the ressource XML without constructors
(glib-compile-resources --manual-register) and to use the -binitfini
option of ld to call resources_register_resource and
resources_unregister_resource whene required :
-binitfini:resources_register_resource:resources_unregister_resource


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n glib-%{version}
# Already applied ?
#%patch0 -p1 -b .aix
# Not OK with constructorwrapper-aix patch
#%patch1 -p1 -b .constructor-aix
%patch2 -p1 -b .glibconfig-aix
%patch3 -p1 -b .configure.ac-aix
%patch4 -p1 -b .constructorwrapper-aix

cp %{SOURCE1} /tmp
chmod +x /tmp/%{XLCW}

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
/usr/bin/env | sort
# setup environment for 32-bit and 64-bit builds
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=/tmp/libintl-0.19.7.1:/opt/freeware/lib:/usr/lib
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CCW="/tmp/%{XLCW} /usr/vac/bin/xlc_r"
export CXXW="/tmp/%{XLCW} /usr/vac/bin/xlC_r"


# first build the 64-bit version
export CC="$CCW   -q64"
export CXX="$CXXW -q64"

export OBJECT_MODE=64

#The following line makes the link using the OLD /opt/freeware/lib/libglib-2.0.a instead of the new one !!!
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS=""

cd 64bit

#LIBS= .... is not useful. Removed
CFLAGS="  -DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g" \
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --disable-Bsymbolic \
    --disable-silent-rules \
    --enable-shared --disable-static \
    --with-threads=posix \
    --disable-fam \
    --with-pcre=internal 

#FC23:
#           --enable-systemtap \
#           --enable-static \
#           --enable-installed-tests

# --with-aix-soname=aix|svr4|both
#     shared library versioning (aka "SONAME") variant to provide on AIX, [default=aix].


export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vac/bin/xlC_r -q64"

gmake %{?_smp_mflags}

# There are hangs blocking the whole thing
if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


# Save 64bits version of libraries:
# Toujours UTILE ????????????????????????????????
#cp gio/.libs/libgio-2.0.so.0 ..
#cp glib/.libs/libglib-2.0.so.0 ..
#cp gmodule/.libs/libgmodule-2.0.so.0 ..
#cp gobject/.libs/libgobject-2.0.so.0 ..
#cp gthread/.libs/libgthread-2.0.so.0 ..


/usr/sbin/slibclean


# now build the 32-bit version
export CC="$CCW"
export CXX="$CXXW"

export OBJECT_MODE=32

#The following line makes the link using the OLD /opt/freeware/lib/libglib-2.0.a instead of the new one !!!
#export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000"

cd ../32bit

CFLAGS="  -DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  \
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --disable-Bsymbolic \
    --enable-shared --disable-static \
    --disable-silent-rules \
    --with-threads=posix \
    --disable-fam \
    --with-pcre=internal

export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vac/bin/xlc_r"

gmake %{?_smp_mflags}

# There are hangs blocking the whole thing
if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# install 64-bit version

export OBJECT_MODE=64
cd 64bit

gmake V=0 DESTDIR=$RPM_BUILD_ROOT install


# install 32-bit version

export OBJECT_MODE=32
cd ../32bit

gmake V=0 DESTDIR=$RPM_BUILD_ROOT install


# 1) Extract 64bits .so files
#cd ${RPM_BUILD_ROOT}%{_libdir64}
#/usr/bin/ar -X64 xv libglib-2.0.a    libglib-2.0.so.0
#/usr/bin/ar -X64 xv libgio-2.0.a     libgio-2.0.so.0
#/usr/bin/ar -X64 xv libgmodule-2.0.a libgmodule-2.0.so.0
#/usr/bin/ar -X64 xv libgobject-2.0.a libgobject-2.0.so.0
#/usr/bin/ar -X64 xv libgthread-2.0.a libgthread-2.0.so.0
#/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}%{_libdir}
for f in lib*.a ; do
    /usr/bin/ar -X32 -x ${f}
done
for f in lib*so* ; do
    ln -s ${f} `basename ${f} .0`
done

cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir64}/lib*.a ; do
    /usr/bin/ar -X64 -x ${f}
done
for f in lib*so* ; do
    ln -s ${f} `basename ${f} .0`
done

# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libglib-2.0.a    ${RPM_BUILD_ROOT}%{_libdir64}/libglib-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgio-2.0.a     ${RPM_BUILD_ROOT}%{_libdir64}/libgio-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgmodule-2.0.a ${RPM_BUILD_ROOT}%{_libdir64}/libgmodule-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgobject-2.0.a ${RPM_BUILD_ROOT}%{_libdir64}/libgobject-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgthread-2.0.a ${RPM_BUILD_ROOT}%{_libdir64}/libgthread-2.0.so.0

cd ${RPM_BUILD_ROOT}
#ln -sf %{_prefix}/include/glib-2.0/glib %{_prefix}/include/glib
ln -sf %{_prefix}/lib/glib-2.0/include/glibconfig.h %{_prefix}/include

cd -
(cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS
%{_libdir}/*.a
%{_libdir}/lib*so*
%{_libdir64}/lib*so*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
/usr/lib/*.a
/usr/lib/lib*so*
/usr/lib64/lib*so*


%files devel
%defattr(-, root, system)
#%doc %{_datadir}/gtk-doc/html/*
%{_prefix}/bin/*
%{_prefix}/lib/*.la
%{_prefix}/lib/glib-2.0/*
# gdbus no more useful in 2.48.0 ??
#%{_prefix}/lib/gdbus-2.0/*
%{_prefix}/lib/pkgconfig/*
%{_prefix}/lib/gio/*
%{_prefix}/include/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*
%{_datadir}/gdb/auto-load/*
%{_datadir}/glib-2.0
/usr/bin/*
/usr/lib/*.la
/usr/include/*


%changelog
* Mon Mar 23 2017 Tony Reix <tony.reix@atos.net> 2.48.1-2
- Rebuild with gettext 0.19.8-1 in order to no more need __dbargs & Co

* Thu Jun 9 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.48.1-1
- Updated to version 2.48.1
- Fixed build issues with libiconv
- Improved BuildRequires

* Wed Apr 27 2016 Tony Reix <tony.reix@bull.net> 2.48.0-2
- Fix issues with .so files that must not be installed

* Wed Apr 13 2016 Tony Reix <tony.reix@bull.net> 2.48.0-1
- Update to version 2.48.0

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.33.2-1
- Update to version 2.33.2

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.22.5-5
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.22.5-4
- rebuild for compatibility with new libiconv.a 1.13.1-2

*  Wed Sep 07 2011  Gerard Visiedo <gerard.visiedo@bull.net> 2.22.5-3
-  Add libraries 64bit

*  Thu Jan 13 2011  Jean Noel Cordenner <Jean-noel.cordenner@bull.net> 2.22.5-2
- Fix some bad link for glib2-devel

*  Wed Oct 27 2010  Jean Noel Cordenner <Jean-noel.cordenner@bull.net> 2.22.5-1
- Update to version 2.22.5

*  Wed Sep 13 2006  BULL
 - Release  4
 - New version  version: 2.10.1
 - added tag to support the build 64 bit
 - changed type long -> int to support 64 bit in fonction g_get_current_dir
 - packaging fixes perl at /usr/lib/

*  Fri Dec 23 2005  BULL
 - Release  3
 -  Prototype gtk 64 bit

*  Tue Dec 06 2005  BULL
 - Release  2
 - correct UTF8 conversion problem that for example prevent metacity to launch at startup.

*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 2.8.1

*  Tue Aug 09 2005  BULL
 - Release  4
 - Create symlinks between /usr/share and /opt/freeware/share

*  Thu Jun 23 2005  BULL
 - Release  3
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 2.6.3

*  Wed Feb 16 2005  BULL
 - Release  2
 - Move setting of G_BROKEN_FILENAMES in /etc/environment from gedit to glib

*  Wed Nov 24 2004  BULL
 - Release  1
 - New version  version: 2.4.7

*  Tue Nov 23 2004  BULL
 - Release  3

*  Mon Sep 20 2004  BULL
 - Release  2
 - Do not core when dlerror() returns NIL
