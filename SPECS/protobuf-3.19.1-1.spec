%bcond_without dotests

%bcond_without java

# The .so version was 8 for 2.5.0, 9 for 2.6.1, 17 for 3.6.1, 21 for 3.10.1, 22 for 3.11.2
# We do not add old .so in archive because protobuf is only used as BuildRequire


#################################
#  End of user-modifiable configs
#################################
%define name protobuf
%define version 3.19.1
%define release 1
%if %{with java}
%define javadir %{_prefix}/java
%endif

%define _libdir64 %{_prefix}/lib64

Summary:    Protocol Buffers - Google's data interchange format
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    BSD
Group:      Development/Libraries/C and C++
URL:        https://github.com/protocolbuffers/protobuf
Source0:    https://github.com/protocolbuffers/protobuf/archive/v%{version}/%{name}-all-%{version}.tar.gz

Source1:    ftdetect-proto.vim
Source2:    protobuf-init.el
# Contains old lib. *.so.17 are version 3.6.1
Source3:    libprotobuf.tar.gz
# For tests   - no longer required as this appears to be integrated with Source0
# Source3:    https://github.com/google/googletest/archive/release-1.8.1.tar.gz#/googletest-1.8.1.tar.gz
Source5:    manifest.txt.in
Source10: %{name}-%{version}-%{release}.build.log

Patch1: %{name}-2.5.0-atomicops_internals_aix.h.patch

# Needed to rebootstrap with gtest 1.5.0
BuildRequires:  libtool
BuildRequires:  zlib-devel >= 1.2.11
# Java 1.6 required
#BuildRequires:  java-devel >= 1.6.0
# Python required
BuildRequires:  python(abi) >= 3.9
BuildRequires:  python3-devel


# Test while build GCC running with 1.11 BuildRequires:  automake >= 1.14
BuildRequires:  gcc-c++
BuildRequires:  automake >= 1.11
# From Fedora 30 & 32
#BuildRequires:  emacs
#BuildRequires:  emacs-el >= 24.1
#Requires:       emacs-filesystem >= %{_emacs_version}


%description
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. Google uses Protocol Buffers for almost all of its internal
RPC protocols and file formats. 

#%package libprotoc - This RPM is named protobuf-compiler on Fedora
%package compiler
Summary:        Protocol Buffers compiler
Group:          System/Libraries
Obsoletes:      %{name}-libprotoc
Requires:       zlib >= 1.2.11

#%description libprotoc
%description compiler
This package contains Protocol Buffers compiler for all programming
languages.

%package lite
Summary:        Protocol Buffers LITE_RUNTIME libraries
Group:          System/Libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The LITE_RUNTIME option causes the compiler to generate code which only
depends on libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package devel
Summary:       Header files, libraries and development documentation for %{name}
Group:         Development/Libraries/C and C++

Requires:      gcc-c++
Requires:      protobuf = %{version}-%{release}
#Requires:       protobuf-lite
Requires:      protobuf-compiler = %{version}-%{release}
Requires:      zlib-devel >= 1.2.11
#BuildRequires:  pkg-config

%description devel
Development files for Google Protocol Buffers.
This includes the Protocol Buffers compiler for all languages and
C++ headers and libraries.

%if %{with java}
%package java
#Requires:       java >= 1.6.0
Summary:        Java Bindings for Google Protocol Buffers
Group:          Development/Libraries/Java

#BuildRequires:  maven-local     - This is present in Fedora 30
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}


%description java
This package contains the Java bindings for Google Protocol Buffers.
%endif


%package -n python%{python_version}-protobuf
Summary:        Python 3 bindings for Google Protocol Buffers
Group:          Development/Libraries/Python

Requires:       python%{python_version}(abi)

BuildRequires:  python%{python_version}(abi) >= 3.9
BuildRequires:  python%{python_version}-devel
BuildRequires:  python%{python_version}-setuptools
# For tests
%if %{with dotests}
#BuildRequires:  python3-google-apputils
BuildRequires:  python%{python_version}-six >= 1.9
BuildRequires:  python%{python_version}-pip
%endif
Requires:       python%{python_version}-six >= 1.9
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}

%description -n python%{python_version}-protobuf
This package contains Python 3 libraries for Google Protocol Buffers

