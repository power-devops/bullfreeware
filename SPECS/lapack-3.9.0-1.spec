%bcond_without dotests
%define _libdir64 %{_libdir}64

# Depends on the machine
%global	_smp_mflags	-j4

%ifos aix6.1 || %ifos aix7.1
%global p7build 1
%else
%global p7build 0
%endif

Summary: The LAPACK libraries for numerical linear algebra.
Name: lapack
Version: 3.9.0
#%if %{p7build}
#Release: 1.p7
#%else
Release: 1
#%endif
License: BSD
Group: Development/Libraries
URL: http://www.netlib.org/lapack/
Source0: http://www.netlib.org/v%{version}.tar.gz
Source1: %{name}-%{version}-manpages.tgz
# Useless due to cmake
# Patch0:  %{name}-%{version}-aix.patch
# Already applied ??   
# Patch1:  %{name}-%{version}-lapacke.patch
# File appears at top in $BUILD
#	%if %{p7build}
#	Source2: %{name}-%{version}-p7-make.inc
#	%else
#	Source2: %{name}-%{version}-make.inc
#	%endif
Source3: lapackqref.ps
Source4: blasqr.ps
Source5: blasqr.pdf

Source1000:      %{name}-%{version}-%{release}.build.log

BuildRequires: AIX-rpm >= 6.1.0.0
BuildRequires: make
BuildRequires: cmake >= 3.16
Requires: libgcc >= 8.3.0-1
Requires: gcc-gfortran >= 8.3.0-1
Requires: blas = %{version}-%{release}

%description
LAPACK (Linear Algebra PACKage) is a standard library for numerical
linear algebra. LAPACK provides routines for solving systems of
simultaneous linear equations, least-squares solutions of linear
systems of equations, eigenvalue problems, and singular value
problems. Associated matrix factorizations (LU, Cholesky, QR, SVD,
Schur, and generalized Schur) and related computations (i.e.,
reordering of Schur factorizations and estimating condition numbers)
are also included. LAPACK can handle dense and banded matrices, but
not general sparse matrices. Similar functionality is provided for
real and complex matrices in both single and double precision. LAPACK
is coded in Fortran77.

The library is available as 32-bit and 64-bit.


%package devel
Summary: LAPACK development libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
LAPACK development include files.


%package -n blas
Summary: The BLAS (Basic Linear Algebra Subprograms) library.
Group: Development/Libraries
Requires: libgcc >= 8.3.0-1
Requires: gcc-gfortran >= 8.3.0-1

%description -n blas
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.

The library is available as 32-bit and 64-bit.

%package -n blas-devel
Summary: BLAS development libraries
Group: Development/Libraries
Requires: blas = %{version}-%{release}
Requires: gcc-gfortran >= 8.3.0-1

%description -n blas-devel
BLAS development include files.


%prep
%setup -q 
%setup -q -D -T -a1
#	cp -f %{SOURCE2} make.inc
cp make.inc.example make.inc


# %patch1
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# %patch0

%build
ulimit -d unlimited
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

# For make used as $(MAKE) in Makefiles
export MAKE="gmake %{?_smp_mflags}"

#export CC="xlc_r"
#export XLF="xlf"

# ------------------- 64-bits start ------------------
# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -O2 -maix64"
export F77="/opt/freeware/bin/gfortran" 
export FFLAGS="-O2 -maix64"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

mkdir build
cd build
cmake .. -L \
  -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=ON -DCBLAS=ON -DLAPACKE=ON \
  -DCMAKE_INSTALL_PREFIX=/opt/freeware/ \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DCMAKE_INSTALL_LIBDIR=%{_lib}64
$MAKE
cd ..
# ------------------- 64-bits end ------------------

# ------------------- 32-bits start ------------------
# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -O2 -maix32 -D_LARGE_FILES"
export F77="/opt/freeware/bin/gfortran"
export FFLAGS="-O2 -maix32 -D_LARGE_FILES"

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

