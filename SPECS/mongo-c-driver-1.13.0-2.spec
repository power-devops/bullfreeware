# remirepo/fedora spec file for mongo-c-driver
#
# Copyright (c) 2015-2018 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     mongodb
%global gh_project   mongo-c-driver
%global libname      libmongoc
%global libver       1.0
#global prever       rc2
%global bsonver      1.13

%define gcc_compiler 1

%define _libdir64 %{_prefix}/lib64


%if 0%{?__isa_bits} == 64
%global with_tests   0
%else
# See https://jira.mongodb.org/browse/CDRIVER-1186
# 32-bit MongoDB support was officially deprecated
# in MongoDB 3.2, and support is being removed in 3.4.
%global with_tests   0
%endif

Name:      mongo-c-driver
Summary:   Client library written in C for MongoDB
Version:   1.13.0
Release:   2
Group:     MongoDB
# See THIRD_PARTY_NOTICES
License:   ASL 2.0 and ISC and MIT and zlib
URL:       https://github.com/%{gh_owner}/%{gh_project}

Source0:   https://github.com/%{gh_owner}/%{gh_project}/releases/download/%{version}%{?prever:-%{prever}}/%{gh_project}-%{version}%{?prever:-%{prever}}.tar.gz

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root


Patch1:	mongo-c-driver-1.11.0-resolv.patch
Patch2:	mongo-c-driver-1.12.0-pragmaO0-null_error_pointer.patch
Patch3:	mongo-c-driver-1.13.0-2-connect-refusal.patch

BuildRequires: cmake >= 3.1
BuildRequires: gcc
# pkg-config may pull compat-openssl10
BuildRequires: openssl-devel
#BuildRequires: pkgconfig(libsasl2)
#BuildRequires: pkgconfig(zlib)
#BuildRequires: pkgconfig(snappy)
#BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkg-config

%if %{with_tests}
#BuildRequires: mongodb-server
BuildRequires: openssl
%endif
#BuildRequires: perl-interpreter
# From man pages
BuildRequires: python
#BuildRequires: /usr/bin/sphinx-build

Requires:   %{name}-libs = %{version}-%{release}
# Sub package removed
Obsoletes:  %{name}-tools         < 1.3.0
Provides:   %{name}-tools         = %{version}
Provides:   %{name}-tools = %{version}


%description
%{name} is a client library written in C for MongoDB.


%package libs
Summary:    Shared libraries for %{name}
Group:     Libs
%description libs
This package contains the shared libraries for %{name}.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Devel
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig
Requires:   cmake-filesystem

%description devel
This package contains the header files and development libraries
for %{name}.

Documentation: http://mongoc.org/libmongoc/%{version}/


%package -n libbson
Summary:    Building, parsing, and iterating BSON documents
Group:      Bson

# Modified (with bson allocator and some warning fixes and huge indentation
# refactoring) jsonsl is bundled <https://github.com/mnunberg/jsonsl>.
# jsonsl upstream likes copylib approach and does not plan a release
# <https://github.com/mnunberg/jsonsl/issues/14>.
Provides:   bundled(jsonsl)

%description -n libbson
This is a library providing useful routines related to building, parsing,
and iterating BSON documents <http://bsonspec.org/>.


%package -n libbson-devel
Summary:    Development files for %{name}
Group:      Bson-devel
Requires:   libbson = %{version}-%{release}
Requires:   pkg-config
Requires:   cmake-filesystem

%description -n libbson-devel
This package contains libraries and header files needed for developing
applications that use %{name}.

Documentation: http://mongoc.org/libbson/%{version}/


%prep
#%setup -q -n %{gh_project}-%{version}%{?prever:-dev}
%setup -q 

%patch1 -p1 -b .resolv
%patch2 -p1 -b .pragma
%patch3 -p1 -b .connect-refusal



# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build

env

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

export CC=${CC__}
export CXX=${CXX__}

#export CC32=" ${CC__}  ${FLAG32}"
#export CXX32="${CXX__} ${FLAG32}"
#export CC64=" ${CC__}  ${FLAG64}"
#export CXX64="${CXX__} ${FLAG64}"

# -O2 adds error compared to -O0 with test in 64bit:
#	/initial_dns_seedlist_discovery/null_error_pointer
# Fixed by: mongo-c-driver-1.12.0-pragmaO0-null_error_pointer.patch
export GLOBAL_CC_OPTIONS="-O2"

export CFLAGS="${GLOBAL_CC_OPTIONS}"


#EXTRA_FLAGS="-Wno-unused-but-set-variable -fno-strict-aliasing -Wno-unused-parameter"
#EXTRA_FLAGS="${EXTRA_FLAGS} -Wno-error"
#export CFLAGS="-DOPENSSL_LOAD_CONF -DPIC -fPIC -DFORCE_INIT_OF_VARS $EXTRA_FLAGS"
#export CXXFLAGS="$CFLAGS"

