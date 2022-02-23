Name:           dbus-1
Summary:        D-Bus Message Bus System
Version:        1.6.2
Release:        1
License:        Other uncritical OpenSource License
Group:          System/Daemons
Url:            http://dbus.freedesktop.org/
Source0:        dbus-%{version}.tar.gz
Source1:        rc.boot.dbus
Source2:        dbus-1.desktop
Source3:        dbus_at_console.ck
Source4:        baselibs.conf
Patch0:         dbus-%{version}-aix.patch
#BuildRequires:  doxygen libexpat-devel libzio pkgconfig
#BuildRequires:  audit-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root


%package -n dbus-1-devel
License:        Other uncritical OpenSource License
Summary:        Developer package for D-Bus
Requires:       %{name} = %{version}
Group:          Development/Libraries/Other

%package -n dbus-1-devel-doc
License:        Other uncritical OpenSource License
Summary:        Developer documentation package for D-Bus
Requires:       %{name} = %{version}
Group:          Development/Libraries/Other
#AutoReqProv:    on
#%if 0%{?suse_version} >= 1120
#BuildArch:      noarch
#%endif

%description
D-Bus is a message bus system, a simple way for applications to talk to
one another. D-Bus supplies both a system daemon and a
per-user-login-session daemon. Also, the message bus is built on top of
a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message
bus daemon).

%description -n dbus-1-devel
D-Bus is a message bus system, a simple way for applications to talk to
one another. D-Bus supplies both a system daemon and a
per-user-login-session daemon. Also, the message bus is built on top of
a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message
bus daemon).

%description -n dbus-1-devel-doc
D-Bus is a message bus system, a simple way for applications to talk to
one another. D-BUS supplies both a system daemon and a
per-user-login-session daemon. Also, the message bus is built on top of
a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message
bus daemon).


%prep
%setup -n dbus-%{version} -q
%patch0 -p1 -b .aix
#%patch1 -p1

sed -e "s;<sys/fcntl.h>;<fcntl.h>;" ./dbus/sd-daemon.c > ./dbus/sd-daemon.c.tmp
mv ./dbus/sd-daemon.c.tmp ./dbus/sd-daemon.c

awk "{  print \$0
        i=match(\$0,/^#include <syslog.h>/) ;
          if ( i != 0 ) {
             print \"\"
             print \"/* # vsyslog doesn't exist on Aix platform */\"
	     print \"#ifndef HAVE_VSYSLOG\"
	     print \"void\"
	     print \"vsyslog(int priority, const char *format, va_list args)\"
	     print \"{\"
	     print \"  char buf[1024];\"
	     print \"  vsnprintf(buf, sizeof(buf), format, args);\"
	     print \"  syslog(priority, \\\"%s\\\", buf);\"
	     print \"}\"
	     print \"#endif\"
          }
     }" dbus/dbus-sysdeps-util-unix.c >dbus/dbus-sysdeps-util-unix.c.tmp
[ -s dbus/dbus-sysdeps-util-unix.c.tmp ] && mv dbus/dbus-sysdeps-util-unix.c.tmp dbus/dbus-sysdeps-util-unix.c




%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vac/bin/xlC_r -q64"

CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libexecdir=%{_libdir} \
	--libdir=%{_libdir} \
	--disable-silent-rules \
	--disable-static \
	--enable-shared

make

cp ./dbus/.libs/libdbus-1.so.3 .
cp ./dbus/.libs/libdbus-internal.a .
cp ./test/.libs/libdbus-testutils.a .

make distclean


# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vac/bin/xlC_r"

CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
CPPFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libexecdir=%{_libdir} \
	--libdir=%{_libdir} \
	--disable-silent-rules \
	--disable-static \
	--enable-shared
make 

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ./dbus/.libs/libdbus-1.a ./libdbus-1.so.3
mkdir tmp
cd tmp
ar -X64 -t ../libdbus-internal.a >listobj64
ar -X64 -x  ../libdbus-internal.a
for file in $(cat listobj64); do
    ar -X32_64 -q ../dbus/.libs/libdbus-internal.a ${file}
done
rm -f *
ar -X64 -t ../libdbus-testutils.a >listobj64
ar -X64 -x  ../libdbus-testutils.a
for file in $(cat listobj64); do
    ar -X32_64 -q ../test/.libs/libdbus-testutils.a ${file}
done

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

