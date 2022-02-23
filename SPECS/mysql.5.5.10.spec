# ----------------------------------------------------------------------------
# Source name
# ----------------------------------------------------------------------------
%define mysql_old_vendor        MySQL AB
%define mysql_vendor_2          Sun Microsystems, Inc.
%define mysql_vendor            Oracle and/or its affiliates
%define src_base mysql
%define mysql_version   5.5.10
%define src_dir %{src_base}-%{mysql_version}
%define release         1
%define mysqld_user    mysql
%define mysqld_group   mysql
%define mysqldatadir   /opt/freeware/lib/mysql


# ----------------------------------------------------------------------------
# Feature set (storage engines, options).  Default to community (everything)
# ----------------------------------------------------------------------------
%define feature_set community

# ----------------------------------------------------------------------------
# Server comment strings
# ----------------------------------------------------------------------------
%define compilation_comment_debug       MySQL Community Server - Debug (GPL)
%define compilation_comment_release     MySQL Community Server (GPL)


##############################################################################
# Main spec file section
##############################################################################

Name:           MySQL
Summary:        MySQL: a very fast and reliable SQL database server
Group:          Applications/Databases
Version:        5.5.10
Release:        %{release}
License:        Copyright (c) 2000, 2011, %{mysql_vendor}.  All rights reserved.  Use is subject to license terms.  Under %{license_type} license as shown in the Description field.
Source:         http://www.mysql.com/Downloads/MySQL-5.5/%{src_dir}.tar.gz
URL:            http://www.mysql.com/
Patch0:		%{src_dir}-bzero.patch
Prefix: 	%{_prefix}/mysql
BuildRoot: 	/var/tmp/%{name}-%{version}-root
Packager:       MySQL Build Team <build@mysql.com>
Vendor:         %{mysql_vendor}
Provides:       msqlormysql MySQL-server mysql
BuildRequires:  ncurses-devel perl readline-devel zlib-devel

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

# From the manual
%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from %{mysql_vendor} if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

##############################################################################
# Sub package definition
##############################################################################

%package -n MySQL-server
Summary:        MySQL: a very fast and reliable SQL database server
Group:          Applications/Databases
Requires:       coreutils grep 
Provides:       msqlormysql mysql-server mysql MySQL MySQL-server
Obsoletes:      MySQL mysql mysql-server MySQL-server MySQL-server-community

%description -n MySQL-server
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

