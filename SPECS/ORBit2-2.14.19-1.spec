Summary:        A high-performance CORBA Object Request Broker.
Name:           ORBit2
Version:        2.14.19
Release:        1
URL:            http://www.labs.redhat.com/orbit/
Source0:         http://ftp.acc.umu.se/pub/GNOME/sources/ORBit2/2.14/%{name}-%{version}.tar.bz2
Source1: 	orbit-config.h
Group:          System Environment/Daemons
License:        LGPL/GPL
Prereq:        /sbin/install-info
BuildRequires:  pkgconfig >= 0.8
Requires:       glib2 >= 2.32.0
Requires:       libIDL >= 0.8.14
BuildRequires:  glib2-devel >= 2.8.0
BuildRequires:  libIDL-devel >= 0.8.2


BuildRoot: /var/tmp/%{name}-%{version}-root

%define _libdir64 %{_prefix}/lib64

%description
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

You will need to install this package and ORBit-devel if you want to
write programs that use CORBA technology.

%package devel
Summary:          Development libraries, header files and utilities for ORBit.
Group:            Development/Libraries
Requires:         %name = %{version}
Requires:         pkgconfig >= 0.8
Requires:         glib2 >= 2.8.0
Requires:         glib2-devel >= 2.8.0
Requires:         libIDL >= 0.8.2
Requires:         libIDL-devel >= 0.8.2


%description devel
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker) with support for the
C language.

%prep
%setup -q
mv ltmain.sh ltmain.sh.orig
sed s/relink=yes/relink=no/ ltmain.sh.orig > ltmain.sh


%build

export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64 -g "
export CXX="/usr/vacpp/bin/xlC_r -q64 -g "

# We must initialyse flags CPP ans CXXCPP due to compilation GConf issue
ORBIT_IDL_LIBS="/opt/freeware/lib/libIDL-2.la" \
CFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include" \
CPPFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include" \
CPP="/usr/ccs/lib/cpp" \
CXXCPP="/usr/vac/exe/xlCcpp" \
LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib -lgmodule-2.0" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir64} \
        --disable-static \
        --enable-shared
make

cp src/orb/.libs/libORBit-2.so.0 .
cp src/services/imodule/.libs/libORBit-imodule-2.so.0 .
cp src/services/name/.libs/libORBitCosNaming-2.so.0 .
cp src/services/name/libname-server-2.a .
cp test/everything/.libs/Everything_module.so .
cp ./include/orbit/orbit-config.h orbit-config-ppc64.h

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r -g"
export CXX="/usr/vacpp/bin/xlC_r -g"

ORBIT_IDL_LIBS="/opt/freeware/lib/libIDL-2.la" \
CFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include" \
CPPFLAGS="-D_LARGE_FILES -D_LINUX_SOURCE_COMPAT -D_LARGEFILE_SOURCE -I/opt/freeware/include -I/usr/include" \
CPP="/usr/ccs/lib/cpp" \
CXXCPP="/usr/vac/exe/xlCcpp" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib -lgmodule-2.0" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir} \
	--disable-static \
	--enable-shared
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/orb/.libs/libORBit-2.a ./libORBit-2.so.0
${AR} -q src/services/imodule/.libs/libORBit-imodule-2.a ./libORBit-imodule-2.so.0
${AR} -q src/services/name/.libs/libORBitCosNaming-2.a ./libORBitCosNaming-2.so.0
${AR} -q test/everything/.libs/Everything_module.a ./Everything_module.so

cp ./include/orbit/orbit-config.h orbit-config-ppc32.h


%install
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make V=0 DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* ||


# Extract dynamic .so X32 librairies
cd ${RPM_BUILD_ROOT}%{_libdir}
for f in lib*.a ; do
    ar -X32 -x ${f}
done
for f in lib*so.* ; do
    ln -s ${f} $(basename ${f} .0)
done
cd orbit-2.0
ar -X32 -x Everything_module.a

${RM} ${RPM_BUILD_ROOT}%{_libdir}/*.o

# Extract dynamic .so X64 librairies
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.a ; do
    ar -X64 -x ${f}
done
ar -X64 -x ../lib/orbit-2.0/Everything_module.a

cp ${RPM_BUILD_DIR}/%{name}-%{version}/libname-server-2.a ${RPM_BUILD_ROOT}%{_libdir64}
for f in lib*so.* ; do
    ln -s ${f} $(basename ${f} .0)
done

# fix multilib conflict caused by orbit-config.h
cp ${RPM_BUILD_DIR}/%{name}-%{version}/orbit-config-ppc64.h $RPM_BUILD_ROOT%{_includedir}/orbit-2.0/orbit
cp ${RPM_BUILD_DIR}/%{name}-%{version}/orbit-config-ppc32.h $RPM_BUILD_ROOT%{_includedir}/orbit-2.0/orbit
cp %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/orbit-2.0/orbit
chmod 644 $RPM_BUILD_ROOT%{_includedir}/orbit-2.0/orbit/*.h

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  ${RM} -r ${RPM_BUILD_ROOT}/usr/lib/orbit-2.0
  mkdir -p usr/lib/orbit-2.0
  cd usr/lib/orbit-2.0
  ln -sf ../../..%{_prefix}/lib/orbit-2.0/* .

  cd ${RPM_BUILD_ROOT}
  for dir in orbit-2.0/ORBitservices orbit-2.0/orbit orbit-2.0/orbit-idl
  do
    mkdir -p usr/include/${dir}
    cd usr/include/${dir}
    ln -sf ../../../..%{_prefix}/include/${dir}/*.h .
    cd -
  done
  for dir in orbit-2.0/orbit/dynamic orbit-2.0/orbit/orb-core orbit-2.0/orbit/poa orbit-2.0/orbit/util
  do
    mkdir -p usr/include/${dir}
    cd usr/include/${dir}
    ln -sf ../../../../..%{_prefix}/include/${dir}/*.h .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*
%dir %{_libdir}/orbit-2.0/
%{_libdir}/orbit-2.0/*.so
%{_libdir}/orbit-2.0/*.a
%{_bindir}/linc-cleanup-sockets
/usr/bin/linc-cleanup-sockets
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib/orbit-2.0/*.a
/usr/lib/orbit-2.0/*.so

%files devel
%defattr(-,root,system)
%{_bindir}/orbit-idl-2
%{_bindir}/typelib-dump
%{_bindir}/orbit2-config
%{_bindir}/ior-decode-2
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_includedir}/orbit-2.0/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc/html/ORBit2
/usr/bin/orbit-idl-2
/usr/bin/typelib-dump
/usr/bin/orbit2-config
/usr/bin/ior-decode-2
/usr/lib/*.la
/usr/lib/orbit-2.0/*.la
/usr/include/orbit-2.0/*

%changelog
* Fri Jul 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> 0.8.14-1
- Initial port on Aix6.1
