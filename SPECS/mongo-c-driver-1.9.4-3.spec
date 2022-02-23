# remirepo/fedora spec file for mongo-c-driver
#
# Copyright (c) 2015-2018 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%{!?gcc_compiler: %define gcc_compiler 0}
%{!?dotests: %define dotests 1}

%define gcc_compiler 1

%define _libdir64 %{_prefix}/lib64

%global gh_owner     mongodb
%global gh_project   mongo-c-driver
%global libname      libmongoc
%global libver       1.0
#global prever       rc2
%global bsonver      1.9

%if 0%{?__isa_bits} == 64
%global with_tests   1
%global with_tests   0%{!?_without_tests:1}
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   1
%global with_tests   0%{?_with_tests:1}
%endif

# Since mongodb is not available on AIX: no tests
# They must be done by hand.
# However, the code must be present... so : 1
%global with_tests   1


Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.9.4
Release:   3
License:   ASL 2.0
Group:     System Environment/Libraries
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz

Source1000: %{name}-%{version}-%{release}.build.log

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


# RPM specific changes
# 1. Ignore check for libbson version = libmongoc version
# 2. Use bundled libbson documentation
#    https://jira.mongodb.org/browse/CDRIVER-2078
# 3. Don't install COPYING file which is not doc but license
Patch0:    %{name}-rpm.patch

# Fix some int64 print issue %lld
Patch1:    %{name}-%{version}.int64-lld.patch

%if %{gcc_compiler} == 0
# Work-around a XLC bug
# This bug has been found.
# Fix will appear in 2018/June XLC versions
Patch2:    %{name}-%{version}.XLC-bug.patch
%endif

# Change message to check
Patch3:     %{name}-1.9.4-topology-scanner.patch

#compute cpu count
Patch4: %{name}-%{version}._mongoc_get_cpu_count.patch

BuildRequires: libbson-devel = %{version}
BuildRequires: libbson = %{version}
Requires: libbson = %{version}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
#	BuildRequires: pkgconfig(openssl)
BuildRequires: openssl
#	BuildRequires: pkgconfig(libbson-1.0) > %{bsonver}
#       BuildRequires: pkgconfig(libsasl2)
#	BuildRequires: pkgconfig(zlib)
BuildRequires: zlib >= 1.2.11 zlib-devel
Requires: zlib >= 1.2.11
# pkgconfig file introduce in 1.1.4
#	BuildRequires: pkgconfig(snappy)
BuildRequires: snappy snappy-devel
Requires: snappy

%if %{with_tests}
#	BuildRequires: mongodb-server
BuildRequires: openssl
%endif

BuildRequires: perl

# From man pages
BuildRequires: python

# sphinx-build is executed from a build script. Depend on the executable name
# instead of a package name not to be disturbed by transition to a different
# Python version.
#   /opt/freeware/bin/sphinx-build is provided by python-sphinx on AIX
BuildRequires:  python-sphinx python-pygments python-jinja2 python-docutils
BuildRequires:  %{_bindir}/sphinx-build


Requires:   %{name}-libs%{?_isa} = %{version}-%{release}
# Sub package removed
Obsoletes:  %{name}-tools         < 1.3.0
Provides:   %{name}-tools         = %{version}
Provides:   %{name}-tools%{?_isa} = %{version}


%description
%{name} is a client library written in C for MongoDB.

The database is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package libs
Summary:    Shared libraries for %{name}
Group:      Development/Libraries

%description libs
This package contains the shared libraries for %{name}.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains the header files and development libraries
for %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".



Documentation: http://api.mongodb.org/c/%{version}/


##################################################################
#                                                                #
#                           %prep                                #
#                                                                #
##################################################################

%prep
# Use BullFreeware patch command
export PATH=/opt/freeware/bin/:$PATH

%setup -q -n %{gh_project}-%{version}%{?prever:-dev}
%patch0 -p1 -b .rpm
%patch1 -p1 -b .int64-lld
%if %{gcc_compiler} == 0
%patch2 -p1 -b .XLC-bug
%endif
%patch3 -p1 -b .topology-scanner
%patch4 -p1 -b ._mongoc_get_cpu_count

