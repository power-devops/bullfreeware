Name: libpcap
Version: 1.3.0
Release: 1
Summary: A system-independent interface for user-level packet capture
Group: System Environment/Libraries
License: IBM_ILA
URL: http://www.tcpdump.org
BuildRoot: /var/tmp/libpcap-%{version}-root
Prefix: %{_prefix}
Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig
Source2: %{name}-0.8.3.a

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

The library is available as 32-bit and 64-bit.


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

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

 
%prep
%setup -q


%build
export CC="/usr/vac/bin/xlc_r -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-pcap=bpf
make %{?_smp_mflags}

mv shr.o shr_64.o
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-pcap=bpf
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# hack to generate AIX-style shared libraries
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a
/usr/bin/ar -X32 -rv ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr.o
/usr/bin/ar -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr_64.o

# Add the older 0.8.3 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
mkdir tmp
cd tmp
cp %{SOURCE2} %{name}-0.8.3.a
ar -x -X32_64 %{name}-0.8.3.a
strip -X32 -e `ls *.o | grep -v _64`
strip -X64 -e `ls *.o | grep _64`
ar -r -X32_64 ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a *.o

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/lib
cd usr/linux/lib
ln -sf ../../..%{_libdir}/* .

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/include
cd usr/linux/include
ln -sf ../../..%{_includedir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc LICENSE README README.aix INSTALL.txt CHANGES CREDITS 
%{_libdir}/*.a
/usr/linux/lib/*.a

%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/man3/*
/usr/bin/*
/usr/linux/include/*


%changelog
* Tue Mar 05 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.3.0-1
- update to version 1.3.0

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
