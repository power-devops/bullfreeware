%define httpd_version 2.2.17
%define neon_version 0.29
%define apr_version 1.4.6
%define apr_util_version 1.5
%define sqlite_version 3.7
%define swig_version 2.0.10
%define db_version 4.8.24
%define pyver 2.7
%define file_version 5.05
%define openssl_version 1.0.1
%define expat_version 2.0.0

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

# If you don't want to take time for the tests then set make_*_check to 0.
%define make_ra_local_bdb_check %{DO_TESTS}
%define make_ra_svn_bdb_check %{DO_TESTS}
%define make_ra_dav_bdb_check %{DO_TESTS}
%define make_ra_local_fsfs_check %{DO_TESTS}
%define make_ra_svn_fsfs_check %{DO_TESTS}
%define make_ra_dav_fsfs_check %{DO_TESTS}
Summary: A Concurrent Versioning system similar to but better than CVS.

Name: subversion
Version: 1.9.4
Release: 2
Copyright: BSD
Group: Utilities/System

URL: http://subversion.tigris.org/
Source0: http://apache.mindstudios.com/subversion/%{name}-%{version}.tar.bz2
Source1: http://apache.mindstudios.com/subversion/%{name}-%{version}.tar.bz2.asc
Source2: %{name}-%{version}-%{release}.build.log
Source3: httpd-subversion.conf

Patch0:  %{name}-%{version}-sqlite3.patch
Patch1:  %{name}-%{version}-usrlocalbin.patch
Source4: %{name}-%{version}-makefile.patch

Requires: apr >= %{apr_version}
Requires: apr-util >= %{apr_util_version}
#Requires: neon >= %{neon_version}
Requires: db >= %{db_version}
Requires: sqlite >= %{sqlite_version}
Requires: expat >= %{expat_version}
Requires: openssl >= %{openssl_version}
Requires: python
Requires: python3
Requires: sqlite >= %{sqlite_version}
Requires: file >= %{file_version}
Requires: httpd >= %{httpd_version}
Requires: zlib
#BuildPreReq: gettext-devel >= 0.17
#BuildPreReq: apr-devel >= %{apr_version}
#BuildPreReq: apr-util-devel >= %{apr_version}
#BuildPreReq: neon-devel >= %{neon_version}
BuildPreReq: sqlite-devel >= %{sqlite_version}
BuildPreReq: expat-devel >= %{expat_version}
#BuildPreReq: openssl-devel >= %{openssl_version}
BuildPreReq: sqlite-devel >= %{sqlite_version}
BuildPreReq: file-devel >= %{file_version}
BuildPreReq: httpd-devel >= %{httpd_version}
#BuildPreReq: swig >= %{swig_version}
BuildPreReq: zlib-devel
BuildPreReq: perl
BuildPreReq: python
BuildPreReq: python-devel

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
%patch0 -p1 -b .sqlite3
%patch1 -p1 -b .usrlocalbin

%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/vac/bin:.
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export MKDIR="/usr/bin/mkdir -p"
export CC=/usr/vac/bin/xlc_r
export CXX=/usr/vacpp/bin/xlC_r
export LDFLAGS="-L/opt/freeware/lib -bmaxdata:0x80000000 -brtl"
export CPPFLAGS="-DSVN_NEON_0_28 -DSVN_NEON_0_27 -DSVN_NEON_0_26 -DSVN_NEON_0_25"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --enable-shared --disable-static \
    --disable-neon-version-check \
    --disable-mod-activation \
    --with-sqlite=%{_prefix} \
    --with-zlib=%{_prefix} \
    --with-apxs=%{_bindir}/apxs \
    --with-ssl \
    --with-openssl

# Due to configure issue
sed "s;-L%{_liddir};-L/opt/freeware/lib;" Makefile >Makefile.tmp
[ -s Makefile.tmp ] && mv -f Makefile.tmp Makefile

patch -p0 < %{SOURCE4}
gmake 

# Build python bindings
gmake swig-py

# Build PERL bindings
gmake swig-pl DESTDIR=$RPM_BUILD_ROOT

%if %{make_ra_local_bdb_check}
echo "*** Running regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
( make check CLEANUP=true FS_TYPE=bdb || true )
echo "*** Finished regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
%endif