# Force cmake to user AIX ar command
export AR=/usr/bin/ar

############################### 64-bit BEGIN ##############################
# first build the 64-bit version



cd 64bit
# Clean the CMake cache in case of "rpm -bc --short-circuit
rm -f CMakeCache.txt

export LIBPATH=/opt/freeware/lib64:/opt/freeware/lib:/usr/lib
# For cmake
export LIBPATH=/opt/freeware/lib/pthread/:$LIBPATH

export OBJECT_MODE=64

export LDFLAGS="${FLAG64} -L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib/pthread/:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lintl -lsnappy -Wl,-bbigtoc"
export CFLAGS64="${FLAG64} $CFLAGS -I/usr/include -I/opt/freeware/include -Wl,-bbigtoc"
export CXXFLAGS64="$CFLAGS64"

cmake . --trace --debug-trycompile --debug-output -G"Unix Makefiles" \
    -DENABLE_BSON:STRING=ON \
    -DENABLE_MONGOC:BOOL=ON \
    -DENABLE_SHM_COUNTERS:BOOL=ON \
    -DENABLE_SSL:STRING=OPENSSL \
    -DENABLE_SASL:STRING=OFF \
    -DENABLE_ICU:STRING=OFF \
    -DENABLE_AUTOMATIC_INIT_AND_CLEANUP:BOOL=OFF \
    -DENABLE_CRYPTO_SYSTEM_PROFILE:BOOL=ON \
    -DENABLE_MAN_PAGES:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    -DWITH_Sphinx=no \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
    -DCMAKE_C_COMPILER="${CC}"	\
    -DCMAKE_C_FLAGS="$CFLAGS64"		\
    -DCMAKE_CXX_COMPILER="${CXX}"	\
    -DCMAKE_CXX_FLAGS="$CXXFLAGS64"	\
    -DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS} " \
    -DCMAKE_MODULE_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_SHARED_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_LINK_LIBRARY_FLAG="$CFLAGS" \
    -DCMAKE_SHARED_LIBRARY_LINK="$LDFLAGS"   \
    -DCMAKE_AR=$AR        \
    -DENABLE_EXAMPLES:BOOL=OFF		\
    -DCMAKE_INSTALL_PREFIX=%{_prefix}	\
    -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%{_libdir64}	\
    -DBUILD_SHARED_LIBS=ON		\
    -DBUILD_STATIC_LIBS=OFF

# Try CMAKE_INSTALL_LIBDIR instead of CMAKE_LIBRARY_OUTPUT_DIRECTORY ?
# However, it does not appear in CMake documentation...

# Do not work...
#    -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%{_libdir64}	\
#    -DLIB_INSTALL_DIR=%{_libdir64}	\

# Do not work...
#    -DCMAKE_C_CREATE_SHARED_LIBRARY=ON	\
#    -DCMAKE_CXX_CREATE_SHARED_LIBRARY=ON	\


gmake --trace  %{?_smp_mflags}

#%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --ipv6 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
export MONGOC_TEST_OFFLINE=on
#export MONGOC_TEST_SKIP_SLOW=on

make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $ret
%endif


############################### 32-bit BEGIN ##############################
# now build the 32-bit version

cd ../32bit
# Clean the CMake cache in case of "rpm -bc --short-circuit
rm -f CMakeCache.txt

export LIBPATH=/opt/freeware/lib:/opt/freeware/lib:/usr/lib
# For cmake
export LIBPATH=/opt/freeware/lib/pthread/:$LIBPATH

export OBJECT_MODE=32

export LDFLAGS="${FLAG32} -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib/pthread/:/opt/freeware/lib:/usr/lib:/lib -lintl -lsnappy"
export CFLAGS32="${FLAG32} $CFLAGS -I/usr/include -I/opt/freeware/include"
export CXXFLAGS32="$CFLAGS32"

cmake . --trace --debug-trycompile --debug-output -G"Unix Makefiles" \
    -DENABLE_BSON:STRING=ON \
    -DENABLE_MONGOC:BOOL=ON \
    -DENABLE_SHM_COUNTERS:BOOL=ON \
    -DENABLE_SSL:STRING=OPENSSL \
    -DENABLE_SASL:STRING=OFF \
    -DENABLE_ICU:STRING=OFF \
    -DENABLE_AUTOMATIC_INIT_AND_CLEANUP:BOOL=OFF \
    -DENABLE_CRYPTO_SYSTEM_PROFILE:BOOL=ON \
    -DENABLE_MAN_PAGES:BOOL=ON \
    -DENABLE_TESTS:BOOL=ON \
    -DWITH_Sphinx=no \
    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
    -DCMAKE_C_COMPILER="${CC}"	\
    -DCMAKE_C_FLAGS="$CFLAGS32"		\
    -DCMAKE_CXX_COMPILER="${CXX}"	\
    -DCMAKE_CXX_FLAGS="$CXXFLAGS32"	\
    -DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS} " \
    -DCMAKE_MODULE_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_SHARED_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_LINK_LIBRARY_FLAG="$CFLAGS" \
    -DCMAKE_SHARED_LIBRARY_LINK="$LDFLAGS"   \
    -DCMAKE_AR=$AR        \
    -DENABLE_EXAMPLES:BOOL=OFF		\
    -DCMAKE_INSTALL_PREFIX=%{_prefix}	\
    -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%{_libdir}	\
    -DBUILD_SHARED_LIBS=ON		\
    -DBUILD_STATIC_LIBS=OFF

