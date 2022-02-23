# avec test : /usr/bin/rpm -ba                             $SPECS/gmp....spec   2>&1  | tee   $SPECS/gmp....spec.res
# sans tests: /usr/bin/rpm -ba   --define dotests=0        $SPECS/gmp....spec   2>&1  | tee   $SPECS/gmp....spec.res

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define _libdir64 %{_prefix}/lib64

Summary: A GNU arbitrary precision library
Name: gmp
Version: 6.1.1
Release: 1
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.xz.sig
Source2: gmp.h
Source3: lib%{name}.so.3-aix32
Source4: lib%{name}.so.3-aix64
Source5: %{name}-%{version}-%{release}.build.log
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
assembly code for many CPUs most common inner loops, and it generally
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
echo "DO_TESTS=%{DO_TESTS}"
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
%setup -q -n %{name}-%{version}

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar -X32_64"
export RM="rm -f"

export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash

export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_ALL_SOURCE -DFUNCPROTO=15 -O3 -I/opt/freeware/include"
export CXXFLAGS="${CFLAGS}"


echo ********  64bit   **********

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CC="gcc -maix64"
export CXX="g++ -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --enable-cxx \
    ABI=mode64

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


echo ********  32bit   **********

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

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

echo **********************************************************************


%install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar"
export RM="rm -f"

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
    $AR -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    $AR -X32 -x ${f}
  done
)

echo "%{name}   10"  >  input.lib.$$.tmp
echo "%{name}xx  4"  >> input.lib.$$.tmp

cat input.lib.$$.tmp | while read lib number pad;
  do
# add the 64-bit shared object to the shared library containing already the
# 32-bit shared object
    $AR -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
    $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a lib"$lib".so.$number
    (
# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
        $RM ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
        cd  ${RPM_BUILD_ROOT}%{_libdir64}
        ln -s ../lib/lib"$lib".a lib"$lib".a
    )
  done
rm -f input.lib.$$.tmp

# Add the older pre-5.0.1 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} lib%{name}.so.3
/usr/bin/strip -X32 -e lib%{name}.so.3
$AR -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.3

cp %{SOURCE4} lib%{name}.so.3
/usr/bin/strip -X64 -e lib%{name}.so.3
$AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.3

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
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
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
* Mon Aug 22 2016 Jean Girardet <Jean.Girardet@atos.net> - 6.1.1-1
- Update to version 6.1.1

* Fri Apr 01 2016 Maximilien Faure <maximilien.faure@atos.net> - 6.1.0-4
- Fixes for ar and 32/64 bits

* Wed Mar 30 2016 Maximilien Faure <maximilien.faure@atos.net> - 6.1.0-1
- Compiling using GCC of version 6.1.0 with 64bits library.

* Thu Aug 06 2015 Hamza Sellami <hamza.sellami@atos.net> - 6.0.0-1
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
