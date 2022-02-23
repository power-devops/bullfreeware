%define _prefix /opt/freeware

Summary: Simple DirectMedia Layer
Name: SDL
Version: 1.2.5
Release: 5
Source0: %{name}-%{version}.tar.bz2
URL: http://www.libsdl.org/
Copyright: LGPL
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}-buildroot

Patch0:		SDL-1.2.5-aix.patch
Patch1:		SDL-1.2.5-autotools.patch

Prefix: %{_prefix}
Provides: libSDL.a

%description
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

%package devel
Summary: Libraries, includes and more to develop SDL applications.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the libraries, include files and other resources you can use
to develop SDL applications.


%prep

%setup -q 

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/SDL-1.2.5-aix.patch
$PATCH -p2 -s < %{_sourcedir}/SDL-1.2.5-autotools.patch


%build
PATH=%{_bindir}:$PATH \
	CPPFLAGS=-I%{_includedir} \
	./configure --prefix=%{prefix} --enable-nas
make

%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

cd %{buildroot}
for dir in bin lib include
do
	mkdir -p usr/$dir
	cd usr/$dir
	ln -sf ../..%{prefix}/$dir/* .
	cd -
done

%clean

%files
%defattr(-,root,system)
%doc README-SDL.txt COPYING CREDITS BUGS
%{prefix}/lib/lib*.a
/usr/lib/lib*.a

%files devel
%defattr(-,root,system)
%doc README README-SDL.txt COPYING CREDITS BUGS WhatsNew docs.html
%doc docs/index.html docs/html
%{prefix}/bin/*
%{prefix}/lib/lib*.la
%{prefix}/include/SDL/
%{prefix}/man/man3/*
%{prefix}/share/aclocal/*
/usr/bin/*
/usr/include/*

%changelog
*  Thu Nov 16 2006  BULL
 - Release  5
 - gnome 2.16.1

*  Tue Nov 15 2005  BULL
 - Release  4

*  Wed May 25 2005  BULL
 - Release  3

*  Tue Nov 24 2004  BULL
 - Release  2
