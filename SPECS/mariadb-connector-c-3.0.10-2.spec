
%define _libdir64 %{_prefix}/lib64
%define gcc_compiler 1
%define cmake /usr/bin/cmake
%define pkg_name mariadb

# ==================================== #
#      FROM MARIADB-10.3.15            #
# ==================================== #

# =======
# Options
# =======
%define debug     0
%define embedded  ON
%define devel     1
%define client    1
%define common    1
%define errmsg    1
%define dotest    0

# ======
# Plugin
# ======
 # YES, AUTO, STATIC, DYNAMIC ou NO
# These plugin work
%define test_sql_discovery YES
%define locales            YES
%define metadata_lock_info YES
%define query_cache_info   YES
%define query_response_time  YES
%define blackhole          YES
%define federatedx         YES
%define archive            YES
%define ftexample          DYNAMIC
%define myisam             YES
%define aria               YES
# These plugin do not work
%define cracklib  NO
%define connect   NO
%define sphinx    NO
%define gssapi    NO
%define innodb    NO
%define spider    NO
%define sql_errlog              NO
%define perfschema              NO
%define auth_ed25519            NO
%define daemon_example          NO
%define dialog_examples         NO
%define example                 NO
%define server_audit            NO
%define audit_null              NO
%define simple_password_check   NO
%define example_key_management  NO
%define file_key_management     NO
%define debug_key_management    NO
%define versioning              NO
%define test_versioning         NO
%define disks                   NO
%define handlersocket           NO

%define innodb_bug_endian_crc32 NO
%define innodb_disallow_writes  NO
%define innodb_snappy           NO
# Linux only, deactivate some plugin
%define tokudb    NO
%define mroonga   NO
%define rocksdb   NO
%define cassandra NO
%define galera    NO
 # wsrep needs galera
%define wsrep     NO

# Gamma plugin
 # The Open Query GRAPH engine (OQGRAPH) is a computation engine allowing
 # hierarchies and more complex graph structures to be handled in a relational fashion
%define oqgraph   NO
%define federated NO

# ======
# Config
# ======
 # Provide a config package. Can conflict with connector. 
%define configpac   0
%define backup   NO
%define bench    1
 # Provide mysql names for compatibility
%define mysql_names  1
 # Conflict with community-mysql
%define conflicts    0
 # Compression lib
%define lz4      1
%define xz_lib   1
 # SSL
 # BUNDLE => YaSSL + GNUTLS
 # SYSTEM => OpenSSL
%define ssl   SYSTEM
%if %{ssl} != "SYSTEM" && %{ssl} != "BUNDLE"
echo "ssl must be SYSTEM or BUNDLE.
exit 1
%endif
%define so_mariadb    3
%define so_mariadbd   19

# ==================================== #
# END  FROM MARIADB-10.3.15            #
# ==================================== #


Name:           mariadb-connector-c
Version:        3.0.10
Release:        2
Summary:        The MariaDB Native Client library (C driver)
Group:          Servers
License:        LGPLv2+
Source:         https://downloads.mariadb.org/interstitial/connector-c-%{version}/mariadb-connector-c-%{version}-src.tar.gz
Source2:        mariadb-connector-c-my.cnf
Source3:        mariadb-connector-c-client.cnf
Url:            http://mariadb.org/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

