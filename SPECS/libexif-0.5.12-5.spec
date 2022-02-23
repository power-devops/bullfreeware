%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: 	EXIF tag library
Name: 		libexif
Version: 	0.5.12
Release: 	5
License:	GPL
Group: 		System Environment/Libraries
Source: 	libexif-%{version}.tar.bz2

Patch0:		libexif-0.5.12-aix.patch
Patch1:		libexif-0.5.12-autotools.patch

Url: 		http://sourceforge.net/projects/libexif/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}

%description
libexif is a library for parsing, editing, and saving EXIF data. It is
intended to replace lots of redundant implementations in command-line
utilities and programs with GUIs.

%package devel
Summary: The files needed for libexif application development
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The libexif-devel package contains the libraries and include files
that you can use to develop libexif applications.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/libexif-0.5.12-aix.patch
$PATCH -p2 -s < %{_sourcedir}/libexif-0.5.12-autotools.patch


%build
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix} --disable-gtk-doc
PATH=%{_bindir}:$PATH make

%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# Make the links
cd %{buildroot}
for dir in bin share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libexif.a
%{_libdir}/libexif.la
%{_datadir}/locale/*/LC_MESSAGES/*.mo
/usr/share/*
/usr/lib/*

%files devel
%defattr(-,root,system)
%{_libdir}/pkgconfig/libexif.pc
%{_includedir}/libexif/*.h
%{_libdir}/libexif.a
%{_libdir}/libexif.la

/usr/include/*
/usr/lib/*
%changelog
*  Mon Feb 13 2006  BULL
 - Release  5
 - Correct unresolved symbols on libintl.a library that impact dgettext and bindtextdomain functions

*  Tue Nov 15 2005  BULL
 - Release  4

*  Wed Aug 10 2005  BULL
 - Release  3
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 0.5.12

