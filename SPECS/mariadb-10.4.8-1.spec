# Create a test package in ANY case, but test only if with dotests.
%bcond_without dotests

# Prefix that is used for patches
%global pkg_name %{name}
%global pkgnamepatch mariadb
%define cmake /usr/bin/cmake
%define _libdir64 %{_prefix}/lib64

# =======
# Options
# =======
# Provides ALWAYS devel, client, common
# NEVER provides clibrary, config
# At least one of release or debug must be 1.
%define release_mode 1
%define debug_mode   1
%define embedded     ON
%define errmsg       1
# Too time and space consuming: unactivate big test by default.
%bcond_with big_test
# Spider tests are also "big-test", but no any spider test
# is computated without big-test. So, enable it in any case.

%define backup       ON
%define bench        1
# Provide mysql names for compatibility
%define mysql_names  1
# Conflict with community-mysql
%define conflicts    1

%define compile_flag "-j10"

# =======
# Plugins
# =======
# Can be
#  xsmall
#  small     :             embedded
#  classic   : (small)   + archive + federatedX + blackhole
#  large     : (classic) + innodb
#  xlarge    : (large)   + partition
#  community : (xlarge)
%define feature                 xlarge
# YES, AUTO, STATIC, DYNAMIC or NO
%define archive                 STATIC
%define blackhole               STATIC
%define federatedx              STATIC
%define file_key_management     DYNAMIC
%define ftexample               DYNAMIC
%define innodb                  STATIC
%define locales                 DYNAMIC
%define metadata_lock_info      DYNAMIC
%define partition               STATIC
%define query_cache_info        DYNAMIC
%define query_response_time     DYNAMIC
 # Some tests fail
 # Can't find symbol 'json_make_array' in library if DYNAMIC
%define connect                 NO
# YES, AUTO, STATIC or NO
%define aria                    STATIC
%define feedback                STATIC
%define myisam                  STATIC
%define perfschema              STATIC
# YES, AUTO, DYNAMIC or NO
%define audit_null              DYNAMIC
%define auth_ed25519            DYNAMIC
 # A test fails
%define dialog_examples         NO
 # Need an unavailable library
%define cracklib                NO
%define example_key_management  DYNAMIC
%define gssapi                  DYNAMIC
%define server_audit            DYNAMIC
%define simple_password_check   DYNAMIC
%define spider                  DYNAMIC
%define sql_errlog              DYNAMIC
# DYNAMIC or OFF
%define client_ed25519          DYNAMIC

# Beta / experimental plugin
# If it does not work, we just unactivate it.
# YES, AUTO, STATIC, DYNAMIC or NO
%define daemon_example          DYNAMIC
# YES, AUTO, DYNAMIC or NO
%define debug_key_management    DYNAMIC
%define example                 DYNAMIC
%define handlersocket           DYNAMIC
%define test_sql_discovery      DYNAMIC
%define test_versioning         DYNAMIC

# Linux only
%define cassandra NO
%define disks     NO
%define galera    NO
%define mroonga   NO
%define rocksdb   NO
%define tokudb    NO
%define wsrep     NO

# Gamma plugins
%define oqgraph   NO
 # Federated works, but we do not want gamma plugin
%define federated NO
%define sphinx    NO


# ======
# Config
# ======
# Innodb options
%bcond_with    innodb_bug_endian_crc32
%bcond_without innodb_snappy

# Compression lib
%define lz4      1
%define xz_lib   1

# SSL
# BUNDLE => WolfSSL for server (bundled) + GNUTLS for client
# SYSTEM => OpenSSL
%define ssl   SYSTEM
%if %{ssl} != "SYSTEM" && %{ssl} != "BUNDLE"
    echo "ssl must be SYSTEM or BUNDLE.
    exit 1
%endif
%if %{ssl} == "SYSTEM"
Requires:       openssl
%else
Requires:       gnutls
%endif

# Values from cmake/mysql_version.cmake
%define so_mariadbd  19

%global _pkgdocdir %{_docdir}/%{pkg_name}-%{version}

# We define some system's well known locations here so we can use them easily
# later when building to another location (like SCL)
%global logrotateddir %{_sysconfdir}/logrotate.d
# %global logfiledir %{_localstatedir}/log/%{daemon_name}
# %global logfile %{logfiledir}/%{daemon_name}.log
%global logfiledir %{_localstatedir}/log/mariadb/
%global logfile %{logfiledir}/mariadb.log
# Directory for storing pid file
# %global _rundir %{_localstatedir}/run
# %global pidfiledir %{_rundir}/%{mysqld_pid_dir}

# Defining where database data live
# /opt/freeware/var/lib/mysql
%global dbdatadir %{_localstatedir}/lib/mysql


Name:             mariadb
Version:          10.4.8
Release:          1
Epoch:            3
Summary:          MariaDB: a very fast and robust SQL database server
URL:              http://mariadb.org
# Exceptions allow client libraries to be linked with most open source SW, not only GPL code.  See LICENCE.mariadb.txt
License:          GPLv2 with exceptions and LGPLv2 and BSD

# Make long macros shorter
%global sameevr   %{epoch}:%{version}-%{release}

Source0:          https://downloads.mariadb.org/Mariadb/mariadb-%{version}/source/mariadb-%{version}.tar.gz
Source1:          mysql_config_multilib.sh
Source2:          mysql-prepare-db-dir.sh
Source3:          mysql-check-socket.sh
Source4:          mysql-scripts-common.sh
Source5:          mysql-check-upgrade.sh
Source6:          LICENCE.mariadb.txt
Source1000:       %{name}-%{version}-%{release}.build.log


#	Fedora Patches 10.3.12

#    Patch2: Make the python interpretter be configurable
# Does not pass on 10.3.15; modified
Patch2:           %{pkgnamepatch}-10.3.15-pythonver.patch
#   Patch4: Red Hat distributions specific logrotate fix
Patch4:           %{pkgnamepatch}-logrotate.patch


#	ATOS patches

# int8 to signed char and not char.
# Needed because defined in an other part of the code.
# "previous declaration of 'int8'" at [ 48%] Building C object libmariadb/CMakeFiles/caching_sha2_password.dir/plugins/auth/caching_sha2_pw.c.o
Patch18:        mariadb-10.3.12_int8.patch
# define MSG_DONTWAIT, used in libmariadb/plugin/pvio/pvio_socket.c
Patch19:        mariadb-10.3.10_dontwait.patch
# Use getopt long
Patch20:        mariadb-10.3.10_getopt1.patch
# Skipped tests via mysql-test-run.pl
Patch24:        mariadb-10.4.6_test_encrypt.patch
# Exit 0 even if an error.
Patch25:        mariadb-10.3.10_test_result.patch

# >= 2019-04 patches.
# Patch pour os/AIX
Patch26:        mariadb-10.4.6-AIX.cmake.patch
# Compile with new CMake
# Modify threadpool, export-import 
Patch27:        mariadb-10.4.6-compile_new_cmake.patch
# Avoid R_TOCL in debug mod
Patch28:        mariadb-10.3.12-compile_debug.patch
# Find krb5 correctly; replace mariadb-10.3.10_gssapi.patch
Patch29:        mariadb-10.3.15-krb5.patch
# shared and static lib as the same suffix in AIX
Patch30:        mariadb-10.3.12-libsuffix.patch
# Skip versioning test and unskip some non failing test
Patch31:        mariadb-10.4.8-skip_test.patch
# Compilation flags and avoid RPM configuration
Patch32:        mariadb-10.3.12-correct_flags.patch
# Erase AIX specific tricks for old AIX.
# They are useless and may have side effect.
Patch33:        mariadb-10.3.12-old_trick.patch
# Compile mariadb_config
Patch36:        mariadb-10.3.12.mariadb_config.patch
# Compile on debug mode without Werror.
Patch37:        mariadb-10.3.15.werror_flag.patch
# SI_KERNEL is not defined
Patch38:        mariadb-10.4.6-SI_KERNEL.patch
# Compile auth_socket
Patch39:        mariadb-10.3.15.auth_socket.patch
# Compile dynamic plugins
Patch40:        mariadb-10.4.6-plugin_dynamic.patch
# Import symbols for test
Patch41:        mariadb-10.4.6-symbols_test.patch
# Export symbol for dynamic plugins
Patch42:        mariadb-10.4.7-plugin_dyn_export.patch
# Test perror
Patch43:        mariadb-10.4.7-errorcode.patch
# Change config files
Patch44:        mariadb-10.4.7-config_files.patch
# Just a typo in CMakeLists; will be corrected in 10.4.9
Patch45:        mariadb-10.4.8-CRYPT.patch

BuildRequires:    gcc-c++
BuildRequires:    cmake >= 3.14
BuildRequires:    cmake < 3.15
BuildRequires:    sed make
BuildRequires:    getopt_long
Requires:         getopt_long

# Page compression algorithms for InnoDB & XtraDB
BuildRequires:    zlib-devel
%if "%{lz4}" == "1"
BuildRequires:    lz4-devel
%endif
%if "%{xz_lib}" == "1"
BuildRequires:    xz-devel
%endif

# CLI graphic
BuildRequires:    ncurses-devel
# Bison SQL parser
BuildRequires:    bison >= 2.0 

# OpenSSL
%if %{ssl} == "SYSTEM"
Requires:         openssl 
BuildRequires:    openssl-devel
%endif

# Extra for InnoDB/XtraDB
%if %{with innodb_snappy}
Requires:         snappy
%endif

%if "%{lz4}" == "1"
Requires:         lz4
%endif
%if "%{xz_lib}" == "1"
Requires:         xz
%endif

Requires:         bash coreutils grep
Requires:         getopt_long
Requires:         libiconv >= 1.16-2

