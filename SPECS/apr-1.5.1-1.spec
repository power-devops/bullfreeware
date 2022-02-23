%define aprver 1

Summary: Apache Portable Runtime library
Name: apr
Version: 1.5.1
Release: 1
License: Apache Software License
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Source1: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.asc
Source2: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2.md5
Source3: %{name}.h
Patch0: %{name}-%{version}-aixconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%ifos aix5.1
BuildRequires: prngd
Requires: prngd
Requires: AIX-rpm < 5.2.0.0
%else
Requires: AIX-rpm >= 5.2.0.0
%endif
BuildRequires: bash
Requires: bash

%define _libdir64 %{_prefix}/lib64

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

The library is available as 32-bit and 64-bit.


%package devel
Group: Development/Libraries
Summary: APR library development kit
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0 -p1 -b .aixconf

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"

export CC="/usr/vac/bin/xlc_r -D_LARGE_FILES"
#export CC="cc"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static \
%ifos aix5.1
    --with-egd=/dev/egd-pool \
%endif
    --with-installbuilddir=%{_libdir64}/%{name}-%{aprver}/build
make %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
%ifos aix5.1
    --with-egd=/dev/egd-pool \
%endif
    --with-installbuilddir=%{_libdir}/%{name}-%{aprver}/build
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}-ppc64.h 

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}-ppc32.h 

cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h

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
%doc 32bit/docs/APRDesign.html 32bit/docs/canonical_filenames.html
%doc 32bit/docs/incomplete_types 32bit/docs/non_apr_programs
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir64}/*.a
%{_libdir64}/*.la
%{_libdir}/%{name}.exp
%{_libdir64}/%{name}.exp
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_libdir}/%{name}-%{aprver}
%{_libdir64}/%{name}-%{aprver}
/usr/bin/*
/usr/include/*
/usr/lib/*.a
/usr/lib/*.la
/usr/lib64/*.a
/usr/lib64/*.la


%changelog
* Tue Dec 09 2014 Gerard Visiedo <Gerard.Visiedo@bull;net> 1.5.1-1
-  Update to version 1.5.1

* Tue Jul 24 2012 Patricia Cugny <Patricia.Cugny@bull.net> 1.4.6-1
-  Update to version 1.4.6

* Tue Mar 27 2012 Gerard Visiedo <Gerard.Visiedo@bull.net> 1.3.9-3
- Add .pc file into apr-devel package

* Thu Feb 17 2011 Gerard Visiedo <Gerard.Visiedo@bull;net> 1.3.9-2
- Add patch for aix6.1

* Wed Jan 20 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.3.9
- Update to version 1.3.9

* Fri Jul 31 2009 BULL 1.3.7
- Fisrt port for AIX
