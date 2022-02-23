%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: 	A library of functions for manipulating PNG image format files.
Name: 		libpng
Version: 	1.2.8
Release: 	5
Epoch:		2
License: 	OSI certified
Group: 		System Environment/Libraries
Source: 	ftp://swrinde.nde.swri.edu/pub/png/src/libpng-%{version}.tar.bz2

Patch0:		libpng-1.2.8-aix.patch
Patch1:		libpng-1.2.8-autotools.patch

Buildroot: 	%{_tmppath}/%{name}-%{version}-root
URL: 		http://www.libpng.org/pub/png/

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package devel
Summary: 	Development tools for programs to manipulate PNG image format files.
Group: 		Development/Libraries
Requires: 	libpng = %{version}, zlib-devel

%description devel
The libpng-devel package contains the header files and static
libraries necessary for developing programs using the PNG (Portable
Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/libpng-1.2.8-aix.patch
$PATCH -p2 -s < %{_sourcedir}/libpng-1.2.8-autotools.patch

# The 'install-sh' script created by the patch is not executable
chmod +x install-sh

%build
CFLAGS="-I%{_includedir}" ./configure --prefix=%{_prefix}
make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install

# make links
cd %{buildroot}
for dir in bin lib include
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc *.txt example.c README TODO CHANGES
%{_bindir}/*-config
%{_libdir}/libpng*.a
%{_prefix}/64/lib/libpng*.a
%{_mandir}/man5/*


/usr/lib/
/usr/bin/

%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/libpng*.la
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc

/usr/include/
%changelog
*  Wed Oct 18 2006  BULL
 - Release  5

*  Mon Sep 18 2006  BULL
 - Release  4
 - support 64 bits

*  Fri Jan 06 2006  BULL
 - Release  3
 - added compatmember= shr.o

*  Fri Dec 23 2005  BULL
 - Release 2 
 - Prototype gtk 64 bit 

*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.2.8

