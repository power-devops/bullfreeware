Summary: Library of graphics routines used by libgnomecanvas
Name: libart_lgpl
Version: 2.3.21
Release: 1
URL: http://www.gnome.org/
Source0: http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/%{name}-%{version}.tar.bz2
Source1: http://ftp.gnome.org/pub/gnome/sources/libart_lgpl/2.3/%{name}-%{version}.sha256sum
Source2: art_config.h
License: LGPLv2+
Group: System Environment/Libraries 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Graphics routines used by the GnomeCanvas widget and some other 
applications. libart renders vector paths and the like.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Libraries and headers for libart_lgpl
Group: Development/Libraries
Requires: %name = %{version}-%{release}

%description devel
Graphics routines used by the GnomeCanvas widget and some other 
applications. libart renders vector paths and the like.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make 

cp .libs/libart_lgpl_2.so.2 .
mv art_config.h art_config-ppc64.h
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make

cp art_config.h art_config-ppc32.h

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libart_lgpl_2.a ./libart_lgpl_2.so.2

cp %{SOURCE2} .


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

cp art_config-ppc??.h ${RPM_BUILD_ROOT}%{_includedir}/libart-2.0/libart_lgpl/

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_includedir}/*
/usr/bin/*
/usr/lib/*.la
/usr/include/*


%changelog
* Fri Mar 23 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.3.21-1
- Initial port on Aix6.1
