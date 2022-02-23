Name:           dbus-1-glib
Url:            http://dbus.freedesktop.org/
Version:        0.98
Release:        1
Summary:        GLib-based library for using D-Bus
License:        AFL-2.1 or GPL-2.0+
Group:          Development/Libraries/Other
Source0:        http://dbus.freedesktop.org/releases/dbus-glib/dbus-glib-%{version}.tar.gz
#Source1:        baselibs.conf
BuildRequires:  dbus-1-devel
BuildRequires:  glib2-devel
BuildRequires:  expat-devel
#BuildRequires:  libselinux-devel
Requires:       dbus-1
## bug437293
#%ifarch ppc64
#Obsoletes:      dbus-1-glib-64bit
#%endif
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%package -n dbus-1-glib-devel
Summary:        Developer package for D-Bus/GLib bindings
Group:          Development/Libraries/Other
Requires:       dbus-1-glib = %{version}
Requires:       glib2-devel
Requires:       dbus-1-devel

#%package -n dbus-1-glib-doc
#Summary:        Documentation for the D-Bus/GLib bindings
#Group:          Documentation/HTML
##%if 0%{?suse_version} >= 1120
##BuildArch:      noarch
##%endif

%description
D-Bus add-on library to integrate the standard D-Bus library with the
GLib thread abstraction and main loop.

%description -n dbus-1-glib-devel
D-Bus add-on library to integrate the standard D-Bus library with the
GLib thread abstraction and main loop.

#%description -n dbus-1-glib-doc
#D-Bus add-on library to integrate the standard D-Bus library with the
#GLib thread abstraction and main loop.

%prep
%setup -n dbus-glib-%{version} -q

%build
#export CFLAGS="${RPM_OPT_FLAGS} -fstack-protector -fPIC"

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vac/bin/xlC_r -q64"

CFLAGS="-D_LARGE_FILE -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILE -D_LARGEFILE_SOURCE" \
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules \
    --libexecdir=%{_libexecdir}/%{name}	\
    --disable-static \
    --enable-sharerd
make

cp ./dbus/.libs/libdbus-glib-1.so.2 .
cp ./dbus/.libs/libdbus-gtool.a .

make distclean


# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vac/bin/xlC_r"
 
CFLAGS="-D_LARGE_FILE -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILE -D_LARGEFILE_SOURCE" \
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules \
    --libexecdir=%{_libexecdir}/%{name}	\
    --disable-static \
    --enable-sharerd
make

slibclean

${AR} -q ./dbus/.libs/libdbus-glib-1.a ./libdbus-glib-1.so.2
mkdir tmp
cd tmp
ar -X64 -t ../libdbus-gtool.a > listobj64
ar -X64 -x ../libdbus-gtool.a
for file in $(cat listobj64); do
    ar -X32_64 -q ../dbus/.libs/libdbus-gtool.a ${file}
done


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cp ${RPM_BUILD_DIR}/dbus-glib-%{version}/dbus/.libs/libdbus-glib-1.so.2 ${RPM_BUILD_ROOT}%{_libdir}
cp ${RPM_BUILD_DIR}/dbus-glib-%{version}/dbus/.libs/libdbus-gtool.a ${RPM_BUILD_ROOT}%{_libdir}
cp ${RPM_BUILD_DIR}/dbus-glib-%{version}/dbus/libdbus-gtool.la ${RPM_BUILD_ROOT}%{_libdir}

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p  usr/include/dbus-1.0/dbus
  cd  usr/include/dbus-1.0/dbus
  ln -sf ../../../..%{_prefix}/include/dbus-1.0/dbus/* .
)

%post
#%{run_ldconfig}

%postun
#%{run_ldconfig}

%files 
%defattr(-, root, system)
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
%{_libexecdir}/%{name}
/usr/lib/*.a
/usr/lib/*.so*

%files -n dbus-1-glib-devel
%defattr(-, root, system)
%{_bindir}/dbus-binding-tool
%{_datadir}/man/man?/dbus-binding-tool.*
%{_includedir}/dbus-1.0/dbus/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/dbus-glib-1.pc
/usr/bin/*
/usr/lib/*.la
/usr/include/dbus-1.0/dbus/*

#%files -n dbus-1-glib-doc
#%defattr(-, root, system)
#%dir %{_datadir}/gtk-doc/
#%dir %{_datadir}/gtk-doc/html
#%{_datadir}/gtk-doc/html/dbus-glib

%changelog
* Fri Jul 13 2012 Gerard Visiedo <gerard.visiedo@bull.net> -0.98-1
- Inital port on Aix6.1
