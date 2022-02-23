# rpm -ba --define 'dotests 0' mpfr.....spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 3.1.4
Release: 1
URL: http://www.mpfr.org/
Source0: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.xz
#Source1: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.asc
#Source2: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.sig
Source3: libmpfr.so.1-aix32
Source4: libmpfr.so.1-aix64
#Patch1: %{name}-%{version}-allpatches.patch
License: LGPLv2+ and GPLv2+ and GFDL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gmp-devel >= 4.2.1, patch
Requires: gmp >= 4.2.1

%define _libdir64 %{_prefix}/lib64

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

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/



%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

export CC=" /opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"

export CFLAGS='-O2 '


# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CFLAGS64="-maix64"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

CC="$CC $CFLAGS $CFLAGS64" \
./configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--libdir=%{_libdir64} \
	--enable-shared	\
	--disable-static \
	--disable-assert

gmake -j4 %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
	(gmake -k check || true)
fi


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CFLAGS32="-maix32"

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

CC="$CC $CFLAGS $CFLAGS32" \
./configure	\
 	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--libdir=%{_libdir} \
	--enable-shared \
	--disable-static \
	--disable-assert

gmake -j4 %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
	(gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

cd 64bit
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
make DESTDIR=${RPM_BUILD_ROOT} install


# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
(
    cd                  ${RPM_BUILD_ROOT}%{_libdir64}
    /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libmpfr.a                              libmpfr.so.4
)
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libmpfr.a  ${RPM_BUILD_ROOT}%{_libdir64}/libmpfr.so.4


# Add the older v2.4.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3}                                                lib%{name}.so.1
/usr/bin/strip -X32 -e                                       lib%{name}.so.1
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libmpfr.a lib%{name}.so.1

cp %{SOURCE4}                                                lib%{name}.so.1
/usr/bin/strip -X64 -e                                       lib%{name}.so.1
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libmpfr.a lib%{name}.so.1


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
%doc 32bit/COPYING 32bit/COPYING.LESSER 32bit/NEWS 32bit/README 32bit/INSTALL
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
* Tue May 31 2016  ATOS Tony Reix <tony.reix@atos.net> - 3.1.2-4
- Fix issue with missing libmpfr.so.4 in 64bits and libmpfr.so.4 appearing 2 times in 32bits

* Mon Feb 16 2015  BULL Hamza Sellami <hamza.sellami@bull.net>
- Rebuild(BoosTrapped) with the new gcc compiler 4.8.3 

* Mon Dec 15 2014  BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-2
- Rebuild with gcc compiler 4.8.2

* Wed Oct 23 2013 BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-1
- Update to version 3.1.2 and built on Aix6.1

* Tue Apr 19 2011 BULL Patricia Cugny <patricia.cugny@bull.net> - 3.0.1-1
- initial version on AIX 5.3
