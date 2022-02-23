Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 3.1.2
Release: 3
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2
Source1: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.asc
Source2: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.sig
Source3: libmpfr.so.1-aix32
Source4: libmpfr.so.1-aix64
#Patch1: %{name}-%{version}-allpatches.patch
License: LGPLv2+ and GPLv2+ and GFDL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gmp-devel >= 4.2.1, patch
Requires: gmp >= 4.2.1

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and 
also has a well-defined semantics. It copies the good ideas from the 
ANSI/IEEE-754 standard for double-precision floating-point arithmetic 
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development tools A C library for mpfr library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: info
Requires: /sbin/install-info

%description devel
The static libraries, header files and documentation for using the MPFR 
multiple-precision floating-point library in applications.

If you want to develop applications which will use the MPFR library,
you'll need to install the mpfr-devel package.  You'll also need to
install the mpfr package.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
##%patch1 -p1


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"
export CC="/home/gnu/gcc482/bin/gcc"
export CXX="/home/gnu/gcc482/bin/g++"
## Use the default compiler for this platform - gcc otherwise
#if [[ -z "$CC" ]]
#then
#    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
#       export CC=%{DEFCC}
#    else
#       export CC=gcc
#    fi
#fi
#if [[ "$CC" != "gcc" ]]
#then
#       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
#        export CFLAGS64="-q64"
#else
#        export CFLAGS64="-I/home/gnu/gcc482/include -maix64"
#fi
#export CFLAGS=$RPM_OPT_FLAGS
export CFLAGS='-O2 '
export CFLAGS64="-I/home/gnu/gcc482/include -maix64"
export LDFLAGS="-L/home/gnu/gcc482/lib"

# first build the 64-bit version
CC="$CC $CFLAGS $CFLAGS64" \
./configure \
	CC="/home/gnu/gcc482/bin/gcc" \
	CXX="/home/gnu/gcc482/bin/g++" \
    --prefix=%{_prefix} \
    --libdir=/home/gnu/gcc482/lib \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-assert
make %{?_smp_mflags}

cp src/.libs/libmpfr.so.4 .
make distclean

# now build the 32-bit version
CC="$CC $CFLAGS" \
./configure 	--prefix=%{_prefix} \
		--infodir=%{_infodir} \
		--enable-shared \
		--disable-static \
		--disable-assert
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libmpfr.a ./libmpfr.so.4

## ??? # add the 64-bit shared objects to the shared library containing already the
## ??? # 32-bit shared objects
## ??? ${AR} -q src/.libs/libmpfr.a ./libmpfr.so.4

# Add the older v2.4.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} lib%{name}.so.1
/usr/bin/strip -X32 -e lib%{name}.so.1
/usr/bin/ar -X32 -q src/.libs/lib%{name}.a lib%{name}.so.1

cp %{SOURCE4} lib%{name}.so.1
/usr/bin/strip -X64 -e lib%{name}.so.1
/usr/bin/ar -X64 -q src/.libs/lib%{name}.a lib%{name}.so.1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/mpfr.info

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
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 -eq 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc COPYING COPYING.LESSER NEWS README INSTALL
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_libdir}/*.la
%{_includedir}/*.h
%{_infodir}/mpfr.info*
%{_datadir}/doc/%{name}
/usr/lib/*.la
/usr/include/*

%changelog
* Mon Feb 16 2015  BULL Hamza Sellami <hamza.sellami@bull.net>
- Rebuild(BoosTrapped) with the new gcc compiler 4.8.3 

* Mon Dec 15 2014  BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-2
- Rebuild with gcc compiler 4.8.2

* Wed Oct 23 2013 BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-1
- Update to version 3.1.2 and built on Aix6.1

* Tue Apr 19 2011 BULL Patricia Cugny <patricia.cugny@bull.net> - 3.0.1-1
- initial version on AIX 5.3
