%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.5.1
Release: 1
License: Apache Software License 2.0
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Source1: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.asc
Source2: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.md5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define _libdir64 %{_prefix}/lib64

#BuildRequires: apr-devel >= 1.3.12
#BuildRequires: db4-devel >= 4.7.25-2
#BuildRequires: expat-devel >= 2.0.0
#BuildRequires: freetds-devel >= 0.82-2
#BuildRequires: gdbm-devel >= 1.8.3-1
#BuildRequires: libiconv >= 1.14-2
#BuildRequires: openldap-devel >= 2.4.23
#BuildRequires: pkg-config
#BuildRequires: sqlite-devel >= 3.6.23.1
#BuildRequires: unixODBC-devel >= 2.2.14

Requires: apr >= 1.4.5
#Requires: expat >= 2.0.0
#Requires: libiconv >= 1.14-2

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: %{name} = %{version}-%{release}
#Requires: apr-devel >= 1.4.5
#Requires: db4-devel >= 4.7.25-2
#Requires: expat-devel >= 2.0.0
#Requires: freetds-devel >= 0.82-2
#Requires: gdbm-devel >= 1.8.3-1
#Requires: openldap-devel >= 2.4.23
#Requires: pkg-config
#Requires: sqlite-devel >= 3.6.23.1
#Requires: unixODBC-devel >= 2.2.14

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.


%package gdbm
Group: Development/Libraries
Summary: APR utility library GDBM driver
BuildRequires: gdbm-devel >= 1.8.3-1
Requires: %{name} = %{version}-%{release}
Requires: gdbm >= 1.8.3-1

%description gdbm
This package provides the GDBM driver for the apr-util DBM interface.


%package db4
Group: Development/Libraries
Summary: APR utility library DB4 driver
#BuildRequires: db4-devel >= 4.7.25-2
Requires: %{name} = %{version}-%{release}
Requires: db >= 4.7.25-2

%description db4
This package provides the db4 driver for the apr-util DBM interface.


%package freetds
Group: Development/Libraries
Summary: APR utility library FreeTDS DBD driver
#BuildRequires: freetds-devel >= 0.82-2
Requires: %{name} = %{version}-%{release}
Requires: freetds >= 0.82-1

%description freetds
This package provides the FreeTDS driver for the apr-util DBD
(database abstraction) interface.


%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
#BuildRequires: openldap-devel >= 2.4.23
Requires: %{name} = %{version}-%{release}
Requires: openldap >= 2.4.23

%description ldap
This package provides the LDAP support for the apr-util.


%package odbc
Group: Development/Libraries
Summary: APR utility library ODBC DBD driver
#BuildRequires: unixODBC-devel >= 2.2.14
Requires: %{name} = %{version}-%{release}
Requires: unixODBC >= 2.2.14

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.


%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel >= 3.6.23.1
Requires: %{name} = %{version}-%{release}
Requires: sqlite >= 3.6.23.1

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.


%prep
%setup -q
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)


%build
export CC="/usr/vac/bin/xlc_r"
#export CPP="/usr/vacpp/bin/xlC_r"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
CFLAGS="-I%{_prefix}/lib64 -I%{_libdir} -I/usr/lib64 -I/usr/lib -I/opt/freeware/include/openssl" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --with-apr=%{_bindir}/apr-1-config_64 \
    --includedir=%{_includedir}/apr-%{apuver} \
    --with-berkeley-db \
    --with-dbm=db47 \
    --with-freetds \
    --with-gdbm \
    --with-ldap=ldap \
    --with-odbc \
    --with-sqlite3 \
    --without-sqlite2

make %{?_smp_mflags}

cd ../32bit
# now build he 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
CFLAGS="-I%{_prefix}/lib64 -I%{_libdir} -I/usr/lib64 -I/usr/lib -I/opt/freeware/include/openssl" \
./configure \
    --prefix=%{_prefix} \
    --with-apr=%{_bindir}/apr-1-config \
    --includedir=%{_includedir}/apr-%{apuver} \
    --with-berkeley-db \
    --with-dbm=db47 \
    --with-freetds \
    --with-gdbm \
    --with-ldap=ldap \
    --with-odbc \
    --with-sqlite3 \
    --without-sqlite2

make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
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
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_bindir}/*
%{_includedir}/*
%dir %{_libdir}/%{name}-%{apuver}
%dir %{_libdir64}/%{name}-%{apuver}
%{_libdir}/aprutil.exp
%{_libdir64}/aprutil.exp
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/bin/*
/usr/include/*
/usr/lib/*.a
/usr/lib64/*.a
/usr/lib/*.la
/usr/lib64/*.la


%files db4
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbm_db*
%{_libdir64}/%{name}-%{apuver}/apr_dbm_db*


%files gdbm
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbm_gdbm*
%{_libdir64}/%{name}-%{apuver}/apr_dbm_gdbm*


%files freetds 
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_freetds*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_freetds*


%files ldap
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_ldap*
%{_libdir64}/%{name}-%{apuver}/apr_ldap*


%files odbc
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_odbc*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_odbc*


%files sqlite
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_sqlite*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_sqlite*


%changelog
* Wed Jun 21 2013  Gerard Visiedo <Gerard.Visiedo@bull.net> 1.5.1-1
-  Update to version 1.5.1

* Tue Jul 24 2012 Patricia Cugny <Patricia.Cugny@bull.net> 1.4.6-1
-  Update to version 1.4.6

* Tue Mar 27 2012 Gerard Visiedo <Gerard.Visiedo@bull.net> 1.3.9-3
- Add .pc file into apr-devel package

* Thu Feb 17 2011 Gerard Visiedo <Gerard.Visiedo@bull;net> 1.3.9-2
- Add patch for aix6.1

* Wed Jan 20 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.3.9
- Update to version 1.3.9

* Fri Jul 31 2009 BULL 1.3.7
- Fisrt port for AIX