The MySQL software has Dual Licensing, which means you can use the MySQL
software free of charge under the GNU General Public License
(http://www.gnu.org/licenses/). You can also purchase commercial MySQL
licenses from %{mysql_vendor} if you do not wish to be bound by the terms of
the GPL. See the chapter "Licensing and Support" in the manual for
further info.

The MySQL web site (http://www.mysql.com/) provides the latest news and 
information about the MySQL software.  Also please see the documentation
and the manual for more information.

This package includes the MySQL server binary as well as related utilities
to run and administer a MySQL server.

If you want to access and work with the database, you have to install
package "MySQL-client" as well!

# ----------------------------------------------------------------------------
%package -n MySQL-client
Summary:        MySQL - Client
Group:          Applications/Databases
Obsoletes:      mysql-client MySQL-client MySQL-client-community
Provides:       mysql-client MySQL-client

%description -n MySQL-client
This package contains the standard MySQL clients and administration tools.

For a description of MySQL see the base MySQL RPM or http://www.mysql.com/

# ----------------------------------------------------------------------------
%package -n MySQL-test
Requires:       MySQL-client perl
Summary:        MySQL - Test suite
Group:          Applications/Databases
Provides:       mysql-test
Obsoletes:      mysql-bench mysql-test MySQL-test-community
AutoReqProv:    no

%description -n MySQL-test
This package contains the MySQL regression test suite.

For a description of MySQL see the base MySQL RPM or http://www.mysql.com/

# ----------------------------------------------------------------------------
%package -n MySQL-devel
Summary:        MySQL - Development header files and libraries
Group:          Applications/Databases
Provides:       mysql-devel
Obsoletes:      mysql-devel MySQL-devel-community

%description -n MySQL-devel
This package contains the development header files and libraries necessary
to develop MySQL client applications.

For a description of MySQL see the base MySQL RPM or http://www.mysql.com/

# ----------------------------------------------------------------------------
%package -n MySQL-shared
Summary:        MySQL - Shared libraries
Group:          Applications/Databases
Provides:       mysql-shared
Obsoletes:      MySQL-shared-community

%description -n MySQL-shared
This package contains the shared libraries (*.so*) which certain languages
and applications need to dynamically load and use MySQL.

# ----------------------------------------------------------------------------
%package -n MySQL-embedded
Summary:        MySQL - embedded library
Group:          Applications/Databases
Requires:       MySQL-devel
Obsoletes:      mysql-embedded MySQL-embedded-community

%description -n MySQL-embedded
This package contains the MySQL server as an embedded library.

The embedded MySQL server library makes it possible to run a full-featured
MySQL server inside the client application. The main benefits are increased
speed and more simple management for embedded applications.

The API is identical for the embedded MySQL version and the
client/server version.

For a description of MySQL see the base MySQL RPM or http://www.mysql.com/

##############################################################################
%prep
%setup -T -a 0 -c -n %{src_dir}
%patch0 -p1 -b .bzero

##############################################################################
%build

# Be strict about variables, bail at earliest opportunity, etc.
set -eu

# Optional package files
touch optional-files-devel

#
# Set environment in order of preference, MYSQL_BUILD_* first, then variable
# name, finally a default.  RPM_OPT_FLAGS is assumed to be a part of the
# default RPM build environment.
#
# We set CXX=gcc by default to support so-called 'generic' binaries, where we
# do not have a dependancy on libgcc/libstdc++.  This only works while we do
# not require C++ features such as exceptions, and may need to be removed at
# a later date.
#

# This is a hack, $RPM_OPT_FLAGS on ia64 hosts contains flags which break
# the compile in cmd-line-utils/readline - needs investigation, but for now
# we simply unset it and use those specified directly in cmake.
%if "%{_arch}" == "ia64"
RPM_OPT_FLAGS=
%endif

export PATH=${MYSQL_BUILD_PATH:-$PATH}
CC='/usr/vacpp/bin/xlc_r'
CXX='/usr/vacpp/bin/xlC_r'
export CFLAGS="-O3 "
export CXXFLAGS="-O3 "
LDFLAGS="-L/opt/freeware/lib "
export LDFLAGS=${MYSQL_BUILD_LDFLAGS:-${LDFLAGS:-}}
export CMAKE=${MYSQL_BUILD_CMAKE:-${CMAKE:-cmake}}
export MAKE_JFLAG=${MYSQL_BUILD_MAKE_JFLAG:-}

# Build debug mysqld and libmysqld.a
[ -d debug ] || mkdir debug
(
  cd debug
  # Attempt to remove any optimisation flags from the debug build
  CFLAGS=`echo " ${CFLAGS} " | \
            sed -e 's/ -O[0-9]* / /' \
                -e 's/ -unroll2 / /' \
                -e 's/ -ip / /' \
                -e 's/^ //' \
                -e 's/ $//'`
  CXXFLAGS=`echo " ${CXXFLAGS} " | \
              sed -e 's/ -O[0-9]* / /' \
                  -e 's/ -unroll2 / /' \
                  -e 's/ -ip / /' \
                  -e 's/^ //' \
                  -e 's/ $//'`
  # XXX: MYSQL_UNIX_ADDR should be in cmake/* but mysql_version is included before
  # XXX: install_layout so we can't just set it based on INSTALL_LAYOUT=RPM


  ${CMAKE} ../%{src_dir}  \
	   -DBUILD_CONFIG=mysql_release \
           -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	   -DCMAKE_VERBOSE_MAKEFILE=1 \
	   -DCMAKE_INCLUDE_PATH=%{_prefix}/include/mysql \
	   -DCMAKE_LIBRARY_PATH=%{_libdir}/mysql \
	   -DCMAKE_PROGRAM_PATH=%{_bindir}/mysql \
	   -DINSTALL_LAYOUT=RPM \
           -DINSTALL_INFODIR=info/mysql \
           -DINSTALL_LIBDIR=lib/mysql \
           -DINSTALL_INCLUDEDIR=include/mysql \
           -DINSTALL_SHAREDIR=share/mysql \
           -DINSTALL_SUPPORTFILESDIR=share/mysql \
           -DINSTALL_PLUGINDIR=lib/mysql/plugin/debug \
           -DINSTALL_MANDIR=man/mysql \
           -DINSTALL_BINDIR=bin/mysql \
           -DINSTALL_SBINDIR=sbin/mysql \
           -DINSTALL_SCRIPTDIR=bin/mysql \
           -DINSTALL_MYSQLTESTDIR=share/mysql-test \
           -DINSTALL_MYSQLSHAREDIR=share/mysql \
	   -DWITH_PIC=1 \
	   -DWITH_SSL=yes \
	   -DWITH_READLINE=1 \
	   -DWITH_ZLIB=1 \
           -DCMAKE_BUILD_TYPE=Debug \
           -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
           -DFEATURE_SET="%{feature_set}" \
           -DCOMPILATION_COMMENT="%{compilation_comment_debug}" \
	   -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
	   -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
	   -DWITH_FEDERATED_STORAGE_ENGINE=1 \
	   -DWITHOUT_PERFSCHEMA_STORAGE_ENGINE=1

  echo BEGIN_DEBUG_CONFIG ; egrep '^#define' include/config.h ; echo END_DEBUG_CONFIG
  make ${MAKE_JFLAG} VERBOSE=1
)

# Build full release
[ -d release ] || mkdir release
(
  cd release
  # XXX: MYSQL_UNIX_ADDR should be in cmake/* but mysql_version is included before
  # XXX: install_layout so we can't just set it based on INSTALL_LAYOUT=RPM


  ${CMAKE} ../%{src_dir} \
	   -DBUILD_CONFIG=mysql_release \
           -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	   -DCMAKE_VERBOSE_MAKEFILE=1 \
	   -DCMAKE_INCLUDE_PATH=%{_prefix}/include/mysql \
	   -DCMAKE_LIBRARY_PATH=%{_libdir}/mysql \
	   -DCMAKE_PROGRAM_PATH=%{_bindir}/mysql \
	   -DINSTALL_LAYOUT=RPM \
           -DINSTALL_INFODIR=info/mysql \
           -DINSTALL_LIBDIR=lib/mysql \
           -DINSTALL_INCLUDEDIR=include/mysql \
           -DINSTALL_SHAREDIR=share/mysql \
           -DINSTALL_SUPPORTFILESDIR=share/mysql \
           -DINSTALL_PLUGINDIR=lib/mysql/plugin \
           -DINSTALL_MANDIR=man/mysql \
           -DINSTALL_BINDIR=bin/mysql \
           -DINSTALL_SBINDIR=sbin/mysql \
           -DINSTALL_SCRIPTDIR=bin/mysql \
           -DINSTALL_MYSQLTESTDIR=share/mysql-test \
           -DINSTALL_MYSQLSHAREDIR=share/mysql \
	   -DWITH_PIC=1 \
	   -DWITH_SSL=yes \
	   -DWITH_READLINE=1 \
	   -DWITH_ZLIB=1 \
           -DCMAKE_BUILD_TYPE=RelWithDebInfo \
           -DMYSQL_UNIX_ADDR="/var/lib/mysql/mysql.sock" \
           -DFEATURE_SET="%{feature_set}" \
           -DCOMPILATION_COMMENT="%{compilation_comment_release}" \
	   -DWITH_ARCHIVE_STORAGE_ENGINE=1 \
	   -DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
	   -DWITH_FEDERATED_STORAGE_ENGINE=1 \
	   -DWITHOUT_PERFSCHEMA_STORAGE_ENGINE=1

  echo BEGIN_NORMAL_CONFIG ; egrep '^#define' include/config.h ; echo END_NORMAL_CONFIG
  make ${MAKE_JFLAG} VERBOSE=1
)

# Use the build root for temporary storage of the shared libraries.
RBR=$RPM_BUILD_ROOT

# Clean up the BuildRoot first
[ "$RBR" != "/" ] && [ -d "$RBR" ] && rm -rf "$RBR";

# For gcc builds, include libgcc.a in the devel subpackage (BUG 4921).  This
# needs to be during build phase as $CC is not set during install.
if "$CC" -v 2>&1 | grep '^gcc.version' >/dev/null 2>&1
then
  libgcc=`$CC $CFLAGS --print-libgcc-file`
  if [ -f "$libgcc" ]
  then
    mkdir -p $RBR%{_libdir}/mysql
    install -m 644 $libgcc $RBR%{_libdir}/mysql/libmygcc.a
    echo "%{_libdir}/mysql/libmygcc.a" >>optional-files-devel
  fi
fi

##############################################################################
%install
set -eu

RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/%{src_dir}

# Ensure that needed directories exists
install -d $RBR%{_sysconfdir}/mysql/logrotate.d
install -d $RBR%{_sysconfdir}/mysql/init.d
install -d $RBR%{mysqldatadir}
install -d $RBR%{_datadir}/mysql-test
install -d $RBR%{_includedir}/mysql
install -d $RBR%{_libdir}/mysql/plugin/debug
install -d $RBR%{_libdir}/mysql
install -d $RBR%{_mandir}/mysql
install -d $RBR%{_bindir}/mysql
install -d $RBR%{_sbindir}/mysql

# Install some debug binaries
(
install -m 755  $MBD/debug/plugin/audit_null/adt_null.so $RBR%{_libdir}/mysql/plugin/debug/adt_null.so
install -m 755  $MBD/debug/plugin/daemon_example/libdaemon_example.so $RBR%{_libdir}/mysql/plugin/debug/libdaemon_example.so
install -m 755  $MBD/debug/plugin/fulltext/mypluglib.so $RBR%{_libdir}/mysql/plugin/debug/mypluglib.so
install -m 755  $MBD/debug/plugin/semisync/semisync_master.so $RBR%{_libdir}/mysql/plugin/debug/semisync_master.so
install -m 755  $MBD/debug/plugin/semisync/semisync_slave.so $RBR%{_libdir}/mysql/plugin/debug/semisync_slave.so
## install -m 755  $MBD/debug/plugin/semisync/semisync_slave.so $RBR%{_libdir}/mysql/plugin/debug/semisync_slave.so
install -m 755  $MBD/debug/plugin/auth/auth.so $RBR%{_libdir}/mysql/plugin/debug/auth.so
install -m 755  $MBD/debug/plugin/auth/auth_test_plugin.so $RBR%{_libdir}/mysql/plugin/debug/auth_test_plugin.so
install -m 755  $MBD/debug/plugin/auth/qa_auth_client.so $RBR%{_libdir}/mysql/plugin/debug/qa_auth_client.so
install -m 755  $MBD/debug/plugin/auth/qa_auth_server.so $RBR%{_libdir}/mysql/plugin/debug/qa_auth_server.so
install -m 755  $MBD/debug/plugin/auth/qa_auth_interface.so $RBR%{_libdir}/mysql/plugin/debug/qa_auth_interface.so
install -m 755  $MBD/debug/sql/mysqld $RBR%{_sbindir}/mysql/mysqld-debug
install -m 755  $MBD/debug/libmysqld/libmysqld.a $RBR%{_libdir}/mysql/libmysqld-debug.a
)

# Install all release binaries
(
  cd $MBD/release
  make DESTDIR=$RBR install
)

# Install logrotate and autostart
install -m 644 $MBD/release/support-files/mysql-log-rotate $RBR%{_sysconfdir}/mysql/logrotate.d/mysql
install -m 755 $MBD/release/support-files/mysql.server $RBR%{_sysconfdir}/mysql/init.d/mysql


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib sbin
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

#Strip the binaries
/usr/bin/strip $RPM_BUILD_ROOT%{_prefix}/bin/* || :

# Touch the place where the my.cnf config file might be located
# Just to make sure it's in the file list and marked as a config file
touch $RBR%{_sysconfdir}/mysql/my.cnf

# Remove man pages we explicitly do not want to package, avoids 'unpackaged
# files' warning.
rm -f $RBR%{_mandir}/mysql/man1/make_win_bin_dist.1*

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre -n MySQL-server
# This is the code running at the beginning of a RPM upgrade action,
# before replacing the old files with the new ones.

# ATTENTION: Parts of this are duplicated in the "triggerpostun" !

# There are users who deviate from the default file system layout.
# Check local settings to support them.
if [ -x %{_bindir}/mysql/my_print_defaults ]
then
  mysql_datadir=`%{_bindir}/mysql/my_print_defaults server mysqld | grep '^--datadir=' | sed -n 's/--datadir=//p'`
  PID_FILE_PATT=`%{_bindir}/mysql/my_print_defaults server mysqld | grep '^--pid-file=' | sed -n 's/--pid-file=//p'`
fi
if [ -z "$mysql_datadir" ]
then
  mysql_datadir=%{mysqldatadir}
fi
if [ -z "$PID_FILE_PATT" ]
then
  PID_FILE_PATT="$mysql_datadir/*.pid"
fi

# Check if we can safely upgrade.  An upgrade is only safe if it's from one
# of our RPMs in the same version family.

installed=`rpm -q --whatprovides mysql-server 2> /dev/null`
if [ $? -eq 0 -a -n "$installed" ]; then
  vendor=`rpm -q --queryformat='%{VENDOR}' "$installed" 2>&1`
  version=`rpm -q --queryformat='%{VERSION}' "$installed" 2>&1`
  myoldvendor='%{mysql_old_vendor}'
  myvendor_2='%{mysql_vendor_2}'
  myvendor='%{mysql_vendor}'
  myversion='%{mysql_version}'

  old_family=`echo $version \
    | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`
  new_family=`echo $myversion \
    | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`

  [ -z "$vendor" ] && vendor='<unknown>'
  [ -z "$old_family" ] && old_family="<unrecognized version $version>"
  [ -z "$new_family" ] && new_family="<bad package specification: version $myversion>"

  error_text=
  if [ "$vendor" != "$myoldvendor" \
    -a "$vendor" != "$myvendor_2" \
    -a "$vendor" != "$myvendor" ]; then
    error_text="$error_text
The current MySQL server package is provided by a different
vendor ($vendor) than $myoldvendor, $myvendor_2, or $myvendor.
Some files may be installed to different locations, including log
files and the service startup script in %{_sysconfdir}/mysql/init.d/.
"
  fi

  if [ "$old_family" != "$new_family" ]; then
    error_text="$error_text
Upgrading directly from MySQL $old_family to MySQL $new_family may not
be safe in all cases.  A manual dump and restore using mysqldump is
recommended.  It is important to review the MySQL manual's Upgrading
section for version-specific incompatibilities.
"
  fi

  if [ -n "$error_text" ]; then
    cat <<HERE >&2

******************************************************************
A MySQL server package ($installed) is installed.
$error_text
A manual upgrade is required.

- Ensure that you have a complete, working backup of your data and my.cnf
  files
- Shut down the MySQL server cleanly
- Remove the existing MySQL packages.  Usually this command will
  list the packages you should remove:
  rpm -qa | grep -i '^mysql-'

  You may choose to use 'rpm --nodeps -ev <package-name>' to remove
  the package which contains the mysqlclient shared library.  The
  library will be reinstalled by the MySQL-shared-compat package.
- Install the new MySQL packages supplied by $myvendor
- Ensure that the MySQL server is started
- Run the 'mysql_upgrade' program

This is a brief description of the upgrade process.  Important details
can be found in the MySQL manual, in the Upgrading section.
******************************************************************
HERE
    exit 1
  fi
fi

# We assume that if there is exactly one ".pid" file,
# it contains the valid PID of a running MySQL server.
NR_PID_FILES_tmp=`ls $PID_FILE_PATT 2>/dev/null | wc -l`
NR_PID_FILES=`echo ${NR_PID_FILES_tmp} | sed -e "s/^[	 ]*//"`
case $NR_PID_FILES in
	0 ) SERVER_TO_START=''  ;;  # No "*.pid" file == no running server
	1 ) SERVER_TO_START='true' ;;
	* ) SERVER_TO_START=''      # Situation not clear
	    SEVERAL_PID_FILES=true ;;
