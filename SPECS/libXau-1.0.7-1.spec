Name:          libXau
Version:       1.0.7
Release:       1
Summary:       X.Org Xau library
Group:		System/Libraries
URL:		http://www.x.org
Source:		http://www.x.org/releases/X11R7.7/src/lib/%{name}-%{version}.tar.bz2
License:	MIT
BuildRoot:	/var/tmp/%{name}-%{version}-root
Obsoletes:     libXorg


%description
X.Org Xau library

%package devel
Summary:       X.Org Xau library
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Obsoletes:     libXorg-devel

%description devel
X.Org Xau library.

%prep
%setup -q

%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"
export LDFLAGS="-Wl,-blibpath:`pwd`/.libs:/opt/freeware/lib:/usr/vac/lib:/usr/lib:/lib"



# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc -q64"
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
	    --disable-selective-werror \
	    --disable-silent-rules
make

cp ./.libs/libXau.so.6 .
make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
	    --disable-selective-werror \
	    --disable-silent-rules
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects

# ${AR} -q ./.libs/libXau.a libXau.so.6 doesn't work
rm -f ./.libs/libXau.a
${AR} -r ./.libs/libXau.a ./.libs/libXau.so.6 libXau.so.6

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
%{_libdir}/libXau.a
%doc AUTHORS COPYING ChangeLog README


%files devel
%defattr(-,root,system)
%{_includedir}/X11/*.h
%{_libdir}/libXau.la
%{_libdir}/pkgconfig/*.pc
#/usr/include/X11/*.h
%{_mandir}/man3/*

%changelog
* Tue Apr 09 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.7-1
- Update to version 1.0.7-1

* Wed Jul 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.0.6-1
- Inital port on Aix 5.3

