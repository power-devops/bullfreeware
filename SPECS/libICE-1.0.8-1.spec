Name:          libICE
Version:       1.0.8
Release:       1
Summary:       X.Org ICE library
Group:         System/Libraries
URL:           http://x.org
Source:        ftp://ftp.x.org/pub/individual/lib/libICE-%{version}.tar.bz2
License:       MIT
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
#BuildRequires: xorg-proto-devel >= 7.1
BuildRequires: xorg-xtrans-devel >= 1.0
Obsoletes:     libXorg
%define _libdir64 %{_prefix}/lib64

%description
X.Org ICE library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
X.Org ICE library.

This package contains static libraries and header files need for development.

%prep
%setup -q -n libICE-%{version}

%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/usr/bin/sh
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"

./configure \
	--prefix=%{_prefix} \
	--enable-shared \
	--disable-static
make

cp ./src/.libs/libICE.so.6 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"

./configure \
        --prefix=%{_prefix} \
        --enable-shared \
        --disable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm -f src/.libs/libICE.a
/usr/bin/ar -X32_64  -r src/.libs/libICE.a src/.libs/libICE.so.6 ./libICE.so.6
# add the 64-bit Aix library to the local shared library
cd /tmp
rm -f shr.o shr_64.o
ar -X32_64 -x /usr/lpp/X11/lib/R7/libICE.a
cd -
ar -X32_64 -r src/.libs/%{name}.a /tmp/shr.o /tmp/shr_64.o
rm -f /tmp/shr.o /tmp/shr_64.o


%install
[ "${RPM_BUILD_ROOT}" != / ] && rm -rf "${RPM_BUILD_ROOT}"
make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}
cp ./src/.libs/libICE.so.6 ${RPM_BUILD_ROOT}%{_libdir}
cp ./libICE.so.6 ${RPM_BUILD_ROOT}%{_libdir64}

(
cd $RPM_BUILD_ROOT
for dir in lib lib64
do
   cd ./%{_prefix}/${dir}
   ln -s %{name}.so.6 %{name}.so
   cd -
done
for dir in lib lib64
do
   mkdir -p usr/${dir}
   cd usr/${dir}
   ln -sf ../..%{_prefix}/${dir}/*.so* .
   ln -sf ../..%{_prefix}/${dir}/*.la .
   cd -
done
#mkdir -p usr/include/X11/ICE
#cd usr/include/X11/ICE
#ln -sf ../../../..%{_prefix}/include/X11/ICE/* .
)

%clean
[ "${RPM_BUILD_ROOT}" != / ] && rm -rf "${RPM_BUILD_ROOT}"


%files
%defattr(-,root,system)
%{_libdir}/libICE.a
%{_libdir}/libICE.so.6
%{_libdir64}/libICE.so.6
%doc AUTHORS COPYING ChangeLog
%{_datadir}/doc/libICE
/usr/lib/*.so.6
/usr/lib64/*.so.6

%files devel
%defattr(-,root,system)
%{_libdir}/libICE.la
%{_libdir}/libICE.so
%{_libdir64}/libICE.so
%dir %{_includedir}/X11/ICE
%{_includedir}/X11/ICE/*.h
%{_libdir}/pkgconfig/*.pc
/usr/lib/*.la
/usr/lib/*.so
/usr/lib64/*.so
#/usr/include/X11/ICE/*

%changelog
* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.8-1
- Update to version 1.0.8-1

* Thu Sep 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-2
- Add shr.o and shr_64.o AIX R7 libICE library to the new libICE.a library

* Fri Jul 20 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-1
- Initial port on Aix6.1

