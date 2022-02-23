%define realname yaml

Name:       libyaml
Version:    0.1.7
Release:    1
Summary:    YAML 1.1 parser and emitter written in C
Group:      System Environment/Libraries
License:    MIT
URL:        http://pyyaml.org/
Source0:    http://pyyaml.org/download/libyaml/%{realname}-%{version}.tar.gz

Source10: %{name}-%{version}-%{release}.build.log

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# Configure tests for gcc first, so default is GCC if installed on the machine
# To force gcc : --define 'gcc_compiler=x'
# To use XLC : --define 'gcc_compiler=0'
%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}

%define _libdir64 %{_prefix}/lib64


%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.

The library is available as 32-bit and 64-bit.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif

%package devel
Summary:   Development files for LibYAML applications
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use LibYAML.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
%setup -q -n %{realname}-%{version}

echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export RM="/usr/bin/rm -f"

# Display build environment and currently installed RPM packages
/usr/bin/env
rpm -qa

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"


# Choose XLC or GCC
%if %{gcc_compiler} == 1

export NM="/opt/freeware/bin/nm"
export CC__="/opt/freeware/bin/gcc"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

export NM="/usr/bin/nm -X32_64"
export CC__="xlc_r"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

type $CC__

export CC32=" ${CC__}  ${FLAG32} -D_LARGE_FILES"
export CC64=" ${CC__}  ${FLAG64} -D_LARGE_FILES"


cd 64bit
# first build the 64-bit version
export CC="${CC64} "
export OBJECT_MODE=64

# export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
   (gmake -k check || true)
fi

cd ../32bit
# now build the 32-bit version
export CC="${CC32} "
export OBJECT_MODE=32

# export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
   (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    #/usr/bin/ar -X64 -x ${f}
    ${AR} -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    #/usr/bin/ar -X32 -x ${f}
    ${AR} -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
# /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}*.so*
${AR} -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}*.so*

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*

%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/html
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig
%{_libdir64}/*.la
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Tue Mar 28 2017 Michael Wilson <michael.a.wilson@atos.net> - 0.1.7-1
- Update to version 0.1.7

* Tue Feb 12 2013 Gerard Visiedo  <gerard.visiedo@bull.net> - 0.1.4-2
- Add omitted file yaml.pc

* Wed Jan 16 2013 Gerard Visiedo  <gerard.visiedo@bull.net> - 0.1.4-1
- Initial port on Aix6.1
