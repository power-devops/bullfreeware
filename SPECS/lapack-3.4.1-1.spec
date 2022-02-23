Summary: The LAPACK libraries for numerical linear algebra.
Name: lapack
Version: 3.4.1
Release: 1
License: BSD
Group: Development/Libraries
URL: http://www.netlib.org/lapack/
Source0: http://www.netlib.org/%{name}/%{name}-%{version}.tgz
Source1: %{name}-%{version}-manpages.tgz
Source2: %{name}-%{version}-make.inc
Source3: lapackqref.ps
Source4: blasqr.ps
Source5: blasqr.pdf
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: make

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


%package -n blas
Summary: The BLAS (Basic Linear Algebra Subprograms) library.
Group: Development/Libraries

%description -n blas
BLAS (Basic Linear Algebra Subprograms) is a standard library which
provides a number of basic algorithms for numerical algebra.

The library is available as 32-bit and 64-bit.


%prep
%setup -q 
%setup -q -D -T -a1
cp -f %{SOURCE2} make.inc


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# ------------------- 64-bits start ------------------
# first build the 64-bit version
export F77="/usr/bin/xlf_r -q64"

# Build BLAS
cd BLAS/SRC
make
cd ../..

# Build the dlamch, dsecnd, lsame, second, slamch bits
cd INSTALL
make
cd ..

# Build the lapack library
cd SRC
make
cd ..

# Build the lapacke libraries
cd lapacke

cd ..

# create shared objects
for f in blas lapack ; do
    /usr/vac/bin/CreateExportList -X64 ${f}.exp ${f}.a
    ${F77} -qmkshrobj ${f}.a -o shr64.o -bE:${f}.exp -berok
    rm -f ${f}.exp
    ${AR} -rv lib${f}.a shr64.o
done
# ------------------- 64-bits end ------------------

make clean
rm -f blas.a lapack.a

# ------------------- 32-bits start ------------------
# now build the 32-bit version
export F77="/usr/bin/xlf_r"

# Build BLAS
cd BLAS/SRC
make
cd ../..

# Build the dlamch, dsecnd, lsame, second, slamch bits
cd INSTALL
make
cd ..

# Build the lapack library
cd SRC
make
cd ..

# Build the lapacke libraries
cd lapacke

cd ..

# create shared objects
for f in blas lapack ; do
    /usr/vac/bin/CreateExportList -X32 ${f}.exp ${f}.a
    ${F77} -qmkshrobj ${f}.a -o shr32.o -bE:${f}.exp -berok
    rm -f ${f}.exp
    ${AR} -q lib${f}.a shr32.o
done
# ------------------- 32-bits end ------------------


cp %{SOURCE3} .
cp %{SOURCE4} .
cp %{SOURCE5} .


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
chmod 755 ${RPM_BUILD_ROOT}%{_mandir}/man3

for f in libblas.a liblapack.a ; do
    cp -f ${f} ${RPM_BUILD_ROOT}%{_libdir}/${f}
done

