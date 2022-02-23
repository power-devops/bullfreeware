%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Name: 		xrender
Version: 	0.8.4
Release: 	9
Group: 		X11/Libraries
Summary: 	X Render Extension
License: 	MIT
URL: 		http://freedesktop.org/Software/xlibs/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Source:         http:///%{name}-%{version}.tar.bz2

Patch0:		xrender-0.8.4-aix.patch


%description
X11 resize and rotate extension library.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/xrender-0.8.4-aix.patch


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
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_prefix}/64/lib/lib*.a
/usr/lib/lib*.a
/usr/lib/lib*.la
%{_includedir}/X11
%changelog
*  Fri Nov 17 2006  BULL
 - Release  9
 - gnome 2.16.1

*  Wed Jul 26 2006  BULL
 - Release  8

*  Mon Feb 13 2006  BULL
 - Release 7 - support 64 bit - build with type CARD32 = unsigned int 
 - Prototype gtk 64 bit
*  Fri Dec 23 2005  BULL
 - Release 6
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  5

*  Wed May 25 2005  BULL
 - Release  4

*  Tue Nov 24 2004  BULL
 - Release  3
*  Thu Sep 30 2004  BULL
 - Release  2
 - Removed the link "/usr/include/X11" which was overwriting a system link

