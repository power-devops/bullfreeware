%define apache_version 2.2.3
%define neon_version 0.29
%define apr_version 1.3.9
%define sqlite_version 3.4
%define swig_version 1.3.29
%define pyver 2.4

Summary: Modern Version Control System designed to replace CVS
Name: subversion
Version: 1.6.9
Release: 1
License: Apache License
Group: Development/Tools
URL: http://subversion.tigris.org/
Source0: http://subversion.tigris.org/tarballs/%{name}-%{version}.tar.gz
Source2: httpd-subversion.conf
Patch1: subversion-%{version}-rpath.patch
Patch2: subversion-%{version}-aix_autogen.patch
Patch3: subversion-%{version}-ltaix.patch
Requires: apr >= %{apr_version}
Requires: apr-util >= %{apr_version}
Requires: neon >= %{neon_version}
Requires: db >= 4.2.52
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
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file.  Subversion is intended to be a
compelling replacement for CVS.


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


%prep
%setup -q
%patch1 -p1
%patch2 -p1

sh autogen.sh

# patch libtool after autogen so that the modification won't be erase.
%patch3 -p1 -b .ltaix

%build
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include -DSVN_NEON_0_26' LDFLAGS="-L/opt/freeware/lib" \
./configure --with-apr=%{_prefix} \
        --with-apr-util=%{_prefix} --enable-shared \
        --with-apxs --with-neon=%{prefix} --with-serf=no \
        --prefix=%{_prefix}
make  clean
make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR="$RPM_BUILD_ROOT"

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# add subversion.conf configuration file into httpd/conf.d directory.
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/httpd/conf/extra/*

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


%post -n mod_dav_svn
cat %{_prefix}/etc/httpd/conf/httpd.conf | \
  grep -v "# Subversion settings" | \
  grep -v "Include conf/extra/httpd-subversion.conf" \
  > %{_prefix}/etc/httpd/conf/tmp_httpd.conf
mv -f %{_prefix}/etc/httpd/conf/tmp_httpd.conf %{_prefix}/etc/httpd/conf/httpd.conf
echo "# Subversion settings" >> %{_prefix}/etc/httpd/conf/httpd.conf
echo "Include conf/extra/httpd-subversion.conf" >> %{_prefix}/etc/httpd/conf/httpd.conf
echo "Please restart your web server using: '/opt/freeware/apache/bin/apachectl restart'"


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
%defattr(-,root,sys)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc subversion/LICENSE mod_authz_svn-INSTALL
%{_bindir}/*
%{_libdir}/libsvn_*.so*
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
%{_datadir}/man/man8/*
%{_datadir}/locale/*/LC_MESSAGES/*
/usr/bin/*
/usr/lib/libsvn_*.so*

%files devel
%defattr(-,root,sys)
%{_includedir}/subversion-1/*
%{_libdir}/libsvn*.a
%{_libdir}/libsvn*.la

%files -n mod_dav_svn
%defattr(-,root,sys)
%config(noreplace) %{_prefix}/etc/httpd/conf/extra/httpd-subversion.conf
%{_prefix}/apache/modules/mod_dav_svn.so
%{_prefix}/apache/modules/mod_authz_svn.so


%changelog
* Thu Oct 7 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.9-1
- Update to version 1.6.9
- debug mod_dav_svn

* Wed Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-2
- add mod_dav_svn and mod_authz_svn modules to subversion

* Wed Mar 3 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-1
- Initial port for AIX
