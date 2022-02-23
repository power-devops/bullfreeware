Summary: X.Org X11 libXft runtime library
Name: libXft
Version: 2.2.0
Release: 3
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Prefix: %{_prefix} 

%define _libdir64 %{_prefix}/lib64

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: %{name}.so.0-aix32
Source2: %{name}.so.0-aix64

#BuildRequires: libXrender-devel >= 0.9.5
BuildRequires: freetype2-devel >= 2.3.5
BuildRequires: fontconfig-devel >= 2.5.0
BuildRequires: pkg-config, xorg-compat-aix

#Requires:      libXrender >= 0.9.5
Requires:      freetype2 >= 2.3.5
Requires:      fontconfig >= 2.5.0

Provides:      xft

%description
X.Org X11 libXft runtime library

The library is available as 32-bit and 64-bit.


%package devel
Summary: X.Org X11 libXft development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXft development package

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xLC_r"

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
CC_prev="$CC"
export CC="$CC -q64"
LDFLAGS="-L/opt/freeware/lib -L/usr/lib64" \
LIBS=' -lXrender' \
./configure \
    --verbose  \
    --libdir=%{_libdir64} \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make %{?_smp_mflags} 

cp src/.libs/%{name}.so.2 .
make distclean

# now build the 32-bit version
export CC="$CC_prev"
LDFLAGS="-L/opt/freeware/lib -L/usr/lib" \
LIBS=' -lXrender' \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make %{?_smp_mflags} 



%install
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.2

# Add the older shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} %{name}.so.0
/usr/bin/strip -X32 -e %{name}.so.0
/usr/bin/ar -X32 -q src/.libs/%{name}.a %{name}.so.0
cp %{SOURCE2} %{name}.so.0
/usr/bin/strip -X64 -e %{name}.so.0
/usr/bin/ar -X64 -q src/.libs/%{name}.a %{name}.so.0
cp src/.libs/%{name}.a ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a
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
%defattr(-,root,system,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%dir %{_includedir}/X11
%dir %{_includedir}/X11/Xft
%{_includedir}/X11/Xft/Xft.h
%{_includedir}/X11/Xft/XftCompat.h
%{_libdir}/*.la
%{_libdir}/pkgconfig/xft.pc
%{_mandir}/man3/Xft.3


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net>  2.2.0-3
- Initial port on Aix6.1

* Mon Sep 26 2011 Patricia Cugny <patricia.cugny@bull.net> 2.2.0-2
- rebuild for compatibility with new libiconv.a 1.13.1-2
