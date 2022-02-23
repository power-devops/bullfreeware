%define apache_version 2.2.3
%define neon_version 0.29
%define apr_version 1.3.9
%define sqlite_version 3.6
%define swig_version 1.3.39
%define db_version 4.2.52
%define pyver 2.6

# If you don't want to take time for the tests then set make_*_check to 0.
%define make_ra_local_bdb_check 0
%define make_ra_svn_bdb_check 0
%define make_ra_dav_bdb_check 0
%define make_ra_local_fsfs_check 0
%define make_ra_svn_fsfs_check 0
%define make_ra_dav_fsfs_check 0
Summary: A Concurrent Versioning system similar to but better than CVS.

Name: subversion
Version: 1.6.17
Release: 1
Copyright: BSD
Group: Utilities/System

URL: http://subversion.tigris.org/
Source0: %{name}-%{version}.tar.gz
Source2: httpd-subversion.conf
Requires: apr >= %{apr_version}
Requires: apr-util >= %{apr_version}
Requires: neon >= %{neon_version}
Requires: db >= %{db_version}
Requires: sqlite >= %{sqlite_version}
Requires: zlib
BuildPreReq: gettext-devel >= 0.17
BuildPreReq: apr-devel >= %{apr_version}
BuildPreReq: apr-util-devel >= %{apr_version}
BuildPreReq: neon-devel >= %{neon_version}
BuildPreReq: sqlite-devel >= %{sqlite_version}
BuildPreReq: expat-devel
BuildPreReq: openssl-devel
BuildPreReq: perl
BuildPreReq: python
BuildPreReq: python-devel
BuildPreReq: sqlite-devel >= %{sqlite_version}
BuildPreReq: swig >= %{swig_version}
BuildPreReq: zlib-devel
BuildRoot: /var/tmp/%{name}-%{version}-root

%description
Subversion is a concurrent version control system which enables one or more
users to collaborate in developing and maintaining a hierarchy of files and
directories while keeping a history of all changes.  Subversion only stores
the differences between versions, instead of every complete file.  Subversion
also keeps a log of who, when, and why changes occurred.

As such it basically does the same thing CVS does (Concurrent Versioning System)
but has major enhancements compared to CVS and fixes a lot of the annoyances
that CVS users face.

*** Note: This is a relocatable package; it can be installed anywhere you like
with the "rpm -Uvh --prefix /your/favorite/path" command. This is useful
if you don't have root access on your machine but would like to use this
package.

%package devel
Group: Development/Tools
Summary: Development package for the Subversion libraries
Requires: subversion = %{version}-%{release}

%description devel
The subversion-devel package includes the static libraries and
include files for developers interacting with the subversion
package.

%package -n mod_dav_svn
Group: System Environment/Daemons
Summary: Apache server module for Subversion server
Requires: httpd >= 2.2.6
Requires: subversion = %{version}-%{release}
BuildRequires: httpd-devel >= 2.2.6

%description -n mod_dav_svn
The mod_dav_svn package allows access to a Subversion repository
using HTTP, via the Apache httpd server.

%package tools
Group: Utilities/System
Summary: Tools for Subversion
Requires: subversion = %{version}-%{release}
%description tools
Tools for Subversion.


%prep
%setup -q

sh autogen.sh

# Delete apr, apr-util, and neon from the tree as those packages should already
# be installed.
rm -rf apr apr-util neon


%build
export RM="rm -f"
export PATH="$PATH:/usr/vac/bin"
export CC="/usr/vac/bin/xlc_r -O2"
export CXX="/usr/vacpp/bin/xlC_r -O2"
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--with-apr=%{_prefix} \
        --with-apr-util=%{_prefix} \
	--with-swig=%{_bindir}/swig \
	--with-serf=no \
	--with-apxs \
        --enable-shared \
	--with-neon=%{_prefix}
make 

# Build python bindings
make swig-py

# Build PERL bindings
make swig-pl DESTDIR=$RPM_BUILD_ROOT
## VSD BAD .... make check-swig-pl

%if %{make_ra_local_bdb_check}
echo "*** Running regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
make check CLEANUP=true FS_TYPE=bdb
echo "*** Finished regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
%endif

%if %{make_ra_svn_bdb_check}
echo "*** Running regression tests on RA_SVN (SVN method) layer ***"
make svnserveautocheck CLEANUP=true FS_TYPE=bdb
echo "*** Finished regression tests on RA_SVN (SVN method) layer ***"
%endif

%if %{make_ra_dav_bdb_check}
echo "*** Running regression tests on RA_DAV (HTTP method) layer ***"
make davautocheck CLEANUP=true FS_TYPE=bdb
echo "*** Finished regression tests on RA_DAV (HTTP method) layer ***"
%endif

