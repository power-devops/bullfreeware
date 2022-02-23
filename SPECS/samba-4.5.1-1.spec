# samba-4.3.8-3 adds a virtual samba-all RPM to include all Samba packages
# Samba is currently built using the XLC compiler
# GCC may be used to build a future (4.5.0) version
#
# samba-4.4.5 contains new security fixes and a number of code changes
#
# Using the recent SPEC file for samba-4.3.8-2 for this new version
#
# Currently, there are no options in this SPEC file to build/not build 
# Samba components for testing and cluster data base (ctdb vs tbd)
#
# The testsuite is disabled by default and is specified by configure
# option  --enable-selftest
# or
# rpmbuild --rebuild --with testsuite
%bcond_with testsuite
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

%define samba_version 4.5.1
%define talloc_version 2.1.8
%define tdb_version 1.3.10
%define tevent_version 0.9.29
%define ldb_version 1.1.27

%define wbpriv_gid 88

%define with_libuuid 0
%define with_GPFS    0

## %define samba_source source3

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# perl_lib_install_dir is hard coded in file buildtools/wafsamba/samba_perl.py
%define perl_lib %{_datadir}/perl5


Summary: Server and Client software to interoperate with Windows machines
Name: samba
Version: 4.5.1
Release: 1
License: GPLv3+ and LGPLv3+
Group: System Environment/Daemons
URL: http://www.samba.org/

Source0: http://www.samba.org/samba/%{name}-%{version}.tar.gz
Source1: http://www.samba.org/samba/%{name}-%{version}.tar.asc

Source2: %{name}.log
# Source3: swat.desktop
Source4: %{name}.sysconfig
Source5: smb.conf.default
Source6: smbprint
Source7: smbd.aix.init
Source8: nmbd.aix.init
Source9: winbindd.aix.init

Source10: %{name}-%{version}-%{release}.build.log
Source11: README.AixSambaInstallGuide


Patch1: %{name}-4.2.0-aix.patch
Patch2: 0002-Bug-8984-AIX-6.1-nmbd-Failed-to-open-nmb-bcast-socket.patch
Patch3: samba-4.2.0-Time.patch
Patch4: samba-4.2.0-TdbAIX.patch

Patch6: samba-4.4.5-Struc_bad_initialization.patch
Patch7: samba-4.2.0-BadInitializationTypes.patch
Patch8: samba-4.2.0-BadInitializationTypesA.patch
Patch9: samba-4.5.0-resolv_wrapper.patch
Patch10: samba-4.5.0-closefrom_dirfd.patch

# Following patch is a temporary(?) work around for XLC internal error
Patch11: samba-4.3.6-xlcWA.patch
# Following patch is a temporary(?) work around for XLC preprocessor error
Patch12: samba-4.5.0-xlcIfdefWA.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# The docs are no longer built
Obsoletes: samba-doc
# Not supported yet
Obsoletes: samba-domainjoin-gui
# SWAT been deprecated and removed from samba
Obsoletes: samba-swat


BuildRequires: make, patch

BuildRequires: cups-devel >= 1.4.4-2
# BuildRequires: gtk2-devel >= 2.8.3-9
BuildRequires: krb5-devel >= 1.8.3-1
# May be BuildRequires: krb5-devel >= 1.14
BuildRequires: libiconv >= 1.14-1
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: popt >= 1.7-2
BuildRequires: readline-devel >= 5.2-3
%if %{with_libuuid}
BuildRequires: uuid-devel >= 1.6.2-1
%endif
BuildRequires: gnutls-devel

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}

Requires: bash
Requires: cups >= 1.4.4-2
# Requires: gtk2 >= 2.8.3-9
Requires: logrotate >= 3.7.9-2
Requires: openssl >= 1.0.1

%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif


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
Group: Applications/System
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
Group: Applications/System
Requires: bash
Requires: %{name}-common = %{version}-%{release}
# Include samba-client-libs
# Requires: %{name}-client-libs = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description client
The samba-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.


# Common package grouping common files with common-libs and common-tools
%package common
Summary: Files used by both Samba servers and clients
Group: Applications/System
# Requires: %{name}-libs = %{version}-%{release}
# Requires: %{name}-winbind-clients = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}
# Requires: krb5-libs >= 1.9.4-2
# May be Requires: krb5-libs >= 1.14 (not yet on Bullfreeware)
Requires: libiconv >= 1.14-2
Requires: openldap >= 2.4.23
Requires: popt >= 1.7-2
Requires: readline >= 5.2-3
%if %{with_libuuid}
Requires: uuid >= 1.6.2-1
%endif
Requires: zlib >= 1.2.3-3
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description common
Samba-common provides files and tools necessary for both the server and client
packages of Samba and internal libraries needed by the SMB/CIFS clients.


# samba-devel package needed to develop programs
%package devel
Summary: Developer tools for Samba libraries
Group: Development/Libraries
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description devel
The samba-devel package contains the header files for the libraries
needed to develop programs that link against the SMB, RPC and other
libraries in the Samba suite.


# samba-libs package
%package libs
Summary: Samba libraries
Group: Applications/System
Requires: krb5-libs >= 1.9.4-2
# May be Requires: krb5-libs >= 1.14 (not yet on Bullfreeware)
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description libs
The samba-libs package contains the libraries needed by programs that
link against the SMB, RPC and other protocols provided by the Samba suite.



%package winbind
Summary: Samba winbind
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
# Requires: %{name}-winbind-modules = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description winbind
The samba-winbind package provides the winbind daemon, the winbind NSS library
and some client tools.
Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.


%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
Group: Applications/System
Requires: %{name}-winbind = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use


