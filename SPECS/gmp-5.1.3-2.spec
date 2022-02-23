Summary: A GNU arbitrary precision library
Name: gmp
Version: 5.1.3
Release: 2
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2.sig
Source2: gmp.h
Source3: libgmp.so.3-aix32
Source4: libgmp.so.3-aix64
Patch1: gmp-5.1.3-aix.patch
License: LGPL 
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

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
%setup -q 
%patch1 -p2

%build
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"

#export CC=/usr/vac/bin/xlc
#export CXX=/usr/vacpp/bin/xlC

export CC=/opt/freeware/bin/gcc
export CXX=/opt/freeware/bin/g++

# first build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --enable-cxx \
    ABI=32
make %{?_smp_mflags}
make check

cp .libs/libgmp.so.10 .
cp .libs/libgmpxx.so.4 .
cp gmp.h gmp-ppc32.h
make distclean

# now build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_prefix}/lib64 \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --enable-cxx \
    --host=powerpc64-ibm-aix6.1.0.0 \
    ABI=mode64
make %{?_smp_mflags}
make check

cp gmp.h gmp-ppc64.h


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
make DESTDIR=${RPM_BUILD_ROOT} install

# Since we used the lib64/ dir for building the 64 bit release, we need to move
# it back to lib/ to have the rest working
mv ${RPM_BUILD_ROOT}%{_libdir}64 ${RPM_BUILD_ROOT}%{_libdir}

# add the 32-bit shared object to the shared library containing already the
# 64-bit shared object
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a ./libgmp.so.10
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmpxx.a ./libgmpxx.so.4

# Add the older pre-5.0.1 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} libgmp.so.3
/usr/bin/strip -X32 -e libgmp.so.3
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a libgmp.so.3

cp %{SOURCE4} libgmp.so.3
/usr/bin/strip -X64 -e libgmp.so.3
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgmp.a libgmp.so.3

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gmp.info*

cp gmp-ppc??.h ${RPM_BUILD_ROOT}%{_includedir}/
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_includedir}/
chmod 644 ${RPM_BUILD_ROOT}%{_includedir}/*.h

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
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
%doc COPYING COPYING.LIB NEWS README
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_libdir}/*.la
%{_includedir}/*.h
%{_infodir}/gmp.info*
/usr/lib/*.la
/usr/include/*


%changelog
* Wed Oct 23 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.1.3-1
- Update to version 5.1.3

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 5.0.2-2
- Initial port on Aix6.1
