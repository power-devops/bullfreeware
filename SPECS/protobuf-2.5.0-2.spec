%define soname 8
%define _libdir64 %{_prefix}/lib64


#################################
#  End of user-modifiable configs
#################################
%define name protobuf
%define version 2.5.0
%define release 2
%define javadir %{_prefix}/java


%define libdir64 %{_prefix}/lib64

Summary: Protocol Buffers - Google's data interchange format
Name: %{name}
Version: %{version}
Release: %{release}
License: SD-3-Clause
Group: Development/Libraries/C and C++
URL: http://code.google.com/p/protobuf/
Source0: http://protobuf.googlecode.com/files/%{name}-%{version}.tar.gz
Source2: manifest.txt.in


Patch1:	%{name}-2.5.0-atomicops_internals_aix.h.patch

Patch2:	%{name}-2.5.0-int64.patch


# Needed to rebootstrap with gtest 1.5.0
BuildRequires:  libtool
BuildRequires:  zlib-devel
# Java 1.6 required
#BuildRequires:  java-devel >= 1.6.0
# Python required
BuildRequires:  python
BuildRequires:  python-devel
#BuildRequires:  python-setuptools
BuildRequires:  automake >= 1.14


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

%patch1 -p1
%patch2 -p1

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"

export PTHREAD_LIBS=-lpthread

# -DGOOGLE_PROTOBUF_OS_AIX is automatically set in code

# 64 bit
cd 64bit

export CC="gcc -maix64"
export CXX="g++ -maix64"
export OBJECT_MODE=64
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"
export LDFLAGS="-lbsd -Wl,-bbigtoc"

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir64} \
        --host=%{buildhost} \
	--target=%{buildhost} \
	--build=%{buildhost} \
        --disable-static

gmake -j8

( gmake -k check || true )
slibclean


# Old 32/64 method
#mkdir src/.libs64
#cp  -P src/.libs/*so* src/.libs64

# We keep the environment
#gmake distclean

echo ****** 64 Finished ******


# 32 bit 
cd ../32bit

export CC="gcc -maix32"
export CXX="g++ -maix32"
export OBJECT_MODE=32
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"
export LDFLAGS="-lbsd -lstdc++"

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir} \
	--host=%{buildhost} \
	--target=%{buildhost} \
	--build=%{buildhost} \
	--disable-static

gmake -j8

export CFLAGS="$CFLAGS -Wl,-bbigtoc"
( gmake -k check || true )
slibclean


cd ..

# create .a with the 64-bit shared objects and the  32-bit shared objects
${AR} -q libprotobuf-lite.a  32bit/src/.libs/libprotobuf-lite.so.8  64bit/src/.libs/libprotobuf-lite.so.8
#rm src/.libs/libprotobuf.a
${AR} -q libprotobuf.a       32bit/src/.libs/libprotobuf.so.8       64bit/src/.libs/libprotobuf.so.8
#rm src/.libs/libprotoc.a
${AR} -q libprotoc.a         32bit/src/.libs/libprotoc.so.8         64bit/src/.libs/libprotoc.so.8


# Java 
cd 32bit/java
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
echo "RPM_BUILD_ROOT: $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{prefix}/lib
mkdir -p $RPM_BUILD_ROOT/%{prefix}/lib64

export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export PTHREAD_LIBS=-lpthread

export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qnamemangling=v5 -qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"


cd 64bit
export OBJECT_MODE=64
export CC="gcc -maix64"
export CXX="g++ -maix64"
export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib -Wl,-brtl"

make DESTDIR=$RPM_BUILD_ROOT install prefix=%{prefix}

