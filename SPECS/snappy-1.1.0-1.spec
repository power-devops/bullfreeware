#
# spec file for package snappy
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           snappy
Version:        1.1.0
Release:        1
#
License:        MIT
Group:          Development/Libraries/C and C++
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gcc-c++ zlib-devel lzo-devel
#
Url:            http://code.google.com/p/snappy/
Source:         snappy-%{version}.tar.gz
Patch:          snappy-static-fct.patch

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%define _libdir64 %{_prefix}/lib64
%endif


#
Summary:        A fast compressor/decompressor library
%description
Snappy is a compression/decompression library. It does not aim for maximum compression, 
or compatibility with any other compression library; instead, it aims for very high 
speeds and reasonable compression. For instance, compared to the fastest mode of zlib, 
Snappy is an order of magnitude faster for most inputs, but the resulting compressed 
files are anywhere from 20% to 100% bigger. On a single core of a Core i7 processor 
in 64-bit mode, Snappy compresses at about 250 MB/sec or more and decompresses at about 
500 MB/sec or more.


This package holds the shared library of snappy.

%package devel
License:        MIT
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}
#
Summary:        Development files for snappy
%description devel
Snappy is a compression/decompression library. It does not aim for maximum compression, 
or compatibility with any other compression library; instead, it aims for very high 
speeds and reasonable compression. For instance, compared to the fastest mode of zlib, 
Snappy is an order of magnitude faster for most inputs, but the resulting compressed 
files are anywhere from 20% to 100% bigger. On a single core of a Core i7 processor 
in 64-bit mode, Snappy compresses at about 250 MB/sec or more and decompresses at about 
500 MB/sec or more.

This package holds the development files for snappy.

%prep
%setup
%patch0 -p1 -b .static

%build
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"


# 64 bit
export CC="/usr/bin/xlc -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"
export OBJECT_MODE=64
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"

%configure --prefix=%{_prefix} --with-pic --disable-static \
           --host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
make %{?_smp_flags}


mkdir .libs64
cp  -P .libs/*so* .libs64

make distclean


export CC="/usr/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"
export OBJECT_MODE=32
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"
%configure --prefix=%{_prefix} --with-pic --disable-static  \
           --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} 
make %{?_smp_flags}

# create .a with the 64-bit shared objects and the  32-bit shared objects
${AR} -q .libs/libsnappy.a  .libs/libsnappy.so.1.1.4 .libs64/libsnappy.so.1.1.4

make check

%install
rm -rf %{buildroot}

export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

%makeinstall
find %{buildroot} -name \*.la -delete -print
cp  %{_prefix}/src/packages/BUILD/%{name}-%{version}/.libs/*.a $RPM_BUILD_ROOT/%{_prefix}/lib

mkdir -p  $RPM_BUILD_ROOT/%{_prefix}/lib64
cp  -P %{_prefix}/src/packages/BUILD/%{name}-%{version}/.libs64/* $RPM_BUILD_ROOT/%{_prefix}/lib64
cd $RPM_BUILD_ROOT/%{_prefix}/lib64
%{__ln_s}  ../lib/*.a .
cd -
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
%{__ln_s} ../../opt/freeware/lib/libsnappy* .
cd -
mkdir -p $RPM_BUILD_ROOT/usr/lib64
cd $RPM_BUILD_ROOT/usr/lib64
%{__ln_s} ../../opt/freeware/lib64/libsnappy* .
cd -

%clean
rm -rf %{buildroot}

%files
%define _libdir64 /opt/freeware/lib64
%defattr(-,root,root,-)
%{_libdir}/libsnappy.a
%{_libdir}/libsnappy.so*
%{_libdir64}/libsnappy.a
%{_libdir64}/libsnappy.so*
/usr/lib/libsnappy.a
/usr/lib/libsnappy.so*
/usr/lib64/libsnappy.a
/usr/lib64/libsnappy.so*
%doc AUTHORS COPYING NEWS README 

%files devel
%defattr(-,root,root,-)
%{_includedir}/snappy-c.h
%{_includedir}/snappy-sinksource.h
%{_includedir}/snappy-stubs-public.h
%{_includedir}/snappy.h

%changelog


