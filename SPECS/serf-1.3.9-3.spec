
%bcond_without dotests

%define apr_version       1.7.0
%define apr_util_version  1.6.1
%define krb5_version      1.14
%define scons_version     3
%define zlib_version      1.2.11-1

%define soversion         0.3.0

%define scons_32 python2_32 /opt/freeware/bin/scons
%define scons_64 python2_64 /opt/freeware/bin/scons

Summary:      High-Performance Asynchronous HTTP Client Library
Name:         serf
Version:      1.3.9
Release:      3
License:      Apache License 2.0
Group:        Applications/Databases
URL:          http://serf.apache.org/
Source0:      https://archive.apache.org/dist/serf/%{name}-%{version}.tar.bz2
Source1:      %{name}-%{version}-1-aix.patch
Source1000:   %{name}-%{version}-%{release}.build.log

Patch0:       %{name}-%{version}-aix.patch

BuildRequires: scons >= %{scons_version}
BuildRequires: apr-devel >= %{apr_version}
BuildRequires: apr-util-devel >= %{apr_util_version}
#BuildRequires: krb5-devel >= %{krb5_version}
BuildRequires: zlib-devel >= %{zlib_version}

Requires: apr >= %{apr_version}
Requires: apr-util >= %{apr_util_version}
#Requires: krb5 >= %{krb5_version}
Requires: zlib >= %{zlib_version}

%define _libdir64 %{_prefix}/lib64

%description
The serf library is a C-based HTTP client library built upon the Apache 
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations
are kept to a minimum to provide high performance operation.


%package devel
Summary: Header files and libraries for developing apps which use serf.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config
Requires: apr-devel >= %{apr_version}
Requires: apr-util-devel >= %{apr_util_version}

%description devel
The serf-devel package contains the header files and libraries needed
to develop programs that use the serf HTTP client library.


%prep
%setup -q
%patch0
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)

%build
# ===================================================
# For xlc. Use brtl. Use scons (older use configure).
# OLD.
# ===================================================
# export CC="xlc_r"
# export PATH="%{_prefix}/bin:$PATH"
# 
# #function to build a shared library
# build_shared_library()
# {
#   f=$2
#   CreateExportList -X${1} ${f}.exp ${f}.a
#   ${CC} -q${1} -qmkshrobj ${f}.a -o ${f}.so.0.0.0 -Wl,-bE:${f}.exp -Wl,-bernotok $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12}
#   rm -f ${f}.exp ${f}.a
#   /usr/bin/ar -X${1} -rv ${f}.a ${f}.so.0.0.0
# }
# 
# cd 64bit
# # first build the 64-bit version
# export OBJECT_MODE=64
# scons \
#     AR="/usr/bin/ar -X64" \
#     CC="/usr/vac/bin/xlc_r -q64 -O2 -qstrict -I/opt/freeware/64/include" \
#     PREFIX=%{_prefix} \
#     LIBDIR=%{_libdir64} \
#     APR=%{_prefix}/bin/apr-1-config_64 \
#     APU=%{_prefix}/bin/apu-1-config_64 \
#     %{?_smp_mflags}
# 
# build_shared_library 64 libserf-1 -L/opt/freeware/lib64 -L/opt/freeware/lib -lssl -lcrypto -Wl,-brtl -lapr-1 -laprutil-1 -liconv -lz
# (scons -i check || true)
# 
# cd ../32bit
# # now build the 32-bit version
# export OBJECT_MODE=32
# scons \
#     AR="/usr/bin/ar -X32" \
#     CC="/usr/vac/bin/xlc_r -q32 -O2 -D_LARGE_FILES -qstrict -I/opt/freeware/include" \
#     PREFIX=%{_prefix} \
#     LIBDIR=%{_libdir} \
#     APR=%{_prefix}/bin/apr-1-config \
#     APU=%{_prefix}/bin/apu-1-config \
#     %{?_smp_mflags}
# 
# build_shared_library 32 libserf-1 -L/opt/freeware/lib -lssl -lcrypto -Wl,-brtl -lapr-1 -laprutil-1 -liconv -lz
# (scons -i check || true)