# See  mariadb-10.3.12_int8.patch
Patch1:       mariadb-connector-c-3.0.10-1-int8.patch 
# See mariadb-10.3.10_dontwait.patch
Patch2:       mariadb-connector-c-3.0.10-1-MSG_DONTWAIT.patch
# See mariadb-10.3.10_getopt1.patch
Patch3:       mariadb-connector-c-3.0.6-2-getopt_long.patch
#Patch4:       mariadb-connector-c-3.0.6-2-my_ulonglong2double.patch
# See mariadb-10.3.12-compile_new_cmake.patch
Patch5:       mariadb-connector-c-3.0.10-1-compile_new_cmake.patch
# See mariadb-10.3.15-krb5.patch
Patch6:       mariadb-connector-c-3.0.10-1-krb5.patch
# See mariadb-10.3.12-libsuffix.patch
Patch7:       mariadb-connector-c-3.0.10-2-libsuffix.patch
# See mariadb-10.3.12-ma_dtoa-BIGENDIAN.patch
Patch8:       mariadb-connector-c-3.0.10-1-ma_dtoa-BIGENDIAN.patch
# See mariadb-10.3.12.mariadb_config.patch 
Patch9:       mariadb-connector-c-3.0.10-1-mariadb_config.patch

Requires:  getopt_long
Requires:         libiconv >= 1.16-2

# More information: https://mariadb.com/kb/en/mariadb/building-connectorc-from-source/

Requires:       %{_sysconfdir}/my.cnf
BuildRequires:  zlib-devel cmake openssl-devel gcc-c++
# Remote-IO plugin
#BuildRequires:  libcurl-devel

%description
The MariaDB Native Client library (C driver) is used to connect applications
developed in C/C++ to MariaDB and MySQL databases.



%package devel
Summary:        Development files for mariadb-connector-c
Group:          devel 
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
#BuildRequires:  multilib-rpm-config

%description devel
Development files for mariadb-connector-c.
Contains everything needed to build against libmariadb.so >=3 client library.



%package config
Summary:        Configuration files for packages that use /etc/my.cnf as a configuration file
Group:          config 
BuildArch:      noarch
Obsoletes:      mariadb-config <= 3:10.3.8-4

%description config
This package delivers /etc/my.cnf that includes other configuration files
from the /etc/my.cnf.d directory and ships this directory as well.
Other packages should only put their files into /etc/my.cnf.d directory
and require this package, so the /etc/my.cnf file is present.



%prep
%setup -q -n mariadb-connector-c-%{version}-src

%patch1  -p1  -b  .int8
%patch2  -p1  -b  .MSG_DONTWAIT
%patch3  -p1  -b  .getopt_long
#patch4  -p1  -b  .my_ulonglong2double
%patch5  -p1  -b  .compile_new_cmake
%patch6  -p1  -b  .krb5
%patch7  -p1  -b  .libsuffix
%patch8  -p1  -b  .bigendian
%patch9  -p1  -b  .config

# Remove unsused parts
rm -r win zlib win-iconv examples

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build

env
export PATH=/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:

# Chose GCC or XLC

echo "CC: %{gcc_compiler}"

%if %{gcc_compiler} == 1

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"


export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
#export CC__="/usr/vac/bin/xlc"
#export  CC__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export CC__="/opt/IBM/xlc/13.1.3/bin/xlc"       #  13.01.0003.0004

#export CXX__="/usr/vacpp/bin/xlC"
#export CXX__="/usr/vac/bin/xlc"            # Version: 12.01.0000.0000
export CXX__="/opt/IBM/xlC/13.1.0/bin/xlC"     #  13.01.0003.0004

export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

# Force cmake to user AIX ar command
export AR=/usr/bin/ar
export NM=/usr/bin/nm

export MAKE="gmake --trace -j8"

############################### 64-bit BEGIN ##############################
# first build the 64-bit version


cd 64bit

#rm -f CMakeCache.txt

# https://jira.mariadb.org/browse/MDEV-13836:
#   The server has (used to have for ages) some magic around the port number.
#   If it's 0, the default port value will use getservbyname("mysql", "tcp"), that is, whatever is written in /etc/services.
#   If it's a positive number, say, 3306, it will be 3306, no matter what /etc/services say.
#   I don't know if that behavior makes much sense, /etc/services wasn't supposed to be a system configuration file.

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

#export LIBPATH=/opt/freeware/lib64:/opt/freeware/lib:/usr/lib
# For cmake
#export LIBPATH=/opt/freeware/lib/gcc/powerpc-ibm-aix7.1.0.0/8.2.0/pthread:$LIBPATH

