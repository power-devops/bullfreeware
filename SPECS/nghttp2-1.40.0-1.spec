%bcond_without dotests

%define _libdir64 %{_libdir}64
Summary: Experimental HTTP/2 client, server and proxy
Name: nghttp2
Version: 1.40.0
Release: 1
License: MIT
URL: https://nghttp2.org/
Source0: https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log


Requires: libnghttp2 = %{version}-%{release}
%if %{with dotests}
BuildRequires: CUnit-devel
%endif


%description
This package contains the HTTP/2 client, server and proxy programs.


%package -n libnghttp2
Summary: A library implementing the HTTP/2 protocol
Requires: libgcc >= 6.3.0

%description -n libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Requires: libnghttp2 = %{version}-%{release}
Requires: pkgconfig

%description -n libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.


%prep
%setup -q
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export CC=/opt/freeware/bin/gcc

# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CFLAGS="-O2 -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

%configure --prefix=%{_prefix} \
    --libdir=%{_libdir64}

make %{?_smp_mflags} V=1

# build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CFLAGS="-O2 -maix32 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
%configure --prefix=%{_prefix} \
    --libdir=%{_libdir} 

make %{?_smp_mflags} V=1

/usr/bin/ar -X64 -q lib/.libs/libnghttp2.a ../64bit/lib/.libs/libnghttp2.so.14


%install
# install on 64bit mode
cd 64bit
export OBJECT_MODE=64

gmake install DESTDIR=${RPM_BUILD_ROOT}

# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32

gmake install DESTDIR=${RPM_BUILD_ROOT}

# lib64 libraries are link of lib librairies
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -sf ../lib/libnghttp2.a .
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
gmake -k check
cd ../32bit
export OBJECT_MODE=32
gmake -k check
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_datadir}/nghttp2
%{_mandir}/man1/*

%files -n libnghttp2
%defattr(-,root,system,-)
%{_libdir}/libnghttp2.a
%{_libdir64}/libnghttp2.a
%doc 32bit/COPYING

%files -n libnghttp2-devel
%defattr(-,root,system,-)
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/libnghttp2.pc
%{_libdir64}/pkgconfig/libnghttp2.pc
%doc 32bit/README.rst


%changelog
* Thu Feb 13 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.40.0-1
- New version 1.40.0

* Tue May 28 2019 Reshma V Kumar <reskumar@in.ibm.com> 1.38.0-1
- Initial port to AIX toolbox