mkdir build
cd build
cmake .. -L \
  -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=ON -DCBLAS=ON -DLAPACKE=ON \
  -DCMAKE_INSTALL_PREFIX=/opt/freeware/ \
  -DCMAKE_INSTALL_INCLUDEDIR=include \
  -DCMAKE_INSTALL_LIBDIR=%{_lib}
$MAKE
cd ..
# ------------------- 32-bits end ------------------


cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .


%check
%if %{with dotests}
cd 64bit/build
export OBJECT_MODE=64
( ctest . || true )
cd ../../32bit/build
export OBJECT_MODE=32
( ctest . || true )
%endif


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
ulimit -d unlimited

# install on 64bit mode
cd 64bit
export OBJECT_MODE=64
cd build
gmake install DESTDIR=${RPM_BUILD_ROOT} %{?_smp_mflags}
cd ..

# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
cd build
gmake install DESTDIR=${RPM_BUILD_ROOT} %{?_smp_mflags}
cd ..

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
chmod 755 ${RPM_BUILD_ROOT}%{_mandir}/man3

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
for f in lapack lapacke blas cblas; do
     /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib${f}.a lib${f}.so.3
     /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${f}.a   lib${f}.so.3
done

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in libblas.a liblapack.a liblapacke.a libcblas.a
  do
    ln -sf ../lib/${f} .
  done
)

