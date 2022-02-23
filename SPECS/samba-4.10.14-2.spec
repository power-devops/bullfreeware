%bcond_without dotests

# Tests cannot be run by default
%bcond_with testsuite

%bcond_without python2
%bcond_with python3

# Use gcc by default
%bcond_with xlc

# 32bit does not work
%bcond_with thirtyTwoBits

%if %{with testsuite}
    %define with_dc 1
%else
    %define with_dc 0
%endif
#
# The ctdb is disabled by default and is specified by configure
# option  --with-cluster-support
#
# Profiling requires configure option  --with-profiling-data
#
# Samba VFS module for GlusterFS (x86_64 only) requires configure
# option  --disable-glusterfs (no package for vfs-glusterfs).
#
# MIT Kerberos requires configure option  --with-system-mitkrb5
#
# Samba AD Domain Controller is enabled by default (--without-ad-dc)

%define samba_version 4.10.14
# Fedora uses package libtalloc at version 2.1.10 (latest 2.1.11)
%define talloc_version 2.1.14
# Fedora uses package libtdb at version 1.3.15
%define tdb_version 1.3.16
%define tevent_version 0.9.37
%define ldb_version 1.4.3

%define wbpriv_gid 88

%define with_libuuid 0
%define with_GPFS    0


%define python2_sitearch32 %(/opt/freeware/bin/python2_32 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python2_sitearch64 %(/opt/freeware/bin/python2_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%define python3_sitearch32 %(/opt/freeware/bin/python3_32 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%define python3_sitearch64 %(/opt/freeware/bin/python3_64 -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

# perl_lib_install_dir is hard coded in file buildtools/wafsamba/samba_perl.py
%define perl_lib %{_datadir}/perl5/vendor_perl/

%define _libdir64 %{_prefix}/lib64

Summary: Server and Client software to interoperate with Windows machines
Name: samba
Version: %{samba_version}
Release: 2
License: GPLv3+ and LGPLv3+
URL: http://www.samba.org/

Source0: https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.gz
Source1: https://download.samba.org/pub/samba/stable/%{name}-%{version}.tar.asc

Source2: %{name}.log
Source4: %{name}.sysconfig
Source5: smb.conf.default
Source6: smbprint
Source7: smbd.aix.init
Source8: nmbd.aix.init
Source9: winbindd.aix.init

Source10: %{name}-%{version}-%{release}.build.log
Source11: README.AixSambaInstallGuide
Source12: ctdbd.conf

# Export winbindd binary symbols for idmap/ad.so winbindd_ads.c/wb_dsgetdcname.c
Source13: samba_winbind_idmap_syms.exp

# To perform minimal check
Source14: test_samba.sh

Patch1: samba-4.2.0-aix.patch
Patch2: 0002-Bug-8984-AIX-6.1-nmbd-Failed-to-open-nmb-bcast-socket.patch
# Patch3: samba-4.7.6-Time.patch
Patch3: samba-4.9.3-Time.patch
# Toolbox patches
Patch4: samba-4.9.3-resolv_wrapper.patch
Patch5: samba-4.5.0-closefrom_dirfd.patch

# Need a run time test to set open() flags
Patch13: samba-4.7.6-openO_NOFOLLOW.patch

# Toolbox patches
Patch7:  gpfswrapper-aix.patch
Patch8:  samba-4.9.3-ctdb-aix.patch

# The wscript_build has to specify an entrypoint for the WINBIND module
Patch14: samba-4.5.10-WINBINDentrypoint.patch

# Toolbox patches
Patch15: samba_winbindd_syms.patch
Patch16: samba-4.10.14-msdfs-aix.patch
Patch17: samba-4.9.3-time-aix.patch
Patch18: samba-posix_fallocate-aix.patch
# Patch19: samba-4.9.6-name_max.patch

Patch21: samba-4.10.14-Struc_bad_initialization.patch
Patch22: samba-4.2.0-BadInitializationTypes.patch
Patch23: samba-4.2.0-BadInitializationTypesA.patch
# Patch9: samba-4.9.0-resolv_wrapper.patch
# Patch10: samba-4.5.0-closefrom_dirfd.patch
# Following patch is a temporary(?) work around for XLC internal error
Patch11: samba-4.3.6-xlcWA.patch
# Following patch is a temporary(?) work around for XLC preprocessor error
Patch12: samba-4.5.0-xlcIfdefWA.patch
# From Toolbox
Patch24: samba-4.10.14-Struc_bad_initialization-2.patch
Patch25: samba-4.10.6-struct-initialization.patch

%if %{without xlc}
# Erase -Wl,-h/B/R from python files. Needed for gcc build on AIX
Patch26: samba-4.10.14-gcc.patch
Patch27: samba-4.10.14-build_with_gcc.patch
# This patch must be applied after configure
# With bexfull
Source1001: samba-4.10.14-cache-py.patch
# Without bexpfull
#Source1001: samba-4.10.14-cache-py-2.patch
%endif

# Structure timespec is not declared in AIX stat.h before AIX 7.1
# Patch21: samba-4.9.0-timespec.patch
# Structure shutdown_state redefines ip_len declared in AIX netinet/ip.h
# Patch22: samba-4.9.0-ip_len-conflict-aix.patch
# Issue in posix_fallocate()
# Patch23: samba-4.9.0-posix_fallocate.patch

# Compiling on AIX 6.1 for execution on 6.1, 7.1, 7.2
# O_NOFOLLOW not supported on 6.1
# O_NOFOLLOW defined as _FCLREAD    0x02000000 on 7.1
# O_NOFOLLOW defined                0x01000000 on 7.2

# The docs are no longer built
Obsoletes: samba-doc
# Not supported yet
Obsoletes: samba-domainjoin-gui
# SWAT been deprecated and removed from samba
Obsoletes: samba-swat


BuildRequires: make, patch, rpcgen

BuildRequires: cups-devel >= 1.4.4-2

# BuildRequires: gtk2-devel >= 2.8.3-9
# 2 New in 4.9 w.r.t. 4.7.10
# BuildRequires: gpgme-devel
# BuildRequires: jansson-devel

# BuildRequires: krb5-devel >= 1.8.3-1
# May be BuildRequires: krb5-devel >= 1.15.1
#BuildRequires: libiconv >= 1.14-1
# 2 New in 4.9 w.r.t. 4.7.10
#BuildRequires: libnsl2-devel
#BuildRequires: libtirpc-devel

BuildRequires: ncurses-devel >= 6.2
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: popt >= 1.16-4
BuildRequires: readline-devel >= 7.0-1
%if %{with_libuuid}
BuildRequires: uuid-devel >= 1.6.2-1
%endif
BuildRequires: gnutls-devel
BuildRequires: libtasn1-tools
BuildRequires: libarchive-devel >= 3.3.3-2
Requires:      libarchive >= 3.3.3-2
BuildRequires: perl(perl)

# Previous versions of libgcrypt were provided .so files
BuildRequires: libgcrypt-devel >= 1.8.6-2
Requires: libgcrypt >= 1.8.6-2

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}

Requires: bash
Requires: cups >= 2.3.1
# Requires: logrotate >= 3.7.9-2


%description
Samba is the suite of programs by which a lot of PC-related machines
share files, printers, and other information (such as lists of
available files and printers). The Windows NT, OS/2, and Linux
operating systems support this natively, and add-on packages can
enable the same thing for DOS, Windows, VMS, UNIX of all kinds, MVS,
and more. This package provides an SMB/CIFS server that can be used to
provide network services to SMB/CIFS clients.
Samba uses NetBIOS over TCP/IP (NetBT) protocols and does NOT
need the NetBEUI (Microsoft Raw NetBIOS frame) protocol.



%package all
Summary: Meta-package to include all Samba RPMs
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
Requires: %{name}-winbind-devel = %{version}-%{release}
Requires: %{name}-winbind-krb5-locator = %{version}-%{release}
Requires: libsmbclient = %{version}-%{release}
Requires: libsmbclient-devel = %{version}-%{release}
Requires: %{name}-python = %{version}-%{release}
Requires: %{name}-pidl = %{version}-%{release}

%description all
Samba is the suite of programs by which a lot of PC-related machines
share files, printers, and other information (such as lists of
available files and printers). The Windows NT, OS/2, and Linux
operating systems support this natively, and add-on packages can
enable the same thing for DOS, Windows, VMS, UNIX of all kinds, MVS,
and more. This package provides an SMB/CIFS server that can be used to
provide network services to SMB/CIFS clients.
Samba uses NetBIOS over TCP/IP (NetBT) protocols and does NOT
need the NetBEUI (Microsoft Raw NetBIOS frame) protocol.

This is a meta-package including all Samba components.



%package client
Summary: Samba client programs
Requires: bash
Requires: %{name}-common = %{version}-%{release}
# Include samba-client-libs
# Requires: %{name}-client-libs = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}

%description client
The samba-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.


# Common package grouping common files with common-libs and common-tools
%package common
Summary: Files used by both Samba servers and clients
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}
# Requires: krb5-libs >= 1.9.4-2
# May be Requires: krb5-libs >= 1.14 (not yet on Bullfreeware)
Requires: openldap >= 2.4.23
Requires: popt >= 1.16-4
Requires: readline >= 7.0-1
Requires: libiconv >= 1.14-2
Requires: gnutls >= 3.6.13-1
%if %{with_libuuid}
Requires: uuid >= 1.6.2-1
%endif
Requires: zlib >= 1.2.3-3

%description common
Samba-common provides files and tools necessary for both the server and client
packages of Samba and internal libraries needed by the SMB/CIFS clients.


# samba-devel package needed to develop programs
%package devel
Summary: Developer tools for Samba libraries
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
The samba-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.


# samba-libs package
%package libs
Summary: Samba libraries
Requires: krb5-libs >= 1.9.4-2

%description libs
The samba-libs package contains the libraries needed by programs that
link against the SMB, RPC and other protocols provided by the Samba suite.


%package winbind
Summary: Samba winbind
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
# Requires: %{name}-winbind-modules = %{version}-%{release}

%description winbind
The samba-winbind package provides the winbind daemon, the winbind NSS library
and some client tools.
Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.


%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
Requires: %{name}-winbind = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use


%package winbind-clients
Summary: Samba winbind clients
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}

%description winbind-clients
The samba-winbind-clients package provides the NSS library and a PAM
module necessary to communicate to the Winbind Daemon


%package winbind-devel
Summary: Developer tools for the winbind library
Requires: %{name}-winbind = %{version}-%{release}

%description winbind-devel
The samba-winbind-devel package provides developer tools for the wbclient library.


%package -n libsmbclient
Summary: The SMB client library
Requires: %{name}-common = %{version}-%{release}

%description -n libsmbclient
The libsmbclient contains the SMB client library from the Samba suite.


%package -n libsmbclient-devel
Summary: Developer tools for the SMB client library
Requires: libsmbclient = %{version}-%{release}

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed to
develop programs that link against the SMB client library in the Samba suite.


%if %{with python2}
# Python 2 is required for Samba AD DC
%package python
Summary: Samba Python libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: python
# Requires: python-tevent
# Requires: python-tdb
# Requires: pyldb
# Requires: pytalloc

%description python
The samba-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.


%package -n python-samba-test
Summary: Samba Python libraries
Requires: %{name}-python = %{version}

%description -n python-samba-test
The python-%{name}-test package contains the Python libraries used by the
test suite of Samba.
If you want to run full set of Samba tests, you need to install this package.
%endif

%if %{with python3}
%package python3
Summary: Samba Python libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: python3 >= 3.8
# Requires: python-tevent
# Requires: python-tdb
# Requires: pyldb
# Requires: pytalloc

%description python3
The samba-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.


%package -n python3-samba-test
Summary: Samba Python libraries
Requires: %{name}-python3 = %{version}

%description -n python3-samba-test
The python-%{name}-test package contains the Python libraries used by the
test suite of Samba.
If you want to run full set of Samba tests, you need to install this package.
%endif


# %if %{with_dc}
%if %{with python2}
%package -n python-samba-dc
Summary: Samba Python libraries for Samba AD
Requires: python-%{name} = %{version}

%description -n python-samba-dc
The python-%{name}-dc package contains the Python libraries needed by programs
to manage Samba AD.
%endif


%if %{with python3}
%package -n python3-samba-dc
Summary: Samba Python libraries for Samba AD
Requires: python-%{name} = %{version}

%description -n python3-samba-dc
The python-%{name}-dc package contains the Python libraries needed by programs
to manage Samba AD.
%endif
# %endif


%package pidl
Summary: Perl IDL compiler
Requires: perl(perl)
# Requires: perl(Parse::Yapp)
# Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description pidl
The samba-pidl package contains the Perl IDL compiler used by Samba
and Wireshark to parse IDL and similar protocols


# There is also the possibility of constructing packages for testing
# tools for Samba servers and clients (samba-test, samba-test-libs,
# samba-test-devel) essentially containing gentest, locktest, masktest,
# ndrdump, smbtorture/libtorture.

### TEST
%package test
Summary: Testing tools for Samba servers and clients
Requires: %{name} = %{samba_version}
Requires: %{name}-common = %{samba_version}
Requires: %{name}-winbind = %{samba_version}

# Requires: %{name}-client-libs = %{samba_version}
Requires: %{name}-libs = %{samba_version}
Requires: %{name}-test-libs = %{samba_version}
# %if %with_dc
# Requires: %{name}-dc-libs = %{samba_version}
# %endif
Requires: %{name}-libs = %{samba_version}
# %if %with_libsmbclient
Requires: libsmbclient = %{samba_version}
# %endif
# %if %with_libwbclient
# Requires: libwbclient = %{samba_version}
# %endif

Provides: samba4-test = %{samba_version}
Obsoletes: samba4-test < %{samba_version}

%description test
The samba-test provides testing tools for both the server and client
packages of Samba.

### TEST-LIBS
%package test-libs
Summary: Libraries need by the testing tools for Samba servers and clients
# Requires: %{name}-client-libs = %{samba_version}
Requires: %{name}-libs = %{samba_version}

Provides: %{name}-test-devel = %{samba_version}
Obsoletes: %{name}-test-devel < %{samba_version}

%description test-libs
The samba-test-libs provides libraries required by the testing tools.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

%patch1
%patch2 -p1
%patch3 -p1 -b .Time
# Following patch corrected in code for 4.9.0
# %patch4 -p1
%patch4 -p1
%patch5 -p1

#%patch6 -p1
%patch7 -p1
%patch8 -p1 
#%patch9 -p1 
#%patch10 -p1 

# Following patch is a temporary(?) work around for XLC internal error
%patch11 -p1
# Following patch is a temporary(?) work around for XLC preprocessor error
%patch12 -p1
%patch13 -p1
%patch14 -p1
# Export winbindd binary symbols for idmap/ad.so winbindd_ads.c/wb_dsgetdcname.c
%patch15 -p1
# EINVAL returned from pthread_cond_destroy() after fork() on AIX
%patch16 -p1

%patch17 -p1

# Integrated in Samba 4.7.10


%patch18 -p1 -b .Aggregated

# Fedora following patch for compile flags
# Removed in 4.9.4  %patch20 -p1 -b .StackProtector

# Structure timespec is not declared in AIX stat.h before AIX 7.1
%patch21 -p1 -b .timespec
# Structure shutdown_state redefines ip_len declared in AIX netinet/ip.h
%patch22 -p1 -b .iplen
# Issue in posix_fallocate()
%patch23 -p1 -b .posix_fallocate

%patch24 -p1

%patch25 -p1
%if %{without xlc}
%patch26 -p0 -b .gcc
%patch27 -p1 -b .build_with_gcc
%endif

cp %{SOURCE12}  ./source3/winbindd/samba_winbind_idmap_syms.exp

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

# Fedora does not include  idmap_adex
%global _samba_idmap_modules idmap_ad,idmap_rid,idmap_adex,idmap_hash,idmap_tdb2

# Fedora does not include  pdb_ads
%global _samba_pdb_modules pdb_tdbsam,pdb_ldap,pdb_ads,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4

# Fedora does not include  auth_netlogond
%global _samba_auth_modules auth_unix,auth_wbc,auth_server,auth_netlogond,auth_script,auth_samba4

%global _samba_vfs_modules vfs_dfs_samba4

%global _samba_modules %{_samba_idmap_modules},%{_samba_pdb_modules},%{_samba_auth_modules},%{_samba_vfs_modules}


# function to build samba
# include --enable-selftest if make test is to be used
build_samba()
{
set -ex

  ./configure \
      --prefix=%{_prefix} \
      --libdir=$1 \
      --includedir=%{_includedir}/samba-4.0 \
      --sysconfdir=/etc/%{name} \
      --mandir=%{_mandir} \
      --with-lockdir=/var/locks \
      --with-piddir=/var/run \
      --with-privatedir=/var/lib/%{name}/private \
      --with-privatelibdir=$1/%{name} \
      --with-logfilebase=/var/log/%{name} \
      --with-logdir=/var/log/%{name} \
      --with-modulesdir=$1/%{name} \
      --with-pammodulesdir=$1/security \
      --with-cachedir=/var/cache \
      --with-acl-support \
      --with-ads \
      --without-ad-dc \
      --without-cluster-support \
      --with-automount \
      --disable-python \
      --without-json \
%if %{with_libuuid}
      --with-dnsupdate \
%endif
      --with-ldap \
      --with-libiconv=%{_prefix} \
      --with-pam \
      --with-quotas \
      --with-sendfile-support \
      --with-syslog \
      --with-utmp \
      --with-libarchive \
%if %{with_GPFS}
      --with-shared-modules=%{_samba_modules},vfs_gpfs \
      --with-gpfs \
%else
      --with-shared-modules=%{_samba_modules} \
      --disable-glusterfs \
%endif
%if %{with testsuite}
      --enable-selftest \
%endif

  # On 64 bit, bad link to /opt/freeware/lib/libz.so
  # Workaround: change file generated.
  # Better solution: rebuild libz witout .so
  patch -p1 < %{SOURCE1001}

  # A smnotify file is badly generated during build
#   ( gmake smnotify || true )
#   sed -i 's|#ifdef 1|#ifdef _AIX|' bin/default/ctdb/utils/smnotify/smnotify.h
#   gmake smnotify

  gmake %{?_smp_mflags}

  gmake debug2html smbfilter

}

cd 64bit
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib64/samba:/opt/freeware/lib:/opt/freeware/lib/samba:/usr/vac/lib:/usr/lib:/lib"
export PYTHON=/opt/freeware/bin/python2_64
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"

%if %{with xlc}
# XLC -- tested with 13.1.3, does not work
export CC="/usr/bin/xlc_r"
export CXX="/usr/bin/xlC_r"
export CFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet -D__PRETTY_FUNCTION__=__func__ -mcmodel=large -I/opt/freeware/include"
export CXXFLAGS="-D_LARGE_FILES=1 -qcpluscmt -mcmodel=large -I/opt/freeware/include"
%else
# GCC
export CC="/opt/freeware/bin/gcc -maix64"
export CXX="/opt/freeware/bin/g++ -maix64"
export CFLAGS="-D_LARGE_FILES=1 -mcmodel=large"
export CXXFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet"
%endif

build_samba %{_libdir64}
cd ..

%if %{with thirtyTwoBits}
cd 32bit
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/opt/freeware/lib/samba:/usr/vac/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export PYTHON=/opt/freeware/bin/python2_32
export LIBPATH="/opt/freeware/lib:/usr/lib"

%if %{with xlc}
# XLC -- tested with 13.1.3, does not work
export CC="/usr/bin/xlc_r"
export CXX="/usr/bin/xlC_r"
export CFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet -D__PRETTY_FUNCTION__=__func__ -mcmodel=large -I/opt/freeware/include"
export CXXFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet -mcmodel=large -I/opt/freeware/include"
%else
# GCC
export CC="/opt/freeware/bin/gcc -maix32"
export CXX="/opt/freeware/bin/g++ -maix32"
export CFLAGS="-D_LARGE_FILES=1 -mcmodel=large"
export CXXFLAGS="-D_LARGE_FILES=1 -mcmodel=large"
%endif

build_samba %{_libdir}
cd ..
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Error in install due to "Generating PKGCONFIG_samba-credentials.pc" and others
cd 64bit
export OBJECT_MODE=64

rm -f ./bin/default/auth/credentials/samba-credentials.pc
rm -f ./bin/default/nsswitch/libwbclient/wbclient.pc
rm -f ./bin/default/lib/util/samba-util.pc
rm -f ./bin/default/source4/rpc_server/dcerpc_server.pc
rm -f ./bin/default/librpc/ndr_krb5pac.pc
rm -f ./bin/default/librpc/ndr_standard.pc
rm -f ./bin/default/librpc/ndr_nbt.pc
rm -f ./bin/default/librpc/ndr.pc
rm -f ./bin/default/source4/lib/policy/samba-policy.pc
rm -f ./bin/default/source3/libnet/netapi.pc
rm -f ./bin/default/source3/libsmb/smbclient.pc

rm -f ./bin/default/source3/rpc_server/rpc.empty.c



echo ---------- ${RPM_BUILD_ROOT} ------------------------------------------------------------------------------
# (gmake install DESTDIR=${RPM_BUILD_ROOT} %{?_smp_mflags} || true )
# sed -i 's|#ifdef 1|#ifdef _AIX|' bin/default/ctdb/utils/smnotify/smnotify.h
gmake install DESTDIR=${RPM_BUILD_ROOT} %{?_smp_mflags}

pwd


/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_sbindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d

mkdir -p ${RPM_BUILD_ROOT}/etc/%{name}
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/winbindd_privileged
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/scripts
mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}/sysvol
mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}/old
mkdir -p ${RPM_BUILD_ROOT}/var/spool/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/samba/setup
# mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/swat/using_samba
mkdir -p ${RPM_BUILD_ROOT}/var/run/winbindd
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/security/WINBIND
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/var/run/nmbd

