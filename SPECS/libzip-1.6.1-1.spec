%bcond_without dotests

# By default, compiler is gcc.
#To compile with xlc : --define 'gcc_compiler=0'
#%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler: %define gcc_compiler 1}

# Current .so version is 5
# See SET_TARGET_PROPERTIES(... SOVERSION 5) in lib/CMakeLists.txt
%define soversion 5

%if %{gcc_compiler} == 1
%define compiler_msg This version has been compiled with GCC.
%else
%define compiler_msg This version has been compiled with XLC.
%endif

#By default, 64bit mode
%{!?default_bits: %define default_bits 64}

# By default, test are runned.
# No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

#default optimize is 2 ; may be 0
%{!?optimize:%define optimize 2}

%define _libdir64     %{_prefix}/lib64


Name:    libzip
Version: 1.6.1
Release: 1
Summary: C library for reading, creating, and modifying zip archives

License: BSD
Group:   Applications/File
URL:     https://libzip.org/
Source0: https://libzip.org/download/libzip-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake >= 3.16.0
# Needed to run the test suite
# find regress/ -type f | /usr/lib/rpm/perl.req
# find regress/ -type f | /usr/lib/rpm/perl.prov
#BuildRequires:  perl-interpreter
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(UNIVERSAL)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)

##Add list of Requires
##Requires: gdbm >= 1.10
##???Epoch: 1

#Patch0: %{name}-1.5.1-2018fallfixes.patch


##Provides examples
##Provides: %{name} 
##Provides: %{name} <= %{version}
##Provides: %{name}(subcomponent) = 9.9TBCsubcomponent version
##Provides: xxxTBC.so

%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%{compiler_msg}

%package devel
Summary:   Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Group:    Applications/File

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary:  Command line tools from %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Group:    Applications/File

%description tools
The %{name}-tools package provides command line tools split off %{name}:
- zipcmp
- zipmerge
- ziptool


%prep

export TAR=/usr/bin/tar
export PATH=/opt/freeware/bin:$PATH

%setup -q
#%patch0 -p0

# unwanted in package documentation
rm INSTALL.md

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit


%build

### many packages needs ulimit adaptation, add following lines if useful
##ulimit -d unlimited
##ulimit -s unlimited
##ulimit -m unlimited

#Display information about build environment
############################################
echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
echo "optimize=%{optimize}"
echo "#####"
/usr/bin/env | /usr/bin/sort | grep -v _proxy | grep -v SSH_
echo "#####"
rpm -qa | sort
echo "#####"
ulimit -a
echo "#####"

export PATH=/opt/freeware/bin:$PATH
###force ld, ar, nm to be AIX base lpp commands
export LD="/usr/bin/ld"
export AR="/usr/bin/ar"
export NM="/usr/bin/nm"
export ARFLAGS="-X32_64"
export NMFLAGS="-X32_64 -B"

### rm -f needed 
#export RM="/usr/bin/rm -f"
### default make is gmake
export MAKE="/opt/freeware/bin/gmake"
export PERL="/opt/freeware/bin/perl"

export CFLAGS="-I/usr/include -I/opt/freeware/include"
export CFLAGS="${CFLAGS} -D_LARGE_FILES -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
export CFLAGS="${CFLAGS} -fPIC"
##export CFLAGS="${CFLAGS} -D_ALL_SOURCE -D_ANSI_C_SOURCE -D_POSIX_SOURCE -D_GNU_SOURCE"
##export CFLAGS="${CFLAGS} -DUSE_NATIVE_DLOPEN -DNEED_PTHREAD_INIT"

###Add -g to CFLAGS for debug
##export CFLAGS="${CFLAGS} -g"
export CFLAGS="${CFLAGS} -O%{optimize}"


## export LDFLAGS="-Wl,-bbigtoc"

# Choose GCC or XLC
%if %{gcc_compiler} == 1

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"
###use full path for gcc except for ... which requires a string beginning with gcc:  export CC="gcc"
export CFLAGS32="-maix32"
export CFLAGS64="-maix64"

echo "GCC version=`$CC --version | head -1`"

%else

export CC="/usr/vac/bin/xlc_r"
export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"
export CFLAGS32="-q32 -qcpluscmt"
export CFLAGS64="-q64 -qcpluscmt"
echo "XLC Version=`$CC -qversion`"

export RPM_OPT_FLAGS=`echo ${RPM_OPT_FLAGS} | sed 's:-fsigned-char::'`
export CFLAGS="${CFLAGS} ${RPM_OPT_FLAGS}"

%endif