# ========================================================================
# For GCC. No brtl. Scons not well educated, so build is partially manual.
# ========================================================================

cd 64bit
export OBJECT_MODE=64
export CC="gcc"
export CPPFLAGS="-maix64"
export LDFLAGS="-L/usr/lib"
export AR="/usr/bin/ar -X64"
export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
%{scons_64} \
        CPPFLAGS="$CPPFLAGS" \
        LDFLAGS="$LDFLAGS" \
        AR="$AR" \
        APR=/opt/freeware/bin/apr-1-config \
        APU=/opt/freeware/bin/apu-1-config \
        OPENSSL=/usr \
        PREFIX=%{_prefix} \
        LIBDIR=%{_libdir64}

# Create manually shared library as an archive
rm -rf tmp
mkdir tmp
cd tmp
ar -X64 -xv ../libserf-1.a
gcc -maix64 -shared -o libserf-1.so.%{soversion} *.o -lapr-1 -laprutil-1 -lssl -lcrypto -liconv -lpthread -lz -Wl,-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib -L/opt/freeware/lib64
ar -X64 -qc libserf-1.a libserf-1.so.%{soversion}
cd ..
cp tmp/libserf-1.a .

cd ../32bit
export OBJECT_MODE=32
export CC="gcc"
export CPPFLAGS="-maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -L/usr/lib"
export AR="/usr/bin/ar -X32"
export LIBPATH="/opt/freeware/lib:/usr/lib"
%{scons_32} \
        CPPFLAGS="$CPPFLAGS" \
        LDFLAGS="$LDFLAGS" \
        AR="$AR" \
        APR=/opt/freeware/bin/apr-1-config \
        APU=/opt/freeware/bin/apu-1-config \
        OPENSSL=/usr \
        PREFIX=%{_prefix} \
        LIBDIR=%{_libdir}

# Create manually shared library as an archive
rm -rf tmp
mkdir tmp
cd tmp
ar -X32 -xv ../libserf-1.a
gcc -maix32 -shared -o libserf-1.so.%{soversion} *.o -lssl -lcrypto -lapr-1 -laprutil-1 -liconv -lpthread -lz -Wl,-blibpath:/opt/freeware/lib:/usr/lib
ar -X32 -qc libserf-1.a libserf-1.so.%{soversion}
cd ..
cp tmp/libserf-1.a .



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# ============
#     OLD
# ============
# 
# cd 64bit
# export OBJECT_MODE=64
# scons install --install-sandbox=${RPM_BUILD_ROOT}
# 
# cd ../32bit
# export OBJECT_MODE=32
# scons install --install-sandbox=${RPM_BUILD_ROOT}
# 
# (
#   cd ${RPM_BUILD_ROOT}%{_libdir64}
#   for f in *.a ; do
#     /usr/bin/ar -X64 -x ${f}
#   done
#   ln -s libserf-1.so.0.0.0 libserf-1.so.0
#   ln -s libserf-1.so.0.0.0 libserf-1.so
# 
#   cd ${RPM_BUILD_ROOT}%{_libdir}
#   for f in *.a ; do
#     /usr/bin/ar -X32 -x ${f}
#   done
#   ln -s libserf-1.so.0.0.0 libserf-1.so.0
#   ln -s libserf-1.so.0.0.0 libserf-1.so
# )
# 
# # add the missing 64-bit shared object to the AIX-style shared library
# /usr/bin/ar -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/libserf-1.a ${RPM_BUILD_ROOT}%{_libdir64}/libserf-1.so.0.0.0
# 
# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in include lib lib64
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )

cd 64bit
export OBJECT_MODE=64
%{scons_64} install --install-sandbox=${RPM_BUILD_ROOT}
cd ../32bit
export OBJECT_MODE=32
%{scons_32} install --install-sandbox=${RPM_BUILD_ROOT}

