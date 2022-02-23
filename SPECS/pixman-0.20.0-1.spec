Name:           pixman
Version:        0.20.0
Release:        1
Summary:        Pixel manipulation library
Group:          System Environment/Libraries
License:        MIT
URL:            http://cgit.freedesktop.org/pixman/
Source:         http://cairographics.org/releases/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

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
./configure --enable-shared --disable-static \
    --disable-gcc-inline-asm --disable-timers \
    --prefix=%{_prefix}

make 

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
* Wed Nov 10 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> - 0.20.0-1
- First port for AIX5.3
