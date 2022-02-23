%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define pkgconfig_version @pkgconfig_version@

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: Shared MIME information database
Name: shared-mime-info
Version: 1.6
Release: 1
License: GPL
Group: System Environment/Libraries
URL: http://freedesktop.org/Software/shared-mime-info
Source0: %{name}-%{version}.tar.xz

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  libxml2-devel
BuildRequires:  glib2-devel
BuildRequires:  intltool >= 0.35
# For intltool:
#BuildRequires: perl-XML-Parser >= 2.31-16
# perl-XML-Parser does not exists on Bull Freeware, it must be
# downloaded from http://search.cpan.org/~msergeant/XML-Parser-2.36/Parser.pm
Requires: libxml2 glib2

%description
This is the freedesktop.org shared MIME info database.

Many programs and desktops use the MIME system to represent the types of
files. Frequently, it is necessary to work out the correct MIME type for
a file. This is generally done by examining the file's name or contents,
and looking up the correct MIME type in a database.

%prep
# need tar from /opt/freeware to handle tar.xz archive
export PATH=/opt/freeware/bin:$PATH
%setup -q

%build
export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

export LDFLAGS=""
export CFLAGS="-g -O2"

export OBJECT_MODE=32

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}/%{_libdir}/pkgconfig
mv %{buildroot}/%{_prefix}/share/pkgconfig/* %{buildroot}/%{_libdir}/pkgconfig

mkdir -p %{buildroot}/usr/share
ln -sf ../..%{_prefix}/share/mime %{buildroot}/usr/share/mime

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

%changelog
* Wed Jun 08 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.6
- Update to 1.6

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

