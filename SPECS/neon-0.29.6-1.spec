Summary: An HTTP and WebDAV client library
Name: neon
Version: 0.29.6
Release: 1
License: LGPL
Group: System Environment/Libraries
URL: http://www.webdav.org/neon/
Source0: http://www.webdav.org/%{name}/%{name}-%{version}.tar.gz
Source1: http://www.webdav.org/%{name}/%{name}-%{version}.tar.gz.asc
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: expat-devel >= 2.0.0
BuildRequires: gettext
BuildRequires: krb5-devel >= 1.8.3-1
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: pkg-config
BuildRequires: zlib-devel
Requires: expat >= 2.0.0
Requires: gettext
Requires: krb5-libs >= 1.8.3-1
Requires: openssl >= 1.0.1
Requires: zlib

%description
neon is an HTTP and WebDAV client library, with a C interface;
providing a high-level interface to HTTP and WebDAV methods along
with a low-level interface for HTTP request handling.  neon
supports persistent connections, proxy servers, basic, digest and
Kerberos authentication, and has complete SSL support.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development libraries and C header files for the neon library
Group: Development/Libraries
Requires: neon = %{version}-%{release}
Requires: expat-devel >= 2.0.0
Requires: openssl-devel >= 1.0.1
Requires: pkg-config
Requires: zlib-devel

%description devel
The development library for the C language HTTP and WebDAV client library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CC="/usr/vac/bin/xlc_r"
export CFLAGS="-I/opt/freeware/include"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --enable-static \
    --with-ssl=openssl \
    --with-expat
make 

cp src/.libs/libneon.so.27 .
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --enable-static \
    --with-ssl=openssl \
    --with-expat
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X32_64 -q src/.libs/libneon.a ./libneon.so.27


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS BUGS TODO src/COPYING.LIB NEWS README THANKS
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/neon.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_libdir}/*.la
%{_datadir}/*
/usr/bin/*
/usr/include/*
/usr/lib/*.la


%changelog
* Tue Jul 09 2013 Gerard Visiedo <gerard.visiedo@bull;net> 0.29.6-1
- update to version 0.29.6

* Thu Jun 23 2011 Gerard Visiedo <gerard.visiedo@bull;net> 0.29.5-1
- Update to 0.29.5

* Thu Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 0.29.3
- Initial port for AIX