%package winbind-clients
Summary: Samba winbind clients
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name}-winbind = %{version}-%{release}
# Requires: libwbclient = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description winbind-clients
The samba-winbind-clients package provides the NSS library and a PAM
module necessary to communicate to the Winbind Daemon


%package winbind-devel
Summary: Developer tools for the winbind library
Group: Development
Requires: %{name}-winbind = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description winbind-devel
The samba-winbind-devel package provides developer tools for the wbclient library.


# SWAT been deprecated and removed from samba
# %package swat
# Summary: The Samba SMB server Web configuration program
# Group: Applications/System
# Requires: %{name} = %{version}-%{release}

# %description swat
# The samba-swat package includes the new SWAT (Samba Web Administration
# Tool), for remotely managing Samba's smb.conf file using your favorite
# Web browser.


# The docs are no longer built
# %package doc
# Summary: Documentation for the Samba suite
# Group: Documentation
# Requires: %{name}-common = %{version}-%{release}

# %description doc
# The samba-doc package includes all the non-manpage documentation for the
# Samba suite.


# Not supported yet
# %package domainjoin-gui
# Summary: Domainjoin GUI
# Group: Applications/System
# Requires: %{name}-common = %{version}-%{release}
# Requires: gtk2 >= 2.8.3-9

# %description domainjoin-gui
# The samba-domainjoin-gui package includes a domainjoin gtk application.


%package -n libsmbclient
Summary: The SMB client library
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description -n libsmbclient
The libsmbclient contains the SMB client library from the Samba suite.

%package -n libsmbclient-devel
Summary: Developer tools for the SMB client library
Group: Development
Requires: libsmbclient = %{version}-%{release}
%ifos aix5.1
Requires: AIX-rpm >= 5.1.0.0
Requires: AIX-rpm < 5.2.0.0
%endif
%ifos aix5.2
Requires: AIX-rpm >= 5.2.0.0
Requires: AIX-rpm < 5.3.0.0
%endif
%ifos aix5.3
Requires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm < 5.4.0.0
%endif
%ifos aix6.1
Requires: AIX-rpm >= 6.1.0.0
#Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
#Requires: AIX-rpm < 7.2.0.0
%endif
%ifos aix7.2
Requires: AIX-rpm >= 7.2.0.0
%endif

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed to
develop programs that link against the SMB client library in the Samba suite.


%package python
Summary: Samba Python libraries
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
# Requires: python-tevent
# Requires: python-tdb
# Requires: pyldb
# Requires: pytalloc

%description python
The samba-python package contains the Python libraries needed by programs
that use SMB, RPC and other Samba provided protocols in Python programs.


%package pidl
Summary: Perl IDL compiler
Group: Development/Tools
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
Group: Applications/System
Requires: %{name} = %{samba_depver}
Requires: %{name}-common = %{samba_depver}
Requires: %{name}-winbind = %{samba_depver}

# Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}
Requires: %{name}-test-libs = %{samba_depver}
# %if %with_dc
# Requires: %{name}-dc-libs = %{samba_depver}
# %endif
Requires: %{name}-libs = %{samba_depver}
# %if %with_libsmbclient
Requires: libsmbclient = %{samba_depver}
# %endif
# %if %with_libwbclient
Requires: libwbclient = %{samba_depver}
# %endif

Provides: samba4-test = %{samba_depver}
Obsoletes: samba4-test < %{samba_depver}

%description test
The samba-test provides testing tools for both the server and client
packages of Samba.

### TEST-LIBS
%package test-libs
Summary: Libraries need by the testing tools for Samba servers and clients
Group: Applications/System
# Requires: %{name}-client-libs = %{samba_depver}
Requires: %{name}-libs = %{samba_depver}

Provides: %{name}-test-devel = %{samba_depver}
Obsoletes: %{name}-test-devel < %{samba_depver}

%description test-libs
The samba-test-libs provides libraries required by the testing tools.



%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

%patch1
%patch2 -p1
%patch3 -p1 -b .Time
%patch4 -p1

%patch6 -p1
%patch7 -p1
%patch8 -p1 
%patch9 -p1 
%patch10 -p1 

# Following patch is a temporary(?) work around for XLC internal error
%patch11 -p1
# Following patch is a temporary(?) work around for XLC preprocessor error
%patch12 -p1



%build

%global _samba4_idmap_modules idmap_ad,idmap_rid,idmap_adex,idmap_hash,idmap_tdb2

%global _samba4_pdb_modules pdb_tdbsam,pdb_ldap,pdb_ads,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4

%global _samba4_auth_modules auth_unix,auth_wbc,auth_server,auth_netlogond,auth_script,auth_samba4

%global _samba4_modules %{_samba4_idmap_modules},%{_samba4_pdb_modules},%{_samba4_auth_modules}


# function to build samba
# include --enable-selftest if make test is to be used
build_samba()
{
##  cd %{samba_source}

  ./configure -v \
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
      --with-modulesdir=$1/%{name} \
      --with-pammodulesdir=$1/security \
      --with-cachedir=/var/cache \
      --with-acl-support \
      --with-ads \
      --with-automount \
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
%if %{with_GPFS}
      --with-shared-modules=%{_samba4_modules},vfs_gpfs \
%else
      --with-shared-modules=%{_samba4_modules} \
      --disable-glusterfs \
%endif
%if %{with testsuite}
      --enable-selftest \
%endif


  gmake
  make debug2html smbfilter

}

export CFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet -D__PRETTY_FUNCTION__=__func__"
export LDFLAGS="-Wl,-blibpath:=/opt/freeware/lib:/opt/freeware/lib/samba:/usr/vac/lib:/usr/lib:/lib"
export CXXFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet"
#export CC="/usr/bin/gcc"
#export CXX="/usr/bin/g++"
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

