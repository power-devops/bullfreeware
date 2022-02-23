%define _prefix /opt/freeware

%define name		cairo
%define release	        1	

Summary:	Cairo provides anti-aliased vector-based rendering for X.
Name:     	%{name}
Version: 	1.2.4
Release:	%{release}
License:	MIT license
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Group:		Development/Graphics
URL:		http://www.cairographics.org
Source:		%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig
BuildRequires:	fontconfig-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel >= 1.2
Requires:	freetype2
Requires:	fontconfig
Requires:	libpng >= 1.2

%description
Cairo provides anti-aliased vector-based rendering for
X. Paths consist of line segments and cubic splines and
can be rendered at any width with various join and cap
styles. All colors may be specified with optional
translucence (opacity/alpha) and combined using the
extended Porter/Duff compositing algebra as found in the X
Render Extension.

%package -n cairo-devel
Summary:	Headers for Cairo
Group:		Development/Graphics
Requires:	%{name} = %{version}

%description -n cairo-devel
Headers for Cairo

%prep
%setup -q 

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/cairo-1.2.4-aix.patch
$PATCH -p2 -s < %{_sourcedir}/cairo-1.2.4-autotools.patch


%build
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix} --enable-gtk-doc
PATH=%{_bindir}:$PATH make




%install
if test "%{buildroot}" != "/"; then
rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# make links
cd %{buildroot}
for dir in lib include
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done


%files
%defattr(-, root, system)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_libdir}/*.a
%{_prefix}/64/lib/*.a
/usr/lib/*.a

%files -n cairo-devel
%defattr(-, root, root)
%{_includedir}/cairo/*.h
%{_libdir}/*.la
%{_prefix}/64/lib/*.la
%{_libdir}/pkgconfig/cairo*.pc
%{_datadir}/gtk-doc/html/cairo/

%changelog
*  Fri Nov 17 2006  BULL
 - Release  1
 - New version  version: 1.2.4
 - gnome 2.16.1

*  Mon Sep 18 2006  BULL
 - Release  5
 - support 64 bits

*  Wed Jul 26 2006  BULL
 - Release  1
 - New version  version: 1.0.2

*  Mon Feb 13 2006  BULL
 - Release 4 
 - Prototype gtk 64 bit - build with type CARD32 = unsigned int 
*  Fri Dec 23 2005  BULL
 - Release 3
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  2

*  Fri Nov 04 2005  BULL
 - Release  1
 - New version  version: 1.0.0

