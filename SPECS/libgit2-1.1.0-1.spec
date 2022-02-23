# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

# Current .so version is 1.1
# See SET_TARGET_PROPERTIES( SOVERSION LIBGIT2_SOVERSION) in src/CMakeLists.txt
# LIBGIT2_SOVERSION taken from include/git2/version.h in CMakeLists.txt
%define soversion 1.1


Name:           libgit2
Version:        1.1.0
Release:        1
Summary:        C implementation of the Git core methods as a library with a solid API
License:        GPLv2 with exceptions
URL:            https://libgit2.org/
Source0:        https://github.com/libgit2/libgit2/releases/download/v%{version}/%{name}-%{version}.tar.gz
# https://github.com/extrawurst/gitui/issues/128
# https://github.com/libgit2/libgit2/commit/d62e44cb8218840a0291fb5fbb7c5106e1e35a12

Source9:        %{name}-libssh2PC
Source10:       %{name}-%{version}-%{release}.build.log

# Patch from Fedora 1.0.1 (Patch1 integrated in 1.1.0)
Patch2:         libgit2-no-fvisibility.patch

# Patch from libgit2 Community (but incomplete - pb not WR -> pb not on DIR)
Patch3:         libgit2-fsync.patch


# AIX patch to find libssh2
Patch4:         libgit2-libssh2-find-package-CMakeLists.patch
# AIX off64_t is long long, 6.1 has no stat/timespec and no futimes()
Patch5:         libgit2-aix-off64_t-timespec-futimes.patch
# AIX patch for doubtful tests using FILENAME_MAX
Patch6:         libgit2-aix-tests.patch
# AIX patch for malloc(0)/calloc(0)/...  - "no memory"  (replaces Linux compat)
Patch7:         libgit2-allocZero.patch

BuildRequires:  gcc
BuildRequires:  cmake >= 3.5.1
# Not yet available on AIX  BuildRequires:  ninja-build
# Not yet available on AIX BuildRequires:  http-parser-devel
BuildRequires:  libcurl-devel
BuildRequires:  libssh2-devel
# Use the LPP on AIX BuildRequires:  openssl-devel
# Package pcre2 not ported to AIX but libgit2 accepts pcre
BuildRequires:  pcre-devel
BuildRequires:  python3
BuildRequires:  zlib-devel
BuildRequires:  sed
# For option -delete of Open Source find not supported by AIX find
BuildRequires:  findutils
Provides:       bundled(libxdiff)

%description
libgit2 is a portable, pure C implementation of the Git core methods
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language
with bindings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

# Remove VCS files from examples
/opt/freeware/bin/find examples -name ".gitignore" -delete -print

# Don't run "online" tests
sed -i '/-sonline/s/^/#/' tests/CMakeLists.txt

# Remove bundled libraries - Fedora does not set USE_HTTP_PARSER=builtin
# If USE_HTTP_PARSER not "system", build needs directory deps
# rm -vr deps

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
# Flag _LINUX_SOURCE_COMPAT added for malloc(0), etc
# but this flag does not help with fsync() on FDs no write perm or directory
# Flag no longer required with libgit2-allocZero.patch

#export FLAG32="-maix32 -pthread -D_LARGE_FILES -D_LINUX_SOURCE_COMPAT"
#export FLAG64="-maix64 -pthread -D_LARGE_FILES -D_LINUX_SOURCE_COMPAT"
export FLAG32="-maix32 -pthread -D_LARGE_FILES"
export FLAG64="-maix64 -pthread -D_LARGE_FILES"


# First build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="${CC__} ${FLAG64}"
export CXX="${CXX__} ${FLAG64}"
export LDFLAGS=" -Wl,-bbigtoc -L/opt/freeware/lib64:/opt/freeware/lib:/usr/lib "

mkdir build && cd build

# Removed ninja build option and changed http parser from system to builtin
# Changed USE_HTTP_PARSER from system to builtin
# Changed REGEX_BACKEND from pcre2 to pcre
#  -GNinja 
#  -DCMAKE_BUILD_TYPE=RelWithDebInfo 

#  -DLIBSSH2_DIR=/opt/freeware/lib64

cmake .. -B%{_target_platform} \
  -DCMAKE_PREFIX_PATH=/opt/freeware \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir64} \
  -DREGEX_BACKEND=pcre \
  -DUSE_HTTP_PARSER=builtin \
  -DUSE_SHA1=HTTPS \
  -DUSE_HTTPS=OpenSSL \
  -DUSE_NTLMCLIENT=OFF \
  %{nil}

# Not yet available on AIX  %%ninja_build -C %{_target_platform}
cd %{_target_platform}
# cmake --build .
gmake --trace %{?_smp_mflags}

cd ../..


# Build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="${CC__} ${FLAG32}"
export CXX="${CXX__} ${FLAG32}"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-bbigtoc -L/opt/freeware/lib:/usr/lib"

