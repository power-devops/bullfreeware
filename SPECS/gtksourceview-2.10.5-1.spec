Summary: Source code viewer
Name: gtksourceview
Version: 2.10.5
Release: 1
License: GPL
Group: Applications/Editors
URL: http://gtksourceview.sourceforge.net/

Source: http://ftp.gnome.org/pub/GNOME/sources/gtksourceview/2.10/gtksourceview-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root
#BuildRequires: gcc-c++, intltool, perl-XML-Parser, gtk2-devel
#BuildRequires: pkgconfig, libxml2-devel, libgnomeprint22
#BuildRequires: libgnomeprint22-devel, gnome-vfs2-devel, libgnomeprintui22-devel

%define _libdir64 %{_prefix}/lib64

%description
GtkSourceView is a text widget that extends the standard gtk+ 2.x
text widget GtkTextView.
It improves GtkTextView by implementing syntax highlighting and other
features typical of a source editor.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"


CFLAGS="-D_LINUX_SOURCE_COMPAT -I/opt/freeware/include -I/usr/include" \
LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib" \
./configure \
	--prefix=%{_prefix} \
 	--disable-silent-rules \
	--mandir=%{_mandir} \
	--disable-static \
	--enable-shared

make

cp ./%{name}/.libs/lib%{name}-2.0.so.0 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

CFLAGS="-D_LINUX_SOURCE_COMPAT -I/opt/freeware/include -I/usr/include" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
./configure \
        --prefix=%{_prefix} \
        --disable-silent-rules \
        --mandir=%{_mandir} \
        --disable-static \
        --enable-shared

make


%install
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

# Clean up buildroot
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* ||

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-2.0.a ./lib%{name}-2.0.so.0

# Extract dynamic .so X32 librairies
cd ${RPM_BUILD_ROOT}%{_libdir}
for f in lib*.a ; do
    ar -X32 -x ${f}
done
#

for f in lib*.so* ; do
    ln -s ${f} $(basename ${f} .0)
done

# Extract dynamic .so X64 librairies
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.a ; do
    ar -X64 -x ${f}
done
for f in lib*.so* ; do
    ln -s ${f} $(basename ${f} .0)
done


(
  cd ${RPM_BUILD_ROOT}
  for dir in lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  
  cd ${RPM_BUILD_ROOT}
  mkdir -p usr/include/%{name}-2.0/%{name}
  cd usr/include/%{name}-2.0/%{name}
  ln -sf ../../../..%{_prefix}/include/%{name}-2.0/%{name}/* .
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


#%files -f %{name}-2.0.lang
%files
%defattr(-, root, system, 0755)
%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_datadir}/%{name}-2.0/
%{_datadir}/locale/*/LC_MESSAGES/*.mo
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*

%files devel
%defattr(-, root, system, 0755)
%doc HACKING
%doc %{_datadir}/gtk-doc/html/%{name}-2.0/
%{_includedir}/%{name}-2.0/
/usr/include/%{name}-2.0/
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jul 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.10.5-1
- First port on Aix6.1 

