%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define pkgconfig_version 0.19

Summary: 	A library for accessing various audio file formats.
Name: 		audiofile
Version: 	0.2.6
Release: 	5
License: 	LGPL
Group:	 	System Environment/Libraries
Source: 	ftp://oss.sgi.com/projects/download/audiofile-%{version}.tar.bz2

Patch0:		audiofile-0.2.6-aix.patch
Patch1:		audiofile-0.2.6-autotools.patch

URL: 		http://oss.sgi.com/projects/audofile/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%description
The Audio File library is an implementation of SGI's Audio File
Library, which provides an API for accessing audio file formats like
AIFF/AIFF-C, WAVE, and NeXT/Sun .snd/.au files. This library is used
by the EsounD daemon.

Install audiofile if you are installing EsounD or you need an API for
any of the sound file formats it can handle.

%package devel
Summary: Development files for Audio File applications.
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkg-config >= %{pkgconfig_version} 

%description devel
The audiofile-devel package contains libraries, include files, and
other resources you can use to develop Audio File applications.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/audiofile-0.2.6-aix.patch
$PATCH -p2 -s < %{_sourcedir}/audiofile-0.2.6-autotools.patch


%build
./configure --prefix=%{_prefix}
make

%install

if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install

# make links
cd %{buildroot}
for dir in bin lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-, root, system)
%doc COPYING TODO README ChangeLog docs
%{_bindir}/sfconvert
%{_bindir}/sfinfo
%{_libdir}/lib*.a
/usr/bin
/usr/lib

%files devel
%defattr(-, root, system)
%{_bindir}/audiofile-config
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/aclocal/*
/usr/bin
/usr/lib
/usr/include
/usr/share

%changelog
*  Wed Nov 15 2006  BULL
 - Release  5
 - Added support 64 bit
 - gnome 2.16.1

*  Tue Nov 15 2005  BULL
 - Release  4

*  Tue Aug 09 2005  BULL
 - Release  3
 - Create symlinks between /usr/share and /opt/freeware/share

*  Wed May 11 2005  BULL
 - Release  1
 - New version  version: 0.2.6
 - merged with 2.8.1