mkdir build && cd build

#  -DLIBSSH2_DIR=/opt/freeware/lib 

cmake .. -B%{_target_platform} \
  -DCMAKE_PREFIX_PATH=/opt/freeware \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DREGEX_BACKEND=pcre \
  -DUSE_HTTP_PARSER=builtin \
  -DUSE_SHA1=HTTPS \
  -DUSE_HTTPS=OpenSSL \
  -DUSE_NTLMCLIENT=OFF \
  %{nil}

# Not yet available on AIX  %%ninja_build -C %{_target_platform}
cd %{_target_platform}
# cmake --build .
gmake %{?_smp_mflags}

cd ../..


# Archive 64 bit shared object in 32 bit shared library   - perform at install
# The .so version built is 1.0, but Fedora installs 1.0.1 with symlink 1.0
# The new .so version from libgit2 github is 1.1
# Note new Cmake strips the .so files
# ${AR} -q ../32bit/build/ppc-ibm-aix6.1-gnu/libgit2.a ../64bit/build/ppc-ibm-aix6.1-gnu/src/libgit2.so.%{soversion}



%install

export AR="/usr/bin/ar"
export LN="/usr/bin/ln -s"
export RM="/usr/bin/rm"


[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


cd 64bit
export OBJECT_MODE=64

# %%ninja_install -C %{_target_platform}

cd build/%{_target_platform}

# cmake .. -DCMAKE_INSTALL_PREFIX=/opt/freeware
# cmake --build . --target install

gmake DESTDIR=${RPM_BUILD_ROOT} install

# Move lib to lib64 not needed with CMAKE_INSTALL_LIBDIR=/opt/freeware/lib64
# mv  ${RPM_BUILD_ROOT}/%{_libdir}/*  ${RPM_BUILD_ROOT}/%{_libdir64}

# The 32/64 bit library will be been created with the 32 bit install
# Must extract the non-stripped .so from the installed library
(
 cd  ${RPM_BUILD_ROOT}
 $AR -X64 -vx ${RPM_BUILD_ROOT}%{_libdir64}/libgit2.a libgit2.so.%{soversion}
) 


 
cd ../..

cd ../32bit
export OBJECT_MODE=32

cd build/%{_target_platform}

# cmake .. -DCMAKE_INSTALL_PREFIX=/opt/freeware
# cmake --build . --target install

gmake DESTDIR=${RPM_BUILD_ROOT} install


# The 32 bit library has been created containing libgit2.a[libgit2.so.1.1]
# Add the 64 bit library member
(
 cd  ${RPM_BUILD_ROOT}
 $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgit2.a ./libgit2.so.%{soversion}
)

# Create lib64/libgit2.a symlink to lib/libgit2.a
$RM  ${RPM_BUILD_ROOT}%{_libdir64}/libgit2.a
$LN  ../lib/libgit2.a ${RPM_BUILD_ROOT}%{_libdir64}/libgit2.a




%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# 3 tests fail calling git_remote_push(), git_stash_apply() with Out of memory
# linked to *alloc(0) returning NULL, patched by libgit2-allocZero.patch

# 7 tests fail due to fsync() on directory not supprted/required on AIX

# 6 tests fail in repo::discover  on AIX 6.1 realpath(file, NULL)
# 2 tests fail in config::conditionals::gitdir / gitdir_i AIX 6.1 realpath()

#AIX6.1 realpath(file_name, resolved_name==NULL) unspecified in early UNIX/POSIX

cd 64bit
export OBJECT_MODE=64

# %%ninja_test -C %{_target_platform}

cd build/%{_target_platform}
  #(ctest -V || true)
  (gmake test  || true)
cd ../..

cd ../32bit
export OBJECT_MODE=32

cd build/%{_target_platform}
  #(ctest -V || true)
  (gmake test  || true)



%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}



%files
%defattr(-,root,system)
%license 32bit/COPYING
# %{_libdir}/libgit2.so.*
# %{_libdir64}/libgit2.so.*
%{_libdir}/libgit2.a
%{_libdir64}/libgit2.a

%files devel
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/docs 32bit/examples 32bit/README.md
# %{_libdir}/libgit2.so
# %{_libdir64}/libgit2.so
%{_libdir}/pkgconfig/libgit2.pc
%{_includedir}/git2.h
%{_includedir}/git2/

%changelog
* Tue Nov 24 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.1.0-1
- Update to version 1.1.0

* Thu Oct 08 2020 Michael Wilson <michael.a.wilson@atos.com> - 1.0.1-1
- Initial port on AIX, largely based on Fedora 33
- Test results indicate fsync(FD_no_write) and malloc(0) issues in code
-   Patch W/A for fsync() received from Community (but incomplete)
-   Patch W/A for alloc zero issues and tests giving error "Out of memory"
-   Patch W/A for AIX 6.1 realpath(file_name, NULL) returns NULL