export OBJECT_MODE=64
export CXX="${CXX__}"
export CC="${CC__}"

export CFLAGS="-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -pthread ${FLAG64}"
export CFLAGS="$CFLAGS -mcmodel=large -fno-omit-frame-pointer -fno-strict-aliasing"

export LDFLAGS="-pthread"

export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

%if "%{debug}" == "1"
CFLAGS="$CFLAGS -O0"
%endif

export CXXFLAGS="$CFLAGS"


# type cmake
# TYPECMAKE=`type cmake | awk '{print $NF}'`
# ldd  $TYPECMAKE

# ==================================== #
#      FROM MARIADB-10.3.15            #
# ==================================== #

%cmake . -L \
%if "%{debug}" == "1"
         -DCMAKE_BUILD_TYPE=DEBUG \
%else
         -DCMAKE_BUILD_TYPE=RELEASE \
         -DBUILD_CONFIG=mysql_release \
%endif
         -DOBJECT_MODE="64" \
         -DCMAKE_INSTALL_RPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib" \
         -DCMAKE_BUILD_RPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib" \
         -DCMAKE_SKIP_BUILD_RPATH=FALSE \
         -DCMAKE_SKIP_INSTALL_RPATH=FALSE \
         -DFEATURE_SET=%{feature} \
         -DLOG_LOCATION="%{logfile}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
         -DINSTALL_SYSCONF2DIR="%{_sysconfdir}/my.cnf.d" \
         -DINSTALL_DOCDIR="%{_pkgdocdir}" \
         -DINSTALL_DOCREADMEDIR="%{_pkgdocdir}" \
         -DINSTALL_INCLUDEDIR=include/mysql \
         -DINSTALL_INFODIR=share/info \
         -DINSTALL_LIBDIR="%{_lib}64" \
         -DINSTALL_MANDIR=man \
         -DINSTALL_MYSQLSHAREDIR=share/%{pkg_name} \
%if "%{dotest}" == "1"
         -DINSTALL_MYSQLTESTDIR=share/mysql-test \
%endif
         -DINSTALL_PLUGINDIR="%{_lib}64/%{pkg_name}/plugin" \
         -DINSTALL_SBINDIR=libexec \
         -DINSTALL_SCRIPTDIR=bin \
         -DINSTALL_SQLBENCHDIR=share \
         -DINSTALL_SUPPORTFILESDIR=share/%{pkg_name} \
         -DMYSQL_DATADIR="%{dbdatadir}" \
         -DTMPDIR=/var/tmp \
         -DENABLED_LOCAL_INFILE=ON \
         -DENABLE_DTRACE=OFF \
         -DSECURITY_HARDENED=ON \
         -DWITH_MYSQLCOMPAT=%{mysql_names} \
         -DWITH_EMBEDDED_SERVER=%{embedded} \
         -DWITH_MARIA_BACKUP=%{backup} \
%if "%{dotest}" == "1"
         -DWITH_UNIT_TESTS=YES \
%else
         -DWITH_UNIT_TESTS=NO \
%endif
%if "%{ssl}" == "SYSTEM"
         -DWITH_SSL=system \
         -DCONC_WITH_SSL=system \
%else
         -DWITH_SSL= bundle \
