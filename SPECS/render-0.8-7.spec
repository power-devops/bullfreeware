%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Name: 		render
Version: 	0.8
Release: 	8
Group: 		X11/Development/Libraries
Summary: 	X Render Extension
License:	MIT
URL: 		http://fontconfig.org/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Source:         http:///%{name}-%{version}.tar.bz2

Patch0:		render-0.8-aix.patch


%description
This package contains header files and documentation for the X render
extension.  Library and server implementations are separate.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/render-0.8-aix.patch


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
for dir in bin lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr (-,root,system)
%doc README library protocol
%{_includedir}/X11
%{_libdir}/pkgconfig/*
%{_datadir}/doc/render
/usr/share
%changelog
*  Fri Nov 17 2006  BULL
 - Release  8
 - gnome 2.16.1

*  Thu Nov 17 2005  BULL
 - Release  7
*  Tue Aug 09 2005  BULL
 - Release  6
 - Create symlinks between /usr/share and /opt/freeware/share

*  Wed May 25 2005  BULL
 - Release  5

*  Tue Nov 24 2004  BULL
 - Release  4