: Generate build scripts from sources
autoreconf --force --install --verbose -I build/autotools

: delete bundled libbson sources
rm -r src/libbson

: delete bundled zlib sources
# Yes but No... because config.status makes use of:
#	 src/zlib-1.2.11/zconf.h.in
#rm -r src/zlib*

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


############################################################################
#                                                                          #
#                                %build                                    #
#                                                                          #
############################################################################

%build

env

export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

export RM="/usr/bin/rm -f"
export LIBS=-lpthread


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

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

export GLOBAL_CC_OPTIONS="-O2"

#Tracing
export MONGOC_TRACE=1


############################### 64-bit BEGIN ##############################
# first build the 64-bit version

cd 64bit
export LIBPATH=/opt/freeware/lib64:/opt/freeware/lib

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lintl"

export CFLAGS="-I/usr/include -I/opt/freeware/include"

./configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir64} \
  --disable-debug \
  --disable-tracing \
  --disable-optimizations \
  --disable-debug-symbols \
  --enable-shm-counters \
  --disable-automatic-init-and-cleanup \
  --enable-crypto-system-profile \
%if %{with_tests}
  --enable-tests \
%else
  --disable-tests \
%endif
  --enable-ssl \
  --with-libbson=system \
  --with-snappy=system \
  --disable-html-docs \
  --disable-man-pages \
  --disable-examples \
  --with-zlib=system

gmake -j12 %{?_smp_mflags} all V=1

# Explicit man target is needed for generating manual pages
#gmake %{?_smp_mflags} doc/man V=1


#	Test are done with a remote MongoDB/ NO local tests !
#%if %{with_tests}
#: mongod must run on another machine
# It requires to have the mongod process built and installed...
#: Run a server
# mkdir dbtest
# mongod \
#   --journal \
#   --ipv6 \
#   --unixSocketPrefix /tmp \
#   --logpath     $PWD/server.log \
#   --pidfilepath $PWD/server.pid \
#   --dbpath      $PWD/dbtest \
#   --fork
#
#: Run the test suite
#ret=0
#export MONGOC_TEST_OFFLINE=on
#export MONGOC_TEST_SKIP_SLOW=on
#make check || ret=1
#: Cleanup
#[ -s server.pid ] && kill $(cat server.pid)
#exit $ret
#%endif


# LOCAL MANUAL TESTS :
#MACHINE_WITH_MONGODB_RUNNING=10.197.64.27   # dorado-vm1
# mongod -vvv | tee tracefile
#REMOTE Tests
# export URI=mongodb://$MACHINE_WITH_MONGODB_RUNNING:27017/
# export MONGOC_TEST_URI=mongodb://$MACHINE_WITH_MONGODB_RUNNING:27017/
# ulimit -d unlimited
# ./test-libmongoc

############################### 64-bit END ##############################


############################### 32-bit BEGIN ##############################

cd ../32bit
export LIBPATH=/opt/freeware/lib

# now build the 32-bit version
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

%if %{gcc_compiler} == 1
        export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib                          -lintl"
%else
        export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lintl"
%endif

export CFLAGS="-I/usr/include -I/opt/freeware/include"

./configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --disable-debug \
  --disable-tracing \
  --disable-optimizations \
  --disable-debug-symbols \
  --enable-shm-counters \
  --disable-automatic-init-and-cleanup \
  --enable-crypto-system-profile \
%if %{with_tests}
  --enable-tests \
%else
  --disable-tests \
%endif
  --enable-ssl \
  --with-libbson=system \
  --with-snappy=system \
  --disable-html-docs \
  --disable-man-pages \
  --disable-examples \
  --with-zlib=system

#        --enable-sasl 			?????

gmake -j12 %{?_smp_mflags} all V=1

#%if %{with_tests}
#: mongod must run on another machine
# It requires to have the mongod process built and installed...
#: Run a server
# mkdir dbtest
# mongod \
#   --journal \
#   --ipv6 \
#   --unixSocketPrefix /tmp \
#   --logpath     $PWD/server.log \
#   --pidfilepath $PWD/server.pid \
#   --dbpath      $PWD/dbtest \
#   --fork

