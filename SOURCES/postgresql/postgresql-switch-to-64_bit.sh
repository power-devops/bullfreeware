#!/bin/sh


PGSQL_BINARIES="
clusterdb
createdb
createlang
createuser
dropdb
droplang
dropuser
pg_config
pg_dump
pg_isready
pg_restore
psql
reindexdb
vacuumdb
oid2name
pg_archivecleanup
pg_standby
pg_test_fsync
pg_test_timing
pg_xlogdump
pgbench
vacuumlo
initdb
pg_basebackup*
pg_controldata
pg_ctl
pg_receivexlog
pg_resetxlog
postgres
postmaster
ecpg
pltcl_delmod
pltcl_listmod
pltcl_loadmod
"


cd /opt/freeware/bin

for f in ${PGSQL_BINARIES} ; do
    if [ -f ${f} ] ; then
        /usr/bin/rm -f ${f}
        ln -s ${f}_64 ${f}
    fi
done

