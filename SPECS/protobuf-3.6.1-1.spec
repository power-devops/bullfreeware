# The .so version was 8 for 2.5.0 and 9 for 2.6.1 - for 3.6.1 it is 17
%define soname 17
%define _libdir64 %{_prefix}/lib64


#################################
#  End of user-modifiable configs
#################################
%define name protobuf
%define version 3.6.1
%define release 1
%define javadir %{_prefix}/java


%define libdir64 %{_prefix}/lib64

Summary:    Protocol Buffers - Google's data interchange format
Name:       %{name}
Version:    %{version}
Release:    %{release}
License:    BSD
Group:      Development/Libraries/C and C++
URL:        https://github.com/protocolbuffers/protobuf
Source0:    https://github.com/protocolbuffers/protobuf/archive/v%{version}/%{name}-%{version}-all.tar.gz

Source1:    ftdetect-proto.vim
Source2:    protobuf-init.el
# For tests
Source3:    https://github.com/google/googlemock/archive/release-1.7.0.tar.gz#/googlemock-1.7.0.tar.gz
Source4:    https://github.com/google/googletest/archive/release-1.7.0.tar.gz#/googletest-1.7.0.tar.gz



Source5:    manifest.txt.in


Patch1:	%{name}-2.5.0-atomicops_internals_aix.h.patch

# No longer needed ?  Patch2: %{name}-2.5.0-int64.patch


# Needed to rebootstrap with gtest 1.5.0
BuildRequires:  libtool
BuildRequires:  zlib-devel
# Java 1.6 required
#BuildRequires:  java-devel >= 1.6.0
# Python required
BuildRequires:  python
BuildRequires:  python-devel


# Test while build GCC running with 1.11 BuildRequires:  automake >= 1.14
BuildRequires:  automake >= 1.11
# From Fedora 30
BuildRequires:  emacs
#BuildRequires:  emacs-el >= 24.1
BuildRequires:  gcc-c++



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

#%package libprotoc - This RPM is named protobuf-compiler on Fedora
%package compiler
Summary:        Protocol Buffers compiler
Group:          System/Libraries
Obsoletes:      %{name}-libprotoc

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
Summary:        Header files, libraries and development documentation for %{name}
Group:          Development/Libraries/C and C++

Requires:       gcc-c++
Requires:       protobuf = %{version}-%{release}
#Requires:       protobuf-lite
Requires:       protobuf-compiler = %{version}-%{release}
Requires:       zlib-devel
#BuildRequires:  pkg-config
#Provides:       protobuf-devel = %version

%description devel
Development files for Google Protocol Buffers.
This includes the Protocol Buffers compiler for all languages and
C++ headers and libraries.

%package java
#Requires:       java >= 1.6.0
Summary:        Java Bindings for Google Protocol Buffers
Group:          Development/Libraries/Java

#BuildRequires:  maven-local     - This is present in Fedora 30
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}


%description java
This package contains the Java bindings for Google Protocol Buffers.

%package python
Requires:       python
Summary:        Python 2 bindings for Google Protocol Buffers
Group:          Development/Libraries/Python

BuildRequires:  python
BuildRequires:  python-devel
BuildRequires:  python-setuptools
# For tests
#BuildRequires:  python-google-apputils
Requires:       python-six >= 1.9
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}

%description python
This package contains the Python 2 bindings for Google Protocol Buffers.


# There is currently no RPMs for Python 3, vim and emacs


#%package python3
#Summary:        Python 3 bindings for Google Protocol Buffers
#BuildRequires:  python3-devel
#BuildRequires:  python3-setuptools
## For tests
#BuildRequires:  python3-google-apputils
#Requires:       python3-six >= 1.9
#Conflicts:      %{name}-compiler > %{version}
#Conflicts:      %{name}-compiler < %{version}
#
#%description python3
#This package contains Python 3 libraries for Google Protocol Buffers


#%package vim
#Summary:      Vim syntax highlighting for Google Protocol Buffers descriptions
#BuildArch:    noarch
#Requires:     vim-enhanced
#
#%description vim
#This package contains syntax highlighting for Google Protocol Buffers
#descriptions in Vim editor


#%package emacs
#Summary:      Emacs mode for Google Protocol Buffers descriptions
#BuildArch:    noarch
#Requires:     emacs(bin) >= 0%{emacs_version}
#
#%description emacs
#This package contains syntax highlighting for Google Protocol Buffers
#descriptions in the Emacs editor.
#
#%package emacs-el
#Summary:      Elisp source files for Google protobuf Emacs mode
#BuildArch:    noarch
#Requires:     protobuf-emacs = %{version}
#
#%description emacs-el
#This package contains the elisp source files for %{name}-emacs
#under GNU Emacs. You do not need to install this package to use
#%{name}-emacs.






%prep

# The -a options add sources from googletest/Source3 and googlemock/Source4
%setup -q -a 3 -a 4

%patch1 -p1
# %patch2 -p1

