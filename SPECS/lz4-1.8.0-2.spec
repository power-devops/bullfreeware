Name:           lz4
Version:        1.8.0
Release:        2
Summary:        Extremely fast compression algorithm
Group:          System Environment/Libraries
License:        GPLv2+ and BSD
URL:            https://lz4.github.io/lz4/
Source0:        https://github.com/Cyan4973/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-aix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  make

Patch1:		lz4-1.8.0-xlc-gcc-2.patch

%define _libdir64 %{_prefix}/lib64

%description
LZ4 is an extremely fast loss-less compression algorithm, providing compression
speed at 400 MB/s per core, scalable with multi-core CPU. It also features
an extremely fast decoder, with speed in multiple GB/s per core, typically
reaching RAM speed limits on multi-core systems.

The library is available as 32-bit and 64-bit.


%package        devel
Summary:        Development files for lz4
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the header(.h) and library(.so) files required to build
applications using liblz4 library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc_r -q64" or "gcc -maix64".


%prep
%setup -q

%patch0
%patch1

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
# nothing to be done here, everything happens in %install


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH

export CC=gcc
export XLCCPATH=/opt/IBM/xlC/13.1.3/bin

cd 64bit
export OBJECT_MODE=64
echo "CFLAGS: $CFLAGS"
export CFLAGS="-maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir64} XLCCPATH=${XLCCPATH} install
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)


cd ../32bit
export OBJECT_MODE=32
export CFLAGS="-maix32"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir} XLCCPATH=${XLCCPATH} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Instead of lib...so.1.8.0 , lets put the same name for 32 & 64bit : lib....so.1 .
rm ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so.1

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.1

/usr/bin/strip -X32_64 -e ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so* ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.so

rm -f ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.a
# symlink of /opt/freeware/lib/... to .../lib64/
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -s ../lib/lib%{name}.a lib%{name}.a
)

# /usr symlinks
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
%doc 32bit/programs/COPYING 32bit/lib/LICENSE 32bit/NEWS
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%doc 32bit/lib/LICENSE
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/include/*


%changelog
* Mon Nov 25 2019 Tony Reix <tony.reix@atos.net> - 1.8.0-2
- Add the missing /usr/lib64/liblz4.a & /opt/freeware/lib64/liblz4.a

* Wed Apr 17 2019 Tony Reix <tony.reix@atos.net> - 1.8.0-1
- Port for BullFreeware

* Wed Nov 15 2017 Michael Perzl <michael@perzl.org> - 1.8.0-1
- updated to version 1.8.0

* Tue Jan 03 2017 Michael Perzl <michael@perzl.org> - 1.7.4.2-1
- updated to version 1.7.4.2

* Tue Dec 13 2016 Michael Perzl <michael@perzl.org> - 1.7.3-1
- first version for AIX V5.1 and higher
