%global _hardened_build 1
# for better compatibility with SCL spec file
%global pkg_name mongodb
# mongod daemon
%global daemon mongod
# mongos daemon
%global daemonshard mongos

%global _initddir %{_sysconfdir}/rc.d/init.d
%global _root_initddir %{_sysconfdir}/rc.d/init.d

# Using Open Source verion of sed for commands using option -i
%define SED /opt/freeware/bin/sed

# Arches officially supported by MongoDB upstream
# %global upstream_arches x86_64 ppc64le aarch64 s390x
# Working storage engines - used for testing
# %ifnarch %{upstream_arches} ppc64
#   %global storageEngines mmapv1
# %else
#   %ifarch s390x ppc64
#     %global storageEngines wiredTiger
#   %else
#     %global storageEngines wiredTiger mmapv1
#   %endif
# %endif
# MozJS version

%global mozjsVersion 45

# Regression tests may take a long time (many cores recommended), skip them by
# passing --nocheck to rpmbuild or by setting runselftest to 0 if defining
# --nocheck is not possible (e.g. in koji build)
%{!?runselftest:%global runselftest 1}
# To disable unit testing (need to be built -> it slows build)
# ('runselftest' has to be enabled)
%{!?rununittests:%global rununittests 1}
# Do we want to package install_tests
# %bcond_without install_tests
# Do we want to package install_unit_tests
# ('rununittests' is needed)
%bcond_with install_unit_tests

%global MONGO_DISTNAME mongo-r%{version}

Name:       mongodb
Version:    4.0.3
Release:    1
Summary:    MongoDB High-performance, schema-free document-oriented database
Group:      Applications/Databases
License:    AGPLv3 and zlib and ASL 2.0
# util/md5 is under the zlib license
# manpages and bson are under ASL 2.0
# everything else is AGPLv3
URL:        https://www.mongodb.org

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0:    https://github.com/mongodb/mongo/archive/r%{version}.tar.gz
Source1:    %{pkg_name}-tmpfile
Source2:    %{pkg_name}.logrotate
Source3:    %{daemon}.conf
Source4:    %{daemon}.init
Source5:    %{daemon}.service
Source6:    %{daemon}.sysconf
Source7:    %{daemonshard}.conf
Source8:    %{daemonshard}.init
Source9:    %{daemonshard}.service
Source10:   %{daemonshard}.sysconf
Source11:   %{pkg_name}-testREADME.txt

Source20:    %{name}-%{version}-%{release}.build.log

# TabError: inconsistent use of tabs and spaces in indentation
#
Patch0:         %{pkg_name}-inconsistent-tabs.patch

# Convert build scripts and testsuite to support python3
# https://jira.mongodb.org/browse/SERVER-32295
# Patch1:         python3-buildscripts-tests.patch

# Fedora specific - adding support for rest of Fedora architectures
# Upstream doesn't support it and isn't considering merging
#
# https://jira.mongodb.org/browse/SERVER-27833
# Enable ppc64 big endian support
Patch20:         %{pkg_name}-4.0.3-ppc64.patch
# Add support also for 32bit platforms
# + set default storage engine for non 64-bit arches - RHBZ#1303846
Patch21:         %{pkg_name}-32bit-support.patch
# Generate mozjs code for ppc64, arm and i386 arches
Patch23:         %{pkg_name}-ppc64-arm-i386-mozjs-code.patch


#Patch100: mongodb-%{version}-aix.patch
#Patch100: mongodb-4.0.1-aix.patch
Patch101: mongodb-4.0.3-aix-part1-GCC.patch
Patch102: mongodb-4.0.1-aix-part2.patch
Patch103: mongodb-4.0.1-aix-part3.patch
Patch104: mongodb-4.0.1-aix-part4.patch
Patch105: mongodb-4.0.1-aix-part5-wiredtiger.patch
# For XL CLANG only,  a priori
Patch106: mongodb-4.0.1-aix-part6-clang.patch
Patch107: mongodb-4.0.1-aix-part7-boost.patch
Patch1080: mongodb-4.0.1-aix-part8-js-A.patch
Patch1081: mongodb-4.0.1-aix-part8-js-B.patch

Patch109: mongodb-4.0.1-aix-part9-gotools.patch