build_libzip()
{
### uncomment following set -x line to debug
set -x

echo "CC=" ${CC}
echo "CFLAGS=" ${CFLAGS}
echo "LD=" ${LD}
echo "LDFLAGS=" ${LDFLAGS}
echo "AR=" ${AR}
echo "ARFLAGS=" ${ARFLAGS}

rm -f CMakeCache.txt

#  export RUNTIME_OUTPUT_DIRECTORY=%{_libdir64} 
#  export ARCHIVE_OUTPUT_DIRECTORY=%{_libdir64}
#  export LIBRARY_OUTPUT_DIRECTORY=%{_libdir64} 
#  export LIBRARY_OUTPUT_PATH=%{_libdir64}

#cmake .  --trace --debug-trycompile --debug-output -G"Unix Makefiles"
cmake -L . \
    -G"Unix Makefiles" \
    -DCMAKE_SYSTEM_NAME="AIX"  \
    -DCMAKE_C_COMPILER="${CC}"  \
    -DCMAKE_CXX_COMPILER="${CXX}" \
    -DCMAKE_C_FLAGS="${CFLAGS}" \
    -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_SHARED_LIBS=ON  \
    -DBUILD_STATIC_LIBS=OFF \
    -DCMAKE_LINK_LIBRARY_FLAG="${CFLAGS}" \
    -DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_MODULE_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_SHARED_LINKER_FLAGS="${LDFLAGS}" \
    -DCMAKE_SHARED_LIBRARY_LINK="${LDFLAGS}" \
    -DCMAKE_AR="${AR}" \
    -DCMAKE_AR_FLAGS="${ARFLAGS}" \
    -DTMPDIR=/var/tmp \
    -DINSTALL_LAYOUT=RPM \
    -DINSTALL_SYSCONFDIR="%{_sysconfdir}" \
    -DCMAKE_INSTALL_MANDIR="%{_mandir}" \
    $*

##    -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
##    -DENABLE_MAN_PAGES:BOOL=ON \
##    -DENABLE_TESTS:BOOL=ON \
##    -DENABLE_EXAMPLES:BOOL=OFF \

#$MAKE %{?_smp_mflags} --trace
$MAKE --trace --print-directory -j16 %{?_smp_mflags} -j16

/usr/sbin/slibclean

} #end build_libzip()


# build 32bit mode
echo "build 32bit mode"

(
  cd 32bit
  export OBJECT_MODE=32
  export LIBS32="-L/opt/freeware/lib -L/usr/lib"

  export CFLAGS="${CFLAGS} ${CFLAGS32} ${LIBS32}"
  export CXXFLAGS="${CFLAGS} ${CFLAGS32} ${LIBS32}"

  export LDFLAGS32="-Wl,-b32"
  export LDFLAGS32="${LDFLAGS32} -Wl,$LIBS32"
  export LDFLAGS32="${LDFLAGS32} -Wl,-bmaxdata:0x80000000"
#  export LDFLAGS32="${LDFLAGS32} -Wl,-blibpath:%{_libdir}:/usr/lib"
  export LDFLAGS="${LDFLAGS32}"

  #build_libzip -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=%{_libdir}  
  build_libzip

  cd ..

)

# build 64bit mode
(
  cd 64bit
  export OBJECT_MODE=64
  export LIBS64="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib"
  export CFLAGS="${CFLAGS} ${CFLAGS64} ${LIBS64}"
  export CXXFLAGS="${CFLAGS} ${CFLAGS64} ${LIBS64}"
  
  export LDFLAGS64="-Wl,-b64"
  export LDFLAGS64="$LDFLAGS64 -Wl,$LIBS64"
  ###no -bmaxdata flag for 64bit
  export LDFLAGS64="$LDFLAGS64 -Wl,-blibpath:%{_libdir64}:/usr/lib64:%{_libdir}:/usr/lib"
  export LDFLAGS="$LDFLAGS64"

  ### call build_xxx with 64bit specific option
  ### KO use -DCMAKE_LIBRARY_OUTPUT_DIRECTORY
  ### the DLL part of a shared library is treated as a runtime target and 
  ### the corresponding import library is treated as an archive target.
  ### KO use -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY instead of -DCMAKE_LIBRARY_OUTPUT_DIRECTORY
  ### KO use -DCMAKE_RUNTIME instead of -DCMAKE_LIBRARY_OUTPUT_DIRECTORY
  ### KO export RUNTIME_OUTPUT_DIRECTORY=%{_libdir64} 
  ### KO export ARCHIVE_OUTPUT_DIRECTORY=%{_libdir64}
  ### KO export LIBRARY_OUTPUT_DIRECTORY=%{_libdir64} 
  ### KO export LIBRARY_OUTPUT_PATH=%{_libdir64}

  ### build_libzip -DCMAKE_RUNTIME_OUTPUT_DIRECTORY=%{_libdir64}   -DCMAKE_ARCHIVE_OUTPUT_DIRECTORY=%{_libdir64} -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=%{_libdir64} -DLIBRARY_OUTPUT_PATH=%{_libdir64}

  build_libzip

  cd ..

)


%install
### uncomment following set -x line to debug
set -x

export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar"
export ARFLAGS="-X32_64"
export NM="/usr/bin/nm"
export NMFLAGS="$NMFLAGS -X32_64 -B"

export INSTALL="/opt/freeware/bin/install "

