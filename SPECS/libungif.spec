%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define LIBVER 4.1.0
%define LIBVERS 4
%define DEFCC cc

Summary: A library for manipulating GIF format image files.
Name: libungif
Version: 4.1.2
Release: 3
License: MIT
URL:	 http://sourceforge.net/projects/libungif/
Source0: http://sourceforge.net/projects/libungif/%{name}-%{version}.tar.bz2

Patch0:		libungif-4.1.2-aix.patch
Patch1:		libungif-4.1.2-autotools.patch

Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}

%description
The libungif package contains a shared library of functions for loading and
saving GIF format image files.  The libungif library can load any GIF file, but
it will save GIFs only in uncompressed format (i.e., it won't use the patented
LZW compression used to save "normal" compressed GIF files).

Install the libungif package if you need to manipulate GIF files.  You
should also install the libungif-progs package.

%package devel
Summary: Development tools for programs which will use the libungif library.
Group: Development/Libraries
%description devel
This package contains the static libraries, header files and documentation
necessary for development of programs that will use the libungif library to
load and save GIF format image files.
You'll also need to install the libungif package.

%package progs
Summary: Programs for manipulating GIF format image files.
Group: Applications/Multimedia
%description progs
The libungif-progs package contains various programs for manipulating GIF
format image files.  You'll also need to install the libungif package.

%prep
%setup -q 

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/libungif-4.1.2-aix.patch
$PATCH -p2 -s < %{_sourcedir}/libungif-4.1.2-autotools.patch


%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       %define optflags -O2
    else 
       export CC=gcc
    fi
fi

%configure --disable-static
make all

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
make DESTDIR=${RPM_BUILD_ROOT} install
{
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/lib || :
  mkdir -p usr/include || :
  mkdir -p usr/bin || :
  cd usr/lib
  ln -sf ../..%{_prefix}/lib/* .
  cd ../include
  ln -sf ../../%{_prefix}/include/* .
  cd ../bin
  ln -sf ../../%{_prefix}/bin/* .
}

/usr/bin/strip ${RPM_BUILD_ROOT}%{prefix}/bin/* || :

%files 
%defattr(-,root,system)
%doc COPYING README UNCOMPRESSED_GIF NEWS ONEWS
/usr/lib/*
%{_prefix}/lib/*

%files devel
%defattr(-,root,system)
%doc doc/*
%doc util/giffiltr.c
%doc util/gifspnge.c
/usr/include/*.h
%{_prefix}/include/*.h

%files progs
%defattr(-,root,system)
%{_prefix}/bin/*
/usr/bin/*
%changelog
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005 BULL
 - Release  1
 - New version  version: 4.1.2
