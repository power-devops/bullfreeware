
# Tests for this package.
%bcond_without dotests

%global _smp_mflags -j4

#%ifos aix6.1 || %ifos aix7.1 || %ifos aix7.2
#%global p7build 1
#%else
%global p7build 0
#%endif

%define _libdir64 %{_prefix}/lib64

%define python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python64_sitearch %(python_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

Summary: Library providing the GNOME XSLT engine
Name: libxslt
Version: 1.1.34
%if %{p7build}
Release: 1.p7
%else
Release: 1
%endif
License: MIT
Group: Development/Libraries
Source0: ftp://xmlsoft.org/XSLT/%{name}-%{version}.tar.gz
Source1: ftp://xmlsoft.org/XSLT/%{name}-%{version}.tar.gz.asc
Source1000: %{name}-%{version}-%{release}.build.log
URL: http://xmlsoft.org/XSLT/

# Fixes an issues that does not appear on Fedora
Patch0:	%{name}-%{version}-PYTHON_SITE_PACKAGES-configure.patch
# Doing the same in configure.ac file leads to another bug with PKG_CHECK_MODULES_STATIC inside it

BuildRequires: make
%if %{p7build}
BuildRequires: libxml2-devel >= 2.9.5-1.p7
# Next line required for %check python tests
BuildRequires: libxml2-python >= 2.9.5-1.p7
%else
BuildRequires: libxml2-devel >= 2.9.5-1
# Next line required for %check python tests
BuildRequires: libxml2-python >= 2.9.5-1
%endif
BuildRequires: libgcrypt-devel >= 1.5.0-1
%if %{p7build}
Requires: libxml2 >= 2.9.5-1.p7
%else
Requires: libxml2 >= 2.9.5-1
%endif
Requires: libgcrypt >= 1.5.0-1

%if %{p7build}
%ifos aix6.1
Requires: AIX-rpm >= 6.1.8.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.3.0
%endif
%endif

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

The library is available as 32-bit and 64-bit.


%package devel
Summary: Libraries, includes, etc. to embed the GNOME XSLT engine
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%if %{p7build}
Requires: libxml2-devel >= 2.9.5-1.p7
%else
Requires: libxml2-devel >= 2.9.5-1
%endif
Requires: libgcrypt-devel >= 1.5.0-1
Requires: pkg-config

%description devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.9.5
installed.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%package -n python2-%{name}
Summary: Python bindings for the libxslt library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

Requires: libxml2-python >= 2.9.5-1
Requires: python >= 2.7.13-1
Provides: %{name}-python = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}

%description -n python2-%{name}
The libxslt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxslt library to apply XSLT transformations.

This library allows to parse sytlesheets, uses the libxml2-python
to load and save XML and HTML files. Direct access to XPath and
the XSLT transformation context are possible to extend the XSLT language
with XPath functions written in Python.


%prep
%setup -q

%patch0 -p1 -b .PYTHON_SITE_PACKAGES

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit
tar cf - . | (cd ../64bit ; tar xpf -)


%build
# Fix issue with python/Makefile with DOCS empty due to /usr/bin/ksh:
#	install-data-local:
#        	@(for doc in $(DOCS) ;
export        SHELL=/usr/bin/bash
export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash

export RM="/usr/bin/rm -f"

# XLC
# '-O3 -qstrict' produces wrong builds on AIX5L V5.1
# export CFLAGS="-qmaxmem=262144 -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_ALL_SOURCE -DFUNCPROTO=15 -I/opt/freeware/include -O"

export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_ALL_SOURCE -DFUNCPROTO=15 -I/opt/freeware/include -O2"

%if %{p7build}
# XLC
#	CFLAGS=${CFLAGS}"3 -qstrict -qarch=pwr7 -qtune=pwr7 -qmaxmem=-1"
	CFLAGS=${CFLAGS}"3"
%else
	CFLAGS=${CFLAGS}"2"
%endif

cd 64bit
# first build the 64-bit version
#export CC="xlc_r -q64"
export CC="gcc -maix64"

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
export PYTHON=%{_bindir}/python2_64

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --with-python \
    --enable-shared --enable-static

gmake %{?_smp_mflags}


cd ../32bit
# now build the 32-bit version
#export CC="xlc_r -q32 -D_LARGE_FILES=1"
export CC="gcc -maix32 -D_LARGE_FILES" 

export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
export PYTHON=%{_bindir}/python2_32

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --with-python=${PYTHON} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

gzip --best ChangeLog


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake install DESTDIR=${RPM_BUILD_ROOT}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  pwd
  ls -l
  for f in * 
  do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a
  do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a
  do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.so*
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libexslt.a ${RPM_BUILD_ROOT}%{_libdir64}/libexslt.so*

# No more add symlinks from /usr to /opt/freeware
#	(
#	  cd ${RPM_BUILD_ROOT}
#	  for dir in bin include lib lib64
#	  do
#	    mkdir -p usr/$dir
#	    cd usr/$dir
#	    ln -sf ../..%{_prefix}/$dir/* .
#	    cd -
#	  done
#	)

