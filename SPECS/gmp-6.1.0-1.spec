%define _libdir64 %{_prefix}/lib64

Summary: A GNU arbitrary precision library
Name: gmp
Version: 6.1.0
Release: 1
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.xz.sig
Source2: gmp.h
Source3: libgmp.so.3-aix32
Source4: libgmp.so.3-aix64
License: LGPL 
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc >= 4.2.3-2
BuildRequires: gcc-c++ >= 4.2.3-2
BuildRequires: libstdc++-devel >= 4.2.3-2
Requires: libgcc >= 4.2.3-2
Requires: libstdc++ >= 4.2.3-2

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development tools for the GNU MP arbitrary precision library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: info
Requires: /sbin/install-info

%description devel
The static libraries, header files and documentation for using the GNU
MP arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
%setup -q -n %{name}-%{version}
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export AR="ar -X32_64"
export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash
export RM="rm -f"
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_ALL_SOURCE -DFUNCPROTO=15 -O3 -I/opt/freeware/include"
export CXXFLAGS="${CFLAGS}"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"
export CXX="g++ -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --enable-cxx \
    ABI=mode64

gmake %{?_smp_mflags}

gmake check

echo ******************

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CC="gcc -maix32 "
export CXX="g++ -maix32 "
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --enable-cxx \
    ABI=32

gmake %{?_smp_mflags}

gmake check

echo **********************************************************************

%install
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/home/faurem/bin:/usr/bin/X11:/sbin:.
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    ar -X32 -x ${f}
  done
)

# add the 64-bit shared object to the shared library containing already the
# 32-bit shared object
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a 64bit/.libs/libgmp.so.10

# Add the older pre-5.0.1 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} libgmp.so.3
/usr/bin/strip -X32 -e libgmp.so.3
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a libgmp.so.3

cp %{SOURCE4} libgmp.so.3
/usr/bin/strip -X64 -e libgmp.so.3
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a libgmp.so.3

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gmp.info*

cp 32bit/gmp.h ${RPM_BUILD_ROOT}%{_includedir}/gmp-ppc32.h
cp 64bit/gmp.h ${RPM_BUILD_ROOT}%{_includedir}/gmp-ppc64.h
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_includedir}/
chmod 644 ${RPM_BUILD_ROOT}%{_includedir}/*.h

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


%post devel
/sbin/install-info %{_infodir}/gmp.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 -eq 0 ]; then
    /sbin/install-info --delete %{_infodir}/gmp.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
#%doc 32bit/COPYING 32bit/COPYING.LIB 32bit/NEWS 32bit/README
%doc 32bit/COPYING 32bit/NEWS 32bit/README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir64}/*.la
%{_infodir}/gmp.info*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Thu Aug 06 2015 Hamza Sellami <hamza.sellami@atos.net>
- Compiling using GCC of version 6.0.0

* Tue Mar 25 2014 Michael Perzl <michael@perzl.org> - 6.0.0a-1
- updated to version 6.0.0a

* Wed Nov 13 2013 Michael Perzl <michael@perzl.org> - 5.1.3-1
- updated to version 5.1.3

* Tue May 21 2013 Michael Perzl <michael@perzl.org> - 5.1.2-1
- updated to version 5.1.2

* Mon Feb 18 2013 Michael Perzl <michael@perzl.org> - 5.1.1-1
- updated to version 5.1.1

* Sat Feb 02 2013 Michael Perzl <michael@perzl.org> - 5.1.0a-1
- updated to version 5.1.0a

* Sun May 06 2012 Michael Perzl <michael@perzl.org> - 5.0.5-1
- updated to version 5.0.5

* Fri Feb 10 2012 Michael Perzl <michael@perzl.org> - 5.0.4-1
- updated to version 5.0.4

* Fri Jan 27 2012 Michael Perzl <michael@perzl.org> - 5.0.3-1
- updated to version 5.0.3

* Mon May 09 2011 Michael Perzl <michael@perzl.org> - 5.0.2-1
- updated to version 5.0.2

* Fri Apr 29 2011 Michael Perzl <michael@perzl.org> - 5.0.1-2
- enabled the C++ interface

* Thu Feb 11 2010 Michael Perzl <michael@perzl.org> - 5.0.1-1
- updated to version 5.0.1

* Fri Jan 08 2010 Michael Perzl <michael@perzl.org> - 5.0.0-1
- updated to version 5.0.0

* Fri Jan 08 2010 Michael Perzl <michael@perzl.org> - 4.3.2-1
- updated to version 4.3.2

* Thu Jul 02 2009 Michael Perzl <michael@perzl.org> - 4.3.1-1
- updated to version 4.3.1 (version 4.3.0 can't be built on AIX)

* Fri Sep 26 2008 Michael Perzl <michael@perzl.org> - 4.2.4-1
- updated to version 4.2.4

* Thu Aug 14 2008 Michael Perzl <michael@perzl.org> - 4.2.3-1
- updated to version 4.2.3

* Wed Nov 28 2007 Michael Perzl <michael@perzl.org> - 4.2.2-1
- first version for AIX V5.1 and higher