%endif
         -DWITH_ZLIB=system \
         -DWITH_EXTERNAL_ZLIB=YES \
         -DICONV_LIBRARIES=/opt/freeware/lib/libiconv.a \
	\
         -DPLUGIN_CASSANDRA=%{cassandra} \
         -DPLUGIN_FILE_KEY_MANAGEMENT=%{file_key_management} \
         -DPLUGIN_EXAMPLE_KEY_MANAGEMENT=%{example_key_management} \
         -DPLUGIN_DEBUG_KEY_MANAGEMENT=%{debug_key_management} \
         -DPLUGIN_TEST_VERSIONING=%{test_versioning} \
	\
         -DPLUGIN_DISKS=%{disks} \
         -DPLUGIN_HANDLERSOCKET=%{handlersocket} \
	\
         -DPLUGIN_SPHINX=%{sphinx} \
         -DPLUGIN_OQGRAPH=%{oqgraph} \
         -DPLUGIN_FEDERATED=%{federated} \
	\
         -DPLUGIN_MYISAM=%{myisam} \
         -DPLUGIN_ARIA=%{aria} \
         -DPLUGIN_INNOBASE=%{innodb} \
         -DPLUGIN_SPIDER=%{spider} \
         -DPLUGIN_PARTITION=%{partition} \
	\
         -DPLUGIN_AUTH_GSSAPI=%{gssapi} \
         -DPLUGIN_AUTH_ED25519=%{auth_ed25519} \
         -DPLUGIN_DAEMON_EXAMPLE=%{daemon_example} \
         -DPLUGIN_DIALOG_EXAMPLES=%{dialog_examples} \
         -DPLUGIN_EXAMPLE=%{example} \
         -DPLUGIN_TEST_SQL_DISCOVERY=%{test_sql_discovery} \
         -DPLUGIN_LOCALES=%{locales} \
         -DPLUGIN_METADATA_LOCK_INFO=%{metadata_lock_info} \
         -DPLUGIN_QUERY_CACHE_INFO=%{query_cache_info}\
         -DPLUGIN_QUERY_RESPONSE_TIME=%{query_response_time} \
         -DPLUGIN_SERVER_AUDIT=%{server_audit} \
         -DPLUGIN_AUDIT_NULL=%{audit_null} \
         -DWITH_WSREP=%{wsrep} \
         -DPLUGIN_WSREP=%{wsrep} \
         -DPLUGIN_WSREP_INFO=%{wsrep} \
         -DPLUGIN_BLACKHOLE=%{blackhole} \
         -DPLUGIN_FEDERATEDX=%{federatedx} \
         -DPLUGIN_ARCHIVE=%{archive} \
         -DPLUGIN_SQL_ERRLOG=%{sql_errlog} \
         -DPLUGIN_SIMPLE_PASSWORD_CHECK=%{simple_password_check} \
	\
         -DPLUGIN_MROONGA=%{mroonga} \
         -DPLUGIN_CRACKLIB_PASSWORD_CHECK=%{cracklib} \
         -DPLUGIN_ROCKSDB=%{rocksdb} \
         -DPLUGIN_TOKUDB=%{tokudb} \
         -DPLUGIN_CONNECT=%{connect} \
         -DPLUGIN_FTEXAMPLE=%{ftexample} \
         -DCONNECT_WITH_MONGO=OFF \
         -DCONNECT_WITH_JDBC=OFF \
         -DPLUGIN_PERFSCHEMA=%{perfschema} \
	\
         -DWITH_INNODB_BUG_ENDIAN_CRC32=%{innodb_bug_endian_crc32} \
         -DWITH_INNODB_DISALLOW_WRITES=%{innodb_disallow_writes} \
         -DWITH_INNODB_SNAPPY=%{innodb_snappy} \
%if "%{debug}" == "1"
         -DWITH_ASAN=OFF -DWITH_INNODB_EXTRA_DEBUG=NO
%endif

# ==================================== #
# END  FROM MARIADB-10.3.15            #
# ==================================== #

$MAKE


#%check
## Check the generated configuration on the actual machine
#%{buildroot}%{_bindir}/mariadb_config
#
## Run the unit tests
## - don't run mytap tests
## - ignore the testsuite result for now. Enable tests now, fix them later.
#pushd unittest/libmariadb/
#ctest || :
#popd