#    -DLIB_INSTALL_DIR=%{_libdir}	\

gmake --trace  %{?_smp_mflags}

#%check
%if %{with_tests}
: Run a server
mkdir dbtest
mongod \
  --journal \
  --ipv6 \
  --unixSocketPrefix /tmp \
  --logpath     $PWD/server.log \
  --pidfilepath $PWD/server.pid \
  --dbpath      $PWD/dbtest \
  --fork

: Run the test suite
ret=0
export MONGOC_TEST_OFFLINE=on
#export MONGOC_TEST_SKIP_SLOW=on

make check || ret=1

: Cleanup
[ -s server.pid ] && kill $(cat server.pid)

exit $ret
%endif


%install

# Use BullFreeware find command !
export PATH=/opt/freeware/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin

[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#export MAKE="gmake --trace"
export MAKE="gmake --trace -j14"
export RM="/usr/bin/rm -f"

echo ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

# Save the 64bit libraries
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cp    -p ${RPM_BUILD_ROOT}%{_libdir}/lib*a \
         ${RPM_BUILD_ROOT}%{_libdir}/lib*so*	${RPM_BUILD_ROOT}%{_libdir64}

# Save other 64bit stuff
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/cmake/libbson-%{libver}
cp    -p ${RPM_BUILD_ROOT}%{_libdir}/cmake/libbson-%{libver}/* ${RPM_BUILD_ROOT}%{_libdir64}/cmake/libbson-%{libver}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/cmake/%{libname}-%{libver}
cp    -p ${RPM_BUILD_ROOT}%{_libdir}/cmake/%{libname}-%{libver}/* ${RPM_BUILD_ROOT}%{_libdir64}/cmake/%{libname}-%{libver}
#/var/tmp/mongo-c-driver-1.11.0-1-root/opt/freeware/lib64/cmake/libbson-1.0
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig
cp    -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/* ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig

mv ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat_64

#$RM    %{buildroot}%{_libdir64}/*.a
#$RM -r %{buildroot}%{_libdir64}/cmake/*static*
#$RM -r %{buildroot}%{_libdir64}/pkgconfig/*static*

cd ../32bit
export OBJECT_MODE=32
$MAKE DESTDIR=${RPM_BUILD_ROOT} install

cp ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat ${RPM_BUILD_ROOT}%{_bindir}/mongoc-stat_32

#$RM    %{buildroot}%{_libdir}/*.a
#$RM -r %{buildroot}%{_libdir}/cmake/*static*
#$RM -r %{buildroot}%{_libdir}/pkgconfig/*static*

cd ..

(
    # create the 32bit shared libraries
    $AR -X32 -q %{buildroot}%{_libdir}/libbson-%{libver}.a	32bit/src/libbson/CMakeFiles/CMakeRelink.dir/libbson-%{libver}.so
    $AR -X32 -q %{buildroot}%{_libdir}/%{libname}-%{libver}.a	32bit/src/libmongoc/CMakeFiles/CMakeRelink.dir/%{libname}-%{libver}.so

    # add the 64-bit shared objects to the shared library containing already the # 32-bit shared objects
    $AR -X64 -q %{buildroot}%{_libdir}/libbson-%{libver}.a    	64bit/src/libbson/CMakeFiles/CMakeRelink.dir/libbson-%{libver}.so
    $AR -X64 -q %{buildroot}%{_libdir}/%{libname}-%{libver}.a 	64bit/src/libmongoc/CMakeFiles/CMakeRelink.dir/%{libname}-%{libver}.so

    # create the sylink to lib64
    rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/libbson-%{libver}.a
    rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}-%{libver}.a
    cd        ${RPM_BUILD_ROOT}%{_libdir64}
    ln -s                      %{_libdir}/libbson-%{libver}.a .
    ln -s                      %{_libdir}/%{libname}-%{libver}.a .
    cd -

    # strip -e the .so files
    strip -X32 -e 32bit/src/libbson/CMakeFiles/CMakeRelink.dir/libbson-%{libver}.so
    strip -X32 -e 32bit/src/libmongoc/CMakeFiles/CMakeRelink.dir/%{libname}-%{libver}.so
    strip -X64 -e 64bit/src/libbson/CMakeFiles/CMakeRelink.dir/libbson-%{libver}.so
    strip -X64 -e 64bit/src/libmongoc/CMakeFiles/CMakeRelink.dir/%{libname}-%{libver}.so
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



%files
%defattr(-,root,system)
%{_bindir}/mongoc-stat*

%files libs
%defattr(-,root,system)
%{!?_licensedir:%global license %%doc}
%license 32bit/COPYING
%license 32bit/THIRD_PARTY_NOTICES
%{_libdir}/%{libname}-%{libver}.a
%{_libdir64}/%{libname}-%{libver}.a
%{_libdir}/%{libname}-%{libver}.so*
%{_libdir64}/%{libname}-%{libver}.so*

%files devel
%doc 32bit/src/%{libname}/examples
%doc 32bit/NEWS
%{_includedir}/%{libname}-%{libver}
%{_libdir}/%{libname}-%{libver}.a
%{_libdir}/%{libname}-%{libver}.so*
%{_libdir}/pkgconfig/%{libname}-*.pc
%{_libdir}/cmake/%{libname}-%{libver}
%{_libdir64}/%{libname}-%{libver}.a
%{_libdir64}/%{libname}-%{libver}.so*
%{_libdir64}/pkgconfig/%{libname}-*.pc
%{_libdir64}/cmake/%{libname}-%{libver}
%{_prefix}/share/man/man3/mongoc*

%files -n libbson
%license 32bit/COPYING
%license 32bit/THIRD_PARTY_NOTICES
%{_libdir}/libbson*.a
%{_libdir}/libbson*.so*
%{_libdir64}/libbson*.a
%{_libdir64}/libbson*.so*

%files -n libbson-devel
%doc 32bit/src/libbson/examples
%doc 32bit/src/libbson/NEWS
%{_includedir}/libbson-%{libver}
%{_libdir}/libbson*.a
%{_libdir}/libbson*.so*
%{_libdir}/cmake/libbson-%{libver}
%{_libdir}/pkgconfig/libbson-*.pc
%{_libdir64}/libbson*.a
%{_libdir64}/libbson*.so*
%{_libdir64}/cmake/libbson-%{libver}
%{_libdir64}/pkgconfig/libbson-*.pc
%{_prefix}/share/man/man3/bson*



%changelog
* Tue Oct 04 2018 Pascal Emmendoerffer <pascal.emmendoerffer@atos.net> - 1.13.0-2 
- Fix connect_refusal test failed 

* Tue Sep 18 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.13.0-1 
- Add new version  1.12.0-1 

* Tue Aug 28 2018 Tony Reix <tony.reix@atos.net> - 1.12.0-12
- Manage -O2 and #pragma workaround

* Thu Aug 09 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.12.0-1 
- Add new version  1.12.0-1

* Fri Aug 03 2018 Sena Apeke <sena.apeke.external@atos.net> - 1.11.0-1 
- Add new version  1.11.0-1

* Wed Jun 20 2018 Remi Collet <remi@remirepo.net> - 1.10.3-1
- update to 1.10.3

* Fri Jun  8 2018 Remi Collet <remi@remirepo.net> - 1.10.2-1
- update to 1.10.2
- soname switch back to 0

* Thu May 31 2018 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Mon May 28 2018 Remi Collet <remi@remirepo.net> - 1.10.0-2
- add patch from https://github.com/mongodb/mongo-c-driver/pull/498
  for https://jira.mongodb.org/browse/CDRIVER-2667
  "mongoc-stat is not supported on your platform"
- open https://jira.mongodb.org/browse/CDRIVER-2668
  "mongoc-stat build but not installed"

* Mon May 28 2018 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0
- also build libbson and create new sub-packages
- switch to cmake
- soname bump to 1

* Wed May  2 2018 Remi Collet <remi@remirepo.net> - 1.9.5-1
- update to 1.9.5

* Tue Apr 10 2018 Remi Collet <remi@remirepo.net> - 1.9.4-1
- update to 1.9.4
- ensure all libraries referenced in pkgconfig file are required by devel
  reported as https://jira.mongodb.org/browse/CDRIVER-2603, #1560611

* Wed Mar 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 1.9.3-2
- Fix docs build with Sphinx >= 1.7

* Thu Mar  1 2018 Remi Collet <remi@remirepo.net> - 1.9.3-1
- update to 1.9.3

* Thu Feb 22 2018 Remi Collet <remi@remirepo.net> - 1.9.2-5
- add workaround for https://jira.mongodb.org/browse/CDRIVER-2516
- enable test suite

* Wed Feb 14 2018 Remi Collet <remi@remirepo.net> - 1.9.2-4
- drop ldconfig scriptlets
- disable again test suite

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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