%package -n python3-protobuf
Summary:        Python 3 bindings for Google Protocol Buffers
Group:          Development/Libraries/Python
Provides:       %{name}-python3

Requires:       python(abi) = %{python_version}
Requires:       python%{python_version}-protobuf = %{version}-%{release}

BuildRequires:  python(abi) >= 3.9
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# For tests
%if %{with dotests}
#BuildRequires:  python3-google-apputils
BuildRequires:  python3-six >= 1.9
BuildRequires:  python3-pip
%endif
Requires:       python3-six >= 1.9
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}

%description -n python3-protobuf
This package contains Python 3 libraries for Google Protocol Buffers


# There is currently no RPMs for vim
#%package vim
#Summary:      Vim syntax highlighting for Google Protocol Buffers descriptions
#BuildArch:    noarch
#Requires:     vim-enhanced
#
#%description vim
#This package contains syntax highlighting for Google Protocol Buffers
#descriptions in Vim editor


%prep

# The -a option adds sources from googletest/Source3
# Source3 longer required as this appears to be integrated with Source0
#%setup -q -a 3
%setup -q

%patch1 -p1
# %patch2 -p1

#mv googletest-release-1.8.1/* third_party/googletest/
##%patch3 -p1 -b .aixWA

find -name \*.cc -o -name \*.h | xargs chmod -x
chmod 644 examples/*


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
export PATH=/opt/freeware/bin:/usr/java8_64/bin/:$PATH
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export AR="ar -X32_64"
export NM="nm -X32_64"

export PTHREAD_LIBS=-lpthread

# -DGOOGLE_PROTOBUF_OS_AIX is automatically set in code

# 64 bit
cd 64bit

export CC="gcc -g -maix64"
export CXX="g++ -g -maix64 -pthread"
export OBJECT_MODE=64
export CFLAGS=" -mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"

#export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"

# export LDFLAGS="-L%{_libdir}/pthread -lbsd -Wl,-bbigtoc"
export LDFLAGS="-L%{_libdir}/pthread/ppc64 -lcrypt"

export LIBPATH=/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib

# The configure file has to be generated using autoreconf
./autogen.sh

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir64} \
        --disable-static

# The -blibpath is required because libtool is preceeding pthread g++ libs
# with non-pthread g++ libs  in  -blibpath

# Primative hack to force -blibpath in libtool to give precedence to pthread
# There may be a libtool var/option to do this, but the main default library
# directory /opt/freeware/lib was always first and the libstdc++.a symlink
# there is non-pthread

# MAIN libtool

mv libtool  libtool.orig
# sed 's?-blibpath:?-blibpath:/opt/freeware/lib/pthread/ppc64:?'  libtool.orig > libtool
sed 's?-blibpath:.*$?-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"?'  libtool.orig > libtool
chmod +x libtool


# googleMOCK libtool
# Primative hack to force -blibpath in libtool to give precedence to pthread
# Must also add -blibpath and -lgtest to libgmock.* to find the dep libgtest.a

mv third_party/googletest/googlemock/libtool  third_party/googletest/googlemock/libtool.orig

sed 's?\\\$wl-blibpath:.*$?-L../googletest/lib/.libs  -lgtest \\$wl-blibpath:\\$progdir/../googletest/lib/.libs:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"?'  third_party/googletest/googlemock/libtool.orig > third_party/googletest/googlemock/libtool.tmp1

# Also eliminate inclusion of flag -berok

sed 's?^allow_undefined_flag=?allow_undefined_flag=" "\n# allow_undefined_flag=?'  third_party/googletest/googlemock/libtool.tmp1 > third_party/googletest/googlemock/libtool
chmod +x third_party/googletest/googlemock/libtool


# googleTEST libtool
# Primative hack to force -blibpath in libtool to give precedence to pthread

mv third_party/googletest/googletest/libtool  third_party/googletest/googletest/libtool.orig
sed 's?-blibpath:.*$?-blibpath:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"?'  third_party/googletest/googletest/libtool.orig > third_party/googletest/googletest/libtool.tmp1


sed 's?^allow_undefined_flag=?allow_undefined_flag=" "\n# allow_undefined_flag=?'  third_party/googletest/googletest/libtool.tmp1 > third_party/googletest/googletest/libtool
chmod +x third_party/googletest/googletest/libtool

gmake -j10


echo ====== 64 Finished ======


# 32 bit 
cd ../32bit

export CC="gcc -g -maix32"
export CXX="g++ -g -maix32 -pthread"
export OBJECT_MODE=32
export CFLAGS=" -mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"

#export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"

# export LDFLAGS="-L%{_libdir}/pthread -lbsd -lstdc++ -latomic -Wl,-bbigtoc"
export LDFLAGS="-L%{_libdir}/pthread -lstdc++ -latomic -Wl,-bmaxdata:0x80000000 -lcrypt"

export LIBPATH=/opt/freeware/lib/pthread:/opt/freeware/lib

# The configure file has to be generated using autoreconf
./autogen.sh

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir} \
	--disable-static

# The -blibpath is required because libtool is preceeding pthread g++ libs
# with non-pthread g++ libs  in  -blibpath

# Primative hack to force -blibbpath in libtool to give precedence to pthread
# There may be a libtool var/option to do this, but the main default library
# directory /opt/freeware/lib was always first and the libstdc++.a symlink
# there is non-pthread


# MAIN libtool

mv libtool  libtool.orig
sed 's?-blibpath:.*$?-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"?'  libtool.orig > libtool
chmod +x libtool


# googleMOCK libtool
# Primative hack to force -blibpath in libtool to give precedence to pthread
# Must also add -blibpath and -lgtest to libgmock.* to find the dep libgtest.a

mv third_party/googletest/googlemock/libtool  third_party/googletest/googlemock/libtool.orig

sed 's?\\\$wl-blibpath:.*$?-L../googletest/lib/.libs  -lgtest \\$wl-blibpath:\\$progdir/../googletest/lib/.libs:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"?'  third_party/googletest/googlemock/libtool.orig > third_party/googletest/googlemock/libtool.tmp1


# Also eliminate inclusion of flag -berok

sed 's?^allow_undefined_flag=?allow_undefined_flag=" "\n# allow_undefined_flag=?'  third_party/googletest/googlemock/libtool.tmp1 > third_party/googletest/googlemock/libtool

chmod +x third_party/googletest/googlemock/libtool


# googleTEST libtool
# Primative hack to force -blibpath in libtool to give precedence to pthread

mv third_party/googletest/googletest/libtool  third_party/googletest/googletest/libtool.orig
sed 's?-blibpath:.*$?-blibpath:/opt/freeware/lib/pthread:/opt/freeware/lib:/usr/lib"?'  third_party/googletest/googletest/libtool.orig > third_party/googletest/googletest/libtool.tmp1

sed 's?^allow_undefined_flag=?allow_undefined_flag=" "\n# allow_undefined_flag=?'  third_party/googletest/googletest/libtool.tmp1 > third_party/googletest/googletest/libtool
chmod +x third_party/googletest/googletest/libtool

gmake -j10
cd ..

echo ====== 32 Finished ======

# create .a with the 64-bit shared objects and the  32-bit shared objects
${AR} -q libprotobuf-lite.a  32bit/src/.libs/libprotobuf-lite.so.*  64bit/src/.libs/libprotobuf-lite.so.*
#rm src/.libs/libprotobuf.a
${AR} -q libprotobuf.a       32bit/src/.libs/libprotobuf.so.*       64bit/src/.libs/libprotobuf.so.*
#rm src/.libs/libprotoc.a
${AR} -q libprotoc.a         32bit/src/.libs/libprotoc.so.*         64bit/src/.libs/libprotoc.so.*

echo Build Python and Java
# Java 

# Problems linking with the pthread/libstc++.a in 32 bit env
#  not finding symbols  __once_call __once_callable __once_proxy
#  when loading lt-protoc and libprotobuf.so.17/libprotoc.so.17
# In 64 bit env pthread/libstc++.a is linked

cd 64bit
%if %{with java}
cd java
#LIBPATH=/opt/freeware/lib/pthread ../src/protoc --java_out=core/src/main/java -I../src ../src/google/protobuf/descriptor.proto
LIBPATH=`pwd`/../src/.libs:/opt/freeware/lib/pthread:/opt/freeware/lib ../src/protoc --java_out=core/src/main/java -I../src ../src/google/protobuf/descriptor.proto
mkdir -p classes
javac  $extra_java_flags -d classes core/src/main/java/com/google/protobuf/*.java
# Is the Java manifest still needed ?
sed -e 's/@VERSION@/%version/' < %{SOURCE5} > manifest.txt
jar cfm %{name}-java-%{version}.jar manifest.txt -C classes com
cd ..
%endif

# python build
# Same pb running lt-protoc as for java

cd python
LIBPATH=`pwd`/../src/.libs:/opt/freeware/lib/pthread:/opt/freeware/lib python3 setup.py build
cd ..


#emacs -batch -f batch-byte-compile editors/protobuf-mode.el
# Or new command
#%{_emacs_bytecompile} editors/protobuf-mode.el


%install
export PATH=/opt/freeware/bin:/usr/java8_64/bin/:$PATH
# The 64 bit version of bin/protoc will be installed then overwritten by
# the 32 bit version  - not sure this was noticed, but may be not a problem
# Rename 64 bit version bin/protoc_64

echo "RPM_BUILD_ROOT: $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib64

# export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export PTHREAD_LIBS=-lpthread

export CFLAGS="-mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-mcmodel=large -I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-qnamemangling=v5 -qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"


cd 64bit
export OBJECT_MODE=64
export CC="gcc -maix64"
export CXX="g++ -maix64 -pthread"
#export CXX="g++ -maix64 -pthread -L%{_libdir}/pthread"
#export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib -Wl,-brtl"
# export LDFLAGS="-lbsd -Wl,-bbigtoc"
export LDFLAGS="-lcrypt"

make DESTDIR=$RPM_BUILD_ROOT install prefix=%{_prefix}

# Move bin/protoc to bin/protoc_64
mv $RPM_BUILD_ROOT%{_bindir}/protoc $RPM_BUILD_ROOT/%{_bindir}/protoc_64

# no need for .la files
rm %{buildroot}%{_libdir64}/*.la

#%if %{with protobuf_java}
#pushd java
#%__install -D -m 0644 %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-java-%{version}.jar
#%__ln_s %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}-java.jar
#%__ln_s %{name}-java-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
#popd
#%endif

%if %{with java}
# java
cd java
mkdir -p  %{buildroot}%{javadir}/%{name}
cp %{name}-java-%{version}.jar      %{buildroot}%{javadir}/%{name}/%{name}-java-%{version}.jar
%__ln_s %{name}-java-%{version}.jar %{buildroot}%{javadir}/%{name}/%{name}-java.jar
%__ln_s %{name}-java-%{version}.jar %{buildroot}%{javadir}/%{name}/%{name}.jar
cd ..
%endif

# python
cd python
LIBPATH=`pwd`/../src/.libs:/opt/freeware/lib/pthread:/opt/freeware/lib python3 setup.py install --skip-build \
	--prefix=%{_prefix} \
	--install-data=$RPM_BUILD_ROOT \
	--root  $RPM_BUILD_ROOT \
	--record=INSTALLED_FILES
cd ..

cd ../32bit
export OBJECT_MODE=32
export CC="gcc -maix32"
export CXX="g++ -maix32 -pthread"
#export CXX="g++ -maix32 -pthread -L%{_libdir}/pthread"
#export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl -latomic"
# export LDFLAGS="-lbsd -lstdc++ -latomic -Wl,-bbigtoc"
export LDFLAGS="-lstdc++ -latomic -Wl,-bmaxdata:0x80000000 -lcrypt"

make DESTDIR=$RPM_BUILD_ROOT install prefix=%{_prefix}

(
  cd $RPM_BUILD_ROOT%{_bindir}
  # Move bin/protoc to bin/protoc_64
  mv protoc protoc_32
  ln -sf protoc_64 protoc
)

# no need for .la files
rm %{buildroot}%{_libdir}/*.la

cd ..

cp  %{_prefix}/src/packages/BUILD/protobuf-%{version}/32bit/src/.libs/*.a $RPM_BUILD_ROOT/%{_prefix}/lib


ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib
ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib64


cd $RPM_BUILD_ROOT/%{_prefix}/lib64
cp %{_prefix}/src/packages/BUILD/protobuf-%{version}/64bit/src/.libs/lib*.so.* .

cd $RPM_BUILD_ROOT/%{_prefix}/lib
cp %{_prefix}/src/packages/BUILD/protobuf-%{version}/32bit/src/.libs/lib*.so.* .
ar -X64 q $RPM_BUILD_ROOT/%{_prefix}/lib/libprotobuf-lite.a $RPM_BUILD_ROOT/%{_prefix}/lib64/libprotobuf-lite.so.*
ar -X64 q $RPM_BUILD_ROOT/%{_prefix}/lib/libprotobuf.a      $RPM_BUILD_ROOT/%{_prefix}/lib64/libprotobuf.so.*
ar -X64 q $RPM_BUILD_ROOT/%{_prefix}/lib/libprotoc.a        $RPM_BUILD_ROOT/%{_prefix}/lib64/libprotoc.so.*


cd $RPM_BUILD_ROOT/%{_prefix}/lib64  
rm -f *.a
%{__ln_s}  ../lib/*.a .


ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib
ls -l  $RPM_BUILD_ROOT/%{_prefix}/lib64


mkdir -p $RPM_BUILD_ROOT/usr/lib64
cd $RPM_BUILD_ROOT/usr/lib64
%{__ln_s} ../../opt/freeware/lib64/libproto* .
mkdir -p $RPM_BUILD_ROOT/usr/lib
cd $RPM_BUILD_ROOT/usr/lib
%{__ln_s} ../../opt/freeware/lib/libproto* .


cd %{_prefix}/src/packages/BUILD/protobuf-%{version}/32bit

# Add old librairies
cd ..
rm -fr tmp ; mkdir tmp
cd tmp
tar xfvz %{SOURCE3}
mv protobuf/libprotobuf.so.17.32bit libprotobuf.so.17
ar -qc -X32 %{buildroot}%{_libdir}/libprotobuf.a libprotobuf.so.17
mv protobuf/libprotobuf.so.17.64bit libprotobuf.so.17
ar -qc -X64 %{buildroot}%{_libdir}/libprotobuf.a libprotobuf.so.17

mv protobuf/libprotobuf-lite.so.17.32bit libprotobuf-lite.so.17
ar -qc -X32 %{buildroot}%{_libdir}/libprotobuf-lite.a libprotobuf-lite.so.17
mv protobuf/libprotobuf-lite.so.17.64bit libprotobuf-lite.so.17
ar -qc -X64 %{buildroot}%{_libdir}/libprotobuf-lite.a libprotobuf-lite.so.17

mv protobuf/libprotoc.so.17.32bit libprotoc.so.17
ar -qc -X32 %{buildroot}%{_libdir}/libprotoc.a libprotoc.so.17
mv protobuf/libprotoc.so.17.64bit libprotoc.so.17
ar -qc -X64 %{buildroot}%{_libdir}/libprotoc.a libprotoc.so.17

# For vim RPM if needed
#install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
#install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

#mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}
#mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir}
#install -p -m 0644 editors/protobuf-mode.el $RPM_BUILD_ROOT%{_emacs_sitelispdir}
#install -p -m 0644 editors/protobuf-mode.elc $RPM_BUILD_ROOT%{_emacs_sitelispdir}
#install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_emacs_sitestartdir}


%check
export PATH=/opt/freeware/bin:/usr/java8_64/bin/:$PATH
%if %{with dotests}
cd 64bit
(
 export LIBPATH=`pwd`/src/.libs:`pwd`/third_party/googletest/googlemock/lib/.libs/:`pwd`/third_party/googletest/googletest/lib/.libs/:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib
 gmake -k -j10 check || true
)
slibclean
(
 cd python
 export LIBPATH=`pwd`/../src/.libs:`pwd`/../third_party/googletest/googlemock/lib/.libs/:`pwd`/../third_party/googletest/googletest/lib/.libs/:/opt/freeware/lib/pthread/ppc64:/opt/freeware/lib64:/opt/freeware/lib
 %{__python} setup.py test || true
)
slibclean

# Old 32/64 method
#mkdir src/.libs64
#cp  -P src/.libs/*so* src/.libs64

# We keep the environment
#gmake distclean
#%{__make} check %{?jobs:-j%jobs}

cd ../32bit
(
 export LIBPATH=`pwd`/src/.libs:`pwd`/third_party/googletest/googlemock/lib/.libs/:`pwd`/third_party/googletest/googletest/lib/.libs/:/opt/freeware/lib/pthread:/opt/freeware/lib
 gmake -k -j10 check || true
)
slibclean

%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%{_libdir}/libprotobuf.a
%{_libdir64}/libprotobuf.a

%files compiler
%defattr(-,root,system,-)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%{_bindir}/protoc
%{_bindir}/protoc_64
%{_libdir}/libprotoc.a
%{_libdir64}/libprotoc.a
#%%{_emacs_sitelispdir}/%%{name}/
#%%{_emacs_sitestartdir}/protobuf-init.el


%files lite
%defattr(-,root,system,-)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%{_libdir}/libprotobuf-lite.a
%{_libdir64}/libprotobuf-lite.a

%files devel
%defattr(-,root,system,-)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt
%doc 32bit/examples/add_person.cc 32bit/examples/addressbook.proto
%doc 32bit/examples/list_people.cc 32bit/examples/Makefile
%doc 32bit/examples/README.md
%{_includedir}/google/protobuf
%{_libdir}/pkgconfig/protobuf.pc


%if %{with java}
# java
%files java
%defattr(-,root,system,-)
%doc 64bit/LICENSE
%doc 64bit/CHANGES.txt 64bit/CONTRIBUTORS.txt 64bit/README.md
%doc 64bit/examples/AddPerson.java 64bit/examples/ListPeople.java
%{javadir}/%{name}/protobuf*
%endif

# python3
%files -n python3-protobuf
%defattr(-,root,system,-)

%files -n python%{python_version}-protobuf
%defattr(-,root,system,-)
%doc 64bit/LICENSE
%doc 64bit/CHANGES.txt 64bit/CONTRIBUTORS.txt 64bit/python/README.md
%doc 64bit/examples/add_person.py 64bit/examples/list_people.py 64bit/examples/addressbook.proto
%{python_sitelib}/*

# For vim RPM if needed
#%files vim
#%%{_datadir}/vim/vimfiles/ftdetect/proto.vim
#%%{_datadir}/vim/vimfiles/syntax/proto.vim


%changelog
* Mon Nov 29 2021 Etienne Guesnet <etienne.guesnet@atos.net> 3.19.1-1
- New version 3.19.1
- Add python metapackage
- Remove python 2 support
- Remove usage of soname variable

* Mon Jan 13 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 3.11.2-1
- New version 3.11.2
- Provide python3 package
- No more provide .so files and link to /usr/lib
- Make python test
- Correct internal libpath to find libz.a at /opt/freeware/lib and not /usr/lib
- Conditional java

* Thu Nov 14 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.10.1-1
- Update to version 3.10.1
- Source for googletest integrated in Protobuf

* Tue Oct 22 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.6.1-2
- Rebuild on reference machine
- Rebuild with new googletest package and run tests
- Update version of zlib dependency due to GCC
- Largely inspired by Fedora 32 3.6.1-7

* Fri Feb 08 2019 Michael Wilson <michael.a.wilson@atos.net> - 3.6.1-1
- Update to version 3.6.1
- Largely inspired by Fedora 30
- Add option -pthread for c++  mutex/pthreads support, e.g.
-          export CXX="g++ -maix64 -pthread"
- Add link with libatomic.a for 32 bit build for symbol __atomic_fetch_add_8
- Change LDFLAGS for %install to same as %build for pthread symbols __once_*
-          to find pthread/libstcc++.a  before non-pthread version
-          -L:/opt/freeware/lib/pthread (a W/A for libtool issue)
- Also add /opt/freeware/lib/pthread to head of -blibpath in libtool
-          so bin/protoc executes with pthread g++ libs
- New java code requires use of Java7 javac (LPP Java7.sdk)
- Change hard coded soname 8 to %{soname}  for the AR commands

* Thu Jun 7 2018 by Tony Reix <tony.reix@atos.net> 2.5.0-2
- Re-Port on AIX 6.1 
- Add atomicops_internals_aix.h moved to AIX assembler
- Fix 32bit/64bit management

* Fri May 3 2013 by Bernard CAHEN <bernard.cahen@bull.net> 2.4.1-1
- Port on AIX 6.1 