BuildRequires:    pcre-devel >= 8.35 pkg-config
# Some tests requires python
BuildRequires:    python3
BuildRequires:         bash coreutils grep
# Tests requires time and ps and some perl modules
BuildRequires:    time
BuildRequires:    perl(Env)
BuildRequires:    perl(Exporter)
BuildRequires:    perl(Fcntl)
BuildRequires:    perl(File::Temp)
BuildRequires:    perl(Data::Dumper)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IPC::Open3)
BuildRequires:    perl(Memoize)
BuildRequires:    perl(Socket)
BuildRequires:    perl(Sys::Hostname)
BuildRequires:    perl(Test::More)
BuildRequires:    perl(Time::HiRes)
BuildRequires:    perl(Symbol)


Requires:         %{name}-common = %{sameevr}

# If not built with client library in this package, use connector-c
Requires:         mariadb-connector-c >= 3.0

%if "%{mysql_names}" == "1"
Provides:         mysql = %{sameevr}
Provides:         mysql = %{sameevr}
Provides:         mysql-compat-client = %{sameevr}
Provides:         mysql-compat-client = %{sameevr}
%endif

Suggests:         %{name}-server = %{sameevr}

# MySQL (with caps) is upstream's spelling of their own RPMs for mysql
%if "%{conflicts}" == "1"
Conflicts:        community-mysql
%endif

# obsoletion of mariadb-galera
Provides:         mariadb-galera = %{sameevr}


%description
MariaDB is a community developed branch of MySQL - a multi-user, multi-threaded
SQL database server. It is a client/server implementation consisting of
a server daemon (mysqld) and many different client programs and libraries.
The base package contains the standard MariaDB/MySQL client programs and
generic MySQL files.

%package          common
Summary:          The shared files required by server and client
Requires:         mariadb-connector-c-config

Obsoletes: %{name}-libs <= %{sameevr}

%description      common
The package provides the essential shared files for any MariaDB program.
You will need to install this package to use any other MariaDB package.


%if "%{errmsg}" == "1"
%package          errmsg
Summary:          The error messages files required by server and embedded
Requires:         %{name}-common = %{sameevr}

%description      errmsg
The package provides error messages files for the MariaDB daemon and the
embedded server. You will need to install this package to use any of those
MariaDB packages.
%endif


%package          server
Summary:          The MariaDB server and related files

# note: no version here = %%{version}-%%{release}
%if "%{mysql_names}" == "1"
Requires:         mysql-compat-client
Requires:         mysql
Recommends:       %{name}
%else
Requires:         %{name}
%endif
Requires:         mariadb-connector-c-config
Requires:         %{name}-common = %{sameevr}
Requires:         %{name}-errmsg = %{sameevr}
Recommends:       %{name}-server-utils = %{sameevr}
Recommends:       %{name}-backup = %{sameevr}
%if "%{cracklib}" != "NO"
Recommends:       %{name}-cracklib-password-check = %{sameevr}
%endif
%if "%{gssapi}" != "NO"
Recommends:       %{name}-gssapi-server = %{sameevr}
%endif

Requires:         coreutils
Suggests:         mytop
Suggests:         logrotate

# for fuser in mysql-check-socket
# AIX : fuser is: /usr/sbin/fuser provided by: LPP bos.rte.filesystem
#	Requires:         psmisc

%if "%{mysql_names}" == "1"
Provides:         mysql-server = %{sameevr}
Provides:         mysql-server = %{sameevr}
Provides:         mysql-compat-server = %{sameevr}
Provides:         mysql-compat-server = %{sameevr}
%endif
%if "%{conflicts}" == "1"
Conflicts:        community-mysql-server
%endif

%description      server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed branch of MySQL.


%if "%{connect}" == "DYNAMIC"
%package          connect-engine
Summary:          The CONNECT storage engine for MariaDB
Requires:         %{name}-server = %{sameevr}

%description      connect-engine
The CONNECT storage engine enables MariaDB to access external local or
remote data (MED). This is done by defining tables based on different data
types, in particular files in various formats, data extracted from other DBMS
or products (such as Excel), or data retrieved from the environment
(for example DIR, WMI, and MAC tables).
%endif


%if "%{backup}" == "ON"
%package          backup
Summary:          The mariabackup tool for physical online backups
Requires:         %{name}-server = %{sameevr}

%description      backup
MariaDB Backup is an open source tool provided by MariaDB for performing
physical online backups of InnoDB, Aria and MyISAM tables.
For InnoDB, "hot online" backups are possible.
%endif


# TODO: NO, DYNAMIC, STATIC ??
%if "%{cracklib}" != "NO"
%package          cracklib-password-check
Summary:          The password strength checking plugin
Requires:         %{name}-server = %{sameevr}
BuildRequires:    cracklib-dicts cracklib-devel
Requires:         cracklib-dicts

%description      cracklib-password-check
CrackLib is a password strength checking library. It is installed by default
in many Linux distributions and is invoked automatically (by pam_cracklib.so)
whenever the user login password is modified.
Now, with the cracklib_password_check password validation plugin, one can
also use it to check MariaDB account passwords.
%endif


%if "%{gssapi}" != "NO"
%package          gssapi-server
Summary:          GSSAPI authentication plugin for server
Requires:         %{name}-server = %{sameevr}
BuildRequires:    krb5-devel
Requires:         krb5-libs

%description      gssapi-server
GSSAPI authentication server-side plugin for MariaDB for passwordless login.
This plugin includes support for Kerberos on Unix.
%endif


%package          server-utils
Summary:          Non-essential server utilities for MariaDB/MySQL applications
Requires:         %{name}-server = %{sameevr}
%if "%{mysql_names}" == "1"
Provides:         mysql-perl = %{sameevr}
%endif
# mysqlhotcopy needs DBI/DBD support
Requires:         perl(DBI) perl(DBD::mysql)

%description      server-utils
This package contains all non-essential server utilities and scripts for
managing databases. It also contains all utilities requiring Perl and it is
the only MariaDB sub-package, except test subpackage, that depends on Perl.


%package          devel
Summary:          Files for development of MariaDB/MySQL applications
%if "%{ssl}" == "SYSTEM"
Requires:         openssl-devel
%endif
Requires:         mariadb-connector-c-devel >= 3.0
%if "%{mysql_names}" == "1"
Provides:         mysql-devel = %{sameevr}
Provides:         mysql-devel = %{sameevr}
%endif
%if "%{conflicts}" == "1"
Conflicts:        community-mysql-devel
%endif

%description      devel
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed branch of MySQL.

This package contains everything needed for developing MariaDB/MySQL server
applications. For developing client applications, use mariadb-connector-c
package.


%if "%{embedded}" != "NO"
%package          embedded
Summary:          MariaDB as an embeddable library
Requires:         %{name}-common = %{sameevr}
Requires:         %{name}-errmsg = %{sameevr}
%if "%{mysql_names}" == "1"
Provides:         mysql-embedded = %{sameevr}
Provides:         mysql-embedded = %{sameevr}
%endif

%description      embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed branch of MySQL.
%endif


%if "%{bench}" == "1"
%package          bench
Summary:          MariaDB benchmark scripts and data
Requires:         %{name} = %{sameevr}
# Maybe perl(DBD:mysql)
Requires:         perl(DBI)
%if "%{mysql_names}" == "1"
Provides:         mysql-bench = %{sameevr}
Provides:         mysql-bench = %{sameevr}
%endif
%if "%{conflicts}" == "1"
Conflicts:        community-mysql-bench
%endif

%description      bench
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed branch of MySQL.
This package contains benchmark scripts and data for use when benchmarking
MariaDB.
%endif


%package          test
Summary:          The test suite distributed with MariaDB
Requires:         %{name} = %{sameevr}

%if "%{conflicts}" == "1"
Conflicts:        community-mysql-test
%endif
%if "%{mysql_names}" == "1"
Provides:         mysql-test = %{sameevr}
Provides:         mysql-test = %{sameevr}
%endif

%description      test
MariaDB is a multi-user, multi-threaded SQL database server.
MariaDB is a community developed branch of MySQL.
This package contains the regression test suite distributed with the MariaDB
sources.


%prep
# Tests + MariaDB use approximatively 20 Gio.
# Big test (complete) uses more than 100.
# Big test (without the two more consuming) uses a lot (how many?).
%if %{with dotests}
SO=`/usr/bin/df -k /opt | awk '{if(NR==2)print $3}'`
echo "Disk space available for testing cmake must be >= 25 Gio"
if [ "$SO" -lt 25000000 ]
then
    echo "Not enough disk space on /opt !"
    exit 1
fi
%if %{with big_test}
SO=`/usr/bin/df -k /opt | awk '{if(NR==2)print $3}'`
echo "Disk space available for testing in big-test cmake must be >= 100 Gio"
if [ "$SO" -lt 100000000 ]
then
    echo "Not enough disk space on /opt !"
    exit 1
fi
%endif
%endif

%if "%{release_mode}" != "1" && "%{debug_mode}" != "1"
echo "No release and no debug. Will compile nothing. Stop here."
exit 1
%endif

%setup -q -n mariadb-%{version}

# Remove JAR files that upstream puts into tarball
find . -name "*.jar" -type f -exec /opt/freeware/bin/rm --verbose -f {} \;

%patch2 -p1
%patch4 -p1

%patch18 -p1  -b  .int8
%patch19 -p1  -b  .dontwait
%patch20 -p1  -b  .getopt1
%patch24 -p1  -b  .encrypt
%patch25 -p1  -b  .test_result

%patch26 -p1  -b  .AIX
%patch27 -p1  -b  .new_cmake
%patch28 -p1  -b  .compile_debug
%patch29 -p1  -b  .krb5
%patch30 -p1  -b  .suffix 
%patch31 -p1  -b  .skip_unskip_test
%patch32 -p1  -b  .flags
%patch33 -p1  -b  .old_trick
%patch36 -p1  -b  .mariadb_config
# Usefull in test mod only
%patch37 -p1  -b  .werror_flag
%patch38 -p1  -b  .SI_KERNEL
%patch39 -p1  -b  .auth_socket
%patch40 -p1  -b  .plugins_dynamic
%patch41 -p1  -b  .symbols_test
%patch42 -p1  -b  .dyn_export
%patch43 -p1  -b  .errorcode
%patch44 -p1  -b  .config_files
%patch45 -p1

