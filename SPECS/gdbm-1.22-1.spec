%define _libdir64 %{_prefix}/lib64

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A GNU set of database routines which use extensible hashing.
Name:    gdbm
Epoch:   1
Version: 1.22
Release: 1
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Source1000: %{name}-%{version}-%{release}.build.log

License: GPLv3
URL: http://www.gnu.org/software/gdbm/
Group: System Environment/Libraries

BuildRequires: gettext-devel >= 0.19.8-1
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: readline-devel
BuildRequires: sed

Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: libgcc >= 6.3.0
Requires: gettext >= 0.20.1-1
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
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

build_gdbm (){
    ./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--includedir=%{_includedir} \
	--libdir=$1 \
	--enable-shared --disable-static

    # get rid of rpath (as per https://fedoraproject.org/wiki/Packaging:Guidelines#Beware_of_Rpath)
    # currently --disable-rpath doesn't work for gdbm_dump|load, gdbmtool and libgdbm_compat.so.4
    # https://puszcza.gnu.org.ua/bugs/index.php?359
    sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
    sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

    gmake %{?_smp_mflags}
}

# first build the 64-bit version
cd 64bit
export CC="gcc -maix64"
export CFLAGS="-fPIC -pthread"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64

build_gdbm %{_libdir64}

# now build the 32-bit version
cd ../32bit
export CC="gcc -maix32"
export CFLAGS="-fPIC -pthread -D_LARGE_FILES"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_gdbm %{_libdir}



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)
cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 32bit binaries' name and make default link towards 64bit
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _32 -e _64)
    do
	mv ${f} ${f}_32
	ln -sf ${f}_64 ${f}
    done
)

(
    %define libsoversion 6
    %define libname libgdbm

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x %{libname}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q %{libname}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/%{libname}.so.%{libsoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{libname}.a
    ln -sf ../lib/%{libname}.a %{libname}.a
)

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

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

cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export CFLAGS="-fPIC -pthread"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=32
export LIBPATH=`pwd`/src/.libs/
#:`pwd`/compat/.libs/
(gmake -k check || true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/NEWS 32bit/README 32bit/AUTHORS 32bit/NOTE-WARNING
%{_bindir}/gdbm*
%{_mandir}/man1/gdbm*

%files libs
%defattr(-,root,system,-)
%{_libdir}/*.a
%{_libdir64}/*.a
%doc 32bit/COPYING

%files devel
%defattr(-,root,system,-)
%{_includedir}/gdbm.h
%{_infodir}/*.info*
%{_mandir}/man3/*


%changelog
* Fri Oct 22 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.22-1
- Update to 1.22

* Thu Oct 14 2021 Clément Chigot <clement.chigot@atos.net> - 1.21-2
- Remove old .so from library to avoid old requires.
- Improve specfile.

* Fri Sep 03 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.21-1
- Update to 1.21

* Fri Jun 18 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.20-1
- Update to 1.20

* Fri Feb 05 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.19-1
- Update to 1.19

* Mon Oct 26 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.18.1-5
- Rebuild 1.18.1

* Mon Oct 26 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 1.18.1-4
- Correct url
- Update specfile for automated build

* Fri Apr 03 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.18.1-3
- No more provide .so
- No more provide .la
- No more provide link to /usr

* Tue Jul 30 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 1.18.1-2
- Split libraries out to separate libs subpackage
- Provides .so files.
- Provides executable files.
- Update specfile to RPMv4.

* Tue Apr 24 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.18.1-1
- Updated to 1.18.1

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-1
- Initial port on Aix6.1
