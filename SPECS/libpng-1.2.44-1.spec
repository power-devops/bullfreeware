Summary: A library of functions for manipulating PNG image format files
Name: 	 libpng
Version: 1.2.44
Release: 1
License: zlib
Group: 	 System Environment/Libraries
URL: 	 http://www.libpng.org/pub/png/
Source:  ftp://ftp.simplesystems.org/pub/png/src/%{name}-%{version}.tar.gz
#Patch0:  %{name}-%{version}-aix.patch
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel
Requires: zlib

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.


%package devel
Summary: Development tools for programs to manipulate PNG image format files
Group: Development/Libraries
Requires: libpng = %{version}-%{release} zlib-devel pkg-config

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.



%prep
%setup -q
#%patch0


%build
#./autogen.sh

./configure --enable-shared --enable-static \
    --prefix=%{_prefix}
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

(
  cd $RPM_BUILD_ROOT
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGES *.txt LICENSE README TODO example.c
%{_libdir}/libpng*.a
/usr/lib/libpng*.a
%{_datadir}/man/man5/png.5


%files devel
%defattr(-,root,system)
%{_bindir}/libpng*config
/usr/bin/libpng*config
%{_includedir}/*
/usr/include/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/libpng*.pc
%{_datadir}/man/man3/*

%changelog
* Wed Nov 30 2010 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.2.44-1
 - Update to version 1.2.44

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
