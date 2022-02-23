%define soname 7
%define _libdir64 %{_prefix}/lib64


#################################
#  End of user-modifiable configs
#################################
%define name protobuf
%define version 2.4.1
%define release 1
%define javadir %{_prefix}/java


%define libdir64 %{_prefix}/lib64

Summary: Protocol Buffers - Google's data interchange format
Name: %{name}
Version: %{version}
Release: %{release}
License: SD-3-Clause
Group: Development/Libraries/C and C++
URL: http://code.google.com/p/protobuf/
Source0: http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0: protobuf-%{version}-gtest-port.patch
Patch1: protobuf-%{version}-cpp_unittest.patch
Source1: setuptools-0.6c11-py2.7.egg
Source2: manifest.txt.in

# Needed to rebootstrap with gtest 1.5.0
BuildRequires:  libtool
BuildRequires:  zlib-devel
# Java 1.6 required
#BuildRequires:  java-devel >= 1.6.0
# Python required
BuildRequires:  python
BuildRequires:  python-devel
#BuildRequires:  python-setuptools


BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif
#%define buildhost ppc-aix6.1.0.0



%description
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats. 

%package libprotoc
Summary:        Protocol Buffers - Google's data interchange format
Group:          System/Libraries

%description libprotoc
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats. 

%package lite
Summary:        Protocol Buffers - Google's data interchange format
Group:          System/Libraries

%description lite
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats. 

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries/C and C++
Requires:       gcc-c++
Requires:       protobuf
Requires:       protobuf-lite
Provides:       protobuf-devel = %version
Requires:       zlib-devel
#BuildRequires:  pkg-config

%description devel
Development files for Google Protocol Buffers

%package java
#Requires:       java >= 1.6.0
Summary:        Java Bindings for Google Protocol Buffers
Group:          Development/Libraries/Java

%description java
This package contains the Java bindings for Google Protocol Buffers.

%package python
Requires:       python
Summary:        Python Bindings for Google Protocol Buffers
Group:          Development/Libraries/Python

%description python
This package contains the Python bindings for Google Protocol Buffers.

%prep

%setup -q
%patch0 -p1 -b .port
%patch1 -p1 -b .unittest

%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"

export PTHREAD_LIBS=-lpthread

# 64 bit
export CC="/usr/bin/xlc -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"
export OBJECT_MODE=64
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qnamemangling=v5 -qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"
./configure --prefix=/opt/freeware \
         --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
         --disable-static
cp %{SOURCE1} %{_prefix}/src/packages/BUILD/protobuf-2.4.1/python
make