build_samba %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

echo ---------- ${RPM_BUILD_ROOT} ------------------------------------------------------------------------------
gmake install DESTDIR=${RPM_BUILD_ROOT}
cd ..
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
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

cp %{SOURCE5} ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf
chmod 0644 ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf

cp samba-4.5.0/source3/script/mksmbpasswd.sh ${RPM_BUILD_ROOT}%{_bindir}/
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/mksmbpasswd.sh

cp samba-4.5.0/packaging/RHEL/setup/smbusers ${RPM_BUILD_ROOT}/etc//%{name}/smbusers
chmod 0644 ${RPM_BUILD_ROOT}/etc//%{name}/smbusers

cp samba-4.5.0/packaging/printing/smbprint ${RPM_BUILD_ROOT}%{_bindir}/
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/smbprint

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

echo 127.0.0.1 localhost > ${RPM_BUILD_ROOT}/etc/%{name}/lmhosts

mkdir -p ${RPM_BUILD_ROOT}/etc/openldap/schema
cp samba-4.5.0/examples/LDAP/%{name}.schema ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema
chmod 0644 ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema

# winbind krb5 locator
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5
cp samba-4.5.0/bin/shared/winbind_krb5_locator.so ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

# pkgconfig files
#list="smbclient smbsharemodes wbclient"
#for i in ${list} ; do
#    cp %{samba_source}/pkgconfig/${i}.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/
#done
cp samba-4.5.0/bin/default/source3/libsmb/smbclient.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/ 
cp samba-4.5.0/bin/default/source3/libnet/netapi.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/ 
cp samba-4.5.0/bin/default/nsswitch/libwbclient/wbclient.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/

mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
cp %{SOURCE4} ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}
chmod 0644 ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}

# cp -r samba-4.5.0/source3/lib/netapi/examples/netdomjoin-gui ${RPM_BUILD_ROOT}%{_sbindir}/
# chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/netdomjoin-gui

# mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}
# cp samba-4.5.0/source3/lib/netapi/examples/netdomjoin-gui/%{name}.ico ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/%{name}.ico
# chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/%{name}.ico

# cp samba-4.5.0/source3/lib/netapi/examples/netdomjoin-gui/logo.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo.png
# chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo.png

# cp samba-4.5.0/source3/lib/netapi/examples/netdomjoin-gui/logo-small.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo-small.png
# chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo-small.png

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
ln -sf '../init.d/smbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Ssmbd
ln -sf '../init.d/smbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Ksmbd
ln -sf '../init.d/smbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Ssmbd
ln -sf '../init.d/smbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Ksmbd
ln -sf '../init.d/nmbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Snmbd
ln -sf '../init.d/nmbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Knmbd
ln -sf '../init.d/nmbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Snmbd
ln -sf '../init.d/nmbd'     ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Knmbd
ln -sf '../init.d/winbindd' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Swinbindd
ln -sf '../init.d/winbindd' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Kwinbindd
ln -sf '../init.d/winbindd' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Swinbindd
ln -sf '../init.d/winbindd' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Kwinbindd

