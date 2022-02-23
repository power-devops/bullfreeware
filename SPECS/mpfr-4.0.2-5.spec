%bcond_without dotests

Summary: A C library for multiple-precision floating-point computations
Name: mpfr
Version: 4.0.2
Release: 5
URL: http://www.mpfr.org/
Source0: https://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2
Source1: https://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.asc
# Source2: http://www.mpfr.org/mpfr-current/%{name}-%{version}.tar.bz2.sig
Source3: libmpfr.so.1-aix32
Source4: libmpfr.so.1-aix64
Source5: libmpfr.so.4-aix32
Source6: libmpfr.so.4-aix64
Source1000: %{name}-%{version}-%{release}.build.log


%define _libdir64 %{_prefix}/lib64

License: LGPLv2+ and GPLv2+ and GFDL
Group: System Environment/Libraries
BuildRequires: gmp-devel >= 6.2.0
BuildRequires: gzip
Requires: gmp >= 6.2.0
Requires: libgcc >= 8.3.0

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
%setup -q


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
# We are not using lib64 as gcc binaries are still 32bit and that creates problem for R package
# because it exports LIBPATH and triggers the R modules build

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="gcc -maix64 -O2"
export LDFLAGS="-L/opt/freeware/lib64 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-assert

gmake %{?_smp_mflags}


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="gcc -maix32 -O2"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static \
    --disable-assert

gmake %{?_smp_mflags}


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q src/.libs/libmpfr.a ../64bit/src/.libs/libmpfr.so.6

# Add the older v2.4.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')

cp %{SOURCE3} lib%{name}.so.1
/usr/bin/strip -X32 -e lib%{name}.so.1
/usr/bin/ar -X32 -q src/.libs/lib%{name}.a lib%{name}.so.1

cp %{SOURCE4} lib%{name}.so.1
/usr/bin/strip -X64 -e lib%{name}.so.1
/usr/bin/ar -X64 -q src/.libs/lib%{name}.a lib%{name}.so.1

cp %{SOURCE5} lib%{name}.so.4
/usr/bin/strip -X32 -e lib%{name}.so.4
/usr/bin/ar -X32 -q src/.libs/lib%{name}.a lib%{name}.so.4

cp %{SOURCE6} lib%{name}.so.4
/usr/bin/strip -X64 -e lib%{name}.so.4
/usr/bin/ar -X64 -q src/.libs/lib%{name}.a lib%{name}.so.4

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#Install on 32bit mode
export OBJECT_MODE=32
cd 32bit

make DESTDIR=${RPM_BUILD_ROOT} install
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/mpfr.info


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
(gmake -k check || true)
/usr/sbin/slibclean
cd ../32bit
export OBJECT_MODE=32
(gmake -k check || true)
/usr/sbin/slibclean
%endif


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

%files devel
%defattr(-,root,system,-)
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_infodir}/mpfr.info*
%{_datadir}/doc/%{name}


%changelog
* Fri Nov 27 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 4.0.2-5
- Right minimal version for gmp

* Wed Oct 28 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 4.0.2-4
- Update specfile for automated build

* Thu Apr 30 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.0.2-3
- Don't ship link to /usr

* Wed Mar 04 2020 Ayappan P <ayappap2@in.ibm.com> - 4.0.2-2
- Don't ship libraries in lib64 as it creates problem for R package
- Clean up unwanted things from specfile
- Ship pkgconfig file

* Thu Aug 8 2019 Harshita Jain <harjain9@in.ibm.com> - 4.0.2-1
- Update to 4.0.2

* Thu Mar 3 2016 Sangamesh Mallayya <smallayy@in.ibm.com> - 3.1.2-3
- Update to 3.1.2.

* Mon Feb 16 2015  BULL Hamza Sellami <hamza.sellami@bull.net>
- Rebuild(BoosTrapped) with the new gcc compiler 4.8.3 

* Mon Dec 15 2014  BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-2
- Rebuild with gcc compiler 4.8.2

* Wed Oct 23 2013 BULL Gerard Visiedo <gerard.visiedo@bull.net> - 3.1.2-1
- Update to version 3.1.2 and built on Aix6.1

* Tue Apr 19 2011 BULL Patricia Cugny <patricia.cugny@bull.net> - 3.0.1-1
- initial version on AIX 5.3
