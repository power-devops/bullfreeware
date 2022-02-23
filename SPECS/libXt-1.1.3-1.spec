Name:          libXt
Version:       1.1.3
Release:       1
Summary:       X Toolkit Intrinsics library
Group:         System/Libraries
URL:           http://xorg.freedesktop.org
Source:        http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.bz2
License:       MIT
## AUTOBUILDREQ-BEGIN
#BuildRequires: glibc-devel
#BuildRequires: libICE-devel
#BuildRequires: libSM-devel
#BuildRequires: libX11-devel
#BuildRequires: libXau-devel
#BuildRequires: libXdmcp-devel
#BuildRequires: libpthread-stubs-devel
#BuildRequires: libuuid-devel
#BuildRequires: libxcb-devel
#BuildRequires: xproto-devel
## AUTOBUILDREQ-END
Obsoletes:     libXorg
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%define _libdir64 %{_prefix}/lib64

%description
X.Org Xt library.

%package devel
Summary:       Development files for the X Toolkit Intrinsics library
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
#Requires:       %lname = %version
Obsoletes:     libXorg-devel

%description devel
X.Org Xt library.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd`/src/.libs -L%{_prefix}/lib64 -L/usr/lib64 -L%{_libdir} -L/usr/lib -Wl,-brtl"
export DED_LD="ld -G -bnoentry -bexpall -b64"

autoconf
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
        --enable-shared \
	 --enable-static \
	--disable-selective-werror \
	--disable-silent-rules

make

cp src/.libs/libXt.so.6.0.0 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CFLAGS="-I`pwd`/include -I%{_includedir} -I/usr/include"
export LDFLAGS="-L`pwd`/src/.libs -L%{_libdir} -L/usr/lib -Wl,-brtl"
export DED_LD="ld -G -bnoentry -bexpall"
##export LIBS="-lXt"

autoconf
./configure \
        --prefix=%{_prefix} \
        --mandir=%{_mandir} \
        --enable-shared \
	--enable-static \
	--disable-selective-werror \
	--disable-silent-rules

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm -f src/.libs/libXt.a
${AR} -r src/.libs/libXt.a src/.libs/libXt.so.6.0.0 ./libXt.so.6.0.0

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
## %makeinstall
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%files
%defattr(-,root,system)
%{_libdir}/libXt.so.*
%{_libdir}/libXt.a
#%{_bindir}/makestrs
%doc COPYING ChangeLog

%files devel
%defattr(-,root,system)
%{_libdir}/libXt.la
%dir %{_includedir}/X11
%{_includedir}/X11/*.h
%{_exec_prefix}/lib/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Wed Apr 10 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.1.3-1
- Initial port on Aix6.1

* Mon May 02 2011 Silvan Calarco <silvan.calarco@mambasoft.it> 1.1.1-1mamba
- update to 1.1.1