# create symlinks to library modules
# samba_common
ln -sf  libtalloc.so.%{talloc_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libtalloc.so
ln -sf  libpytalloc-util.so.%{talloc_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libpytalloc-util.so
ln -sf  libtevent.so.%{tevent_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libtevent.so
ln -sf  libtdb.so.%{tdb_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libtdb.so
ln -sf  libldb.so.%{ldb_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libldb.so
ln -sf  libpyldb-util.so.%{ldb_version}     ${RPM_BUILD_ROOT}%{_libdir}/samba/libpyldb-util.so
ln -sf  libheimntlm-samba4.so.1.0.1     ${RPM_BUILD_ROOT}%{_libdir}/samba/libheimntlm-samba4.so
ln -sf  libkdc-samba4.so.2.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libkdc-samba4.so

# samba_libs
ln -sf  libasn1-samba4.so.8.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libasn1-samba4.so
ln -sf  libcom_err-samba4.so.0.25     ${RPM_BUILD_ROOT}%{_libdir}/samba/libcom_err-samba4.so
ln -sf  libgssapi-samba4.so.2.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libgssapi-samba4.so
ln -sf  libhcrypto-samba4.so.5.0.1     ${RPM_BUILD_ROOT}%{_libdir}/samba/libhcrypto-samba4.so
ln -sf  libhdb-samba4.so.11.0.2     ${RPM_BUILD_ROOT}%{_libdir}/samba/libhdb-samba4.so
ln -sf  libheimbase-samba4.so.1.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libheimbase-samba4.so
ln -sf  libhx509-samba4.so.5.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libhx509-samba4.so
ln -sf  libkrb5-samba4.so.26.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libkrb5-samba4.so
ln -sf  libroken-samba4.so.19.0.1     ${RPM_BUILD_ROOT}%{_libdir}/samba/libroken-samba4.so
ln -sf  libwind-samba4.so.0.0.0     ${RPM_BUILD_ROOT}%{_libdir}/samba/libwind-samba4.so


%if %{with testsuite}
%check
LIBPATH=${RPM_BUILD_ROOT}%{_libdir}/:${RPM_BUILD_ROOT}%{_libdir}/samba:$LIBPATH  TDB_NO_FSYNC=1 gmake test
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
%doc COPYING README WHATSNEW.txt Roadmap
%doc examples/autofs examples/LDAP examples/libsmbclient examples/misc
%doc examples/printer-accounting examples/printing
%{_docdir}/%{name}-%{version}/README.AixSambaInstallGuide
%{_bindir}/eventlogadm
%{_bindir}/mksmbpasswd.sh
%{_bindir}/smbstatus
%{_sbindir}/nmbd
%{_sbindir}/smbd
%config(noreplace) /etc/%{name}/smbusers
%attr(755,root,system) /etc/rc.d/init.d/nmbd
%attr(755,root,system) /etc/rc.d/init.d/smbd
%attr(755,root,system) /etc/rc.d/rc2.d/Knmbd
%attr(755,root,system) /etc/rc.d/rc2.d/Snmbd
%attr(755,root,system) /etc/rc.d/rc2.d/Ksmbd
%attr(755,root,system) /etc/rc.d/rc2.d/Ssmbd
%attr(755,root,system) /etc/rc.d/rc3.d/Knmbd
%attr(755,root,system) /etc/rc.d/rc3.d/Snmbd
%attr(755,root,system) /etc/rc.d/rc3.d/Ksmbd
%attr(755,root,system) /etc/rc.d/rc3.d/Ssmbd
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
# %{_mandir}/man1/smbstatus.1*
# %{_mandir}/man7/%{name}.7*
# %{_mandir}/man8/eventlogadm.8*
# %{_mandir}/man8/nmbd.8*
# %{_mandir}/man8/smbd.8*
# %{_mandir}/man8/vfs_*.8*
%{_libdir}/%{name}/vfs
%{_libdir}/%{name}/auth
#%{_libdir}/%{name}/charset
%attr(1777,root,system) %dir /var/spool/%{name}
/etc/openldap/schema/%{name}.schema


# samba-all meta-package
%files all
%defattr(-,root,system)


# %files swat
# %defattr(-,root,system)
# ###%config(noreplace) /etc/xinetd.d/swat
# %{_datadir}/swat


# samba-client package
# Man pages not included because in Tex format
%files client
%defattr(-,root,system)
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/findsmb
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/rpcclient
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/smbtree

# TDB Trivial Data Base is the database engine used within Samba.
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbrestore
%{_bindir}/tdbtool

# Internal or independent LDB library/package (1.1.21) is the database
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
%{_libdir}/samba/libldb-cmdline-samba4.so
%{_libdir}/samba/ldb/asq.so
%{_libdir}/samba/ldb/paged_results.so
%{_libdir}/samba/ldb/paged_searches.so
%{_libdir}/samba/ldb/rdn_name.so
%{_libdir}/samba/ldb/sample.so
%{_libdir}/samba/ldb/server_sort.so
%{_libdir}/samba/ldb/skel.so
%{_libdir}/samba/ldb/tdb.so



# Include  krb5-printing in the samba-client package
# %description krb5-printing
# If you need Kerberos for print jobs to a printer connection to cups via the
# SMB backend, then you need to install this utility.
# It will allow cups to access the Kerberos credentials cache of the user
# issuing the print job.

%dir %{_libexecdir}/samba
%attr(0700,root,root) %{_libexecdir}/samba/smbspool_krb5_wrapper

%files common
%defattr(-,root,system)

# samba-common-tools
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcquotas
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/tdb*
%{_bindir}/testparm
#%{_libdir}/libnetapi.so*
#%{_libdir}/libtalloc.so*
#%{_libdir}/libtdb.so*
#%{_libdir}/libtevent.so*
%{_includedir}/samba-4.0/netapi.h
#%{_includedir}/tevent.h
#%{_includedir}/tevent_internal.h
#%{_includedir}/talloc.h
#%{_includedir}/tdb.h
#/opt/freeware/src/packages/BUILD/samba-4.3.4/bin/default/source3/libnet/netapi.pc
%dir /var/lib/%{name}
%attr(700,root,system) %dir /var/lib/%{name}/private
%dir /var/lib/%{name}/scripts
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/smb.conf
%config(noreplace) /etc/%{name}/lmhosts
%config(noreplace) /etc/sysconfig/%{name}
%attr(0700,root,system) %dir /var/log/%{name}
%attr(0700,root,system) %dir /var/log/%{name}/old


# Include samba-client-libs in the samba-common package
%{_libdir}/libdcerpc-binding.so.*
%{_libdir}/libndr.so.*
%{_libdir}/libndr-krb5pac.so.*
%{_libdir}/libndr-nbt.so.*
%{_libdir}/libndr-standard.so.*
%{_libdir}/libnetapi.so.*
%{_libdir}/libsamba-credentials.so.*
%{_libdir}/libsamba-errors.so.*
%{_libdir}/libsamba-passdb.so.*
%{_libdir}/libsamba-util.so.*
%{_libdir}/libsamba-hostconfig.so.*
%{_libdir}/libsamdb.so.*
%{_libdir}/libsmbconf.so.*
%{_libdir}/libsmbldap.so.*
%{_libdir}/libtevent-util.so.*
%{_libdir}/libdcerpc.so.*

%dir %{_libdir}/samba
%{_libdir}/samba/libCHARSET3-samba4.so
%{_libdir}/samba/libaddns-samba4.so
%{_libdir}/samba/libads-samba4.so
%{_libdir}/samba/libasn1util-samba4.so
%{_libdir}/samba/libauth-sam-reply-samba4.so
%{_libdir}/samba/libauth-samba4.so
%{_libdir}/samba/libauthkrb5-samba4.so
%{_libdir}/samba/libcli-cldap-samba4.so
%{_libdir}/samba/libcli-ldap-common-samba4.so
%{_libdir}/samba/libcli-ldap-samba4.so
%{_libdir}/samba/libcli-nbt-samba4.so
%{_libdir}/samba/libcli-smb-common-samba4.so
%{_libdir}/samba/libcli-spoolss-samba4.so
%{_libdir}/samba/libcliauth-samba4.so
%{_libdir}/samba/libcmdline-credentials-samba4.so
%{_libdir}/samba/libdbwrap-samba4.so
%{_libdir}/samba/libdcerpc-samba-samba4.so
%{_libdir}/samba/libdsdb-garbage-collect-tombstones-samba4.so
%{_libdir}/samba/libevents-samba4.so
%{_libdir}/samba/libflag-mapping-samba4.so
%{_libdir}/samba/libgenrand-samba4.so
%{_libdir}/samba/libgensec-samba4.so
%{_libdir}/samba/libgpo-samba4.so
%{_libdir}/samba/libgse-samba4.so
%{_libdir}/samba/libhttp-samba4.so
%{_libdir}/samba/libinterfaces-samba4.so
%{_libdir}/samba/libiov-buf-samba4.so
%{_libdir}/samba/libkrb5samba-samba4.so
%{_libdir}/samba/libldbsamba-samba4.so
%{_libdir}/samba/liblibcli-lsa3-samba4.so
%{_libdir}/samba/liblibcli-netlogon3-samba4.so
%{_libdir}/samba/liblibsmb-samba4.so
%{_libdir}/samba/libmessages-dgm-samba4.so
%{_libdir}/samba/libmessages-util-samba4.so
%{_libdir}/samba/libmsghdr-samba4.so
%{_libdir}/samba/libmsrpc3-samba4.so
%{_libdir}/samba/libndr-samba-samba4.so
%{_libdir}/samba/libndr-samba4.so
%{_libdir}/samba/libnet-keytab-samba4.so
%{_libdir}/samba/libnetif-samba4.so
%{_libdir}/samba/libnpa-tstream-samba4.so
%{_libdir}/samba/libposix-eadb-samba4.so
%{_libdir}/samba/libprinting-migrate-samba4.so
%{_libdir}/samba/libreplace-samba4.so
%{_libdir}/samba/libregistry-samba4.so
%{_libdir}/samba/libsamba-cluster-support-samba4.so
%{_libdir}/samba/libsamba-debug-samba4.so
%{_libdir}/samba/libsamba-modules-samba4.so
%{_libdir}/samba/libsamba-security-samba4.so
%{_libdir}/samba/libsamba-sockets-samba4.so
%{_libdir}/samba/libsamba3-util-samba4.so
%{_libdir}/samba/libsamdb-common-samba4.so
%{_libdir}/samba/libsecrets3-samba4.so
%{_libdir}/samba/libserver-id-db-samba4.so
%{_libdir}/samba/libserver-role-samba4.so
%{_libdir}/samba/libsmb-transport-samba4.so
%{_libdir}/samba/libsmbclient-raw-samba4.so
%{_libdir}/samba/libsmbd-base-samba4.so
%{_libdir}/samba/libsmbd-conn-samba4.so
%{_libdir}/samba/libsmbd-shim-samba4.so
%{_libdir}/samba/libsmbldaphelper-samba4.so
%{_libdir}/samba/libsmbregistry-samba4.so
%{_libdir}/samba/libsys-rw-samba4.so
%{_libdir}/samba/libsocket-blocking-samba4.so
%{_libdir}/samba/libtalloc-report-samba4.so
%{_libdir}/samba/libtdb-wrap-samba4.so
%{_libdir}/samba/libtime-basic-samba4.so
%{_libdir}/samba/libtorture-samba4.so
%{_libdir}/samba/libtrusts-util-samba4.so
%{_libdir}/samba/libutil-cmdline-samba4.so
%{_libdir}/samba/libutil-reg-samba4.so
%{_libdir}/samba/libutil-setid-samba4.so
%{_libdir}/samba/libutil-tdb-samba4.so

# Internal or independent TALLOC library/package (2.1.8)
%{_libdir}/samba/libtalloc.so
%{_libdir}/samba/libtalloc.so.2
%{_libdir}/samba/libtalloc.so.%{talloc_version}
%{_libdir}/samba/libpytalloc-util.so
%{_libdir}/samba/libpytalloc-util.so.2
%{_libdir}/samba/libpytalloc-util.so.%{talloc_version}

# Internal or independent TEVENT library/package (0.9.29)
%{_libdir}/samba/libtevent.so
%{_libdir}/samba/libtevent.so.0
%{_libdir}/samba/libtevent.so.%{tevent_version}

# Internal or independent TDB library/package (1.3.10)
%{_libdir}/samba/libtdb.so
%{_libdir}/samba/libtdb.so.1
%{_libdir}/samba/libtdb.so.%{tdb_version}

# Internal or independent LDB library/package (1.1.27)
%{_libdir}/samba/libldb.so
%{_libdir}/samba/libldb.so.1
%{_libdir}/samba/libldb.so.%{ldb_version}
%{_libdir}/samba/libpyldb-util.so
%{_libdir}/samba/libpyldb-util.so.1
%{_libdir}/samba/libpyldb-util.so.%{ldb_version}



# Include samba-common-libs in the samba-common package
%{_libdir}/samba/libpopt-samba3-samba4.so

%dir %{_libdir}/samba/ldb

%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so
%{_libdir}/samba/pdb/wbc_sam.so


# Samba AD Domain Controller
# Include samba-dc in the samba-common package
%{_bindir}/samba-tool
%{_sbindir}/samba
%{_sbindir}/samba_kcc
%{_sbindir}/samba_dnsupdate
%{_sbindir}/samba_spnupdate
%{_sbindir}/samba_upgradedns
%{_libdir}/samba/auth/samba4.so
%{_libdir}/samba/bind9/dlz_bind9.so
%{_libdir}/samba/bind9/dlz_bind9_10.so
%{_libdir}/samba/libheimntlm-samba4.so
%{_libdir}/samba/libheimntlm-samba4.so.1
%{_libdir}/samba/libheimntlm-samba4.so.1.0.1
%{_libdir}/samba/libkdc-samba4.so
%{_libdir}/samba/libkdc-samba4.so.2
%{_libdir}/samba/libkdc-samba4.so.2.0.0
%{_libdir}/samba/libpac-samba4.so
%dir %{_libdir}/samba/gensec
%{_libdir}/samba/gensec/krb5.so
%{_libdir}/samba/ldb/acl.so
%{_libdir}/samba/ldb/aclread.so
%{_libdir}/samba/ldb/anr.so
%{_libdir}/samba/ldb/descriptor.so
%{_libdir}/samba/ldb/dirsync.so
%{_libdir}/samba/ldb/dns_notify.so
%{_libdir}/samba/ldb/extended_dn_in.so
%{_libdir}/samba/ldb/extended_dn_out.so
%{_libdir}/samba/ldb/extended_dn_store.so
%{_libdir}/samba/ldb/ildap.so
%{_libdir}/samba/ldb/instancetype.so
%{_libdir}/samba/ldb/lazy_commit.so
%{_libdir}/samba/ldb/ldbsamba_extensions.so
%{_libdir}/samba/ldb/linked_attributes.so
%{_libdir}/samba/ldb/local_password.so
%{_libdir}/samba/ldb/new_partition.so
%{_libdir}/samba/ldb/objectclass.so
%{_libdir}/samba/ldb/objectclass_attrs.so
%{_libdir}/samba/ldb/objectguid.so
%{_libdir}/samba/ldb/operational.so
%{_libdir}/samba/ldb/partition.so
%{_libdir}/samba/ldb/password_hash.so
%{_libdir}/samba/ldb/ranged_results.so
%{_libdir}/samba/ldb/repl_meta_data.so
%{_libdir}/samba/ldb/resolve_oids.so
%{_libdir}/samba/ldb/rootdse.so
%{_libdir}/samba/ldb/samba3sam.so
%{_libdir}/samba/ldb/samba3sid.so
%{_libdir}/samba/ldb/samba_dsdb.so
%{_libdir}/samba/ldb/samba_secrets.so
%{_libdir}/samba/ldb/samldb.so
%{_libdir}/samba/ldb/schema_data.so
%{_libdir}/samba/ldb/schema_load.so
%{_libdir}/samba/ldb/secrets_tdb_sync.so
%{_libdir}/samba/ldb/show_deleted.so
%{_libdir}/samba/ldb/simple_dn.so
%{_libdir}/samba/ldb/simple_ldap_map.so
%{_libdir}/samba/ldb/subtree_delete.so
%{_libdir}/samba/ldb/subtree_rename.so
%{_libdir}/samba/ldb/tombstone_reanimate.so
%{_libdir}/samba/ldb/update_keytab.so
%{_libdir}/samba/ldb/wins_ldb.so
%{_libdir}/samba/vfs/posix_eadb.so
%dir /var/lib/samba/sysvol
%{_datadir}/samba/setup


# Include samba-dc-libs in the samba-common package
%{_libdir}/samba/libprocess-model-samba4.so
%{_libdir}/samba/libservice-samba4.so
%dir %{_libdir}/samba/process_model
%{_libdir}/samba/process_model/standard.so
%dir %{_libdir}/samba/service
%{_libdir}/samba/service/cldap.so
%{_libdir}/samba/service/dcerpc.so
%{_libdir}/samba/service/dns.so
%{_libdir}/samba/service/dns_update.so
%{_libdir}/samba/service/drepl.so
%{_libdir}/samba/service/kcc.so
%{_libdir}/samba/service/kdc.so
%{_libdir}/samba/service/ldap.so
%{_libdir}/samba/service/nbtd.so
%{_libdir}/samba/service/ntp_signd.so
%{_libdir}/samba/service/s3fs.so
%{_libdir}/samba/service/web.so
%{_libdir}/samba/service/winbindd.so
%{_libdir}/samba/service/wrepl.so
%{_libdir}/libdcerpc-server.so.*
%{_libdir}/samba/libdfs-server-ad-samba4.so
%{_libdir}/samba/libdnsserver-common-samba4.so
%{_libdir}/samba/libdsdb-module-samba4.so
# Not found %{_libdir}/samba/libntvfs-samba4.so
%{_libdir}/samba/bind9/dlz_bind9_9.so



### DEVEL
%files devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/charset.h
%{_includedir}/samba-4.0/core/doserr.h
%{_includedir}/samba-4.0/core/error.h
%{_includedir}/samba-4.0/core/hresult.h
%{_includedir}/samba-4.0/core/ntstatus.h
%{_includedir}/samba-4.0/core/werror.h
%{_includedir}/samba-4.0/credentials.h
%{_includedir}/samba-4.0/dcerpc.h
%{_includedir}/samba-4.0/domain_credentials.h
%{_includedir}/samba-4.0/gen_ndr/atsvc.h
%{_includedir}/samba-4.0/gen_ndr/auth.h
%{_includedir}/samba-4.0/gen_ndr/dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/lsa.h
%{_includedir}/samba-4.0/gen_ndr/misc.h
%{_includedir}/samba-4.0/gen_ndr/nbt.h
%{_includedir}/samba-4.0/gen_ndr/drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/gen_ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/gen_ndr/ndr_atsvc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/gen_ndr/ndr_misc.h
%{_includedir}/samba-4.0/gen_ndr/ndr_nbt.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr.h
%{_includedir}/samba-4.0/gen_ndr/ndr_samr_c.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/gen_ndr/ndr_svcctl_c.h
%{_includedir}/samba-4.0/gen_ndr/netlogon.h
%{_includedir}/samba-4.0/gen_ndr/samr.h
%{_includedir}/samba-4.0/gen_ndr/security.h
%{_includedir}/samba-4.0/gen_ndr/server_id.h
%{_includedir}/samba-4.0/gen_ndr/svcctl.h
%{_includedir}/samba-4.0/ldb_wrap.h
%{_includedir}/samba-4.0/lookup_sid.h
%{_includedir}/samba-4.0/machine_sid.h
%{_includedir}/samba-4.0/ndr.h
%dir %{_includedir}/samba-4.0/ndr
%{_includedir}/samba-4.0/ndr/ndr_dcerpc.h
%{_includedir}/samba-4.0/ndr/ndr_drsblobs.h
%{_includedir}/samba-4.0/ndr/ndr_drsuapi.h
%{_includedir}/samba-4.0/ndr/ndr_krb5pac.h
%{_includedir}/samba-4.0/ndr/ndr_svcctl.h
%{_includedir}/samba-4.0/ndr/ndr_nbt.h
%{_includedir}/samba-4.0/netapi.h
%{_includedir}/samba-4.0/param.h
%{_includedir}/samba-4.0/passdb.h
%{_includedir}/samba-4.0/policy.h
%{_includedir}/samba-4.0/rpc_common.h
%{_includedir}/samba-4.0/samba/session.h
%{_includedir}/samba-4.0/samba/version.h
%{_includedir}/samba-4.0/share.h
%{_includedir}/samba-4.0/smb2_lease_struct.h
%{_includedir}/samba-4.0/smbconf.h
%{_includedir}/samba-4.0/smb_ldap.h
%{_includedir}/samba-4.0/smbldap.h
%{_includedir}/samba-4.0/tdr.h
%{_includedir}/samba-4.0/tsocket.h
%{_includedir}/samba-4.0/tsocket_internal.h
%dir %{_includedir}/samba-4.0/util
%{_includedir}/samba-4.0/util/attr.h
%{_includedir}/samba-4.0/util/blocking.h
%{_includedir}/samba-4.0/util/byteorder.h
%{_includedir}/samba-4.0/util/data_blob.h
%{_includedir}/samba-4.0/util/debug.h
%{_includedir}/samba-4.0/util/fault.h
%{_includedir}/samba-4.0/util/genrand.h
%{_includedir}/samba-4.0/util/idtree.h
%{_includedir}/samba-4.0/util/idtree_random.h
%{_includedir}/samba-4.0/util/memory.h
%{_includedir}/samba-4.0/util/safe_string.h
%{_includedir}/samba-4.0/util/signal.h
%{_includedir}/samba-4.0/util/string_wrappers.h
%{_includedir}/samba-4.0/util/substitute.h
%{_includedir}/samba-4.0/util/talloc_stack.h
%{_includedir}/samba-4.0/util/tevent_ntstatus.h
%{_includedir}/samba-4.0/util/tevent_unix.h
%{_includedir}/samba-4.0/util/tevent_werror.h
%{_includedir}/samba-4.0/util/time.h
%{_includedir}/samba-4.0/util/xfile.h
%{_includedir}/samba-4.0/util_ldb.h
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-samr.so
%{_libdir}/libdcerpc.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so
%{_libdir}/libndr.so
%{_libdir}/libnetapi.so
%{_libdir}/libsamba-credentials.so
%{_libdir}/libsamba-errors.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-policy.so
%{_libdir}/libsamba-util.so
%{_libdir}/libsamdb.so
%{_libdir}/libsmbconf.so
%{_libdir}/libtevent-util.so
%{_libdir}/pkgconfig/dcerpc.pc
%{_libdir}/pkgconfig/dcerpc_samr.pc
%{_libdir}/pkgconfig/ndr.pc
%{_libdir}/pkgconfig/ndr_krb5pac.pc
%{_libdir}/pkgconfig/ndr_nbt.pc
%{_libdir}/pkgconfig/ndr_standard.pc
%{_libdir}/pkgconfig/netapi.pc
%{_libdir}/pkgconfig/samba-credentials.pc
%{_libdir}/pkgconfig/samba-hostconfig.pc
%{_libdir}/pkgconfig/samba-policy.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/samdb.pc
%{_libdir}/libsamba-passdb.so
%{_libdir}/libsmbldap.so

# For samba-dc
%{_includedir}/samba-4.0/dcerpc_server.h
%{_libdir}/libdcerpc-server.so
%{_libdir}/pkgconfig/dcerpc_server.pc

%{_includedir}/samba-4.0/libsmbclient.h

%{_includedir}/samba-4.0/wbclient.h


### Package samba-libs
%files libs
%defattr(-,root,system)
%{_libdir}/libdcerpc-samr.so.*
%{_libdir}/libsamba-policy.so.*

# libraries needed by the public libraries
%{_libdir}/samba/libMESSAGING-samba4.so
%{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so
%{_libdir}/samba/libauth4-samba4.so
%{_libdir}/samba/libauth-unix-token-samba4.so
%{_libdir}/samba/libcluster-samba4.so
%{_libdir}/samba/libdcerpc-samba4.so
%{_libdir}/samba/libnon-posix-acls-samba4.so
%{_libdir}/samba/libsamba-net-samba4.so
%{_libdir}/samba/libsamba-python-samba4.so
%{_libdir}/samba/libshares-samba4.so
%{_libdir}/samba/libsmbpasswdparser-samba4.so
%{_libdir}/samba/libxattr-tdb-samba4.so

# For samba-dc
%{_libdir}/samba/libdb-glue-samba4.so
%{_libdir}/samba/libHDB-SAMBA4-samba4.so
%{_libdir}/samba/libasn1-samba4.so
%{_libdir}/samba/libasn1-samba4.so.8
%{_libdir}/samba/libasn1-samba4.so.8.0.0
%{_libdir}/samba/libcom_err-samba4.so
%{_libdir}/samba/libcom_err-samba4.so.0
%{_libdir}/samba/libcom_err-samba4.so.0.25
%{_libdir}/samba/libgssapi-samba4.so
%{_libdir}/samba/libgssapi-samba4.so.2
%{_libdir}/samba/libgssapi-samba4.so.2.0.0
%{_libdir}/samba/libhcrypto-samba4.so
%{_libdir}/samba/libhcrypto-samba4.so.5
%{_libdir}/samba/libhcrypto-samba4.so.5.0.1
%{_libdir}/samba/libhdb-samba4.so
%{_libdir}/samba/libhdb-samba4.so.11
%{_libdir}/samba/libhdb-samba4.so.11.0.2
%{_libdir}/samba/libheimbase-samba4.so
%{_libdir}/samba/libheimbase-samba4.so.1
%{_libdir}/samba/libheimbase-samba4.so.1.0.0
%{_libdir}/samba/libhx509-samba4.so
%{_libdir}/samba/libhx509-samba4.so.5
%{_libdir}/samba/libhx509-samba4.so.5.0.0
%{_libdir}/samba/libkrb5-samba4.so
%{_libdir}/samba/libkrb5-samba4.so.26
%{_libdir}/samba/libkrb5-samba4.so.26.0.0
%{_libdir}/samba/libroken-samba4.so
%{_libdir}/samba/libroken-samba4.so.19
%{_libdir}/samba/libroken-samba4.so.19.0.1
%{_libdir}/samba/libwind-samba4.so
%{_libdir}/samba/libwind-samba4.so.0
%{_libdir}/samba/libwind-samba4.so.0.0.0



# Test package samba-test
%files test
%defattr(-,root,root)
%{_bindir}/gentest
%{_bindir}/locktest
%{_bindir}/masktest
%{_bindir}/ndrdump
%{_bindir}/smbtorture
# %{_mandir}/man1/gentest.1*
# %{_mandir}/man1/locktest.1*
# %{_mandir}/man1/masktest.1*
# %{_mandir}/man1/ndrdump.1*
# %{_mandir}/man1/smbtorture.1*
# %{_mandir}/man1/vfstest.1*

%if %{with testsuite}
# files to ignore in testsuite mode
%{_libdir}/samba/libnss-wrapper.so
%{_libdir}/samba/libsocket-wrapper.so
%{_libdir}/samba/libuid-wrapper.so
%endif

# Test package samba-test-libs
%files test-libs
%defattr(-,root,root)
# %if %with_dc
%{_libdir}/samba/libdlz-bind9-for-torture-samba4.so
# %else
%{_libdir}/samba/libdsdb-module-samba4.so
# %endif



%files winbind
%defattr(-,root,system)
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_sbindir}/winbindd
%{_libdir}/%{name}/idmap
%{_libdir}/%{name}/nss_info
%{_libdir}/samba/libnss-info-samba4.so
%{_libdir}/samba/libidmap-samba4.so
%ghost %dir /var/run/winbindd
%attr(750,root,wbpriv) %dir /var/lib/%{name}/winbindd_privileged
/etc/rc.d/init.d/winbindd
/etc/rc.d/rc2.d/Kwinbindd
/etc/rc.d/rc2.d/Swinbindd
/etc/rc.d/rc3.d/Kwinbindd
/etc/rc.d/rc3.d/Swinbindd


%files winbind-krb5-locator
%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so


%files winbind-clients
%defattr(-,root,system)
%{_libdir}/libwbclient.so*
%{_libdir}/samba/libwinbind-client-samba4.so
%{_libdir}/security/pam_winbind.so


%files winbind-devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc


# %files doc
# %defattr(-,root,system)


%files -n libsmbclient
%defattr(-,root,system)
%{_libdir}/libsmbclient.so*
#%{_libdir}/libsmbsharemodes.so*


%files -n libsmbclient-devel
%defattr(-,root,system)
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/pkgconfig/smbclient.pc
#%{_libdir}/pkgconfig/smbsharemodes.pc
#%{_mandir}/man7/libsmbclient.7*


# %files domainjoin-gui
# %defattr(-,root,system)
# %{_sbindir}/netdomjoin-gui
# %dir %{_datadir}/pixmaps/%{name}
# %{_datadir}/pixmaps/%{name}/%{name}.ico
# %{_datadir}/pixmaps/%{name}/logo.png
# %{_datadir}/pixmaps/%{name}/logo-small.png


# Samba Python libraries
%files python
%defattr(-,root,root,-)
%{python_sitearch}/*


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
* Wed Dec 08 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.1-1
- Update to version 4.5.1

* Wed Oct 26 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.0-3
- Add AIX installation guide in %doc and echo a message post install

* Wed Oct 10 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.5.0-2
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

* Wed Apr 08 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.6-3
- Not downloaded as of 13th April
- Patch0 in 589 source files for CVE security fixes
- Patch11 in 8 source files to work around latest XLC issue
- Remove Patch10, fix in latest XLC

* Wed Mar 29 2016 Michael Wilson <michael.a.wilson@atos.net> - 4.3.6-2
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
