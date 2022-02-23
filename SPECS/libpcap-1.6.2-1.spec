Name: libpcap
Version: 1.6.2
# Since version 4.7.4/1.7.4 of tcpdump/libpcap has 38 FAILED tests out
# of 165 tests, both on AIX and on Ubuntu/Intel, master of 2016 March 11th
# is used instead, waiting for official 4.7.5/1.7.5 .
Release: 1
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD
URL: http://www.tcpdump.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
#Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig
Source2: %{name}.so.0.9.8-aix32
Source3: %{name}.so.0.9.8-aix64

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
#export CC="cc -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export CC="cc -qcpluscmt -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export AR="/usr/bin/ar -X32_64"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-ipv6 \
    --with-pcap=bpf
make %{?_smp_mflags}

mv shr.o shr_64.o
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-ipv6 \
    --with-pcap=bpf
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# hack to generate AIX-style shared libraries
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a
/usr/bin/ar -X32 -rv ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr.o
/usr/bin/ar -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a shr_64.o

# Add the older 0.9.8 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} %{name}.so.0.9.8
/usr/bin/strip -X32 -e %{name}.so.0.9.8
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0.9.8

cp %{SOURCE3} %{name}.so.0.9.8
/usr/bin/strip -X64 -e %{name}.so.0.9.8
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.0.9.8

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
* Tue Jan 19 2016 Tony Reix <tony.reix@atos.net - 4.7.4-1
- updated to version 4.7.4

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 1.6.2-1
- updated to version 1.6.2

* Wed Aug 13 2014 Michael Perzl <michael@perzl.org> - 1.6.1-1
- updated to version 1.6.1

* Mon Jan 20 2014 Michael Perzl <michael@perzl.org> - 1.5.3-1
- updated to version 1.5.3

* Thu Nov 28 2013 Michael Perzl <michael@perzl.org> - 1.5.1-1
- updated to version 1.5.1

* Wed Jun 26 2013 Michael Perzl <michael@perzl.org> - 1.4.0-1
- updated to version 1.4.0

* Tue Apr 30 2013 Michael Perzl <michael@perzl.org> - 1.3.0-2
- enabled IPV6

* Mon Jun 25 2012 Michael Perzl <michael@perzl.org> - 1.3.0-1
- updated to version 1.3.0

* Sat Jan 28 2012 Michael Perzl <michael@perzl.org> - 1.2.1-1
- updated to version 1.2.1

* Mon Nov 28 2011 Michael Perzl <michael@perzl.org> - 1.2.0-1
- updated to version 1.2.0
- added symbolic links to /usr/linux

* Tue Apr 13 2010 Michael Perzl <michael@perzl.org> - 1.1.1-1
- updated to version 1.1.1

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 0.9.8-2
- included both 32-bit and 64-bit shared objects

* Tue Oct 16 2007 Michael Perzl <michael@perzl.org> - 0.9.8-1
- first version for AIX V5.1 and higher
