# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)


Name:		cmake
Version:	3.13.1
Release:	1
Summary:	Cross-platform, open-source build system
Group:		Development/Tools
License:	BSD
URL:		http://www.cmake.org
Source0:	http://www.cmake.org/files/v3.2/%{name}-%{version}.tar.gz

Source1:        cmake-init-aix
Source2:        macros.%{name}
Source1000: %{name}-%{version}-%{release}.build.log

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

# we don't want any dependencies
BuildConflicts:	libidn

Patch1:		cmake-3.13.1_expall.patch

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
Requires: AIX-rpm <  7.3.0.0
%endif


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.

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

%patch1 -p1  -b .expall


%build

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
%ifos aix6.1
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O2"
%endif
%ifos aix7.1 aix7.2
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_AIX71 -D_AIX72 -D_ALL_SOURCE -DFUNCPROTO=15 -g -O0"
%endif


echo "C compiler version:"

export CC=gcc
export CXX=g++
$CC --version

# IBM XLC is refused by "bootstrap"
#export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
#export CXX="/opt/IBM/xlC/13.1.3/bin/xlC"
#export CFLAGS="-qmaxmem=16384 -bnoquiet " $CFLAGS
#$CC -qversion


# Required n CFLAGS and CXXFLAGS by this phase of gmake:
#	[100%] Linking CXX executable ../bin/ctest
export LDFLAGS="-Wl,-bbigtoc"
export CFLAGS="$CFLAGS $LDFLAGS"

# no "-I/usr/vacpp/include" & "-I/opt/freeware/include" allowed otherwise compile of internal libs fails
export CXXFLAGS="$CFLAGS"


./bootstrap \
    --verbose \
    --parallel=16 \
    --init=%{SOURCE1} \
    --prefix=%{_prefix} \
    --datadir=/share/%{name} \
    --docdir=/doc/%{name}-%{version} \
    --mandir=/man

# This phase requires nearly 6GB on /opt
gmake --trace %{?_smp_mflags} -j16

(gmake test || true)


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

BUILD_CMAKE=`pwd`

gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/*

find %{buildroot}/%{_datadir}/%{name}/Modules -type f | xargs chmod -x

# RPM macros
#mkdir -p %{buildroot}%{rpm_macros_dir}
#/opt/freeware/bin/install -c -m 644 %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
#/usr/bin/install -i -M0644 %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
#/opt/freeware/bin/sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}/macros.%{name}
#touch -r %{SOURCE2} %{buildroot}/macros.%{name}


# RPM macros
/opt/freeware/bin/install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}
/opt/freeware/bin/sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{name}
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{name}


# Install copyright files for main package
mkdir -p %{buildroot}/%{_docdir}/%{name}/
cp -p Copyright.txt %{buildroot}/%{_docdir}/%{name}/

/opt/freeware/bin/find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f %{buildroot}/%{_docdir}/%{name}/${fname}_${dname}
done

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

cd $BUILD_CMAKE
# create manifests for splitting files and directories for filesystem-package
/opt/freeware/bin/find %{buildroot}%{_datadir}/%{name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > data_dirs.mf
/opt/freeware/bin/find %{buildroot}%{_datadir}/%{name} -type f | \
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
%{_prefix}/doc/%{name}-%{version}/
%{_bindir}/*
%{_datadir}/%{name}/
/usr/bin/*


%files data -f data_files.mf
%{_datadir}/aclocal/%{name}.m4
%{_datadir}/bash-completion

%files filesystem -f data_dirs.mf -f lib_dirs.mf

%files rpm-macros
%{rpm_macros_dir}/macros.%{name}


%changelog
* Fri Jun 15 2018 Sena Apeke <sena.apeke.external@atos.net> - 3.11.4-1
- Add new version 3.11.4 

* Thu May 03 2018 Ton Reix <tony.reix@atos.net> - 3.11.1-1
- upgrade for AIX V6.1

* Fri Jul 24 2015 Laurent Gay <laurent.gay@atos.net> - 3.2.3-1
- upgrade for AIX V6.1

* Tue May 24 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.8.4-1
- initial version for AIX V5.3

