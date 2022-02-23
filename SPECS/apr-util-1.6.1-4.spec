%define apuver 1

%bcond_without dotests

%bcond_without db
%bcond_without gdbm
%bcond_without ldap
# Does not work; needed include are not provided by mariadb nor mysql
%bcond_with mysql
%bcond_without odbc
%bcond_without pgsql
%bcond_without sqlite


Summary:    Apache Portable Runtime Utility library
Name:       apr-util
Version: 1.6.1
Release: 4
License:    Apache Software License 2.0
Group:      System Environment/Libraries
URL:        http://apr.apache.org/
Source0:    https://downloads.apache.org/apr/%{name}-%{version}.tar.bz2
Source1000: %{name}-%{version}-%{release}.build.log


%define _libdir64 %{_prefix}/lib64

BuildRequires: apr-devel
BuildRequires: expat-devel
BuildRequires: libiconv
BuildRequires: pkg-config
BuildRequires: libgcrypt-devel
BuildRequires: gnutls-devel
BuildRequires: p11-kit-devel
BuildRequires: db-devel >= 5.3.28
BuildRequires: sed, bzip2

Requires: apr
Requires: expat
Requires: libiconv


%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: %{name} = %{version}-%{release}
Requires: apr-devel
Requires: expat-devel
Requires: pkg-config


%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.


%if %{with db}
%package db
Group: Development/Libraries
Summary: APR utility library DB4 driver
BuildRequires: db-devel
Requires: %{name} = %{version}-%{release}
Requires: db >= 5.3.28

%description db
This package provides the db driver for the apr-util DBM interface.
%endif


%if %{with gdbm}
%package gdbm
Group: Development/Libraries
Summary: APR utility library GDBM driver
BuildRequires: gdbm-devel
Requires: %{name} = %{version}-%{release}
Requires: gdbm

%description gdbm
This package provides the GDBM driver for the apr-util DBM interface.
%endif


%if %{with ldap}
%package ldap
Group: Development/Libraries
Summary: APR utility library LDAP support
BuildRequires: openldap-devel
Requires: %{name} = %{version}-%{release}
Requires: openldap

%description ldap
This package provides the LDAP support for the apr-util.
%endif


%if %{with mysql}
%package mysql
Summary: APR utility library MySQL DBD driver
BuildRequires: mariadb-connector-c-devel
Requires: mariadb-connector-c
Requires: apr-util = %{version}-%{release}
 
%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.
%endif


%if %{with odbc}
%package odbc
Group: Development/Libraries
Summary: APR utility library ODBC DBD driver
BuildRequires: unixODBC-devel
Requires: %{name} = %{version}-%{release}
Requires: unixODBC

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.
%endif


%if %{with pgsql}
%package pgsql
Summary: APR utility library PostgreSQL DBD driver
BuildRequires: postgresql-libs
BuildRequires: postgresql-devel
Requires: postgresql-libs
Requires: apr-util = %{version}-%{release}
 
%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.
%endif


%if %{with sqlite}
%package sqlite
Group: Development/Libraries
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel
Requires: %{name} = %{version}-%{release}
Requires: sqlite

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.
%endif


%prep
%setup -q
# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
# export CONFIG_SHELL=/usr/bin/ksh
# export CONFIG_ENV_ARGS=/usr/bin/ksh
# export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
# export AR="/usr/bin/ar"
# export CC="/usr/vac/bin/xlc_r -qcpluscmt"
# export CC32="${CC} -q32"
# export CC64="${CC} -q64"
# export LTFLAGS="--tag=CC --silent"
# export RM="/usr/bin/rm -f"

