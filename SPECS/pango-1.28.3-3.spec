Summary: System for layout and rendering of internationalized text
Name: pango
Version: 1.28.3
Release: 3
License: GNU GPL
Url: 	 http://www.pango.org
Source:  http://ftp.gnome.org/pub/GNOME/sources/pango/1.28/%{name}-%{version}.tar.gz
Patch0:	 pango-1.28.3-aix.patch
Group:   System Environment/Libraries
Buildroot: /var/tmp/%{name}-root
Prefix:  %{_prefix}
BuildRequires: glib2-devel
Requires: glib2

%description 
Pango is a library for laying out and rendering of text, with an emphasis
on internationalization. Pango can be used anywhere that text layout is needed,
though most of the work on Pango so far has been done in the context of the
GTK+ widget toolkit. Pango forms the core of text and font handling for GTK+.

Pango is designed to be modular; the core Pango layout engine can be used
with different font backends.

The integration of Pango with Cairo provides a complete solution with high
quality text handling and graphics rendering.

The library is available as 32-bit and 64-bit

%package devel
Summary: System for layout and rendering of internationalized text
Group: Development/Libraries
Requires: pango = %{version}-%{release}

%description devel
The pango-devel package includes the header files and developer docs
for the pango package.

%prep
%setup -q
%patch0 -p1 -b .aix
#%patch0


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64 -ma"
export CXX="/usr/vacpp/bin/xlC_r -q64 -ma"

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  \
CXXFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
LDFLAGS="-L/opt/freeware/lib" \
./configure  -v \
	--prefix=%{prefix} \
	--mandir=%{_mandir} \
	--enable-shared  --disable-static \
	--with-included-modules=yes

make 

cp ./pango/.libs/libpango-1.0.so.0 .
cp ./pango/.libs/libpangox-1.0.so.0 .
cp ./pango/.libs/libpangoft2-1.0.so.0 .
cp ./pango/.libs/libpangoxft-1.0.so.0 .
cp ./pango/.libs/libpangocairo-1.0.so.0 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r -ma"
export CXX="/usr/vacpp/bin/xlC_r -ma"
LIBPATH="%{_libdir}:/usr/lib" \
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE" \
CXXFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE" \
LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' \
LDFLAGS="-L/opt/freeware/lib" \
./configure \
	--prefix=%{prefix} \
	--mandir=%{_mandir} \
	--enable-shared  --disable-static \
	--with-included-modules=yes

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpango-1.0.a ./libpango-1.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpangox-1.0.a ./libpangox-1.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpangoft2-1.0.a ./libpangoft2-1.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpangoxft-1.0.a ./libpangoxft-1.0.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpangocairo-1.0.a ./libpangocairo-1.0.so.0

mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/usr/lib

(
  cd $RPM_BUILD_ROOT
  for dir in bin lib include
  do
	mkdir -p usr/$dir
	cd usr/$dir
	ln -sf ../..%{prefix}/$dir/* .
	cd -
  done
)


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc README AUTHORS COPYING NEWS
%{_mandir}/man1/*
%{_bindir}/pango*
/usr/bin/pango*
%{_prefix}/etc/pango/pangox.aliases
%{_libdir}/libpango*.a
/usr/lib/libpango*.a

%files devel
%defattr(-,root,system)
%doc %{_datadir}/gtk-doc/html/pango/*
%{_includedir}/pango-1.0/pango/*.h
/usr/include/pango-1.0/pango/*.h
%{_libdir}/libpango*.la
%{_libdir}/pkgconfig/pango*.pc


%changelog
* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.28.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 8 2011 Gerard Visiedo <gerard.visiedo@bull.fnet> 1.28.3-2
- Add libraries 64-bit

* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.28.3-1
- update to version 1.28.3

*  Fri Dec 23 2005  BULL
 - Release 2
 - Prototype gtk 64 bit
*  Tue Nov 15 2005  BULL
 - Release  1
 - New version  version: 1.10.0

*  Wed Aug 10 2005  BULL
 - Release  3

*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 1.8.1
 - Fix Xscreensaver-demo core at initialisation on AIX

*  Tue Nov 23 2004  BULL
 - Release  1
 - New version  version: 1.6.0

*  Wed Jul 28 2004  BULL
 - Release  2
 - fix bug causing the generation of a core file
