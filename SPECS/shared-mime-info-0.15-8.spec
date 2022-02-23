%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define pkgconfig_version @pkgconfig_version@

Summary: Shared MIME information database
Name: shared-mime-info
Version: 0.15
Release: 8
License: GPL
Group: System Environment/Libraries
URL: http://freedesktop.org/Software/shared-mime-info
Source0: %{name}-%{version}.tar.bz2

Patch0:		shared-mime-info-0.15-aix.patch
Patch1:		shared-mime-info-0.15-autotools.patch

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
# For intltool:
BuildRequires: perl-XML-Parser >= 2.31-16
Requires: libxml2 glib2

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/shared-mime-info-0.15-aix.patch
$PATCH -p2 -s < %{_sourcedir}/shared-mime-info-0.15-autotools.patch


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
for dir in bin
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%post 
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null


%files
%defattr(-,root,system)
%doc README NEWS shared-mime-info-spec.xml
%{_datadir}/locale/*/LC_MESSAGES/shared-mime-info.mo
%{_bindir}/*
%dir %{_datadir}/mime/
%{_datadir}/mime/packages
%{_libdir}/pkgconfig/*
%{_mandir}/man*/*
/usr/share/*
/usr/bin/*
%changelog
*  Fri Nov 17 2006  BULL
 - Release  8

*  Thu Jul 20 2006  BULL
 - Release  7

*  Tue Nov 15 2005  BULL
 - Release  6

*  Wed Aug 10 2005  BULL
 - Release  5
 - Create symlinks between /usr/share/ and /opt/freeware/share

*  Wed May 25 2005  BULL
 - Release  4

*  Thu Dec 09 2004  BULL
 - Release  3
 - Don't override CFLAGS in build process (fixes bug #2033)

*  Tue Nov 23 2004  BULL
 - Release  2
 - Added the translation files
 - new package for AIX
 - new package for AIX

*  Wed Oct 20 2004  BULL
 - Release  1

