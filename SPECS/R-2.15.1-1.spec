Summary:	A language for data analysis and graphics
Name:		R
Version:	2.15.1
#Version:	patched
Release:	1
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

echo "%{_libdir}/R/lib/" >R.ld.conf

sed -e "s;nm=nm;nm=/usr/bin/nm;" ./tools/ldAIX4 >./tools/ldAIX4.tmp
[ -s ./tools/ldAIX4.tmp ] && mv -f ./tools/ldAIX4.tmp ./tools/ldAIX4

%build
# Add PATHS to Renviron for R_LIBS_SITE
export R_BROWSER="%{_bindir}/firefox"
export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export FC="/usr/bin/xlf_r"
export F77="/usr/bin/xlf_r"

export LDFLAGS="-L%{_libdir} -L/usr/lib"

export CFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict"
export CXXFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict"
export CPPFLAGS="-I%{_includedir} -I/usr/include -ma -qarch=auto -qcache=auto -qtune=auto -qstrict"
export FFLAGS="-I%{_includedir} -I/usr/include -qarch=auto -qcache=auto -qtune=auto -qstrict"
export FCLAGS="-I%{_includedir} -I/usr/include -qarch=auto -qcache=auto -qtune=auto -qstrict"

export NM=/usr/bin/nm
export RM="/usr/bin/rm -f"


aclocal -I ./m4

autoconf

./configure \
	--prefix=%{_prefix} \
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

## Convert to UTF-8
#for i in doc/manual/R-intro.info doc/manual/R-FAQ.info doc/FAQ doc/manual/R-admin.info doc/manual/R-exts.info-1
#do
#    iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
#    mv $i{.utf8,}
#done


%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"

mkdir -p /var/tmp/R-2.15.1-1-root/opt/freeware/lib/R/lib

make DESTDIR=${RPM_BUILD_ROOT} install install-info
#make DESTDIR=${RPM_BUILD_ROOT} install-pdf
make DESTDIR=${RPM_BUILD_ROOT} install -C src/nmath/standalone

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old

# Install libRmath files
make -C src/nmath/standalone install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > ${RPM_BUILD_ROOT}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/R/library

# Install rpm helper macros
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/rpm/macros.d

# Install rpm helper script
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/rpm/

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/R/html
cp  ${RPM_BUILD_DIR}/%{name}-%{version}/doc/html/packages.html ${RPM_BUILD_ROOT}%{_docdir}/R/html/packages.html
sed -e 's|\..\/\..|%{_libdir}/R|g' ${RPM_BUILD_ROOT}%{_docdir}/R/html/packages.html

# Fix exec bits
chmod +x ${RPM_BUILD_ROOT}%{_libdir}/R/share/sh/echo.sh
chmod -x ${RPM_BUILD_ROOT}%{_libdir}/R/library/base/CITATION

# Symbolic link for convenience
# Actually do make the reverse link done in fedora, to avoid the need to
# fight rpm to convert a directory into a symlink if upgrading from
# previous mandriva packages
ln -sf ../%{_lib}/R/include ${RPM_BUILD_ROOT}%{_includedir}/R

mv ${RPM_BUILD_ROOT}/etc/* ${RPM_BUILD_ROOT}%{_sysconfdir}

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
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
%doc ChangeLog COPYING INSTALL *NEWS README VERSION
%doc doc/AUTHORS doc/COPYING* doc/COPYRIGHTS
%doc doc/CRAN_mirrors.csv doc/FAQ doc/KEYWORDS
%doc doc/RESOURCES doc/THANKS doc/manual/
%doc %{_docdir}/R
%{_bindir}/R
%{_bindir}/Rscript
%dir %{_libdir}/R
%{_libdir}/R/bin
%{_libdir}/R/doc
%{_libdir}/R/etc
%{_libdir}/R/lib
%{_libdir}/R/library
%{_libdir}/R/modules
%{_libdir}/R/share
%{_datadir}/R
%{_datadir}/info/R-*.info*
%{_sysconfdir}/rpm
%{_sysconfdir}/ld.so.conf.d/R-*
%{_datadir}/man/man1/*
/usr/bin/*


%files	devel
%defattr(-,root,system,-)
%{_includedir}/R
%{_libdir}/R/include

%files	-n libRmath
%defattr(-,root,system,-)
%{_libdir}/libRmath.a
%{_libdir}/libRmath.so
/usr/lib/libRmath.a
/usr/lib/libRmath.so

%files	-n libRmath-devel
%defattr(-,root,system,-)
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

%files	-n libRmath-static-devel
%defattr(-,root,system,-)
%{_libdir}/libRmath.a
/usr/lib/libRmath.a


%changelog
* Thu Sep 27 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.15.1-1
- Initial port on Aix6.1

