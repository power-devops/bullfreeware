
# Tests for this package.
# They need a mysqld server running.
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64
%define pkg_name mariadb
%define logfile /opt/freeware/var/log/mariadb/mariadb.log


# ======
# Config
# ======
%define debug     0
# Provide mysql names for compatibility
%bcond_with mysql_names
# SSL
# BUNDLE => YaSSL + GNUTLS
# SYSTEM => OpenSSL
%define ssl   SYSTEM
%if %{ssl} != "SYSTEM" && %{ssl} != "BUNDLE"
  echo "ssl must be SYSTEM or BUNDLE."
  exit 1
%endif
%if %{ssl} == "SYSTEM"
# Use AIX Openssl
# Requires:   openssl
%else
Requires:   gnutls
%endif


Name:           mariadb-connector-c
Version:        3.1.9
Release:        1
Summary:        The MariaDB Native Client library (C driver)
Group:          Servers
License:        LGPLv2+
Source:         https://downloads.mariadb.org/interstitial/connector-c-%{version}/mariadb-connector-c-%{version}-src.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
Url:            http://mariadb.org/

# See  mariadb-10.3.12_int8.patch
Patch1:       mariadb-connector-c-3.0.10-1-int8.patch 
# See mariadb-10.3.10_dontwait.patch
Patch2:       mariadb-connector-c-3.1.9-1-MSG_DONTWAIT.patch
# See mariadb-10.3.12-compile_new_cmake.patch
Patch5:       mariadb-connector-c-3.1.9-compile_new_cmake.patch
# See mariadb-10.3.15-krb5.patch
Patch6:       mariadb-connector-c-3.0.10-1-krb5.patch
# See mariadb-10.3.12-libsuffix.patch
Patch7:       mariadb-connector-c-3.0.10-2-libsuffixNEW.patch
# See mariadb-10.3.12.mariadb_config.patch 
Patch9:       mariadb-connector-c-3.1.6-1-mariadb_config.patch
# Correct .pc file for compatibility
Patch10:      mariadb-connector-c-3.1.9-compat.patch

Requires:  libiconv >= 1.16-2

# More information: https://mariadb.com/kb/en/mariadb/building-connectorc-from-source/

BuildRequires:  zlib-devel cmake gcc-c++
BuildRequires:  cmake >= 3.16
BuildRequires:  compat-getopt-devel

# Remote-IO plugin
BuildRequires:  curl-devel

# my.cnf is provided by mysql-config
Requires:       mysql-config

Requires:       compat-getopt


%description
The MariaDB Native Client library (C driver) is used to connect applications
developed in C/C++ to MariaDB and MySQL databases.


%package devel
Summary:        Development files for mariadb-connector-c
Group:          devel 
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for mariadb-connector-c.
Contains everything needed to build against libmariadb.so >=3 client library.


%package static
Summary:        Static libraries for mariadb-connector-c
Requires:       %{name} = %{version}-%{release}

%description static
Static libraries for mariadb-connector-c.
Contains static libraries needed to build some MariaDB tools.


%prep
%setup -q -n mariadb-connector-c-%{version}-src

%patch1  -p1  -b  .int8
%patch2  -p1  -b  .MSG_DONTWAIT
%patch5  -p1  -b  .compile_new_cmake
%patch6  -p1  -b  .krb5
%patch7  -p1  -b  .libsuffix
%patch9  -p1  -b  .config
%patch10 -p1  -b  .compat

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
env | sort

export PATH=/opt/freeware/bin:/usr/bin

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"

export FLAG32="-maix32"
export FLAG64="-maix64"

echo "GCC Version:"
$CC --version

# Force cmake to user AIX ar command
export AR=/usr/bin/ar
export NM=/usr/bin/nm

export MAKE="gmake --trace %{?_smp_mflags}"

# https://jira.mariadb.org/browse/MDEV-13836:
#   The server has (used to have for ages) some magic around the port number.
#   If it's 0, the default port value will use getservbyname("mysql", "tcp"), that is, whatever is written in /etc/services.
#   If it's a positive number, say, 3306, it will be 3306, no matter what /etc/services say.
#   I don't know if that behavior makes much sense, /etc/services wasn't supposed to be a system configuration file.

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

run_compile()
{
set -ex

cmake . -L \
%if %{debug} == 1
         -DCMAKE_BUILD_TYPE=DEBUG \
%else
         -DCMAKE_BUILD_TYPE=RELEASE \
%endif
         -DOBJECT_MODE="$OBJECT_MODE" \
         -DCMAKE_POLICY_DEFAULT_CMP0065=NEW \
         -DCMAKE_INSTALL_RPATH=$PATH_MODE \
         -DCMAKE_BUILD_RPATH=$PATH_MODE \
         -DLOG_LOCATION="%{logfile}" \
         -DNICE_PROJECT_NAME="MariaDB" \
         -DMARIADB_UNIX_ADDR=%{_prefix}/var/lib/mysql/mysql.sock \
         -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
         -DINSTALL_INCLUDEDIR=include/mariadb \
         -DINSTALL_LIBDIR="%{_lib}$OBJECT_MODE_LIB" \
         -DINSTALL_PLUGINDIR="%{_lib}$OBJECT_MODE_LIB/%{pkg_name}/plugin" \
         -DENABLED_LOCAL_INFILE=ON \
         -DSECURITY_HARDENED=ON \
         -DWITH_MYSQLCOMPAT=%{?with_mysql_names:YES}%{!?with_mysql_names:NO} \
         -DWITH_UNIT_TESTS=%{?with_dotests:ON}%{!?with_dotests:NO} \
%if %{ssl} == "SYSTEM"
         -DWITH_SSL="OPENSSL" \
%else
         -DWITH_SSL= bundle \
%endif
         -DWITH_EXTERNAL_ZLIB=YES \
         -DICONV_LIBRARIES=/opt/freeware/lib/libiconv.a \
         -DPLUGIN_CLIENT_ED25519=OFF \
%if %{debug} == 1
         -DWITH_ASAN=OFF -DWITH_INNODB_EXTRA_DEBUG=NO
%endif

}


