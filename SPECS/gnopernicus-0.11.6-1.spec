%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

%define cspi_version 1.6.6
%define GConf_version 2.12.0
%define gtk2_version 2.8.3
%define libglade_version 2.5.1
%define libgnome_version 2.12.0.1
%define libgnomeui_version 2.12.0
%define libxml_version 2.6.21
%define gnome_speech_version 0.3.7
%define gnome_mag_version 0.12.1

Summary:        gnopernicus
Name:           gnopernicus
Version:        0.11.6
Release:        1
URL:            http://www.gnome.org
Source:         %{name}-%{version}.tar.bz2

Patch0:		gnopernicus-0.11.6-aix.patch
Patch1:		gnopernicus-0.11.6-autotools.patch

License:        GPL
Group:          Gnome2/Accessibility
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       at-spi >= %{cspi_version}
Requires:       GConf2 >= %{GConf_version}
Requires:       gtk2 >= %{gtk2_version}
Requires:       libglade2 >= %{libglade_version}
Requires:       libgnome >= %{libgnome_version}
Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       libxml2 >= %{libxml_version}
Requires:       gnome-speech  >= %{gnome_speech_version}
Requires:       gnome-mag >= %{gnome_mag_version}

%description
gnopernicus

%package devel
Summary:	Development tools.
Group:          Gnome2/Accessibility
Requires:	gnopernicus = %{version}

%description devel
Lib for development

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/gnopernicus-0.11.6-aix.patch
$PATCH -p2 -s < %{_sourcedir}/gnopernicus-0.11.6-autotools.patch

chmod +x configure
chmod +x install-sh
chmod +x mkinstalldirs

%build
LDFLAGS=-L%{_libdir} CPPFLAGS=-I%{_includedir} PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix}
make

%install
if test "%{buildroot}" != "/"; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# Make the links
cd %{buildroot}
for dir in bin include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/gnopernicus-1.0/*.a
%{_libexecdir}/brlmonitor
%{_bindir}/*
%{_datadir}/gnopernicus
%{_datadir}/applications
%{_datadir}/gnome/help
%{_datadir}/omf/gnopernicus
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/pixmaps/*png
%{_sysconfdir}/gconf/schemas
%{_sysconfdir}/gnopernicus-1.0/translation_tables

/usr/bin/*
/usr/share

%files devel
%defattr(-, root, system)
%{_libdir}/gnopernicus-1.0/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnopernicus-1.0

/usr/include/*

%changelog
*  Wed Nov 16 2005  BULL
 - Release  1
 - New version  version: 0.11.6

*  Tue Aug 09 2005  BULL
 - Release  4
 - Create symlinks between /usr/share and /opt/freeware/share

*  Wed Jun 08 2005  BULL
 - Release 3
 - Fix speech pb on AIX
*  Tue Jun 07 2005  BULL
 - Release  2
 - wrong version
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 0.10.4

*  Mon Mar 14 2005  BULL
 - Release  2
 - Fix rate problem on AIX.
 - fix problem of srcore speech on AIX with a driver that support callbakcs.

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 0.9.16

