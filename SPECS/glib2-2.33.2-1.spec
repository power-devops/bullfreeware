Summary: A library of handy utility functions
Name: 	 glib2
Version: 2.33.2
Release: 1
License: LGPLv2+
Group: 	 System Environment/Libraries
URL: 	 http://www.gtk.org
Source0: http://download.gnome.org/sources/glib/2.33/glib-%{version}.tar.gz
Patch0:  glib-%{version}-aix.patch
BuildRoot: /var/tmp/%{name}-%{version}-buildroot
BuildRequires: pkg-config
BuildRequires: libffi-devel >= 3.0.10-1
BuildRequires: gettext-devel >= 0.17
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


%prep
%setup -q -n glib-%{version}
%patch0 -p1 -b .aix


%build
# setup environment for 32-bit and 64-bit builds
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vac/bin/xlC_r -q64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

CFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
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

make

cp gio/.libs/libgio-2.0.so.0 .
cp glib/.libs/libglib-2.0.so.0 .
cp gmodule/.libs/libgmodule-2.0.so.0 .
cp gobject/.libs/libgobject-2.0.so.0 .
cp gthread/.libs/libgthread-2.0.so.0 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vac/bin/xlc_r"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

CFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS="-DLINUX_SOURCE_COMPAT -D_LARGE_FILES -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include -g"  LIBS=' -L/opt/freeware/lib' \
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
make


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"

make V=0 DESTDIR=$RPM_BUILD_ROOT install

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libglib-2.0.a     ./libglib-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgio-2.0.a     ./libgio-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgmodule-2.0.a ./libgmodule-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgobject-2.0.a ./libgobject-2.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgthread-2.0.a ./libgthread-2.0.so.0
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cd ${RPM_BUILD_ROOT}%{_libdir}
for f in lib*.a ; do
    ar -X32 -x ${f}
done
for f in lib*so* ; do
    ln -s ${f} `basename ${f} .0`
done

mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.a ; do
    ar -X64 -x ${f}
done
for f in lib*so* ; do
    ln -s ${f} `basename ${f} .0`
done

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
%doc AUTHORS COPYING NEWS
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
%{_prefix}/lib/gdbus-2.0/*
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
