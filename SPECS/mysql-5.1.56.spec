# Copyright (c) 2000, 2011, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston
# MA  02110-1301  USA.

##############################################################################
# Some common macro definitions
##############################################################################

# NOTE: "vendor" is used in upgrade/downgrade check, so you can't
# change these, has to be exactly as is.
%define mysql_old_vendor	MySQL AB
%define mysql_vendor_2		Sun Microsystems, Inc.
%define mysql_vendor		Oracle and/or its affiliates

%define mysql_version 5.1.56

%define mysqld_user    mysql
%define mysqld_group   mysql
%define mysqldatadir   /var/lib/mysql
%define see_base For a description of MySQL see the base MySQL RPM or http://www.mysql.com

# ------------------------------------------------------------------------------
# We don't package all files installed into the build root by intention -
# See BUG#998 for details.
# ------------------------------------------------------------------------------
%define _unpackaged_files_terminate_build 0

# ------------------------------------------------------------------------------
# RPM build tools now automatically detects Perl module dependencies. This
# detection gives problems as it is broken in some versions, and it also
# give unwanted dependencies from mandatory scripts in our package.
# Might not be possible to disable in all RPM tool versions, but here we
# try. We keep the "AutoReqProv: no" for the "test" sub package, as disabling
# here might fail, and that package has the most problems.
# See http://fedoraproject.org/wiki/Packaging/Perl#Filtering_Requires:_and_Provides
#     http://www.wideopen.com/archives/rpm-list/2002-October/msg00343.html
# ------------------------------------------------------------------------------
%undefine __perl_provides
%undefine __perl_requires

##############################################################################
# Command line handling
##############################################################################

# ----------------------------------------------------------------------
# use "rpmbuild --with yassl" or "rpm --define '_with_yassl 1'" (for RPM 3.x)
# to build with yaSSL support (off by default)
# ----------------------------------------------------------------------
%{?_with_yassl:%define YASSL_BUILD 1}
%{!?_with_yassl:%define YASSL_BUILD 0}

# ----------------------------------------------------------------------
# use "rpmbuild --without bundled_zlib" or "rpm --define '_without_bundled_zlib 1'"
# (for RPM 3.x) to not build using the bundled zlib (on by default)
# ----------------------------------------------------------------------
%{!?_with_bundled_zlib: %{!?_without_bundled_zlib: %define WITH_BUNDLED_ZLIB 1}}
%{?_with_bundled_zlib:%define WITH_BUNDLED_ZLIB 1}
%{?_without_bundled_zlib:%define WITH_BUNDLED_ZLIB 0}

# ----------------------------------------------------------------------
# use "rpmbuild --without innodb_plugin" or "rpm --define '_without_innodb_plugin 1'"
# (for RPM 3.x) to not build the innodb plugin (on by default with innodb builds)
# ----------------------------------------------------------------------
%{!?_with_innodb_plugin: %{!?_without_innodb_plugin: %define WITH_INNODB_PLUGIN 1}}
%{?_with_innodb_plugin:%define WITH_INNODB_PLUGIN 1}
%{?_without_innodb_plugin:%define WITH_INNODB_PLUGIN 0}

# ----------------------------------------------------------------------
# use "rpmbuild --with cluster" or "rpm --define '_with_cluster 1'" (for RPM 3.x)
# to build with cluster support (off by default)
# ----------------------------------------------------------------------
%{?_with_cluster:%define CLUSTER_BUILD 1}
%{!?_with_cluster:%define CLUSTER_BUILD 0}

##############################################################################
# Product definitions - set for a "community" package
##############################################################################

%define server_suffix  -community
%define package_suffix -community
%define ndbug_comment "MySQL Community Server (GPL)"
%define debug_comment "MySQL Community Server - Debug (GPL)"
%define commercial 0
%define EMBEDDED_BUILD 0
%define PARTITION_BUILD 0

# Default for CLUSTER_BUILD is "0", but command line option may override it
%define COMMUNITY_BUILD 1
%define INNODB_BUILD 1

%define NORMAL_TEST_MODE test-bt
%define DEBUG_TEST_MODE test-bt-debug

%define release 1

%define mysql_license GPL
%define src_dir mysql-%{mysql_version}

##############################################################################
# Main spec file section
##############################################################################