cp %{SOURCE5} ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf
chmod 0644 ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf

cp source3/script/mksmbpasswd.sh ${RPM_BUILD_ROOT}%{_bindir}/
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/mksmbpasswd.sh

# File smbusers has disappeared from the build
# cp samba-%{version}/packaging/RHEL/setup/smbusers ${RPM_BUILD_ROOT}/etc//%{name}/smbusers
# chmod 0644 ${RPM_BUILD_ROOT}/etc//%{name}/smbusers

cp packaging/printing/smbprint ${RPM_BUILD_ROOT}%{_bindir}/
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/smbprint

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

echo 127.0.0.1 localhost > ${RPM_BUILD_ROOT}/etc/%{name}/lmhosts

mkdir -p ${RPM_BUILD_ROOT}/etc/openldap/schema
cp examples/LDAP/%{name}.schema ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema
chmod 0644 ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema

# winbind krb5 locator
mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/krb5/plugins/libkrb5
cp bin/shared/winbind_krb5_locator.so ${RPM_BUILD_ROOT}%{_libdir64}/krb5/plugins/libkrb5/winbind_krb5_locator.so
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir64}/krb5/plugins/libkrb5/winbind_krb5_locator.so

# WINBIND from libnss_winbind.so / nsswitch/winbind_nss_aix.c
cp bin/shared/WINBIND.so ${RPM_BUILD_ROOT}%{_libdir64}/security/WINBIND