# workaround for upstream bug #56342
#rm mysql-test/t/ssl_8k_key-master.opt

cp %{SOURCE1}  %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} scripts


# Get version of PCRE, that upstream use
pcre_maj=`grep '^m4_define(pcre_major' pcre/configure.ac | /opt/freeware/bin/sed -r 's/^m4_define\(pcre_major, \[([0-9]+)\]\)/\1/'`
pcre_min=`grep '^m4_define(pcre_minor' pcre/configure.ac | /opt/freeware/bin/sed -r 's/^m4_define\(pcre_minor, \[([0-9]+)\]\)/\1/'`

# Check if the PCRE version that upstream use, is the same as the one present in system
pcre_system_version=`pkg-config %{_libdir}/pkgconfig/libpcre.pc --modversion 2>/dev/null `
if [ "$pcre_system_version" != "$pcre_maj.$pcre_min" ]
then
  echo "\n Warning: System PCRE version is not correct. \n\tSystem version number:$pcre_system_version \n\tUpstream version number: $pcre_maj.$pcre_min\n"
fi


rm -r storage/rocksdb/
rm -r storage/mroonga/
rm -r storage/cassandra/
rm -r storage/tokudb/
rm INSTALL-WIN-SOURCE
rm -r zlib
rm -r win
# TODO: PCRE? WolfSSL

# If cassandra, rocksdb or mroonga, we need to modify this.
%define all_folder ./BUILD ./BUILD-CMAKE ./CMakeLists.txt ./CONTRIBUTING.md ./COPYING ./CREDITS ./Docs ./EXCEPTIONS-CLIENT ./INSTALL-SOURCE ./KNOWN_BUGS.txt ./README.md ./THIRDPARTY ./VERSION ./appveyor.yml ./client ./cmake ./config.h.cmake ./configure.cmake ./dbug ./debian ./extra ./include ./libmariadb ./libmysqld ./libservices ./man ./mysql-test ./mysys ./mysys_ssl ./pcre ./plugin ./randgen ./scripts ./sql ./sql-bench ./sql-common ./storage ./strings ./support-files ./tests ./unittest ./vio ./wsrep-lib 

%if "%{release_mode}" == "1" && "%{debug_mode}" == "1"
mkdir release
mkdir debug
mv %{all_folder} ./release
cd release
cp -r %{all_folder} ../debug
%else
%if "%{release_mode}" == "1"
mkdir release
mv %{all_folder} ./release
%else
mkdir debug
mv %{all_folder} ./debug
%endif
%endif

cp %{SOURCE6} ..

%build

env | sort

#rm -f CMakeCache.txt

CFLAGS="-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGE_FILES -maix64 -pthread"
# use mcmodel
CFLAGS="$CFLAGS -mcmodel=large"
CFLAGS="$CFLAGS -mtune=power8"

export LDFLAGS="-pthread"

export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

CXXFLAGS="$CFLAGS"

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"
echo "CC Version:"
$CC --version

export OBJECT_MODE=64

export CFLAGS
export CXXFLAGS

compile() {
    set -ex
    %cmake . -L \
            -DCMAKE_BUILD_TYPE=$1 \
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
            -DWITH_JEMALLOC="NO" \
    %if %{with dotests}
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
    %if %{with dotests}
            -DWITH_UNIT_TESTS=YES \
    %else
            -DWITH_UNIT_TESTS=NO \
    %endif
    %if "%{ssl}" == "SYSTEM"
            -DWITH_SSL=system \
    %else
            -DWITH_SSL=bundled \
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
            -DPLUGIN_SPIDER=%{spider} \
        \
            -DPLUGIN_BLACKHOLE=%{blackhole} \
            -DPLUGIN_FEDERATEDX=%{federatedx} \
            -DPLUGIN_ARCHIVE=%{archive} \
            -DPLUGIN_PARTITION=%{partition} \
            -DPLUGIN_INNOBASE=%{innodb} \
        \
            -DPLUGIN_AUTH_GSSAPI=%{gssapi} \
            -DPLUGIN_AUTH_ED25519=%{auth_ed25519} \
            -DPLUGIN_CLIENT_ED25519=%{client_ed25519} \
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
            -DPLUGIN_SQL_ERRLOG=%{sql_errlog} \
            -DPLUGIN_SIMPLE_PASSWORD_CHECK=%{simple_password_check} \
            -DPLUGIN_FEEDBACK=%{feedback} \
        \
            -DPLUGIN_MROONGA=%{mroonga} \
            -DPLUGIN_CRACKLIB_PASSWORD_CHECK=%{cracklib} \
            -DPLUGIN_ROCKSDB=%{rocksdb} \
            -DPLUGIN_TOKUDB=%{tokudb} \
            -DPLUGIN_CONNECT=%{connect} \
            -DPLUGIN_FTEXAMPLE=%{ftexample} \
            -DCONNECT_WITH_MONGO=OFF \
            -DCONNECT_WITH_JDBC=OFF \
        \
            -DWITH_INNODB_BUG_ENDIAN_CRC32=%{?with_innodb_bug_endian_crc32:YES}%{!?with_innodb_bug_endian_crc32:NO} \
            -DWITH_INNODB_SNAPPY=%{?with_innodb_snappy:YES}%{!?with_innodb_snappy:NO}

    gmake VERBOSE=1 %{compile_flag}

    # stack-trace flag (or skip-stack-trace) are not available.
    # TODO: still needed?
    find mysql-test -name "*.opt" -exec /opt/freeware/bin/sed -i 's|\-\-skip-stack-trace| |g' {} \;
}


%if "%{release_mode}" == "1"
################################################################
#                             RELEASE                          #
################################################################
cd release
compile "RELEASE"
cd ..
%endif

%if "%{debug_mode}" == "1"
################################################################
#                             DEBUG                            #
################################################################
cd debug
compile "DEBUG"
cd ..
%endif


%check

export SED="/opt/freeware/bin/sed"
export AR=/usr/bin/ar

%if %{with dotests}
# Create user mysql (if it does not exist) and use it to test
# Usefull if you create RPM as root.
mkgroup mysql || :
/usr/sbin/useradd -g mysql -d %{dbdatadir} -c "MySQL Server"  -u 27 mysql || :

# The cmake build scripts don't provide any simple way to control the
# options for mysql-test-run, so ignore the make target and just call it
# manually.  Nonstandard options chosen are:
# --force to continue tests after a failure
# no retries please
# test SSL with --ssl
# skip tests that are listed in unstable_test
# avoid redundant test runs with --binlog-format=mixed
# increase timeouts to prevent unwanted failures during mass rebuilds

# Usefull arguments:
#    --do-test=mysql_client_test_nonblock \
#    --skip-rpl
#    --suite=roles
#    --mem for running in the RAM; Not enough space in KOJI for this

%define common_testsuite_arguments " --parallel=8 --force --retry=0 --suite-timeout=900 --testcase-timeout=30 --force-restart --shutdown-timeout=60 --max-test-fail=9999 "

%if "%{debug_mode}" == "1"
cd debug/mysql-test
rm -rf var
mkdir var
chown mysql:mysql .
(
su mysql -c "
ulimit -n unlimited
ulimit -c 10
ulimit -m unlimited
ulimit -d unlimited
set -ex

perl ./mysql-test-run.pl %{common_testsuite_arguments} \
    --ssl --skip-test=spider --skip-test-list=unstable-tests \
%if %{with big_test}
     --big-test
%endif

%if "%{spider}" != "NO"
# Second run for the SPIDER suites that fail with SCA (ssl self signed certificate)
# All tests need big-test, but are no so time consuming.

# spider/oracle and spider/oracle2 tests are skipped.
perl ./mysql-test-run.pl %{common_testsuite_arguments} \
    --skip-ssl --suite=spider,spider/bg,spider/bugfix,spider/feature,spider/handler,spider/regression/e1121,spider/regression/e112122 \
    --big-test
%endif # spider
"
)
cd ../..
%endif #debug_mode

%if "%{release_mode}" == "1"
cd release/mysql-test
# Erase even if debug tests done: too space consuming.
rm -rf var
mkdir var
chown mysql:mysql .
(
su mysql -c "
ulimit -n unlimited
ulimit -c 10
ulimit -m unlimited
ulimit -d unlimited
set -ex

perl ./mysql-test-run.pl %{common_testsuite_arguments} \
    --ssl --skip-test=spider --skip-test-list=unstable-tests \
%if %{with big_test}
     --big-test
%endif

%if "%{spider}" != "NO"
# Second run for the SPIDER suites that fail with SCA (ssl self signed certificate)
# All tests need big-test, but are no so time consuming.

# spider/oracle and spider/oracle2 tests are skipped.
perl ./mysql-test-run.pl %{common_testsuite_arguments} \
    --skip-ssl --suite=spider,spider/bg,spider/bugfix,spider/feature,spider/handler,spider/regression/e1121,spider/regression/e112122 \
    --big-test
%endif # spider
"
)

cd ../..
%endif #release_mode

%endif # dotests


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%install

export INSTALL="/usr/bin/install"
export SED="/opt/freeware/bin/sed"
export AR=/usr/bin/ar

# If release is 1, only install release.
%if "%{release_mode}" == "1"
cd release
%else
cd debug
%endif

export OBJECT_MODE=64

# libmariadbd.a contains *liblib*mariadbd.so without version. Manual correction.
# libmysqld.a needs to link to libmariadbd.a and 
# libmariadbd.a needs to contain libmariadbd.so and libmysqld.so (same file, but different name).
# TODO: improve this...
mkdir -p tmp
cd tmp
$AR -X64 -x ../libmysqld/libmariadbd.a   	 # contains liblibmysqld.so (!)