export LN="/usr/bin/ln -s"
export RM="/usr/bin/rm -f"
export MAKE="/opt/freeware/bin/gmake"


[ "${RPM_BUILD_ROOT}" == "" ] && exit 1
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT


# ==========================
# Install the 64 bit version
# ==========================
cd 64bit

export OBJECT_MODE=64

$MAKE DESTDIR=${RPM_BUILD_ROOT} install 

# The 32/64 bit library will be been created with the 32 bit install
# Must extract the non-stripped .so from the installed library
(
 cd  ${RPM_BUILD_ROOT}
 $AR -X64 -vx ${RPM_BUILD_ROOT}%{_libdir}/libzip.a libzip.so.%{soversion}
)
# Create the symlink to libzip.a
$RM  ${RPM_BUILD_ROOT}%{_libdir}/libzip.a
$LN  ../lib/libzip.a   ${RPM_BUILD_ROOT}%{_libdir}/libzip.a

# Install stripped 64 bit .so files if required - Note new Cmake stripped them
cp lib/libzip.so.%{soversion} ${RPM_BUILD_ROOT}%{_libdir}
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/libzip.so.%{soversion}
$LN  ./libzip.so.%{soversion} ${RPM_BUILD_ROOT}%{_libdir}/libzip.so

# Move the 64 bit libraries
mv ${RPM_BUILD_ROOT}/%{_libdir} ${RPM_BUILD_ROOT}/%{_libdir64}

# Move the 64 bit utilities
(
 cd  ${RPM_BUILD_ROOT}
 for dir in bin
 do
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/$dir
    for f in $(ls -1| grep -v -e _32 -e _64)
    do
        mv ${f} ${f}_64
        /usr/bin/strip -X32_64 ${f}_64 || :
    done
 done
)

cd ..


# ==========================
# Install the 32 bit version ${RPM_BUILD_ROOT} = %buildroot
# ==========================
cd 32bit

export OBJECT_MODE=32

#$MAKE install 
#$MAKE --trace --print-directory -d DESTDIR=${RPM_BUILD_ROOT} install 
$MAKE DESTDIR=${RPM_BUILD_ROOT} install 

# The 32 bit library has been created containing libzip.a[libzip.so.5]
# Add the 64 bit library member
(
 cd  ${RPM_BUILD_ROOT}
 $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libzip.a ./libzip.so.%{soversion}
)

# Install stripped .so files if required - Note the new Cmake stripped them
cp lib/libzip.so.%{soversion} ${RPM_BUILD_ROOT}%{_libdir}
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/libzip.so.%{soversion}
ln -s ./libzip.so.%{soversion} ${RPM_BUILD_ROOT}%{_libdir}/libzip.so

# Move the 32 bit utilities
(
 cd  ${RPM_BUILD_ROOT}
 for dir in bin
 do
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/$dir
    for f in $(ls -1| grep -v -e _32 -e _64)
    do
        mv ${f} ${f}_32
        /usr/bin/strip -X32_64 ${f}_32 || :
        $LN ${f}_64 ${f}
    done
 done
)

cd ..

###RPM4 check call
###how to make RPM4 check camll dependant on dotests??
#%check
##ctest -V %{?_smp_mflags}

%check
%if %{with dotests}
cd 64bit
( gmake --trace --print-directory -k check || true )
/usr/sbin/slibclean
cd ../32bit
( gmake --trace --print-directory -k check || true )
/usr/sbin/slibclean
%endif


%post
###Add package specific post installation stuff
exit 0


%preun
###Add package specific pre uninstallation stuff
exit 0

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc 32bit/LICENSE
%{_libdir}/libzip.a
# The .so files are no longer included unless specific need
# %{_libdir}/libzip.so
# %{_libdir}/libzip.so.%{soversion}
%{_libdir64}/libzip.a
# The .so files are no longer included unless specific need
# %{_libdir64}/libzip.so
# %{_libdir64}/libzip.so.%{soversion}

%files tools
%defattr(-,root,system)
%{_bindir}/zipcmp*
%{_bindir}/zipmerge*
%{_bindir}/ziptool*
%{_mandir}/man1/zip*

%files devel
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/THANKS* 32bit/*.md
%{_includedir}/zip.h
%{_includedir}/zipconf*.h
%{_libdir}/pkgconfig/libzip.pc
%{_mandir}/man3/libzip*
%{_mandir}/man3/zip*
%{_mandir}/man3/ZIP*

%changelog
* Wed Feb 18 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.6.1-1
- New version 1.6.1

* Fri Dec 13 2019 Michael Wilson <michael.a.wilson@atos.net> 1.5.1-2
- Archive non-stripped 32 & 64 bit libzip.so.soversion in libzip.a
- Adaptation to new Cmake
- Adaptation to RPM version 4, brpm.OLD and build environment laurel2

* Fri Feb 15 2019 Daniele Silvestre <daniele.silvestre@atos.net> 1.5.1-1
- First delivery for AIX on bullfreeware

