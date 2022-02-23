Summary: C-based HTTP client library built upon the Apache APR library.
Name: serf
Version: 1.2.1
Release: 2
License: Apache License 2.0
Group: 	Applications/Databases
URL: http://code.google.com/p/serf/
Source0: http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: apr-devel >= 1.3.12
BuildRequires: apr-util-devel >= 1.3.10
BuildRequires: db-devel >= 4.7.25-2
BuildRequires: make
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: zlib-devel >= 1.2.3-3

Requires: apr >= 1.3.12
Requires: apr-util >= 1.3.10
Requires: db >= 4.7.25-2
Requires: openssl >= 1.0.1
Requires: zlib >= 1.2.3-3

%define _libdir64 %{_prefix}/lib64

%description
The serf library is a C-based HTTP client library built upon the Apache 
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations
are kept to a minimum to provide high performance operation.


%package devel
Summary: Header files and libraries for developing apps which use serf.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config, apr-devel >= 1.3.12, apr-util-devel >= 1.3.9

%description devel
The serf-devel package contains the header files and libraries needed
to develop programs that use the serf HTTP client library.


%prep
%setup -q
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r -qcpluscmt"

cd 64bit
# first build the 64-bit version 
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64}
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version 
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix}
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

# add AIX-style libraries
/usr/bin/rm -f ${RPM_BUILD_ROOT}%{_libdir}/libserf-1.a
/usr/bin/ar -X32 -rv ${RPM_BUILD_ROOT}%{_libdir}/libserf-1.a ${RPM_BUILD_ROOT}%{_libdir}/libserf-1.so.0.0.0
/usr/bin/ar -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/libserf-1.a ${RPM_BUILD_ROOT}%{_libdir64}/libserf-1.so.0.0.0

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
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%doc 32bit/design-guide.txt
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Mon Jul 08 2013 Gerard Visiedo <gerard.visiedo@bull.net>  1.2.1-2
- Initial port on Aix6.1

* Wed Jun 19 2013 Michael Perzl <michael@perzl.org> - 1.2.1-1
- update to version 1.2.1

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 1.2.0-1
- update to version 1.2.0

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.1.1-1
- update to version 1.1.1

* Mon Jun 18 2012 Michael Perzl <michael@perzl.org> - 1.1.0-1
- update to version 1.1.0

* Mon Jun 18 2012 Michael Perzl <michael@perzl.org> - 1.0.3-1
- update to version 1.0.3

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 1.0.0-1
- update to version 1.0.0

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 0.7.2-1
- update to version 0.7.2

* Thu Dec 03 2010 Michael Perzl <michael@perzl.org> - 0.7.0-1
- update to version 0.7.0, added 64-bit library

* Tue Dec 18 2007 Michael Perzl <michael@perzl.org> - 0.1.2-1
- first version for AIX5L v5.1 and higher
