%define apache_version 2.2.3
%define apr_version 1.3.9
%define sqlite_version 3.4
%define swig_version 1.3.29
%define pyver 2.4

Summary: A Concurrent Versioning system similar to but better than CVS.
Name: subversion
Version: 1.6.6
Release: 1
License: BSD
Group: Utilities/System
URL: http://subversion.tigris.org
SOURCE0: subversion-%{version}.tar.gz
Patch1: subversion-0.31.0-rpath.patch
Patch2: subversion-1.6.6-aix_autogen.patch
Patch3: subversion-1.6.6-ltaix.patch
Requires: apr >= %{apr_version}
Requires: apr-util >= %{apr_version}
Requires: db >= 4.2.52
Requires: sqlite >= %{sqlite_version}
BuildPreReq: autoconf >= 2.53
BuildPreReq: automake
BuildPreReq: db >= 4.2.52
BuildPreReq: expat-devel
BuildPreReq: gettext
BuildPreReq: httpd >= %{apache_version}
BuildPreReq: apr-devel >= %{apr_version}
BuildPreReq: apr-util-devel >= %{apr_version}
BuildPreReq: libtool
BuildPreReq: libxslt
BuildPreReq: openssl-devel
BuildPreReq: perl
BuildPreReq: python
BuildPreReq: python-devel
BuildPreReq: sqlite-devel >= %{sqlite_version}
BuildPreReq: swig >= %{swig_version}
BuildPreReq: zlib-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

%description
Subversion is a concurrent version control system which enables one or more
users to collaborate in developing and maintaining a hierarchy of files and
directories while keeping a history of all changes.  Subversion only stores
the differences between versions, instead of every complete file.  Subversion
also keeps a log of who, when, and why changes occurred.

As such it basically does the same thing CVS does (Concurrent Versioning System)
but has major enhancements compared to CVS and fixes a lot of the annoyances
that CVS users face.

%package devel
Group: Utilities/System
Summary: Development package for Subversion developers.
Requires: subversion = %{version}-%{release}
%description devel
The subversion-devel package includes the static libraries and include files
for developers interacting with the subversion package.

%package tools
Group: Utilities/System
Summary: Tools for Subversion
%description tools
Tools for Subversion.


%prep
%setup -q
%patch1 -p1
%patch2 -p1

sh autogen.sh

# patch libtool after autogen so that the modification won't be erase.
%patch3 -p1 -b .ltaix

# Delete apr, apr-util, and neon from the tree as those packages should already
# be installed.
rm -rf apr apr-util neon

SED=/bin/sed
export SED
CFLAGS="-I/opt/freeware/include/ -D_GNU_SOURCE"  LIBS=' -L/opt/freeware/lib' \
CPPFLAGS='-I/opt/freeware/include' LDFLAGS="-L/opt/freeware/lib -L.libs/" \
./configure  --with-apr=%{_prefix} \
	--with-apr-util=%{_prefix} \
	--with-apxs=no \
	--prefix=%{_prefix}

%build
make clean
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{apache_dir}/conf
make install DESTDIR="$RPM_BUILD_ROOT"

# Add subversion.conf configuration file into httpd/conf.d directory.
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp packages/rpm/rhel-4/subversion.conf $RPM_BUILD_ROOT/etc/httpd/conf.d


# Set up contrib and tools package files.
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/subversion
cp -r tools $RPM_BUILD_ROOT/%{_libdir}/subversion
cp -r contrib $RPM_BUILD_ROOT/%{_libdir}/subversion


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,sys)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc subversion/LICENSE
%{_bindir}/svn
%{_bindir}/svnadmin
%{_bindir}/svndumpfilter
%{_bindir}/svnlook
%{_bindir}/svnserve
%{_bindir}/svnsync
%{_bindir}/svnversion
%{_libdir}/libsvn_client*so*
%{_libdir}/libsvn_delta*so*
%{_libdir}/libsvn_diff*so*
%{_libdir}/libsvn_fs*so*
%{_libdir}/libsvn_ra*so*
%{_libdir}/libsvn_repos*so*
%{_libdir}/libsvn_subr*so*
%{_libdir}/libsvn_wc*so*
%{_datadir}/locale/*/*/*
%{_datadir}/man/man1/*
%{_datadir}/man/man5/*
%{_datadir}/man/man8/*

%files devel
%defattr(-,root,sys)
%{_libdir}/libsvn*.a
%{_libdir}/libsvn*.la
%{_includedir}/subversion-1/*

%files tools
%defattr(-,root,sys)
%{_libdir}/subversion/tools
%{_libdir}/subversion/contrib

%changelog
* Wed Mar 3 2010 Jean Noel Cordenner <jean-noel.cordenenr@bull.net> 1.6.6-1
- Initial port for AIX
