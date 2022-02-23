Name:          libX11
Version:       1.5.0
Release:       1
Summary:       X.Org X11 library
Group:		System/Libraries
URL:		http://www.x.org
Source:		http://www.x.org/releases/X11R7.6/src/lib/%{name}-%{version}.tar.gz
License:	MIT
BuildRequires: fixesproto-devel >= 4.0
BuildRequires: kbproto-devel >= 1.0
BuildRequires: xextproto-devel >= 7.2
BuildRequires: inputproto-devel >= 2.0
BuildRequires: xproto-devel >= 7.0
BuildRequires: xcb-proto >= 1.6
BuildRequires: libXau-devel >= 1.0.1
BuildRequires: libXdmcp-devel >= 1.0.1
BuildRequires: libxcb-devel >= 1.0
BuildRequires: xtrans-devel
Obsoletes:     libXorg
BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRoot:	/var/tmp/%{name}-%{version}-root

%description
X.Org Xext library

%package devel
Summary:	X.Org X11 library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libXau-devel >= 1.0.3
Requires:	libXdmcp-devel >= 1.0.2
Obsoletes:	libXorg-devel


%description devel
X.Org X11 library.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
export OBJECT_MODE=64
CONFIG_SHELL=/usr/bin/sh \
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	--enable-shared \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules
make

cp src/.libs/libX11-xcb.so.1 .
cp src/.libs/libX11.so.6 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
export OBJECT_MODE=32
CONFIG_SHELL=/usr/bin/sh \
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
	--enable-shared \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm -f  src/.libs/libX11-xcb.a
rm -f src/.libs/libX11.a
${AR} -q src/.libs/libX11-xcb.a  src/.libs/libX11-xcb.so.1 libX11-xcb.so.1
${AR} -q src/.libs/libX11.a src/.libs/libX11.so.6 libX11.so.6

%install
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install
# Due to issue copying libX11-xcb from BUILD
${RM} ${RPM_BUILD_ROOT}%{_libdir}/libX11-xcb.a
cp ${RPM_BUILD_DIR}/%{name}-%{version}/src/.libs/libX11-xcb.a ${RPM_BUILD_ROOT}%{_libdir}/libX11-xcb.a

#(
#  cd ${RPM_BUILD_ROOT}
#  mkdir -p usr/include/X11
#  cd usr/include/X11
#  ln -sf ../../..%{_prefix}/include/X11/* .
#  cd -
#)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#%post

#%postun


%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libX11*.a
%{_datadir}/X11/XErrorDB
%{_datadir}/X11/locale/*


%files devel
%defattr(-,root,system)
%{_libdir}/X11/Xcms.txt
%{_libdir}/libX11*.la
#%dir %{_includedir}/X11
%{_includedir}/X11/*.h
#/usr/include/X11/*.h
%{_libdir}/pkgconfig/*.pc
%dir %{_docdir}/libX11-%{version}
%{_docdir}/libX11-%{version}/*
%{_datadir}/doc/libX11/*
%{_mandir}/man*/*


%changelog
* Wed Apr 10 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.0-1
- Inital port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.4.0
- Inital port on Aix 5.3