Patch110: mongodb-4.0.1-aix-part10-int64.patch
Patch111: mongodb-4.0.1-aix-part11-aix.patch
Patch112: mongodb-4.0.1-aix-part12-isself.patch
Patch113: mongodb-4.0.1-aix-part13-misc.patch
Patch114: mongodb-4.0.1-aix-part14-CLOCK_REALTIME.patch
Patch115: mongodb-4.0.1-aix-part15-ftdc_system_stats.patch
Patch116: mongodb-4.0.3-aix-part16-mozjs-45.patch
Patch117: mongodb-4.0.3-aix-part17-mmap_v1.patch
Patch118: mongodb-4.0.1-aix-part18-bswap.patch
Patch119: mongodb-4.0.3-aix-part19-db.patch
Patch120: mongodb-4.0.3-aix-part20-strcasestr.patch

# Avoid Power CRC32 HW checksum, for now, and use SW checksum
Patch121: mongodb-4.0.3-aix-part21-crc32.patch

# Patch for tests
Patch122: mongodb-4.0.3-aix-part22-tests.patch


BuildRequires:  gcc-c++ >= 5.3.0
# BuildRequires:  boost-devel >= 1.56
# Provides tcmalloc
# BuildRequires:  gperftools-devel
BuildRequires:  libpcap-devel
# BuildRequires:  libstemmer-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
# BuildRequires:  python3-scons
BuildRequires:  snappy-devel
# BuildRequires:  yaml-cpp-devel
BuildRequires:  zlib-devel
# BuildRequires:  valgrind-devel
BuildRequires:  curl
# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
# BuildRequires:  systemd
# %endif
# BuildRequires:  python3-devel
# BuildRequires:  python3-yaml
# BuildRequires:  python3-requests
# Required by test suite
%if %runselftest
# BuildRequires:  python3-pymongo
%endif
# BuildRequires:  python3-cheetah

# pkg_resources :
BuildRequires:  python-setuptools

# %if 0%{?_module_build}
# Provide modules only on upstream architectures
# ExclusiveArch:  %{upstream_arches}
# %else
# Mongodb must run on a 64-bit CPU (see bug #630898)
# ExcludeArch:    ppc %{sparc} s390
# %endif

%description
Mongo (from "humongous") is a high-performance, open source, schema-free
document-oriented database. MongoDB is written in C++ and offers the following
features:
    * Collection oriented storage: easy storage of object/JSON-style data
    * Dynamic queries
    * Full index support, including on inner objects and embedded arrays
    * Query profiling
    * Replication and fail-over support
    * Efficient storage of binary data including large objects (e.g. photos
    and videos)
    * Auto-sharding for cloud-level scalability (currently in early alpha)
    * Commercial Support Available

A key goal of MongoDB is to bridge the gap between key/value stores (which are
fast and highly scalable) and traditional RDBMS systems (which are deep in
functionality).


%package server
Summary:        MongoDB server, sharding server and support scripts
Group:          Applications/Databases

# Requires(pre):  shadow-utils
# Requires(post): chkconfig
# Requires(preun): chkconfig
# Requires(postun): initscripts

# Same upstream - wiredtiger is primarilly developed for MongoDB
Provides: bundled(wiredtiger) = %{version}
# MongoDB bundles development release of asio 1.11
# This is not in Fedora yet (only asio-1.10)
Provides: bundled(asio) = 1.11.0
# MongoDB stores version of icu into database (if using collators)
# - mongod with using different icu version can't cooperate
Provides: bundled(icu) = 57.1
# https://software.intel.com/en-us/articles/intel-decimal-floating-point-math-library
Provides: bundled(IntelRDFPMathLib) = 20U1
# https://github.com/derickr/timelib
Provides: bundled(timelib) = 2017.05beta10
# MongoDB provides mozjs customization to recover from OOM
Provides: bundled(mozjs45) = 45.8.0

%description server
This package provides the mongo server software, mongo sharding server
software, default configuration files, and init scripts.


%if %{with install_tests}
%package test
Summary:          MongoDB test suite
Group:            Applications/Databases
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         %{name}-server%{?_isa} = %{version}-%{release}
Requires:         python3-pymongo
Requires:         python3-yaml
Requires:         python3-requests