Name:		MySQL
Summary:	MySQL: a very fast and reliable SQL database server
Group:		Applications/Databases
Version:	5.1.56
Release:	1
License:	Copyright 2000-2008 MySQL AB, 2011 %{mysql_vendor}  All rights reserved.  Use is subject to license terms.  Under %{mysql_license} license as shown in the Description field.
Source:		http://www.mysql.com/Downloads/MySQL-5.1/%{src_dir}.tar.gz
Patch0:		mysql-%{version}-bzero.patch
Patch1:		mysql-%{version}-info.patch
Patch2:		mysql-%{version}-abi_check.patch
URL:		http://www.mysql.com/
Packager:	%{mysql_vendor} Product Engineering Team <build@mysql.com>
Vendor:		%{mysql_vendor}
Provides:	msqlormysql MySQL-server mysql
BuildRequires: ncurses-devel
Obsoletes:	mysql

# Think about what you use here since the first step is to
# run a rm -rf
BuildRoot:    %{_tmppath}/%{name}-%{version}-root

# From the manual
%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

Copyright 2000-2008 MySQL AB, 2011 %{mysql_vendor}  All rights reserved.
Use is subject to license terms.

This software comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to modify and redistribute it under the GPL license.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

##############################################################################
# Sub package definition
##############################################################################

%package server
Summary:	MySQL: a very fast and reliable SQL database server
Group:		Applications/Databases
Requires:	%{name}-shared
Provides:	msqlormysql mysql-server mysql MySQL
Obsoletes:	MySQL mysql mysql-server

%description server
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
%{mysql_vendor}

Copyright 2000-2008 MySQL AB, 2011 %{mysql_vendor}  All rights reserved.
Use is subject to license terms.

This software comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to modify and redistribute it under the GPL license.

