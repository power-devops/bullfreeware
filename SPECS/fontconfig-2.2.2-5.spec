%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define freetype_version 2.0.9

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.2.2
Release:	5
License:	MIT
Group:		System Environment/Libraries

Patch0:		fontconfig-2.2.2-aix.patch
Patch1:		fontconfig-2.2.2-autotools.patch

URL:		http://fontconfig.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Source:		%{name}-%{version}.tar.bz2
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

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/fontconfig-2.2.2-aix.patch
$PATCH -p2 -s < %{_sourcedir}/fontconfig-2.2.2-autotools.patch


%build
./configure --prefix=%{_prefix}
make

%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install

%post
# Force regeneration of all fontconfig cache files.
%{_bindir}/fc-cache -f >/dev/null 2>&1
# Prototype support gtk 64 bit
mkdir -p /opt/freeware/64/lib
cd /opt/freeware/64/lib
ln -sf /opt/freeware/lib/libfontconfig.a .

%files
%defattr(-, root, system)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.a
%{_bindir}/fc-cache
%{_bindir}/fc-list
%{_sysconfdir}/fonts
/usr/bin/fc-cache
/usr/bin/fc-list
/usr/lib/libfontconfig.a

%files devel
%defattr(-, root, system)
%{_libdir}/libfontconfig.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/fontconfig
%{_mandir}/man1/*
%{_mandir}/man3/*
/usr/include/fontconfig

%changelog
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