# blas manpages
mkdir manpages
mv man manpages/
cd manpages
mkdir -p blas/man/man3
cd man/man3
mv caxpy.f.3 caxpy.3 ccopy.f.3 ccopy.3 cdotc.f.3 cdotc.3 cdotu.f.3 cdotu.3 cgbmv.f.3 cgbmv.3 \
cgemm.f.3 cgemm.3 cgemv.f.3 cgemv.3 cgerc.f.3 cgerc.3 cgeru.f.3 cgeru.3 chbmv.f.3 chbmv.3 \
chemm.f.3 chemm.3 chemv.f.3 chemv.3 cher.f.3 cher.3 cher2.f.3 cher2.3 cher2k.f.3 cher2k.3 \
cherk.f.3 cherk.3 chpmv.f.3 chpmv.3 chpr.f.3 chpr.3 chpr2.f.3 chpr2.3 crotg.f.3 crotg.3 \
cscal.f.3 cscal.3 csrot.f.3 csrot.3 csscal.f.3 csscal.3 cswap.f.3 cswap.3 csymm.f.3 \
csymm.3 csyr2k.f.3 csyr2k.3 csyrk.f.3 csyrk.3 ctbmv.f.3 ctbmv.3 ctbsv.f.3 ctbsv.3 ctpmv.f.3 \
ctpmv.3 ctpsv.f.3 ctpsv.3 ctrmm.f.3 ctrmm.3 ctrmv.f.3 ctrmv.3 ctrsm.f.3 ctrsm.3 ctrsv.f.3 \
ctrsv.3 dasum.f.3 dasum.3 daxpy.f.3 daxpy.3 dcabs1.f.3 dcabs1.3 dcopy.f.3 dcopy.3 ddot.f.3 \
ddot.3 dgbmv.f.3 dgbmv.3 dgemm.f.3 dgemm.3 dgemv.f.3 dgemv.3 dger.f.3 dger.3 dnrm2.f.3 \
dnrm2.3 drot.f.3 drot.3 drotg.f.3 drotg.3 drotm.f.3 drotm.3 drotmg.f.3 drotmg.3 dsbmv.f.3 \
dsbmv.3 dscal.f.3 dscal.3 dsdot.f.3 dsdot.3 dspmv.f.3 dspmv.3 dspr.f.3 dspr.3 dspr2.f.3 \
dspr2.3 dswap.f.3 dswap.3 dsymm.f.3 dsymm.3 dsymv.f.3 dsymv.3 dsyr.f.3 dsyr.3 dsyr2.f.3 \
dsyr2.3 dsyr2k.f.3 dsyr2k.3 dsyrk.f.3 dsyrk.3 dtbmv.f.3 dtbmv.3 dtbsv.f.3 dtbsv.3 dtpmv.f.3 \
dtpmv.3 dtpsv.f.3 dtpsv.3 dtrmm.f.3 dtrmm.3 dtrmv.f.3 dtrmv.3 dtrsm.f.3 dtrsm.3 dtrsv.f.3 \
dtrsv.3 dzasum.f.3 dzasum.3 dznrm2.f.3 dznrm2.3 icamax.f.3 icamax.3 idamax.f.3 idamax.3 \
isamax.f.3 isamax.3 izamax.f.3 izamax.3 lsame.3 sasum.f.3 sasum.3 saxpy.f.3 saxpy.3 \
scabs1.f.3 scabs1.3 scasum.f.3 scasum.3 scnrm2.f.3 scnrm2.3 scopy.f.3 scopy.3 sdot.f.3 sdot.3 \
sdsdot.f.3 sdsdot.3 sgbmv.f.3 sgbmv.3 sgemm.f.3 sgemm.3 sgemv.f.3 sgemv.3 sger.f.3 sger.3 \
snrm2.f.3 snrm2.3 srot.f.3 srot.3 srotg.f.3 srotg.3 srotm.f.3 srotm.3 srotmg.f.3 srotmg.3 \
ssbmv.f.3 ssbmv.3 sscal.f.3 sscal.3 sspmv.f.3 sspmv.3 sspr.f.3 sspr.3 sspr2.f.3 sspr2.3 \
sswap.f.3 sswap.3 ssymm.f.3 ssymm.3 ssymv.f.3 ssymv.3 ssyr.f.3 ssyr.3 ssyr2.f.3 ssyr2.3 \
ssyr2k.f.3 ssyr2k.3 ssyrk.f.3 ssyrk.3 stbmv.f.3 stbmv.3 stbsv.f.3 stbsv.3 stpmv.f.3 stpmv.3 \
stpsv.f.3 stpsv.3 strmm.f.3 strmm.3 strmv.f.3 strmv.3 strsm.f.3 strsm.3 strsv.f.3 strsv.3 \
xerbla.3 xerbla_array.3 zaxpy.f.3 zaxpy.3 zcopy.f.3 zcopy.3 \
zdotc.f.3 zdotc.3 zdotu.f.3 zdotu.3 zdrot.f.3 zdrot.3 zdscal.f.3 zdscal.3 zgbmv.f.3 zgbmv.3 \
zgemm.f.3 zgemm.3 zgemv.f.3 zgemv.3 zgerc.f.3 zgerc.3 zgeru.f.3 zgeru.3 zhbmv.f.3 zhbmv.3 \
zhemm.f.3 zhemm.3 zhemv.f.3 zhemv.3 zher.f.3 zher.3 zher2.f.3 zher2.3 zher2k.f.3 zher2k.3 \
zherk.f.3 zherk.3 zhpmv.f.3 zhpmv.3 zhpr.f.3 zhpr.3 zhpr2.f.3 zhpr2.3 zrotg.f.3 zrotg.3 \
zscal.f.3 zscal.3 zswap.f.3 zswap.3 zsymm.f.3 zsymm.3 zsyr2k.f.3 zsyr2k.3 zsyrk.f.3 zsyrk.3 \
ztbmv.f.3 ztbmv.3 ztbsv.f.3 ztbsv.3 ztpmv.f.3 ztpmv.3 ztpsv.f.3 ztpsv.3 ztrmm.f.3 ztrmm.3 \
ztrmv.f.3 ztrmv.3 ztrsm.f.3 ztrsm.3 ztrsv.f.3 ztrsv.3 ../../blas/man/man3
cd ../../..

# remove weird man pages
rm -f manpages/man/man3/_Users_julie*

