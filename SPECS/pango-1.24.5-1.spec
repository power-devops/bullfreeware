Summary: System for layout and rendering of internationalized text
Name: 	 pango
Version: 1.24.5
Release: 1
License: GNU GPL
Url: 	 http://www.pango.org
Source:  http://ftp.gnome.org/pub/GNOME/sources/pango/1.24/%{name}-%{version}.tar.gz
Group:   System Environment/Libraries
Buildroot: /var/tmp/%{name}-root
Prefix:  %{_prefix}
BuildRequires: glib2-devel
Requires: glib2

%description 
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

%package devel
Summary: System for layout and rendering of internationalized text
Group: Development/Libraries
Requires: pango = %{version}-%{release}

%description devel
The pango-devel package includes the header files and developer docs
for the pango package.

%prep
%setup -q


%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure --enable-shared --disable-static --with-included-modules=yes \
		--prefix=%{prefix}

make 

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib
cd $RPM_BUILD_ROOT
for dir in bin lib
do
	mkdir -p usr/$dir
	cd usr/$dir
	ln -sf ../..%{prefix}/$dir/* .
	cd -
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc README AUTHORS COPYING NEWS
%{_datadir}/man/man1/*
%{_bindir}/pango*
/usr/bin/pango*
%{_prefix}/etc/pango/pangox.aliases
%{_libdir}/libpango*.a
/usr/lib/libpango*.a

%files devel
%defattr(-,root,system)
%doc %{_datadir}/gtk-doc/html/pango/*
%{_prefix}/include/pango-1.0/pango/*.h
%{_libdir}/libpango*.la
%{_libdir}/pkgconfig/pango*.pc

%changelog
* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.24.5
- update to version 1.24.5

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
