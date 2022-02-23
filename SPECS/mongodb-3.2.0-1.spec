Name: mongodb-org
Obsoletes: mongo-10gen-server mongo-10gen
Version: 3.2.0
Release: alpha1
Summary: MongoDB open source document-oriented database system (metapackage)
License: AGPL 3.0
URL: http://www.mongodb.org
Group: Applications/Databases
Requires: mongodb-org-server = %{version}, mongodb-org-shell = %{version}, mongodb-org-mongos = %{version}, mongodb-org-tools = %{version}

Source0: mongodb-src-r%{version}.tar.bz2
Patch0: mongodb-%{version}-aix.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This metapackage will install the mongo shell, import/export tools, other client utilities, server software, default configuration, and init.d scripts.

%package server
Summary: MongoDB database server
Group: Applications/Databases
Requires: openssl
Obsoletes: mongo-10gen-server

%description server
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This package contains the MongoDB server software, default configuration files, and init.d scripts.

%package shell
Summary: MongoDB shell client
Group: Applications/Databases
Requires: openssl
Obsoletes: mongo-10gen

%description shell
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This package contains the mongo shell.

%package mongos
Summary: MongoDB sharded cluster query router
Group: Applications/Databases

%description mongos
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This package contains mongos, the MongoDB sharded cluster query router.

%package tools
Summary: MongoDB tools
Group: Applications/Databases
Requires: openssl
Obsoletes: mongo-10gen

%description tools
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This package contains standard utilities for interacting with MongoDB.

%package devel
Summary: Headers and libraries for MongoDB development
Group: Applications/Databases

%description devel
WARNING: this is an alpha release of Mongo for AIX, for testing purpose only.
Do NOT install this package on a production system.

MongoDB is built for scalability, performance and high availability, scaling from single server deployments to large, complex multi-site architectures. By leveraging in-memory computing, MongoDB provides high performance for both reads and writes. MongoDB’s native replication and automated failover enable enterprise-grade reliability and operational flexibility.

MongoDB is an open-source database used by companies of all sizes, across all industries and for a wide variety of applications. It is an agile database that allows schemas to change quickly as applications evolve, while still providing the functionality developers expect from traditional databases, such as secondary indexes, a full query language and strict consistency.

MongoDB has a rich client ecosystem including hadoop integration, officially supported drivers for 10 programming languages and environments, as well as 40 drivers supported by the user community.

MongoDB features:
* JSON Data Model with Dynamic Schemas
* Auto-Sharding for Horizontal Scalability
* Built-In Replication for High Availability
* Rich Secondary Indexes, including geospatial
* TTL indexes
* Text Search
* Aggregation Framework & Native MapReduce

This package provides the MongoDB static library and header files needed to develop MongoDB client software.

%prep
%setup -q -n mongodb-src-r%{version}
%patch0 -p1

%build
ulimit -f unlimited
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar"
export RM="rm -f"
export BUILD_DIR=$RPM_BUILD_DIR/mongodb-src-r%{version}/build
scons --prefix=%{_prefix} -j3 --js-engine=mozjs --ssl --opt=off core tools

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
scons --prefix=$RPM_BUILD_ROOT%{_prefix} -j3 --js-engine=mozjs --ssl --opt=off install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
cp debian/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
cp rpm/init.d-mongod $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mongod
chmod a+x $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mongod
cp rpm/mongod.conf $RPM_BUILD_ROOT%{_sysconfdir}/mongod.conf
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
#cp rpm/mongod.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mongod
mkdir -p $RPM_BUILD_ROOT/var/lib/mongo
mkdir -p $RPM_BUILD_ROOT/var/log/mongodb
mkdir -p $RPM_BUILD_ROOT/var/run/mongodb
touch $RPM_BUILD_ROOT/var/log/mongodb/mongod.log
cp distsrc/* .

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
if ! /usr/bin/id -g mongod &>/dev/null; then
  /usr/bin/mkgroup mongod
fi

%post server
if test $1 = 1
then
  # Detecting the memory size to set the cache size is currently not implemented in mongodb for AIX,
  # so it is requiered to use the --wiredTigerCacheSizeGB argument when starting mongod.
  MEM_SIZE=`lsattr -El sys0 | grep realmem | awk '{ print $2 }'`
  CACHE_SIZE=`expr 6 \* $MEM_SIZE / 10485760 - 1`
  /bin/mkssys -s mongod -G mongod -p /opt/freeware/bin/mongod -u 0 -o /var/log/mongodb/MongoOutput.log -e /var/log/mongodb/MongoError.log -a "--wiredTigerCacheSizeGB=${CACHE_SIZE}"
  startsrc -s mongod
fi

%preun server
if test $1 = 0
then
  rmssys -s mongod
fi

%postun server
if test $1 -ge 1
then
  startsrc -s mongod
fi

%files server
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/mongod.conf
%{_bindir}/mongod
%{_mandir}/man1/mongod.1*
%{_sysconfdir}/rc.d/init.d/mongod
#%{_sysconfdir}/sysconfig/mongod
%attr(0755,mongod,mongod) %dir /var/lib/mongo
%attr(0755,mongod,mongod) %dir /var/log/mongodb
%attr(0755,mongod,mongod) %dir /var/run/mongodb
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongodb/mongod.log
%doc GNU-AGPL-3.0
%doc README
%doc THIRD-PARTY-NOTICES
%doc MPL-2

%files shell
%defattr(-,root,root,-)
%{_bindir}/mongo
%{_mandir}/man1/mongo.1*

%files mongos
%defattr(-,root,root,-)
%{_bindir}/mongos
%{_mandir}/man1/mongos.1*

%files tools
%defattr(-,root,root,-)
#%doc README GNU-AGPL-3.0.txt

#%{_bindir}/bsondump
#%{_bindir}/mongodump
#%{_bindir}/mongoexport
#%{_bindir}/mongofiles
#%{_bindir}/mongoimport
#%{_bindir}/mongooplog
%{_bindir}/mongoperf
#%{_bindir}/mongorestore
#%{_bindir}/mongotop
#%{_bindir}/mongostat
%{_bindir}/mongosniff

#%{_mandir}/man1/bsondump.1*
#%{_mandir}/man1/mongodump.1*
#%{_mandir}/man1/mongoexport.1*
#%{_mandir}/man1/mongofiles.1*
#%{_mandir}/man1/mongoimport.1*
#%{_mandir}/man1/mongooplog.1*
%{_mandir}/man1/mongoperf.1*
#%{_mandir}/man1/mongorestore.1*
#%{_mandir}/man1/mongotop.1*
#%{_mandir}/man1/mongostat.1*
%{_mandir}/man1/mongosniff.1*

%changelog
* Mon Apr 04 2016 Matthieu Sarter <matthieu.sarter.external@atos.net>
- AIX port

* Thu Dec 19 2013 Ernie Hershey <ernie.hershey@mongodb.com>
- Packaging file cleanup

* Thu Jan 28 2010 Richard M Kreuter <richard@10gen.com>
- Minor fixes.

* Sat Oct 24 2009 Joe Miklojcik <jmiklojcik@shopwiki.com> -
- Wrote mongo.spec.