find manpages/blas/man/man3 -type f > tmpFile
rm -f blasmans ; touch blasmans
for f in `cat tmpFile` ; do
    echo %{_mandir}/man3/`basename $f manpages/blas/man/man3/` >> blasmans
done

find manpages/man/man3 -type f > tmpFile
rm -f lapackmans ; touch lapackmans
for f in `cat tmpFile` ; do
    echo %{_mandir}/man3/`basename $f manpages/man/man3/` >> lapackmans
done

cp -f manpages/blas/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3
cp -f manpages/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3

# lapacke headers
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/lapacke
chmod 0755 ${RPM_BUILD_ROOT}%{_includedir}/lapacke
cp -r LAPACKE/include/*.h ${RPM_BUILD_ROOT}%{_includedir}/lapacke/

# Move cblas headers
(
  cd ${RPM_BUILD_ROOT}%{_includedir}
  mkdir -p cblas
  chmod 0755 cblas
  mv cblas_*.h cblas
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f 32bit/lapackmans
%defattr(-,root,system)
%doc 32bit/README.md 32bit/LICENSE 32bit/lapackqref.ps
%{_libdir}/liblapack*.a
%{_libdir64}/liblapack*.a


%files devel
%defattr(-,root,system)
%doc 32bit/README.md 32bit/LICENSE 32bit/lapackqref.ps
%{_includedir}/*


%files -n blas -f 32bit/blasmans
%defattr(-,root,system)
%doc 32bit/blasqr.ps 32bit/blasqr.pdf 32bit/LICENSE
%{_libdir}/libblas.a
%{_libdir64}/libblas.a
%{_libdir}/libcblas.a
%{_libdir64}/libcblas.a


%files -n blas-devel
%defattr(-,root,system)
%{_includedir}/cblas/


%changelog
* Tue May 26 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.9.0-1
- New version for BullFreeware

* Tue May 19 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.8.0-3
- Add include files of blas in a blas-devel subpackage
- Add cblas
- Build with cmake

* Tue Dec 03 2019 Tony Reix <tony.reix@atos.net> - 3.8.0-2
- Initial port for BullFreeware
- Built with GCC 8.3.0 and libgfortran.so.5

* Mon Jan 14 2019 Reshma V Kumar <reskumar@in.ibm.com> -3.8.0-1
- Initial port for AIX toolbox

* Thu Nov 23 2017 Michael Perzl <michael@perzl.org> - 3.8.0-1
- updated to version 3.8.0

* Fri Sep 22 2017 Michael Perzl <michael@perzl.org> - 3.7.1-1
- updated to version 3.7.1

* Fri Feb 10 2017 Michael Perzl <michael@perzl.org> - 3.7.0-1
- updated to version 3.7.0

* Tue Jun 21 2016 Michael Perzl <michael@perzl.org> - 3.6.1-1
- updated to version 3.6.1

* Tue Jan 05 2016 Michael Perzl <michael@perzl.org> - 3.6.0-1
- updated to version 3.6.0

* Mon Dec 09 2013 Michael Perzl <michael@perzl.org> - 3.5.0-1
- updated to version 3.5.0

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 3.4.2-1
- updated to version 3.4.2

* Mon Apr 30 2012 Michael Perzl <michael@perzl.org> - 3.4.1-1
- updated to version 3.4.1

* Mon Nov 21 2011 Michael Perzl <michael@perzl.org> - 3.4.0-1
- updated to version 3.4.0
- build and include lapacke

* Mon Jun 13 2011 Michael Perzl <michael@perzl.org> - 3.3.1-1
- updated to version 3.3.1

* Tue Feb 15 2011 Michael Perzl <michael@perzl.org> - 3.3.0-1
- updated to version 3.3.0

* Tue Feb 15 2011 Michael Perzl <michael@perzl.org> - 3.2.2-1
- updated to version 3.2.2

* Fri Feb 01 2008 Michael Perzl <michael@perzl.org> - 3.1.1-1
- first version for AIX V5.1 and higher
