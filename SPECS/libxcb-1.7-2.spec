Name:          libxcb
Version:       1.7
Release:       2
Summary:       X.Org xcb library
Group:		System/Libraries
URL:		http://www.x.org
Source:		http://www.x.org/releases/X11R7.6/src/xcb/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-aix64bit.patch
License:	MIT
BuildRoot:	/var/tmp/%{name}-%{version}-root
Obsoletes:     libXorg


%description
X.Org xcb library

%package devel
Summary:       X.Org xcb library
Group:         Development/Libraries
Obsoletes:     libXorg-devel

%description devel
X.Org xcb library.

This package contains static libraries and header files need for development.


%prep
%setup -q
%patch0 -p1 -b .aix64bit

%build
# setup environment for 32-bit and 64-bit builds

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vac/bin/xlC_r -q64"
export OBJECT_MODE=64
export LIBS="-lpthread"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure --prefix=%{_prefix} \
	    --mandir=%{_mandir} \
         --enable-shared --disable-static

make

LISTLIB="libxcb 
libxcb-composite
libxcb-record
libxcb-sync
libxcb-xtest 
libxcb-damage
libxcb-render
libxcb-xevie
libxcb-xv 
libxcb-dpms
libxcb-res
libxcb-xf86dri
libxcb-xvmc
libxcb-dri2
libxcb-screensaver
libxcb-xfixes
libxcb-glx
libxcb-shape
libxcb-xinerama 
libxcb-randr
libxcb-shm
libxcb-xprint"

for lib in ${LISTLIB}
do
   if [ ${lib} = "libxcb" ]
   then
	cp src/.libs/${lib}.so.1 ${lib}.so.1
   else
	cp src/.libs/${lib}.so.0 ${lib}.so.0
   fi
done

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vac/bin/xlC_r"
export OBJECT_MODE=32
export LIBS="-lpthread"
LIBPATH="%{_libdir}:/usr/lib" \
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --enable-shared --disable-static
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
#Doesn't work ${AR} -q libxcb/.libs/libxcb.a libxcb.so.1
for lib in ${LISTLIB}
do
   rm -f src/.libs/${lib}.a
   if [ ${lib} = "libxcb" ]
   then
	 ${AR} -r src/.libs/${lib}.a src/.libs/${lib}.so.1 ${lib}.so.1
   else
	 ${AR} -r src/.libs/${lib}.a src/.libs/${lib}.so.0 ${lib}.so.0
   fi
done


%install
export AR="/usr/bin/ar -X32_64"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# Due to an inexpected rebuild of the librairy, we force to copy into the
# BUIL_ROOT directory, the library whith the objects with 32 and 64 bit.
#

LISTLIB="libxcb 
libxcb-composite
libxcb-record
libxcb-sync
libxcb-xtest 
libxcb-damage
libxcb-render
libxcb-xevie
libxcb-xv 
libxcb-dpms
libxcb-res
libxcb-xf86dri
libxcb-xvmc
libxcb-dri2
libxcb-screensaver
libxcb-xfixes
libxcb-glx
libxcb-shape
libxcb-xinerama 
libxcb-randr
libxcb-shm
libxcb-xprint"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
#Doesn't work ${AR} -q libxcb/.libs/libxcb.a libxcb.so.1
for lib in ${LISTLIB}
do
   rm -f src/.libs/${lib}.a
   if [ ${lib} = "libxcb" ]
   then
	 ${AR} -r src/.libs/${lib}.a src/.libs/${lib}.so.1 ${lib}.so.1
   else
	 ${AR} -r src/.libs/${lib}.a src/.libs/${lib}.so.0 ${lib}.so.0
   fi
done

for lib in ${LISTLIB}
do
   cp src/.libs/${lib}.a ${RPM_BUILD_ROOT}%{_libdir}
done


(
  cd ${RPM_BUILD_ROOT}
    mkdir -p usr/lib; cd usr/lib; ln -sf ../..%{_prefix}/lib/* .
    cd -
    mkdir -p usr/include/xcb ; cd usr/include/xcb; ln -sf ../../..%{_prefix}/include/xcb/* .
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%{_libdir}/*.a
/usr/lib/*.a
%doc INSTALL NEWS COPYING README


%files devel
%defattr(-,root,system)
%{_libdir}/libxcb*.la
%{_includedir}/xcb/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/libxcb
/usr/include/xcb/*.h
/usr/lib/*.la


%changelog
* Mon Oct 03 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.9.6-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 01 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.7-1
- Inital port on Aix 5.3