esac
# That logic may be debated: We might check whether it is non-empty,
# contains exactly one number (possibly a PID), and whether "ps" finds it.
# OTOH, if there is no such process, it means a crash without a cleanup -
# is that a reason not to start a new server after upgrade?

STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER

if [ -f "$STATUS_FILE" ]; then
	echo "Some previous upgrade was not finished:"
	ls -ld $STATUS_FILE
	echo "Please check its status, then do"
	echo "    rm $STATUS_FILE"
	echo "before repeating the MySQL upgrade."
	exit 1
elif [ -n "$SEVERAL_PID_FILES" ] ; then
	echo "You have more than one PID file:"
	ls -ld $PID_FILE_PATT
	echo "Please check which one (if any) corresponds to a running server"
	echo "and delete all others before repeating the MySQL upgrade."
	exit 1
fi

NEW_VERSION=%{mysql_version}-%{release}

# The "pre" section code is also run on a first installation,
# when there  is no data directory yet. Protect against error messages.
if [ -d "$mysql_datadir" ] ; then
	echo "MySQL RPM upgrade to version $NEW_VERSION"  > $STATUS_FILE
	echo "'pre' step running at `date`"          >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "ERR file(s):"                          >> $STATUS_FILE
[ -f $mysql_datadir/*.err ] && 	ls -ltr $mysql_datadir/*.err  2>/dev/null >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "Latest 'Version' line in latest file:" >> $STATUS_FILE
	grep '^Version' `ls -tr $mysql_datadir/*.err | tail -1` | \
		tail -1                              >> $STATUS_FILE
	echo                                         >> $STATUS_FILE

	if [ -n "$SERVER_TO_START" ] ; then
		# There is only one PID file, race possibility ignored
		echo "PID file:"                           >> $STATUS_FILE
		ls -l   $PID_FILE_PATT                     >> $STATUS_FILE
		cat     $PID_FILE_PATT                     >> $STATUS_FILE
		echo                                       >> $STATUS_FILE
		echo "Server process:"                     >> $STATUS_FILE
		ps -fp `cat $PID_FILE_PATT`                >> $STATUS_FILE
		echo                                       >> $STATUS_FILE
		echo "SERVER_TO_START=$SERVER_TO_START"    >> $STATUS_FILE
	else
		# Take a note we checked it ...
		echo "PID file:"                           >> $STATUS_FILE
		ls -l   $PID_FILE_PATT                     >> $STATUS_FILE 2>&1
	fi
fi

# Shut down a previously installed server first
# Note we *could* make that depend on $SERVER_TO_START, but we rather don't,
# so a "stop" is attempted even if there is no PID file.
# (Maybe the "stop" doesn't work then, but we might fix that in itself.)
if [ -x %{_sysconfdir}/mysql/init.d/mysql ] ; then
        %{_sysconfdir}/mysql/init.d/mysql stop > /dev/null 2>&1
        echo "Giving mysqld 5 seconds to exit nicely"
        sleep 5
fi




%post -n MySQL-server
# This is the code running at the end of a RPM install or upgrade action,
# after the (new) files have been written.

# ATTENTION: Parts of this are duplicated in the "triggerpostun" !

# There are users who deviate from the default file system layout.
# Check local settings to support them.
if [ -x %{_bindir}/mysql/my_print_defaults ]
then
  mysql_datadir=`%{_bindir}/mysql/my_print_defaults server mysqld | grep '^--datadir=' | sed -n 's/--datadir=//p'`
fi
if [ -z "$mysql_datadir" ]
then
  mysql_datadir=%{mysqldatadir}
fi

NEW_VERSION=%{mysql_version}-%{release}
STATUS_FILE=$mysql_datadir/RPM_UPGRADE_MARKER

# ----------------------------------------------------------------------
# Create data directory if needed, check whether upgrade or install
# ----------------------------------------------------------------------
if [ ! -d "$mysql_datadir" ] ; then mkdir -m 755 $mysql_datadir; fi
if [ -f "$STATUS_FILE" ] ; then
	SERVER_TO_START=`grep '^SERVER_TO_START=' $STATUS_FILE | cut -c17-`
else
	SERVER_TO_START=''
fi
# echo "Analyzed: SERVER_TO_START=$SERVER_TO_START"
if [ ! -d "$mysql_datadir/mysql" ] ; then
	mkdir $mysql_datadir/mysql;
	echo "MySQL RPM installation of version $NEW_VERSION" >> $STATUS_FILE
else
	# If the directory exists, we may assume it is an upgrade.
	echo "MySQL RPM upgrade to version $NEW_VERSION" >> $STATUS_FILE
fi
if [ ! -d "$mysql_datadir/test" ] ; then mkdir $mysql_datadir/test; fi

## # ----------------------------------------------------------------------
## # Make MySQL start/shutdown automatically when the machine does it.
## # ----------------------------------------------------------------------
## # NOTE: This still needs to be debated. Should we check whether these links
## # for the other run levels exist(ed) before the upgrade?
## # use chkconfig on Enterprise Linux and newer SuSE releases
## if [ -x /sbin/chkconfig ] ; then
##         /sbin/chkconfig --add mysql
## # use insserv for older SuSE Linux versions
## elif [ -x /sbin/insserv ] ; then
##         /sbin/insserv %{_sysconfdir}/mysql/init.d/mysql
## fi

# ----------------------------------------------------------------------
# Create a MySQL user and group. Do not report any problems if it already
# exists.
# ----------------------------------------------------------------------
mkgroup %{mysqld_group} 2> /dev/null || true
useradd -d $mysql_datadir -s /usr/bin/bash -c "MySQL server" \
  -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
# The user may already exist, make sure it has the proper group nevertheless
# (BUG#12823)
chgroup users=%{mysqld_user} %{mysqld_group} 2> /dev/null || true

# ----------------------------------------------------------------------
# Change permissions so that the user that will run the MySQL daemon
# owns all database files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Initiate databases if needed
# ----------------------------------------------------------------------
%{_bindir}/mysql/mysql_install_db --rpm --user=%{mysqld_user}

# ----------------------------------------------------------------------
# Upgrade databases if needed would go here - but it cannot be automated yet
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Change permissions again to fix any new files.
# ----------------------------------------------------------------------
chown -R %{mysqld_user}:%{mysqld_group} $mysql_datadir

# ----------------------------------------------------------------------
# Fix permissions for the permission database so that only the user
# can read them.
# ----------------------------------------------------------------------
chmod -R og-rw $mysql_datadir/mysql

# Was the server running before the upgrade? If so, restart the new one.
if [ "$SERVER_TO_START" = "true" ] ; then
	# Restart in the same way that mysqld will be started normally.
	if [ -x %{_sysconfdir}/mysql/init.d/mysql ] ; then
		%{_sysconfdir}/mysql/init.d/mysql start
		echo "Giving mysqld 5 seconds to start"
		sleep 5
	fi
fi

# Collect an upgrade history ...
echo "Upgrade/install finished at `date`"        >> $STATUS_FILE
echo                                             >> $STATUS_FILE
echo "====="                                     >> $STATUS_FILE
STATUS_HISTORY=$mysql_datadir/RPM_UPGRADE_HISTORY
cat $STATUS_FILE >> $STATUS_HISTORY
mv -f  $STATUS_FILE ${STATUS_FILE}-LAST  # for "triggerpostun"


echo "Thank you for installing the MySQL Community Server! For Production
systems, we recommend MySQL Enterprise, which contains enterprise-ready
software, intelligent advisory services, and full production support with
scheduled service packs and more.  Visit www.mysql.com/enterprise for more
information."



%preun -n MySQL-server

# Which '$1' does this refer to?  Fedora docs have info:
# " ... a count of the number of versions of the package that are installed.
#   Action                           Count
#   Install the first time           1
#   Upgrade                          2 or higher (depending on the number of versions installed)
#   Remove last version of package   0 "
#
#  http://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch09s04s05.html
 
if [ $1 = 0 ] ; then
        # Stop MySQL before uninstalling it
        if [ -x %{_sysconfdir}/mysql/init.d/mysql ] ; then
                %{_sysconfdir}/mysql/init.d/mysql stop > /dev/null
        fi
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] \
  && rm -rf $RPM_BUILD_ROOT;

##############################################################################
#  Files section
##############################################################################

%files -n MySQL-server
%defattr(-,root,system,0755)

%doc %{src_dir}/Docs/ChangeLog
%doc release/support-files/my-*.cnf

%doc %attr(644, root, system) %{_infodir}/mysql/mysql.info*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/innochecksum.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/my_print_defaults.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/myisam_ftdump.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/myisamchk.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/myisamlog.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/myisampack.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_convert_table_format.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_fix_extensions.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man8/mysqld.8*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqld_multi.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqld_safe.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqldumpslow.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlman.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql.server.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqltest.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_tzinfo_to_sql.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_zap.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlbug.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/perror.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/replace.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/resolve_stack_dump.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/resolveip.1*

%ghost %config(noreplace,missingok) %{_sysconfdir}/mysql/my.cnf

%attr(755, root, system) %{_bindir}/mysql/innochecksum
%attr(755, root, system) %{_bindir}/mysql/my_print_defaults
%attr(755, root, system) %{_bindir}/mysql/myisam_ftdump
%attr(755, root, system) %{_bindir}/mysql/myisamchk
%attr(755, root, system) %{_bindir}/mysql/myisamlog
%attr(755, root, system) %{_bindir}/mysql/myisampack
%attr(755, root, system) %{_bindir}/mysql/mysql_convert_table_format
%attr(755, root, system) %{_bindir}/mysql/mysql_fix_extensions
%attr(755, root, system) %{_bindir}/mysql/mysql_install_db
%attr(755, root, system) %{_bindir}/mysql/mysql_secure_installation
%attr(755, root, system) %{_bindir}/mysql/mysql_setpermission
%attr(755, root, system) %{_bindir}/mysql/mysql_tzinfo_to_sql
%attr(755, root, system) %{_bindir}/mysql/mysql_upgrade
%attr(755, root, system) %{_bindir}/mysql/mysql_zap
%attr(755, root, system) %{_bindir}/mysql/mysqlbug
%attr(755, root, system) %{_bindir}/mysql/mysqld_multi
%attr(755, root, system) %{_bindir}/mysql/mysqld_safe
%attr(755, root, system) %{_bindir}/mysql/mysqldumpslow
%attr(755, root, system) %{_bindir}/mysql/mysqlhotcopy
%attr(755, root, system) %{_bindir}/mysql/mysqltest
%attr(755, root, system) %{_bindir}/mysql/perror
%attr(755, root, system) %{_bindir}/mysql/replace
%attr(755, root, system) %{_bindir}/mysql/resolve_stack_dump
%attr(755, root, system) %{_bindir}/mysql/resolveip

%attr(755, root, system) %{_sbindir}/mysql/mysqld
%attr(755, root, system) %{_sbindir}/mysql/mysqld-debug
%attr(755, root, system) %{_libdir}/mysql/plugin/adt_null.so
%attr(755, root, system) %{_libdir}/mysql/plugin/libdaemon_example.so
%attr(755, root, system) %{_libdir}/mysql/plugin/mypluglib.so
%attr(755, root, system) %{_libdir}/mysql/plugin/semisync_master.so
%attr(755, root, system) %{_libdir}/mysql/plugin/semisync_slave.so
%attr(755, root, system) %{_libdir}/mysql/plugin/auth.so
%attr(755, root, system) %{_libdir}/mysql/plugin/auth_test_plugin.so
%attr(755, root, system) %{_libdir}/mysql/plugin/qa_auth_client.so
%attr(755, root, system) %{_libdir}/mysql/plugin/qa_auth_interface.so
%attr(755, root, system) %{_libdir}/mysql/plugin/qa_auth_server.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/adt_null.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/libdaemon_example.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/mypluglib.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/semisync_master.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/semisync_slave.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/auth.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/auth_test_plugin.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/qa_auth_client.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/qa_auth_interface.so
%attr(755, root, system) %{_libdir}/mysql/plugin/debug/qa_auth_server.so

%attr(644, root, system) %config(noreplace,missingok) %{_sysconfdir}/mysql/logrotate.d/mysql
%attr(755, root, system) %{_sysconfdir}/mysql/init.d/mysql

%attr(755, root, system) %{_datadir}/mysql
/usr/bin/*
/usr/sbin/*
/usr/lib/*

# ----------------------------------------------------------------------------
%files -n MySQL-client

%defattr(-, root, system, 0755)
%attr(755, root, system) %{_bindir}/mysql/msql2mysql
%attr(755, root, system) %{_bindir}/mysql/mysql
%attr(755, root, system) %{_bindir}/mysql/mysql_find_rows
%attr(755, root, system) %{_bindir}/mysql/mysql_waitpid
%attr(755, root, system) %{_bindir}/mysql/mysqlaccess
# XXX: This should be moved to %{_sysconfdir}/mysql
%attr(644, root, system) %{_bindir}/mysql/mysqlaccess.conf
%attr(755, root, system) %{_bindir}/mysql/mysqladmin
%attr(755, root, system) %{_bindir}/mysql/mysqlbinlog
%attr(755, root, system) %{_bindir}/mysql/mysqlcheck
%attr(755, root, system) %{_bindir}/mysql/mysqldump
%attr(755, root, system) %{_bindir}/mysql/mysqlimport
%attr(755, root, system) %{_bindir}/mysql/mysqlshow
%attr(755, root, system) %{_bindir}/mysql/mysqlslap

%doc %attr(644, root, man) %{_mandir}/mysql/man1/msql2mysql.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_find_rows.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_waitpid.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqladmin.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqldump.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlimport.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlshow.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlslap.1*
/usr/bin/*

# ----------------------------------------------------------------------------
%files -n MySQL-devel -f optional-files-devel
%defattr(-, root, system, 0755)
%doc %attr(644, root, man) %{_mandir}/mysql/man1/comp_err.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_config.1*
%attr(755, root, system) %{_bindir}/mysql/mysql_config
%dir %attr(755, root, system) %{_includedir}/mysql
%dir %attr(755, root, system) %{_libdir}/mysql
%{_includedir}/mysql/*
%{_datadir}/mysql/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.a
%{_libdir}/mysql/libmysqlclient_r.a
%{_libdir}/mysql/libmysqlservices.a
/usr/lib/*


# ----------------------------------------------------------------------------
%files -n MySQL-shared
%defattr(-, root, system, 0755)
# Shared libraries (omit for architectures that don't support them)
%{_libdir}/mysql/libmysql*.so*
/usr/lib/*


# ----------------------------------------------------------------------------
%files -n MySQL-test
%defattr(-, root, system, 0755)
%attr(-, root, system) %{_datadir}/mysql-test
%attr(755, root, system) %{_bindir}/mysql/mysql_client_test
%attr(755, root, system) %{_bindir}/mysql/mysqltest_embedded
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql-test-run.pl.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqltest_embedded.1*
/usr/bin/*

# ----------------------------------------------------------------------------
%files -n MySQL-embedded
%defattr(-, root, system, 0755)
%attr(644, root, system) %{_libdir}/mysql/libmysqld.a
%attr(644, root, system) %{_libdir}/mysql/libmysqld-debug.a
/usr/lib/*

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog
* Tue Apr 19 2011 Gerard Visiedo <gerar.visiedo@bull.net> 5.5.10
- Initial port for AIX 5.5.10

