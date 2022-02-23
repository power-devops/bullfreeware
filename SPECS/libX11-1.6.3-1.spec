Name:          libX11
Version:       1.6.3
Release:       1
Summary:       X.Org X11 library
Group:		System/Libraries
URL:		http://www.x.org
#Old Source:	http://www.x.org/releases/X11R7.6/src/lib/%{name}-%{version}.tar.gz
Source0: 	http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.bz2
Patch2: %{name}-%{version}-dont-forward-keycode-0.patch
License:	MIT

#Old 1.5.0
#BuildRequires: fixesproto-devel >= 4.0
#BuildRequires: kbproto-devel >= 1.0
#BuildRequires: xextproto-devel >= 7.2
#BuildRequires: inputproto-devel >= 2.0
#BuildRequires: xproto-devel >= 7.0
#BuildRequires: xcb-proto >= 1.6
#BuildRequires: libXau-devel >= 1.0.1
#BuildRequires: libXdmcp-devel >= 1.0.1
#BuildRequires: libxcb-devel >= 1.0
#BuildRequires: xtrans-devel
#Obsoletes:     libXorg

BuildRequires: xorg-x11-util-macros >= 1.11
BuildRequires: xproto-devel >= 7.0.15
BuildRequires: xtrans-devel >= 1.0.3-4
BuildRequires: libxcb-devel >= 1.2
BuildRequires: libXau
BuildRequires: libXdmcp
BuildRequires: perl(Pod::Usage)
BuildRequires: inputproto-devel >= 2.0


BuildRoot:     %{_tmppath}/%{name}-%{version}-root
BuildRoot:	/var/tmp/%{name}-%{version}-root

%description
X.Org Xext library
Core X11 protocol client library.


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
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
#export CFLAGS="-O2"
export CFLAGS="-g"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
export OBJECT_MODE=64
CONFIG_SHELL=/usr/bin/sh \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--enable-shared \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules

gmake

(gmake -k check || true)


cp src/.libs/libX11-xcb.so.1 .
cp src/.libs/libX11.so.6 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
export OBJECT_MODE=32
CONFIG_SHELL=/usr/bin/sh \
./configure \
	--prefix=%{_prefix} \
        --mandir=%{_mandir} \
	--enable-shared \
        --enable-static \
        --disable-selective-werror \
        --disable-silent-rules

gmake

(gmake -k check || true)


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm -f  src/.libs/libX11-xcb.a
rm -f src/.libs/libX11.a
${AR} -q src/.libs/libX11-xcb.a  src/.libs/libX11-xcb.so.1 libX11-xcb.so.1
${AR} -q src/.libs/libX11.a src/.libs/libX11.so.6 libX11.so.6


%install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
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
%{_prefix}/share/X11/Xcms.txt
%{_libdir}/libX11*.la

#%dir %{_includedir}/X11
%{_includedir}/X11/*.h
#%{_includedir}/X11/ImUtil.h
#%{_includedir}/X11/XKBlib.h
#%{_includedir}/X11/Xcms.h
#%{_includedir}/X11/Xlib.h
#%{_includedir}/X11/XlibConf.h
#%{_includedir}/X11/Xlibint.h
#%{_includedir}/X11/Xlib-xcb.h
#%{_includedir}/X11/Xlocale.h
#%{_includedir}/X11/Xregion.h
#%{_includedir}/X11/Xresource.h
#%{_includedir}/X11/Xutil.h
#%{_includedir}/X11/cursorfont.h

%{_libdir}/pkgconfig/*.pc
#%{_libdir}/pkgconfig/x11.pc
#%{_libdir}/pkgconfig/x11-xcb.pc

%dir %{_docdir}/libX11-%{version}
%{_docdir}/libX11-%{version}/*
%{_datadir}/doc/libX11/*

%{_mandir}/man*/*
#%{_mandir}/man3/*.3*
#%{_mandir}/man5/*.5*


%changelog
* Tue Apr 12 2016 Tony Reix <tony.reix@bull.net> - 1.6.3-1
- Inital port of version 1.6.3 on AIX 6.1

* Wed Apr 10 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.5.0-1
- Inital port on AIX 6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.4.0
- Inital port on Aix 5.3

