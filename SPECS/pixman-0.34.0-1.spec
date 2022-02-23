%define do_tests 0
Name:           pixman
Version:        0.34.0
Release:        1
Summary:        Pixel manipulation library
Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Source:         http://cairographics.org/releases/%{name}-%{version}.tar.gz
Patch0:         pixman-0.34.0-aix-tests.patch
BuildRoot:      /var/tmp/%{name}-%{version}-root
BuildRequires:  automake >= 1.15

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
%patch0 -p1

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit

# Build process requires aclocal and automake binaries names with version suffix
if [ ! -e /opt/freeware/bin/aclocal-1.15 ]; then
  ln -s /opt/freeware/bin/aclocal /opt/freeware/bin/aclocal-1.15
fi
if [ ! -e /opt/freeware/bin/automake-1.15 ]; then
  ln -s /opt/freeware/bin/aclocal /opt/freeware/bin/automake-1.15
fi


%build
export PATH=/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export SHELL=/opt/freeware/bin/bash
export LDFLAGS=
CONFIG_SHELL=/usr/bin/ksh
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --disable-static \
    --disable-gcc-inline-asm \
    --disable-timers
make %{?_smp_mflags}
%if %{do_tests} != 0
make check
slibclean
%endif

# now build the 32-bit version
cd ../32bit
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared \
    --disable-static \
    --disable-gcc-inline-asm \
    --disable-timers
make %{?_smp_mflags}
%if %{do_tests} != 0
make check
slibclean
%endif

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q  %{name}/.libs/lib%{name}-1.a ../64bit/%{name}/.libs/lib%{name}-1.so.0

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
cd 64bit
export OBJECT_MODE=64
make DESTDIR=$RPM_BUILD_ROOT install

cd ../32bit
export OBJECT_MODE=32
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
* Wed Apr 13 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 0.34.0-1
- Update to version 0.34.0

* Tue Jun 12 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.26.0-1
- Update to version 0.26.0

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.20.0-4
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.20.0-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Sep 08 2011  Gerard Visiedo <gerard.visiedo@bull.net> - 0.20.0-2
- Add 64bit libraries

* Wed Nov 10 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> - 0.20.0-1
- First port for AIX5.3
