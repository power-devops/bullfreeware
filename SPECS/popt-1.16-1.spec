Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	1
License:	 X Consortium
Group:		Development/Libraries
URL:		http://www.rpm5.org/
Source0:	http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gettext
Requires:	gettext

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

The library is available as 32-bit and 64-bit.

%prep
%setup -q


%build
export LDFLAGS="-L./.libs -L/opt/freeware/lib -bmaxdata:0x80000000 -blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib"

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
CFLAGS="-q64" \
CXXFLAGS="-q64" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make %{?_smp_mflags}

cp .libs/libpopt.so.0 .
make distclean

# now build the 32-bit version
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libpopt.a ./libpopt.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

cp .libs/libpopt.so.0 ${RPM_BUILD_ROOT}%{_libdir}
cd ${RPM_BUILD_ROOT}%{_libdir}
ln -s libpopt.so.0 libpopt.so
ln -s libpopt.so.0 libpopt.so.0.0.0

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


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGES COPYING README
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir}/*.la
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib/*.la
%{_includedir}/*
/usr/include/*
%{_mandir}/man3/*
%{_datadir}/locale/*


%changelog
* Fri May 13 2011 Patricia Cugny <patricia.cugny@bull.net> 1.16-1
- Update to version 1.16

* Thu Nov 5 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.14-1
- Update to version 1.14
