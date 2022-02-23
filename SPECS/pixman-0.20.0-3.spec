Name:           pixman
Version:        0.20.0
Release:        3
Summary:        Pixel manipulation library
Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Source:         http://cairographics.org/releases/%{name}-%{version}.tar.gz
BuildRoot:      /var/tmp/%{name}-%{version}-root

%description
Pixman is a pixel manipulation library for X and cairo.


%package devel
Summary: Pixel manipulation library development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development library for pixman


%prep
%setup -q


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"

LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure --enable-shared --disable-static \
    --disable-gcc-inline-asm --disable-timers \
    --prefix=%{_prefix}

make 

cp %{name}/.libs/libpixman-1.so.0 .
make distclean


# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"

LIBPATH="%{_libdir}:/usr/lib" \
./configure --enable-shared --disable-static \
    --disable-gcc-inline-asm --disable-timers \
    --prefix=%{_prefix}

make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q %{name}/.libs/lib%{name}-1.a ./lib%{name}-1.so.0


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

cd $RPM_BUILD_ROOT
for dir in include lib
do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
done


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system,-)
%{_libdir}/libpixman*.a
/usr/lib/libpixman*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/pixman-1/*.h
%{_libdir}/libpixman*.la
%{_libdir}/pkgconfig/*.pc
/usr/lib/libpixman*.la


%changelog
* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.20.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 08 2011  Gerard Visiedo <gerard.visiedo@bull.net> - 0.20.0-2
- Add 64bit libraries

* Wed Nov 10 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> - 0.20.0-1
- First port for AIX5.3