# pkgconfig files
#list="smbclient smbsharemodes wbclient"
#for i in ${list} ; do
#    cp %{samba_source}/pkgconfig/${i}.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/
#done
cp bin/default/source3/libsmb/smbclient.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/ 
cp bin/default/source3/libnet/netapi.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/ 
cp bin/default/nsswitch/libwbclient/wbclient.pc ${RPM_BUILD_ROOT}%{_libdir64}/pkgconfig/

mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
cp %{SOURCE4} ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}
chmod 0644 ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}

# create additional directory structure
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d

# move the files into the structure
cp %{SOURCE7} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/smbd
cp %{SOURCE8} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/nmbd
cp %{SOURCE9} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/winbindd
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/*

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/doc
cp %{SOURCE11} ${RPM_BUILD_ROOT}%{_docdir}/%{name}-%{version}/README.AixSambaInstallGuide

# make symlinks for the appropriate run levels
for i in smbd nmbd winbindd
do
     ln -sf ../init.d/${i}  ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/S${i}
     ln -sf ../init.d/${i}  ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/K${i}
     ln -sf ../init.d/${i}  ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/S${i}
     ln -sf ../init.d/${i}  ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/K${i}
done

# create symlinks to library modules

# samba_common
{
  cd ${RPM_BUILD_ROOT}%{_libdir64}/samba
  for i in talloc pytalloc-util tevent tdb ldb pyldb-util heimntlm-samba4 kdc-samba4
  do
      ln -sf lib${i}.so.*.*.*  lib${i}.so
  done
}

#ln -sf  libtalloc.so.%{talloc_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libtalloc.so
#ln -sf  libpytalloc-util.so.%{talloc_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libpytalloc-util.so
#ln -sf  libtevent.so.%{tevent_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libtevent.so
#ln -sf  libtdb.so.%{tdb_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libtdb.so
#ln -sf  libldb.so.%{ldb_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libldb.so
#ln -sf  libpyldb-util.so.%{ldb_version}     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libpyldb-util.so
#ln -sf  libheimntlm-samba4.so.1.0.1     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libheimntlm-samba4.so
#ln -sf  libkdc-samba4.so.2.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libkdc-samba4.so

# samba_libs
{
  cd ${RPM_BUILD_ROOT}%{_libdir64}/samba
  for i in asn1 gssapi hcrypto hdb heimbase hx509 krb5 roken wind
  do
      ln -sf lib${i}-samba4.so.*.*.*  lib${i}-samba4.so
  done
  ln -sf  libcom_err-samba4.so.*.*  libcom_err-samba4.so
}
#ln -sf  libasn1-samba4.so.8.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libasn1-samba4.so
#ln -sf  libcom_err-samba4.so.0.25     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libcom_err-samba4.so
#ln -sf  libgssapi-samba4.so.2.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libgssapi-samba4.so
#ln -sf  libhcrypto-samba4.so.5.0.1     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libhcrypto-samba4.so
#ln -sf  libhdb-samba4.so.11.0.2     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libhdb-samba4.so
#ln -sf  libheimbase-samba4.so.1.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libheimbase-samba4.so
#ln -sf  libhx509-samba4.so.5.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libhx509-samba4.so
#ln -sf  libkrb5-samba4.so.26.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libkrb5-samba4.so
#ln -sf  libroken-samba4.so.19.0.1     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libroken-samba4.so
#ln -sf  libwind-samba4.so.0.0.0     ${RPM_BUILD_ROOT}%{_libdir64}/samba/libwind-samba4.so


%check
%if %{with dotests}
%if %{with testsuite}
(LIBPATH=${RPM_BUILD_ROOT}%{_libdir64}/:${RPM_BUILD_ROOT}%{_libdir64}/samba:$LIBPATH  TDB_NO_FSYNC=1 gmake test || true)
%endif
%endif


%post
if [ "$1" -ge "1" ]; then
    /etc/rc.d/init.d/smbd condrestart >/dev/null 2>&1 || :
    /etc/rc.d/init.d/nmbd condrestart >/dev/null 2>&1 || :
fi
echo
echo "A guide to installing Samba on AIX can be found in /opt/freeware/doc/%{name}-%{version}/README.AixSambaInstallGuide"
echo
exit 0


%preun
if [ $1 = 0 ] ; then
    /etc/rc.d/init.d/smbd stop >/dev/null 2>&1 || :
    /etc/rc.d/init.d/nmbd stop >/dev/null 2>&1 || :
fi
exit 0


%pre winbind
# add the "wbpriv" group only if it does not yet exist
result=`/usr/sbin/lsgroup wbpriv | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [[ "${result}" != "wbpriv" ]] ; then
    /usr/bin/mkgroup -A id=%{wbpriv_gid} wbpriv 2> /dev/null || :
fi
exit 0


%post winbind
if [ "$1" -ge "1" ]; then
    /etc/rc.d/init.d/winbindd condrestart >/dev/null 2>&1 || :
fi
exit 0


%preun winbind
if [ "$1" = "0" ] ; then
    /etc/rc.d/init.d/winbindd stop >/dev/null 2>&1 || :
fi
exit 0


%postun winbind
if [ "$1" = "0" ] ; then
    # remove the "wbpriv" group
    /usr/sbin/rmgroup wbpriv || :
fi
exit 0


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/COPYING 32bit/README.md 32bit/WHATSNEW.txt
%doc 32bit/examples/autofs 32bit/examples/LDAP 32bit/examples/libsmbclient 32bit/examples/misc
%doc 32bit/examples/printer-accounting 32bit/examples/printing
%{_docdir}/%{name}-%{version}/README.AixSambaInstallGuide
%{_bindir}/mksmbpasswd.sh
%{_bindir}/smbstatus
%{_sbindir}/eventlogadm
%{_sbindir}/nmbd
%{_sbindir}/smbd
# %dir %{_prefix}/var/run/ctdb
%dir %{_prefix}/var/run/nmbd
%dir %{_prefix}/var/locks
%attr(755,root,system) /etc/rc.d/init.d/nmbd
%attr(755,root,system) /etc/rc.d/init.d/smbd
%attr(755,root,system) /etc/rc.d/init.d/winbindd
/etc/rc.d/rc2.d/Knmbd
/etc/rc.d/rc2.d/Snmbd
/etc/rc.d/rc2.d/Ksmbd
/etc/rc.d/rc2.d/Ssmbd
/etc/rc.d/rc3.d/Knmbd
/etc/rc.d/rc3.d/Snmbd
/etc/rc.d/rc3.d/Ksmbd
/etc/rc.d/rc3.d/Ssmbd
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
# %{_mandir}/man1/smbstatus.1*
# %{_mandir}/man7/%{name}.7*
# %{_mandir}/man8/eventlogadm.8*
# %{_mandir}/man8/nmbd.8*
# %{_mandir}/man8/smbd.8*
# %{_mandir}/man8/vfs_*.8*

%dir %{_libdir64}/samba/auth
%{_libdir64}/samba/auth/script.so
%{_libdir64}/samba/auth/unix.so

%dir %{_libdir64}/samba/vfs
%{_libdir64}/samba/vfs/acl_tdb.so
%{_libdir64}/samba/vfs/acl_xattr.so
%{_libdir64}/samba/vfs/aio_fork.so
%{_libdir64}/samba/vfs/aio_pthread.so
%{_libdir64}/samba/vfs/audit.so
# %{_libdir64}/samba/vfs/btrfs.so
%{_libdir64}/samba/vfs/cap.so
%{_libdir64}/samba/vfs/catia.so
%{_libdir64}/samba/vfs/commit.so
%{_libdir64}/samba/vfs/crossrename.so
%{_libdir64}/samba/vfs/default_quota.so
%if %{with_dc}
%{_libdir64}/samba/vfs/dfs_samba4.so
%endif
# %{_libdir64}/samba/vfs/dirsort.so
%{_libdir64}/samba/vfs/expand_msdfs.so
%{_libdir64}/samba/vfs/extd_audit.so
%{_libdir64}/samba/vfs/fake_perms.so
# %{_libdir64}/samba/vfs/fileid.so
%{_libdir64}/samba/vfs/fruit.so
%{_libdir64}/samba/vfs/full_audit.so
# %{_libdir64}/samba/vfs/gpfs.so
%{_libdir64}/samba/vfs/glusterfs_fuse.so
%{_libdir64}/samba/vfs/linux_xfs_sgid.so
%{_libdir64}/samba/vfs/media_harmony.so
%{_libdir64}/samba/vfs/netatalk.so
%{_libdir64}/samba/vfs/offline.so
%{_libdir64}/samba/vfs/preopen.so
%{_libdir64}/samba/vfs/readahead.so
%{_libdir64}/samba/vfs/readonly.so
%{_libdir64}/samba/vfs/recycle.so
%{_libdir64}/samba/vfs/shadow_copy.so
%{_libdir64}/samba/vfs/shadow_copy2.so
%{_libdir64}/samba/vfs/shell_snap.so
# %{_libdir64}/samba/vfs/snapper.so
%{_libdir64}/samba/vfs/streams_depot.so
%{_libdir64}/samba/vfs/streams_xattr.so
# %{_libdir64}/samba/vfs/syncops.so
%{_libdir64}/samba/vfs/time_audit.so
%{_libdir64}/samba/vfs/unityed_media.so
%{_libdir64}/samba/vfs/virusfilter.so
%{_libdir64}/samba/vfs/worm.so
%{_libdir64}/samba/vfs/xattr_tdb.so

%attr(1777,root,system) %dir /var/spool/%{name}
/etc/openldap/schema/%{name}.schema


# samba-all meta-package
%files all
%defattr(-,root,system)


# samba-client package
# Man pages not included because in Tex format
%files client
%defattr(-,root,system)
%doc 32bit/source3/client/README.smbspool
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/dumpmscat
%{_bindir}/findsmb
%{_bindir}/mvxattr
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/regdiff
%{_bindir}/regpatch
%{_bindir}/regshell
%{_bindir}/regtree
%{_bindir}/rpcclient
# In 4.11.7
# %{_bindir}/samba-regedit
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/smbtree

#### Not on Fedora (begin)
# TDB Trivial Data Base is the database engine used within Samba.
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbrestore
%{_bindir}/tdbtool

# Internal or independent LDB library/package is the database
# engine used within Samba.
# LDB is an an embedded LDAP-Like database library, but not completely
# LDAP compliant. It can store its database in regular files (using TDB),
# or talk to a standard LDAP server.
# LDB is a core part of Samba4.
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir64}/samba/libldb-cmdline-samba4.so
%{_libdir64}/samba/libldb-key-value-samba4.so
%{_libdir64}/samba/ldb/asq.so
# Not found
# %{_libdir64}/samba/ldb/paged_results.so
%{_libdir64}/samba/ldb/paged_searches.so
%{_libdir64}/samba/ldb/rdn_name.so
%{_libdir64}/samba/ldb/sample.so
%{_libdir64}/samba/ldb/server_sort.so
%{_libdir64}/samba/ldb/skel.so
%{_libdir64}/samba/ldb/tdb.so
%{_libdir64}/samba/ldb/ldb.so
#### Not on Fedora (end)

# Include  krb5-printing in the samba-client package
# %description krb5-printing
# If you need Kerberos for print jobs to a printer connection to cups via the
# SMB backend, then you need to install this utility.
# It will allow cups to access the Kerberos credentials cache of the user
# issuing the print job.

%dir %{_libexecdir}/samba
%attr(0700,root,system) %{_libexecdir}/samba/smbspool_krb5_wrapper

%files common
%defattr(-,root,system)

# samba-common-tools
# %{_bindir}/ctdb
# %{_bindir}/ctdb_diagnostics
# %{_bindir}/ctdb_run_cluster_tests
# %{_bindir}/ctdb_run_tests
# %{_bindir}/ltdbtool
# %{_bindir}/onnode
# %{_bindir}/ping_pong
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcquotas
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/tdb*
%{_bindir}/testparm
# %{_sbindir}/ctdbd
# %{_sbindir}/ctdbd_wrapper
%{_includedir}/samba-4.0/netapi.h
%dir /var/lib/%{name}
%attr(700,root,system) %dir /var/lib/%{name}/private
%dir /var/lib/%{name}/scripts
%dir /etc/%{name}
# /etc/%{name}/ctdb/*
# %dir %{_prefix}/var/lib/ctdb
# %dir %{_prefix}/var/run/ctdb
# %dir %{_libexecdir}/ctdb
# %{_libexecdir}/ctdb/*
%config(noreplace) /etc/%{name}/smb.conf
%config(noreplace) /etc/%{name}/lmhosts
%config(noreplace) /etc/sysconfig/%{name}
%attr(0700,root,system) %dir /var/log/%{name}
%attr(0700,root,system) %dir /var/log/%{name}/old


# Include samba-client-libs in the samba-common package
%{_libdir64}/libdcerpc-binding.so.*
%{_libdir64}/libndr.so.*
%{_libdir64}/libndr-krb5pac.so.*
%{_libdir64}/libndr-nbt.so.*
%{_libdir64}/libndr-standard.so.*
%{_libdir64}/libnetapi.so.*
%{_libdir64}/libsamba-credentials.so.*
%{_libdir64}/libsamba-errors.so.*
%{_libdir64}/libsamba-passdb.so.*
%{_libdir64}/libsamba-util.so.*
%{_libdir64}/libsamba-hostconfig.so.*
%{_libdir64}/libsamdb.so.*
%{_libdir64}/libsmbconf.so.*
%{_libdir64}/libsmbldap.so.*
%{_libdir64}/libtevent-util.so.*
%{_libdir64}/libdcerpc.so.*

%dir %{_libdir64}/samba
%{_libdir64}/samba/libCHARSET3-samba4.so
%{_libdir64}/samba/libaddns-samba4.so
%{_libdir64}/samba/libads-samba4.so
%{_libdir64}/samba/libasn1util-samba4.so
%{_libdir64}/samba/libauth-samba4.so
%{_libdir64}/samba/libauthkrb5-samba4.so
%{_libdir64}/samba/libcli-cldap-samba4.so
%{_libdir64}/samba/libcli-ldap-common-samba4.so
%{_libdir64}/samba/libcli-ldap-samba4.so
%{_libdir64}/samba/libcli-nbt-samba4.so
%{_libdir64}/samba/libcli-smb-common-samba4.so
%{_libdir64}/samba/libcli-spoolss-samba4.so
%{_libdir64}/samba/libcliauth-samba4.so
%{_libdir64}/samba/libclidns-samba4.so
%{_libdir64}/samba/libcmdline-contexts-samba4.so
%{_libdir64}/samba/libcmdline-credentials-samba4.so
%{_libdir64}/samba/libcmocka-samba4.so
%{_libdir64}/samba/libcommon-auth-samba4.so
# CTDB not built %{_libdir64}/samba/libctdb-event-client-samba4.so
%{_libdir64}/samba/libdbwrap-samba4.so
%{_libdir64}/samba/libdcerpc-samba-samba4.so
# Removed in 4.7.6 ?
# %{_libdir64}/samba/libdsdb-garbage-collect-tombstones-samba4.so
# %{_libdir64}/samba/libscavenge-dns-records-samba4.so
%{_libdir64}/samba/libevents-samba4.so
%{_libdir64}/samba/libflag-mapping-samba4.so
%{_libdir64}/samba/libgenrand-samba4.so
%{_libdir64}/samba/libgensec-samba4.so
%{_libdir64}/samba/libgpext-samba4.so
%{_libdir64}/samba/libgse-samba4.so
%{_libdir64}/samba/libhttp-samba4.so
%{_libdir64}/samba/libinterfaces-samba4.so
%{_libdir64}/samba/libiov-buf-samba4.so
%{_libdir64}/samba/libkrb5samba-samba4.so
%{_libdir64}/samba/libldbsamba-samba4.so
%{_libdir64}/samba/libldb-tdb-err-map-samba4.so
%{_libdir64}/samba/libldb-tdb-int-samba4.so
%{_libdir64}/samba/liblibcli-lsa3-samba4.so
%{_libdir64}/samba/liblibcli-netlogon3-samba4.so
%{_libdir64}/samba/liblibsmb-samba4.so
%{_libdir64}/samba/libmessages-dgm-samba4.so
%{_libdir64}/samba/libmessages-util-samba4.so
%{_libdir64}/samba/libmscat-samba4.so
%{_libdir64}/samba/libmsghdr-samba4.so
%{_libdir64}/samba/libmsrpc3-samba4.so
%{_libdir64}/samba/libndr-samba-samba4.so
%{_libdir64}/samba/libndr-samba4.so
%{_libdir64}/samba/libnet-keytab-samba4.so
%{_libdir64}/samba/libnetif-samba4.so
%{_libdir64}/samba/libnpa-tstream-samba4.so
%{_libdir64}/samba/libposix-eadb-samba4.so
%{_libdir64}/samba/libprinting-migrate-samba4.so
%{_libdir64}/samba/libreplace-samba4.so
%{_libdir64}/samba/libregistry-samba4.so
%{_libdir64}/samba/libsamba-cluster-support-samba4.so
%{_libdir64}/samba/libsamba-debug-samba4.so
%{_libdir64}/samba/libsamba-modules-samba4.so
%{_libdir64}/samba/libsamba-security-samba4.so
%{_libdir64}/samba/libsamba-sockets-samba4.so
%{_libdir64}/samba/libsamba3-util-samba4.so
%{_libdir64}/samba/libsamdb-common-samba4.so
%{_libdir64}/samba/libsecrets3-samba4.so
%{_libdir64}/samba/libserver-id-db-samba4.so
%{_libdir64}/samba/libserver-role-samba4.so
%{_libdir64}/samba/libsmb-transport-samba4.so
%{_libdir64}/samba/libsmbclient-raw-samba4.so
%{_libdir64}/samba/libsmbd-base-samba4.so
%{_libdir64}/samba/libsmbd-conn-samba4.so
%{_libdir64}/samba/libsmbd-shim-samba4.so
%{_libdir64}/samba/libsmbldaphelper-samba4.so
%{_libdir64}/samba/libsys-rw-samba4.so
%{_libdir64}/samba/libsocket-blocking-samba4.so
%{_libdir64}/samba/libtalloc-report-samba4.so
%{_libdir64}/samba/libtdb-wrap-samba4.so
%{_libdir64}/samba/libtime-basic-samba4.so
%{_libdir64}/samba/libtorture-samba4.so
%{_libdir64}/samba/libtrusts-util-samba4.so
%{_libdir64}/samba/libutil-cmdline-samba4.so
%{_libdir64}/samba/libutil-reg-samba4.so
%{_libdir64}/samba/libutil-setid-samba4.so
%{_libdir64}/samba/libutil-tdb-samba4.so

# Internal or independent TALLOC library/package
%{_libdir64}/samba/libtalloc.so*
%{_libdir64}/samba/libpytalloc-util.so*

# Internal or independent TEVENT library/package
%{_libdir64}/samba/libtevent.so*

# Internal or independent TDB library/package
%{_libdir64}/samba/libtdb.so*

# Internal or independent LDB library/package
%{_libdir64}/samba/libldb.so*
%{_libdir64}/samba/libpyldb-util.so*



# Include samba-common-libs in the samba-common package
%{_libdir64}/samba/libpopt-samba3-cmdline-samba4.so
%{_libdir64}/samba/libpopt-samba3-samba4.so

%dir %{_libdir64}/samba/ldb

%dir %{_libdir64}/samba/pdb
%{_libdir64}/samba/pdb/ldapsam.so
%{_libdir64}/samba/pdb/smbpasswd.so
%{_libdir64}/samba/pdb/tdbsam.so


%{_libdir64}/samba/libheimntlm-samba4.so*
%{_libdir64}/samba/libkdc-samba4.so*
# Samba AD Domain Controller
# Include samba-dc in the samba-common package
# %{_bindir}/samba-tool
# %{_sbindir}/samba
# %{_sbindir}/samba_kcc
# %{_sbindir}/samba_dnsupdate
%{_sbindir}/samba-gpupdate
# %{_sbindir}/samba_spnupdate
# %{_sbindir}/samba_upgradedns

# Not found - part of MIT Kerberos ?
# %{_libdir64}/krb5/plugins/kdb/samba.so

%if %{with_dc}
# This is only used by vfs_dfs_samba4
%{_libdir64}/samba/libdfs-server-ad-samba4.so
%endif

# %{_libdir64}/samba/auth/samba4.so
# Removed in 4.7.6 ?
# %{_libdir64}/samba/libpac-samba4.so
# %dir %{_libdir64}/samba/gensec
# %{_libdir64}/samba/gensec/krb5.so
# %{_libdir64}/samba/ldb/acl.so
# %{_libdir64}/samba/ldb/aclread.so
# %{_libdir64}/samba/ldb/anr.so
# %{_libdir64}/samba/ldb/audit_log.so
# %{_libdir64}/samba/ldb/descriptor.so
# %{_libdir64}/samba/ldb/dirsync.so
# %{_libdir64}/samba/ldb/dns_notify.so
# %{_libdir64}/samba/ldb/dsdb_notification.so
# %{_libdir64}/samba/ldb/encrypted_secrets.so
# %{_libdir64}/samba/ldb/extended_dn_in.so
# %{_libdir64}/samba/ldb/extended_dn_out.so
# %{_libdir64}/samba/ldb/extended_dn_store.so
# %{_libdir64}/samba/ldb/group_audit_log.so
%{_libdir64}/samba/ldb/ildap.so
# %{_libdir64}/samba/ldb/instancetype.so
# %{_libdir64}/samba/ldb/lazy_commit.so
%{_libdir64}/samba/ldb/ldbsamba_extensions.so
# %{_libdir64}/samba/ldb/linked_attributes.so
# %{_libdir64}/samba/ldb/local_password.so
# %{_libdir64}/samba/ldb/new_partition.so
# %{_libdir64}/samba/ldb/objectclass.so
# %{_libdir64}/samba/ldb/objectclass_attrs.so
# %{_libdir64}/samba/ldb/objectguid.so
# %{_libdir64}/samba/ldb/operational.so
# %{_libdir64}/samba/ldb/partition.so
# %{_libdir64}/samba/ldb/password_hash.so
# %{_libdir64}/samba/ldb/ranged_results.so
# %{_libdir64}/samba/ldb/repl_meta_data.so
# %{_libdir64}/samba/ldb/resolve_oids.so
# %{_libdir64}/samba/ldb/rootdse.so
# %{_libdir64}/samba/ldb/samba3sam.so
# %{_libdir64}/samba/ldb/samba3sid.so
# %{_libdir64}/samba/ldb/samba_dsdb.so
# %{_libdir64}/samba/ldb/samba_secrets.so
# %{_libdir64}/samba/ldb/samldb.so
# %{_libdir64}/samba/ldb/schema_data.so
# %{_libdir64}/samba/ldb/schema_load.so
# %{_libdir64}/samba/ldb/secrets_tdb_sync.so
# %{_libdir64}/samba/ldb/show_deleted.so
# %{_libdir64}/samba/ldb/simple_dn.so
# %{_libdir64}/samba/ldb/simple_ldap_map.so
# %{_libdir64}/samba/ldb/subtree_delete.so
# %{_libdir64}/samba/ldb/subtree_rename.so
# %{_libdir64}/samba/ldb/tombstone_reanimate.so
# %{_libdir64}/samba/ldb/unique_object_sids.so
# %{_libdir64}/samba/ldb/update_keytab.so
# %{_libdir64}/samba/ldb/vlv.so
# %{_libdir64}/samba/ldb/wins_ldb.so
# %{_libdir64}/samba/vfs/posix_eadb.so
%dir /var/lib/samba/sysvol
%{_datadir}/samba/setup


# Include samba-dc-libs in the samba-common package
# %{_libdir64}/samba/libdb-glue-samba4.so
# %{_libdir64}/samba/libprocess-model-samba4.so
# %{_libdir64}/samba/libservice-samba4.so
# %dir %{_libdir64}/samba/process_model
# %{_libdir64}/samba/process_model/prefork.so
# %{_libdir64}/samba/process_model/standard.so
# %dir %{_libdir64}/samba/service
# %{_libdir64}/samba/service/cldap.so
# %{_libdir64}/samba/service/dcerpc.so
# %{_libdir64}/samba/service/dns.so
# %{_libdir64}/samba/service/dns_update.so
# %{_libdir64}/samba/service/drepl.so
# %{_libdir64}/samba/service/kcc.so
# %{_libdir64}/samba/service/kdc.so
# %{_libdir64}/samba/service/ldap.so
# %{_libdir64}/samba/service/nbtd.so
# %{_libdir64}/samba/service/ntp_signd.so
# %{_libdir64}/samba/service/s3fs.so
# %{_libdir64}/samba/service/web.so
# %{_libdir64}/samba/service/winbindd.so
# %{_libdir64}/samba/service/wrepl.so
# %{_libdir64}/libdcerpc-server.so.*
# Not found in 4.7.6 ?
# %{_libdir64}/samba/vfs/dfs_samba4.so
# %{_libdir64}/samba/libdnsserver-common-samba4.so
%{_libdir64}/samba/libdsdb-module-samba4.so

# Following has been packaged in new RPM samba-dc-bind-dlz on Fedora
# %attr(770,root,named) %dir /var/lib/samba/bind-dns
# %dir %{_libdir64}/samba/bind9
# %{_libdir64}/samba/bind9/dlz_bind9.so
# %{_libdir64}/samba/bind9/dlz_bind9_9.so
# %{_libdir64}/samba/bind9/dlz_bind9_10.so
# %{_libdir64}/samba/bind9/dlz_bind9_11.so



### DEVEL
%files devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/charset.h
%{_includedir}/samba-4.0/core/*
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/domain_credentials.h
%{_includedir}/samba-4.0/gen_ndr/*
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/*
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/passdb.h
# %{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%{_includedir}/samba-4.0/samba/*
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/*
%{_includedir}/samba-4.0/util_ldb.h

%{_libdir64}/libdcerpc-binding.so
%{_libdir64}/libdcerpc-samr.so
%{_libdir64}/libdcerpc.so
%{_libdir64}/libndr-krb5pac.so
%{_libdir64}/libndr-nbt.so
%{_libdir64}/libndr-standard.so
%{_libdir64}/libndr.so
%{_libdir64}/libnetapi.so
%{_libdir64}/libsamba-credentials.so
%{_libdir64}/libsamba-errors.so
%{_libdir64}/libsamba-hostconfig.so
%{_libdir64}/libsamba-util.so
%{_libdir64}/libsamdb.so
%{_libdir64}/libsmbconf.so
%{_libdir64}/libtevent-util.so
%{_libdir64}/pkgconfig/dcerpc.pc
%{_libdir64}/pkgconfig/dcerpc_samr.pc
%{_libdir64}/pkgconfig/ndr.pc
%{_libdir64}/pkgconfig/ndr_krb5pac.pc
%{_libdir64}/pkgconfig/ndr_nbt.pc
%{_libdir64}/pkgconfig/ndr_standard.pc
%{_libdir64}/pkgconfig/netapi.pc
%{_libdir64}/pkgconfig/samba-credentials.pc
%{_libdir64}/pkgconfig/samba-hostconfig.pc
%{_libdir64}/pkgconfig/samba-util.pc
%{_libdir64}/pkgconfig/samdb.pc
%{_libdir64}/libsamba-passdb.so
%{_libdir64}/libsmbldap.so

# For samba-dc
# %{_includedir}/samba-4.0/dcerpc_server.h
# %{_libdir64}/pkgconfig/dcerpc_server.pc
# 
# %{_libdir64}/libsamba-policy.so
# %{_libdir64}/pkgconfig/samba-policy.pc


### Package samba-libs
%files libs
%defattr(-,root,system)
%{_libdir64}/libdcerpc-samr.so.*

# libraries needed by the public libraries
%{_libdir64}/samba/libMESSAGING-samba4.so
%{_libdir64}/samba/libLIBWBCLIENT-OLD-samba4.so
%{_libdir64}/samba/libMESSAGING-SEND-samba4.so
%{_libdir64}/samba/libauth4-samba4.so
%{_libdir64}/samba/libauth-unix-token-samba4.so
%{_libdir64}/samba/libcluster-samba4.so
%{_libdir64}/samba/libcommon-auth-samba4.so
# %{_libdir64}/samba/libctdb-event-client-samba4.so
%{_libdir64}/samba/libdcerpc-samba4.so
%{_libdir64}/samba/libnon-posix-acls-samba4.so
# %{_libdir64}/samba/libsamba-net-samba4.so
# %{_libdir64}/samba/libsamba-python-samba4.so
%{_libdir64}/samba/libshares-samba4.so
%{_libdir64}/samba/libsmbpasswdparser-samba4.so
%{_libdir64}/samba/libxattr-tdb-samba4.so

# For samba-dc
# %{_libdir64}/samba/libdb-glue-samba4.so
# %{_libdir64}/samba/libHDB-SAMBA4-samba4.so
%{_libdir64}/samba/libasn1-samba4.so*
%{_libdir64}/samba/libcom_err-samba4.so*
%{_libdir64}/samba/libgssapi-samba4.so*
%{_libdir64}/samba/libhcrypto-samba4.so*
%{_libdir64}/samba/libhdb-samba4.so*
%{_libdir64}/samba/libheimbase-samba4.so*
%{_libdir64}/samba/libhx509-samba4.so*
%{_libdir64}/samba/libkrb5-samba4.so*
%{_libdir64}/samba/libroken-samba4.so*
%{_libdir64}/samba/libwind-samba4.so*


# Test package samba-test
%files test
%defattr(-,root,system)
%{_bindir}/gentest
%{_bindir}/locktest
%{_bindir}/masktest
%{_bindir}/ndrdump
# This binary must be available!
# %{_bindir}/smbtorture

# %{_mandir}/man1/gentest.1*
# %{_mandir}/man1/locktest.1*
# %{_mandir}/man1/masktest.1*
# %{_mandir}/man1/ndrdump.1*
# %{_mandir}/man1/smbtorture.1*
# %{_mandir}/man1/vfstest.1*

%if %{with testsuite}
# files to ignore in testsuite mode
%{_libdir64}/samba/libnss-wrapper.so
%{_libdir64}/samba/libsocket-wrapper.so
%{_libdir64}/samba/libuid-wrapper.so
%endif

# Test package samba-test-libs
%files test-libs
%defattr(-,root,system)
%if %with_dc
%{_libdir64}/samba/libdlz-bind9-for-torture-samba4.so
%else
%{_libdir64}/samba/libdsdb-module-samba4.so
%endif



%files winbind
%defattr(-,root,system)
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo*
%{_sbindir}/winbindd*
%{_libdir64}/%{name}/idmap
%{_libdir64}/%{name}/nss_info
%{_libdir64}/samba/libnss-info-samba4.so
%{_libdir64}/samba/libidmap-samba4.so
# winbind_krb5_localauth is a plugin for MIT Kerberos for mapping user accounts
# %{_libdir64}/samba/krb5/winbind_krb5_localauth.so
%{_libdir64}/WINBIND.so
%ghost %dir /var/run/winbindd
%attr(750,root,wbpriv) %dir /var/lib/%{name}/winbindd_privileged
/etc/rc.d/init.d/winbindd
/etc/rc.d/rc2.d/Kwinbindd
/etc/rc.d/rc2.d/Swinbindd
/etc/rc.d/rc3.d/Kwinbindd
/etc/rc.d/rc3.d/Swinbindd


%files winbind-krb5-locator
%defattr(-,root,system)
%{_libdir64}/krb5/plugins/libkrb5/winbind_krb5_locator.so
%{_libdir64}/samba/krb5/winbind_krb5_locator.so


%files winbind-clients
%defattr(-,root,system)
%{_libdir64}/libwbclient.so*
%{_libdir64}/samba/libwinbind-client-samba4.so
%{_libdir64}/security/pam_winbind.so
# %{_libdir64}/libnss-winbind.so*
# %{_libdir64}/libnss-wrapper-winbind.so*
%{_libdir64}/security/WINBIND


%files winbind-devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/wbclient.h
%{_libdir64}/pkgconfig/wbclient.pc


# %files doc
# %defattr(-,root,system)


%files -n libsmbclient
%defattr(-,root,system)
%{_libdir64}/libsmbclient.so*
#%{_libdir64}/libsmbsharemodes.so*


%files -n libsmbclient-devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir64}/pkgconfig/smbclient.pc


# Samba Python libraries
%files python
%defattr(-,root,system,-)
%{python2_sitearch64}/*


# Perl IDL compiler
%files pidl
%defattr(-,root,system)
%attr(755,root,system) %{_bindir}/pidl
%dir %{perl_lib}/Parse
%{perl_lib}/Parse/Pidl.pm
%dir %{perl_lib}/Parse/Pidl
%{perl_lib}/Parse/Pidl/CUtil.pm
%{perl_lib}/Parse/Pidl/Samba4.pm
%{perl_lib}/Parse/Pidl/Expr.pm
%{perl_lib}/Parse/Pidl/ODL.pm
%{perl_lib}/Parse/Pidl/Typelist.pm
%{perl_lib}/Parse/Pidl/IDL.pm
%{perl_lib}/Parse/Pidl/Compat.pm
%dir %{perl_lib}/Parse/Pidl/Wireshark
%{perl_lib}/Parse/Pidl/Wireshark/Conformance.pm
%{perl_lib}/Parse/Pidl/Wireshark/NDR.pm
%{perl_lib}/Parse/Pidl/Dump.pm
%dir %{perl_lib}/Parse/Pidl/Samba3
%{perl_lib}/Parse/Pidl/Samba3/ServerNDR.pm
%{perl_lib}/Parse/Pidl/Samba3/ClientNDR.pm
%dir %{perl_lib}/Parse/Pidl/Samba4
%{perl_lib}/Parse/Pidl/Samba4/Header.pm
%dir %{perl_lib}/Parse/Pidl/Samba4/COM
%{perl_lib}/Parse/Pidl/Samba4/COM/Header.pm
%{perl_lib}/Parse/Pidl/Samba4/COM/Proxy.pm
%{perl_lib}/Parse/Pidl/Samba4/COM/Stub.pm
%{perl_lib}/Parse/Pidl/Samba4/Python.pm
%{perl_lib}/Parse/Pidl/Samba4/Template.pm
%dir %{perl_lib}/Parse/Pidl/Samba4/NDR
%{perl_lib}/Parse/Pidl/Samba4/NDR/Server.pm
%{perl_lib}/Parse/Pidl/Samba4/NDR/Client.pm
%{perl_lib}/Parse/Pidl/Samba4/NDR/Parser.pm
%{perl_lib}/Parse/Pidl/Samba4/TDR.pm
%{perl_lib}/Parse/Pidl/NDR.pm
%{perl_lib}/Parse/Pidl/Util.pm


%changelog
* Thu Oct 22 2020 Clement Chigot <clement.chigot@atos.net> - 4.10.14-2
- Rebuild with new libgcrypt without .so files

* Wed Apr 15 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.10.14-1
- Update to version 4.10.14
- Partial merge of Bullfreeware, Toolbox and Fedora specfile
- Compile on 64 bit only (was 32 only in previous version)
- Compile with GCC
- Lots of libraries, especially ldb, are no more available
- ctdb (clustering) no more provided by default

* Wed Jan 30 2019 Michael Wilson <michael.a.wilson@atos.net> - 4.9.4-1
- Update to version 4.9.4
- Security fixes for CVE-2018-14629 CVE-2018-16841 CVE-2018-16851
-                    CVE-2018-16852 CVE-2018-16853 CVE-2018-16857
- Fedora 4.9.4-0.fc30.1 rebuilt for libcrypt.so.2

* Fri Sep 21 2018 Michael Wilson <michael.a.wilson@atos.net> - 4.9.0-1
- First port to version 4.9.0
-   File smbusers (/etc/samba/smbusers) is no longer in the build
- Include Fedora patch for linker flags
- Include patches for structure timespec not declared in stat.h before AIX 7.1,
-   structure shutdown_state redefines ip_len declared in AIX netinet/ip.h
-   and issue in posix_fallocate()
- Remove integrated TdbAIX and vfs_aixacl2 patches
- Issue in make install Generating PKGCONFIG files already gernerated
-   may be due to embedded Heimdal build

* Wed Sep 12 2018 Michael Wilson <michael.a.wilson@atos.net> - 4.7.10-1
- Update to version 4.7.10
- Includes following CVE security fixes in Samba 4.7.9
- CVE-2018-1139
- CVE-2018-1140
- CVE-2018-10858
- CVE-2018-10918
- CVE-2018-10919

* Fri Mar 16 2018 Michael Wilson <michael.a.wilson@atos.net> - 4.7.6-1
- First port to version 4.7.6
- At same CVE level as version 4.6.14
- Updated Samba Time.patch and openO_NOFOLLOW.patch
- New Samba tfork.patch for missing #if defined(HAVE_*SYSCALL_H)
- New Samba vfs_aixacl2.patch for residual unspecified name symbol

* Thu Mar 15 2018 Michael Wilson <michael.a.wilson@atos.net> - 4.6.14-1
- Update to version 4.6.14
- includes CVE-2018-1057    and    CVE-2018-1050

* Tue Dec 05 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.6.11-2
- Include patch fix samba-4.6.11-PthreadCond.patch instead of assert() WA

* Thu Nov 23 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.6.11-1
- Update to version 4.6.11
- includes CVE-2017-12150 CVE-2017-12151 CVE-2017-12163  from 4.6.8
- and      CVE-2017-14746 CVE-2017-15275                 from 4.6.11
- Export winbindd binary symbols for idmap/ad.so winbindd_ads.c/wb_dsgetdcname.c
- EINVAL returned from pthread_cond_destroy() after fork() on AIX

* Thu Sep 14 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.6.7-1
- Update to version 4.6.7

* Thu Sep 07 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.6.4-2
- Add authentication module libnss_winbind.so/WINBIND to samba-winbind-clients
-     source file is nsswitch/winbind_nss_aix.c
-     Patch14 wscript_build must specify an entrypoint for the WINBIND module
- Correction to -blibpath:= (remove "=")

* Tue May 30 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.6.4-1
- Update to version 4.6.4

* Mon May 29 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.5.10-1
- Update to version 4.5.10
- Patch13 for open(O_NOFOLLOW) not supported on 6.1,
-         and run time test    0x01000000 on 7.2
-         else                 0x02000000 on 7.1,

* Mon Jan 16 2017 Michael Wilson <michael.a.wilson@atos.net> - 4.5.3-1
- Update to version 4.5.3

* Thu Dec 08 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.1-1
- Update to version 4.5.1

* Wed Oct 26 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.0-3
- Add AIX installation guide in %doc and echo a message post install

* Mon Oct 10 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.0-2
- Include LDFLAGS=-Wl,-blibpath
- Add packages samba-test and samba-test-libs for gmake test
- Add missing module libpyldb-util.so (required during selftest)

* Wed Sep 07 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.0-1
- Update to version 4.5.0
- Patch9 modified for new resolv_wrapper.c source
- Patch10 added for dirfd() in closefrom.c source
- Patch11 still required to work around XLC internal error issue
- Patch12 added for krb5pac.c to work around XLC preprocessor issue

* Wed Sep 07 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.4.5-1
- Update to version 4.4.5

* Mon Aug 29 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.8-3
- Create a global meta-package to include all Samba component RPMs
- Add the build trace to list of sources in SRPM

* Mon Apr 18 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.8-2
- Remove dependencies on gtk2/gtk2-devel  2.8.3-9

* Wed Apr 13 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.8-1
- Update to version 4.3.8 for CVE security and regression fixes
- Patch11 still required to work around latest XLC issue
- Remove Patch0, it concerned 4.3.6

* Fri Apr 08 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.6-3
- Not downloaded as of 13th April
- Patch0 in 589 source files for CVE security fixes
- Patch11 in 8 source files to work around latest XLC issue
- Remove Patch10, fix in latest XLC

* Tue Mar 29 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.6-2
- Patch10 in unix_msg.c for sigsegv core dump in smbcontrol

* Wed Mar 16 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.6-1
- Update to version 4.3.6

* Wed Jan 20 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.4-1
- Update to version 4.3.4

* Wed Aug 12 2015 Hamza Sellami <hamza.sellami@atos.net> - 4.2.0-1
- Update to version 4.2.0

* Tue Mar 31 2015 Gerard Visiedo <gerard.visiedo@bull.net> - 3.6.24-2
- Initial port on aix6.1

* Mon Jun 23 2014 Michael Perzl <michael@perzl.org> - 3.6.24-1
- updated to version 3.6.24

* Wed Mar 12 2014 Michael Perzl <michael@perzl.org> - 3.6.23-1
- updated to version 3.6.23

* Tue Dec 10 2013 Michael Perzl <michael@perzl.org> - 3.6.22-1
- updated to version 3.6.22

* Sat Nov 30 2013 Michael Perzl <michael@perzl.org> - 3.6.21-1
- updated to version 3.6.21

* Mon Nov 11 2013 Michael Perzl <michael@perzl.org> - 3.6.20-1
- updated to version 3.6.20

* Thu Sep 26 2013 Michael Perzl <michael@perzl.org> - 3.6.19-1
- updated to version 3.6.19

* Wed Aug 28 2013 Michael Perzl <michael@perzl.org> - 3.6.18-2
- added the patch to fix the bug 8984

* Wed Aug 14 2013 Michael Perzl <michael@perzl.org> - 3.6.18-1
- updated to version 3.6.18

* Tue Aug 06 2013 Michael Perzl <michael@perzl.org> - 3.6.17-1
- updated to version 3.6.17

* Thu Jul 04 2013 Michael Perzl <michael@perzl.org> - 3.6.16-2
- added the missing shared libraries introduced with version 3.6.16
- reworked some of the RPM %pre(un) and %post(un) scripts

* Thu Jun 20 2013 Michael Perzl <michael@perzl.org> - 3.6.16-1
- updated to version 3.6.16

* Thu May 09 2013 Michael Perzl <michael@perzl.org> - 3.6.15-1
- updated to version 3.6.15

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 3.6.14-1
- updated to version 3.6.14

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 3.6.13-2
- added missing dependency on samba-winbind-clients for samba-common
  (libwbclient.so)

* Mon Mar 18 2013 Michael Perzl <michael@perzl.org> - 3.6.13-1
- updated to version 3.6.13

* Thu Jan 31 2013 Michael Perzl <michael@perzl.org> - 3.6.12-1
- updated to version 3.6.12

* Tue Jan 22 2013 Michael Perzl <michael@perzl.org> - 3.6.11-1
- updated to version 3.6.11

* Tue Dec 11 2012 Michael Perzl <michael@perzl.org> - 3.6.10-1
- updated to version 3.6.10

* Tue Oct 30 2012 Michael Perzl <michael@perzl.org> - 3.6.9-1
- updated to version 3.6.9

* Mon Oct 15 2012 Michael Perzl <michael@perzl.org> - 3.6.8-1
- updated to version 3.6.8

* Tue Aug 07 2012 Michael Perzl <michael@perzl.org> - 3.6.7-1
- updated to version 3.6.7

* Mon Jun 25 2012 Michael Perzl <michael@perzl.org> - 3.6.6-1
- updated to version 3.6.6

* Mon Apr 30 2012 Michael Perzl <michael@perzl.org> - 3.6.5-1
- updated to version 3.6.5

* Thu Apr 19 2012 Michael Perzl <michael@perzl.org> - 3.6.4-1
- first version for AIX V5.1 and higher
