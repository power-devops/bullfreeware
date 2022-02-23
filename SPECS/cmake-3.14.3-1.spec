# By default, test are runned. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)


%global major_version 3
%global minor_version 14

Name:		cmake
Version:        %{major_version}.%{minor_version}.3
Release:	1
Summary:	Cross-platform, open-source build system
Group:		Development/Tools
License:	BSD
URL:		http://www.cmake.org
Source0:	http://www.cmake.org/files/v3.2/%{name}-%{version}.tar.gz

Source1:        cmake-init-aix
Source2:        macros.%{name}

Source1000: %{name}-%{version}-%{release}.build.log

BuildRoot:	/var/tmp/%{name}-%{version}-root

# we don't want any dependencies
BuildConflicts:	libidn

Patch1:         cmake-3.14.1_NewAIXbehavior.patch
Patch2:         cmake-3.14.1_NewAIXbehavior_tests.patch
Patch3:         cmake-3.14.1_NewAIXbehavior_readme.patch

Requires:       %{name}-data = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}


# cmake depends on the availability of functions, like futimens, appearing in 7.1
# So, cmake must be built on AIX 6.1 and on AIX 7.1
# The AIX 6.1 version should work on AIX 7.* too, but without some features
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
Requires: AIX-rpm <  6.2.0.0
%endif
%ifos aix7.1 aix7.2
Requires: AIX-rpm >= 7.1.0.0
%endif


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.

Behavior of CMake on AIX has been changed in 3.14 to obey to AIX rules.
See /opt/freeware/share/cmake-3.14/Modules/readme_aix.txt for more informations.

%package        data
Summary:        Common data-files for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}

%description    data
This package contains common data-files for %{name}.

%package        filesystem
Summary:        Directories used by CMake modules
Group:          Development/Tools

%description    filesystem
This package owns all directories used by CMake modules.

%package        rpm-macros
Summary:        Common RPM macros for %{name}
Group:          Development/Tools
Requires:       AIX-rpm
# when subpkg introduced
Conflicts:      cmake-data < 3.10.1-2
#BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for %{name}.


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
SO=`/usr/bin/df -k /var | awk '{if(NR==2)print $3}'`
echo "Disk space available for building cmake must be >= 2GB"
if [ "$SO" -lt 2000000 ]
then
	echo "Not enough disk space on /var !"
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
#	#elif defined(_AIX71)
#  	    return futimens(req->file, ts);
# -mcmodel=large or -Wl,-bbigtoc is required to link ctest.
# -mcmodel is better, but not available in AIX6.1.
LDFLAGS="-Wl,-bmaxdata:0x80000000"
CFLAGS="-D_LARGE_FILES -DSYSV -D_AIX -D_ALL_SOURCE -DFUNCPROTO=15"
%ifos aix6.1
export LDFLAGS="$LDFLAGS -Wl,-bbigtoc"
export CFLAGS="$CFLAGS -D_AIX61" 
%else
# aix7.1 aix7.2
export LDFLAGS="$LDFLAGS"
export CFLAGS="$CFLAGS -D_AIX71 -D_AIX72 -mcmodel=large"
%endif

echo "C compiler version:"
export CC=gcc
export CXX=g++
$CC  --version
$CXX --version

# IBM XLC is refused by "bootstrap"
# XLC support of C++11 is not OK for CMake.
# XLC 16 (XLClang) should be OK.
# Not OK in 2019-04.
#export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
#export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
#export CFLAGS="-qmaxmem=16384 -bnoquiet " $CFLAGS
#$CC -qversion

# no "-I/usr/vacpp/include" & "-I/opt/freeware/include" allowed otherwise compile of internal libs fails
export CXXFLAGS="$CFLAGS"

./bootstrap \
    --verbose \
    --parallel=16 \
    --init=%{SOURCE1} \
    --prefix=%{_prefix}

# This phase requires nearly 6GB on /opt
gmake --trace %{?_smp_mflags} -j16 VERBOSE=1


####### TEST #######
if [ "%{dotests}" == 1 ]
then
  if [ -e /lib/syscalls.exp ]
   then
    TEST_ARGS=""
   else
    TEST_ARGS="-E LinkStatic"
  fi

  TEST_ARGS="$TEST_ARGS -j 16"
  export TAR=/opt/freeware/bin/tar
  export OBJECT_MODE=
  export LDFLAGS=""
  export CFLAGS=""
  export CXXFLAGS=""

echo "================================================================="
echo "== Tests with GCC - 32bit ======================================="
echo "================================================================="
  # Test with gcc
  export CC=gcc
  export CXX=g++
  export OBJECT_MODE=32
  export CFLAGS="-maix32"
  export CXXFLAGS="-maix32"
  cp -r Tests Tests_orig
  (ARGS=$TEST_ARGS gmake -k test || true)
  rm -rf Tests_GCC ; mv Tests Tests_GCC32

