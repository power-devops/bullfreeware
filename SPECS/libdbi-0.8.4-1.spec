Summary: Database Independent Abstraction Layer for C
Name: libdbi
Version: 0.8.4
Release: 1
Group: Development/Libraries
License: LGPLv2+
URL: http://libdbi.sourceforge.net/
Source0: http://prdownloads.sourceforge.net/libdbi/%{name}-%{version}.tar.gz
Patch0: %{name}-%{version}-aix.patch
Patch1: %{name}-%{version}-aixconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: make

%define _libdir64 %{_prefix}/lib64

%description
libdbi implements a database-independent abstraction layer in C, similar to the
DBI/DBD layer in Perl. Writing one generic set of code, programmers can
leverage the power of multiple databases and multiple simultaneous database
connections by using this framework.

The libdbi package contains just the libdbi framework.  To make use of
libdbi you will also need one or more plugins from libdbi-drivers, which
contains the plugins needed to interface to specific database servers.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development files for %{name} (Database Independent Abstraction Layer for C)
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and documentation
needed to develop applications with %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".



%prep
%setup -q
%patch0 -p1 -b .aix
%patch1 -p1 -b .aixconf

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export CC="/usr/vac/bin/xlc_r -qcpluscmt"
export RM="/usr/bin/rm -f"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64}
make

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
export AR="/usr/bin/ar -X32_64"
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so.1

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
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/COPYING 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
/usr/lib/*.a
/usr/lib/*.so*


%files devel
%defattr(-,root,system)
%doc 32bit/TODO 32bit/doc/programmers-guide.pdf 32bit/doc/driver-guide.pdf
%doc 32bit/doc/programmers-guide/ 32bit/doc/driver-guide/
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%changelog
* Mon Mar 26 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.8.4-1
- Initial port on Aix6.1