The MySQL web site (http://www.mysql.com/) provides the latest
news and information about the MySQL software. Also please see the
documentation and the manual for more information.

This package includes the MySQL server binary
%if %{INNODB_BUILD}
(configured including InnoDB)
%endif
as well as related utilities to run and administer a MySQL server.

If you want to access and work with the database, you have to install
package "MySQL-client" as well!

# ------------------------------------------------------------------------------

%package client
Summary: MySQL - Client
Group: Applications/Databases
Requires:	%{name}-shared
Obsoletes: mysql-client
Provides: mysql-client

%description client
This package contains the standard MySQL clients and administration tools.

%{see_base}

# ------------------------------------------------------------------------------

%if %{CLUSTER_BUILD}
%package ndb-storage
Summary:	MySQL - ndbcluster storage engine
Group:		Applications/Databases

%description ndb-storage
This package contains the ndbcluster storage engine.
It is necessary to have this package installed on all
computers that should store ndbcluster table data.

%{see_base}

# ------------------------------------------------------------------------------

%package ndb-management
Summary:	MySQL - ndbcluster storage engine management
Group:		Applications/Databases

%description ndb-management
This package contains ndbcluster storage engine management.
It is necessary to have this package installed on at least
one computer in the cluster.

%{see_base}

# ------------------------------------------------------------------------------

%package ndb-tools
Summary:	MySQL - ndbcluster storage engine basic tools
Group:		Applications/Databases

%description ndb-tools
This package contains ndbcluster storage engine basic tools.

%{see_base}

# ------------------------------------------------------------------------------

%package ndb-extra
Summary:	MySQL - ndbcluster storage engine extra tools
Group:		Applications/Databases

%description ndb-extra
This package contains some extra ndbcluster storage engine tools for the advanced user.
They should be used with caution.

%{see_base}
%endif

# ------------------------------------------------------------------------------

%package test
Requires: %{name}-client perl
Summary: MySQL - Test suite
Group: Applications/Databases
Provides: mysql-test
Obsoletes: mysql-bench mysql-test
AutoReqProv: no

%description test
This package contains the MySQL regression test suite.

%{see_base}

# ------------------------------------------------------------------------------

%package devel
Summary: MySQL - Development header files and libraries
Group: Applications/Databases
Provides: mysql-devel
Obsoletes: mysql-devel

%description devel
This package contains the development header files and libraries
necessary to develop MySQL client applications.

%{see_base}

# ------------------------------------------------------------------------------

%package shared
Summary: MySQL - Shared libraries
Group: Applications/Databases

%description shared
This package contains the shared libraries (*.so*) which certain
languages and applications need to dynamically load and use MySQL.

# ------------------------------------------------------------------------------

%if %{EMBEDDED_BUILD}

%package embedded
Requires: %{name}-devel
Summary: MySQL - embedded library
Group: Applications/Databases
Obsoletes: mysql-embedded

%description embedded
This package contains the MySQL server as an embedded library.

The embedded MySQL server library makes it possible to run a
full-featured MySQL server inside the client application.
The main benefits are increased speed and more simple management
for embedded applications.

The API is identical for the embedded MySQL version and the
client/server version.

%{see_base}

%endif

##############################################################################
#
##############################################################################

%prep
# We unpack the source two times, for 'debug' and 'release' build.
%setup -T -a 0 -c -n mysql-%{mysql_version}
mv mysql-%{mysql_version} mysql-debug-%{mysql_version}
%setup -D -T -a 0 -n mysql-%{mysql_version}
mv mysql-%{mysql_version} mysql-release-%{mysql_version}
%patch0 -p1 -b .bzero
%patch1 -p1 -b .info
%patch2 -p1 -b .abi_check

##############################################################################
# The actual build
##############################################################################

%build

#unset RM
RM="rm -f"

#Building with gcc
export CC='/usr/bin/gcc'
export CXX='/usr/bin/gcc'

BuildMySQL() {
# Let "MYSQL_BUILD_*FLAGS" take precedence.
# Fall back on RPM_OPT_FLAGS (part of RPM environment) if no flags are given.
# Evaluate current setting of $DEBUG
if [ $DEBUG -gt 0 ] ; then
	OPT_COMMENT='--with-comment="%{debug_comment}"'
	OPT_DEBUG='--with-debug'
	CFLAGS=`echo   " $CFLAGS "   | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
	CXXFLAGS=`echo " $CXXFLAGS " | \
	    sed -e 's/ -O[0-9]* / /' -e 's/ -unroll2 / /' -e 's/ -ip / /' \
	        -e 's/^ //' -e 's/ $//'`
else
	OPT_COMMENT='--with-comment="%{ndbug_comment}"'
	OPT_DEBUG=''
fi
# The --enable-assembler simply does nothing on systems that does not
# support assembler speedups.

	## CC='/usr/vacpp/bin/xlc_r' \
	## CXX='/usr/vacpp/bin/xlC_r' \
	CC='/usr/bin/gcc' \
	CXX='/usr/bin/gcc' \
	CFLAGS="$CFLAGS" \
	CXXFLAGS="$CXXFLAGS" \
        LDFLAGS="$LDFLAGS" \
	./configure \
		$* \
		--prefix=%{_prefix} \
		--exec-prefix=%{_exec_prefix}/mysql \
		--libexecdir=%{_sbindir}/mysql \
		--bindir=%{_bindir}/mysql \
		--libdir=%{_libdir}/mysql \
		--sysconfdir=%{_sysconfdir}/mysql \
		--datadir=%{_datadir}/mysql \
		--localstatedir=%{mysqldatadir} \
		--infodir=%{_prefix}/info/mysql \
		--includedir=%{_includedir}/mysql \
		--mandir=%{_mandir}/mysql \
		--enable-thread-safe-client \
		--with-extra-charsets=all \
		--with-ssl \
		--enable-mysql-maintainer-mode=no \
		"$OPT_COMMENT" \
		$OPT_DEBUG

 	make
}
# end of function definition "BuildMySQL"

# Use our own copy of glibc

OTHER_LIBC_DIR=/opt/freeware/mysql-glibc
USE_OTHER_LIBC_DIR=""
if test -d "$OTHER_LIBC_DIR"
then
  USE_OTHER_LIBC_DIR="--with-other-libc=$OTHER_LIBC_DIR"
fi

# Use the build root for temporary storage of the shared libraries.

RBR=$RPM_BUILD_ROOT

# Clean up the BuildRoot first
[ "$RBR" != "/" ] && [ -d $RBR ] && rm -rf $RBR;
mkdir -p $RBR%{_libdir}/mysql

#
# Use MYSQL_BUILD_PATH so that we can use a dedicated version of gcc
#
## PATH=${MYSQL_BUILD_PATH:-/bin:/usr/bin}
export PATH=$PATH:/opt/freeware/bin

# Build the Debug binary.

# Use gcc for C and C++ code (to avoid a dependency on libstdc++ and
# including exceptions into the code
if [ -z "$CXX" -a -z "$CC" ] ; then
	export CC="gcc" CXX="gcc"
fi


##############################################################################
#
#  Build the debug version
#
##############################################################################

(
# We are in a subshell, so we can modify variables just for one run.

# Add -g and --with-debug.
DEBUG=1
cd mysql-debug-%{mysql_version} &&
CFLAGS="-I/opt/freeware/include" \
CXXFLAGS="-I/opt/freeware/include" \
LDFLAGS="-L/opt/freeware/lib" \
BuildMySQL 
)

# We might want to save the config log file
if test -n "$MYSQL_DEBUGCONFLOG_DEST"
then
  cp -fp mysql-debug-%{mysql_version}/config.log "$MYSQL_DEBUGCONFLOG_DEST"
fi

## Mask (cd mysql-debug-%{mysql_version} ; make test-bt-debug)

##############################################################################
#
#  Build the release binary
#
##############################################################################

DEBUG=0
(cd mysql-release-%{mysql_version} &&
# flags for xlc CFLAGS=" -O3 -qstrict -qoptimize=3 -qmaxmem=8192 -I/opt/freeware/include -I/usr/include "
# flags for xlC CXXFLAGS="-O3 -qstrict -qoptimize=3 -qmaxmem=8192 -I/opt/freeware/include -I/usr/include  -I/opt/freeware/include "
CFLAGS=" -O3 -I/opt/freeware/include -I/usr/include " \
CXXFLAGS=" -O3 \
		-felide-constructors \
		-fno-exceptions \
		-fno-rtti \
		-I/opt/freeware/include -I/usr/include \
		-I/opt/freeware/include " \
LDFLAGS="-L/opt/freeware/lib " \
BuildMySQL 
)
# We might want to save the config log file
if test -n "$MYSQL_CONFLOG_DEST"
then
  cp -fp  mysql-release-%{mysql_version}/config.log "$MYSQL_CONFLOG_DEST"
fi

## Mask (cd mysql-release-%{mysql_version} ; make test-bt)

##############################################################################

# For gcc builds, include libgcc.a in the devel subpackage (BUG 4921)
# Some "icc" calls may have "gcc" in the argument string, so we should first
# check for "icc". (If we don't check, the "--print-libgcc-file" call will fail.)
if expr "$CC" : ".*icc.*" > /dev/null ;
then
    %define WITH_LIBGCC 0
    :
elif expr "$CC" : ".*gcc.*" > /dev/null ;
then
  libgcc=`$CC $CFLAGS --print-libgcc-file`
  if [ -f $libgcc ]
  then
    %define WITH_LIBGCC 1
    install -m 644 $libgcc $RBR%{_libdir}/mysql/libmygcc.a
  else
    %define WITH_LIBGCC 0
    :
  fi
else
    %define WITH_LIBGCC 0
    :
fi

##############################################################################

##############################################################################

%install

#unset RM
RM="rm -f"

RBR=$RPM_BUILD_ROOT
MBD=$RPM_BUILD_DIR/mysql-%{mysql_version}/mysql-release-%{mysql_version}

# Ensure that needed directories exists
install -d $RBR%{_sysconfdir}/mysql/logrotate.d
install -d $RBR%{_sysconfdir}/mysql/init.d
install -d $RBR%{mysqldatadir}
install -d $RBR%{_datadir}/mysql/mysql-test
install -d $RBR%{_includedir}/mysql
install -d $RBR%{_bindir}/mysql
install -d $RBR%{_libdir}/mysql
install -d $RBR%{_mandir}/mysql
install -d $RBR%{_sbindir}/mysql
install -d $RBR%{_prefix}/info/mysql


# Install all binaries
(cd $MBD && make install DESTDIR=$RBR testroot=%{_datadir}/mysql)
# Old packages put shared libs in %{_libdir}/mysql/ (not %{_libdir}/mysql), so do
# the same here.


# install "mysqld-debug"
$MBD/libtool --mode=execute install -m 755 \
                 $RPM_BUILD_DIR/mysql-%{mysql_version}/mysql-debug-%{mysql_version}/sql/mysqld \
                 $RBR%{_sbindir}/mysql/mysqld-debug

# install saved perror binary with NDB support (BUG#13740)
install -m 755 $MBD/extra/perror $RBR%{_bindir}/mysql/perror

# Install logrotate and autostart
install -m 644 $MBD/support-files/mysql-log-rotate $RBR%{_sysconfdir}/mysql/logrotate.d/mysql
install -m 755 $MBD/support-files/mysql.server $RBR%{_sysconfdir}/mysql/init.d/mysql

%if %{EMBEDDED_BUILD}
# Install embedded server library in the build root
install -m 644 $MBD/libmysqld/libmysqld.a $RBR%{_libdir}/mysql/
%endif

# in RPMs, it is unlikely that anybody should use "sql-bench"
rm -fr $RBR%{_datadir}/mysql/sql-bench

# Touch the place where the my.cnf config file and mysqlmanager.passwd
# (MySQL Instance Manager password file) might be located
# Just to make sure it's in the file list and marked as a config file
touch $RBR%{_sysconfdir}/mysql/my.cnf
touch $RBR%{_sysconfdir}/mysql/mysqlmanager.passwd

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

##############################################################################
#  Post processing actions, i.e. when installed
##############################################################################

%pre server
# This is the code running at the beginning of a RPM upgrade action,
# before replacing the old files with the new ones.

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

  old_family=`echo $version   | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`
  new_family=`echo $myversion | sed -n -e 's,^\([1-9][0-9]*\.[0-9][0-9]*\)\..*$,\1,p'`

  [ -z "$vendor" ] && vendor='<unknown>'
  [ -z "$old_family" ] && old_family="<unrecognized version $version>"
  [ -z "$new_family" ] && new_family="<bad package specification: version $myversion>"

  error_text=
  if [ "$vendor" != "$myoldvendor" -a "$vendor" != "$myvendor_2" -a "$vendor" != "$myvendor" ]; then
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
NR_PID_FILES=`echo ${NR_PID_FILES_tmp} |sed -e "s/Ã^[	 ]*//"`

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

if [ -f $STATUS_FILE ]; then
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
if [ -d $mysql_datadir ] ; then
	echo "MySQL RPM upgrade to version $NEW_VERSION"  > $STATUS_FILE
	echo "'pre' step running at `date`"          >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "ERR file(s):"                          >> $STATUS_FILE
	ls -ltr $mysql_datadir/*.err 2>/dev/null     >> $STATUS_FILE
	echo                                         >> $STATUS_FILE
	echo "Latest 'Version' line in latest file:" >> $STATUS_FILE
	grep '^Version' `ls -tr $mysql_datadir/*.err 2>/dev/null | tail -1` | \
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

%post server
# This is the code running at the end of a RPM install or upgrade action,
# after the (new) files have been written.

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
if [ ! -d $mysql_datadir ] ; then mkdir -m 755 $mysql_datadir; fi
if [ -f $STATUS_FILE ] ; then
	SERVER_TO_START=`grep '^SERVER_TO_START=' $STATUS_FILE | cut -c17-`
else
	SERVER_TO_START='true'   # This is for 5.1 only, to not change behavior
fi
# echo "Analyzed: SERVER_TO_START=$SERVER_TO_START"
if [ ! -d $mysql_datadir/mysql ] ; then
	mkdir $mysql_datadir/mysql;
	echo "MySQL RPM installation of version $NEW_VERSION" >> $STATUS_FILE
else
	# If the directory exists, we may assume it is an upgrade.
	echo "MySQL RPM upgrade to version $NEW_VERSION" >> $STATUS_FILE
fi
if [ ! -d $mysql_datadir/test ] ; then mkdir $mysql_datadir/test; fi

# ----------------------------------------------------------------------
# Create a MySQL user and group. Do not report any problems if it already
# exists.
# ----------------------------------------------------------------------
mkgroup %{mysqld_group} 2> /dev/null || true
useradd -d $mysql_datadir -s /bin/bash -c "MySQL server" -g %{mysqld_group} %{mysqld_user} 2> /dev/null || true
# The user may already exist, make sure it has the proper group nevertheless (BUG#12823)
chgroup users=%{mysqld_user} %{mysqld_group} 2>/dev/null || true

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
	%{_sysconfdir}/mysql/init.d/mysql start

	# Allow mysqld_safe to start mysqld and print a message before we exit
	sleep 5
fi

echo "Thank you for installing the MySQL Community Server! For Production
systems, we recommend MySQL Enterprise, which contains enterprise-ready
software, intelligent advisory services, and full production support with
scheduled service packs and more.  Visit www.mysql.com/enterprise for more
information."

# Collect an upgrade history ...
echo "Upgrade/install finished at `date`"        >> $STATUS_FILE
echo                                             >> $STATUS_FILE
echo "====="                                     >> $STATUS_FILE
STATUS_HISTORY=$mysql_datadir/RPM_UPGRADE_HISTORY
cat $STATUS_FILE >> $STATUS_HISTORY
rm  $STATUS_FILE
  
%if %{CLUSTER_BUILD}
%post ndb-storage
mysql_clusterdir=/var/lib/mysql-cluster

# Create cluster directory if needed
if test ! -d $mysql_clusterdir; then mkdir -m 755 $mysql_clusterdir; fi
%endif

%preun server
if [ $1 = 0 ] ; then
	# Stop MySQL before uninstalling it
	if [ -x %{_sysconfdir}/mysql/init.d/mysql ] ; then
		%{_sysconfdir}/mysql/init.d/mysql stop > /dev/null
		# Remove autostart of MySQL
	fi
fi

# We do not remove the mysql user since it may still own a lot of
# database files.

# ----------------------------------------------------------------------
# Clean up the BuildRoot after build is done
# ----------------------------------------------------------------------
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

##############################################################################
#  Files section
##############################################################################

%files server
%defattr(-,root,system,0755)

%doc mysql-release-%{mysql_version}/COPYING mysql-release-%{mysql_version}/README
%doc mysql-release-%{mysql_version}/support-files/my-*.cnf
%if %{CLUSTER_BUILD}
%doc mysql-release-%{mysql_version}/support-files/ndb-*.ini
%endif

%doc %attr(644, root, system) %{_prefix}/info/mysql/mysql.info*

%if %{INNODB_BUILD}
%doc %attr(644, root, man) %{_mandir}/mysql/man1/innochecksum.1*
%endif
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
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_fix_privilege_tables.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_install_db.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_secure_installation.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_setpermission.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_upgrade.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlhotcopy.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlman.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man8/mysqlmanager.8*
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
%ghost %config(noreplace,missingok) %{_sysconfdir}/mysql/mysqlmanager.passwd

%if %{INNODB_BUILD}
%attr(755, root, system) %{_bindir}/mysql/innochecksum
%endif
%attr(755, root, system) %{_bindir}/mysql/my_print_defaults
%attr(755, root, system) %{_bindir}/mysql/myisam_ftdump
%attr(755, root, system) %{_bindir}/mysql/myisamchk
%attr(755, root, system) %{_bindir}/mysql/myisamlog
%attr(755, root, system) %{_bindir}/mysql/myisampack
%attr(755, root, system) %{_bindir}/mysql/mysql_convert_table_format
%attr(755, root, system) %{_bindir}/mysql/mysql_fix_extensions
%attr(755, root, system) %{_bindir}/mysql/mysql_fix_privilege_tables
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

%attr(755, root, system) %{_sbindir}/mysql
%attr(755, root, system) %{_libdir}/mysql/mysql/plugin

%attr(644, root, system) %config(noreplace,missingok) %{_sysconfdir}/mysql/logrotate.d/mysql
%attr(755, root, system) %{_sysconfdir}/mysql/init.d/mysql

%attr(755, root, system) %{_datadir}/mysql/mysql

%files client
%defattr(-, root, system, 0755)
%attr(755, root, system) %{_bindir}/mysql/mysql
%attr(755, root, system) %{_bindir}/mysql/msql2mysql
%attr(755, root, system) %{_bindir}/mysql/mysql_find_rows
%attr(755, root, system) %{_bindir}/mysql/mysql_waitpid
%attr(755, root, system) %{_bindir}/mysql/mysqlaccess
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
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlaccess.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqladmin.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlbinlog.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlcheck.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqldump.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlimport.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlshow.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqlslap.1*

%if %{CLUSTER_BUILD}
%files ndb-storage
%defattr(-,root,system,0755)
%attr(755, root, system) %{_sbindir}/mysql/ndbd
%doc %attr(644, root, man) %{_mandir}/mysql/man8/ndbd.8*

%files ndb-management
%defattr(-,root,system,0755)
%attr(755, root, system) %{_sbindir}/mysql/ndb_mgmd
%doc %attr(644, root, man) %{_mandir}/mysql/man8/ndb_mgmd.8*

%files ndb-tools
%defattr(-,root,root,0755)
%attr(755, root, system) %{_bindir}/mysql/ndb_config
%attr(755, root, system) %{_bindir}/mysql/ndb_desc
%attr(755, root, system) %{_bindir}/mysql/ndb_error_reporter
%attr(755, root, system) %{_bindir}/mysql/ndb_mgm
%attr(755, root, system) %{_bindir}/mysql/ndb_print_backup_file
%attr(755, root, system) %{_bindir}/mysql/ndb_print_schema_file
%attr(755, root, system) %{_bindir}/mysql/ndb_print_sys_file
%attr(755, root, system) %{_bindir}/mysql/ndb_restore
%attr(755, root, system) %{_bindir}/mysql/ndb_select_all
%attr(755, root, system) %{_bindir}/mysql/ndb_select_count
%attr(755, root, system) %{_bindir}/mysql/ndb_show_tables
%attr(755, root, system) %{_bindir}/mysql/ndb_size.pl
%attr(755, root, system) %{_bindir}/mysql/ndb_test_platform
%attr(755, root, system) %{_bindir}/mysql/ndb_waiter
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_config.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_desc.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_error_reporter.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_mgm.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_restore.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_print_backup_file.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_print_schema_file.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_print_sys_file.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_select_all.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_select_count.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_show_tables.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_size.pl.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_waiter.1*

%files ndb-extra
%defattr(-,root,root,0755)
%attr(755, root, system) %{_bindir}/mysql/ndb_delete_all
%attr(755, root, system) %{_bindir}/mysql/ndb_drop_index
%attr(755, root, system) %{_bindir}/mysql/ndb_drop_table
%attr(755, root, system) %{_sbindir}/mysql/ndb_cpcd
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_delete_all.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_drop_index.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_drop_table.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/ndb_cpcd.1*
%endif

%files devel
%defattr(-, root, system, 0755)
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_config.1*
%attr(755, root, system) %{_bindir}/mysql/mysql_config
%dir %attr(755, root, system) %{_includedir}/mysql
%dir %attr(755, root, system) %{_libdir}/mysql
%{_includedir}/mysql/*
%{_datadir}/mysql/aclocal/mysql.m4
%{_libdir}/mysql/mysql/libdbug.a
%{_libdir}/mysql/mysql/libheap.a
%if %{WITH_LIBGCC}
%{_libdir}/mysql/libmygcc.a
%endif
%{_libdir}/mysql/mysql/libmyisam.a
%{_libdir}/mysql/mysql/libmyisammrg.a
%{_libdir}/mysql/mysql/libmysqlclient.a
%{_libdir}/mysql/mysql/libmysqlclient_r.a
%{_libdir}/mysql/mysql/libmystrings.a
%{_libdir}/mysql/mysql/libmysys.a
%if %{CLUSTER_BUILD}
%{_libdir}/mysql/mysql/libndbclient.a
%endif
%{_libdir}/mysql/mysql/libvio.a
%{_libdir}/mysql/mysql/plugin
/usr/lib/*

%files shared
%defattr(-, root, system, 0755)
# Shared libraries (omit for architectures that don't support them)
%{_libdir}/mysql/mysql/libmysql*.a
%if %{CLUSTER_BUILD}
%{_libdir}/mysql/libndb*.so*
/usr/lib/*
%endif

%files test
%defattr(-, root, system, 0755)
%attr(-, root, system) %{_datadir}/mysql/mysql-test
%attr(755, root, system) %{_bindir}/mysql/mysql_client_test
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_client_test.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql-stress-test.pl.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql-test-run.pl.1*
%if %{EMBEDDED_BUILD}
%attr(755, root, system) %{_bindir}/mysql/mysql_client_test_embedded
%attr(755, root, system) %{_bindir}/mysql/mysqltest_embedded
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysql_client_test_embedded.1*
%doc %attr(644, root, man) %{_mandir}/mysql/man1/mysqltest_embedded.1*
%endif
/usr/bin/*

%if %{EMBEDDED_BUILD}
%files embedded
%defattr(-, root, system, 0755)
%attr(644, root, system) %{_libdir}/mysql/libmysqld.a
/usr/lib/*
%endif

##############################################################################
# The spec file changelog only includes changes made to the spec file
# itself - note that they must be ordered by date (important when
# merging BK trees)
##############################################################################
%changelog

* Tue Apr 19 2011 Gerard Visiedo <gerard.visiedo@bull.net> 5.1.56
- Initial port on AIX  5.1.56