echo "================================================================="
echo "== Tests with GCC - 64bit ======================================="
echo "================================================================="
  # Test with gcc 64 bits
  slibclean
  export CC=gcc
  export CXX=g++
  export OBJECT_MODE=64
  export CFLAGS="-maix64"
  export CXXFLAGS="-maix64"
  cp -r Tests_orig Tests
  (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
  rm -rf Tests_GCC64 ; mv Tests Tests_GCC64

echo "================================================================="
echo "== Tests with XLC v13 - 32bit ==================================="
echo "================================================================="
  # Test with xlc 13
  slibclean
  export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
  export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
  export OBJECT_MODE=32
  export CFLAGS="-q32"
  export CXXFLAGS="-q32"
  cp -r Tests_orig Tests
  (ARGS=$TEST_ARGS gmake -k test || true)
  rm -rf Tests_XLC ; mv Tests Tests_XLC32

echo "================================================================="
echo "== Tests with XLC v13 - 64bit ==================================="
echo "================================================================="
  # Test with xlc 13
  slibclean
  export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
  export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
  export OBJECT_MODE=64
  export CFLAGS="-q64"
  export CXXFLAGS="-q64"
  cp -r Tests_orig Tests
  (ARGS="$TEST_ARGS --build-options -DCMAKE_C_FLAGS=$CFLAGS -DCMAKE_CXX_FLAGS=$CXXFLAGS" gmake -k test || true)
  rm -rf Tests_XLC ; mv Tests Tests_XLC64

echo "================================================================="
echo "== Tests with XLC v16 - 32bit ==================================="
echo "================================================================="
  # Test with xlc 16 (xlclang)
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
    rm -rf Tests_XLCLANG ; mv Tests Tests_XLCLANG
  fi

echo "================================================================="
echo "== Tests with XLC v16 - 64bit ==================================="
echo "================================================================="
  # Test with xlc 16 (xlclang)
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
    rm -rf Tests_XLCLANG ; mv Tests Tests_XLCLANG64
  fi

  # Needed for instal
  cp -r Tests_orig Tests
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -c"

BUILD_CMAKE=`pwd`

gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/*

find %{buildroot}%{_datadir}/%{name}-%{major_version}.%{minor_version}/Modules -type f | xargs chmod -x

# RPM macros
#mkdir -p %{buildroot}%{rpm_macros_dir}
#/opt/freeware/bin/install -c -m 644 %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
#/usr/bin/install -i -M0644 %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
#/opt/freeware/bin/sed -i -e "s|@@CMAKE_VERSION@@|%{major_version}.%{minor_version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}/macros.%{name}
#touch -r %{SOURCE2} %{buildroot}/macros.%{name}


# RPM macros
/opt/freeware/bin/install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
/opt/freeware/bin/sed -i -e "s|@@CMAKE_VERSION@@|%{major_version}.%{minor_version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{name}
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}


# Install copyright files for main package
mkdir -p %{buildroot}/%{_docdir}%{name}/
cp -p Copyright.txt %{buildroot}%{_docdir}/%{name}-%{major_version}.%{minor_version}/

/opt/freeware/bin/find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f %{buildroot}%{_docdir}/%{name}-%{major_version}.%{minor_version}/${fname}_${dname}
done

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

cd $BUILD_CMAKE
# create manifests for splitting files and directories for filesystem-package
/opt/freeware/bin/find %{buildroot}%{_datadir}/%{name}-%{major_version}.%{minor_version} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > data_dirs.mf
/opt/freeware/bin/find %{buildroot}%{_datadir}/%{name}-%{major_version}.%{minor_version} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > data_files.mf
/opt/freeware/bin/find %{buildroot}%{_libdir}/%{name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > lib_dirs.mf
/opt/freeware/bin/find %{buildroot}%{_libdir}/%{name} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > lib_files.mf
/opt/freeware/bin/find %{buildroot}%{_bindir} -type f -or -type l -or -xtype l | \
  sed -e '/.*-gui$/d' -e '/^$/d' -e 's!^%{buildroot}!"!g' -e 's!$!"!g' >> lib_files.mf

cp -r ./Auxiliary/bash-completion %{buildroot}%{_datadir}


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system,-)
%{_prefix}/doc/%{name}-%{major_version}.%{minor_version}/
%{_bindir}/*
%{_datadir}/%{name}-%{major_version}.%{minor_version}/
/usr/bin/*


%files data -f data_files.mf
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/bash-completion

%files filesystem -f data_dirs.mf -f lib_dirs.mf

%files rpm-macros
%{rpm_macros_dir}/macros.%{name}


%changelog
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

