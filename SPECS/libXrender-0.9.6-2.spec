Summary: X.Org X11 libXrender runtime library
Name: libXrender
Version: 0.9.6
Release: 2
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
Source1: %{name}.so.0-aix32
Source2: %{name}.so.0-aix64
Patch0: %{name}-%{version}-aix.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: pkg-config, patch, xorg-compat-aix
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%else
Requires: AIX-rpm < 6.1.0.0
%endif

Provides: xrender

%description
X.Org X11 libXrender runtime library

The library is available as 32-bit and 64-bit.


%package devel
Summary: X.Org X11 libXrender development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org X11 libXrender development package

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -b .aix


%build
# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
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

CC_prev="$CC"
export CC="$CC -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

cp src/.libs/%{name}.so.1 .
make distclean

# now build the 32-bit version
export CC="$CC_prev"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.1

# Add the older shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} %{name}.so.0
/usr/bin/strip -X32 -e %{name}.so.0
/usr/bin/ar -X32 -q src/.libs/%{name}.a %{name}.so.0
cp %{SOURCE2} %{name}.so.0
/usr/bin/strip -X64 -e %{name}.so.0
/usr/bin/ar -X64 -q src/.libs/%{name}.a %{name}.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

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
%defattr(-,root,system,-)
%doc AUTHORS COPYING ChangeLog
%{_prefix}/lib/*.a
%ifnos aix6.1
/usr/lib/*.a
%endif


%files devel
%defattr(-,root,system,-)
%dir %{_prefix}/include/X11
%dir %{_prefix}/include/X11/extensions
%{_prefix}/include/X11/extensions/Xrender.h
%{_prefix}/lib/*.la
%{_prefix}/lib/pkgconfig/xrender.pc
/usr/lib/*.la


%changelog
* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 0.9.6-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-1
- Initial porting on platform Aix5.3 

