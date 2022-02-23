Summary:	A language for data analysis and graphics
Name:		R
Version:	2.15.1
#Version:	patched
Release:	2
License:        GPLv2+
Group:          Sciences/Mathematics
URL:            http://www.r-project.org
Source0:        ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
Patch0:		%{name}-%{version}-aix_tre.patch
BuildRoot: 	/var/tmp/%{name}-%{version}-%{release}-root
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  cairo-devel

%description
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package        devel
Summary:        Files for development of R packages
Group:          Development/Other
#Requires:       R-core = %{EVRD}

%description    devel
Install R-devel if you are going to develop or compile R packages.


%package        -n libRmath
Summary:        Standalone math library from the R project
Group:          System/Libraries
#Provides:       Rmath = %{EVRD}

%description    -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the shared libRmath library.

%package        -n libRmath-devel
Summary:        Headers from the R Standalone math library
Group:          Development/Libraries
Requires:       libRmath = %{version}-%{release}
Requires:       pkgconfig
#Provides:       Rmath-devel = %{EVRD}

%description    -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the libRmath header files.

%package        -n libRmath-static-devel
Summary:        Static R Standalone math library
Group:          Development/Libraries
Requires:       libRmath = %{version}-%{release}
#Provides:       Rmath-static-devel = %{version}-%{release}

%description    -n libRmath-static-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This package provides the static libRmath library.

%prep
%setup -q
%patch0 -p1 -b .aix_tre


sed -e "s;nm=nm;nm='/usr/bin/nm -X32_64';" ./tools/ldAIX4 >./tools/ldAIX4.tmp
[ -s ./tools/ldAIX4.tmp ] && mv -f ./tools/ldAIX4.tmp ./tools/ldAIX4

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

cd 32bit
echo "%{_libdir}/R/lib/" >R.ld.conf
cd ../64bit
echo "%{_prefix}/lib64/R/lib/" >R.ld.conf

%build
# Add PATHS to Renviron for R_LIBS_SITE
export R_BROWSER="%{_bindir}/firefox"
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
# We use the AIX nm with the -B option to display the symbols in the BSD format
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64 -B"


# first build the 64-bit version
cd 64bit
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"
export FC="/usr/bin/xlf_r -q64"
export F77="/usr/bin/xlf_r -q64"

export LDFLAGS="-L%{_prefix}/lib64  -L%{_libdir} -L/usr/lib64 -L/usr/lib"
export CFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict -qmaxmem=16384"
export CXXFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict -qmaxmem=16384"
export CPPFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict -qmaxmem=16384"
export FFLAGS="-I%{_includedir} -I/usr/include -qarch=auto -qcache=auto -qtune=auto -qstrict -qmaxmem=16384"
export FCLAGS="-I%{_includedir} -I/usr/include -qarch=auto -qcache=auto -qtune=auto -qstrict -qmaxmem=16384"

aclocal -I ./m4
autoconf

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib64 \
	--with-blas="-lblas" \
	--without-recommended-packages \
	--with-system-pcre

# (tpg) somehow --prefix is not honored
sed -e 's#/usr/local#%{_prefix}#g' Makeconf

make
make -C src/nmath/standalone

#make check-all
#make pdf
make info


# now build the 32-bit version
cd ../32bit
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export FC="/usr/bin/xlf_r"
export F77="/usr/bin/xlf_r"
export LDFLAGS="-L%{_libdir} -L/usr/lib"

aclocal -I ./m4
autoconf

./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--with-blas="-lblas" \
	--without-recommended-packages \
	--with-system-pcre

make
make -C src/nmath/standalone
#make check-all
#make pdf
make info


## Convert to UTF-8
#for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1
#do
#    iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
#    mv $i{.utf8,}
#done


%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"

#First build 64bit mode
cd 64bit
export CC="/usr/vac/bin/xlc_r -q64"
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib64/R/lib
make DESTDIR=${RPM_BUILD_ROOT} install install-info
#make DESTDIR=${RPM_BUILD_ROOT} install-pdf
make DESTDIR=${RPM_BUILD_ROOT} install -C src/nmath/standalone

# Install libRmath files
make -C src/nmath/standalone install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/ld.so.conf.d
echo "%{_prefix}/lib64/R/lib" > ${RPM_BUILD_ROOT}/etc/ld.so.conf.d/%{name}-%{_arch}64.conf

# Fix exec bits
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/lib64/R/share/sh/echo.sh
chmod -x ${RPM_BUILD_ROOT}%{_prefix}/lib64/R/library/base/CITATION

# Preserve binaries 64bit
cd ${RPM_BUILD_ROOT}%{_bindir}
for f in R Rscript
do
  mv  ${f}  ${f}64
done
cd -
#Now build 32bit mode
cd ../32bit
export CC="/usr/vac/bin/xlc_r"
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/R/lib
make DESTDIR=${RPM_BUILD_ROOT} install install-info
#make DESTDIR=${RPM_BUILD_ROOT} install-pdf
make DESTDIR=${RPM_BUILD_ROOT} install -C src/nmath/standalone

# Install libRmath files
make -C src/nmath/standalone install DESTDIR=${RPM_BUILD_ROOT}

echo "%{_prefix}/lib/R/lib" > ${RPM_BUILD_ROOT}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/R/html
cp  ${RPM_BUILD_DIR}/%{name}-%{version}/32bit/doc/html/packages.html ${RPM_BUILD_ROOT}%{_docdir}/R/html/packages.html
sed -e "s|\..\/\..|%{_libdir}/R|g" ${RPM_BUILD_ROOT}%{_docdir}/R/html/packages.html > ${RPM_BUILD_ROOT}%{_docdir}/R/html/file.tmp

