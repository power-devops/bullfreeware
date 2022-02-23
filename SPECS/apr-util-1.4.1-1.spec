%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.4.1
Release: 1
License: Apache Software License 2.0
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Source1: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.asc
Source2: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.md5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%define _libdir64 %{_prefix}/lib64

BuildRequires: apr-devel >= 1.4.0
BuildRequires: expat-devel >= 2.0.0
BuildRequires: freetds-devel >= 0.82
BuildRequires: pkg-config
BuildRequires: sqlite-devel >= 3.6.23.1
BuildRequires: unixODBC-devel >= 2.2.14
Requires: apr >= 1.3.12
Requires: expat >= 2.0.0
Requires: freetds >= 0.82
Requires: sqlite >= 3.6.23.1
Requires: unixODBC >= 2.2.14

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.


%package devel
Group: Development/Libraries
Summary: APR utility library development kit
Requires: %{name} = %{version}-%{release}
Requires: apr-devel >= 1.4.0
Requires: expat-devel >= 2.0.0
Requires: freetds-devel >= 0.82
Requires: pkg-config
Requires: sqlite-devel >= 3.6.23.1
Requires: unixODBC-devel >= 2.2.14

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.


%prep
%setup -q
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
CC_prev="$CC"
export CC="$CC -q64"
export NM="/usr/bin/nm -X32_64"
export AR="/usr/bin/ar -X32_64"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
autoheader && autoconf
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --with-berkeley-db=%{_prefix} \
    --with-apr=%{_bindir}/apr-1-config_64 \
    --includedir=%{_includedir}/apr-%{apuver}
make %{?_smp_mflags}

cd ../32bit
# now build he 32-bit version
export CC="$CC_prev"
autoheader && autoconf
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --with-apr=%{_bindir}/apr-1-config \
    --with-berkeley-db=%{_prefix} \
    --includedir=%{_includedir}/apr-%{apuver}
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
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
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/apr-util-%{apuver}
%{_libdir64}/apr-util-%{apuver}
%{_libdir}/aprutil.exp
%{_libdir64}/aprutil.exp
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/bin/*
/usr/include/*
/usr/lib/*.a
/usr/lib64/*.a
/usr/lib/*.la
/usr/lib64/*.la
/usr/lib/apr-util-%{apuver}
/usr/lib64/apr-util-%{apuver}


%changelog
* Mon Jul 04 2011 Gerard Visiedo <Gerard.Visiedo@bull.net> 1.3.9-4
- Compile module with db4

* Thu Jun 23 2011 Gerard Visiedo <Gerard.Visiedo@bull.net> 1.3.9-3
- Compile libraries on 32 and 64 bits

* Thu Jan 21 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.3.9
- Initial port for AIX