############################### 64-bit BEGIN ##############################
# first build the 64-bit version

cd 64bit
export OBJECT_MODE=64
export OBJECT_MODE_LIB=64
export PATH_MODE="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

export CFLAGS="-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -pthread ${FLAG64}"
export CFLAGS="$CFLAGS -mcmodel=large -fno-omit-frame-pointer -fno-strict-aliasing"
export LDFLAGS="-pthread"
export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

%if %{debug} == 1
CFLAGS="$CFLAGS -O0"
%endif

export CXXFLAGS="$CFLAGS"

run_compile
$MAKE

############################### 32-bit BEGIN ##############################

cd ../32bit

export OBJECT_MODE=32
export OBJECT_MODE_LIB=""
export PATH_MODE="/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"

export CFLAGS="-D_GNU_SOURCE -D_LARGEFILE_SOURCE -pthread ${FLAG32}"
export CFLAGS="$CFLAGS -mcmodel=large -fno-omit-frame-pointer -fno-strict-aliasing"
export LDFLAGS="-pthread -Wl,-bmaxdata:0x80000000"
export LIBPATH="/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"

%if %{debug} == 1
CFLAGS="$CFLAGS -O0"
%endif

export CXXFLAGS="$CFLAGS"

run_compile
$MAKE

########################### END 32-bit #####################################


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%check
%if %{with dotests}
cd 32bit/unittest/libmariadb/
(ctest || true)
cd ../../../64bit/unittest/libmariadb/
(ctest || true)
%endif


%install

export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export MAKE="gmake --trace %{?_smp_mflags}"
export AR="/usr/bin/ar"
export STRIP="/usr/bin/strip"

############################### 32-bit BEGIN ##############################

cd 32bit
export OBJECT_MODE=32

$MAKE DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/mariadb_config ${RPM_BUILD_ROOT}%{_bindir}/mariadb_config_32

########################### END 32-bit #####################################

############################### 64-bit BEGIN ##############################

cd ../64bit
export OBJECT_MODE=64

$MAKE DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/mariadb_config ${RPM_BUILD_ROOT}%{_bindir}/mariadb_config_64

cd ..

########################### END 64-bit #####################################


# link 64 to 32 library
(
 cd ${RPM_BUILD_ROOT}%{_libdir64}
 $AR -X64 x libmariadb.a
 rm ./libmariadb.a
 $AR -X64 qc ../lib/libmariadb.a libmariadb.so.*
 ln -s ../lib/libmariadb.a libmariadb.a
)

# Add a compatibility symlinks
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  ln -s mariadb_config_64 mariadb_config
  cd ${RPM_BUILD_ROOT}%{_includedir}
  (ls -l mariadb_config mariadb_version.h || true)
)


%files
%defattr(-,root,system,-)
%{_libdir64}/libmariadb.a
%dir %{_libdir64}/mariadb
%dir %{_libdir64}/mariadb/plugin
%{_libdir64}/mariadb/plugin/*
%exclude %{_libdir64}/mariadb/plugin/auth_gssapi_client.so

%{_libdir}/libmariadb.a
%dir %{_libdir}/mariadb
%dir %{_libdir}/mariadb/plugin
%{_libdir}/mariadb/plugin/*
# caching_sha2_password.so, dialog.so, mysql_clear_password.so, remote_io.so, sha256_password.so
# auth_gssapi_client.so -> not provided
%exclude %{_libdir}/mariadb/plugin/auth_gssapi_client.so
%doc 32bit/README 32bit/COPYING.LIB

%files devel
%defattr(-,root,system,-)
# # Binary which provides compiler info for software compiling against this library
%{_bindir}/mariadb_config
%{_bindir}/mariadb_config_32
%{_bindir}/mariadb_config_64

%{_libdir}/pkgconfig/libmariadb.pc

# Header files
%dir %{_includedir}/mariadb
%{_includedir}/mariadb/*

%files static
%defattr(-,root,system,-)
%{_libdir}/libmariadbclient.a
%{_libdir64}/libmariadbclient.a


%changelog
* Mon Jul 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.9-1
- New version 3.1.9

* Wed Jan 22 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.6-1
- New version 3.1.6
- Provide static libraries
- Bullfreeware OpenSSL removal

* Mon Dec 02 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.5-1
- New version 3.1.5
- Increase compatibility with MySQL
- Compilation with new cmake.

* Thu Oct 03 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.4-2
- Correct config file

* Wed Sep 25 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.4-1
- New version 3.1.4

* Tue Sep 3 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.3-1
- New version 3.1.3

* Mon Aug 26 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.2-2
- No more provide auth_ed25519 (provided by server).

* Mon Jul 29 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.1.2-1
- New version 3.1.2

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