# # # # Pass 32 bits
# # # ############################### 32-bit BEGIN ##############################
# # # 
# # # cd ../32bit
# # # 
# # # rm -f CMakeCache.txt
# # # 
# # # export LIBPATH=/opt/freeware/lib:/opt/freeware/lib:/usr/lib
# # # # For cmake
# # # export LIBPATH=/opt/freeware/lib/gcc/powerpc-ibm-aix7.1.0.0/8.2.0/pthread:$LIBPATH
# # # 
# # # export OBJECT_MODE=32
# # # export CC="${CC32}   $GLOBAL_CC_OPTIONS"
# # # export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
# # # 
# # # export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -lintl"
# # # export LDFLAGS="${LDFLAGS} -lgetopt_long"
# # # 
# # # export CFLAGS="-I/usr/include -I/opt/freeware/include"
# # # export CXXFLAGS="$CFLAGS"
# # # 
# # # 
# # # 
# # # cmake . \
# # #        -DCMAKE_BUILD_TYPE=RelWithDebInfo \
# # # \
# # #        -DMARIADB_UNIX_ADDR=%{_sharedstatedir}/mysql/mysql.sock \
# # #        -DMARIADB_PORT=3306 \
# # # \
# # #        -DWITH_EXTERNAL_ZLIB=YES \
# # #        -DWITH_SSL=OPENSSL \
# # #        -DWITH_MYSQLCOMPAT=ON \
# # # \
# # #        -DCMAKE_AR=$AR  \
# # #        -DINSTALL_LAYOUT=RPM \
# # #        -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
# # #        -DINSTALL_LIBDIR="%{_libdir64}" \
# # #        -DINSTALL_INCLUDEDIR="include/mysql" \
# # #        -DINSTALL_PLUGINDIR="%{_libdir64}/mariadb/plugin" \
# # # \
# # #        -DWITH_UNITTEST=ON
# # # 
# # # 
# # # 
# # # #cmake -LAH
# # # $MAKE



%install
#make install DESTDIR=%{buildroot}

# Use BullFreeware find command !
export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#export MAKE="gmake --trace"
export MAKE="gmake --trace -j8"
export RM="/usr/bin/rm -f"

echo ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64

mkdir -p tmp
cd tmp
ar -X64 -x ../libmariadb/libmariadb.a # contains liblibmariadb.so

mv liblibmariadb.so libmariadb.so

ar -qc libmariadb.a  libmariadb.so

# libmariadb.so.3 and limariadbd.19 are provided by Linux RPM,
# we include it into archive.
# libsql*.so.N do not exist in Linux.
cp libmariadb.so  libmariadb.so.%{so_mariadb}
ar -qc libmariadb.a  libmariadb.so.%{so_mariadb}

cp libmariadb.a ../libmariadb/libmariadb.a
cp libmariadb.a ../libmariadb/CMakeFiles/CMakeRelink.dir/libmariadb.a

cd ..
rm -rf tmp


$MAKE DESTDIR=${RPM_BUILD_ROOT} install


####TODO: liblib et cie




# https://fedoraproject.org/wiki/PackagingDrafts/MultilibTricks
##	%multilib_fix_c_header --file %{_includedir}/mysql/mariadb_version.h

# TODO: Not the right way!
# Remove static linked libraries and symlinks to them
#rm %{buildroot}%{_libdir64}/lib*.a

# Add a compatibility symlinks
(ls -l mariadb_config mariadb_version.h || true)
ln -s mariadb_config %{buildroot}%{_bindir}/mysql_config
ln -s mariadb_version.h %{buildroot}%{_includedir}/mysql/mysql_version.h

# Install config files
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/my.cnf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf

##############End 64bit install #################################################



