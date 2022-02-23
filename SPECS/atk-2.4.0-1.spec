Summary: Interfaces for accessibility support
Name: 	 atk
Version: 2.4.0
Release: 1
License: LGPLv2+
Group: 	 System Environment/Libraries
Source0: http://download.gnome.org/sources/%{name}/2.4/%{name}-%{version}.tar.gz
URL: 	 http://developer.gnome.org/doc/API/2.0/gtk/gtk-building.html
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: glib2-devel >= 2.31.2
BuildRequires: gettext, pkg-config
Requires: glib2 >= 2.31.2
Requires: gettext

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
The atk-devel package includes the static libraries, header files, and
developer docs for the atk package.

Install atk-devel if you want to develop programs which will use ATK.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export OBJECT_MODE=64

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
CFLAGS="-I/opt/freeware/include -D_LINUX_SOURCE_COMPAT"  \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
LDFLAGS="-L/opt/freeware/lib"  \
./configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --disable-static \
    --disable-gtk-doc \
    --disable-silent-rules
    
make

cp ./atk/.libs/libatk-1.0.so.0 .
cp ./tests/.libs/libtestrelation.so .
cp ./tests/.libs/libteststateset.so .

make distclean


# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
export OBJECT_MODE=32
LIBPATH="%{_libdir}:/usr/lib" \
CFLAGS="-I/opt/freeware/include -D_LINUX_SOURCE_COMPAT"  \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
LDFLAGS="-L/opt/freeware/lib"  \
./configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --disable-static \
    --disable-gtk-doc \
    --disable-silent-rules
make

rm -f ./atk/.libs/libatk-1.a
rm -f ./atk/.libs/libatk-1.0.a
rm -f ./tests/.libs/libtestrelation.a
rm -f ./tests/.libs/libteststateset.a
${AR} -rv ./atk/.libs/libatk-1.a ./atk/.libs/libatk-1.0.so.0 ./libatk-1.0.so.0
${AR} -rv ./atk/.libs/libatk-1.0.a ./atk/.libs/libatk-1.0.so.0 ./libatk-1.0.so.0
${AR} -rv ./tests/.libs/libtestrelation.a ./tests/.libs/libtestrelation.so ./libtestrelation.so
${AR} -rv ./tests/.libs/libteststateset.a ./tests/.libs/libteststateset.so ./libteststateset.so


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
make DESTDIR=$RPM_BUILD_ROOT install

cd ${RPM_BUILD_ROOT}
mkdir -p usr/lib
cd usr/lib
ln -sf ../..%{_prefix}/lib/* .


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc README AUTHORS COPYING NEWS
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
