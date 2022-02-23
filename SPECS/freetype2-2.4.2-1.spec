Summary: A free and portable font rendering engine
Name: 	 freetype2
Version: 2.4.2
Release: 1
License: BSD/GPL dual license
Group: 	 System Environment/Libraries
URL: 	 http://www.freetype.org
Source0: http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.gz
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.gz
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.gz
BuildRequires: zlib-devel, coreutils
Requires: zlib
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.


%package demos
Summary: A collection of FreeType demos
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.


%package devel
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel
Requires: pkg-config

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.
Install freetype-devel if you want to develop programs which will use
FreeType.


%prep
%setup -q -n freetype-%{version} -b 1 -a 2


%build
./configure --enable-shared --enable-static \
		--prefix=%{_prefix}
    
make

# Build demos
cd ft2demos-%{version}
make TOP_DIR=".."


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

for file in ftbench ftdiff ftdump ftgamma ftgrid ftlint \
         ftmulti ftstring ftvalid ftview ; do
    builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$file ${RPM_BUILD_ROOT}%{_bindir}
done

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc ChangeLog README
%{_libdir}/libfreetype.a
/usr/lib/libfreetype.a


%files demos
%defattr(-,root,system)
%{_bindir}/ft*
/usr/bin/ft*


%files devel
%defattr(-,root,system)
%{_bindir}/freetype-config
/usr/bin/freetype-config
%{_includedir}/freetype2/freetype/*
%{_includedir}/ft*.h
%{_libdir}/libfreetype.la
/usr/lib/libfreetype.la
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/freetype2.m4


%changelog
* Tue Nov 16 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.2
- Update to version 2.4.2

*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
