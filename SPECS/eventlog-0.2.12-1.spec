Name:           eventlog
Version:        0.2.12
Release:        1
Summary:        Syslog-ng v2 support library

Group:          System Environment/Libraries
License:        BSD
Url:            http://www.balabit.com/products/syslog-ng/
Source0:        http://www.balabit.com/downloads/syslog-ng/2.0/src/%{name}_%{version}.tar.gz
Source1:        http://www.balabit.com/downloads/syslog-ng/2.0/src/%{name}_%{version}.dsc
Patch0:		%{name}_%{version}-aix.patch
BuildRoot:      /var/tmp/%{name}-%{version}-%{release}-root

%description
The EventLog library aims to be a replacement of the simple syslog() API
provided on UNIX systems. The major difference between EventLog and syslog
is that EventLog tries to add structure to messages.

EventLog provides an interface to build, format and output an event record.
The exact format and output method can be customized by the administrator
via a configuration file.

This package is the runtime part of the library.

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Syslog-ng v2 support library development files
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The EventLog library aims to be a replacement of the simple syslog() API
provided on UNIX systems. The major difference between EventLog and syslog
is that EventLog tries to add structure to messages.

EventLog provides an interface to build, format and output an event record.
The exact format and output method can be customized by the administrator
via a configuration file.

This package contains the development files.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0 -p1 -b .aix

# xlc doesn't like the "-Wall" option, so remove it from configure
cat configure | sed -e "s| -Wall -g||" > configure.tmp
mv configure.tmp configure
chmod 755 configure

%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix}
make

cp src/.libs/libevtlog.so.0 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix}
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libevtlog.a ./libevtlog.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
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
%doc AUTHORS ChangeLog COPYING CREDITS NEWS README
%{_libdir}/libevtlog.a
/usr/lib/libevtlog.a


%files devel
%defattr(-,root,system,-)
%doc doc/*
%{_includedir}/%{name}
%{_libdir}/libevtlog.la
%{_libdir}/pkgconfig/%{name}.pc
/usr/include/%{name}
/usr/lib/libevtlog.la


%changelog
* Wed Jan 04 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.2.12-1
- Initial port on Aix5.3

