%define _prefix /opt/freeware

Summary: Library of Optimized Inner Loops, CPU optimized functions
Name: liboil
Version: 0.3.8
Release: 1
License: LGPL
Group: System Environment/Libraries
URL: http://liboil.freedesktop.org/
Source: http://liboil.freedesktop.org/download/liboil-%{version}.tar.bz2

Patch0:		liboil-0.3.8-aix.patch
Patch1:		liboil-0.3.8-autotools.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: glib2-devel

%description
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).


%package devel
Summary: Development files and static library for liboil
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Liboil is a library of simple functions that are optimized for various CPUs.
These functions are generally loops implementing simple algorithms, such as
converting an array of N integers to floating-poing numbers or multiplying
and summing an array of N numbers. Clearly such functions are candidates for
significant optimization using various techniques, especially by using
extended instructions provided by modern CPUs (Altivec, MMX, SSE, etc.).


%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/liboil-0.3.8-aix.patch
$PATCH -p2 -s < %{_sourcedir}/liboil-0.3.8-autotools.patch




%build
%configure
# multi-jobbed make makes the build fail:
# ./build_prototypes_doc >liboilfuncs-doc.h
# /bin/sh: ./build_prototypes_doc: No such file or directory
# %{__make} %{?_smp_mflags}
%make


%install
if test "%{buildroot}" != "/"; then
        rm -rf  %{buildroot}
fi
%makeinstall

# Make the links
cd %{buildroot}
for dir in lib include share
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README README-XPDF TODO
%{_libdir}/*.a
/usr/lib

%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/html/liboil/
/usr/bin
/usr/include
/usr/lib
/usr/share
%changelog
*  Tue Apr 25 2006  BULL
 - Release  1
 - New version  version: 0.3.8
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - gnome 2.14 merge
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - add new module liboil
 - gnome 2.14 merge

