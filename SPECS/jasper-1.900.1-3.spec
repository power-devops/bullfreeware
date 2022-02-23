Summary: Implementation of the JPEG-2000 standard, Part 1
Name:    jasper
Group:   System Environment/Libraries
Version: 1.900.1
Release: 2

License: JasPer License Version 2.0
URL:     http://www.ece.uvic.ca/~mdadams/jasper/
Source:  %{name}-%{version}.tar.bz2
Patch0:	 %{name}-%{version}-aixconf.patch
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: libjpeg-devel

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

The library is available as 32-bit and 64-bit.


%package devel
Summary: JPEG-2000 library developer files
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel

%description devel
%{summary}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0 -p1 -b .aixconf


%build
export CFLAGS="-O"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-opengl
make 

cp src/libjasper/.libs/libjasper.so.1 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static \
    --disable-opengl
make

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/libjasper/.libs/libjasper.a ./libjasper.so.1


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# avoid conflict(s) with tomcat
mv $RPM_BUILD_ROOT%{_bindir}/jasper $RPM_BUILD_ROOT%{_bindir}/jaspertool
mv $RPM_BUILD_ROOT%{_mandir}/man1/jasper.1 $RPM_BUILD_ROOT%{_mandir}/man1/jaspertool.1


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYRIGHT LICENSE NEWS README
%{_bindir}/*
%{_mandir}/*
%{_libdir}/lib*.a

%files devel
%defattr(-,root,root)
%doc doc/*
%{_includedir}/*
%{_libdir}/lib*.la


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 1.900.1-3
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.900.1-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Tue Sep 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> 1.900.1-1
- Initial port on Aix5.3


