%define _libdir64 %{_prefix}/lib64

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A GNU set of database routines which use extensible hashing.
Name:    gdbm
Epoch:   1
Version: 1.18.1
Release: 2
Source0: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}-%{version}.tar.gz.sig
Source2: libgdbm.so.3-aix32
Source3: libgdbm.so.3-aix64
Source4: libgdbm.so.4-aix32
Source5: libgdbm.so.4-aix64
Source6: libgdbm.so.5-aix32
Source7: libgdbm.so.5-aix64
Source1000: %{name}-%{version}-%{release}.build.log

License: GPLv3
URL: http://www.gnu.org/software/gdbm/
Group: System Environment/Libraries

BuildRequires: gettext >= 0.19.8-1
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: readline-devel

Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: libgcc >= 6.3.0
Requires: gettext >= 0.19.8-1
# when -libs subpkg was introduced
Obsoletes: gdbm < 1:1.14.1-4

%description
Gdbm is a GNU database indexing library, including routines which use
extensible hashing.  Gdbm works in a similar way to standard UNIX dbm
routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.

If you're a C developer and your programs need access to simple
database routines, you should install gdbm.  You will also need to
install gdbm-devel.


%package libs
Summary: Libraries files for gdbm
# when -libs subpkg was introduced
Obsoletes: gdbm < 1:1.14.1-4

%description libs
Libraries for the Gdbm GNU database indexing library

%package devel
Summary: Development libraries and header files for the gdbm library
Requires: %{name} =  %{epoch}:%{version}-%{release}
Requires(post): info
Requires(preun): info

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build

env | sort

gcc --version

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
export CC="gcc -maix64 -D_LARGE_FILES"
export CFLAGS="-fPIC -pthread"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
./configure \
    --libdir=%{_libdir64} \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --includedir=%{_includedir} \
    --enable-shared --disable-static
    
# get rid of rpath (as per https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath)
# currently --disable-rpath doesn't work for gdbm_dump|load, gdbmtool and libgdbm_compat.so.4
# https://puszcza.gnu.org.ua/bugs/index.php?359
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
    
gmake %{?_smp_mflags} 

# now build the 32-bit version
cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export CFLAGS="-fPIC -pthread"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
./configure \
    --libdir=%{_libdir} \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --includedir=%{_includedir} \
    --enable-shared --disable-static

# get rid of rpath (as per https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath)
# currently --disable-rpath doesn't work for gdbm_dump|load, gdbmtool and libgdbm_compat.so.4
# https://puszcza.gnu.org.ua/bugs/index.php?359
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

gmake %{?_smp_mflags}


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
$AR -q src/.libs/libgdbm.a ../64bit/src/.libs/libgdbm.so.6
/usr/bin/strip -e -X64     ../64bit/src/.libs/libgdbm.so.6
/usr/bin/strip -e -X32              src/.libs/libgdbm.so.6
cp src/.libs/libgdbm.so.6 .
cp ../64bit/src/.libs/libgdbm.so.6 ../64bit

# Add the older 1.8.3 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE6} libgdbm.so.5
/usr/bin/strip -X32 -e libgdbm.so.5
/usr/bin/ar -X32 -q src/.libs/libgdbm.a libgdbm.so.5

cp %{SOURCE4} libgdbm.so.4
/usr/bin/strip -X32 -e libgdbm.so.4
/usr/bin/ar -X32 -q src/.libs/libgdbm.a libgdbm.so.4

cp %{SOURCE2} libgdbm.so.3
/usr/bin/strip -X32 -e libgdbm.so.3
/usr/bin/ar -X32 -q src/.libs/libgdbm.a libgdbm.so.3

# 64 bits
cp %{SOURCE7} ../64bit/libgdbm.so.5
/usr/bin/strip -X64 -e ../64bit/libgdbm.so.5
/usr/bin/ar -X64 -q src/.libs/libgdbm.a ../64bit/libgdbm.so.5

cp %{SOURCE5} ../64bit/libgdbm.so.4
/usr/bin/strip -X64 -e ../64bit/libgdbm.so.4
/usr/bin/ar -X64 -q src/.libs/libgdbm.a ../64bit/libgdbm.so.4

cp %{SOURCE3} ../64bit/libgdbm.so.3
/usr/bin/strip -X64 -e ../64bit/libgdbm.so.3
/usr/bin/ar -X64 -q src/.libs/libgdbm.a ../64bit/libgdbm.so.3

rm ../64bit/src/.libs/libgdbm.a
cp src/.libs/libgdbm.a ../64bit/src/.libs/libgdbm.a

