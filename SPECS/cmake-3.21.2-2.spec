# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%global major_version 3
%global minor_version 21
%define bugfix_version 2

Name:       cmake
Version:    %{major_version}.%{minor_version}.%{bugfix_version}
Release: 2
Summary:    Cross-platform, open-source build system
Group:      Development/Tools
License:    BSD
URL:        http://www.cmake.org
Source0:    https://github.com/Kitware/CMake/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

Patch1:         cmake-3.21.1-2_NewAIXbehavior.patch
Patch2:         cmake-3.20.4_NewAIXbehavior_tests.patch
Patch3:         cmake-3.16.0_NewAIXbehavior_readme.patch

BuildRequires:  gcc make
Requires:       %{name}-data = %{version}-%{release}
Requires:       ncurses >= 6

# Unsued package on AIX.
Obsoletes:      %{name}-filesystem
Obsoletes:      %{name}-rpm-macros


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.

Behavior of CMake on AIX has been changed in 3.14 to obey to AIX rules.
See /opt/freeware/share/cmake-%{major_version}.%{minor_version}/Modules/readme_aix.txt for more informations.

%package        data
Summary:        Common data-files for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    data
This package contains common data-files for %{name}.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
env | /usr/bin/sort

# Quiet ar needed for test
export AR="/usr/bin/ar -c"


# Verify disk space for tests.
SO=`/usr/bin/df -k /var/tmp | awk '{if(NR==2)print $3}'`
echo "Disk space available for building cmake must be >= 2GB"
if [ "$SO" -lt 2000000 ]
then
    echo "Not enough disk space on /var/tmp !"
    exit 1
fi

SO=`/usr/bin/df -k /opt/freeware | awk '{if(NR==2)print $3}'`
echo "Disk space available for building cmake must be >= 6.5GB"
if [ "$SO" -lt 6500000 ]
then
    echo "Not enough disk space on /opt !"
    exit 1
fi


# Utilities/cmlibuv/src/unix/fs.c :
#    #elif defined(_AIX71)
#          return futimens(req->file, ts);
# -mcmodel=large or -Wl,-bbigtoc is required to link ctest.

# 32 bits only: -Wl,-bmaxdata:0x80000000"
LDFLAGS="-pthread"

CFLAGS="-D_LARGE_FILES -DSYSV -D_AIX -D_ALL_SOURCE -DFUNCPROTO=15 -mcmodel=large -pthread -maix64"
export LDFLAGS="$LDFLAGS"
export CFLAGS="$CFLAGS -D_AIX71 -D_AIX72"
export OBJECT_MODE=64

echo "C compiler version:"
export CC=gcc
export CXX=g++
$CC  --version
$CXX --version

export CXXFLAGS="$CFLAGS"

%define _smp_parallel %(echo %{?_smp_mflags} | sed "s|-j|--parallel=|")
./bootstrap \
    --verbose \
    %{_smp_parallel} \
    --prefix=%{_prefix}

# This phase requires nearly 6GB on /opt
gmake --trace %{?_smp_mflags} VERBOSE=1


%check
%if %{with dotests}
export LIBPATH="/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export PATH="/opt/freeware/bin:/usr/bin:/usr/sbin"

# No static in AIX. No objdump in AIX.
# RuntimePath must fail dut to different behavior in AIX and Linux.
  TEST_ARGS="-E \"(LinkStatic|RunCMake.CPack_RPM.DEBUGINFO|RunCMake.CPack_RPM.DEPENDENCIES|RunCMake.CPack_RPM.SINGLE_DEBUGINFO|RunCMake.CPack_RPM.EXTRA_SLASH_IN_PATH|RuntimePath)\""

  TEST_ARGS="$TEST_ARGS %{?_smp_mflags}"
  export TAR=/opt/freeware/bin/tar
  export OBJECT_MODE=
  export LDFLAGS=""
  export CFLAGS=""
  export CXXFLAGS=""