mv googlemock-release-1.7.0 gmock
mv googletest-release-1.7.0 gmock/gtest


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
export CXX="g++ -maix64 -pthread"
export OBJECT_MODE=64
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"

#export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib64 -L/usr/lib -Wl,-brtl"

export LDFLAGS="-L%{_libdir}/pthread -lbsd -Wl,-bbigtoc"

export LIBPATH=/opt/freeware/lib/pthread:/opt/freeware/lib

# The configure file has to be generated using autoreconf
./autogen.sh

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir64} \
        --host=%{buildhost} \
	--target=%{buildhost} \
	--build=%{buildhost} \
        --disable-static

# The -blibpath is required because libtool is preceeding pthread g++ libs
# with non-pthread g++ libs  in  -blibpath

# Primative hack to force -blibbpath in libtool to give precedence to pthread
# There may be a libtool var/option to do this, but the main default library
# directory /opt/freeware/lib was always first and the libstdc++.a symlink
# there is non-pthread

mv libtool  libtool.orig
sed 's?-blibpath:?-blibpath:/opt/freeware/lib/pthread:?'  libtool.orig > libtool
chmod +x libtool


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
export CXX="g++ -maix32 -pthread"
export OBJECT_MODE=32
export CFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CXXFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"
#export CPPFLAGS="-qrtti -I`pwd`/include -I/opt/freeware/include -I/usr/include"
export CPPFLAGS="-I`pwd`/include -I/opt/freeware/include -I/usr/include"

#export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl"

export LDFLAGS="-L%{_libdir}/pthread -lbsd -lstdc++ -latomic"

export LIBPATH=/opt/freeware/lib/pthread:/opt/freeware/lib

# The configure file has to be generated using autoreconf
./autogen.sh

./configure \
	--prefix=/opt/freeware \
	--libdir=%{_libdir} \
	--host=%{buildhost} \
	--target=%{buildhost} \
	--build=%{buildhost} \
	--disable-static

# The -blibpath is required because libtool is preceeding pthread g++ libs
# with non-pthread g++ libs  in  -blibpath

# Primative hack to force -blibbpath in libtool to give precedence to pthread
# There may be a libtool var/option to do this, but the main default library
# directory /opt/freeware/lib was always first and the libstdc++.a symlink
# there is non-pthread

mv libtool  libtool.orig
sed 's?-blibpath:?-blibpath:/opt/freeware/lib/pthread:?'  libtool.orig > libtool
chmod +x libtool


gmake -j8

export CFLAGS="$CFLAGS -Wl,-bbigtoc"
( gmake -k check || true )
slibclean


cd ..

# create .a with the 64-bit shared objects and the  32-bit shared objects
${AR} -q libprotobuf-lite.a  32bit/src/.libs/libprotobuf-lite.so.%{soname}  64bit/src/.libs/libprotobuf-lite.so.%{soname}
#rm src/.libs/libprotobuf.a
${AR} -q libprotobuf.a       32bit/src/.libs/libprotobuf.so.%{soname}       64bit/src/.libs/libprotobuf.so.%{soname}
#rm src/.libs/libprotoc.a
${AR} -q libprotoc.a         32bit/src/.libs/libprotoc.so.%{soname}         64bit/src/.libs/libprotoc.so.%{soname}


# Java 

# Problems linking with the pthread/libstc++.a in 32 bit env
#  not finding symbols  __once_call __once_callable __once_proxy
#  when loading lt-protoc and libprotobuf.so.17/libprotoc.so.17
# In 64 bit env pthread/libstc++.a is linked

