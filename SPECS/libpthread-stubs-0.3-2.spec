Name:          libpthread-stubs
Version:       0.3
Release:       2
Summary:       This library provides weak aliases for pthread functions not provided in libc
Group:         System/Libraries
URL:           http://xcb.freedesktop.org
Source:        http://xcb.freedesktop.org/dist/libpthread-stubs-%{version}.tar.gz
License:       MIT
BuildRoot:     /var/tmp/%{name}-%{version}-root

%description
This library provides weak aliases for pthread functions not provided in libc or otherwise available by default.
Libraries like libxcb rely on pthread stubs to use pthreads optionally, becoming thread-safe when linked to libpthread, while avoiding any performance hit when running single-threaded. libpthread-stubs supports this behavior even on platforms which do not supply all the necessary pthread stubs.
On platforms which already supply all the necessary pthread stubs, this package ships only the pkg-config file pthread-stubs.pc, to allow libraries to unconditionally express a dependency on pthread-stubs and still obtain correct behavior.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%description devel
This library provides weak aliases for pthread functions not provided in libc or otherwise available by default.  
Libraries like libxcb rely on pthread stubs to use pthreads optionally, becoming thread-safe when linked to libpthread, while avoiding any performance hit when running single-threaded. libpthread-stubs supports this behavior even on platforms which do not supply all the necessary pthread stubs.
On platforms which already supply all the necessary pthread stubs, this package ships only the pkg-config file pthread-stubs.pc, to allow libraries to unconditionally express a dependency on pthread-stubs and still obtain correct behavior.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc -q64 -bexpall"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure --prefix=%{_prefix}
make


[ -d 64bits ] || mkdir 64bits
cp .libs/libpthread-stubs.so.0 64bits
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc -bexpall"
./configure --prefix=%{_prefix}
make

# doesn't work ${AR} -q libpthread-stubs.a 64bits/libpthread-stubs.so.0
rm -f ./.libs/libpthread-stubs.a
${AR} -r ./.libs/libpthread-stubs.a .libs/libpthread-stubs.so.0 64bits/libpthread-stubs.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_libdir}/libpthread-stubs.a
%doc COPYING README

%files devel
%defattr(-,root,system)
%{_libdir}/libpthread-stubs.la
%{_libdir}/pkgconfig/*.pc
%doc COPYING README

%changelog
* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.3-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Jul 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.3-1
- Initial port on Aix 5.3

