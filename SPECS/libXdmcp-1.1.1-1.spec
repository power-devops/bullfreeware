Name:          libXdmcp
Version:       1.1.1
Release:       1
Summary:       X.Org Xdmcp library
Group:		System/Libraries
URL:		http://www.x.org
Source:		http://www.x.org/releases/X11R7.7/src/lib/%{name}-%{version}.tar.gz
Patch0:         %{name}-%{version}-bash.patch
License:	MIT
BuildRoot:	/var/tmp/%{name}-%{version}-root
Obsoletes:     libXorg


%description
X.Org Xdmcp library

%package devel
Summary:       X.Org Xdmcp library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xdmcp library.

This package contains static libraries and header files need for development.


%prep
%setup -q
%patch0 -p1 -b .bash


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc_r -q64"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --enable-shared --disable-static
make

cp ./.libs/libXdmcp.so.6 .
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
	    --enable-shared --disable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
#Doesn't work ${AR} -q ./.libs/libXdmcp.a libXdmcp.so.6
rm -f ./.libs/libXdmcp.a
${AR} -r ./.libs/libXdmcp.a  ./.libs/libXdmcp.so.6  libXdmcp.so.6


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install


#(
#  cd ${RPM_BUILD_ROOT}
#    mkdir -p usr/include/X11
#    cd usr/include/X11
#    ln -sf ../../..%{_prefix}/include/X11/* .
#    cd -
#)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_libdir}/libXdmcp.a
%doc AUTHORS COPYING ChangeLog README


%files devel
%defattr(-,root,system)
%{_libdir}/libXdmcp.la
%{_includedir}/X11/*.h
#/usr/include/X11/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/libXdmcp


%changelog
* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.1-1
- Inital port on Aix6.1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.1.0
- Inital port on Aix 5.3

