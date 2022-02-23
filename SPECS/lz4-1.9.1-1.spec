# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%global xlccpath	/opt/IBM/xlC/13.1.3/bin
%global optflags	-O2


Name:           lz4
Version:        1.9.1
Release:        1
Summary:        Extremely fast compression algorithm
Group:          System Environment/Libraries
License:        GPLv2+ and BSD
URL:            https://lz4.github.io/lz4/
Source0:        https://github.com/Cyan4973/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-aix.patch
# Old
#	BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  make

Source1:	%{name}-%{version}-%{release}.build.log

Patch1:		%{name}-%{version}-xlc-gcc-2.patch
Patch2:		lz4-1.9.1-test-shell.patch

%define _libdir64	%{_prefix}/lib64
%define _sharemandir	%{_prefix}/share/man

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
%patch2

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build

export PATH=/opt/freeware/bin:$PATH
export CC=gcc
export XLCCPATH=%{xlccpath}
export OPT_FLAGS=%{optflags}

echo "       CFLAGS: $CFLAGS"
echo "RPM_OPT_FLAGS: $RPM_OPT_FLAGS"
echo "    OPT_FLAGS: $OPT_FLAGS"

cd 64bit
export OBJECT_MODE=64
export CFLAGS="$OPT_FLAGS -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir64} XLCCPATH=${XLCCPATH}

cd ../32bit
export OBJECT_MODE=32
export CFLAGS="$OPT_FLAGS -maix32"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir} XLCCPATH=${XLCCPATH}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH
export CC=gcc
export XLCCPATH=%{xlccpath}
export OPT_FLAGS=%{optflags}
echo "CFLAGS: $CFLAGS"

cd 64bit
export OBJECT_MODE=64
export CFLAGS="$OPT_FLAGS -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir64} XLCCPATH=${XLCCPATH} install
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  rm lz4c unlz4 lz4cat
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
export CFLAGS="$OPT_FLAGS -maix32"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "
gmake DESTDIR=${RPM_BUILD_ROOT} PREFIX=%{_prefix} LIBDIR=%{_libdir} XLCCPATH=${XLCCPATH} install
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  rm lz4c unlz4 lz4cat
  for f in `ls | grep -v _64` ; do
    mv -f ${f} ${f}_32
  done
)

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  ln -s lz4_64 lz4
  ln -s lz4    lz4c
  ln -s lz4    lz4cat
  ln -s lz4    unlz4
)

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
# No more /usr files are delivered
#	(
#	  cd ${RPM_BUILD_ROOT}
#	  for dir in bin include lib lib64
#	  do
#	    mkdir -p usr/${dir}
#	    cd usr/${dir}
#	    for f in `ls ../..%{_prefix}/${dir} | grep -v _64 | grep -v _32` ; do
#	      ln -sf ../..%{_prefix}/${dir}/$f .
#	    done
#	    cd -
#	  done
#	)


%check

%if %{with dotests}

# Required for some read tests of large file
ulimit -f unlimited

# Required for some BullFreeware diff or grep on >131MB files
ulimit -d unlimited

export PATH=/opt/freeware/bin:$PATH
export CC=gcc
export XLCCPATH=%{xlccpath}
export OPT_FLAGS=%{optflags}

cd 64bit
export OBJECT_MODE=64
export CFLAGS="$OPT_FLAGS -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
time gmake test
# TODO
# gmake versionsTest

cd ../32bit
export OBJECT_MODE=32
export CFLAGS="$OPT_FLAGS -maix32"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "
time gmake test
# TODO
# gmake versionsTest

%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
# No more .so  files are delivered
# No more /usr files are delivered
%defattr(-,root,system)
%doc 32bit/programs/COPYING 32bit/lib/LICENSE 32bit/NEWS
%{_bindir}/*
%{_sharemandir}/man1/*
%{_libdir}/*.a
%{_libdir64}/*.a
#	%{_libdir}/*.so*
#	%{_libdir64}/*.so*
#	/usr/bin/*
#	/usr/lib/*.a
#	/usr/lib/*.so*
#	/usr/lib64/*.a
#	/usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%doc 32bit/lib/LICENSE
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
#	/usr/include/*


%changelog
* Tue Nov 26 2019 Tony Reix <tony.reix@atos.net> - 1.9.1-1
- Move to version 1.9.1
- .so and /usr files are no more delivered

* Mon Nov 25 2019 Tony Reix <tony.reix@atos.net> - 1.8.0-3
- Add running tests in %check

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