%if %{make_ra_local_fsfs_check}
echo "*** Running regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
make check CLEANUP=true FS_TYPE=fsfs
echo "*** Finished regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
%endif

%if %{make_ra_svn_fsfs_check}
echo "*** Running regression tests on RA_SVN (SVN method) layer ***"
make svnserveautocheck CLEANUP=true FS_TYPE=fsfs



 "*** Finished regression tests on RA_SVN (SVN method) layer ***"
%endif

%if %{make_ra_dav_fsfs_check}
echo "*** Running regression tests on RA_DAV (HTTP method) layer ***"
make davautocheck CLEANUP=true FS_TYPE=fsfs
echo "*** Finished regression tests on RA_DAV (HTTP method) layer ***"
%endif

%install
export PATH="$PATH:/usr/vac/bin"
export RM="rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR="$RPM_BUILD_ROOT"

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

## louche # add subversion.conf configuration file into httpd/conf.d directory.
## louche mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/*

# Install Python SWIG bindings.
make install-swig-py DESTDIR=$RPM_BUILD_ROOT DISTUTIL_PARAM=--prefix=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python%{pyver}/site-packages
mv ${RPM_BUILD_ROOT}%{_libdir}/svn-python/* ${RPM_BUILD_ROOT}%{_libdir}/python%{pyver}/site-packages
rmdir  ${RPM_BUILD_ROOT}%{_libdir}/svn-python

# Install PERL SWIG bindings.
make install-swig-pl DESTDIR=$RPM_BUILD_ROOT

# Rename authz_svn INSTALL doc for docdir
ln -f subversion/mod_authz_svn/INSTALL mod_authz_svn-INSTALL

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

# Set up contrib and tools package files.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/subversion
cp -r tools $RPM_BUILD_ROOT%{_libdir}/subversion
cp -r contrib $RPM_BUILD_ROOT%{_libdir}/subversion

%post -n mod_dav_svn
if [ -d %{_prefix}/etc/httpd/conf/httpd.conf ]; then
   cat %{_prefix}/etc/httpd/conf/httpd.conf | \
   grep -v "# Subversion settings" | \
   grep -v "Include conf/extra/httpd-subversion.conf" \
   > %{_prefix}/etc/httpd/conf/tmp_httpd.conf
   mv -f %{_prefix}/etc/httpd/conf/tmp_httpd.conf %{_prefix}/etc/httpd/conf/httpd.conf
fi
echo # Subversion settings" >> %{_prefix}/etc/httpd/conf/httpd.conf
echo "Include conf/extra/httpd-subversion.conf" >> %{_prefix}/etc/httpd/conf/httpd.conf
echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"


%preun -n mod_dav_svn
if [ "$1" = 0 ]; then
    cat %{_prefix}/etc/httpd/conf/httpd.conf | \
      grep -v "# Subversion settings" | \
      grep -v "Include conf/extra/httpd-subversion.conf" \
      > %{_prefix}/etc/httpd/conf/tmp_httpd.conf
    mv -f %{_prefix}/etc/httpd/conf/tmp_httpd.conf %{_prefix}/etc/httpd/conf/httpd.conf
    echo "Please restart your web server using: '/opt/freeware/sbin/apachectl restart'"
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc tools subversion/LICENSE mod_authz_svn-INSTALL
%{_bindir}/*
%{_libdir}/libsvn_*.so*
%{_mandir}/man*/*
%{_datadir}/locale/*/LC_MESSAGES/*
/usr/bin/*
/usr/lib/libsvn_*.so*

%files devel
%defattr(-,root,system)
%{_includedir}/subversion-1/*
%{_libdir}/libsvn*.a
%{_libdir}/libsvn*.la
/usr/include/*
/usr/lib/libsvn*.*a


%files -n mod_dav_svn
%defattr(-,root,system)
%config(noreplace) %{_prefix}/etc/httpd/conf/extra/httpd-subversion.conf
%{_prefix}/apache/modules/mod_dav_svn.so
%{_prefix}/apache/modules/mod_authz_svn.so

%files tools
%defattr(-,root,system)
%{_libdir}/subversion/*
%{_libdir}/python%{pyver}/*


%changelog
* Fri Jun 30 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.6.17-1
- Update to version 1.6.17

* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.9-1
- Update to version 1.6.9
- debug mod_dav_svn

* Wed Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-2
- add mod_dav_svn and mod_authz_svn modules to subversion

* Wed Mar 3 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-1
- Initial port for AIX