# # # # Pass 32 bits
# # # cd ../32bit
# # # export OBJECT_MODE=32
# # # $MAKE DESTDIR=${RPM_BUILD_ROOT} install
# # # 
# # # # Remove static linked libraries and symlinks to them
# # # rm %{buildroot}%{_libdir64}/lib*.a
# # # 
# # # # Add a compatibility symlinks
# # # (ls -l mariadb_config mariadb_version.h || true)
# # # # already done in 64bit. Same files??
# # # #ln -s mariadb_config %{buildroot}%{_bindir}/mysql_config
# # # #ln -s mariadb_version.h %{buildroot}%{_includedir}/mysql/mysql_version.h
# # # 
# # # # Install config files
# # # install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/my.cnf
# # # install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
# # # 
# # # 
# # # ## https://fedoraproject.org/wiki/Packaging:Directory_Replacement
# # # #%pretrans -p <lua>
# # # #path = "%{_libdir64}/mariadb"
# # # #st = posix.stat(path)
# # # #if st and st.type == "link" then
# # # #  os.remove(path)
# # # #end
# # # #path = "%{_libdir64}/mysql"
# # # #st = posix.stat(path)
# # # #if st and st.type == "link" then
# # # #  os.remove(path)
# # # #end

# /etc/my.cnf(.d) is /opt/freeware/my.cnf(.d)
mkdir %{buildroot}/etc
ln -s %{_sysconfdir}/my.cnf.d %{buildroot}/etc/my.cnf.d
ln -s %{_sysconfdir}/my.cnf   %{buildroot}/etc/my.cnf


