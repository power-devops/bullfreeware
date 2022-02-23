%bcond_without dotests

%bcond_with bdb

# No python
%bcond_with python2
%bcond_with python3
%bcond_with pyswig

# No ruby
# swig use 32 bit as a default and cannot be configurated easily
# Try after rebuiding swig
%bcond_with ruby

# Provide a mod_dav_svn for apache httpd.
# Not provided for now because error in install part
%bcond_with httpd


%global _libdir64 %{_libdir}64

%global with_java 0

# set JDK path to build javahl; default for JPackage
%define jdk_path /usr/lib/jvm/java

%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

%global perl_vendorarch_32 %(eval "`%{_bindir}/perl_32 -V:installvendorarch`"; echo $installvendorarch)
%global perl_vendorarch_64 %(eval "`%{_bindir}/perl_64 -V:installvendorarch`"; echo $installvendorarch)

%global svn_python2_32 /opt/freeware/bin/python2_32
%global svn_python2_64 /opt/freeware/bin/python2_64
%global python2_sitearch_32   %(%{svn_python2_32} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%global python2_sitearch_64   %(%{svn_python2_64} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%global svn_python2_br python-devel

%global svn_python3_32 /opt/freeware/bin/python3_32
%global svn_python3_64 /opt/freeware/bin/python3_64
%global python3_minor_version %(%{svn_python3_64} -c "import sys; print(sys.version.split('.')[1])")
%global python3_sitearch_32 %(%{svn_python3_32} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global python3_sitearch_64 %(%{svn_python3_64} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")
%global svn_python3_br python3-devel

%global perl %{_bindir}/perl_64
%global perl_32 %{_bindir}/perl_32
%global perl_64 %{_bindir}/perl_64
%global perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%global ruby_ver 2.6
%global ruby_vendorarchdir_32 %{_libdir}/ruby/site_ruby/%{ruby_ver}/
%global ruby_vendorarchdir_64 %{_libdir64}/ruby/site_ruby/%{ruby_ver}/

%global http_mod32 %{_libdir}/httpd/modules/
%global http_mod64 %{_libdir64}/httpd/modules/

# Put Python bindings in site-packages
%global swigdirs2_32 swig_pydir=%{python2_sitearch_32}/libsvn swig_pydir_extra=%{svn_python_sitearch}/svn
%global swigdirs2_64 swig_pydir=%{python2_sitearch_64}/libsvn swig_pydir_extra=%{svn_python_sitearch}/svn
%global swigdirs3_32 swig_pydir=%{python3_sitearch_32}/libsvn swig_pydir_extra=%{svn_python_sitearch}/svn
%global swigdirs3_64 swig_pydir=%{python3_sitearch_64}/libsvn swig_pydir_extra=%{svn_python_sitearch}/svn


%global _httpd_modconfdir %{_sysconfdir}/httpd/conf
%global _httpd_confdir %{_sysconfdir}/httpd/conf

Summary: A Modern Concurrent Version Control System
Name:    subversion
Version: 1.13.0
Release: 1
License: ASL 2.0
URL: https://subversion.apache.org/

Source0: https://www.apache.org/dist/subversion/subversion-%{version}.tar.bz2
#Source1: subversion.conf
# Source3: filter-requires.sh
Source4: http://www.xsteve.at/prg/emacs/psvn.el
Source5: psvn-init.el
# Source6: svnserve.service
Source7: svnserve.tmpfiles
Source8: svnserve.sysconf
# Patch1: subversion-1.12.0-linking.patch
# Patch2: subversion-1.12.2-py3tests.patch
# Patch4: subversion-1.8.0-rubybind.patch
# Patch5: subversion-1.8.5-swigplWall.patch

Source1: httpd-subversion.conf
# Source2: subversion-Makefile.patch
Source1000: %{name}-%{version}-%{release}.build.log
Patch0: %{name}-1.10.6-sqlite3.patch
# Patch1: %{name}-1.10.6-perl.patch
# Patch2: %{name}-1.10.6-perl32bit.patch
Patch3: %{name}-1.10.6-io.patch

BuildRequires: autoconf, libtool, sed, findutils
BuildRequires: swig >= 1.3.24, gettext
%if %{with bdb}
BuildRequires: libdb-devel >= 4.1.25
%endif
BuildRequires: %{svn_python2_br}
BuildRequires: %{svn_python3_br}
BuildRequires: apr-devel >= 1.7.0, apr-util-devel >= 1.6.1
BuildRequires: serf-devel >= 1.3.0, cyrus-sasl-devel
BuildRequires: zlib-devel
BuildRequires: sqlite-devel >= 3.4.0
BuildRequires: lz4-devel
BuildRequires: file-devel
BuildRequires: gettext-devel

Provides: svn = %{version}-%{release}
Requires: subversion-libs%{?_isa} = %{version}-%{release}

##%define __perl_requires %{SOURCE3}


%description
Subversion is a concurrent version control system which enables one
or more users to collaborate in developing and maintaining a
hierarchy of files and directories while keeping a history of all
changes.  Subversion only stores the differences between versions,
instead of every complete file. Subversion is intended to be a
compelling replacement for CVS.

%package libs
Summary: Libraries for Subversion Version Control system
Requires: libgcc >= 6.3.0-1
Requires: gettext >= 0.19.8.1-3
Requires: serf >= 1.3.9-2
Requires: cyrus-sasl >= 2.1.26-2
Requires: zlib >= 1.2.11-1
Requires: apr >= 1.7.0
Requires: apr-util >= 1.6.1
Requires: file-libs

%description libs
The subversion-libs package includes the essential shared libraries
used by the Subversion version control tools.

%if %{with python2} && %{with pyswig}
%package -n python-subversion
Provides: %{name}-python = %{version}-%{release}
BuildRequires: python-devel
Summary: Python bindings for Subversion Version Control system

%description -n python-subversion
The python2-subversion package includes the Python 2.x bindings to the
Subversion libraries.
%endif


%if %{with python3} && %{with pyswig}
%package -n python3-subversion
Provides: %{name}-python3 = %{version}-%{release}
Summary: Python bindings for Subversion Version Control system
BuildRequires: python3-devel

%description -n python3-subversion
The python3-subversion package includes the Python 3.x bindings to the
Subversion libraries.
%endif


%package devel
Summary: Development package for the Subversion libraries
Requires: subversion = %{version}-%{release}
Requires: apr-devel >= 1.7.0, apr-util-devel >= 1.6.1

%description devel
The subversion-devel package includes the libraries and include files
for developers interacting with the subversion package.


%if %{with httpd}
%package -n mod_dav_svn
Summary: Apache httpd module for Subversion server
Requires: httpd >= 2.4.37-2
Requires: libgcc >= 6.3.0-1
Requires: sqlite >= 3.23.0-1
Requires: apr >= 1.5.2
Requires: apr-util >= 1.6.1
Requires: expat
Requires: subversion-libs = %{version}-%{release}
BuildRequires: httpd-devel >= 2.0.45

%description -n mod_dav_svn
The mod_dav_svn package allows access to a Subversion repository
using HTTP, via the Apache httpd server.
%endif


%package perl
Summary: Perl bindings to the Subversion libraries
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More), perl(ExtUtils::Embed)
Requires: perl(:MODULE_COMPAT_%{perl_version})
Requires: subversion = %{version}-%{release}

%description perl
This package includes the Perl bindings to the Subversion libraries.


%if %{with_java}
%package javahl
Summary: JNI bindings to the Subversion libraries
Requires: subversion = %{version}-%{release}
BuildRequires: java-devel-openjdk
# JAR repacking requires both zip and unzip in the buildroot
BuildRequires: zip, unzip
# For the tests
# BuildRequires: junit
BuildArch: noarch

%description javahl
This package includes the JNI bindings to the Subversion libraries.
%endif


%if %{with ruby}
%package ruby
Summary: Ruby bindings to the Subversion libraries
BuildRequires: ruby-devel, ruby(ruby) = %{ruby_ver}
# BuildRequires: rubygem(test-unit)
Requires: subversion = %{version}-%{release}

%description ruby
This package includes the Ruby bindings to the Subversion libraries.
%endif


%package tools
Summary: Supplementary tools for Subversion
Requires: subversion = %{version}-%{release}

%description tools
This package includes supplementary tools for use with Subversion.


%prep
%setup -q
%patch0 -p1 -b .sqlite3
%patch3 -p0
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


# %patch1 -p1 -b .linking
# %if %{with python3}
# %patch2 -p1 -b .py3tests
# %endif
# %patch4 -p1 -b .rubybind
# %patch5 -p1 -b .swigplWall

%build
# Regenerate the buildsystem, so that:
#  1) patches applied to configure.in take effect
#  2) the swig bindings are regenerated using the system swig
# (2) is not ideal since typically upstream test with a different
# swig version
# This PATH order makes the fugly test for libtoolize work...
# mv build-outputs.mk build-outputs.mk.old

export PATH=/opt/freeware/bin:/usr/bin

# # fix shebang lines, #111498
# perl -pi -e 's|/usr/bin/env perl -w|/usr/bin/perl -w|' tools/hook-scripts/*.pl.in
# fix python executable
# perl -pi -e 's|/usr/bin/env python.*|%{svn_python}|' subversion/tests/cmdline/svneditor.py

build_svn () {
    set -ex
    
    export CPPFLAGS=" -I/opt/freeware/include -I/opt/freeware/include/serf-1 -O2"
    # ./autogen.sh --release
    ./configure --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
            --prefix=%{_prefix} \
            --libdir=$1 \
            --bindir=%{_bindir} \
            --mandir=%{_prefix}/man \
            --disable-debug \
            --enable-shared \
            --disable-static \
            --disable-mod-activation \
            --with-sqlite=%{_prefix} \
            --with-zlib=%{_prefix} \
            --with-ssl \
            --with-openssl \
            --with-serf=%{_prefix} \
            --with-swig --with-serf=%{_prefix} \
    %if %{with ruby}
            --with-ruby-sitedir=$3 \
            --with-ruby-test-verbose=verbose \
    %endif
    %if %{with httpd}
            --with-apxs \
            --with-apache-libexecdir=$1/httpd/modules \
    %endif
            --with-sasl=%{_prefix} \
            --with-libmagic=$1 \
            --with-utf8proc=internal \
    %if %{with bdb}
            --with-berkeley-db \
    %else
            --without-berkeley-db \
    %endif
            || (cat config.log; exit 1)

    # sed -i "s;-L%{_libdir};-L$1;" Makefile
    # patch -p0 < %{SOURCE2}
    # patch -p0 < %{PATCH1}

    gmake %{?_smp_mflags} all tools

    %if %{with pyswig}
    gmake swig-py swig-py-lib $2
    %endif
    gmake swig-pl swig-pl-lib
    %if %{with ruby}
    gmake swig-rb swig-rb-lib
    %endif
}

#export APACHE_LDFLAGS="-Wl,-z,relro,-z,now"
cd 64bit
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64"
export CXX="/opt/freeware/bin/g++ -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -lz -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
# -Wl,-brtl

export PERL=%{perl_64}
export PYTHON=%{svn_python3_64}

# override weird -shrext from ruby
export svn_cv_ruby_link="$CC -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""

build_svn %{_libdir64} %{swigdirs2_64} %{ruby_vendorarchdir_64}

cd ../32bit
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32"
export CXX="/opt/freeware/bin/g++ -maix32"
export LDFLAGS="-L/opt/freeware/lib -lz -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
# -Wl,-brtl

export PERL=%{perl_32}
export PYTHON=%{svn_python3_32}

# override weird -shrext from ruby
export svn_cv_ruby_link="$CC -shared"
export svn_cv_ruby_sitedir_libsuffix=""
export svn_cv_ruby_sitedir_archsuffix=""

build_svn %{_libdir} %{swigdirs2_32} %{ruby_vendorarchdir_32}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

install_svn () {
    set -ex
    gmake install DESTDIR=$RPM_BUILD_ROOT

    # Python
    %if %{with pyswig}
    gmake install-swig-py %{swigdirs} DESTDIR=$RPM_BUILD_ROOT
    %endif

    # Perl
    gmake install-swig-pl-lib DESTDIR=$RPM_BUILD_ROOT
    gmake pure_vendor_install -C subversion/bindings/swig/perl/native \
            PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

    # Ruby
    %if %{with ruby}
    gmake install-swig-rb DESTDIR=$RPM_BUILD_ROOT
    %endif

    # Java
    %if %{with_java}
    gmake install-javahl-java install-javahl-lib javahl_javadir=%{_javadir} DESTDIR=$RPM_BUILD_ROOT
    %endif
    
    # The SVN build system is broken w.r.t. DSO support; it treats
    # normal libraries as DSOs and puts them in $libdir, whereas they
    # should go in some subdir somewhere, and be linked using -module,
    # etc.  So, forcibly nuke the .so's for libsvn_auth_{gnome,kde},
    # since nothing should ever link against them directly.
    rm -f ${RPM_BUILD_ROOT}$1/libsvn_auth_*.so
    
    # unnecessary libraries for swig bindings
    rm -f ${RPM_BUILD_ROOT}$1/libsvn_swig_*.so \
        ${RPM_BUILD_ROOT}$1/libsvn_swig_*.la
    
    # Remove unnecessary ruby libraries
    rm -f ${RPM_BUILD_ROOT}$2/svn/ext/*.*a
    
    mkdir -p ${RPM_BUILD_ROOT}$1/tmpfiles.d
    install -p -m 644 $RPM_SOURCE_DIR/svnserve.tmpfiles \
        ${RPM_BUILD_ROOT}$1/tmpfiles.d/svnserve.conf
}

cd 64bit
export OBJECT_MODE=64
install_svn %{_libdir64} %{ruby_vendorarchdir_64}

cd ../32bit
export OBJECT_MODE=32
install_svn %{_libdir} %{ruby_vendorarchdir_32}

cd ..

install -m 755 -d ${RPM_BUILD_ROOT}%{_sysconfdir}/subversion

%if %{with httpd}
mkdir -p ${RPM_BUILD_ROOT}%{_httpd_modconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_httpd_confdir}

%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# httpd <= 2.2.x
install -p -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_httpd_confdir}
%else
sed -n /^LoadModule/p %{SOURCE1} > 10-subversion.conf
sed    /^LoadModule/d %{SOURCE1} > example.conf
touch -r %{SOURCE1} 10-subversion.conf example.conf
install -p -m 644 10-subversion.conf ${RPM_BUILD_ROOT}%{_httpd_modconfdir}
%endif
%endif

# Remove unpackaged files
rm -rf ${RPM_BUILD_ROOT}%{_includedir}/subversion-*/*.txt \
       ${RPM_BUILD_ROOT}%{svn_python_sitearch}/*/*.a \
       ${RPM_BUILD_ROOT}%{svn_python_sitearch}/*/*.la 

# remove stuff produced with Perl modules
find $RPM_BUILD_ROOT -type f \
    -a \( -name .packlist -o \( -name '*.bs' -a -empty \) \) \
    -print0 | xargs -0 rm -f

# # make Perl modules writable so they get stripped
# find $RPM_BUILD_ROOT%{_libdir64}/perl5 -type f -perm 555 -print0 |
#         xargs -0 chmod a+r


# Trim what goes in docdir
rm -rvf tools/*/*.in tools/hook-scripts/mailer/tests

# Install psvn for emacs and xemacs
for f in emacs/site-lisp xemacs/site-packages/lisp; do
  install -m 755 -d ${RPM_BUILD_ROOT}%{_datadir}/$f
  install -m 644 $RPM_SOURCE_DIR/psvn.el ${RPM_BUILD_ROOT}%{_datadir}/$f
done

install -m 644 $RPM_SOURCE_DIR/psvn-init.el \
        ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# Rename authz_svn INSTALL doc for docdir
ln -f 32bit/subversion/mod_authz_svn/INSTALL mod_authz_svn-INSTALL

# # Trim exported dependencies to APR libraries only:
# sed -i "/^dependency_libs/{
#      s, -l[^ ']*, ,g;
#      s, -L[^ ']*, ,g;
#      s,%{_libdir}/lib[^a][^p][^r][^ ']*.la, ,g;
#      }"  $RPM_BUILD_ROOT%{_libdir64}/*.la

# Install bash completion
install -Dpm 644 32bit/tools/client-side/bash_completion \
        $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/svn
for comp in svnadmin svndumpfilter svnlook svnsync svnversion; do
    ln -sf svn \
        $RPM_BUILD_ROOT%{_datadir}/bash-completion/completions/${comp}
done

# Install svnserve bits
mkdir -p %{buildroot}/run/svnserve \
         %{buildroot}%{_sysconfdir}/sysconfig


install -p -m 644 $RPM_SOURCE_DIR/svnserve.sysconf \
        %{buildroot}%{_sysconfdir}/sysconfig/svnserve

# # Does not work on AIX
# # Install tools ex diff*, x509-parser
# gmake install-tools DESTDIR=$RPM_BUILD_ROOT toolsdir=%{_bindir}
# rm -f $RPM_BUILD_ROOT%{_bindir}/diff* $RPM_BUILD_ROOT%{_bindir}/x509-parser

# Don't add spurious dependency in libserf-devel
( sed -i "/^Requires.private/s, serf-1, ," \
    $RPM_BUILD_ROOT%{_datadir}/pkgconfig/libsvn_ra_serf.pc || true)

# Make svnauthz-validate a symlink
ln -sf svnauthz $RPM_BUILD_ROOT%{_bindir}/svnauthz-validate

# TODO These binaries does not existe
# svnauthz svnauthz-validate svnraisetreeconflict
# fsfs-stats fsfs-access-map svnmover svnconflict
# svn-populate-node-origins-index svn-mergeinfo-normalizer
for f in svnmucc svnbench ; do
    echo %{_bindir}/$f
    if test -f $RPM_BUILD_ROOT%{_mandir}/man?/${f}.*; then
       echo %{_mandir}/man?/${f}.*
    fi
done | tee tools.files | sed 's/^/%%exclude /' > exclude.tools.files

%find_lang %{name}

cat %{name}.lang exclude.tools.files >> %{name}.files

# Man files are not in the right location
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3 ${RPM_BUILD_ROOT}%{_mandir}

# Avoid /usr/bin/python dependency
/opt/freeware/bin/sed -i -e 's|#!/usr/bin/python|#!/usr/bin/env python2|' 32bit/tools/examples/SvnCLBrowse

# Build AIX-style shared libraries
(
    cd ${RPM_BUILD_ROOT}%{_libdir}
    for f in `ls *.a`; do
        /usr/bin/ar -X64 -x  ../lib64/${f}
        /usr/bin/ar -X64 -qc ${f} `basename ${f} .a`.so.*
    done
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for f in `ls *.a`; do
        ln -sf ../lib/${f} ${f}
    done
)


%check
%if %{with dotests}
check_svn () {
    set -ex
    export LANG=C LC_ALL=C
    export LD_LIBRARY_PATH=$RPM_BUILD_ROOT$1
    export MALLOC_PERTURB_=171 MALLOC_CHECK_=3
    export LIBC_FATAL_STDERR_=1
    # export PYTHON=%{svn_python}
    if ! gmake check CLEANUP=yes; then
    : Base test suite failure.
    cat fails.log
    exit 1
    fi
    if ! gmake check-swig-pl; then
    : Perl swig test failure.
    exit 1
    fi
    %if %{with ruby}
    if ! gmake check-swig-rb; then
    : Ruby swig test failure.
    exit 1
    fi
    %endif
    %if %{with pyswig}
    if ! gmake check-swig-py; then
    : Python swig test failure.
    exit 1
    fi
    %endif
    # check-swig-rb omitted: it runs svnserve
    %if %{with_java}
    gmake check-javahl
    %endif
}

cd 64bit
check_svn %{_libdir64}
cd ../32bit
check_svn %{_libdir}

%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f %{name}.files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/NOTICE
%doc 32bit/BUGS 32bit/COMMITTERS 32bit/INSTALL 32bit/README 32bit/CHANGES
%doc mod_authz_svn-INSTALL
%{_bindir}/*
%{_mandir}/man*/*
%{_datadir}/emacs/site-lisp/*.el
%{_datadir}/xemacs/site-packages/lisp/*.el
%{_datadir}/bash-completion/
%config(noreplace) %{_sysconfdir}/sysconfig/svnserve
%dir %{_sysconfdir}/subversion
%exclude %{_mandir}/man*/*::*
# %{_unitdir}/*.service
%attr(0700,root,root) %dir /run/svnserve
%{_prefix}/lib/tmpfiles.d/svnserve.conf

%files tools -f tools.files
%defattr(-,root,system,-)
%doc 32bit/tools/hook-scripts 32bit/tools/backup 32bit/tools/bdb 32bit/tools/examples 32bit/tools/xslt

%files libs
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/NOTICE
%{_libdir}/libsvn*.a
%{_libdir64}/libsvn*.a
%exclude %{_libdir}/libsvn_swig_perl*
%exclude %{_libdir64}/libsvn_swig_perl*
%if %{with ruby}
%exclude %{_libdir}/libsvn_swig_ruby*
%exclude %{_libdir64}/libsvn_swig_ruby*
%endif
%if %{with_java}
%{_libdir}/libsvnjavahl-*.so
%{_libdir64}/libsvnjavahl-*.so
%endif
# %exclude %{_libdir}/libsvn_auth_gnome*
# %exclude %{_libdir64}/libsvn_auth_gnome*

%if %{with python2} && %{with pyswig}
%files -n python-subversion
%defattr(-,root,system,-)
%{python2_sitearch}/svn
%{python2_sitearch}/libsvn
%endif

%if %{with python3} && %{with pyswig}
%files -n python3-subversion
%defattr(-,root,system,-)
%{python3_sitearch}/svn
%{python3_sitearch}/libsvn
%endif

%files devel
%defattr(-,root,system,-)
%{_includedir}/subversion-1
%{_datadir}/pkgconfig/*.pc

%if %{with httpd}
%files -n mod_dav_svn
%defattr(-,root,system,-)
%config(noreplace) %{_httpd_modconfdir}/*.conf
%{_libdir}/httpd/modules/mod_*.so
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%doc example.conf
%endif
%endif

%files perl
%defattr(-,root,system,-)
%{perl_vendorarch_32}/auto/SVN
%{perl_vendorarch_32}/SVN
%{perl_vendorarch_64}/auto/SVN
%{perl_vendorarch_64}/SVN
%{_libdir}/libsvn_swig_perl*.a
%{_libdir64}/libsvn_swig_perl*.a
%{_mandir}/man*/*::*


%if %{with ruby}
%files ruby
%defattr(-,root,system,-)
%{_libdir}/libsvn_swig_ruby*
%{ruby_vendorarchdir}/svn
%endif


%changelog
* Mon Mar 09 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.13.0-1
- New specfile from Fedora
- Port to AIX
- Bullfreeware OpenSSL removal
- Use new apr

* Mon Jan  6 2020 Joe Orton <jorton@redhat.com> - 1.12.2-3
- update for KDE 5 (Phil O, #1768693)

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1.12.2-2
- switch to Python 3 for F32+ (#1737928)

* Thu Jul 25 2019 Joe Orton <jorton@redhat.com> - 1.12.2-1
- update to 1.12.2

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.12.0-2
- Perl 5.30 rebuild

* Wed May  1 2019 Joe Orton <jorton@redhat.com> - 1.12.0-1
- update to 1.12.0 (#1702471)

* Wed Apr 17 2019 Joe Orton <jorton@redhat.com> - 1.11.1-5
- fix build with APR 1.7.0 (upstream r1857391)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.11.1-3
- F-30: rebuild against ruby26

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.11.1-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jan 11 2019 Joe Orton <jorton@redhat.com> - 1.11.1-1
- update to 1.11.1

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 1.11.0-1
- update to 1.11.0

* Thu Oct 11 2018 Joe Orton <jorton@redhat.com> - 1.10.3-1
- update to 1.10.3

* Fri Jul 20 2018 Joe Orton <jorton@redhat.com> - 1.10.2-1
- update to 1.10.2 (#1603197)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.10.0-9
- Perl 5.28 rebuild

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 1.10.0-8
- fix test suite invocation

* Thu Jun 28 2018 Joe Orton <jorton@redhat.com> - 1.10.0-7
- switch build conditional to disable only python bindings

* Thu May  3 2018 Joe Orton <jorton@redhat.com> - 1.10.0-6
- really disable Berkeley DB support if required by bcond
- add build conditional to disable swig binding subpackages

* Tue May  1 2018 Joe Orton <jorton@redhat.com> - 1.10.0-5
- remove build and -devel deps on libgnome-keyring-devel

* Tue May  1 2018 Joe Orton <jorton@redhat.com> - 1.10.0-4
- drop -devel dep on libserf-devel

* Tue Apr 24 2018 Joe Orton <jorton@redhat.com> - 1.10.0-3
- add bdb, tests as build conditional

* Tue Apr 17 2018 Joe Orton <jorton@redhat.com> - 1.10.0-2
- move new tools to -tools

* Mon Apr 16 2018 Joe Orton <jorton@redhat.com> - 1.10.0-1
- update to 1.10.0 (#1566493)

* Tue Mar 27 2018 Joe Orton <jorton@redhat.com> - 1.9.7-7
- add build conditionals for python2, python3 and kwallet

* Thu Feb  8 2018 Joe Orton <jorton@redhat.com> - 1.9.7-6
- force use of Python2 in test suite

* Thu Feb 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.7-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.9.7-4
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.7-3
- F-28: rebuild for ruby25

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.7-2
- Python 2 binary package renamed to python2-subversion
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Fri Aug 11 2017 Joe Orton <jorton@redhat.com> - 1.9.7-1
- update to 1.9.7 (CVE-2017-9800, #1480402)
- add Documentation= to svnserve.service

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Joe Orton <jorton@redhat.com> - 1.9.6-2
- move javahl .so to -libs (#1469158)

* Thu Jul  6 2017 Joe Orton <jorton@redhat.com> - 1.9.6-1
- update to 1.9.6 (#1467890)
- update to latest upstream psvn.el
- move libsvnjavahl to -libs, build -javahl noarch
- fix javahl Requires

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.5-4
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.9.5-2
- F-26: rebuild for ruby24

* Mon Jan  2 2017 Joe Orton <jorton@redhat.com> - 1.9.5-1
- update to 1.9.5 (#1400040, CVE-2016-8734)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed May 25 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.4-3
- Enable tests
- Revert one of Ruby 2.2 fixes

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.9.4-2
- Perl 5.24 rebuild

* Sun May  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.4-1
- Update to 1.9.4 (#1331222) CVE-2016-2167 CVE-2016-2168
- Move tools in docs to tools subpackage (rhbz 1171757 1199761)
- Disable make check to work around FTBFS

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Joe Orton <jorton@redhat.com> - 1.9.3-2
- rebuild for Ruby 2.3

* Tue Dec 15 2015 Joe Orton <jorton@redhat.com> - 1.9.3-1
- update to 1.9.3 (#1291683)
- use private /tmp in svnserve.service

* Thu Sep 24 2015 Joe Orton <jorton@redhat.com> - 1.9.2-1
- update to 1.9.2 (#1265447)

* Mon Sep 14 2015 Joe Orton <jorton@redhat.com> - 1.9.1-1
- update to 1.9.1 (#1259099)

* Mon Aug 24 2015 Joe Orton <jorton@redhat.com> - 1.9.0-1
- update to 1.9.0 (#1207835)
- package pkgconfig files

* Tue Jul 14 2015 Joe Orton <jorton@redhat.com> - 1.8.13-7
- move svnauthz to -tools; make svnauthz-validate a symlink
- move svnmucc man page to -tools
- restore dep on systemd (#1183873)

* Fri Jul 10 2015 Joe Orton <jorton@redhat.com> - 1.8.13-6
- rebuild with tests enabled

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.8.13-4
- Own bash-completion dirs not owned by anything in dep chain

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.13-3
- Perl 5.22 rebuild

* Tue Apr 21 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.13-2
- Disable tests to fix swig test issues

* Wed Apr 08 2015 <vondruch@redhat.com> - 1.8.13-1
- Fix Ruby's test suite.

* Tue Apr  7 2015 Joe Orton <jorton@redhat.com> - 1.8.13-1
- update to 1.8.13 (#1207835)
- attempt to patch around SWIG issues

* Tue Dec 16 2014 Joe Orton <jorton@redhat.com> - 1.8.11-1
- update to 1.8.11 (#1174521)
- require newer libserf (#1155670)

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-6
- prevents assert()ions in library code (#1058693)

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-5
- drop sysv conversion trigger (#1133786)

* Tue Sep 23 2014 Joe Orton <jorton@redhat.com> - 1.8.10-4
- move svn-bench, fsfs-* to -tools

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.8.10-3
- Perl 5.20 rebuild

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 1.8.10-2
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Joe Orton <jorton@redhat.com> - 1.8.10-1
- update to 1.8.10 (#1129100, #1128884, #1125800)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Joe Orton <jorton@redhat.com> - 1.8.9-1
- update to 1.8.9 (#1100779)

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Apr 22 2014 Joe Orton <jorton@redhat.com> - 1.8.8-2
- require minitest 4 to fix tests for Ruby bindings (#1089252)

* Fri Feb 28 2014 Joe Orton <jorton@redhat.com> - 1.8.8-1
- update to 1.8.8

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 1.8.5-4
- fix _httpd_mmn expansion in absence of httpd-devel

* Mon Jan  6 2014 Joe Orton <jorton@redhat.com> - 1.8.5-3
- fix permissions of /run/svnserve (#1048422)

* Tue Dec 10 2013 Joe Orton <jorton@redhat.com> - 1.8.5-2
- don't drop -Wall when building swig Perl bindings (#1037341)

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com> - 1.8.5-1
- update to 1.8.5 (#1034130)
- add fix for wc-queries-test breakage (h/t Andreas Stieger, r1542774)

* Mon Nov 18 2013 Joe Orton <jorton@redhat.com> - 1.8.4-2
- add fix for ppc breakage (Andreas Stieger, #985582)

* Tue Oct 29 2013 Joe Orton <jorton@redhat.com> - 1.8.4-1
- update to 1.8.4

* Tue Sep  3 2013 Joe Orton <jorton@redhat.com> - 1.8.3-1
- update to 1.8.3
- move bash completions out of /etc (#922993)

* Tue Aug 06 2013 Adam Williamson <awilliam@redhat.com> - 1.8.1-2
- rebuild for perl 5.18 (again; 1.8.1-1 beat out 1.8.0-2)

* Thu Jul 25 2013 Joe Orton <jorton@redhat.com> - 1.8.1-1
- update to 1.8.1

* Fri Jul 19 2013 Joe Orton <jorton@redhat.com> - 1.8.0-3
- temporarily ignore test suite failures on ppc* (#985582)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.8.0-2
- Perl 5.18 rebuild

* Tue Jun 18 2013 Joe Orton <jorton@redhat.com> - 1.8.0-1
- update to 1.8.0; switch to serf
- use full relro in mod_dav_svn build (#973694)

* Mon Jun  3 2013 Joe Orton <jorton@redhat.com> - 1.7.10-1
- update to 1.7.10 (#970014)
- fix aarch64 build issues (Dennis Gilmore, #926578)

* Thu May  9 2013 Joe Orton <jorton@redhat.com> - 1.7.9-3
- fix spurious failures in ruby test suite (upstream r1327373)

* Thu May  9 2013 Joe Orton <jorton@redhat.com> - 1.7.9-2
- try harder to avoid svnserve bind failures in ruby binding tests
- enable verbose output for ruby binding tests

* Tue Apr  9 2013 Joe Orton <jorton@redhat.com> - 1.7.9-1
- update to 1.7.9

* Wed Mar 27 2013 Vít Ondruch <vondruch@redhat.com> - 1.7.8-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Drop Ruby version checks from configuration script.
- Fix and enable Ruby test suite.

* Thu Mar 14 2013 Joe Orton <jorton@redhat.com> - 1.7.8-5
- drop specific dep on ruby(abi)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 1.7.8-3
- update to latest psvn.el

* Tue Jan  8 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 1.7.8-2
- Scriptlets replaced with new systemd macros (#850410)

* Fri Jan  4 2013 Joe Orton <jorton@redhat.com> - 1.7.8-1
- update to 1.7.8

* Thu Oct 11 2012 Joe Orton <jorton@redhat.com> - 1.7.7-1
- update to 1.7.7

* Fri Aug 17 2012 Joe Orton <jorton@redhat.com> - 1.7.6-1
- update to 1.7.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Joe Orton <jorton@redhat.com> - 1.7.5-5
- switch svnserve pidfile to use /run, use /usr/lib/tmpfiles.d (#840195)

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.7.5-4
- Perl 5.16 rebuild

* Mon Jun 18 2012 Dan Horák <dan[at]danny.cz - 1.7.5-3
- fix build with recent gcc 4.7 (svn rev 1345740)

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.7.5-2
- Perl 5.16 rebuild

* Tue May 22 2012 Joe Orton <jorton@redhat.com> - 1.7.5-1
- update to 1.7.5

* Tue Apr 24 2012 Joe Orton <jorton@redhat.com> - 1.7.4-6
- drop strict sqlite version requirement (#815396)

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 1.7.4-5
- switch to libdb-devel (#814090)

* Thu Apr 19 2012 Joe Orton <jorton@redhat.com> - 1.7.4-4
- adapt for conf.modules.d with httpd 2.4
- add possible workaround for kwallet crasher (#810861)

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 1.7.4-3
- re-enable test suite

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 1.7.4-2
- fix build with httpd 2.4

* Mon Mar 12 2012 Joe Orton <jorton@redhat.com> - 1.7.4-1
- update to 1.7.4
- fix build with httpd 2.4

* Thu Mar  1 2012 Joe Orton <jorton@redhat.com> - 1.7.3-7
- re-enable kwallet (#791031)

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-6
- update psvn

* Wed Feb 29 2012 Joe Orton <jorton@redhat.com> - 1.7.3-5
- add tools subpackage (#648015)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-4
- trim contents of doc dic (#746433)

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-3
- re-enable test suite

* Tue Feb 28 2012 Joe Orton <jorton@redhat.com> - 1.7.3-2
- add upstream test suite fixes for APR hash change (r1293602, r1293811)
- use ruby vendorlib directory (#798203)
- convert svnserve to systemd (#754074)

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.3-1
- update to 1.7.3
- ship, enable mod_dontdothat

* Mon Feb 13 2012 Joe Orton <jorton@redhat.com> - 1.7.2-2
- require ruby 1.9.1 abi

* Thu Feb  9 2012 Joe Orton <jorton@redhat.com> - 1.7.2-1
- update to 1.7.2
- add Vincent Batts' Ruby 1.9 fixes from dev@

* Sun Feb  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.1-3
- fix gnome-keyring build deps 

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Joe Orton <jorton@redhat.com> - 1.7.1-1
- update to 1.7.1
- (temporarily) disable failing kwallet support

* Sun Nov 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-3
- Build with libmagic support.

* Sat Oct 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-2
- Fix apr Conflicts syntax in -libs.
- Fix obsolete chown syntax in subversion.conf.
- Fix use of spaces vs tabs in specfile.

* Wed Oct 12 2011 Joe Orton <jorton@redhat.com> - 1.7.0-1
- update to 1.7.0
- drop svn2cl (no longer shipped in upstream tarball)
