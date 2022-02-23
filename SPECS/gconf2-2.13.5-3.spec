%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define libxml2_version 2.6.23
%define orbit2_version 2.14.0
%define glib2_version 2.10.1
%define popt_version 1.7
%define gtk_doc_version 1.5
%define pkgconfig_version @pkgconfig_version@

Summary: 	A process-transparent configuration system
Name: 		GConf2
Version: 	2.13.5
Release: 	3
License: 	LGPL
Group: 		System Environment/Base
Source: 	ftp://ftp.gnome.org/pub/GNOME/unstable/sources/GConf/GConf-%{version}.tar.bz2

Patch0:		GConf-2.13.5-aix.patch
Patch1:		GConf-2.13.5-autotools.patch

BuildRoot: 	%{_tmppath}/GConf2-%{version}-root
URL: 		http://www.gnome.org

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: ORBit2-devel >= %{orbit2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk-doc >= %{gtk_doc_version} 
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: libtool, autoconf

Prereq: /sbin/install-info
PreReq: glib2 >= %{glib2_version}
PreReq: libxml2 >= %{libxml2_version}
PreReq: popt >= %{popt_version}

%description
GConf is a process-transparent configuration database API used to 
store user preferences. It has pluggable backends and features to 
support workgroup administration.

%package devel
Summary: Headers and libraries for GConf development
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: libxml2-devel >= %{libxml2_version}
Requires: ORBit2-devel >= %{orbit2_version}
Requires: glib2-devel >= %{glib2_version}

%description devel
GConf development package. Contains files needed for doing
development using GConf.

%prep
%setup -q -n GConf-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/GConf-2.13.5-aix.patch
$PATCH -p2 -s < %{_sourcedir}/GConf-2.13.5-autotools.patch


# work around glib-gettextize bug affecting tarball
perl -pi -e 's/-lintl//g' aclocal.m4

%build
CPPFLAGS="-I%{_includedir}" LDFLAGS="-L%{_libdir}" \
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix} --disable-gtk-doc
PATH=%{_bindir}:$PATH make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
PATH=%{_bindir}:$PATH make DESTDIR=%{buildroot} install-strip

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
#%defattr(-, root, root)
%defattr(-, root, system)
%doc COPYING ChangeLog NEWS README
%config %{_sysconfdir}/gconf/2/path
%dir %{_prefix}/etc/gconf/gconf.xml.defaults
%dir %{_prefix}/etc/gconf/gconf.xml.mandatory
%{_bindir}/*
/usr/bin/*
%{_libexecdir}/*
%{_libdir}/*.a
 %{_prefix}/64/lib/*.a
/usr/lib/*.a
%{_libdir}/GConf/2/*a
%dir %{_libdir}/GConf
%dir %{_libdir}/GConf/2
%{_datadir}/locale/*/LC_MESSAGES/GConf2.mo
%{_datadir}/sgml
%{_mandir}/man1/*
/usr/share

%files devel
%defattr(-, root, system)
%{_includedir}/gconf
/usr/include/*
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.la
/usr/share
%changelog
*  Fri Sep 15 2006  BULL
 - Release  3
 - added support 64 bits

*  Wed Jul 19 2006  BULL
 - Release  2
 - built with ORBit 2.14

*  Wed Jul 10 2006  BULL
 - Release  1
 - New version  version: 2.13.5

*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 2.12.0

*  Tue Aug 09 2005  BULL
 - Release  3
 - Create symlinks between /usr/share and /opt/freeware/share

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 2.10.0

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 2.8.1

