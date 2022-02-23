Summary: Library providing the GNOME XSLT engine
Name: libxslt
Version: 1.1.26
Release: 2
License: MIT
Group: Development/Libraries
Source0: ftp://xmlsoft.org/XSLT/%{name}-%{version}.tar.gz
URL: http://xmlsoft.org/XSLT/
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: libxml2-devel >= 2.6.27
BuildRequires: libgcrypt-devel
Requires: libxml2 >= 2.6.27
Requires: libgcrypt

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
Requires: libxml2-devel >= 2.6.27
Requires: libgcrypt-devel
Requires: pkg-config

%description devel
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
%setup -q


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM='/usr/linux/bin/rm -f'
# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static 

make 


cp libexslt/.libs/libexslt.so.0 .
cp libxslt/.libs/libxslt.so.1 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make

gzip --best ChangeLog


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

# Due to an inexpected rebuild of the librairy, we force to copy into the
# BUIL_ROOT directory, the library whith the objects with 32 and 64 bit.
#
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm -f libexslt/.libs/libexslt.a libxslt/.libs/libxslt.a
/usr/bin/ar -X32_64  -r libexslt/.libs/libexslt.a libexslt/.libs/libexslt.so.0 libexslt.so.0
/usr/bin/ar -X32_64  -r libxslt/.libs/libxslt.a libxslt/.libs/libxslt.so.1 libxslt.so.1
cp libexslt/.libs/libexslt.a libxslt/.libs/libxslt.a ${RPM_BUILD_ROOT}%{_libdir}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS ChangeLog.gz NEWS README Copyright TODO FEATURES
%doc doc/*.html doc/html doc/tutorial doc/tutorial2 doc/*.gif
%doc doc/EXSLT
%{_bindir}/xsltproc
%{_libdir}/lib*.a
%{_libdir}/libxslt-plugins
%{_mandir}/man1/xsltproc.1
/usr/bin/xsltproc
/usr/lib/lib*.a


%files devel
%defattr(-,root,system)
%doc AUTHORS ChangeLog.gz NEWS README Copyright TODO FEATURES
%doc doc/libxslt-api.xml
%doc doc/libxslt-refs.xml
%doc doc/EXSLT/libexslt-api.xml
%doc doc/EXSLT/libexslt-refs.xml
%{_bindir}/xslt-config
%{_libdir}/lib*.la
%{_libdir}/*.sh
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*
%{_datadir}/aclocal/libxslt.m4
/usr/bin/xslt-config
/usr/lib/lib*.la
/usr/lib/*.sh


%changelog
* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.26-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri Aug 12 2011 Gerard Visiedo  <gerard.visiedo@bull.net> 1.1.26-1
- Initial port on Aix5.3 

