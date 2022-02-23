# rpm -ba --define 'dotests 0' atk-2.20.0-1.spec ...
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: Interfaces for accessibility support
Name: 	 atk
Version: 2.20.0
Release: 2
License: LGPLv2+
Group: 	 System Environment/Libraries
URL: 	 http://developer.gnome.org/doc/API/2.0/gtk/gtk-building.html

Source0: http://download.gnome.org/sources/atk/2.20/%{name}-%{version}.tar.xz
Source1: http://download.gnome.org/sources/atk/2.20/%{name}-%{version}.sha256sum

BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: glib2-devel >= 2.31.2
BuildRequires: gettext, pkg-config
# BuildRequires: gobject-introspection-devel >= 0.9.6

Requires: glib2 >= 2.31.2
Requires: gettext

%define         _libdir64 %{_prefix}/lib64

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.


%package devel
Summary: Files necessary to develop applications using ATK
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel >= 2.31.2
Requires: pkg-config

%description devel
The atk-devel package includes libraries, header files, and
developer documentation needed for development of applications
or toolkits which use ATK.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# first build the 64-bit version
cd 64bit

# Not needed   - LDFLAGS='-L/opt/freeware/lib'
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=64

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
CFLAGS="-I/opt/freeware/include -D_LINUX_SOURCE_COMPAT"  \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared \
    --disable-static \
    --disable-gtk-doc \
    --disable-silent-rules
    
gmake

if [ "%{DO_TESTS}" == 1 ]
then
	cd tests
	./testdocument
	./testrelation
	./testrole
	./teststateset
	./testvalue
	cd ..
	/usr/sbin/slibclean
fi


# now build the 32-bit version
cd ../32bit

# Not needed   - LDFLAGS='-L/opt/freeware/lib'
export CC="/usr/vac/bin/xlc"
export OBJECT_MODE=32

LIBPATH="%{_libdir}:/usr/lib" \
CFLAGS="-I/opt/freeware/include -D_LINUX_SOURCE_COMPAT"  \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --disable-static \
    --disable-gtk-doc \
    --disable-silent-rules

gmake

if [ "%{DO_TESTS}" == 1 ]
then
	cd tests
	./testdocument
	./testrelation
	./testrole
	./teststateset
	./testvalue
	cd ..
	/usr/sbin/slibclean
fi


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=$RPM_BUILD_ROOT install


export OBJECT_MODE=32
cd ../32bit
gmake DESTDIR=$RPM_BUILD_ROOT install


cd ${RPM_BUILD_ROOT}
mkdir -p usr/lib
cd usr/lib
ln -sf ../..%{_prefix}/lib/* .


cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir64}/lib*.a ; do
    /usr/bin/ar -X64 -x ${f}
    ls -l
done
cd -

# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libatk-1.0.a  ${RPM_BUILD_ROOT}%{_libdir64}/libatk-1.0.so.0


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc 32bit/README 32bit/AUTHORS 32bit/COPYING 32bit/NEWS
%{_libdir}/libatk*.a
/usr/lib/libatk*.a
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-,root,system)
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_includedir}/atk-1.0/atk/*.h
/usr/lib/*.la


%changelog
* Thu Apr 28 2016 Tony Reix <tony.reix@bull.net> - 2.20.0-2
- Change 32/64bits management

* Mon Apr 11 2016 Michael Wilson <michael.wilson@bull.net> - 2.20.0-1
- Update to version 2.20.0

* Thu Jun 21 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.0-1
- Update to version 2.4.0

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.32.0-3
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.32.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Sep 09 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.32.0-1
- Add 64bit libraries

* Mon Nov 08 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.32
- Update to version 1.32.0
