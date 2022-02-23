Name:          libXext
Version:       1.3.1
Release:       1
Summary:       X.Org Xext library
Group:         System/Libraries
URL:           http://x.org
Source:        http://ftp.x.org/pub/individual/lib/libXext-%{version}.tar.bz2
License:       MIT
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
Obsoletes:     libXorg

%description
X.Org Xext library.

%package devel
Summary:       Devel package for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xext library.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"

./configure \
	--prefix=%{_prefix} \
	--enable-static \
	--disable-selective-werror \
	--disable-silent-rules

make

cp src/.libs/%{name}.so.6 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"

./configure \
        --prefix=%{_prefix} \
        --enable-shared \
	--enable-static \
	--disable-selective-werror \
	--disable-silent-rules

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.6

%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f %{buildroot}%{_includedir}/X11/extensions/lbxbuf.h
rm -f %{buildroot}%{_includedir}/X11/extensions/lbxbufstr.h

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
#%{_libdir}/libXext.so.*
%{_libdir}/libXext.a
%doc AUTHORS COPYING ChangeLog

%files devel
%defattr(-,root,system)
%{_includedir}/X11/extensions/*.h
%{_libdir}/libXext.la
#%{_libdir}/libXext.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/man3/*
%dir %{_datadir}/doc/libXext
%{_datadir}/doc/libXext/*

%changelog
* Thu Apr 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.3.1-1
- Initial port on Aix6.1

* Tue May 10 2011 Automatic Build System <autodist@...> 1.3.0-1mamba
- automatic update by autodist

* Fri Dec 10 2010 Automatic Build System <autodist@...> 1.2.0-1mamba
- automatic update by autodist

* Fri Jul 02 2010 Silvan Calarco <silvan.calarco@...> 1.1.2-2mamba
- rebuilt to add pkgconfig provides

* Sat Jun 05 2010 Automatic Build System <autodist@...> 1.1.2-1mamba
- automatic update by autodist