mv ${RPM_BUILD_ROOT}%{_docdir}/R/html/file.tmp ${RPM_BUILD_ROOT}%{_docdir}/R/html/packages.html

# Fix exec bits
chmod +x ${RPM_BUILD_ROOT}%{_libdir}/R/share/sh/echo.sh
chmod -x ${RPM_BUILD_ROOT}%{_libdir}/R/library/base/CITATION

# Preserve binaries 32bit
cd ${RPM_BUILD_ROOT}%{_bindir}
for f in R Rscript
do
  mv  ${f}  ${f}32
done
cd -

# Add 64bit objects into 32bit library
mkdir -p /tmp/extract
cd  /tmp/extract
rm -f *.o
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_prefix}/lib64/libRmath.a
ls *\.o >list_ar
for f in $(cat list_ar)
do
  f1="$(echo $f | cut -d'.' -f1)"
  mv ${f} ${f1}_64.o
  ar -X32_64 -q ${RPM_BUILD_ROOT}%{_libdir}/libRmath.a ${f1}_64.o
done
cd -
rm -rf /tmp/extract

# Common build 32 and 64bit
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/R/library

# Install rpm helper macros
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.d

# Symbolic link for convenience
# Actually do make the reverse link done in fedora, to avoid the need to
# fight rpm to convert a directory into a symlink if upgrading from
# previous mandriva packages
ln -sf ../%{_lib}/R/include ${RPM_BUILD_ROOT}%{_includedir}/R

cp -pr ${RPM_BUILD_ROOT}/etc/* ${RPM_BUILD_ROOT}%{_sysconfdir}

#Default binaries are 64bit
cd ${RPM_BUILD_ROOT}/%{_bindir}
ln -sf R64 R
ln -sf Rscript64 Rscript

(
  cd ${RPM_BUILD_ROOT}
  for dir in include bin lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  mkdir -p  ${RPM_BUILD_ROOT}/etc/ld.so.conf.d
  cd ${RPM_BUILD_ROOT}/etc/ld.so.conf.d
  ln -sf ../..%{_prefix}/etc/ld.so.conf.d/* .
)


%post
/sbin/install-info %{_datadir}/info/R-FAQ.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info %{_datadir}/info/R-admin.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info %{_datadir}/info/R-exts.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info %{_datadir}/info/R-intro.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info %{_datadir}/info/R-ints.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info %{_datadir}/info/R-lang.info.gz %{_infodir}/dir 2>/dev/null

%preun
/sbin/install-info --delete %{_datadir}/info/R-FAQ.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info --delete %{_datadir}/info/R-admin.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info --delete %{_datadir}/info/R-exts.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info --delete %{_datadir}/info/R-intro.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info --delete %{_datadir}/info/R-ints.info.gz %{_infodir}/dir 2>/dev/null
/sbin/install-info --delete %{_datadir}/info/R-lang.info.gz %{_infodir}/dir 2>/dev/null


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,system,-)
%doc 32bit/ChangeLog 32bit/COPYING 32bit/INSTALL 32bit/*NEWS 32bit/README 32bit/VERSION
%doc 32bit/doc/AUTHORS 32bit/doc/COPYING* 32bit/doc/COPYRIGHTS
%doc 32bit/doc/CRAN_mirrors.csv 32bit/doc/FAQ 32bit/doc/KEYWORDS
%doc 32bit/doc/RESOURCES 32bit/doc/THANKS 32bit/doc/manual/
%doc %{_docdir}/R
%{_bindir}/R*
%dir %{_prefix}/lib64/R
%dir %{_libdir}/R
%{_libdir}/R/bin
%{_prefix}/lib64/R/bin
%{_libdir}/R/doc
%{_prefix}/lib64/R/doc
%{_libdir}/R/etc
%{_prefix}/lib64/R/etc
%{_libdir}/R/lib
%{_prefix}/lib64/R/lib
%{_libdir}/R/library
%{_prefix}/lib64/R/library
%{_libdir}/R/modules
%{_prefix}/lib64/R/modules
%{_libdir}/R/share
%{_prefix}/lib64/R/share
%{_datadir}/R
%{_datadir}/info/R-*.info*
%{_sysconfdir}/rpm
%{_sysconfdir}/ld.so.conf.d/R-*
%{_datadir}/man/man1/*
/etc/ld.so.conf.d/R-*
/usr/bin/*
/usr/lib/*
/usr/lib64/*


%files	devel
%defattr(-,root,system,-)
%{_includedir}/R
%{_libdir}/R/include
%{_prefix}/lib64/R/include
/usr/include

%files	-n libRmath
%defattr(-,root,system,-)
%{_libdir}/libRmath.a
%{_prefix}/lib64/libRmath.a
%{_libdir}/libRmath.so
%{_prefix}/lib64/libRmath.so
/usr/lib/libRmath.a
/usr/lib64/libRmath.a
/usr/lib/libRmath.so
/usr/lib64/libRmath.so

%files	-n libRmath-devel
%defattr(-,root,system,-)
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc
%{_prefix}/lib64/pkgconfig/libRmath.pc

%files	-n libRmath-static-devel
%defattr(-,root,system,-)
%{_libdir}/libRmath.a
%{_prefix}/lib64/libRmath.a
/usr/lib/libRmath.a
/usr/lib64/libRmath.a

%changelog
* Thu Nov 08 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.15.1-2
- Building on 32bit and 64bit

* Thu Sep 27 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.15.1-1
- Initial port on Aix6.1

