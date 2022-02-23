# Tests by default.
# No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# GCC compiler by defauft gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%define _libdir64 %{_prefix}/lib64

Name: libpcap
Version: 1.8.1
Release: 1
Summary: A system-independent interface for user-level packet capture
Group: Development/Libraries
License: BSD
URL: http://www.tcpdump.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig
Source2: %{name}.so.0.9.8-aix32
Source3: %{name}.so.0.9.8-aix64

%description
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Libraries and header files for the libpcap library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Libpcap provides a portable framework for low-level network
monitoring.  Libpcap can provide network statistics collection,
security monitoring and network debugging.  Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

This package provides the libraries, include files, and other 
resources needed for developing libpcap applications.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%endif
%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%endif


 
%prep
#####
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "default_bits=%{default_bits}"

export PATH=/opt/freeware/bin:$PATH

%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
######
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

#originally export CC="cc -qcpluscmt -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"

# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC="/opt/freeware/bin/gcc"
#export CXX="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64 -g"

echo "GCC version=`$CC --version | head -1`"

%else

# XLC specific (do NOT compile yet...)
export CC="/usr/vac/bin/xlc"
export CXX="/usr/vacpp/bin/xlC"
export FLAG32="-q32 -qcpluscmt"
export FLAG64="-q64 -qcpluscmt"

echo "XLC Version:"
$CC -qversion

%endif

export CC32=" ${CC}  ${FLAG32}"
export CXX32="${CXX} ${FLAG32}"
export CC64=" ${CC}  ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"

export GLOBAL_CC_OPTIONS="-O2 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"


build_libpcap()
{
    cd ${OBJECT_MODE}bit
    ./configure \
        --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
        --prefix=%{_prefix} \
        --libdir=$1 \
        --libexecdir=$1 \
        --mandir=%{_mandir} \
        --enable-ipv6 \
        --with-pcap=bpf

    echo "###########################################################"
    echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE}bit configure completed"
    echo "###########################################################"

    echo "MAKE :" ${MAKE} "_smp_mflags:" %{?_smp_mflags} 
    ${MAKE}  %{?_smp_mflags} 
    echo "###########################################################"
    echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE}bit build completed"
    echo "###########################################################"

    mv shr.o shr_${OBJECT_MODE}.o

    # make test produces tests program but don't run them automaticall
    if [ "%{dotests}" == 1 ]
    then
        ${MAKE} -k tests     || true
    fi
    echo "###########################################################"
    echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE}bit tests completed"
    echo "###########################################################"
    cd ..

}


# build on 32bit mode
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
#export LDFLAGS="-L/opt/freeware/lib"

build_libpcap %{_libdir}

# build on 64bit mode
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
#export LDFLAGS="-L/opt/freeware/lib64"

build_libpcap %{_libdir64}


# standard libpcap Makefile creates the static lib : libpcap.a and the shared lib : libpcap.shareda
# and then install-sh script delivers libpcap.shareda as shared library lib/libpcap.a
# hack to generate AIX-style shared libraries : lib/libxxx.a includes both 32 and 64 bits libxxx objects
cd '%{_builddir}'/%{name}-%{version}/32bit
cp '%{_builddir}'/%{name}-%{version}/64bit/shr_64.o .
/usr/bin/ar -X32_64 -q %{name}.shareda shr_64.o

# Add the older 0.9.8 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} %{name}.so.0.9.8
/usr/bin/strip -X32 -e %{name}.so.0.9.8
/usr/bin/ar -X32_64 -q %{name}.shareda %{name}.so.0.9.8

cp %{SOURCE3} %{name}.so.0.9.8
/usr/bin/strip -X64 -e %{name}.so.0.9.8
/usr/bin/ar -X32_64 -q %{name}.shareda %{name}.so.0.9.8


%install
########
export RBUILD=$PWD
export INSTALL=/opt/freeware/bin/install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export MAKE="gmake --trace"

echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

# installing 32bit mode

cd '%{_builddir}'/%{name}-%{version}/32bit
pwd

export OBJECT_MODE=32
export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=""

${MAKE} DESTDIR=$RPM_BUILD_ROOT install


# no binaries to strip : bin dir only contain pcap-config file

echo "###########################################################"
echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE} installation completed"
echo "###########################################################"

# installing 64bit mode

cd '%{_builddir}'/%{name}-%{version}/64bit

export OBJECT_MODE=64
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

${MAKE} DESTDIR=$RPM_BUILD_ROOT install 

# no binaries to strip : bin dir only contain pcap-config file
(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib bin
  do
    mkdir -p usr/linux/${dir}
    cd usr/linux/${dir}
    ln -sf ../../..%{_prefix}/${dir}/* .
    cd -
  done
)

echo "###########################################################"
echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE} installation completed"
echo "###########################################################"



%clean
######
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
######
%defattr(-,root,system)
%doc 64bit/CHANGES 64bit/CREDITS 64bit/INSTALL.txt 64bit/LICENSE 64bit/README 64bit/README.aix
%{_libdir}/*.a
/usr/linux/lib/*.a

%files devel
%defattr(-,root,system)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/man3/*
/usr/linux/bin/*
/usr/linux/include/*


%changelog
* Wed Jan 04 2017 Daniele Silvestre <daniele.silvestre@atos.net - 1.8.1-1
- updated to version 1.8.1

* Tue Jan 19 2016 Tony Reix <tony.reix@atos.net - 4.7.4-1
- updated to version 4.7.4

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 1.6.2-1
- updated to version 1.6.2

* Wed Aug 13 2014 Michael Perzl <michael@perzl.org> - 1.6.1-1
- updated to version 1.6.1

* Mon Jan 20 2014 Michael Perzl <michael@perzl.org> - 1.5.3-1
- updated to version 1.5.3

* Thu Nov 28 2013 Michael Perzl <michael@perzl.org> - 1.5.1-1
- updated to version 1.5.1

* Wed Jun 26 2013 Michael Perzl <michael@perzl.org> - 1.4.0-1
- updated to version 1.4.0

* Tue Apr 30 2013 Michael Perzl <michael@perzl.org> - 1.3.0-2
- enabled IPV6

* Mon Jun 25 2012 Michael Perzl <michael@perzl.org> - 1.3.0-1
- updated to version 1.3.0

* Sat Jan 28 2012 Michael Perzl <michael@perzl.org> - 1.2.1-1
- updated to version 1.2.1

* Mon Nov 28 2011 Michael Perzl <michael@perzl.org> - 1.2.0-1
- updated to version 1.2.0
- added symbolic links to /usr/linux

* Tue Apr 13 2010 Michael Perzl <michael@perzl.org> - 1.1.1-1
- updated to version 1.1.1

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 0.9.8-2
- included both 32-bit and 64-bit shared objects

* Tue Oct 16 2007 Michael Perzl <michael@perzl.org> - 0.9.8-1
- first version for AIX V5.1 and higher