%description test
This package contains the regression test suite distributed with
the MongoDB sources.
%endif

%prep
%setup -q -n %{MONGO_DISTNAME}

%patch0 -p1
# %patch1 -p1
# Patch only Fedora specific architectures
%ifnarch %{upstream_arches}
%patch20 -p1
%patch21 -p1
%patch23 -p1

# Patchs AIX
#	%patch100 -p1 -b .aix
%patch101  -p1 -b .aix-1
%patch102  -p1 -b .aix-2
%patch103  -p1 -b .aix-3
%patch104  -p1 -b .aix-4
%patch105  -p1 -b .aix-5-wiredtiger
%patch106  -p1 -b .aix-6-clang
%patch107  -p1 -b .aix-7-boost
%patch1080 -p1 -b .aix-8-js-A
%patch1081 -p1 -b .aix-8-js-B
%patch109  -p1 -b .aix-9-gotools
%patch110  -p1 -b .aix-10-int64
%patch111  -p1 -b .aix-11-aix
%patch112  -p1 -b .aix-12-isself
%patch113  -p1 -b .aix-13-misc
%patch114  -p1 -b .aix-14-CLOCK_REALTIME
%patch115  -p1 -b .aix-15-ftdc_system_stats
%patch116  -p1 -b .aix-16-mozjs-45
%patch117  -p1 -b .aix-17-mmap_v1
%patch118  -p1 -b .aix-18-bswap
%patch119  -p1 -b .aix-19-db
%patch120  -p1 -b .aix-20-strcasestr

%patch121  -p1 -b .aix-21-crc32

%patch122  -p1 -b .aix-22-tests

# For mongodb <=3.6 mozjs sources are generated wrong
%{SED} -i -e "/extract\/js\/src\/jit\/ProcessExecutableMemory.cpp/d" src/third_party/mozjs-45/SConscript
%endif

# Workaround for https://jira.mongodb.org/browse/SERVER-37135 to make mongodb buildable with new openssl
%{SED} -i "s|\(#ifdef TLS1_3_VERSION\)|#undef TLS1_3_VERSION\n\1|" src/mongo/util/net/ssl_manager_openssl.cpp

# CRLF -> LF
%{SED} -i 's/\r//' README

#TODO - removed unused bundles
# Use system versions of header files (bundled does not differ)

# AIX does not support libstemmer package, as yet
# %{SED} -i -r "s|third_party/libstemmer_c/include/libstemmer.h|libstemmer.h|" src/mongo/db/fts/stemmer.h

# AIX does support yaml-cpp package, as yet
# %{SED} -i -r "s|third_party/yaml-cpp-0.5.1/include/yaml-cpp/yaml.h|yaml-cpp/yaml.h|" src/mongo/util/options_parser/options_parser.cpp

# Following refers to resmoke and tests - TBC
# by default use system mongod, mongos and mongo binaries in resmoke.py
# %{SED} -i -r "s|os.curdir(, \"mongo\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py
# %{SED} -i -r "s|os.curdir(, \"mongod\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py
# %{SED} -i -r "s|os.curdir(, \"mongos\")|\"%{_bindir}\"\1|"   buildscripts/resmokelib/config.py
# set default data prefix in resmoke.py
# %{SED} -i -r "s|/data/db|%{_datadir}/%{pkg_name}-test/var|"   buildscripts/resmokelib/config.py

# Stay with Python 2 for now
# %{SED} -i -r "s|env python|env python3|" buildscripts/resmoke.py


%build

ulimit -n unlimited
ulimit -f unlimited
ulimit -c 10
ulimit -m unlimited
ulimit -s unlimited
ulimit -d unlimited


export OBJECT_MODE=64
export AR="/usr/bin/ar -X64"
export ARFLAGS="-rc"
export RM="rm -f"

export LIBPATH=

# export LANG=C.UTF-8
# Prepare variables for building

# Original Fedora variables list

