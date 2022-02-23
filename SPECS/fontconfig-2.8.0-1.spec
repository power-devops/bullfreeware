%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define freetype_version 2.0.9

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.8.0
Release:	1
License:	MIT
Group:		System Environment/Libraries
Source:		http://cgit.freedesktop.org/fontconfig/snapshot/fontconfig-2.8.0.tar.gz
URL:		http://fontconfig.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
PreReq:		freetype2 >= %{freetype_version}
BuildRequires:	freetype2-devel >= %{freetype_version}

%description
Fontconfig is designed to locate fonts within the system and select them
according to requirements specified by applications.

%package devel
Summary:	Font configuration and customization library
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	freetype2-devel >= %{freetype_version}

%description devel
The fontconfig-devel package includes the header files, and developer docs
for the fontconfig package.
Install fontconfig-devel if you want to develop programs which will use
fontconfig.

%prep
%setup -q

%build
./configure     --enable-shared --disable-static --prefix=%{_prefix}
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


%post
# Force regeneration of all fontconfig cache files.
%{_bindir}/fc-cache -f >/dev/null 2>&1

%files
%defattr(-, root, system)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.a
/usr/lib/libfontconfig.a
%{_bindir}/fc*
/usr/bin/fc*
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
/opt/freeware/etc/fonts/*

%files devel
%defattr(-, root, system)
%{_libdir}/*.la
/usr/lib/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig/*.h
/usr/include/*
%{_datadir}/doc/fontconfig*
%{_datadir}/man/man3/*

%changelog
*  Wed Nov 26 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.8.0-1
 - Update to version 2.8.0

*  Wed Nov 15 2006  BULL
 - Release 7 
 - gnome 2.16.1

*  Tue Sep 19 2006  BULL
 - Release 6
 - support 64 bit
*  Fri Dec 23 2005  BULL
 - Release 5
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  4
*  Mon May 30 2005  BULL
 - Release  3
 - .o removed from lib
*  Fri Sep 24 2004  BULL
 - Release  2
 - Package the directories /opt/freeware/etc/fonts, /opt/freeware/include/fontconfig and /usr/include/fontconfig along with their contents

