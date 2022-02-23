%define _prefix /opt/freeware

Summary: 	X Cursor library
Name: 		xcursor
Version: 	1.0.2
Release: 	4
Source: 	%{name}-%{version}.tar.bz2

Patch0:		xcursor-1.0.2-aix.patch
Patch1:		xcursor-1.0.2-autotools.patch

License: 	MIT
Group:		X11/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Obsoletes:	xcursor-static

BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	libtool
#BuildRequires:	pkgconfig
#BuildRequires:	xrender-devel

%description
X Cursor library.

%package devel
Summary:	X Cursor library headers
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
#Requires:	xrender-devel
Obsoletes:	xcursor-static

%description devel
X Cursor library headers.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/xcursor-1.0.2-aix.patch
$PATCH -p2 -s < %{_sourcedir}/xcursor-1.0.2-autotools.patch


%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
PATH=%{_bindir}:$PATH ./configure --prefix=%{_prefix} --disable-static
PATH=%{_bindir}:$PATH make

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} install-strip

# Make the links
cd %{buildroot}
for dir in bin share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libXcursor.a
%{_prefix}/64/lib/libXcursor.a

/usr/lib

%files devel
%defattr(-,root,system)
#%attr(755,root,root) %{_libdir}/libXcursor.a
#%{_libdir}/libXcursor.la
#%{_includedir}/X11/Xcursor
#%{_pkgconfigdir}/xcursor.pc
#%{_mandir}/man3/Xcursor.3*

#/usr/include
#/usr/share
#/usr/lib
%changelog
*  Wed Jul 26 2006  BULL
 - Release  4

*  Thu Jan 19 2006  BULL
 - Release  3
 - Library contain both 32 and 64 bit members
*  Tue Nov 15 2005  BULL
 - Release  2

*  Fri Nov 04 2005  BULL
 - Release  1
 - New version  version: 1.0.2