%files
%{_libdir64}/libmariadb.a
%dir %{_libdir64}/mariadb
%dir %{_libdir64}/mariadb/plugin
%{_libdir64}/mariadb/plugin/*
# auth_gssapi_client.so, caching_sha2_password.so, dialog.so, mysql_clear_password.so, sha256_password.so
# %doc README
# %license COPYING.LIB

%files devel
# # Binary which provides compiler info for software compiling against this library
%{_bindir}/mariadb_config
%{_bindir}/mysql_config

# Symlinks to the versioned library
%{_libdir64}/libmysqlclient.a
%{_libdir64}/libmysqlclient_r.a

# Header files
%dir %{_includedir}/mysql
%{_includedir}/mysql/*

%files config
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf
%config(noreplace) /etc/my.cnf
%config(noreplace) /etc/my.cnf.d


# RPMLint issues from 2.3.2 release tracked on the upstream JIRA:
#   https://jira.mariadb.org/browse/CONC-232
#   https://jira.mariadb.org/browse/CONC-234
# RPMLint issues from 3.0.2 release tracked on the upstream JIRA:
#   https://jira.mariadb.org/browse/CONC-287
#   https://jira.mariadb.org/browse/CONC-291

%changelog
* Wed Jun 19 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.0.10-2
- Use GNU iconv.

* Wed Jun 05 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> -3.0.10-1
- New version 3.0.10
- Tested with Mariadb 10.3.15
- Provides archive

* Fri Sep 14 2018 Sena Apeke <sena.apeke.external@atos.net> - 3.0.6-1
- Port to AIX 6.1 .
 
* Tue Sep 04 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-2
- Fix parallel installability of x86_64 and i686 devel package

* Fri Aug 03 2018 Michal Schorm <mschorm@redhat.com> - 3.0.6-1
- Rebase to 3.0.6

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 3.0.5-3
- Add -config sub-package that delivers system-wide /etc/my.cnf and
  /etc/my.cnf.d directory, that other packages should use
  This package also obsoletes mariadb-config

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 08 2018 Michal Schorm <mschorm@redhat.com> - 3.0.5-1
- Rebase to 3.0.5

* Thu Apr 26 2018 Michal Schorm <mschorm@redhat.com> - 3.0.4-1
- Rebase to 3.0.4

* Mon Apr 23 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-4
- Further fix of the '--plugindir' output from the config binary
  Realted: #1569159

* Wed Mar 21 2018 Richard W.M. Jones <rjones@redhat.com> - 3.0.3-3
- Fix plugin install directory (INSTALL_PLUGINDIR not PLUGIN_INSTALL_DIR).

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Michal Schorm <mschorm@redhat.com> - 3.0.3-1
- Rebase to 3.0.3

* Mon Nov 27 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-21
- Remove unneeded dependency on xmlto

* Tue Nov 14 2017 Pavel Raiskup <praiskup@redhat.com> - 3.0.2-19
- drop misleading provides

* Wed Nov 08 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-19
- Move the scriptlet to the correct package

* Thu Nov 02 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-18
- Fix typo in require

* Wed Nov 01 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-17
- Use correct require for OpenSSL

* Wed Nov 01 2017 Merlin Mathesius <mmathesi@redhat.com> - 3.0.2-16
- Correct typo in spec file conditional

* Tue Oct 31 2017 Merlin Mathesius <mmathesi@redhat.com> - 3.0.2-15
- Cleanup spec file conditionals

* Tue Oct 31 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-14
- Remove Requires for openssl. Managed by RPM.

* Mon Oct 30 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-13
- Update scriplet dealing with symlinks as Guidelines suggests
  Related: #1501933

* Thu Oct 26 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-12
- Move library directly to libdir, don't create any symlinks to directories
- Update scritplets, so they only check for old symlinks to directories
  Related: #1501933
- Add 'Conflicts' with mariadb package on F<28
  Related: #1506441

* Mon Oct 09 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-11
- Fix ldconfig path

* Wed Oct 04 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-10
- Add scriptlets to handle errors in /usr/lib64/ created by older versions
  of mariadb and mariadb-connector-c pakages

* Wed Sep 20 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-9
- Add symlinks so more packages will build succesfully
- Change libdir from .../lib64/mariadb to mysql
  Related: #1497234

* Wed Sep 13 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-7
- Move header files to the same location, as they would be in mariadb-server
- Add provides "libmysqlclient.so"

* Tue Sep 05 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-5
- Remove a symlink /usr/lib64/mysql that conflicts with mariadb-libs

* Mon Aug 14 2017 Honza Horak <hhorak@redhat.com> - 3.0.2-4
- Add compatibility symlinks

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Michal Schorm <mschorm@redhat.com> - 3.0.2-1
- Rebase to version 3.0.2
- Library libmariadb.so.3 introduced
- Plugin Remote-IO enabled

* Wed Jun 07 2017 Michal Schorm <mschorm@redhat.com> - 2.3.3-1
- Rebase to version 2.3.3
- Patch dropped, solved by upstream; https://jira.mariadb.org/browse/CONC-231

* Tue Feb 07 2017 Michal Schorm <mschorm@redhat.com> - 2.3.2-2
- Fix based on output from RPMLint in previous version

* Tue Jan 24 2017 Michal Schorm <mschorm@redhat.com> - 2.3.2-1
- Rebase to version 2.3.2, patch needed (fixed by upstream in later versions)
- Plugin dir moved from /libdir/plugin to /libdir/mariadb/plugin

* Thu Oct 27 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-3
- Fixed ownership of {_libdir}/mariadb (this dir must me owned by package)
- Fixed ownership of {_sysconfigdir}/ld.so.conf.d (this dir must me owned by package)
- Fixed redundnace on lines with {_sysconfigdir}/ld.so.conf.d
- Fixed ownership of {_bindir} (only one program is owned, so let's be accurate)
- Some comments added, for me and future maintainers

* Mon Oct 17 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-2
- Fixed ownership of {_libdir}/mariadb directory and cosmetic specfile changes

* Tue Sep 13 2016 Michal Schorm <mschorm@redhat.com> - 2.3.1-1
- Rebase to version 2.3.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 23 2015 Matej Mužila <mmuzila@redhat.com> - 2.1.0-1
- Rebase to version 2.1.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 24 2014 Matej Mužila <mmuzila@redhat.com> - 2.0.0-2
- Fixed html IDs in documentation

* Tue Aug 26 2014 Matej Mužila <mmuzila@redhat.com> - 2.0.0-2
- Initial version for 2.0.0