# # Strip compat lib
# $AR -X64 -q compat/.libs/libgdbm_compat.a ../64bit/compat/.libs/libgdbm_compat.so.4
# /usr/bin/strip -e -X32          compat/.libs/libgdbm_compat.so.4
# /usr/bin/strip -e -X64 ../64bit/compat/.libs/libgdbm_compat.so.4
# cp          compat/.libs/libgdbm_compat.so.4 .
# cp ../64bit/compat/.libs/libgdbm_compat.so.4 ../64bit
# 
# rm ../64bit/compat/.libs/libgdbm_compat.a
# cp compat/.libs/libgdbm_compat.a ../64bit/compat/.libs/libgdbm_compat.a


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
export CC="gcc -maix64 -D_LARGE_FILES"
export CFLAGS="-fPIC -pthread"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
export LIBPATH=`pwd`/src/.libs/
#:`pwd`/compat/.libs/
(gmake -k check || true)
/usr/sbin/slibclean

cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export CFLAGS="-fPIC -pthread"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=32
export LIBPATH=`pwd`/src/.libs/
#:`pwd`/compat/.libs/
(gmake -k check || true)
/usr/sbin/slibclean


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
rm ${RPM_BUILD_ROOT}%{_libdir64}/libgdbm.a
#rm ${RPM_BUILD_ROOT}%{_libdir64}/libgdbm_compat.a
# Provides all .so (including very old .so.3) for compatibility
cp libgdbm.so* ${RPM_BUILD_ROOT}%{_libdir64}
#cp libgdbm_compat.so* ${RPM_BUILD_ROOT}%{_libdir64}
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  mv gdbm_dump gdbm_dump_64
  mv gdbm_load gdbm_load_64
  mv gdbmtool  gdbmtool_64
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
# Relink... Put the right manually
#rm ${RPM_BUILD_ROOT}%{_libdir}/libgdbm_compat.a
#cp compat/.libs/libgdbm_compat.a ${RPM_BUILD_ROOT}%{_libdir}
cp libgdbm* ${RPM_BUILD_ROOT}%{_libdir}
#cp libgdbm_compat* ${RPM_BUILD_ROOT}%{_libdir}

mkdir -p ${RPM_BUILD_ROOT}/usr/lib
mkdir -p ${RPM_BUILD_ROOT}/usr/include

# Provides some stuff on /usr for compatibility
ln -s %{_libdir}/libgdbm.a ${RPM_BUILD_ROOT}/usr/lib/libgdbm.a
ln -s %{_libdir}/libgdbm.la ${RPM_BUILD_ROOT}/usr/lib/libgdbm.la
ln -s %{_includedir}/gdbm.h ${RPM_BUILD_ROOT}/usr/include/gdbm.h
# 64 bit archive is a link to 32 bit archive
ln -s ../lib/libgdbm.a        ${RPM_BUILD_ROOT}%{_libdir64}/libgdbm.a
#ln -s ../lib/libgdbm_compat.a ${RPM_BUILD_ROOT}%{_libdir64}/libgdbm_compat.a

# Use 64 bit executable
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  mv gdbm_dump gdbm_dump_32
  mv gdbm_load gdbm_load_32
  mv gdbmtool  gdbmtool_32
  ln -s gdbm_dump_64 gdbm_dump
  ln -s gdbm_load_64 gdbm_load
  ln -s gdbmtool_64  gdbmtool
)

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/NEWS 32bit/README 32bit/AUTHORS 32bit/NOTE-WARNING
%{_bindir}/gdbm*
%{_mandir}/man1/gdbm*

%files libs
%{_libdir}/*.a
/usr/lib/libgdbm.a
%{_libdir64}/*.a
%doc 32bit/COPYING
%{_libdir}/libgdbm.so.6*
%{_libdir}/libgdbm.so.5*
%{_libdir}/libgdbm.so.4*
%{_libdir}/libgdbm.so.3*
%{_libdir64}/libgdbm.so.6*
%{_libdir64}/libgdbm.so.5*
%{_libdir64}/libgdbm.so.4*
%{_libdir64}/libgdbm.so.3*
#%{_libdir}/libgdbm_compat.so.4
#%{_libdir64}/libgdbm_compat.so.4

%files devel
%{_libdir}/*.la
/usr/lib/libgdbm.la
%{_libdir64}/*.la
#%{_libdir}/libgdbm_compat.la
#%{_libdir64}/libgdbm_compat.la
%{_includedir}/gdbm.h
/usr/include/gdbm.h
%{_infodir}/*.info*
%{_mandir}/man3/*


%changelog
* Tue Jul 30 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 1.18.1-2
- Split libraries out to separate libs subpackage
- Provides .so files.
- Provides executable files.
- Update specfile to RPMv4.

* Tue Apr 24 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.18.1-1
- Updated to 1.18.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-1
- Initial port on Aix6.1
