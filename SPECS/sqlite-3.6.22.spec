Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: 3.6.22
Release: 1
License: Public Domain
Group: Applications/Databases
URL: http://www.sqlite.org/
Source0: http://www.sqlite.org/sqlite-amalgamation-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-root

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development documentation 
for %{name}. If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%prep
%setup -q

%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure --exec-prefix=%{_prefix} --prefix=%{_prefix}

make 

#cd .libs
#cp libsqlite3.a libsqlite3-static.a
#ar -qv libsqlite3.a libsqlite3.so.0
%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 

install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_datadir}/man1/sqlite3.1
cp -p .libs/libsqlite3.so.* $RPM_BUILD_ROOT/%{_libdir}

cd  $RPM_BUILD_ROOT
for dir in bin lib include
do
        mkdir -p usr/$dir
        cd usr/$dir
        ln -sf ../..%{_prefix}/$dir/* .
        cd -
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc %{name}-%{docver}-docs/*
%{_bindir}/sqlite3
/usr/bin/sqlite3
%{_libdir}/*
/usr/lib/*
%{_datadir}/man?/*

%files devel
%defattr(-, root, root)
%{_includedir}/*.h
/usr/include/*.h
/usr/lib/*.la

%changelog
* Tue Jan 19 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.6.22-1
- Initial port for AIX