chmod a-x AUTHORS COPYING HACKING NEWS README doc/*.txt doc/file-boilerplate.c doc/TODO

mkdir -p ${RPM_BUILD_ROOT}/%{_datadir}/dbus-1/interfaces
touch ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/dbus/machine-id

cp ${RPM_BUILD_DIR}/dbus-%{version}/dbus/.libs/libdbus-1.so.3 ${RPM_BUILD_ROOT}%{_libdir}/
cp ${RPM_BUILD_DIR}/dbus-%{version}/dbus/.libs/libdbus-internal.a ${RPM_BUILD_ROOT}%{_libdir}/
cp ${RPM_BUILD_DIR}/dbus-%{version}/dbus/libdbus-internal.la ${RPM_BUILD_ROOT}%{_libdir}/
cp ${RPM_BUILD_DIR}/dbus-%{version}/test/.libs/libdbus-testutils.a ${RPM_BUILD_ROOT}%{_libdir}/
cp ${RPM_BUILD_DIR}/dbus-%{version}/test/libdbus-testutils.la ${RPM_BUILD_ROOT}%{_libdir}/

cp ${RPM_BUILD_DIR}/dbus-%{version}/test/data/valid-config-files/session.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/dbus-1
cp ${RPM_BUILD_DIR}/dbus-%{version}/test/data/valid-config-files/system.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/dbus-1

cp ${RPM_BUILD_DIR}/dbus-%{version}/bus/dbus.service ${RPM_BUILD_ROOT}%{_sysconfdir}/dbus-1
cp ${RPM_BUILD_DIR}/dbus-%{version}/bus/dbus.socket ${RPM_BUILD_ROOT}%{_sysconfdir}/dbus-1

cp ${RPM_BUILD_DIR}/dbus-%{version}/dbus/dbus-arch-deps.h ${RPM_BUILD_ROOT}%{_includedir}/dbus-1.0/dbus

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}
cp ${RPM_BUILD_DIR}/dbus-%{version}/doc/file-boilerplate.c ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/
cp ${RPM_BUILD_DIR}/dbus-%{version}/doc/dcop-howto.txt ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p  usr/include/dbus-1.0/dbus
  cd  usr/include/dbus-1.0/dbus
  ln -sf ../../../..%{_prefix}/include/dbus-1.0/dbus/* .
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, system)
%doc AUTHORS COPYING HACKING NEWS README
%{_datadir}/doc/dbus/*
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/dbus-1/system-services
%dir %{_datadir}/dbus-1/interfaces
%dir %{_localstatedir}/lib/dbus
%dir %{_sysconfdir}/dbus-1
%dir %{_sysconfdir}/dbus-1/session.d
%dir %{_sysconfdir}/dbus-1/system.d
%config(noreplace) %{_sysconfdir}/dbus-1/session.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.conf
%{_bindir}/*
#%{_sysconfdir}/init.d/dbus
#%{_sysconfdir}/ConsoleKit
%{_libdir}/libdbus-1.so*
%{_libdir}/libdbus*.a
#%{_libdir}/dbus-daemon-launch-helper
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,messabus) %{_libdir}/dbus-daemon-launch-helper
%{_datadir}/man/man1/*
#%{_sbindir}/rcdbus
#%verify(not mode) /lib/%{name}/dbus-daemon-launch-helper
%ghost %{_localstatedir}/run/dbus
%ghost %{_localstatedir}/lib/dbus/machine-id
#%dir /lib/systemd
#%dir /lib/systemd/system
#/lib/systemd/system/dbus.service
#/lib/systemd/system/dbus.socket
%{_sysconfdir}/dbus-1/dbus.service
%{_sysconfdir}/dbus-1/dbus.socket
#%dir /lib/systemd/system/dbus.target.wants
#/lib/systemd/system/dbus.target.wants/dbus.socket
#%dir /lib/systemd/system/multi-user.target.wants
#/lib/systemd/system/multi-user.target.wants/dbus.service
#%dir /lib/systemd/system/sockets.target.wants
#/lib/systemd/system/sockets.target.wants/dbus.socket
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*


%files -n dbus-1-devel
%defattr(-,root,system)
%{_includedir}/dbus-1.0/dbus/*
/usr/include/dbus-1.0/dbus/*
%{_libdir}/libdbus*.la
%dir %{_libdir}/dbus-1.0
%{_libdir}/dbus-1.0/include
%{_libdir}/pkgconfig/dbus-1.pc

%files -n dbus-1-devel-doc
%defattr(-,root,sytrem)
%doc doc/dcop-howto.txt doc/file-boilerplate.c doc/TODO
###%{_datadir}/susehelp

%changelog
* Fri Jul 13 2012 Gerard Visiedo <gerard.visiedo@bull.net> -0.98-1
- Inital port on Aix6.1