# Replace /usr/bin/python by env python2 everywhere.
# Useful both for tests and for delivery
# Moreover, .py are taken both from RPM_BUILD_ROOT and from $BUILD (doc files)
pwd
find ../32bit ${RPM_BUILD_ROOT} -name "*.py" | xargs /opt/freeware/bin/sed -i "s|/usr/bin/python|/usr/bin/env python2_32|"
find ../64bit ${RPM_BUILD_ROOT} -name "*.py" | xargs /opt/freeware/bin/sed -i "s|/usr/bin/python|/usr/bin/env python2_64|"

# Remove all .la
# To be done also after %check
find ${RPM_BUILD_ROOT} -name "*.la" | xargs rm


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export TRACE="--trace"
export TRACE=""

cd 64bit
export OBJECT_MODE=64
export LDFLAGS_="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "
(gmake $TRACE -k check LDFLAGS="-L%{_builddir}/%{name}-%{version}/64bit/libxslt/.libs -L%{_builddir}/%{name}-%{version}/64bit/libexslt/.libs -L%{_builddir}/%{name}-%{version}/64bit/python/.libs $LDFLAGS_" LIBPATH="%{_builddir}/%{name}-%{version}/64bit/libxslt/.libs:%{_builddir}/%{name}-%{version}/64bit/libexslt/.libs:%{_builddir}/%{name}-%{version}/64bit/python/.libs" || true)

cd ../32bit
export OBJECT_MODE=32
export LDFLAGS_="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib "
(gmake $TRACE -k check LDFLAGS="-L%{_builddir}/%{name}-%{version}/32bit/libxslt/.libs -L%{_builddir}/%{name}-%{version}/32bit/libexslt/.libs -L%{_builddir}/%{name}-%{version}/32bit/python/.libs $LDFLAGS_" LIBPATH="%{_builddir}/%{name}-%{version}/32bit/libxslt/.libs:%{_builddir}/%{name}-%{version}/32bit/libexslt/.libs:%{_builddir}/%{name}-%{version}/32bit/python/.libs" || true)

# Remove all .la since some are recreated by %check after %install
# To be done also after %check
find .. -name "*.la" | xargs rm


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/ChangeLog.gz 32bit/NEWS 32bit/README 32bit/Copyright
%doc 32bit/TODO 32bit/FEATURES
%{_bindir}/xsltproc*
%{_libdir}/lib*.a
%{_libdir}/libxslt-plugins
%{_libdir64}/libxslt-plugins
%{_mandir}/man1/xsltproc.1


%files devel
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/ChangeLog.gz 32bit/NEWS 32bit/README 32bit/Copyright
%doc 32bit/TODO 32bit/FEATURES
%doc 32bit/doc/libxslt-api.xml
%doc 32bit/doc/libxslt-refs.xml
%doc 32bit/doc/EXSLT/libexslt-api.xml
%doc 32bit/doc/EXSLT/libexslt-refs.xml
%doc 32bit/doc/*.html 32bit/doc/html 32bit/doc/tutorial 32bit/doc/tutorial2
%doc 32bit/doc/*.gif 32bit/doc/*.png 32bit/doc/images 32bit/doc/EXSLT
%{_bindir}/xslt-config*
%{_libdir}/*.sh
%{_libdir64}/*.sh
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*
%{_datadir}/aclocal/libxslt.m4


%files -n python2-%{name}
%defattr(-,root,system,-)
%doc 32bit/python/libxsltclass.txt
%doc 32bit/python/tests/*.py
%doc 32bit/python/tests/*.xml
%doc 32bit/python/tests/*.xsl
%{python_sitearch}/libxslt.py*
%{python64_sitearch}/libxslt.py*
%{python_sitearch}/libxsltmod*
%{python64_sitearch}/libxsltmod*


%changelog
* Mon Jan 06 2020 Tony Reix <tony.reix@atos.net> -1.1.34-1
- Updated to 1.1.34
- Move to new brpm rules

* Tue Mar 20 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> -1.1.32-1
- Updated to 1.1.32 

* Thu Nov 16 2017 Michael Perzl <michael@perzl.org> - 1.1.31-1
- updated to version 1.1.31

* Mon Sep 18 2017 Michael Perzl <michael@perzl.org> - 1.1.30-1
- added RTL-style shared libraries
- updated to version 1.1.30

* Mon May 30 2016 Michael Perzl <michael@perzl.org> - 1.1.29-1
- updated to version 1.1.29

* Wed Jun 12 2013 Michael Perzl <michael@perzl.org> - 1.1.28-2
- rebuilt to fix segmentation faults

* Thu Dec 13 2012 Michael Perzl <michael@perzl.org> - 1.1.28-1
- updated to version 1.1.28

* Tue Oct 16 2012 Michael Perzl <michael@perzl.org> - 1.1.27-1
- updated to version 1.1.27

* Wed Nov 16 2011 Michael Perzl <michael@perzl.org> - 1.1.26-2
- added missing 64-bit shared library libexslt.so.1

* Thu Nov 19 2009 Michael Perzl <michael@perzl.org> - 1.1.26-1
- updated to version 1.1.26

* Fri May 16 2008 Michael Perzl <michael@perzl.org> - 1.1.24-1
- updated to version 1.1.24

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 1.1.22-2
- some minor spec file fixes

* Tue Jan 15 2008 Michael Perzl <michael@perzl.org> - 1.1.22-1
- first version for AIX V5.1 and higher
