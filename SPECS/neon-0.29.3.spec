Summary: An HTTP and WebDAV client library
Name: neon
Version: 0.29.3
Release: 1
License: GNU GPL
Url: http://www.webdav.org/neon/
Group: System Environment/Libraries
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
Source: http://www.webdav.org/neon/%{name}-%{version}.tar.gz
Requires: openssl
Requires: gettext
Requires: expat
Requires: zlib

%description 
neon is an HTTP and WebDAV client library, with a C interface;
providing a high-level interface to HTTP and WebDAV methods along
with a low-level interface for HTTP request handling.  neon
supports persistent connections, proxy servers, basic, digest and
Kerberos authentication, and has complete SSL support.

%package devel
Group: Utilities/System
Summary: Development package for neon developers.
Requires: neon = %{version}-%{release}
%description devel
The neon-devel package includes include files for developers 
interacting with the neon package.

%prep
%setup -q


%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure --with-ssl=openssl \
	    --with-libs=/opt/freeware/lib/ \
	    --enable-shared --prefix=%{prefix}
make 

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}/usr/lib 
cd ${RPM_BUILD_ROOT}/usr/lib
ln -sf ../..%{prefix}/lib/libneon.a .
cd -
cd ${RPM_BUILD_ROOT}/opt/freeware/include
cp -p neon/* .
cd -

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS README THANKS TODO ChangeLog BUGS
%{prefix}/bin/neon-config
%{prefix}/lib/libneon.a
%{prefix}/lib/libneon.la
%{prefix}/share/locale/*/LC_MESSAGES/neon.mo
%{prefix}/share/doc/neon*/html/*
%{prefix}/share/man/man1/*
%{prefix}/share/man/man3/*

%files devel
%defattr(-,root,root,-)
%{prefix}/include/*.h

%changelog
* Thu Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 0.29.3
- Initial port for AIX