(
cd ${RPM_BUILD_ROOT}%{_libdir}
ar -X64 -xv ../lib64/libserf-1.a
ar -X64 -qc          libserf-1.a libserf-1.so.%{soversion}
cd ${RPM_BUILD_ROOT}%{_libdir64}
rm                        libserf-1.a
ln -sf ../lib/libserf-1.a libserf-1.a
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
export LIBPATH="`pwd`:`pwd`/tmp:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
# Compile stuff with bad command.
# First pass, manual creation, second pass.
(%{scons_64} -i check || true)
gcc -maix64 -o test/serf_get      -pthread test/serf_get.o      -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
gcc -maix64 -o test/serf_response -pthread test/serf_response.o -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
gcc -maix64 -o test/serf_request  -pthread test/serf_request.o  -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
gcc -maix64 -o test/serf_spider   -pthread test/serf_spider.o   -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
gcc -maix64 -o test/test_all      -pthread test/test_all.o test/CuTest.o test/test_util.o test/test_context.o test/test_buckets.o test/test_auth.o test/mock_buckets.o test/test_ssl.o test/server/test_server.o test/server/test_sslserver.o -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -laprutil-1 -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
gcc -maix64 -o test/serf_bwtp     -pthread test/serf_bwtp.o     -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv /opt/freeware/lib64/libapr-1.a  /opt/freeware/lib64/libaprutil-1.a
(%{scons_64} -i check || true)

cd ../32bit
export OBJECT_MODE=32
export LIBPATH="`pwd`:`pwd`/tmp:/opt/freeware/lib:/usr/lib"
(%{scons_32} -i check || true)
gcc -maix32 -o test/serf_get      -pthread test/serf_get.o      -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
gcc -maix32 -o test/serf_response -pthread test/serf_response.o -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
gcc -maix32 -o test/serf_request  -pthread test/serf_request.o  -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
gcc -maix32 -o test/serf_spider   -pthread test/serf_spider.o   -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
gcc -maix32 -o test/test_all      -pthread test/test_all.o test/CuTest.o test/test_util.o test/test_context.o test/test_buckets.o test/test_auth.o test/mock_buckets.o test/test_ssl.o test/server/test_server.o test/server/test_sslserver.o -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -laprutil-1 -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
gcc -maix32 -o test/serf_bwtp     -pthread test/serf_bwtp.o     -L. -L/opt/freeware/lib -L/usr/lib -lserf-1 -lssl -lcrypto -lz -lpthread -lldap -llber -ldb-4 -lgdbm -lexpat -liconv -lapr-1 -laprutil-1
(/opt/freeware/bin/python2_32 build/check.py || true)
#(%{scons_32} -i check || true)
cd ..
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE 32bit/README
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/design-guide.txt
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*


%changelog
* Wed Feb 05 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.3.9-3
- Remove .so
- Use gcc
- No more brtl
- Bullfreeware OpenSSL removal
- BullFreeware Compatibility Improvements

* Wed Jan 11 2017 Michael Perzl <michael@perzl.org> - 1.3.9-1
- update to version 1.3.9

* Wed Nov 16 2016 Michael Perzl <michael@perzl.org> - 1.2.1-3
- recompiled against latest versions

* Fri Mar 04 2016 Michael Perzl <michael@perzl.org> - 1.2.1-2
- recompiled against latest versions

* Wed Jun 19 2013 Michael Perzl <michael@perzl.org> - 1.2.1-1
- update to version 1.2.1

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 1.2.0-1
- update to version 1.2.0

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.1.1-1
- update to version 1.1.1

* Mon Jun 18 2012 Michael Perzl <michael@perzl.org> - 1.1.0-1
- update to version 1.1.0

* Mon Jun 18 2012 Michael Perzl <michael@perzl.org> - 1.0.3-1
- update to version 1.0.3

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 1.0.0-1
- update to version 1.0.0

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 0.7.2-1
- update to version 0.7.2

* Thu Dec 03 2010 Michael Perzl <michael@perzl.org> - 0.7.0-1
- update to version 0.7.0, added 64-bit library

* Tue Dec 18 2007 Michael Perzl <michael@perzl.org> - 0.1.2-1
- first version for AIX5L v5.1 and higher