mkdir src/.libs64
cp  -P src/.libs/*so* src/.libs64

make distclean


# 32 bit 
export CC="/usr/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"
export OBJECT_MODE=32
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qnamemangling=v5 -qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"
autoreconf -fiv
./configure --prefix=/opt/freeware \
	 --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
	 --disable-static
cp %{SOURCE1} %{_prefix}/src/packages/BUILD/protobuf-2.4.1/python
make 


# create .a with the 64-bit shared objects and the  32-bit shared objects
${AR} -q src/.libs/libprotobuf-lite.a  src/.libs/libprotobuf-lite.so.7.0.0 src/.libs64/libprotobuf-lite.so.7.0.0
${AR} -q src/.libs/libprotobuf.a  src/.libs/libprotobuf.so.7.0.0 src/.libs64/libprotobuf.so.7.0.0
${AR} -q src/.libs/libprotoc.a  src/.libs/libprotoc.so.7.0.0 src/.libs64/libprotoc.so.7.0.0


# Java 
cd java
../src/protoc --java_out=src/main/java -I../src ../src/google/protobuf/descriptor.proto
mkdir classes
javac $extra_java_flags -d classes src/main/java/com/google/protobuf/*.java
sed -e 's/@VERSION@/%version/' < %{SOURCE2} > manifest.txt
jar cfm %{name}-java-%{version}.jar manifest.txt -C classes com
cd ..

# python build
cd python
python setup.py build
cd ..


#%check
#%{__make} check %{?jobs:-j%jobs}

%install
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export PTHREAD_LIBS=-lpthread
export OBJECT_MODE=32
export CC="/usr/bin/xlc"
export CXX="/usr/vacpp/bin/xlC_r"
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qnamemangling=v5 -qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"

echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install prefix=%{prefix}
mv $RPM_BUILD_ROOT/%{prefix}/bin/ppc-aix6.1.0.0-protoc $RPM_BUILD_ROOT/%{prefix}/bin/protoc

# no need for .la files
rm %{buildroot}%{_libdir}/*.la

cp  %{prefix}/src/packages/BUILD/protobuf-%{version}/src/.libs/*.a $RPM_BUILD_ROOT/%{prefix}/lib

mkdir  $RPM_BUILD_ROOT/%{prefix}/lib64
cp  -P %{prefix}/src/packages/BUILD/protobuf-%{version}/src/.libs64/* $RPM_BUILD_ROOT/%{prefix}/lib64
#%{__ln_s} libprotobuf-lite.so.7.0.0 libprotobuf-lite.so
#%{__ln_s} libprotobuf.so.7.0.0 libprotobuf.so
#%{__ln_s} libprotoc.so.7.0.0 libprotoc.so
cd $RPM_BUILD_ROOT/%{prefix}/lib64  
%{__ln_s}  ../lib/*.a .
cd -
#cd $RPM_BUILD_ROOT/%{prefix}/lib
#%{__ln_s} libprotobuf-lite.so.7.0.0 libprotobuf-lite.so
#%{__ln_s} libprotobuf.so.7.0.0 libprotobuf.so
#%{__ln_s} libprotoc.so.7.0.0 libprotoc.so
#cd -
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
%{__ln_s} ../../opt/freeware/lib/libproto* .
cd -
mkdir -p $RPM_BUILD_ROOT/usr/lib64
cd $RPM_BUILD_ROOT/usr/lib64
%{__ln_s} ../../opt/freeware/lib64/libproto* .
cd -


#%if %{with protobuf_java}
#pushd java
#%__install -D -m 0644 %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-java-%{version}.jar
#%__ln_s %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-java.jar
#%__ln_s %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
#popd
#%endif
# java
cd java
mkdir -p  %{buildroot}%{javadir}/%{name}
cp %{name}-java-%{version}.jar %{buildroot}%{javadir}/%{name}/%{name}-java-%{version}.jar
%__ln_s %{name}-java-%{version}.jar %{buildroot}%{javadir}/%{name}/%{name}-java.jar
%__ln_s %{name}-java-%{version}.jar %{buildroot}%{javadir}/%{name}/%{name}.jar
cd ..

# python
cd python
python setup.py install --skip-build \
	--prefix=%{_prefix} \
	--install-data=$RPM_BUILD_ROOT \
	--root  $RPM_BUILD_ROOT \
	--record=INSTALLED_FILES
cd ..

#%if 0%{?suse_version} > 1010
#%fdupes %{buildroot}%{py_sitedir}/%{name}-%{version}-py%{py_ver}.egg-info
#%endif

%clean
rm -rf $RPM_BUILD_ROOT;


%files
%defattr(-, root, root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{_libdir}/libprotobuf.so.%{soname}*
%{_libdir}/libprotobuf.so
%{_libdir}/libprotobuf.a
%{_libdir64}/libprotobuf.so.%{soname}*
%{_libdir64}/libprotobuf.so
%{_libdir64}/libprotobuf.a
/usr/lib/libprotobuf.*
/usr/lib64/libprotobuf.*

%files libprotoc
%defattr(-, root, root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{_libdir}/libprotoc.so.%{soname}*
%{_libdir}/libprotoc.so
%{_libdir}/libprotoc.a
%{_libdir64}/libprotoc.so.%{soname}*
%{_libdir64}/libprotoc.so
%{_libdir64}/libprotoc.a
/usr/lib/libprotoc.*
/usr/lib64/libprotoc.*

%files lite
%defattr(-, root, root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{_libdir}/libprotobuf-lite.so.%{soname}*
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf-lite.a
%{_libdir64}/libprotobuf-lite.so.%{soname}*
%{_libdir64}/libprotobuf-lite.so
%{_libdir64}/libprotobuf-lite.a
/usr/lib/libprotobuf-lite.*
/usr/lib64/libprotobuf-lite.*

%files devel
%defattr(-,root,root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%doc examples
%{_bindir}/protoc
%{_includedir}/google
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_libdir64}/*.so
%{_libdir64}/*.a
#%{_datadir}/vim
/usr/lib/*
/usr/lib64/*

# java
%files java
%defattr(-,root,root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{javadir}/%{name}/protobuf*

# python
#%files -n python-%{name} -f python/INSTALLED_FILES
%files python
%defattr(-,root,root)
%doc COPYING.txt 
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{_libdir}/python2.7/site-packages/*

%changelog
* Fri May 3 2013 by Bernard CAHEN <bernard.cahen@bull.net> 2.4.1-1
- Port on AIX 6.1 
