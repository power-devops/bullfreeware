# Tests by default. 
# No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# GCC compiler by defauft gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%define libdir64 %{_prefix}/lib64

Summary: A network traffic monitoring tool
Name: tcpdump
Version: 4.9.0
Release: 1
License: BSD with advertising
URL: http://www.tcpdump.org
Group: Applications/Internet
Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel
BuildRequires: libpcap-devel >= 1.8.1
BuildRequires: sed
Requires: openssl >= 1.0.1i-1
Requires: libpcap >= 1.8.1

#Configure option : without-smi 
#So remove libsmi requires
#BuildRequires: libsmi-devel >= 0.4.8-1
#Requires: libsmi >= 0.4.8-1

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "default_bits=%{default_bits}"

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

# export PATH=/opt/freeware/bin:$PATH

%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
#####
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
echo "GCC version=`$CC --version | head -1`"

%else

# XLC specific (do NOT compile yet...)
# export CC="cc -qcpluscmt"
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

 
build_tcpdump()
{
    cd ${OBJECT_MODE}bit

    # configure options
    # --without-smi : don't link with libsmi
    ./configure \
        --prefix=%{_prefix} \
        --mandir=%{_mandir} \
        --without-smi

    echo "###########################################################" 
    echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE}bit configure completed" 
    echo "###########################################################" 

    echo "MAKE :" ${MAKE} "_smp_mflags:" %{?_smp_mflags} 
    ${MAKE}  %{?_smp_mflags}
    echo "###########################################################" 
    echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE}bit build completed"
    echo "###########################################################" 

    if [ "%{dotests}" == 1 ]
    then
        ${MAKE} -k check     || true
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

build_tcpdump %{_libdir}

# build on 64bit mode
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
#export LDFLAGS="-L/opt/freeware/lib64"

build_tcpdump %{libdir64}

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

cd 32bit
pwd
cd '%{_builddir}'/%{name}-%{version}/32bit
pwd

export OBJECT_MODE=32
export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=""

${MAKE} DESTDIR=$RPM_BUILD_ROOT install 


# strip binaries:
# originally strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :
# move <files>  bin to <files>_32
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in sbin
  do
      cd $dir
      for fic in * ;
      do
          [ -L "$fic" ] && continue
          [ -f "$fic" ] || continue
          /usr/bin/strip -X32 $fic
          mv $fic $fic"_32"
      done
      cd -
  done
)
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

# move sbin/<files> to <files>_64
# and strip
# and link to <files>
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in sbin 
  do
      cd $dir
      for fic in * ;
      do
          [ -L "$fic" ] && continue
          [ -f "$fic" ] || continue
          grep _32 $fic || continue
          /usr/bin/strip -X64 $fic
          mv $fic $fic"_64"
          ln -s $fic"_64" $fic  # By default, binaries link to 64bit
      done
      cd -
  done
)


echo "###########################################################" 
echo `date +%Y%m%d_%H%M`" : ${OBJECT_MODE} installation completed" 
echo "###########################################################" 


#install man1/tcpdump.1 as ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdump.8
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man8
mv -f ${RPM_BUILD_ROOT}%{_mandir}/man1/tcpdump.1 ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdump.8

# and fix section numbers
/opt/freeware/bin/sed -i 's/\(\.TH[a-zA-Z ]*\)[1-9]\(.*\)/\18\2/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man8/*


%clean
######
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc 64bit/LICENSE 64bit/README.md 64bit/CHANGES 64bit/CREDITS
%{_mandir}/man8/tcpdump*
%{_sbindir}/tcpdump*

# Standard AIX lpp :  bos.net.tcp.tcpdump installs under /usr/sbin/tcpdump an old version of the tcpdump version
# Be careful don't overwrite it

%changelog
* Fri Feb 03 2017 Daniele Silvestre  <daniele.silvestre@atos.net - 4.9.0-1
- updated to version 4.9.0

* Fri Jan 13 2017 Daniele Silvestre  <daniele.silvestre@atos.net - 4.8.1-1
- updated to version 4.8.1
- 64-bit binary

* Tue Jan 19 2016 Tony Reix <tony.reix@atos.net - 4.7.4-1
- updated to version 4.7.4

* Wed Aug 13 2014 Michael Perzl <michael@perzl.org> - 4.6.2-1
- updated to version 4.6.2

* Wed Aug 13 2014 Michael Perzl <michael@perzl.org> - 4.6.1-1
- updated to version 4.6.1

* Thu Nov 28 2013 Michael Perzl <michael@perzl.org> - 4.5.1-1
- updated to version 4.5.1

* Wed Jun 26 2013 Michael Perzl <michael@perzl.org> - 4.4.0-1
- updated to version 4.4.0

* Mon Jun 25 2012 Michael Perzl <michael@perzl.org> - 4.3.0-1
- updated to version 4.3.0

* Sat Jan 28 2012 Michael Perzl <michael@perzl.org> - 4.2.1-1
- updated to version 4.2.1

* Tue Apr 13 2010 Michael Perzl <michael@perzl.org> - 4.1.1-1
- updated to version 4.1.1

* Tue Apr 13 2010 Michael Perzl <michael@perzl.org> - 3.9.8-1
- first version for AIX V5.1 and higher