# "-mcmodel=large" can be added for XLC in CFLAGS only in AIX 7.1+.
# OK with GCC 8+ on AIX 6.1+.
  
echo "================================================================="
echo "== Tests with GCC - 32bit ======================================="
echo "================================================================="
  export CC=gcc
  export CXX=g++
  export OBJECT_MODE=32
  export CFLAGS="-maix32 -pthread"
  export CXXFLAGS="-maix32 -pthread"
  cp -r Tests Tests_orig
  (ARGS=$TEST_ARGS gmake -k test || true)
  rm -rf Tests_GCC32 ; mv Tests Tests_GCC32

echo "================================================================="
echo "== Tests with GCC - 64bit ======================================="
echo "================================================================="
  slibclean
  export CC=gcc
  export CXX=g++
  export OBJECT_MODE=64
  export CFLAGS="-maix64 -pthread"
  export CXXFLAGS="-maix64 -pthread"
  cp -r Tests_orig Tests
  (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
  rm -rf Tests_GCC64 ; mv Tests Tests_GCC64

echo "================================================================="
echo "== Tests with XLC v13 - 32bit ==================================="
echo "================================================================="
  slibclean
  if [ -e /opt/IBM/xlc/13.1.3/bin/xlc ]
  then
    export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
    export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
    export OBJECT_MODE=32
    export CFLAGS="-q32"
    export CXXFLAGS="-q32"
    cp -r Tests_orig Tests
    (ARGS=$TEST_ARGS gmake -k test || true)
    rm -rf Tests_XL13_32 ; mv Tests Tests_XL13_32
  fi

echo "================================================================="
echo "== Tests with XLC v13 - 64bit ==================================="
echo "================================================================="
  slibclean
  if [ -e /opt/IBM/xlc/13.1.3/bin/xlc ]
  then
    export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
    export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
    export OBJECT_MODE=64
    export CFLAGS="-q64"
    export CXXFLAGS="-q64"
    cp -r Tests_orig Tests
    (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
    rm -rf Tests_XL13_64 ; mv Tests Tests_XL13_64
  fi

echo "================================================================="
echo "== Tests with XLC v16 - 32bit ==================================="
echo "================================================================="
  slibclean
  if [ -e /opt/IBM/xlc/16.1.0/bin/xlc ]
  then
    export CC="/opt/IBM/xlc/16.1.0/bin/xlc"
    export CXX="/opt/IBM/xlC/16.1.0/bin/xlC"
    export OBJECT_MODE=32
    export CFLAGS="-q32"
    export CXXFLAGS="-q32"
    cp -r Tests_orig Tests
    (ARGS=$TEST_ARGS gmake -k test || true)
    rm -rf Tests_XL16_32 ; mv Tests Tests_XL16_32
  fi

echo "================================================================="
echo "== Tests with XLC v16 - 64bit ==================================="
echo "================================================================="
  slibclean
  if [ -e /opt/IBM/xlc/16.1.0/bin/xlc ]
  then
    export CC="/opt/IBM/xlc/16.1.0/bin/xlc"
    export CXX="/opt/IBM/xlC/16.1.0/bin/xlC"
    export OBJECT_MODE=64
    export CFLAGS="-q64"
    export CXXFLAGS="-q64"
    cp -r Tests_orig Tests
    (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
    rm -rf Tests_XL16_64 ; mv Tests Tests_XL16_64
  fi
  
echo "================================================================="
echo "== Tests with XLClang v16 - 32bit ==============================="
echo "================================================================="
  slibclean
  # Test with xlc 16 (xlclang)
  if [ -e /opt/IBM/xlC/16.1.0/bin/xlclang ]
  then
    export CC="/opt/IBM/xlC/16.1.0/bin/xlclang"
    export CXX="/opt/IBM/xlC/16.1.0/bin/xlclang++"
    export OBJECT_MODE=32
    export CFLAGS="-m32 -pthread"
    export CXXFLAGS="-m32 -pthread"
    cp -r Tests_orig Tests
    (ARGS=$TEST_ARGS gmake -k test || true)
    rm -rf Tests_XLCLANG16_32 ; mv Tests Tests_XLCLANG16_32
  fi

echo "================================================================="
echo "== Tests with XLClang v16 - 64bit ==============================="
echo "================================================================="
  slibclean
  if [ -e /opt/IBM/xlC/16.1.0/bin/xlclang ]
  then
    export CC="/opt/IBM/xlC/16.1.0/bin/xlclang"
    export CXX="/opt/IBM/xlC/16.1.0/bin/xlclang++"
    export OBJECT_MODE=64
    export CFLAGS="-m64 -pthread"
    export CXXFLAGS="-m64 -pthread"
    cp -r Tests_orig Tests
    (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
    rm -rf Tests_XLCLANG16_64 ; mv Tests Tests_XLCLANG16_64
  fi
  # Needed for install
  cp -r Tests_orig Tests
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -c"
export OBJECT_MODE=64
%define _cmakedatadir %{_datadir}/%{name}-%{major_version}.%{minor_version}
%define _cmakedocdir   %{_docdir}/%{name}-%{major_version}.%{minor_version}
BUILD_CMAKE=`pwd`

gmake DESTDIR=${RPM_BUILD_ROOT} install %{?_smp_mflags}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/*

find %{buildroot}%{_cmakedatadir}/Modules -type f | xargs chmod -x

# Install copyright files for main package
mkdir -p %{buildroot}/%{_cmakedocdir}
cp -p Copyright.txt %{buildroot}%{_cmakedocdir}/

cd $BUILD_CMAKE
cp -r ./Auxiliary/bash-completion %{buildroot}%{_datadir}

# CMake provides an include file... in share directory.
mkdir %{buildroot}%{_includedir}/
mv %{buildroot}%{_cmakedatadir}/include/cmCPluginAPI.h %{buildroot}%{_includedir}/
rmdir %{buildroot}%{_cmakedatadir}/include

chmod +x %{buildroot}%{_cmakedatadir}/Modules/Platform/AIX/ExportImportList


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
# Licence
%{_cmakedocdir}
%{_bindir}/*

%files data
%defattr(-,root,system,-)
# aclocal, cmake scripts, bash-completion and documentation
%{_cmakedatadir}
%{_includedir}/*


%changelog
* Fri Sep 24 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 3.21.2-2
- Correct RPATH for binaries

* Sat Aug 28 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 3.21.2-1
- Update to 3.21.2

* Wed Jul 28 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 3.21.1-1
- New version 3.21.1
- Change in strip and ar flag during archive creation (shared librairies)

* Mon Jul 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.16.8-2
- ExportImportList is executable by default

* Wed Jul 15 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.16.8-1
- New version 3.16.8
- AIX CMake variable is no more set to 1

* Wed Nov 27 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.16.0-1
- New version 3.16.0
- Automatic export of symbols

* Wed Sep 11 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.15.3-1
- New version 3.15.3
- Now compile on 64 bit
- Do not distribute macro nor filesystem subpackage
- Improve way to create a library

* Tue Apr 23 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.14.3-1
- Port new version 3.14.3
- Add more 64bit tests

* Thu Apr 18 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.14.2-1
- Port new version 3.14.2
- Erase unused files.

* Wed Apr 17 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 3.14.1-1
- Port new version 3.14.1
- Improved AIX port.

* Fri Jun 15 2018 Sena Apeke <sena.apeke.external@atos.net> - 3.11.4-1
- Add new version 3.11.4 

* Thu May 03 2018 Tony Reix <tony.reix@atos.net> - 3.11.1-1
- upgrade for AIX V6.1

* Fri Jul 24 2015 Laurent Gay <laurent.gay@atos.net> - 3.2.3-1
- upgrade for AIX V6.1

* Tue May 24 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.8.4-1
- initial version for AIX V5.3