mv    liblibmysqld.so               libmariadbd.so.%{so_mariadbd}
ln -s libmariadbd.so.%{so_mariadbd} libmysqld.so.%{so_mariadbd}
# First, add libmariadbd
$AR -qc libmariadbd.a libmariadbd.so.%{so_mariadbd}
# Next, add stripped -e libmysqld
/usr/bin/strip -e -X64 libmysqld.so.%{so_mariadbd}
$AR -qc libmariadbd.a libmysqld.so.%{so_mariadbd}
# Now, strip -e libmariadbd.**so** and create symlinks
/usr/bin/strip -e -X64 libmariadbd.so.%{so_mariadbd}
ln -s   libmariadbd.a                 libmysqld.a                 
rm      libmysqld.so.%{so_mariadbd}
ln -s   libmariadbd.so.%{so_mariadbd} libmysqld.so.%{so_mariadbd} 

# Copy all stuff to the right location
cp libmariadbd.a ../libmysqld/libmariadbd.a
cp libmariadbd.a ../libmysqld/CMakeFiles/CMakeRelink.dir/libmariadbd.a
cp libmysqld.a   ../libmysqld/libmysqld.a
cp libmysqld.a   ../libmysqld/CMakeFiles/CMakeRelink.dir/libmysqld.a

cp libmariadbd.so.%{so_mariadbd} ..
cp libmysqld.so.%{so_mariadbd}   ..

cd ..
rm -rf tmp

export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

gmake DESTDIR=%{buildroot} install -j10

# Copy .so to lib
cp libmariadbd.so.%{so_mariadbd} ${RPM_BUILD_ROOT}%{_libdir}64
cp libmysqld.so.%{so_mariadbd}   ${RPM_BUILD_ROOT}%{_libdir}64
# Create a symlink for lib*.a to lib64
(
  cd ${RPM_BUILD_ROOT}%{_libdir}64
  mv    libmariadbd.a ../lib
  mv    libmysqld.a   ../lib
  ln -s ../lib/libmariadbd.a libmariadbd.a 
  ln -s ../lib/libmysqld.a   libmysqld.a   
)

# All .a are copied. Erase useless (static).
rm %{buildroot}/%{_libdir64}/libmariadbclient.a
rm %{buildroot}/%{_libdir64}/libmysqlservices.a
rm %{buildroot}/%{_libdir64}/libmariadbd_server.a

ln -sf mysql_config.1.gz %{buildroot}%{_mandir}/man1/mariadb_config.1.gz

