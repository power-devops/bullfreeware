# Tests by default. 
# No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# GCC compiler by defauft gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

Name: rsync
Version: 3.1.2
Release: 1
URL: http://rsync.samba.org
License: GPLv3+
Prefix:         %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define libdir64 %{_prefix}/lib64

Source0: ftp://rsync.samba.org/pub/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://rsync.samba.org/pub/%{name}/%{name}-%{version}.tar.gz.asc
Source2: ftp://rsync.samba.org/pub/%{name}/%{name}-patches-%{version}.tar.gz
Source3: ftp://rsync.samba.org/pub/%{name}/%{name}-patches-%{version}.tar.gz.asc
Source4: %{name}-%{version}.%{release}.build.log
#SID pb1
#Patch0:  %{name}-%{version}-aix_plat.patch

Summary: A program for synchronizing files over a network.
Group: Applications/Internet

# Perzl BuildRequires: patch make libiconv >= 1.14-2
BuildRequires: patch make
#Perzl Requires: popt libiconv >= 1.14-2
# Requires: popt
#  build with --with-included-popt

%description
Rsync uses a reliable algorithm to bring remote and host files into
sync very quickly. Rsync is fast because it just sends the differences
in the files over the network instead of sending the complete
files. Rsync is often used as a very powerful mirroring process or
just as a more capable replacement for the rcp command. A technical
report which describes the rsync algorithm is included in this
package.

# %package ssl-client
#Summary: Provides rsync-ssl
#Group: Applications/Internet
#Requires: rsync, stunnel >= 4

#%description ssl-client
#Summary: An stunnel config file to support ssl rsync daemon connections.
#Provides the rsync-ssl script that makes use of stunnel 4 to open an ssl
#connection to an rsync daemon (on port 874).  This setup does NOT require
#any local stunnel daemon to be running to connect to the remote ssl rsyncd.

#%package ssl-daemon
#Summary: An stunnel config file to support ssl rsync daemon connections.
#Group: Applications/Internet
#Requires: rsync, stunnel >= 4

#%description ssl-daemon
#Provides a config file for stunnel that will (if you start your stunnel
#service) cause stunnel to listen for ssl rsync-daemon connections and run
#"rsync --daemon" to handle them.


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

export PATH=/opt/freeware/bin:$PATH
%setup -q -b 2

# Needed for compatibility with previous patched rsync versions
patch -p1 -i patches/acls.diff
patch -p1 -i patches/xattrs.diff

# attention commenté chez IBM
# SID pb1 bis
#%patch0 -p1 -b .aix_plat

#Copied from Fedora : 5 lines

#Enable --copy-devices parameter
patch -p1 -i patches/copy-devices.diff

# SID pb2
#%patch0 -p1 -b .man
#%patch1 -p1 -b .noatime

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
######

# manually remove MKSTEMP from config.h
perl -i.bak -pe 's/#define HAVE_SECURE_MKSTEMP 1/\/* #undef HAVE_SECURE_MKSTEMP *\//' config.h


export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

#export CC="/usr/vac/bin/xlc_r  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export GLOBAL_CC_OPTIONS="-O2 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC="/opt/freeware/bin/gcc"
#export CXX="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC --version

%else

# XLC specific (do NOT compile yet...)
export CC="/usr/vac/bin/xlc"
#export CXX="/usr/vacpp/bin/xlC"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC -qversion

%endif

#export CC="/usr/vac/bin/xlc_r  -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"
export CC32=" ${CC}  ${FLAG32}"
#export CXX32="${CXX} ${FLAG32}"
export CC64=" ${CC}  ${FLAG64}"
#export CXX64="${CXX} ${FLAG64}"

build_rsync()
{
    cd ${OBJECT_MODE}bit
#    autoconf
    ./configure \
        --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
        --prefix=%{_prefix} \
        --libdir=$1 \
        --libexecdir=$1 \
        --with-included-popt \
        --mandir=%{_mandir} \
        --disable-acl-support
# SID to check how to support acl
# ajout IBM --with-included-popt
    echo "###########################################################" 
    echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit configure completed" 
    echo "###########################################################" 

    echo "MAKE :" ${MAKE} "_smp_mflags:" %{?_smp_mflags} "FIN :"  COPY="cp -p" Q=
    ${MAKE}  %{?_smp_mflags} COPY="cp -p" Q=
    echo "###########################################################" 
    echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit build completed"
    echo "###########################################################" 

    if [ "%{dotests}" == 1 ]
    then
        ${MAKE} -k test     || true
    fi
    echo "###########################################################" 
    echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE}bit tests completed" 
    echo "###########################################################" 
    cd ..
    
}

# build on 64bit mode
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
#export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
#export LDFLAGS="-L/opt/freeware/lib64"

build_rsync %{libdir64}

# build on 32bit mode
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
#export LDFLAGS="-L/opt/freeware/lib"

build_rsync %{_libdir}


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
export GLOBAL_CC_OPTIONS="-O2 "
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

${MAKE} DESTDIR=$RPM_BUILD_ROOT install  install-ssl-client install-ssl-daemon

mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d $RPM_BUILD_ROOT/etc/rsync-ssl/certs
/opt/freeware/bin/install -m644 packaging/lsb/rsync.xinetd $RPM_BUILD_ROOT/etc/xinetd.d/rsync

# strip rsync binary: rsync-ssl and stunnel-rsync are shell-scripts
# move <files>  bin to <files>_32
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in bin
  do
      cd $dir
      for fic in rsync ;
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
echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE} installation completed" 
echo "###########################################################" 


 
# installing 64bit mode

cd '%{_builddir}'/%{name}-%{version}/64bit

export OBJECT_MODE=64
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

${MAKE} DESTDIR=$RPM_BUILD_ROOT install  install-ssl-client install-ssl-daemon

# move bin/<files> to <files>_64
# and strip
# and link to <files>
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in bin 
  do
      cd $dir
      for fic in rsync ;
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
cd $RPM_BUILD_ROOT/%{_prefix}
mkdir -p usr/bin
cd usr/bin
ln -sf ../../%{_bindir}/rsync_64 rsync

echo "###########################################################" 
echo `date +%Y%m%d_%H%M%S`" : ${OBJECT_MODE} installation completed" 
echo "###########################################################" 


%clean
######
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT


%files
######
# Fedora %defattr(-,root,root)
%defattr(-,root,system)

#Fedora %doc NEWS OLDNEWS README support/ tech_report.tex
%doc 32bit/COPYING 32bit/doc/* 32bit/NEWS 32bit/OLDNEWS 32bit/README 32bit/TODO 32bit/support/* 32bit/tech_report.tex

%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*

%config(noreplace) /etc/xinetd.d/rsync

%attr(0755,root,system) %{_bindir}/rsync*
%{_prefix}/usr/bin/rsync

#%files ssl-client
#%{_prefix}/bin/rsync-ssl
#%{_prefix}/bin/stunnel-rsync

#%files ssl-daemon
#%config(noreplace) /etc/stunnel/rsyncd.conf
#%dir /etc/rsync-ssl/certs


%changelog
##########
* Wed Oct 19 2016 Daniele Silvestre <daniele.silvestre@atos.net> - 3.1.2-1
- Update to version 3.1.2
- Build 32 and 64 bit
- Compile with GCC or XLC
- Add tests

* Tue Mar 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 3.0.9-1
- Initial port on Aix6.1
