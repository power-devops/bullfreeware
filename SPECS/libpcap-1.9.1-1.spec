%bcond_without dotests
%bcond_without cmake

%define _libdir64 %{_libdir}64
%define soversion 1

Name: libpcap
Version: 1.9.1
Release: 1
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD
URL: http://www.tcpdump.org

BuildRequires: flex >= 2.5.0
%if %{with cmake}
BuildRequires: cmake >= 3.16.0
BuildRequires: bison
%endif

# Work without dbus
#BuildRequires: dbus >= 1.11.12-1
#BuildRequires: dbus-devel >= 1.11.12-1

Requires: libgcc >= 6.3.0
#Requires: dbus >= 1.11.12-1

Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
#Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig
Source2: %{name}.so.0.9.8-aix32
Source3: %{name}.so.0.9.8-aix64
Source100: %{name}-%{version}-%{release}.build.log

#Patch0:  %{name}-1.9.0-pcapbpf-aix.patch
Patch1:  %{name}-1.9.1-cmake.patch

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.


%package devel
Summary: Libraries and header files for the libpcap library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other 
resources needed for developing libpcap applications.

 
%prep
%setup -q
#%patch0 -p0
%patch1 -p1 -b .cmake

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export AR="/usr/bin/ar -X32_64"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc"
export CXX="g++"
export CFLAGS="-maix64 -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

%if %{with cmake}
mkdir build
cd build
cmake .. -L \
    -DCMAKE_C_FLAGS="$CFLAGS" \
    -DDISABLE_DBUS=ON \
    -DCMAKE_INSTALL_MANDIR=man \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir64} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DDESTDIR=${RPM_BUILD_ROOT}
%else
./configure \
    --disable-static \
    --enable-shared \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --enable-ipv6 \
    --with-pcap=bpf
%endif

gmake %{?_smp_mflags}

%if %{with cmake}
cd ..
%else
rm libpcap.a
$AR -qc libpcap.a libpcap.so.%{soversion}
%endif

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc"
export CXX="g++"
export CFLAGS="-maix32 -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

%if %{with cmake}
mkdir build
cd build
cmake .. -L \
    -DCMAKE_C_FLAGS="$CFLAGS" \
    -DDISABLE_DBUS=ON \
    -DCMAKE_INSTALL_MANDIR=man \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DDESTDIR=${RPM_BUILD_ROOT}
%else
./configure \
    --disable-static \
    --enable-shared \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --enable-ipv6 \
    --with-pcap=bpf
%endif

gmake %{?_smp_mflags}

%if %{with cmake}
cd ..
%else
rm libpcap.a
$AR -qc libpcap.a libpcap.so.%{soversion}
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
%if %{with cmake}
cd build
%endif
make DESTDIR=${RPM_BUILD_ROOT} install
%if %{with cmake}
cd ..
%endif

cd ../32bit
export OBJECT_MODE=32
%if %{with cmake}
cd build
%endif
make DESTDIR=${RPM_BUILD_ROOT} install
%if %{with cmake}
cd ..
%endif

(
  cd ${RPM_BUILD_ROOT}/%{_libdir}
  $AR -x  ../lib64/libpcap.a libpcap.so.%{soversion}
  $AR -qc          libpcap.a libpcap.so.%{soversion}

  cp %{SOURCE2} %{name}.so.0.9.8
  /usr/bin/strip -X32 -e %{name}.so.0.9.8
  /usr/bin/ar -X32 -q %{name}.a %{name}.so.0.9.8
  
  cp %{SOURCE3} %{name}.so.0.9.8
  /usr/bin/strip -X64 -e %{name}.so.0.9.8
  /usr/bin/ar -X64 -q %{name}.a %{name}.so.0.9.8


  cd ../lib64
  rm libpcap.a
  ln -sf    ../lib/libpcap.a libpcap.a
)


%check
%if %{with dotests}
# No test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/LICENSE 32bit/README.md 32bit/INSTALL.md 32bit/CHANGES 32bit/CREDITS 
%{_libdir}/libpcap.a
%{_libdir64}/libpcap.a


%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/man3/*


%changelog
* Wed Feb 19 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.9.1-1
- BullFreeware Compatibility Improvements
- Add an empty check section (no test to do)
- New version 1.9.1-1
- Build with cmake

* Sun Nov 04 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> - 1.9.0-1
- Updated to 1.9.0
- Built with gcc

* Mon Nov 21 2016 Ravi Hirekurabar<rhirekur@in.ibm.com> 1.8.1-1
- Updated to Version 1.8.1

* Thu Apr 14 2016 Ravi Hirekurabar<rhirekur@in.ibm.com> 1.7.4
- Update to Version 1.7.4

* Thu Aug 19 2004 David Clissold <cliss@austin.ibm.com> 0.8.3-1
- Update to version 0.8.3

* Mon Jan 19 2004 David Clissold <cliss@austin.ibm.com> 0.8.1-1
- Update to version 0.8.1

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Mon Nov 05 2001 Marc Stephenson <marc@austin.ibm.com>
- Squash /usr/lib link due to conflict with bos.net.tcp.server

* Wed Jun 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Ship the include files

* Tue May 22 2001 Olof Johansson
- Added IA64 hooks

* Mon May 21 2001 Olof Johansson
- First version