# Upstream install this into arch-independent directory
# Reported to upstream as: https://jira.mariadb.org/browse/MDEV-14340
# TODO: check, if it changes location inside that file depending on values passed to CMake
mkdir -p %{buildroot}/%{_libdir64}/pkgconfig
mv %{buildroot}/%{_datadir}/pkgconfig/*.pc %{buildroot}/%{_libdir64}/pkgconfig

# Logfile creation
mkdir -p   %{buildroot}%{logfiledir}
chmod 0750 %{buildroot}%{logfiledir}
touch      %{buildroot}%{logfile}

mkdir -p %{buildroot}%{dbdatadir}
chmod 0755 %{buildroot}%{dbdatadir}

mkdir -p %{buildroot}/%{_pkgdocdir}
chmod 0755 %{buildroot}/%{_pkgdocdir}

# TODO verify this point
# rm scripts/my.cnf

# use different config file name for each variant of server (mariadb / mysql)
mv %{buildroot}%{_sysconfdir}/my.cnf.d/server.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf

# helper scripts for service starting
$INSTALL -M 755 -f %{buildroot}%{_libexecdir} scripts/mysql-prepare-db-dir.sh  
$INSTALL -M 755 -f %{buildroot}%{_libexecdir} scripts/mysql-check-socket.sh    
$INSTALL -M 755 -f %{buildroot}%{_libexecdir} scripts/mysql-check-upgrade.sh   
$INSTALL -M 644 -f %{buildroot}%{_libexecdir} scripts/mysql-scripts-common.sh 

# additional
cp -p scripts/mariadb-service-convert %{buildroot}%{_bindir}/mariadb-service-convert
cp -p sql/mysqld %{buildroot}%{_bindir}/mysqld


# Test package
# mysql-test includes one executable that doesn't belong under /usr/share, so move it and provide a symlink
(mv %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir} || true)
(ln -s ../../../../../bin/my_safe_process %{buildroot}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process || true)

# Client that uses libmysqld embedded server.
# Pretty much like normal mysql command line client, but it doesn't require a running mariadb server.
%if "%{embedded}" != "NO"
rm %{buildroot}%{_bindir}/mysql_embedded
%endif
rm %{buildroot}%{_mandir}/man1/mysql_embedded.1*
# This script creates the MySQL system tables and starts the server.
# Upstream says:
#   It looks like it's just "mysql_install_db && mysqld_safe"
#   I've never heard of anyone using it, I'd say, no need to pack it.
rm %{buildroot}%{_datadir}/%{pkg_name}/binary-configure
# FS files first-bytes recoginiton
# Not updated by upstream since nobody realy use that
rm %{buildroot}%{_datadir}/%{pkg_name}/magic

# Binary for monitoring MySQL performance
# Shipped as a standalona package in Fedora
rm %{buildroot}%{_bindir}/mytop

# put logrotate script where it needs to be
mkdir -p %{buildroot}%{logrotateddir}
mv %{buildroot}%{_datadir}/%{pkg_name}/mysql-log-rotate %{buildroot}%{logrotateddir}
chmod 644 %{buildroot}%{logrotateddir}

# remove duplicate logrotate script
rm %{buildroot}%{_sysconfdir}/logrotate.d/mysql
# Remove AppArmor files
rm -r %{buildroot}%{_datadir}/%{pkg_name}/policy/apparmor

# script without shebang: https://jira.mariadb.org/browse/MDEV-14266
chmod -x %{buildroot}%{_datadir}/sql-bench/myisam.cnf

# Disable plugins
# TODO: No cnf file.
# %if "%{gssapi}" != "NO"
# $SED -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
# %endif
%if "%{cracklib}" != "NO"
$SED -i 's/^plugin-load-add/#plugin-load-add/' %{buildroot}%{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%endif

%if "%{embedded}" == "NO"
rm %{buildroot}%{_mandir}/man1/{mysql_client_test_embedded,mysqltest_embedded}.1
%endif


rm %{buildroot}%{_sysconfdir}/my.cnf.d/client.cnf
# Client library and links
unlink %{buildroot}%{_libdir64}/libmysqlclient.a
unlink %{buildroot}%{_libdir64}/libmysqlclient_r.a
unlink %{buildroot}%{_libdir64}/libmariadb.a
# Client plugins
rm %{buildroot}%{_libdir64}/%{pkg_name}/plugin/dialog.so
rm %{buildroot}%{_libdir64}/%{pkg_name}/plugin/mysql_clear_password.so
rm %{buildroot}%{_libdir64}/%{pkg_name}/plugin/sha256_password.so
rm %{buildroot}%{_libdir64}/%{pkg_name}/plugin/auth_gssapi_client.so
rm %{buildroot}%{_libdir64}/%{pkg_name}/plugin/caching_sha2_password.so

# This files are already included in mariadb-connector-c
rm %{buildroot}%{_includedir}/mysql/mysql_version.h
rm %{buildroot}%{_includedir}/mysql/errmsg.h
rm %{buildroot}%{_includedir}/mysql/ma_list.h
rm %{buildroot}%{_includedir}/mysql/ma_pvio.h
rm %{buildroot}%{_includedir}/mysql/mariadb_com.h
rm %{buildroot}%{_includedir}/mysql/mariadb_ctype.h
rm %{buildroot}%{_includedir}/mysql/mariadb_dyncol.h
rm %{buildroot}%{_includedir}/mysql/mariadb_stmt.h
rm %{buildroot}%{_includedir}/mysql/mariadb_version.h
rm %{buildroot}%{_includedir}/mysql/ma_tls.h
rm %{buildroot}%{_includedir}/mysql/mysqld_error.h
rm %{buildroot}%{_includedir}/mysql/mysql.h
rm -r %{buildroot}%{_includedir}/mysql/mariadb
#rm -r %{buildroot}%{_includedir}/mysql/mariadbmysql

# No config.
# TODO: verify. Twice?
rm %{buildroot}%{_sysconfdir}/my.cnf

# TODO: No cnf file.
# %if "%{gssapi}" == "NO"
# rm -rf %{buildroot}%{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
# %endif

%if "%{errmsg}" == "0"
rm %{buildroot}%{_datadir}/%{pkg_name}/errmsg-utf8.txt
rm -r %{buildroot}%{_datadir}/%{pkg_name}/{english,czech,danish,dutch,estonian,\
french,german,greek,hungarian,italian,japanese,korean,norwegian,norwegian-ny,\
polish,portuguese,romanian,russian,serbian,slovak,spanish,swedish,ukrainian,hindi}
%endif

%if "%{bench}" == "0"
rm -r %{buildroot}%{_datadir}/sql-bench
%endif

%pre server
#/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
mkgroup mysql || :
/usr/sbin/useradd -g mysql -d %{dbdatadir} -c "MySQL Server"  -u 27 mysql || :
#/usr/sbin/useradd -M -N -g mysql -o -r -d %{mysqluserhome} -s /sbin/nologin \
#  -c "MySQL Server" -u 27 mysql >/dev/null 2>&1 || :


%files
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_plugin
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf


%files common
%doc LICENCE.mariadb.txt
%doc %{_pkgdocdir}
%dir %{_datadir}/%{pkg_name}
%{_datadir}/%{pkg_name}/charsets

%if "%{errmsg}" == "1"
%files errmsg
%{_datadir}/%{pkg_name}/errmsg-utf8.txt
%{_datadir}/%{pkg_name}/english
%lang(cs) %{_datadir}/%{pkg_name}/czech
%lang(da) %{_datadir}/%{pkg_name}/danish
%lang(nl) %{_datadir}/%{pkg_name}/dutch
%lang(et) %{_datadir}/%{pkg_name}/estonian
%lang(fr) %{_datadir}/%{pkg_name}/french
%lang(de) %{_datadir}/%{pkg_name}/german
%lang(el) %{_datadir}/%{pkg_name}/greek
%lang(hi) %{_datadir}/%{pkg_name}/hindi
%lang(hu) %{_datadir}/%{pkg_name}/hungarian
%lang(it) %{_datadir}/%{pkg_name}/italian
%lang(ja) %{_datadir}/%{pkg_name}/japanese
%lang(ko) %{_datadir}/%{pkg_name}/korean
%lang(no) %{_datadir}/%{pkg_name}/norwegian
%lang(no) %{_datadir}/%{pkg_name}/norwegian-ny
%lang(pl) %{_datadir}/%{pkg_name}/polish
%lang(pt) %{_datadir}/%{pkg_name}/portuguese
%lang(ro) %{_datadir}/%{pkg_name}/romanian
%lang(ru) %{_datadir}/%{pkg_name}/russian
%lang(sr) %{_datadir}/%{pkg_name}/serbian
%lang(sk) %{_datadir}/%{pkg_name}/slovak
%lang(es) %{_datadir}/%{pkg_name}/spanish
%lang(sv) %{_datadir}/%{pkg_name}/swedish
%lang(uk) %{_datadir}/%{pkg_name}/ukrainian
%endif


%files server
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log
%{_bindir}/mariadb-service-convert
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/my_print_defaults
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysqld_safe
%{_bindir}/innochecksum
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip
# wsrep_sst_common should be moved to /usr/share/mariadb: https://jira.mariadb.org/browse/MDEV-14296
%{_bindir}/wsrep_*

%config(noreplace) %{_sysconfdir}/my.cnf.d/%{pkg_name}-server.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/enable_encryption.preset

%{_libexecdir}/mysqld

%dir %{_libdir64}/%{pkg_name}
%dir %{_libdir64}/%{pkg_name}/plugin
%{_libdir64}/%{pkg_name}/plugin/*
%if "%{connect}" != "NO"
%exclude %{_libdir64}/%{pkg_name}/plugin/ha_connect.so
%endif
%if "%{cracklib}" != "NO"
%exclude %{_libdir64}/%{pkg_name}/plugin/cracklib_password_check.so
%endif
%if "%{gssapi}" != "NO"
%exclude %{_libdir64}/%{pkg_name}/plugin/auth_gssapi.so
%endif

%{_mandir}/man1/aria_chk.1*
%{_mandir}/man1/aria_dump_log.1*
%{_mandir}/man1/aria_ftdump.1*
%{_mandir}/man1/aria_pack.1*
%{_mandir}/man1/aria_read_log.1*
%{_mandir}/man1/galera_new_cluster.1*
%{_mandir}/man1/galera_recovery.1*
%{_mandir}/man1/mariadb-service-convert.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqld_safe_helper.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man8/mysqld.8*
%{_mandir}/man1/wsrep_*.1*

%{_datadir}/%{pkg_name}/fill_help_tables.sql
%if %{spider} != "NO"
%{_datadir}/%{pkg_name}/install_spider.sql
%endif
%{_datadir}/%{pkg_name}/maria_add_gis_sp.sql
%{_datadir}/%{pkg_name}/maria_add_gis_sp_bootstrap.sql
%{_datadir}/%{pkg_name}/mysql_system_tables.sql
%{_datadir}/%{pkg_name}/mysql_system_tables_data.sql
%{_datadir}/%{pkg_name}/mysql_test_data_timezone.sql
%{_datadir}/%{pkg_name}/mysql_to_mariadb.sql
%{_datadir}/%{pkg_name}/mysql_performance_tables.sql
%{_datadir}/%{pkg_name}/mysql_test_db.sql

%{_libexecdir}/mysql-prepare-db-dir.sh
%{_libexecdir}/mysql-check-socket.sh
%{_libexecdir}/mysql-check-upgrade.sh
%{_libexecdir}/mysql-scripts-common.sh

%attr(0755,mysql,mysql) %dir %{dbdatadir}
%attr(0750,mysql,mysql) %dir %{logfiledir}
# This does what it should.
# RPMLint error "conffile-without-noreplace-flag /opt/var/log/mariadb/mariadb.log" is false positive.
%attr(0640,mysql,mysql) %config %ghost %verify(not md5 size mtime) %{logfile}

%if "%{cracklib}" != "NO"
%files cracklib-password-check
%config(noreplace) %{_sysconfdir}/my.cnf.d/cracklib_password_check.cnf
%{_libdir64}/%{pkg_name}/plugin/cracklib_password_check.so
%endif

%if "%{backup}" == "ON"
%files backup
%{_bindir}/mariabackup
%{_bindir}/mbstream
%{_mandir}/man1/mariabackup.1*
%{_mandir}/man1/mbstream.1*
%endif

%if "%{gssapi}" != "NO"
%files gssapi-server
%{_libdir64}/%{pkg_name}/plugin/auth_gssapi.so
# TODO: No cnf file.
#%config(noreplace) %{_sysconfdir}/my.cnf.d/auth_gssapi.cnf
%endif

%if "%{connect}" == "DYNAMIC"
%files connect-engine
%config(noreplace) %{_sysconfdir}/my.cnf.d/connect.cnf
%{_libdir64}/%{pkg_name}/plugin/ha_connect.so
%endif

%files server-utils
# Perl utilities
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_setpermission
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqlhotcopy
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysql_setpermission.1*
# Utilities that can be used remotely
%{_bindir}/mysql_upgrade
%{_bindir}/perror
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/perror.1*
# Other utilities
%{_bindir}/mysqld_safe_helper

%files devel
%{_includedir}/*
%exclude %{_includedir}/mysql/mysql
%exclude %{_includedir}/mysql/mysql/client_plugin.h
%exclude %{_includedir}/mysql/mysql/plugin_auth.h
%exclude %{_includedir}/mysql/mysql/plugin_auth_common.h

%exclude %{_datadir}/aclocal/mysql.m4
%exclude %{_libdir64}/pkgconfig/mariadb.pc

%if "%{embedded}" != "NO"
%files embedded
%{_libdir}/libmariadbd.a
%{_libdir}/libmysqld.a
%{_libdir64}/libmariadbd.a
%{_libdir64}/libmysqld.a
%{_libdir64}/libmariadbd.so.%{so_mariadbd}
%{_libdir64}/libmysqld.so.%{so_mariadbd}
%endif

%if "%{bench}" == "1"
%files bench
%{_datadir}/sql-bench
%doc %{_datadir}/sql-bench/README
%endif

%files test
%if "%{embedded}" != "NO"
%{_bindir}/test-connect-t
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*
%endif
%{_bindir}/mysql_client_test
%if %{with dotests}
%{_bindir}/my_safe_process
%{_mandir}/man1/my_safe_process.1*
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%endif
%{_bindir}/mysqltest
%{_mandir}/man1/mysql_client_test.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*

%changelog
* Fri Sep 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 10.4.7-1
- New version 10.4.7
- Provides more plugin
- Build and tested on debug and release mode
- Erase all systemd files.
- Update default location of config files (now /opt/freeware/var/lib/mysql)

* Mon Jul 29 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 10.4.6-1
- New version 10.4.6
- Compiles more plugins
- Compiles unittest
- Provides tests and bench packages

* Wed Jun 19 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 10.3.15-2beta
- Innodb is available.
- Uses GNU iconv.

* Wed Jun 05 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 10.3.15-1beta
- New version 10.3.15
- Provides archive

* Thu Mar 21 2019 Tony Reix <tony.reix@atos.net> - 10.3.12-1beta
- Move to 10.3.12 with new CMake

* Mon Dec 17 2018 Pascal Emmendoerffer <pascal.emmendoerffer@atos.net> - 3:10.3.10Beta-1
- Adaptation for AIX 7.2 with RPMV4
- only .so files are delivered in rpms (without lib*.a)

* Fri Oct 05 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.10-1
- Rebase to 10.3.10

* Tue Sep 04 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.9-2
- Fix parallel installability of x86_64 and i686 devel packages

* Mon Aug 20 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.9-1
- Rebase to 10.3.9

* Fri Aug 10 2018 Petr Lautrbach <plautrba@redhat.com> - 3:10.3.8-5
- Update mariadb-server-galera sub-package to require the correct package with /usr/sbin/semanage

* Wed Jul 25 2018 Honza Horak <hhorak@redhat.com> - 3:10.3.8-4
- Do not build config on systems where mariadb-connector-c-config exists instead

* Tue Jul 17 2018 Honza Horak <hhorak@redhat.com> - 3:10.3.8-3
- Move config files mysql-clients.cnf and enable_encryption.preset to correct
  sub-packages, similar to what upstream does

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.8-1
- Rebase to 10.3.8
- Build TokuDB with jemalloc

* Wed Jun 27 2018 Michal Schorm <mschorm@redhat.com> - 3:10.3.7-2
- Rebase to 10.3.7
- Remove the galera obsoletes

* Tue Jun 05 2018 Honza Horak <hhorak@redhat.com> - 3:10.2.15-2
- Use mysqladmin for checking the socket
- Jemalloc dependency moved to the TokuDB subpackage.
  CMake jemalloc option removed, not used anymore.
  The server doesn't need jemalloc since 10.2: https://jira.mariadb.org/browse/MDEV-11059
- Build MariaDB with TokuDB without Jemalloc.

* Wed May 23 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.15-1
- Rebase to 10.2.15
- CVEs fixed: #1568962
  CVE-2018-2755 CVE-2018-2761 CVE-2018-2766 CVE-2018-2771 CVE-2018-2781
  CVE-2018-2782 CVE-2018-2784 CVE-2018-2787 CVE-2018-2813 CVE-2018-2817
  CVE-2018-2819 CVE-2018-2786 CVE-2018-2759 CVE-2018-2777 CVE-2018-2810

* Thu Mar 29 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.14-1
- Rebase to 10.2.14
- Update testsuite run for SSL self signed certificates

* Tue Mar 6 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.13-2
- Further fix of ldconfig scriptlets for F27
- Fix hardcoded paths, move unversioned libraries and symlinks to the devel subpackage

* Thu Mar 1 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.13-1
- Rebase to 10.2.13

* Mon Feb 26 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-8
- SPECfile refresh, RHEL6, SySV init and old fedora stuff removed

* Sun Feb 25 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-7
- Rebuilt for ldconfig_post and ldconfig_postun bug
  Related: #1548331

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-5
- Use '-ldl' compiler flag when associated library used
  Resolves: #1538990

* Thu Jan 25 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-4
- Fix the upgrade path. Build TokuDB subpackage again, but build a unsupported
  configuration by upstream (without Jemalloc).
  Jemmalloc has been updated to version 5, which isn't backwards compatible.
- Use downstream tmpfiles instead of the upstream one
  Related: #1538066

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3:10.2.12-3
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Honza Horak <hhorak@redhat.com> - 3:10.2.12-1
- Do not build connect plugin with mongo and jdbc connectors
- Support MYSQLD_OPTS and _WSREP_NEW_CLUSTER env vars in init script,
  same as it is done in case of systemd unit file
  Related: #1455850
- Print the same messages as before when starting the service in SysV init,
  to not scare users
  Related: #1463411

* Wed Jan 10 2018 Michal Schorm <mschorm@redhat.com> - 3:10.2.12-1
- Rebase to 10.2.12
- Temporary fix for https://jira.mariadb.org/browse/MDEV-14537 removed
- TokuDB disabled

* Mon Dec 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.11-2
- Temporary fix for #1523875 removed, bug in Annobin fixed
  Resolves: #1523875

* Sat Dec 09 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.11-1
- Rebase to 10.2.11
- Temporary fix for https://jira.mariadb.org/browse/MDEV-14537 introduced
- Temporary fix for #1523875 intoruced
  Related: #1523875

* Wed Dec 06 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.10-2
- Fix PID file location
  Related: #1483331, #1515779
- Remove 'Group' tags as they should not be used any more
  Related: https://fedoraproject.org/wiki/RPMGroups

* Mon Nov 20 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.10-1
- Rebase to 10.2.10 version
- Patch 2: mariadb-install-test.patch has been incorporated by upstream
- Patch 8: mariadb-install-db-sharedir.patch; upstream started to use macros
- Update PCRE check
- Start using location libdir/mariadb for plugins
- Move libraries to libdir
- Divided to more sub-packages to match upstream's RPM list
  Resolves: #1490401; #1400463
- Update of Cmake arguments to supported format
  Related: https://lists.launchpad.net/maria-discuss/msg04852.html
- Remove false Provides

* Thu Oct 05 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-3
- Fix client library obsolete
  Related: #1498956
- Enable testsuite again
- RPMLint error fix:
  Remove unused python scripts which remained from TokuDB upstream
- RPMLint error fix: description line too long

* Wed Oct 04 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-2
- Fix of "with" and "without" macros, so they works
- Use 'iproute' dependency instead of 'net-tools'
  Related: #1496131
- Set server package to own /usr/lib64/mysql directory
- Use correct obsolete, so upgrade from maridb 10.1 to 10.2 is possible
  with dnf "--allowerasing" option
  Related: #1497234
- Fix building with client library

* Thu Sep 28 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.9-1
- Rebase to 10.2.9
- Testsuite temorarly disabled in order to fast deploy critical fix
  Related: #1497234

* Wed Sep 20 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.8-5
- Fix building without client library part
- Start building mariadb without client library part,
  use mariadb-connector-c package >= 3.0 instead
- Use obosletes of "-libs" in "-common", if built without client library part

* Mon Aug 28 2017 Honza Horak <hhorak@redhat.com> - 3:10.2.8-2
- Fix paths in galera_recovery and galera_new_cluster
  Resolves: #1403416
- Support --defaults-group-suffix properly in systemd unit file
  Resolves: #1485777
- Allow 4567 port for tcp as well
- Install mysql-wait-ready on RHEL-6 for the SysV init
- Run mysql-prepare-db-dir as non-root
- Sync mysql.init with community-mysql

* Sun Aug 20 2017 Honza Horak <hhorak@redhat.com> - 3:10.2.8-1
- Rebase to 10.2.8

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.7-6
- Revert previous change, go back to libmariadb headers (RHBZ #1474764)

* Fri Jul 21 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.7-5
- Install correct headers (server, not client) - MDEV-13370

* Wed Jul 19 2017 Jonathan Wakely <jwakely@redhat.com> - 3:10.2.7-4
- Rebuilt for s390x binutils bug

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 3:10.2.7-3
- Rebuilt for Boost 1.64

* Thu Jul 13 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.7-2
- Remove mysql-wait-* scripts. They aren't needed when using systemd "Type=notify"

* Thu Jul 13 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.7-1
- Rebase to 10.2.7
- Get back mysql_config, its "--libmysqld-libs" is still needed

* Wed Jul 12 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.6-4
- Add manual Provides: for the libmysqlcient compat symlink

* Wed Jul 12 2017 Adam Williamson <awilliam@redhat.com> - 3:10.2.6-3
- Move libmysqlclient.so.18 compat link to -libs subpackage

* Tue Jul 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.6-2
- Disable Dtrace
- Disable Sphinx, circural dependency

* Tue Jul 11 2017 Michal Schorm <mschorm@redhat.com> - 3:10.2.6-1
- Rebase to 10.2.6
- SSL patch removed
- 'libmariadb.so.3' replaced 'limysqlclient.so.18.0.0', symlinks provided
- "make test" removed, it needs running server and same test are included in the testsuite

* Mon Jul 10 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.25-1
- Rebase to 10.1.25
- Disable plugins 'cracklib' and 'gssapi' by default
- Related: #1468028, #1464070
- Looks like the testsuite removes its 'var' content correctly,
  no need to do that explicitly.

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 3:10.1.24-5
- Rebuild due to bug in RPM (RHBZ #1468476)

* Mon Jun 19 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-4
- Use "/run" location instead of "/var/run" symlink
- Related: #1455811
- Remove AppArmor files

* Fri Jun 09 2017 Honza Horak <hhorak@redhat.com> - 3:10.1.24-3
- Downstream script mariadb-prepare-db-dir fixed for CVE-2017-3265
- Resolves: #1458940
- Check properly that datadir includes only expected files
- Related: #1356897

* Wed Jun 07 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-2
- Fixed incorrect Jemalloc initialization; #1459671

* Fri Jun 02 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.24-1
- Rebase to 10.1.24
- Build dependecies Bison and Libarchive added, others corrected
- Disabling Mroonga engine for i686 architecture, as it is not supported by MariaDB
- Removed patches: (fixed by upstream)
    #{Patch5:  mariadb-file-contents.patch
    #Patch14: mariadb-example-config-files.patch
    #Patch31: mariadb-string-overflow.patch
    #Patch32: mariadb-basedir.patch
    #Patch41: mariadb-galera-new-cluster-help.patch
- Resolves: rhbz#1414387
    CVE-2017-3313
- Resolves partly: rhbz#1443408
    CVE-2017-3308 CVE-2017-3309 CVE-2017-3453 CVE-2017-3456 CVE-2017-3464

* Tue May 23 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-6
- Plugin oqgraph enabled
- Plugin jemalloc enabled
- 'force' option for 'rm' removed
- Enabled '--big-test' option for the testsuite
- Disabled '--skip-rpl' option for the testsuite = replication tests enabled
- Multilib manpage added

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:10.1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Mar 07 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-4
- Cracklib plugin enabled
- Removed strmov patch, it is no longer needed. The issue was fixed long ago in both MariaDB and MySQL

* Wed Feb 15 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-3
- Fix for some RPMLint issues
- Fix: Only server utilities can be move to server-utils subpackage. The rest (from client)
  were moved back to where they came from (client - the main subpackage)
- Added correct "Obsoletes" for the server-utils subpackage
- Fixed FTBFS in F26 on x86_64, because of -Werror option
- Related: #1421092, #1395127

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:10.1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Michal Schorm <mschorm@redhat.com> - 3:10.1.21-1
- Rebase to version 10.1.21
- Most of the non-essential utilites has been moved to the new sub-package mariadb-server-utils
- Patches "admincrash" and "errno" removed, they are no longer relevant
  "mysql-embedded-check.c" removed, no longer relevant
- Buildrequires krb5-devel duplicity removed
- Manpage for mysql_secure_installation extended
- Preparation for the CrackLib plugin to be added (waiting for correct SELinux rules to be relased)
- Related: #1260821, #1205082, #1414387

* Tue Jan 03 2017 Honza Horak <hhorak@redhat.com> - 3:10.1.20-3
- Add explicit EVR requirement in main package for -libs
- Related: #1406320

* Tue Dec 20 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.20-2
- Use correct macro when removing doc files
- Resolves: #1400981

* Sat Dec 17 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.20-1
- Rebase to version 10.1.20
- Related: #1405258

* Fri Dec 02 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-6
- Move patch from specfile to standalone patch file
- Related: #1382988

* Thu Dec 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 3:10.1.19-6
- -devel: use pkgconfig(openssl) to allow any implementation (like compat-openssl10)

* Wed Nov 30 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-5
- Testsuite blacklists heavily updated. Current tracker: #1399847
- Log-error option added to all config files examples
- Resolves: #1382988

* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-4
- JdbcMariaDB.jar test removed
- PCRE version check added
- Related: #1382988, #1396945, #1096787

* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-4
- test suite ENABLED, consensus was made it still should be run every build

* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-2
- fixed bug 1382988
- added comment to the test suite
- test suite DISABLED for most builds in Koji, see comments

* Wed Nov 16 2016 Michal Schorm <mschorm@redhat.com> - 3:10.1.19-1
- Update to 10.1.19
- added temporary support to build with OpenSSL 1.0 on Fedora >= 26
- added krb5-devel pkg as Buldrquires to prevent gssapi failure

* Tue Oct  4 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.18-1
- Update to 10.1.18

* Wed Aug 31 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.17-1
- Update to 10.1.17

* Mon Aug 29 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.16-2
- Fixed galera replication
- Resolves: #1352946

* Tue Jul 19 2016 Jakub Dorňák <jdornak@redhat.com> - 3:10.1.16-1
- Update to 10.1.16

* Fri Jul 15 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.14-5
- Fail build when test-suite fails
- Use license macro for inclusion of licenses

* Thu Jul 14 2016 Honza Horak <hhorak@redhat.com> - 3:10.1.14-4
- Revert Update to 10.1.15, this release is broken
  https://lists.launchpad.net/maria-discuss/msg03691.html

* Thu Jul 14 2016 Honza Horak <hhorak@redhat.com> - 2:10.1.15-3
- Check datadir more carefully to avoid unwanted data corruption
- Related: #1335849

* Thu Jul  7 2016 Jakub Dorňák <jdornak@redhat.com> - 2:10.1.15-2
- Bump epoch
  (related to the downgrade from the pre-release version)

* Fri Jul  1 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.15-1
- Update to 10.1.15

* Fri Jul  1 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.14-3
- Revert "Update to 10.2.0"
  It is possible that MariaDB 10.2.0 won't be stable till f25 GA.

* Tue Jun 21 2016 Pavel Raiskup <praiskup@redhat.com> - 1:10.1.14-3
- BR multilib-rpm-config and use it for multilib workarounds
- install architecture dependant pc file to arch-dependant location

* Thu May 26 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.2.0-2
- Fix mysql-prepare-db-dir
- Resolves: #1335849

* Thu May 12 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.2.0-1
- Update to 10.2.0

* Thu May 12 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.14-1
- Add selinux policy
- Update to 10.1.14 (includes various bug fixes)
- Add -h and --help options to galera_new_cluster

* Thu Apr  7 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-3
- wsrep_on in galera.cnf

* Tue Apr  5 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-2
- Moved /etc/sysconfig/clustercheck
  and /usr/share/mariadb/systemd/use_galera_new_cluster.conf
  to mariadb-server-galera

* Tue Mar 29 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.13-1
- Update to 10.1.13

* Wed Mar 23 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-4
- Fixed conflict with mariadb-galera-server

* Tue Mar 22 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-3
- Add subpackage mariadb-server-galera
- Resolves: 1310622

* Tue Mar 01 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.12-2
- Rebuild for BZ#1309199 (symbol versioning)

* Mon Feb 29 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.12-1
- Update to 10.1.12

* Tue Feb 16 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-9
- Remove dangling symlink to /etc/init.d/mysql

* Sat Feb 13 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-8
- Use epoch for obsoleting mariadb-galera-server

* Fri Feb 12 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-7
- Add Provides: bundled(pcre) in case we build with bundled pcre
- Related: #1302296
- embedded-devel should require libaio-devel
- Resolves: #1290517

* Fri Feb 12 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-6
- Fix typo s/obsolate/obsolete/

* Thu Feb 11 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-5
- Add missing requirements for proper wsrep functionality
- Obsolate mariadb-galera & mariadb-galera-server (thanks Tomas Repik)
- Resolves: #1279753
- Re-enable using libedit, which should be now fixed
- Related: #1201988
- Remove mariadb-wait-ready call from systemd unit, we have now systemd notify support
- Make mariadb@.service similar to mariadb.service

* Mon Feb 08 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-4
- Use systemd unit file more compatible with upstream

* Sun Feb 07 2016 Honza Horak <hhorak@redhat.com> - 1:10.1.11-3
- Temporarily disabling oqgraph for
  https://mariadb.atlassian.net/browse/MDEV-9479

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:10.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Feb  3 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.11-1
- Update to 10.1.11

* Tue Jan 19 2016 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.10-1
- Update to 10.1.10

* Mon Dec 07 2015 Dan Horák <dan[at]danny.cz> - 1:10.1.8-3
- rebuilt for s390(x)

* Tue Nov 03 2015 Honza Horak <hhorak@redhat.com> - 1:10.1.8-2
- Expand variables in server.cnf

* Thu Oct 22 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.1.8-1
- Update to 10.1.8

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1:10.0.21-2
- Rebuilt for Boost 1.59

* Mon Aug 10 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.21-1
- Update to 10.0.21

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1:10.0.20-2
- rebuild for Boost 1.58

* Tue Jun 23 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.20-1
- Update to 10.0.20

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Dan Horák <dan[at]danny.cz> - 1:10.0.19-2
- Update lists of failing tests (jdornak)
- Related: #1149647

* Mon May 11 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.19-1
- Update to 10.0.19

* Thu May 07 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.18-1
- Update to 10.0.18

* Thu May 07 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-4
- Include client plugins into -common package since they are used by both -libs
  and base packages.
- Do not use libedit
- Related: #1201988
- Let plugin dir to be owned by -common
- Use correct comment in the init script
- Related: #1184604
- Add openssl as BuildRequires to run some openssl tests during build
- Related: #1189180
- Fail in case any command in check fails
- Related: #1124791
- Fix mysqladmin crash if run with -u root -p
- Resolves: #1207170

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:10.0.17-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 06 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-2
- Wait for daemon ends
- Resolves: #1072958
- Do not include symlink to libmysqlclient if not shipping the library
- Do not use scl prefix more than once in paths
  Based on https://www.redhat.com/archives/sclorg/2015-February/msg00038.html

* Wed Mar 04 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.17-1
- Rebase to version 10.0.17
- Added variable for turn off skipping some tests

* Tue Mar 03 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.16-6
- Check permissions when starting service on RHEL-6
- Resolves: #1194699
- Do not create test database by default
- Related: #1194611

* Fri Feb 13 2015 Matej Muzila <mmuzila@redhat.com> - 1:10.0.16-4
- Enable tokudb

* Tue Feb 10 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.16-3
- Fix openssl_1 test

* Wed Feb  4 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.16-2
- Include new certificate for tests
- Update lists of failing tests
- Related: #1186110

* Tue Feb  3 2015 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.16-9
- Rebase to version 10.0.16
- Resolves: #1187895

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1:10.0.15-9
- Rebuild for boost 1.57.0

* Mon Jan 26 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-8
- Fix typo in the config file

* Sun Jan 25 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-7
- Do not create log file in post script

* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-6
- Move server settings to config file under my.cnf.d dir

* Sat Jan 24 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-5
- Fix path for sysconfig file
  Filter provides in el6 properly
  Fix initscript file location

* Tue Jan 06 2015 Honza Horak <hhorak@redhat.com> - 1:10.0.15-4
- Disable failing tests connect.mrr, connect.updelx2 on ppc and s390

* Mon Dec 22 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.15-3
- Fix macros paths in my.cnf
- Create old location for pid file if it remained in my.cnf

* Fri Dec 05 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.15-2
- Rework usage of macros and remove some compatibility artefacts

* Thu Nov 27 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.15-1
- Update to 10.0.15

* Thu Nov 20 2014 Jan Stanek <jstanek@redhat.com> - 1:10.0.14-8
- Applied upstream fix for mysql_config --cflags output.
- Resolves: #1160845

* Fri Oct 24 2014 Jan Stanek <jstanek@redhat.com> - 1:10.0.14-7
- Fixed compat service file.
- Resolves: #1155700

* Mon Oct 13 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-6
- Remove bundled cmd-line-utils
- Related: #1079637
- Move mysqlimport man page to proper package
- Disable main.key_cache test on s390
  Releated: #1149647

* Wed Oct 08 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-5
- Disable tests connect.part_file, connect.part_table
  and connect.updelx
- Related: #1149647

* Wed Oct 01 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-4
- Add bcond_without mysql_names
  Use more correct path when deleting mysql logrotate script

* Wed Oct 01 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-3
- Build with system libedit
- Resolves: #1079637

* Mon Sep 29 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-2
- Add with_debug option

* Mon Sep 29 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.14-1
- Update to 10.0.14

* Wed Sep 24 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-8
- Move connect engine to a separate package
  Rename oqgraph engine to align with upstream packages
- Move some files to correspond with MariaDB upstream packages
  client.cnf into -libs, mysql_plugin and msql2mysql into base,
  tokuftdump and aria_* into -server, errmsg-utf8.txt into -errmsg
- Remove duplicate cnf files packaged using %%doc
- Check upgrade script added to warn about need for mysql_upgrade

* Wed Sep 24 2014 Matej Muzila <mmuzila@redhat.com> - 1:10.0.13-7
- Client related libraries moved from mariadb-server to mariadb-libs
- Related: #1138843

* Mon Sep 08 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-6
- Disable vcol_supported_sql_funcs_myisam test on all arches
- Related: #1096787
- Install systemd service file on RHEL-7+
  Server requires any mysql package, so it should be fine with older client

* Thu Sep 04 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-5
- Fix paths in mysql_install_db script
- Resolves: #1134328
- Use %%cmake macro

* Tue Aug 19 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-4
- Build config subpackage everytime
- Disable failing tests: innodb_simulate_comp_failures_small, key_cache
  rhbz#1096787

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-2
- Include mysqld_unit only if required; enable tokudb in f20-

* Wed Aug 13 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.13-1
- Rebase to version 10.0.13

* Tue Aug 12 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-8
- Introduce -config subpackage and ship base config files here

* Tue Aug  5 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-7
- Adopt changes from mysql, thanks Bjorn Munch <bjorn.munch@oracle.com>

* Mon Jul 28 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-6
- Use explicit sysconfdir
- Absolut path for default value for pid file and error log

* Tue Jul 22 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-5
- Hardcoded paths removed to work fine in chroot
- Spec rewrite to be more similar to oterh MySQL implementations
- Use variable for daemon unit name
- Include SysV init script if built on older system
- Add possibility to not ship some sub-packages

* Mon Jul 21 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-4
- Reformating spec and removing unnecessary snippets

* Tue Jul 15 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.12-3
- Enable OQGRAPH engine and package it as a sub-package
- Add support for TokuDB engine for x86_64 (currently still disabled)
- Re-enable tokudb_innodb_xa_crash again, seems to be fixed now
- Drop superfluous -libs and -embedded ldconfig deps (thanks Ville Skyttä)
- Separate -lib and -common sub-packages
- Require /etc/my.cnf instead of shipping it
- Include README.mysql-cnf
- Multilib support re-worked
- Introduce new option with_mysqld_unit
- Removed obsolete mysql-cluster, the package should already be removed
- Improve error message when log file is not writable
- Compile all binaries with full RELRO (RHBZ#1092548)
- Use modern symbol filtering with compatible backup
- Add more groupnames for server's my.cnf
- Error messages now provided by a separate package (thanks Alexander Barkov)
- Expand paths in helper scripts using cmake

* Wed Jun 18 2014 Mikko Tiihonen <mikko.tiihonen@iki.fi> - 1:10.0.12-2
- Use -fno-delete-null-pointer-checks to avoid segfaults with gcc 4.9

* Tue Jun 17 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.12-1
- Rebase to version 10.0.12

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:10.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.11-4
- rebuild with tests failing on different arches disabled (#1096787)

* Thu May 29 2014 Dan Horák <dan[at]danny.cz> - 1:10.0.11-2
- rebuild with tests failing on big endian arches disabled (#1096787)

* Wed May 14 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.11-1
- Rebase to version 10.0.11

* Mon May 05 2014 Honza Horak <hhorak@redhat.com> - 1:10.0.10-3
- Script for socket check enhanced

* Thu Apr 10 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.10-2
- use system pcre library

* Thu Apr 10 2014 Jakub Dorňák <jdornak@redhat.com> - 1:10.0.10-1
- Rebase to version 10.0.10

* Wed Mar 12 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.36-2
- Server crashes on SQL select containing more group by and left join statements using innodb tables
- Resolves: #1065676
- Fix paths in helper scripts
- Move language files into mariadb directory

* Thu Mar 06 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.36-1
- Rebase to 5.5.36
  https://kb.askmonty.org/en/mariadb-5536-changelog/

* Tue Feb 25 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-5
- Daemon helper scripts sanity changes and spec files clean-up

* Tue Feb 11 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-4
- Fix typo in mysqld.service
- Resolves: #1063981

* Wed Feb  5 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-3
- Do not touch the log file in post script, so it does not get wrong owner
- Resolves: #1061045

* Thu Jan 30 2014 Honza Horak <hhorak@redhat.com> 1:5.5.35-1
- Rebase to 5.5.35
  https://kb.askmonty.org/en/mariadb-5535-changelog/
  Also fixes: CVE-2014-0001, CVE-2014-0412, CVE-2014-0437, CVE-2013-5908,
  CVE-2014-0420, CVE-2014-0393, CVE-2013-5891, CVE-2014-0386, CVE-2014-0401,
  CVE-2014-0402
- Resolves: #1054043
- Resolves: #1059546

* Tue Jan 14 2014 Honza Horak <hhorak@redhat.com> - 1:5.5.34-9
- Adopt compatible system versioning
- Related: #1045013
- Use compatibility mysqld.service instead of link
- Related: #1014311

* Mon Jan 13 2014 Rex Dieter <rdieter@fedoraproject.org> 1:5.5.34-8
- move mysql_config alternatives scriptlets to -devel too

* Fri Jan 10 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-7
- Build with -O3 on ppc64
- Related: #1051069
- Move mysql_config to -devel sub-package and remove Require: mariadb
- Related: #1050920

* Fri Jan 10 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 1:5.5.34-6
- Disable main.gis-precise test also for AArch64
- Disable perfschema.func_file_io and perfschema.func_mutex for AArch64
  (like it is done for 32-bit ARM)

* Fri Jan 10 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-5
- Clean all non-needed doc files properly

* Wed Jan  8 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-4
- Read socketfile location in mariadb-prepare-db-dir script

* Mon Jan  6 2014 Honza Horak <hhorak@redhat.com> 1:5.5.34-3
- Don't test EDH-RSA-DES-CBC-SHA cipher, it seems to be removed from openssl
  which now makes mariadb/mysql FTBFS because openssl_1 test fails
- Related: #1044565
- Use upstream's layout for symbols version in client library
- Related: #1045013
- Check if socket file is not being used by another process at a time
  of starting the service
- Related: #1045435
- Use %%ghost directive for the log file
- Related: 1043501

* Wed Nov 27 2013 Honza Horak <hhorak@redhat.com> 1:5.5.34-2
- Fix mariadb-wait-ready script

* Fri Nov 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.34-1
- Rebase to 5.5.34

* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-4
- Fix spec file to be ready for backport by Oden Eriksson
- Resolves: #1026404

* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-3
- Add pam-devel to build-requires in order to build
- Related: #1019945
- Check if correct process is running in mysql-wait-ready script
- Related: #1026313

* Mon Oct 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-2
- Turn on test suite

* Thu Oct 10 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-1
- Rebase to 5.5.33a
  https://kb.askmonty.org/en/mariadb-5533-changelog/
  https://kb.askmonty.org/en/mariadb-5533a-changelog/
- Enable outfile_loaddata test
- Disable tokudb_innodb_xa_crash test

* Mon Sep  2 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-12
- Re-organize my.cnf to include only generic settings
- Resolves: #1003115
- Move pid file location to /var/run/mariadb
- Make mysqld a symlink to mariadb unit file rather than the opposite way
- Related: #999589

* Thu Aug 29 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-11
- Move log file into /var/log/mariadb/mariadb.log
- Rename logrotate script to mariadb
- Resolves: #999589

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1:5.5.32-10
- fix alternatives usage

* Tue Aug 13 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-9
- Multilib issues solved by alternatives
- Resolves: #986959

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.32-8
- Perl 5.18 rebuild

* Wed Jul 31 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-7
- Do not use login shell for mysql user

* Tue Jul 30 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-6
- Remove unneeded systemd-sysv requires
- Provide mysql-compat-server symbol
- Create mariadb.service symlink
- Fix multilib header location for arm
- Enhance documentation in the unit file
- Use scriptstub instead of links to avoid multilib conflicts
- Add condition for doc placement in F20+

* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 1:5.5.32-5
- remove "Requires(pretrans): systemd" since its not possible
- when installing mariadb and systemd at the same time. as in a new install

* Sat Jul 27 2013 Kevin Fenzi <kevin@scrye.com> 1:5.5.32-4
- Set rpm doc macro to install docs in unversioned dir

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-3
- add Requires(pre) on systemd for the server package

* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-2
- replace systemd-units requires with systemd
- remove solaris files

* Fri Jul 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.32-1
- Rebase to 5.5.32
  https://kb.askmonty.org/en/mariadb-5532-changelog/
- Clean-up un-necessary systemd snippets

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.31-7
- Perl 5.18 rebuild

* Mon Jul  1 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-6
- Test suite params enhanced to decrease server condition influence
- Fix misleading error message when uninstalling built-in plugins
- Related: #966873

* Thu Jun 27 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-5
- Apply fixes found by Coverity static analysis tool

* Wed Jun 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-4
- Do not use pretrans scriptlet, which doesn't work in anaconda
- Resolves: #975348

* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-3
- Explicitly enable mysqld if it was enabled in the beginning
  of the transaction.

* Thu Jun 13 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-2
- Apply man page fix from Jan Stanek

* Fri May 24 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-1
- Rebase to 5.5.31
  https://kb.askmonty.org/en/mariadb-5531-changelog/
- Preserve time-stamps in case of installed files
- Use /var/tmp instead of /tmp, since the later is using tmpfs,
  which can cause problems
- Resolves: #962087
- Fix test suite requirements

* Sun May  5 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-2
- Remove mytop utility, which is packaged separately
- Resolve multilib conflicts in mysql/private/config.h

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-1
- Rebase to 5.5.30
  https://kb.askmonty.org/en/mariadb-5530-changelog/

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-11
- Obsolete MySQL since it is now renamed to community-mysql
- Remove real- virtual names

* Thu Mar 21 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-10
- Adding epoch to have higher priority than other mysql implementations
  when comes to provider comparison

* Wed Mar 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-9
- Let mariadb-embedded-devel conflict with MySQL-embedded-devel
- Adjust mariadb-sortbuffer.patch to correspond with upstream patch

* Mon Mar  4 2013 Honza Horak <hhorak@redhat.com> 5.5.29-8
- Mask expected warnings about setrlimit in test suite

* Thu Feb 28 2013 Honza Horak <hhorak@redhat.com> 5.5.29-7
- Use configured prefix value instead of guessing basedir
  in mysql_config
- Resolves: #916189
- Export dynamic columns and non-blocking API functions documented
  by upstream

* Wed Feb 27 2013 Honza Horak <hhorak@redhat.com> 5.5.29-6
- Fix sort_buffer_length option type

* Wed Feb 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-5
- Suppress warnings in tests and skip tests also on ppc64p7

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-4
- Suppress warning in tests on ppc
- Enable fixed index_merge_myisam test case

* Thu Feb 07 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Packages need to provide also %%_isa version of mysql package
- Provide own symbols with real- prefix to distinguish from mysql
  unambiguously
- Fix format for buffer size in error messages (MDEV-4156)
- Disable some tests that fail on ppc and s390
- Conflict only with real-mysql, otherwise mariadb conflicts with ourself

* Tue Feb 05 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Let mariadb-libs to own /etc/my.cnf.d

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.29-1
- Rebase to 5.5.29
  https://kb.askmonty.org/en/mariadb-5529-changelog/
- Fix inaccurate default for socket location in mysqld-wait-ready
- Resolves: #890535

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-8
- Enable obsoleting mysql

* Wed Jan 30 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-7
- Adding necessary hacks for perl dependency checking, rpm is still
  not wise enough
- Namespace sanity re-added for symbol default_charset_info

* Mon Jan 28 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-6
- Removed %%{_isa} from provides/obsoletes, which doesn't allow
  proper obsoleting
- Do not obsolete mysql at the time of testing

* Thu Jan 10 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-5
- Added licenses LGPLv2 and BSD
- Removed wrong usage of %%{epoch}
- Test-suite is run in %%check
- Removed perl dependency checking adjustment, rpm seems to be smart enough
- Other minor spec file fixes

* Tue Dec 18 2012 Honza Horak <hhorak@redhat.com> 5.5.28a-4
- Packaging of MariaDB based on MySQL package

