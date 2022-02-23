Summary: X.Org X11 libXcursor runtime library
Name: libXcursor
Version: 1.1.11
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
#Patch0: %{name}-%{version}-aix.patch

BuildRequires: pkg-config
BuildRequires: xorg-compat-aix
BuildRequires: libXrender-devel >= 0.9.5
Requires: libXrender >= 0.9.5
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
%else
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
%else
Requires: AIX-rpm < 6.1.0.0
%endif

Provides: xcursor

%description
X.Org X11 libXcursor runtime library

The library is available as 32-bit and 64-bit.


%package devel
Summary: X.Org X11 libXcursor development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
X.Org X11 libXcursor development package

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
%setup -q


%build
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export LDFLAGS="-lXfixes"

# work around strange libtool error, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
#patch -p0 -s < %{PATCH0}
make 

cp src/.libs/%{name}.so.1 .
make distclean

# now build the 32-bit version

export CC="/usr/vac/bin/xlc_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
#patch -p0 -s < %{PATCH0}
make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# Due to an inexpected rebuild of the librairy, we force to copy into the
# BUIL_ROOT directory, the library whith the objects with 32 and 64 bit.
#
# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
rm  ./src/.libs/%{name}.a
/usr/bin/ar -X32_64 -q ./src/.libs/%{name}.a ./src/.libs/%{name}.so.1 ./%{name}.so.1
ar -tv -Xany  src/.libs/%{name}.a
cp ./src/.libs/%{name}.a ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a


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
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/*.a
%ifnos aix6.1
/usr/lib/*.a
%endif


%files devel
%defattr(-,root,system,-)
%dir %{_includedir}/X11/Xcursor
%{_includedir}/X11/Xcursor/Xcursor.h
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/Xcursor*.3*
/usr/lib/*.la


%changelog
* Tue Oct 18 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.11-1
- Initial port on Aix5.3