export PATH=/opt/freeware/bin:/usr/bin
export AR="/usr/bin/ar -X32_64"
export CC="gcc"
export CC32="${CC} -maix32"
export CC64="${CC} -maix64"
export LTFLAGS="--tag=CC --silent"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC=${CC64}
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
%if %{with mysql}
export CPPFLAGS="-I/opt/freeware/include/mariadb"
export LDFLAGS="$LDFLAGS -L/opt/freeware/lib64/mariadb"
%endif
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --with-apr=%{_bindir}/apr-1-config_64 \
    --includedir=%{_includedir}/apr-%{apuver} \
    %{?with_db:--with-berkeley-db} \
    %{?with_db:--with-dbm=db53} \
    %{?with_gdbm:--with-gdbm} \
    %{?with_ldap:--with-ldap=ldap} \
    %{?with_odbc:--with-odbc} \
    %{?with_sqlite:--with-sqlite3} \
    --without-sqlite2 \
    %{?with_mysql:--with-mysql=%{_prefix}} \
    %{?with_pgsql:--with-pgsql=%{_libdir}} \

# strangely, what worked before (1.3.12) does not work anymore :-(
/opt/freeware/bin/sed -i 's|lber.h|ldap.h|g' include/apr_ldap.h
gmake %{?_smp_mflags}

cd ../32bit
# now build he 32-bit version
export OBJECT_MODE=32
export CC=${CC32}
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
%if %{with mysql}
export CPPFLAGS="-I/opt/freeware/include/mariadb"
export LDFLAGS="$LDFLAGS -L/opt/freeware/lib/mariadb"
%endif
./configure \
    --prefix=%{_prefix} \
    --with-apr=%{_bindir}/apr-1-config_32 \
    --includedir=%{_includedir}/apr-%{apuver} \
    %{?with_db:--with-berkeley-db} \
    %{?with_db:--with-dbm=db53} \
    %{?with_gdbm:--with-gdbm} \
    %{?with_ldap:--with-ldap=ldap} \
    %{?with_odbc:--with-odbc} \
    %{?with_sqlite:--with-sqlite3} \
    --without-sqlite2 \
    %{?with_mysql:--with-mysql=%{_prefix}} \
    %{?with_pgsql:--with-pgsql=%{_libdir}} \

# strangely, what worked before (1.3.12) does not work anymore :-(
/opt/freeware/bin/sed -i 's|lber.h|ldap.h|g' include/apr_ldap.h
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  cd  ${RPM_BUILD_ROOT}/%{_bindir}
  for fic in $(ls -1| grep -v -e _32 -e _64)
  do
    mv $fic "$fic"_32
    ln -sf "$fic"_64 $fic
  done
)