# cat > variables.list << EOF
# CCFLAGS="$(echo %{?optflags} | %{SED} -e "s/-O. //" -e "s/-g //")"
# LINKFLAGS="%{?__global_ldflags} -Wl,-z,noexecstack -Wl,--reduce-memory-overheads,--no-keep-memory"
# VERBOSE=1
# MONGO_VERSION="%{version}"
# VARIANT_DIR="fedora"
# 
# %ifarch %{ix86}
# # On i686 -ffloat-store is requred to round in GranularityRounderPreferredNumbers
# # properly, without this:
# # -> build/opt/mongo/db/pipeline/granularity_rounder_test,
# #    build/opt/mongo/db/pipeline/accumulator_test, build/opt/mongo/util/summation_test
# #    and build/opt/mongo/db/pipeline/document_source_test unittests fail
# CCFLAGS+=" -ffloat-store"
# %endif

%ifarch ppc
#	%ifarch ppc64	# rpm command on AIX is 32bit and thus defines only ppc and not ppc64
# Needed for altivec instructions in mongo/db/fts/unicode/byte_vector_altivec.h
# Need -qaltivec for CLANG
#CCFLAGS="$CCFLAGS -q64 -mcpu=power8 -qaltivec -I /opt/freeware/include/libmongoc-1.0 -I /opt/freeware/include/libbson-1.0"
# GCC
CCFLAGS="$CCFLAGS  -maix64 -mcpu=power8 -mtune=power8 -pthread -maltivec -D__powerpc64__ -D__BIG_ENDIAN__ -D_LARGE_FILES"
%endif


# %ifarch aarch64
# # Needed for CRC32 instructions in third_party/wiredtiger/src/checksum/arm64/crc32-arm64.c
# CCFLAGS+=" -march=armv8-a+crc"
# %endif

# EOF


# export LDFLAGS="-L%{_libdir}/pthread -lbsd -lstdc++ -latomic"
# export LIBPATH=/opt/freeware/lib/pthread:/opt/freeware/lib

cat > variables.list << EOF
CCFLAGS="$CCFLAGS -pthread -D__powerpc64__ -D__BIG_ENDIAN__"
# CLANG:
#LINKFLAGS="-q64 -lpthread -L/opt/freeware/lib/pthread -L/opt/freeware/lib -latomic "
LINKFLAGS="-maix64 -lpthread -L/opt/freeware/lib/pthread -L/opt/freeware/lib -latomic -lm -Wl,-bbigtoc"
MONGO_VERSION="%{version}"
EOF


cat variables.list

# Build options from Fedora which are not currently ported to AIX
# --use-system-boost \
# --use-system-stemmer \
# --use-system-valgrind \
# --use-system-yaml \
# Pose un probleme :
# --use-system-pcre \

# -j3

# Define build options

# Options to scons from AIX 3.2.0 spec file
# --prefix=%{_prefix} -j3 --js-engine=mozjs --ssl --opt=off core tools
#	%ifarch s390x ppc64
#	%ifarch %{upstream_arches} ppc64

# This produces binaries that lack performance gains provided by MongoDB internal tcmalloc
# --use-system-tcmalloc \

# Useful now ??
# --runtime-hardening=off \

# XL CLANG:
# CC=/opt/IBM/xlC/16.1.0/bin/xlclang \
# CXX=/opt/IBM/xlC/16.1.0/bin/xlclang++ \


# --ignore-errors \

cat > build-options << EOF
 %{?_smp_mflags} \
 --prefix=%{_prefix} \
 -j16 \
 --js-engine=mozjs \
 --use-system-snappy \
 --use-system-zlib \
%ifarch s390x ppc
 --mmapv1=off \
%else
 --mmapv1=on \
%endif
%ifarch %{upstream_arches} ppc
 --wiredtiger=on \
%else
 --wiredtiger=off \
%endif
%ifarch s390x
 --use-s390x-crc32=off \
%endif
 --ssl \
 --nostrip \
 --disable-warnings-as-errors \
 --variables-files=variables.list \
 CC=gcc \
 CXX=g++ \
 --runtime-hardening=off \
 VERBOSE=1 \
 AR=/usr/bin/ar \
 ARFLAGS=-rc \
 --opt=on \
 --dbg=off
EOF

# see output of "scons --help" for options
env
scons $(cat build-options) core tools

%if 0%{rununittests}
rm -rf build/
%{SED} -i "/^.*ggdb.*$/d" SConstruct
scons unittests $(cat build-options)
%endif