cd 32bit/java
LIBPATH=/opt/freeware/lib/pthread ../src/protoc --java_out=core/src/main/java -I../src ../src/google/protobuf/descriptor.proto
mkdir classes
/usr/java7/bin/javac  $extra_java_flags -d classes core/src/main/java/com/google/protobuf/*.java
# Is the Java manifest still needed ?
sed -e 's/@VERSION@/%version/' < %{SOURCE5} > manifest.txt
/usr/java7/bin/jar cfm %{name}-java-%{version}.jar manifest.txt -C classes com
cd ..

# python build
# Same pb running lt-protoc as for java

cd python
LIBPATH=/opt/freeware/lib/pthread python setup.py build
cd ..

# Does not seem to exist ?
#cd python3
#LIBPATH=/opt/freeware/lib/pthread python3 setup.py build
#cd ..


#emacs -batch -f batch-byte-compile editors/protobuf-mode.el


#%check
#%{__make} check %{?jobs:-j%jobs}


%install

# The 64 bit version of bin/protoc will be installed then overwritten by
# the 32 bit version  - not sure this was noticed, but may be not a problem

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
export CXX="g++ -maix64 -pthread"
#export CXX="g++ -maix64 -pthread -L%{_libdir}/pthread"
#export LDFLAGS="-L`pwd` -L%{_libdir64} -L%{_libdir} -L/usr/lib -Wl,-brtl"
export LDFLAGS="-lbsd -Wl,-bbigtoc"

make DESTDIR=$RPM_BUILD_ROOT install prefix=%{prefix}

# no need for .la files
rm %{buildroot}%{_libdir64}/*.la


cd ../32bit
export OBJECT_MODE=32
export CC="gcc -maix32"
export CXX="g++ -maix32 -pthread"
#export CXX="g++ -maix32 -pthread -L%{_libdir}/pthread"
#export LDFLAGS="-L`pwd` -L%{_libdir} -L/usr/lib -Wl,-brtl -latomic"
export LDFLAGS="-lbsd -lstdc++ -latomic"

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
%{__ln_s} libprotobuf-lite.so.%{soname} libprotobuf-lite.so
%{__ln_s} libprotobuf.so.%{soname}      libprotobuf.so
%{__ln_s} libprotoc.so.%{soname}        libprotoc.so

cd $RPM_BUILD_ROOT/%{prefix}/lib
cp %{prefix}/src/packages/BUILD/protobuf-%{version}/32bit/src/.libs/lib*.so.* .
%{__ln_s} libprotobuf-lite.so.%{soname} libprotobuf-lite.so
%{__ln_s} libprotobuf.so.%{soname}      libprotobuf.so
%{__ln_s} libprotoc.so.%{soname}        libprotoc.so
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotobuf-lite.a $RPM_BUILD_ROOT/%{prefix}/lib64/libprotobuf-lite.so.%{soname}
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotobuf.a      $RPM_BUILD_ROOT/%{prefix}/lib64/libprotobuf.so.%{soname}
ar -X64 q $RPM_BUILD_ROOT/%{prefix}/lib/libprotoc.a        $RPM_BUILD_ROOT/%{prefix}/lib64/libprotoc.so.%{soname}


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
LIBPATH=/opt/freeware/lib/pthread python setup.py install --skip-build \
	--prefix=%{_prefix} \
	--install-data=$RPM_BUILD_ROOT \
	--root  $RPM_BUILD_ROOT \
	--record=INSTALLED_FILES
cd ..

#cd python3
#python3 setup.py install --skip-build \
#	--prefix=%{_prefix} \
#	--install-data=$RPM_BUILD_ROOT \
#	--root  $RPM_BUILD_ROOT \
#	--record=INSTALLED_FILES
#cd ..


# What is this ?
#%if 0%{?suse_version} > 1010
#%fdupes %{buildroot}%{py_sitedir}/%{name}-%{version}-py%{py_ver}.egg-info
#%endif

# For vim and emacs RPMs if needed
#install -p -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
#install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim

#mkdir -p $RPM_BUILD_ROOT%{emacs_lispdir}
#mkdir -p $RPM_BUILD_ROOT%{emacs_startdir}
#install -p -m 0644 editors/protobuf-mode.el $RPM_BUILD_ROOT%{emacs_lispdir}
#install -p -m 0644 editors/protobuf-mode.elc $RPM_BUILD_ROOT%{emacs_lispdir}
#install -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{emacs_startdir}



%clean
# [ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-, root, root)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%{_libdir}/libprotobuf.so.%{soname}*
%{_libdir}/libprotobuf.a
%{_libdir64}/libprotobuf.so.%{soname}*
%{_libdir64}/libprotobuf.a
/usr/lib/libprotobuf.*
/usr/lib64/libprotobuf.*

%files compiler
%defattr(-, root, root)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%{_bindir}/protoc
%{_libdir}/libprotoc.so.%{soname}*
%{_libdir}/libprotoc.a
%{_libdir64}/libprotoc.so.%{soname}*
%{_libdir64}/libprotoc.a
/usr/lib/libprotoc.*
/usr/lib64/libprotoc.*

%files lite
%defattr(-, root, root)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
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
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%doc 32bit/examples/add_person.cc 32bit/examples/addressbook.proto
%doc 32bit/examples/list_people.cc 32bit/examples/Makefile
%doc 32bit/examples/README.md
%{_includedir}/google/protobuf
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir64}/libprotobuf.so
%{_libdir64}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc


# java
%files java
%defattr(-,root,root)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/README.md
%doc 32bit/examples/AddPerson.java 32bit/examples/ListPeople.java
%{javadir}/%{name}/protobuf*

# python
#%files -n python-%{name} -f python/INSTALLED_FILES
%files python
%defattr(-,root,root)
%doc 32bit/LICENSE
%doc 32bit/CHANGES.txt 32bit/CONTRIBUTORS.txt 32bit/python/README.md
%doc 32bit/examples/add_person.py 32bit/examples/list_people.py 32bit/examples/addressbook.proto
%{_libdir}/python2.7/site-packages/*



# For vim and emacs RPMs if needed
#%files vim
#%{_datadir}/vim/vimfiles/ftdetect/proto.vim
#%{_datadir}/vim/vimfiles/syntax/proto.vim

#%files emacs
#%{emacs_startdir}/protobuf-init.el
#%{emacs_lispdir}/protobuf-mode.elc
#
#%files emacs-el
#%{emacs_lispdir}/protobuf-mode.el





%changelog
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
