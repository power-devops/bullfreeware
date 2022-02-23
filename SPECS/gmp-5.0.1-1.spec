Summary: A GNU arbitrary precision library
Name: gmp
Version: 5.0.1
Release: 1
URL: http://gmplib.org/
Source0: ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.gz
Source1: gmp.h
Source2: libgmp.so.3-aix32
Source3: libgmp.so.3-aix64
License: LGPL 
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

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


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
        export CFLAGS64="-q64"
else
        export CFLAGS64="-maix64"
fi
export CFLAGS=$RPM_OPT_FLAGS

# first build the 32-bit version
CC="$CC $CFLAGS" \
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    ABI=32
make %{?_smp_mflags}

cp .libs/libgmp.so.10 .
cp gmp.h gmp-ppc32.h
make distclean

# now build the 64-bit version
CC="$CC $CFLAGS $CFLAGS64" \
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    ABI=aix64
make %{?_smp_mflags}

cp gmp.h gmp-ppc64.h

# add the 32-bit shared object to the shared library containing already the
# 64-bit shared object
ar -X32_64 -q .libs/libgmp.a ./libgmp.so.10

# Add the older pre-5.0.1 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libgmp.so.3
/usr/bin/strip -X32 -e libgmp.so.3
/usr/bin/ar -X32 -q .libs/libgmp.a libgmp.so.3

cp %{SOURCE3} libgmp.so.3
/usr/bin/strip -X64 -e libgmp.so.3
/usr/bin/ar -X64 -q .libs/libgmp.a libgmp.so.3


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gmp.info*

cp gmp-ppc??.h ${RPM_BUILD_ROOT}%{_includedir}/
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/
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
* Thu Apr 21 2011 BULL Patricia Cugny <patricia.cugny@bull.net> - 5.0.1-1
-  first version for AIX 5.3
