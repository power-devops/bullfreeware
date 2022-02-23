Summary:   IDL parsing library
Name:           libIDL
Version:        0.8.14
Release:        1
Source:         http://ftp.acc.umu.se/pub/GNOME/sources/%{name}/0.8/%{name}-%{version}.tar.bz2
#Patch0:	%{name}-%{version}-aix.patch
Group:     Libraries
License:        LGPL
BuildRequires: bison
BuildRoot: /var/tmp/%{name}-%{version}-root

%define _libdir64 %{_prefix}/lib64

%description
libIDL is a small library for creating parse trees of CORBA v2.2
compliant Interface Definition Language (IDL) files, which is a
specification for defining interfaces which can be used between
different CORBA implementations.

%package devel
Summary:  Header files and libraries needed for libIDL development
Group:    Development/Libraries
Requires: %{name} = %{version}

%description devel
This package includes the header files and libraries needed for
developing programs using libIDL.


%prep
%setup -q

#%patch0 -p1 -b .aix

%build

export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"

# We must initialyse flags CPP ans CXXCPP due to compilation GConf issue
CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPP="/usr/ccs/lib/cpp" \
CXXCPP="/usr/vac/exe/xlCcpp" \
LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib" \
./configure \
	--disable-silent-rules \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
        --disable-static \
        --enable-shared

make

cp .libs/libIDL-2.so.0 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPP="/usr/ccs/lib/cpp" \
CXXCPP="/usr/vac/exe/xlCcpp" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--disable-static \
	--enable-shared

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libIDL-2.a ./libIDL-2.so.0


%install
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p  ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
cp %{name}*.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

# Extract dynamic .so X32 librairies
cd ${RPM_BUILD_ROOT}%{_libdir}
for f in lib*.a ; do
    ar -X32 -x ${f}
done
#
for f in lib*so* ; do
    ln -s ${f} $(basename ${f} .0)
done

mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.a ; do
    ar -X64 -x ${f}
done
for f in lib*so* ; do
    ln -s ${f} $(basename ${f} .0)
done

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p usr/include/%{name}
  cd usr/include/%{name}
  ln -sf ../../..%{_prefix}/include/%{name}-2.0/%{name}/* .
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc COPYING ChangeLog AUTHORS
%doc README NEWS BUGS tstidl.c
%{_libdir}/lib*.a
%{_libdir}/lib*.so.*
%{_libdir}/lib*.so
%{_libdir64}/lib*.so.*
%{_libdir64}/lib*.so
/usr/lib/*.a

%files devel
%defattr(-,root,system)
%{_bindir}/%{name}-config-2
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.la
%{_includedir}/%{name}-2.0/%{name}/*.h
/usr/include/%{name}/*.h


%changelog
* Thu Jul 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> 0.8.14-1
- Initial port on Aix6.1