#: Run the test suite
#ret=0
#export MONGOC_TEST_OFFLINE=on
#export MONGOC_TEST_SKIP_SLOW=on
#make check || ret=1
#: Cleanup
#[ -s server.pid ] && kill $(cat server.pid)
#exit $ret
#%endif

# LOCAL MANUAL TESTS :
#MACHINE_WITH_MONGODB_RUNNING=10.197.64.27   # dorado-vm1
# mongod -vvv | tee tracefile
#REMOTE Tests
# export URI=mongodb://$MACHINE_WITH_MONGODB_RUNNING:27017/
# export MONGOC_TEST_URI=mongodb://$MACHINE_WITH_MONGODB_RUNNING:27017/
# /test-libmongoc


############################################################################
#                                                                          #
#                                %install                                  #
#                                                                          #
############################################################################

%install

export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

export AR=/usr/bin/ar
export RM="/usr/bin/rm -f"

echo ${RPM_BUILD_ROOT}

[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export MAKE="gmake"

cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lintl"

$MAKE DESTDIR=${RPM_BUILD_ROOT} install

mv ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat_64

$RM ${RPM_BUILD_ROOT}%{_libdir}/*la

#: install examples
#for i in examples/*.c examples/*/*.c; do
#  install -Dpm 644 $i ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}/$i
#done

: Rename documentation to match subpackage name
#mv ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name} \
#   ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}-devel


cd ../32bit
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lintl"

$MAKE DESTDIR=${RPM_BUILD_ROOT} install

cp ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat_32

$RM ${RPM_BUILD_ROOT}%{_libdir}/*la

#: install examples
#for i in examples/*.c examples/*/*.c; do
#  install -Dpm 644 $i ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}/$i
#done

#: Rename documentation to match subpackage name
#mv ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name} \
#   ${RPM_BUILD_ROOT}%{_datadir}/doc/%{name}-devel

cd ..
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libmongoc-1.0.a
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libmongoc-1.0.a libmongoc-1.0.so.0
(
  rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/libmongoc-1.0.a
  cd        ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s                      %{_libdir}/libmongoc-1.0.a .
)


# create link from /usr/bin to /opt/freeware/bin
(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


# Linux !
#%post   libs -p /sbin/ldconfig
#%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,system)
%{_bindir}/mongoc-stat*

%files libs
%defattr(-,root,system)
%{!?_licensedir:%global license %%doc}
#%license COPYING
#%license THIRD_PARTY_NOTICES
%dir %{_libdir}
%dir %{_libdir64}
%{_libdir}/%{libname}-%{libver}.a
%{_libdir64}/%{libname}-%{libver}.a

%files devel
%defattr(-,root,system)
#%{_docdir}/%{name}-devel
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.a
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_libdir}/cmake/%{libname}-%{libver}
#%{_mandir}/man3/mongoc*


%changelog
* Mon Apr 23 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.9.4-3
- Manage _mongoc_get_cpu_count() for AIX

* Tue Apr 17 2018 Tony Reix <tony.reix@atos.net> - 1.9.4-2
- Manage error message of topology-scanner test
- Provide mongoc-stat 32 & 64bit.

* Thu Apr 12 2018 Tony Reix <tony.reix@atos.net> - 1.9.4-1
- Update to 1.9.4

* Wed Apr 11 2018 Tony Reix <tony.reix@atos.net> - 1.9.3-2
- Use installed zlib version >= 1.2.11

* Wed Apr 11 2018 Tony Reix <tony.reix@atos.net> - 1.9.3-1
- First port on AIX

* Wed Jan 17 2018 Tony Reix <tony.reix@atos.net> - 1.9.2-1
- First port on AIX
- Fix int64 %d - %lld issue for tests

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 1.9.2-2
- enable test suite on 64-bit

* Fri Jan 12 2018 Remi Collet <remi@remirepo.net> - 1.9.2-1
- update to 1.9.2 (no change)

* Wed Jan 10 2018 Remi Collet <remi@remirepo.net> - 1.9.1-1
- update to 1.9.1

* Fri Dec 22 2017 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0
- raise dependency on libbson 1.9

* Fri Nov 17 2017 Remi Collet <remi@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Thu Oct 12 2017 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Fri Sep 15 2017 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- update to 1.8.0

* Thu Aug 10 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0
- disable test suite in rawhide (mongodb-server is broken)

* Tue Aug  8 2017 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.1.rc2
- update to 1.7.0-rc2
- add --with-snappy and --with-zlib build options

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 24 2017 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- update to 1.6.2

* Tue Mar 28 2017 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- update to 1.6.2

* Wed Mar  8 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-2
- rebuild with new upstream tarball
- add examples in devel documentation
- use patch instead of sed hacks for rpm specific changes

* Tue Mar  7 2017 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- update to 1.6.1
- open https://jira.mongodb.org/browse/CDRIVER-2078
  can't build man pages

* Thu Feb  9 2017 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- add fix for https://jira.mongodb.org/browse/CDRIVER-2042
  from https://github.com/mongodb/mongo-c-driver/pull/421

* Thu Jan 12 2017 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- update to 1.5.3

* Wed Jan 11 2017 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- update to 1.5.2
- run server on both IPv4 and IPv6
- open https://jira.mongodb.org/browse/CDRIVER-1988 - Failed test
- revert IPv6 commit

* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- update to 1.5.1

* Mon Nov 28 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Fri Nov 18 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.5.rc6
- update to 1.5.0-rc6

* Fri Nov  4 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.4.rc4
- update to 1.5.0-rc4

* Thu Oct 20 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.3.rc3
- update to 1.5.0-rc3
- drop patches merged upstream

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.2.rc2
- open https://jira.mongodb.org/browse/CDRIVER-1703 missing files
- open https://jira.mongodb.org/browse/CDRIVER-1702 broken test
- enable test suite

* Fri Oct 14 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-0.1.rc2
- update to 1.5.0-rc2
- drop crypto patch merged upstream
- drop the private library
- disable test suite

* Mon Aug 29 2016 Petr Pisar <ppisar@redhat.com> - 1.3.5-6
- Rebuild against libbson-1.4.0 (bug #1361166)

* Tue Jul 26 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-5
- add BR on perl, FTBFS from Koschei

* Mon Jun 13 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-4
- add workaround to abicheck failure
  see https://bugzilla.redhat.com/1345868

* Mon May 16 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-2
- add patch to enforce system crypto policies

* Thu Mar 31 2016 Remi Collet <remi@fedoraproject.org> - 1.3.5-1
- update to 1.3.5
- use --disable-automatic-init-and-cleanup build option
- ignore check for libbson version = libmongoc version

* Sat Mar 19 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- build with MONGOC_NO_AUTOMATIC_GLOBALS

* Tue Mar 15 2016 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- update to 1.3.4
- drop patch merged upstream

* Mon Feb 29 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- cleanup for review
- move libraries in "libs" sub-package
- add patch to skip online tests
  open https://github.com/mongodb/mongo-c-driver/pull/314
- temporarily disable test suite on arm  (#1303864)
- temporarily disable test suite on i686/F24+ (#1313018)

* Sun Feb  7 2016 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3

* Tue Feb  2 2016 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Thu Jan 21 2016 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Wed Dec 16 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- move tools in devel package

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Tue Dec  8 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- open https://jira.mongodb.org/browse/CDRIVER-1040 - ABI breaks

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.6.rc0
- Update to 1.2.0-rc0

* Fri Sep 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.5.20150903git3eaf73e
- add patch to export library verson in the API
  open https://github.com/mongodb/mongo-c-driver/pull/265

* Fri Sep  4 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.4.20150903git3eaf73e
- update to version 1.2.0beta1 from git snapshot
- https://jira.mongodb.org/browse/CDRIVER-828 missing tests/json

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.3.beta
- more upstream patch (for EL-6)

* Mon Aug 31 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-0.2.beta
- Upstream version 1.2.0beta

* Wed May 20 2015 Remi Collet <remi@fedoraproject.org> - 1.1.6-1
- Upstream version 1.1.6

* Mon May 18 2015 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Upstream version 1.1.5

* Sat Apr 25 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-3
- test build for upstream patch

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-2
- cleanup build dependencies and options

* Wed Apr 22 2015 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Initial package
- open https://jira.mongodb.org/browse/CDRIVER-624 - gcc 5