%if %{make_ra_svn_bdb_check}
echo "*** Running regression tests on RA_SVN (SVN method) layer ***"
( make svnserveautocheck CLEANUP=true FS_TYPE=bdb || true )
echo "*** Finished regression tests on RA_SVN (SVN method) layer ***"
%endif

%if %{make_ra_dav_bdb_check}
echo "*** Running regression tests on RA_DAV (HTTP method) layer ***"
( make davautocheck CLEANUP=true FS_TYPE=bdb || true )
echo "*** Finished regression tests on RA_DAV (HTTP method) layer ***"
%endif

%if %{make_ra_local_fsfs_check}
echo "*** Running regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
( make check CLEANUP=true FS_TYPE=fsfs || true )
echo "*** Finished regression tests on RA_LOCAL (FILE SYSTEM) layer ***"
%endif

%if %{make_ra_svn_fsfs_check}
echo "*** Running regression tests on RA_SVN (SVN method) layer ***"
( make svnserveautocheck CLEANUP=true FS_TYPE=fsfs || true )
echo "*** Finished regression tests on RA_SVN (SVN method) layer ***"
%endif

%if %{make_ra_dav_fsfs_check}
echo "*** Running regression tests on RA_DAV (HTTP method) layer ***"
( make davautocheck CLEANUP=true FS_TYPE=fsfs || true )
echo "*** Finished regression tests on RA_DAV (HTTP method) layer ***"
%endif

#make check 2>&1 | tee /tmp/%{name}-%{version}.MakeCheck.log

%install
export PATH="$PATH:/usr/vac/bin"
export RM="rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR="$RPM_BUILD_ROOT"

#/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/*

# Install Python SWIG bindings.
gmake install-swig-py DESTDIR=$RPM_BUILD_ROOT DISTUTIL_PARAM=--prefix=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python%{pyver}/site-packages
mv ${RPM_BUILD_ROOT}%{_libdir}/svn-python/* ${RPM_BUILD_ROOT}%{_libdir}/python%{pyver}/site-packages
rmdir  ${RPM_BUILD_ROOT}%{_libdir}/svn-python

# Install PERL SWIG bindings.
gmake install-swig-pl DESTDIR=$RPM_BUILD_ROOT

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
#mkdir -p $RPM_BUILD_ROOT%{_libdir}/subversion
#cp -r tools $RPM_BUILD_ROOT%{_libdir}/subversion
#cp -r contrib $RPM_BUILD_ROOT%{_libdir}/subversion


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
%doc BUGS CHANGES COMMITTERS INSTALL README
%doc tools LICENSE mod_authz_svn-INSTALL
%{_bindir}/*
%{_libdir}/libsvn_*.so*
%{_mandir}/man*/*
%{_datadir}/locale/*/LC_MESSAGES/*
/usr/bin/*
/usr/lib/libsvn_*.so*

%files devel
%defattr(-,root,system)
%{_includedir}/subversion-1/*
%{_libdir}/libsvn*.*a
/usr/include/*
/usr/lib/libsvn*.*a


%files -n mod_dav_svn
%defattr(-,root,system)
%config(noreplace) %{_prefix}/etc/httpd/conf/extra/httpd-subversion.conf
%{_prefix}/libexec/mod_dav_svn.so
%{_prefix}/libexec/mod_authz_svn.so

%files tools
%defattr(-,root,system)
%{_libdir}/python%{pyver}/*
/usr/opt/perl5/lib/5.8.8/*
/usr/opt/perl5/lib/site_perl/5.8.8/*
/usr/opt/perl5/man/*


%changelog
* Wed Aug 09 2016 Tony Reix <tony.reix@atos.net> 1.9.4-2
- Fix issues: neon not required, python3 Requires, /usr/local/bin path

* Wed Jul 21 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 1.9.4-1
- Update to version 1.9.4

* Fri Jul 12 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.7.9-1
- Update to version 17.9. Build on Aix6.1

* Mon Jul 08 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.6.23-1
- Update to version 1.6.23 . Build on Aix5.3

* Fri Jun 30 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.6.17-1
- Update to version 1.6.17

* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.9-1
- Update to version 1.6.9
- debug mod_dav_svn

* Wed Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-2
- add mod_dav_svn and mod_authz_svn modules to subversion

* Wed Mar 3 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-1
- Initial port for AIX