# blas manpages
mkdir manpages
mv man manpages/
cd manpages
mkdir -p blas/man/man3
cd man/man3
mv caxpy.f.3 CAXPY.3 ccopy.f.3 CCOPY.3 cdotc.f.3 CDOTC.3 cdotu.f.3 CDOTU.3 cgbmv.f.3 CGBMV.3 \
cgemm.f.3 CGEMM.3 cgemv.f.3 CGEMV.3 cgerc.f.3 CGERC.3 cgeru.f.3 CGERU.3 chbmv.f.3 CHBMV.3 \
chemm.f.3 CHEMM.3 chemv.f.3 CHEMV.3 cher.f.3 CHER.3 cher2.f.3 CHER2.3 cher2k.f.3 CHER2K.3 \
cherk.f.3 CHERK.3 chpmv.f.3 CHPMV.3 chpr.f.3 CHPR.3 chpr2.f.3 CHPR2.3 crotg.f.3 CROTG.3 \
cscal.f.3 CSCAL.3 csrot.f.3 CSROT.3 csscal.f.3 CSSCAL.3 cswap.f.3 CSWAP.3 csymm.f.3 \
CSYMM.3 csyr2k.f.3 CSYR2K.3 csyrk.f.3 CSYRK.3 ctbmv.f.3 CTBMV.3 ctbsv.f.3 CTBSV.3 ctpmv.f.3 \
CTPMV.3 ctpsv.f.3 CTPSV.3 ctrmm.f.3 CTRMM.3 ctrmv.f.3 CTRMV.3 ctrsm.f.3 CTRSM.3 ctrsv.f.3 \
CTRSV.3 dasum.f.3 DASUM.3 daxpy.f.3 DAXPY.3 dcabs1.f.3 DCABS1.3 dcopy.f.3 DCOPY.3 ddot.f.3 \
DDOT.3 dgbmv.f.3 DGBMV.3 dgemm.f.3 DGEMM.3 dgemv.f.3 DGEMV.3 dger.f.3 DGER.3 dnrm2.f.3 \
DNRM2.3 drot.f.3 DROT.3 drotg.f.3 DROTG.3 drotm.f.3 DROTM.3 drotmg.f.3 DROTMG.3 dsbmv.f.3 \
DSBMV.3 dscal.f.3 DSCAL.3 dsdot.f.3 DSDOT.3 dspmv.f.3 DSPMV.3 dspr.f.3 DSPR.3 dspr2.f.3 \
DSPR2.3 dswap.f.3 DSWAP.3 dsymm.f.3 DSYMM.3 dsymv.f.3 DSYMV.3 dsyr.f.3 DSYR.3 dsyr2.f.3 \
DSYR2.3 dsyr2k.f.3 DSYR2K.3 dsyrk.f.3 DSYRK.3 dtbmv.f.3 DTBMV.3 dtbsv.f.3 DTBSV.3 dtpmv.f.3 \
DTPMV.3 dtpsv.f.3 DTPSV.3 dtrmm.f.3 DTRMM.3 dtrmv.f.3 DTRMV.3 dtrsm.f.3 DTRSM.3 dtrsv.f.3 \
DTRSV.3 dzasum.f.3 DZASUM.3 dznrm2.f.3 DZNRM2.3 icamax.f.3 ICAMAX.3 idamax.f.3 IDAMAX.3 \
isamax.f.3 ISAMAX.3 izamax.f.3 IZAMAX.3 LSAME.3 sasum.f.3 SASUM.3 saxpy.f.3 SAXPY.3 \
scabs1.f.3 SCABS1.3 scasum.f.3 SCASUM.3 scnrm2.f.3 SCNRM2.3 scopy.f.3 SCOPY.3 sdot.f.3 SDOT.3 \
sdsdot.f.3 SDSDOT.3 sgbmv.f.3 SGBMV.3 sgemm.f.3 SGEMM.3 sgemv.f.3 SGEMV.3 sger.f.3 SGER.3 \
snrm2.f.3 SNRM2.3 srot.f.3 SROT.3 srotg.f.3 SROTG.3 srotm.f.3 SROTM.3 srotmg.f.3 SROTMG.3 \
ssbmv.f.3 SSBMV.3 sscal.f.3 SSCAL.3 sspmv.f.3 SSPMV.3 sspr.f.3 SSPR.3 sspr2.f.3 SSPR2.3 \
sswap.f.3 SSWAP.3 ssymm.f.3 SSYMM.3 ssymv.f.3 SSYMV.3 ssyr.f.3 SSYR.3 ssyr2.f.3 SSYR2.3 \
ssyr2k.f.3 SSYR2K.3 ssyrk.f.3 SSYRK.3 stbmv.f.3 STBMV.3 stbsv.f.3 STBSV.3 stpmv.f.3 STPMV.3 \
stpsv.f.3 STPSV.3 strmm.f.3 STRMM.3 strmv.f.3 STRMV.3 strsm.f.3 STRSM.3 strsv.f.3 STRSV.3 \
XERBLA.3 XERBLA_ARRAY.3 zaxpy.f.3 ZAXPY.3 zcopy.f.3 ZCOPY.3 \
zdotc.f.3 ZDOTC.3 zdotu.f.3 ZDOTU.3 zdrot.f.3 ZDROT.3 zdscal.f.3 ZDSCAL.3 zgbmv.f.3 ZGBMV.3 \
zgemm.f.3 ZGEMM.3 zgemv.f.3 ZGEMV.3 zgerc.f.3 ZGERC.3 zgeru.f.3 ZGERU.3 zhbmv.f.3 ZHBMV.3 \
zhemm.f.3 ZHEMM.3 zhemv.f.3 ZHEMV.3 zher.f.3 ZHER.3 zher2.f.3 ZHER2.3 zher2k.f.3 ZHER2K.3 \
zherk.f.3 ZHERK.3 zhpmv.f.3 ZHPMV.3 zhpr.f.3 ZHPR.3 zhpr2.f.3 ZHPR2.3 zrotg.f.3 ZROTG.3 \
zscal.f.3 ZSCAL.3 zswap.f.3 ZSWAP.3 zsymm.f.3 ZSYMM.3 zsyr2k.f.3 ZSYR2K.3 zsyrk.f.3 ZSYRK.3 \
ztbmv.f.3 ZTBMV.3 ztbsv.f.3 ZTBSV.3 ztpmv.f.3 ZTPMV.3 ztpsv.f.3 ZTPSV.3 ztrmm.f.3 ZTRMM.3 \
ztrmv.f.3 ZTRMV.3 ztrsm.f.3 ZTRSM.3 ztrsv.f.3 ZTRSV.3 ../../blas/man/man3
cd ../../..

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
cp -r lapacke/include/*.h ${RPM_BUILD_ROOT}%{_includedir}/lapacke/

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/lib
cd usr/linux/lib
ln -sf ../../..%{_libdir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f lapackmans
%defattr(-,root,system)
%doc README lapackqref.ps
%{_libdir}/liblapack.a
/usr/linux/lib/liblapack.a


%files -n blas -f blasmans
%defattr(-,root,system)
%doc blasqr.ps blasqr.pdf
%{_libdir}/libblas*.a
/usr/linux/lib/libblas*.a


%changelog
* Fri Sep 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 3.4.1-1
- Initial port on Aix6.1
