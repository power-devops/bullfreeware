%define majver %(echo %version | cut -d. -f1-2)
Name:          libnotify
Version:       0.7.5
Release:       1
Summary:       Desktop notifications library
Group:         System/Libraries
URL:           http://www.gnome.org
Source:        ftp://ftp.gnome.org/pub/gnome/sources/libnotify/%{majver}/libnotify-%{version}.tar.xz
License:       LGPL
BuildRequires: pkgconfig
#BuildRequires: libpopt-devel
## AUTOBUILDREQ-BEGIN
BuildRequires: glib2-devel
BuildRequires: gtk
BuildRequires: gdk-pixbuf-devel
#BuildRequires: libglib-devel
BuildRequires: libpng-devel
#BuildRequires: libselinux-devel
BuildRequires: zlib-devel
## AUTOBUILDREQ-END
Provides:      libnotify07
Obsoletes:     libnotify07
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
A library that sends desktop notifications to a notification daemon, as defined in the Desktop Notifications spec.
These notifications can be used to inform the user about an event or display some form of information without getting in the user's way.

%package devel
Group:         Development/Libraries
Summary:       Static libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Provides:      libnotify07-devel
Obsoletes:     libnotify07-devel

%description devel
A library that sends desktop notifications to a notification daemon, as defined in the Desktop Notifications spec.
These notifications can be used to inform the user about an event or display some form of information without getting in the user's way.

This package contains static libraries and header files need for development.

#%package apidocs
#Summary:       Libnotify API documentation
#Group:         Documentation
##Requires:      gtk-doc
#Provides:      libnotify07-apidocs
#Obsoletes:     libnotify07-apidocs

#%description apidocs
#Libnotify API documentation.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"

CFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT" \
./configure \
	--prefix=%{_prefix}  \
	--enable-shared \
	--disable-gtk-doc

# --enable-gtk-doc warning: failed to load external entity "http://docbook.sourceforge.net/release/xsl/current/html/chunk.xsl"
make
cp ./libnotify/.libs/libnotify.so.4 .
mv ./tools/notify-send ./notify-send_64

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"

CFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT" \
./configure \
        --prefix=%{_prefix}  \
        --enable-shared \
        --disable-gtk-doc
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ./libnotify/.libs/%{name}.a ./%{name}.so.4

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export RM="/usr/bin/rm -f"
make install DESTDIR=${RPM_BUILD_ROOT}

cp ./notify-send_64 ${RPM_BUILD_ROOT}%{_bindir}

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
     mkdir -p usr/${dir}
     cd usr/${dir}
     ln -sf ../..%{_prefix}/${dir}/* .
     cd -
  done
  mkdir -p usr/include/libnotify
  cd usr/include/libnotify
  ln -sf ../../..%{_prefix}/include/libnotify/* .
  cd -
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS
%{_bindir}/notify-send*
%{_libdir}/libnotify.a
/usr/bin/*
/usr/lib/%{name}.a

%files devel
%defattr(-,root,system)
%{_includedir}/%{name}/
/usr/include/%{name}/
%{_libdir}/%{name}.la
/usr/lib/%{name}.la
%{_libdir}/pkgconfig/libnotify.pc
#%{_libdir}/girepository-1.0/Notify-0.7.typelib
#%{_datadir}/gir-1.0/Notify-0.7.gir

#%files apidocs
#%defattr(-,root,system)
#%{_datadir}/gtk-doc/html/%{name}/

%changelog
* Wed Apr 17 2013 Gerard Visiedo <gerard.visiedo@bull.net> 0.7.5-1
- Initial port on Aix6.1