%install
/opt/freeware/bin/install -p -D -m 755 mongod %{buildroot}%{_bindir}/mongod
/opt/freeware/bin/install -p -D -m 755 mongos %{buildroot}%{_bindir}/mongos
/opt/freeware/bin/install -p -D -m 755 mongo %{buildroot}%{_bindir}/mongo
/opt/freeware/bin/install -p -D -m 755 mongobridge %{buildroot}%{_bindir}/mongobridge

/opt/freeware/bin/install -p -D -m 755 README %{buildroot}%{_docdir}/mongodb-4.0.3/README
/opt/freeware/bin/install -p -D -m 755 GNU-AGPL-3.0.txt %{buildroot}%{_docdir}/mongodb-4.0.3/GNU-AGPL-3.0.txt
/opt/freeware/bin/install -p -D -m 755 APACHE-2.0.txt %{buildroot}%{_docdir}/mongodb-4.0.3/APACHE-2.0.txt

mkdir -p %{buildroot}%{_sharedstatedir}/%{pkg_name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{pkg_name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{pkg_name}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
# /opt/freeware/bin/install -p -D -m 644 "%{SOURCE1}"  %{buildroot}%{_tmpfilesdir}/%{pkg_name}.conf
# install -p -D -m 644 "%{SOURCE5}"  %{buildroot}%{_unitdir}/%{daemon}.service
# install -p -D -m 644 "%{SOURCE9}"  %{buildroot}%{_unitdir}/%{daemonshard}.service
# %else
/opt/freeware/bin/install -p -D -m 755 "%{SOURCE4}"  %{buildroot}%{_root_initddir}/%{daemon}
/opt/freeware/bin/install -p -D -m 755 "%{SOURCE8}"  %{buildroot}%{_root_initddir}/%{daemonshard}
# %endif
/opt/freeware/bin/install -p -D -m 644 "%{SOURCE2}"  %{buildroot}%{_sysconfdir}/logrotate.d/%{pkg_name}
/opt/freeware/bin/install -p -D -m 644 "%{SOURCE3}"  %{buildroot}%{_sysconfdir}/%{daemon}.conf
/opt/freeware/bin/install -p -D -m 644 "%{SOURCE7}"  %{buildroot}%{_sysconfdir}/%{daemonshard}.conf
/opt/freeware/bin/install -p -D -m 644 "%{SOURCE6}"  %{buildroot}%{_sysconfdir}/sysconfig/%{daemon}
/opt/freeware/bin/install -p -D -m 644 "%{SOURCE10}" %{buildroot}%{_sysconfdir}/sysconfig/%{daemonshard}

# Enable WiredTiger for 64-bit architectures by default
# %ifarch %{upstream_arches} ppc64

%{SED} -i -r "s|(engine: )mmapv1|\1wiredTiger|" %{buildroot}%{_sysconfdir}/%{daemon}.conf

# %endif

#TODO - create man page for mongobridge
/opt/freeware/bin/install -d -m 755                     %{buildroot}%{_mandir}/man1
/opt/freeware/bin/install -p -m 644 debian/mongo.1      %{buildroot}%{_mandir}/man1/
/opt/freeware/bin/install -p -m 644 debian/mongod.1     %{buildroot}%{_mandir}/man1/
/opt/freeware/bin/install -p -m 644 debian/mongos.1     %{buildroot}%{_mandir}/man1/

%if %{with install_tests}
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/var
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/ciconfig
/opt/freeware/bin/install -p -D -m 755 buildscripts/resmoke.py   %{buildroot}%{_datadir}/%{pkg_name}-test/
/opt/freeware/bin/install -p -D -m 444 buildscripts/__init__.py  %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/
/opt/freeware/bin/install -p -D -m 444 buildscripts/ciconfig/__init__.py      %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/ciconfig
/opt/freeware/bin/install -p -D -m 444 buildscripts/ciconfig/tags.py          %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/ciconfig

cp -R     buildscripts/resmokeconfig     %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/
cp -R     buildscripts/resmokelib        %{buildroot}%{_datadir}/%{pkg_name}-test/buildscripts/
cp -R     jstests                        %{buildroot}%{_datadir}/%{pkg_name}-test/

# Remove executable flag from JS tests
for file in `find %{buildroot}%{_datadir}/%{pkg_name}-test/jstests -type f`; do
  chmod a-x $file
done

/opt/freeware/bin/install -p -D -m 444 "%{SOURCE11}"       %{buildroot}%{_datadir}/%{pkg_name}-test/
# Manually invoke the python byte compile macro
#%py_byte_compile %{__python3} %{buildroot}%{_datadir}/%{pkg_name}-test/

%if %{with install_unit_tests}
mkdir -p %{buildroot}%{_datadir}/%{pkg_name}-test/unittests
while read unittest
do
    /opt/freeware/bin/install -p -D $unittest %{buildroot}%{_datadir}/%{pkg_name}-test/unittests/
done < ./build/unittests.txt
%endif
%endif


# Tests are dumping core about 30 times and 2 tests block after sig abort
# They can be deblocked by runing dbx -a <processID> and q command
# %check
# export LANG=C.UTF-8
# %if %runselftest
# More info about testing:
# http://www.mongodb.org/about/contributors/tutorial/test-the-mongodb-server/
# cd %{_builddir}/%{MONGO_DISTNAME}
# mkdir -p ./var
# 
# Run old-style heavy unit tests (dbtest binary)
#mkdir ./var/dbtest
#./dbtest --dbpath `pwd`/var/dbtest
# 
# %if 0%{rununittests}
#TODO - failed on x86_64 and aarch64
# %{SED} -i "/session_catalog_migration_destination_test/d" build/unittests.txt
# %{SED} -i "/connection_string_test/d" build/unittests.txt
# %{SED} -i "/dns_query_test/d" build/unittests.txt
# %{SED} -i "/mongo_uri_test/d" build/unittests.txt
#TODO
# %ifarch %{ix86} %{arm}
# %{SED} -i "/service_entry_point_mock_test/d" build/unittests.txt
# %{SED} -i "/rs_rollback_test/d" build/unittests.txt
# Crashing on armv7hl due to optimizations
# %{SED} -i "/chunk_diff_test/d" build/unittests.txt
# %endif
# %ifarch %{arm}
# TODO
# ArraySerialization	Expected [ mongo::fromjson(outJson) == outObj ] but found [ { a: { b: [ "c", "d", [ "e" ] ] } } == { a: { b: [ "c", "d", [ "X" ] ] } }] @src/mongo/bson/mutable
# https://koji.fedoraproject.org/koji/getfile?taskID=22825582&volume=DEFAULT&name=build.log
# %{SED} -i "/mutable_bson_test/d" build/unittests.txt
# %endif

# Run new-style unit tests (*_test files)
# ./buildscripts/resmoke.py --dbpathPrefix `pwd`/var --continueOnFailure --mongo=%{buildroot}%{_bindir}/mongo --mongod=%{buildroot}%{_bindir}/%{daemon} --mongos=%{buildroot}%{_bindir}/%{daemonshard} --nopreallocj --suites unittests
# %endif

# %ifarch %{arm}
# rm -f jstests/core/hostinfo.js
# %endif
# %ifarch ppc64le
# rm -f jstests/core/shelltypes.js
# %endif

# for engine in %{storageEngines}; do
  # Run JavaScript integration tests
#   ./buildscripts/resmoke.py --dbpathPrefix `pwd`/var --continueOnFailure --mongo=%{buildroot}%{_bindir}/mongo --mongod=%{buildroot}%{_bindir}/%{daemon} --mongos=%{buildroot}%{_bindir}/%{daemonshard} --nopreallocj --suites core --storageEngine=$engine
# done
# 
# rm -Rf ./var
# %endif


%pre server
if ! /usr/bin/id -g mongod &>/dev/null; then
  /usr/bin/mkgroup mongod
fi
#
# getent group  %{pkg_name} >/dev/null || groupadd -f -g 184 -r %{pkg_name}
# if ! getent passwd %{pkg_name} >/dev/null ; then
#     if ! getent passwd 184 >/dev/null ; then
#       useradd -r -u 184 -g %{pkg_name} -d /var/lib/%{pkg_name} \
#       -s /sbin/nologin -c "MongoDB Database Server" %{pkg_name}
#     else
#       useradd -r -g %{pkg_name} -d /var/lib/%{pkg_name} \
#       -s /sbin/nologin -c "MongoDB Database Server" %{pkg_name}
#     fi
# fi
exit 0


%post server
if test "$1" = 1
then
  # Detecting the memory size to set the cache size is currently not implemented in mongodb for AIX,
  # so it is requiered to use the --wiredTigerCacheSizeGB argument when starting mongod.
  MEM_SIZE=`lsattr -El sys0 | grep realmem | awk '{ print $2 }'`
  CACHE_SIZE=`expr 6 \* $MEM_SIZE / 10485760 - 1`
  /bin/mkssys -s mongod -G mongod -p /opt/freeware/bin/mongod -u 0 -o /var/log/mongodb/MongoOutput.log -e /var/log/mongodb/MongoError.log -a "--wiredTigerCacheSizeGB=${CACHE_SIZE}"
  startsrc -s mongod
fi
# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
#   # https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
#   # daemon-reload
#   %systemd_postun
# %else
#   /sbin/chkconfig --add %{daemon}
#   /sbin/chkconfig --add %{daemonshard}
# %endif



%preun server
if test "$1" = 0
then
  rmssys -s mongod
fi
# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
#   # --no-reload disable; stop
#   %systemd_preun %{daemon}.service
#   %systemd_preun %{daemonshard}.service
# %else
#   /sbin/service %{daemon}       stop >/dev/null 2>&1
#   /sbin/service %{daemonshard}  stop >/dev/null 2>&1
#   /sbin/chkconfig --del %{daemon}
#   /sbin/chkconfig --del %{daemonshard}
# %endif
# fi


%postun server
if test "$1" -ge 1
then
  startsrc -s mongod
fi
# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
#   # daemon-reload
#   %systemd_postun
# %endif
# if [ "$1" -ge 1 ] ; then
# %if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
#   # try-restart
#   %systemd_postun_with_restart %{daemon}.service
#   %systemd_postun_with_restart %{daemonshard}.service
# %else
#   /sbin/service %{daemon}       condrestart >/dev/null 2>&1 || :
#   /sbin/service %{daemonshard}  condrestart >/dev/null 2>&1 || :
# %endif
# fi


%files
%{!?_licensedir:%global license %%doc}
#%license GNU-AGPL-3.0.txt APACHE-2.0.txt
%doc GNU-AGPL-3.0.txt APACHE-2.0.txt
%doc README
%{_bindir}/mongo
%{_bindir}/mongobridge

%{_mandir}/man1/mongo.1*


%files server
%{_bindir}/mongod
%{_bindir}/mongos
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongos.1*
%dir %attr(0755, %{pkg_name}, root) %{_sharedstatedir}/%{pkg_name}
%dir %attr(0750, %{pkg_name}, root) %{_localstatedir}/log/%{pkg_name}
%dir %attr(0755, %{pkg_name}, root) %{_localstatedir}/run/%{pkg_name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pkg_name}
%config(noreplace) %{_sysconfdir}/%{daemon}.conf
%config(noreplace) %{_sysconfdir}/%{daemonshard}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemon}
%config(noreplace) %{_sysconfdir}/sysconfig/%{daemonshard}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
#%{_tmpfilesdir}/%{pkg_name}.conf
%{_unitdir}/*.service
%else
%{_initddir}/%{daemon}
%{_initddir}/%{daemonshard}
%endif


%if %{with install_tests}
%files test
%defattr(-,%{pkg_name},root)
%dir %attr(0755, %{pkg_name}, root) %{_datadir}/%{pkg_name}-test
%dir %attr(0755, %{pkg_name}, root) %{_datadir}/%{pkg_name}-test/var
%{_datadir}/%{pkg_name}-test
%endif


%changelog
* Thu Apr 25 2019 Michael Wilson <michael.a.wilson@atos.net> - 4.0.3-1
- AIX port to 4.0.3 based on Fedora package and unpublished 3.2.0-1

* Mon Apr 04 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 3.2.0-1
- AIX port

* Thu Dec 19 2013 Ernie Hershey <ernie.hershey@mongodb.com>
- Packaging file cleanup

* Thu Jan 28 2010 Richard M Kreuter <richard@10gen.com>
- Minor fixes.

* Sat Oct 24 2009 Joe Miklojcik <jmiklojcik@shopwiki.com> -
- Wrote mongo.spec.

