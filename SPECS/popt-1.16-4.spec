%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary:	C library for parsing command line parameters
Name:		popt
Version:	1.16
Release:	4
License:	 X Consortium
Group:		Development/Libraries
URL:		http://www.rpm5.org/
Source0:	http://www.rpm5.org/files/%{name}/%{name}-%{version}.tar.gz
Source100:  %{name}-%{version}-%{release}.build.log
BuildRequires:	gettext-devel
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

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
# export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L./.libs -L/opt/freeware/lib64 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

# first build the 64-bit version
# CFLAGS="-q64" \
# CXXFLAGS="-q64" \

export CC="/opt/freeware/bin/gcc -maix64"
export CXX="/opt/freeware/bin/g++ -maix64"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}

cp .libs/libpopt.so.0 .

cd ../32bit
export OBJECT_MODE=32
export LDFLAGS="-L./.libs -L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib"

export CC="/opt/freeware/bin/gcc -maix32"
export CXX="/opt/freeware/bin/g++ -maix32"

# now build the 32-bit version
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --enable-shared --disable-static
gmake %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libpopt.a ../64bit/libpopt.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

cp .libs/libpopt.so.0 ${RPM_BUILD_ROOT}%{_libdir64}
(
cd ${RPM_BUILD_ROOT}%{_libdir64}
ln -s libpopt.so.0 libpopt.so
ln -s libpopt.so.0 libpopt.so.0.0.0
)

cd ../32bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

cp .libs/libpopt.so.0 ${RPM_BUILD_ROOT}%{_libdir}
(
cd ${RPM_BUILD_ROOT}%{_libdir}
ln -s libpopt.so.0 libpopt.so
ln -s libpopt.so.0 libpopt.so.0.0.0
)

(
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/*.a .
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
gmake check || true
cd ../32bit
export OBJECT_MODE=32
gmake check || true
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/CHANGES 32bit/COPYING 32bit/README
%{_libdir}/*.a
%{_libdir64}/*.a
# used by rpm-devel-python
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_includedir}/*
%{_mandir}/man3/*
%{_datadir}/locale/*


%changelog
* Mon Apr 20 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.16-4
- Add check section
- Add link from lib to lib64
- Do not provide .la

* Tue Apr 3 2012 Patricia Cugny <patricia.cugny@bull.net> 1.16-2
- port on AIX 6.1

* Fri May 13 2011 Patricia Cugny <patricia.cugny@bull.net> 1.16-1
- Update to version 1.16

* Thu Nov 5 2009 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.14-1
- Update to version 1.14
