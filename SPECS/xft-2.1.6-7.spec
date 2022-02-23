%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Name: 		xft
Version: 	2.1.6
Release: 	7
Group: 		X11/Libraries
Summary: 	X Font Rendering library
License: 	MIT
URL: 		http://fontconfig.org/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Source:         http:///%{name}-%{version}.tar.bz2

Patch0:		xft-2.1.6-aix.patch


%description

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/xft-2.1.6-aix.patch


%build
./configure --prefix=%{_prefix}
make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
%{_make} INSTALL_PATH=%{buildroot}%{_prefix} install-dtd
PATH=%{_bindir}:$PATH DATADIR=%{buildroot}%{_datadir}/xml/ \
SYSCONFDIR=%{buildroot}%{_sysconfdir}/xml/ ./buildDocBookCatalog

# Make the links
cd %{buildroot}
for dir in bin lib include
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr (-,root,system)
%{_bindir}/xft-config
/usr/bin/xft-config
%{_libdir}/pkgconfig/*
%{_libdir}/lib*a
%{_prefix}/64/lib/lib*.a
/usr/lib/lib*.a
%{_includedir}/X11/*
/usr/include/X11/*
%{_mandir}/man3/*
%changelog
*  Fri Nov 17 2006  BULL
 - Release  7
 - gnome 2.16.1

*  Wed Jul 26 2006  BULL
 - Release  6

*  Fri Dec 23 2005  BULL
 - Release 5
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  4

*  Wed May 25 2005  BULL
 - Release  3

*  Tue Nov 24 2004  BULL
 - Release  2