# no need for .la files
rm %{buildroot}%{_libdir64}/*.la


cd ../32bit
export OBJECT_MODE=32
export CC="gcc -maix32"
export CXX="g++ -maix32"
export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"

make DESTDIR=$RPM_BUILD_ROOT install prefix=%{prefix}

mv $RPM_BUILD_ROOT/%{prefix}/bin/ppc-aix6.1.0.0-protoc $RPM_BUILD_ROOT/%{prefix}/bin/protoc

# no need for .la files
rm %{buildroot}%{_libdir}/*.la

cd ..

cp  %{prefix}/src/packages/BUILD/protobuf-%{version}/32bit/src/.libs/*.a $RPM_BUILD_ROOT/%{prefix}/lib


ls -l  $RPM_BUILD_ROOT/%{prefix}/lib
ls -l  $RPM_BUILD_ROOT/%{prefix}/lib64


cd $RPM_BUILD_ROOT/%{prefix}/lib64
cp %{prefix}/src/packages/BUILD/protobuf-%{version}/64bit/src/.libs/lib*.so.* .
%{__ln_s} libprotobuf-lite.so.8 libprotobuf-lite.so
%{__ln_s} libprotobuf.so.8      libprotobuf.so
%{__ln_s} libprotoc.so.8        libprotoc.so

cd $RPM_BUILD_ROOT/%{prefix}/lib
cp %{prefix}/src/packages/BUILD/protobuf-%{version}/32bit/src/.libs/lib*.so.* .
%{__ln_s} libprotobuf-lite.so.8 libprotobuf-lite.so
%{__ln_s} libprotobuf.so.8      libprotobuf.so
%{__ln_s} libprotoc.so.8        libprotoc.so
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotobuf-lite.a $RPM_BUILD_ROOT/%{prefix}/lib64/libprotobuf-lite.so.8
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotobuf.a      $RPM_BUILD_ROOT/%{prefix}/lib64/libprotobuf.so.8
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotoc.a        $RPM_BUILD_ROOT/%{prefix}/lib64/libprotoc.so.8


cd $RPM_BUILD_ROOT/%{prefix}/lib64  
rm -f *.a
%{__ln_s}  ../lib/*.a .


ls -l  $RPM_BUILD_ROOT/%{prefix}/lib
ls -l  $RPM_BUILD_ROOT/%{prefix}/lib64


mkdir -p $RPM_BUILD_ROOT/usr/lib64
cd $RPM_BUILD_ROOT/usr/lib64
%{__ln_s} ../../opt/freeware/lib64/libproto* .
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
%{__ln_s} ../../opt/freeware/lib/libproto* .


cd %{prefix}/src/packages/BUILD/protobuf-%{version}/32bit

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
cp %{name}-java-%{version}.jar      %{buildroot}%{javadir}/%{name}/%{name}-java-%{version}.jar
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

%if 0%{?suse_version} > 1010
%fdupes %{buildroot}%{py_sitedir}/%{name}-%{version}-py%{py_ver}.egg-info
%endif

%clean
rm -rf $RPM_BUILD_ROOT;


%files
%defattr(-, root, root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%{_libdir}/libprotobuf.so.%{soname}
%{_libdir}/libprotobuf.so
%{_libdir}/libprotobuf.a
%{_libdir64}/libprotobuf.so.%{soname}*
%{_libdir64}/libprotobuf.so
%{_libdir64}/libprotobuf.a
/usr/lib/libprotobuf.*
/usr/lib64/libprotobuf.*

%files libprotoc
%defattr(-, root, root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%{_libdir}/libprotoc.so.%{soname}
%{_libdir}/libprotoc.so
%{_libdir}/libprotoc.a
%{_libdir64}/libprotoc.so.%{soname}*
%{_libdir64}/libprotoc.so
%{_libdir64}/libprotoc.a
/usr/lib/libprotoc.*
/usr/lib64/libprotoc.*

%files lite
%defattr(-, root, root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%{_libdir}/libprotobuf-lite.so.%{soname}
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf-lite.a
%{_libdir64}/libprotobuf-lite.so.%{soname}*
%{_libdir64}/libprotobuf-lite.so
%{_libdir64}/libprotobuf-lite.a
/usr/lib/libprotobuf-lite.*
/usr/lib64/libprotobuf-lite.*

%files devel
%defattr(-,root,root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%doc 32bit/examples
%{_bindir}/protoc
%{_includedir}/google
#Why again all .a and .so* ???
#%{_libdir}/*.so
#%{_libdir}/*.a
%{_libdir}/pkgconfig/*
#%{_libdir64}/*.so
#%{_libdir64}/*.a
##%{_datadir}/vim	 ???????????
#/usr/lib/*
#/usr/lib64/*

# java
%files java
%defattr(-,root,root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%{javadir}/%{name}/protobuf*

# python
#%files -n python-%{name} -f python/INSTALLED_FILES
%files python
%defattr(-,root,root)
%doc 32bit/COPYING.txt 
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.txt
%{_libdir}/python2.7/site-packages/*

%changelog
* Thu Jun 7 2018 by Tony Reix <tony.reix@atos.net> 2.5.0-2
- Re-Port on AIX 6.1 
- Add atomicops_internals_aix.h moved to AIX assembler
- Fix 32bit/64bit management

* Fri May 3 2013 by Bernard CAHEN <bernard.cahen@bull.net> 2.4.1-1
- Port on AIX 6.1 