# Create archive
(
  cd ${RPM_BUILD_ROOT}/%{_libdir}
  # Main
  $AR qc libaprutil-1.a libaprutil-1.so.0.6.1
  $AR qc libaprutil-1.a ../lib64/libaprutil-1.so.0.6.1
  # Other archive
  cd apr-util-%{apuver}
  for fich in `ls  *-1.so`
  do $AR qc `basename $fich .so`.a                                $fich
     $AR qc `basename $fich .so`.a ../../lib64/apr-util-%{apuver}/$fich
  done
  # Link
  for fich in `find  -name "*.so" | grep -v "\-1.so"`
  do ln -sf `basename $fich .so`-1.a `basename $fich .so`.a
  done
  
  # Link of 64 bits
  cd ${RPM_BUILD_ROOT}/%{_libdir64}
  ln -sf ../lib/libaprutil-1.a .
  cd apr-util-%{apuver}
  for fich in `find ../../lib/apr-util-%{apuver}/ -name "*.a"`
  do ln -sf $fich .
  done
  
  # Remove .la and .so files
  cd ${RPM_BUILD_ROOT}
  find . -name "*.la" | xargs rm
  find . -name "*.so*" | xargs rm
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
(gmake -k check || true)
cd ../32bit
export OBJECT_MODE=32
(gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
%defattr(-,root,system,-)
%{_bindir}/*
%{_includedir}/*
%dir %{_libdir}/%{name}-%{apuver}
%dir %{_libdir64}/%{name}-%{apuver}
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc


%if %{with db}
%files db
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbm_db*
%{_libdir64}/%{name}-%{apuver}/apr_dbm_db*
%endif


%if %{with gdbm}
%files gdbm
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbm_gdbm*
%{_libdir64}/%{name}-%{apuver}/apr_dbm_gdbm*
%endif


%if %{with ldap}
%files ldap
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_ldap*
%{_libdir64}/%{name}-%{apuver}/apr_ldap*
%endif


%if %{with mysql}
%files mysql
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_mysql*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_mysql*
%endif


%if %{with odbc}
%files odbc
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_odbc*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_odbc*
%endif


%if %{with pgsql}
%files pgsql
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_pgsql*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_pgsql*
%endif

%if %{with sqlite}
%files sqlite
%defattr(-,root,system,-)
%{_libdir}/%{name}-%{apuver}/apr_dbd_sqlite*
%{_libdir64}/%{name}-%{apuver}/apr_dbd_sqlite*
%endif


%changelog
* Fri Oct 23 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.6.1-4
- Rebuild 1.6.1

* Mon Oct 19 2020 Étienne Guesnet <etienne.guesnet@atos.net> 1.6.1-3
- Remove db module and dependency

* Fri Apr 03 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.6.1-2
- Drop freetds subpackage
- Rebuild for odbc subpackage
- Build gdbm subpackage

* Wed Feb 12 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.6.1-1
- Add postgresql subpackage
- Add conditional mysql subpackage, not by default
- Conditional freetds subpackage, not by default
- Conditional gdbm subpackage, not by default
- No more provide .so
- Default binary are 64 bit

* Tue Feb 07 2017 Tony Reix <tony.reix@bull.net>  1.5.4-3
- Rebuilt for deleting dependency on libssl.so

* Wed Jul 06 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.5.4-2
- improved build environment to fix crashes

* Tue Oct 28 2014 Michael Perzl <michael@perzl.org> - 1.5.4-1
- updated to version 1.5.4

* Tue Oct 28 2014 Michael Perzl <michael@perzl.org> - 1.5.3-1
- updated to version 1.5.3

* Tue Jun 18 2013 Michael Perzl <michael@perzl.org> - 1.5.2-1
- updated to version 1.5.2

* Tue Oct 09 2012 Michael Perzl <michael@perzl.org> - 1.5.1-1
- updated to version 1.5.1

* Wed Dec 21 2011 Michael Perzl <michael@perzl.org> - 1.4.1-1
- updated to version 1.4.1

* Mon Jun 06 2011 Michael Perzl <michael@perzl.org> - 1.3.12-1
- updated to version 1.3.12

* Thu Jan 27 2011 Michael Perzl <michael@perzl.org> - 1.3.10-3
- split the package into multiple subpackages
- added LDAP support for apr-util, thus introduced a dependency on openldap

* Fri Dec 03 2010 Michael Perzl <michael@perzl.org> - 1.3.10-2
- fixed 64-bit issue

* Thu Oct 07 2010 Michael Perzl <michael@perzl.org> - 1.3.10-1
- updated to version 1.3.10

* Mon Jul 12 2010 Michael Perzl <michael@perzl.org> - 1.3.9-2
- rebuilt for better compatibility issues

* Tue Nov 17 2009 Michael Perzl <michael@perzl.org> - 1.3.9-1
- updated to version 1.3.9

* Tue Aug 19 2008 Michael Perzl <michael@perzl.org> - 1.3.4-1
- updated to version 1.3.4

* Sat Aug 16 2008 Michael Perzl <michael@perzl.org> - 1.3.2-1
- updated to version 1.3.2 and included both 32-bit and 64-bit shared objects

* Mon Mar 31 2008 Michael Perzl <michael@perzl.org> - 1.2.12-2
- rebuilt against new version of expat

* Tue Nov 27 2007 Michael Perzl <michael@perzl.org> - 1.2.12-1
- updated to v1.2.12

* Wed Sep 12 2007 Michael Perzl <michael@perzl.org> - 1.2.10-1
- first version for AIX V5.1 and higher
