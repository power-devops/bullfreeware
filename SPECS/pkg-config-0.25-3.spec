%define _libdir64 %{_prefix}/lib64

Summary: A tool for determining compilation options
Name: pkg-config
Version: 0.25
Release: 3
License: GPLv2+
URL: http://pkgconfig.freedesktop.org
Group: Development/Tools
Source0:  http://www.freedesktop.org/software/pkgconfig/releases/%{name}-%{version}.tar.gz
# https://bugs.freedesktop.org/show_bug.cgi?id=16095
Patch3: pkg-config-lib64-excludes.patch
# workaround for breakage with autoconf 2.66
# https://bugzilla.redhat.com/show_bug.cgi?id=611781
Patch4: pkg-config-dnl.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: patch

Obsoletes: pkgconfig < %{version}
Provides:  pkgconfig = %{version}


%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch3 -p0 -b .lib64
%patch4 -p1 -R -b .dnl

%build
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"
CC_prev="$CC"
export CC="$CC -q64"

# first compile pkg-config for 64-bit packages
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-pc-path=%{_libdir64}/pkgconfig
make %{?_smp_mflags} 
mv pkg-config pkg-config_64

make distclean

export CC="$CC_prev"
# now compile pkg-config for 32-bit packages
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-pc-path=%{_libdir}/pkgconfig
make %{?_smp_mflags} 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT}  install


cp pkg-config_64 ${RPM_BUILD_ROOT}%{_bindir}

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS README NEWS COPYING
%{_bindir}/*
%{_libdir}/pkgconfig
%{_libdir64}/pkgconfig
%{_datadir}/aclocal/*
%{_mandir}/man?/*
/usr/bin/*


%changelog
* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 0.25-3
- Initial port on Aix6.1

* Mon Jun 06 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.25-2
- Porting on Aix5.3

