Summary: A library of handy utility functions
Name: 	 glib2
Version: 2.22.5
Release: 1
License: LGPLv2+
Group: 	 System Environment/Libraries
URL: 	 http://www.gtk.org
Source0: http://download.gnome.org/sources/glib/2.22/glib-%{version}.tar.gz
Patch0:  glib-%{version}-aix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: pkg-config
BuildRequires: gettext-devel >= 0.17, pcre-devel >= 7.9
Requires: gettext >= 0.17, pcre >= 7.9

%description 
GLib is the low-level core library that forms the basis
for projects such as GTK+ and GNOME. It provides data structure
handling for C, portability wrappers, and interfaces for such runtime
functionality as an event loop, threads, dynamic loading, and an 
object system.



%package devel
Summary: A library of handy utility functions
Group: Development/Libraries
Requires: pkg-config
Requires: %{name} = %{version}-%{release}

%description devel
The glib2-devel package includes the header files for 
version 2 of the GLib library. 

%prep
%setup -q 
%patch0 -p1


%build
CFLAGS="-I/opt/freeware/include/"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure \
    --enable-shared --disable-static \
    --with-threads=posix --disable-visibility \
    --with-pcre=system --prefix=%{_prefix} 
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
cd ${RPM_BUILD_ROOT}
ln -sf %{_prefix}/include/glib-2.0/glib %{_prefix}/include/glib
ln -sf %{_prefix}/lib/glib-2.0/include/glibconfig.h %{_prefix}/include
cd -

(cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
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
%{_prefix}/lib/*.a
%{_datadir}/locale/*/LC_MESSAGES/*.mo
/usr/lib/*.a


%files devel
%defattr(-, root, system)
%doc %{_datadir}/gtk-doc/html/*
%{_prefix}/bin/*
%{_prefix}/lib/*.la
%{_prefix}/lib/glib-2.0/*
%{_prefix}/lib/pkgconfig/*
%{_prefix}/include/*
%{_datadir}/man/man1/*
%{_datadir}/aclocal/*
%{_datadir}/glib-2.0
/usr/bin/*
/usr/lib/*.la
/usr/include/*


%changelog
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
