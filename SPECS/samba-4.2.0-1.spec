
%define wbpriv_gid 88

%define with_libuuid 0
%define with_GPFS    0

%define samba_source source3

Summary: Server and Client software to interoperate with Windows machines
Name: samba
Version: 4.2.0
Release: 1
License: GPLv3+ and LGPLv3+
Group: System Environment/Daemons
URL: http://www.samba.org/

Source0: http://www.samba.org/samba/%{name}-%{version}.tar.gz
Source1: http://www.samba.org/samba/%{name}-%{version}.tar.asc

Source2: %{name}.log
Source3: swat.desktop
Source4: %{name}.sysconfig
Source5: smb.conf.default
Source6: smbprint
Source7: smbd.aix.init
Source8: nmbd.aix.init
Source9: winbindd.aix.init

Patch0: %{name}-3.6.24-aix.patch
Patch1: 0002-Bug-8984-AIX-6.1-nmbd-Failed-to-open-nmb-bcast-socket.patch
Patch2: samba-4.2.0-Time.patch
Patch3: samba-4.2.0-Texpect.patch
Patch4: samba-4.2.0-TdbAIX.patch
Patch5: samba-4.2.0-netlogon_creds_cli.patch
Patch6: samba-4.2.0-Struc_bad_initialization.patch
Patch7: samba-4.2.0-BadInitializationTypes.patch
Patch8: samba-4.2.0-BadInitializationTypesA.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: make, patch

BuildRequires: cups-devel >= 1.4.4-2
BuildRequires: gtk2-devel >= 2.8.3-9
BuildRequires: krb5-devel >= 1.8.3-1
BuildRequires: libiconv >= 1.14-1
BuildRequires: openldap-devel >= 2.4.23
BuildRequires: openssl-devel >= 1.0.1
BuildRequires: popt >= 1.7-2
BuildRequires: readline-devel >= 5.2-3
%if %{with_libuuid}
BuildRequires: uuid-devel >= 1.6.2-1
%endif

Requires: %{name}-common = %{version}-%{release}

Requires: bash
Requires: cups >= 1.4.4-2
Requires: gtk2 >= 2.8.3-9
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
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


%package client
Summary: Samba client programs
Group: Applications/System
Requires: bash
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description client
The samba-client package provides some SMB/CIFS clients to complement
the built-in SMB/CIFS filesystem in Linux. These clients allow access
of SMB/CIFS shares and printing to SMB/CIFS printers.


%package common
Summary: Files used by both Samba servers and clients
Group: Applications/System
Requires: %{name}-winbind-clients = %{version}-%{release}
Requires: krb5-libs >= 1.8.3-1
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.


%package winbind
Summary: Samba winbind
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-winbind-clients = %{version}-%{release}
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description winbind
The samba-winbind package provides the winbind daemon and some client tools.
Winbind enables Linux to be a full member in Windows domains and to use
Windows user and group accounts on Linux.


%package winbind-krb5-locator
Summary: Samba winbind krb5 locator
Group: Applications/System
Requires: %{name}-winbind-clients = %{version}-%{release}
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description winbind-krb5-locator
The winbind krb5 locator is a plugin for the system kerberos library to allow
the local kerberos library to use the same KDC as samba and winbind use


%package winbind-clients
Summary: Samba winbind clients
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description winbind-devel
The samba-winbind package provides developer tools for the wbclient library.


%package swat
Summary: The Samba SMB server Web configuration program
Group: Applications/System
Requires: %{name} = %{version}-%{release}
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description swat
The samba-swat package includes the new SWAT (Samba Web Administration
Tool), for remotely managing Samba's smb.conf file using your favorite
Web browser.


%package doc
Summary: Documentation for the Samba suite
Group: Documentation
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description doc
The samba-doc package includes all the non-manpage documentation for the
Samba suite.


%package domainjoin-gui
Summary: Domainjoin GUI
Group: Applications/System
Requires: %{name}-common = %{version}-%{release}
Requires: gtk2 >= 2.8.3-9
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description domainjoin-gui
The samba-domainjoin-gui package includes a domainjoin gtk application.


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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
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
Requires: AIX-rpm < 6.2.0.0
%endif
%ifos aix7.1
Requires: AIX-rpm >= 7.1.0.0
Requires: AIX-rpm < 7.2.0.0
%endif

%description -n libsmbclient-devel
The libsmbclient-devel package contains the header files and libraries needed to
develop programs that link against the SMB client library in the Samba suite.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0
%patch1 -p1
%patch2 -p1 -b .Time
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 



%build

# function to build samba
build_samba()
{
##  cd %{samba_source}

  ./configure -v \
      --prefix=%{_prefix} \
      --libdir=$1 \
      --sysconfdir=/etc/%{name} \
      --mandir=%{_mandir} \
      --with-lockdir=/var/locks \
      --with-piddir=/var/run \
      --with-privatedir=/var/lib/%{name}/private \
      --with-logfilebase=/var/log/%{name} \
      --with-modulesdir=$1/%{name} \
      --with-pammodulesdir=$1/security \
      --with-acl-support \
      --with-ads \
      --with-automount \
%if %{with_libuuid}
      --with-dnsupdate \
%endif
      --with-ldap \
      --with-libiconv=%{_prefix} \
      --with-pam \
      --with-pam_smbpass \
      --with-quotas \
      --with-sendfile-support \
      --with-syslog \
      --with-utmp \
%if %{with_GPFS}
      --with-shared-modules=idmap_ad,idmap_adex,idmap_rid,idmap_hash,idmap_tdb2,vfs_gpfs \
%else
      --with-shared-modules=idmap_ad,idmap_adex,idmap_rid,idmap_hash,idmap_tdb2 \
%endif

  gmake
  make debug2html smbfilter

}

export CFLAGS="-D_LARGE_FILES=1 -qcpluscmt -bnoquiet"
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
mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}/old
mkdir -p ${RPM_BUILD_ROOT}/var/spool/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/swat/using_samba
mkdir -p ${RPM_BUILD_ROOT}/var/run/winbindd
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig

cp %{SOURCE5} ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf
chmod 0644 ${RPM_BUILD_ROOT}/etc/%{name}/smb.conf

cp samba-4.2.0/source3/script/mksmbpasswd.sh ${RPM_BUILD_ROOT}%{_bindir}/
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/mksmbpasswd.sh

cp samba-4.2.0/packaging/RHEL/setup/smbusers ${RPM_BUILD_ROOT}/etc//%{name}/smbusers
chmod 0644 ${RPM_BUILD_ROOT}/etc//%{name}/smbusers

cp samba-4.2.0/packaging/printing/smbprint ${RPM_BUILD_ROOT}%{_bindir}/
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/smbprint

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

echo 127.0.0.1 localhost > ${RPM_BUILD_ROOT}/etc/%{name}/lmhosts

mkdir -p ${RPM_BUILD_ROOT}/etc/openldap/schema
cp samba-4.2.0/examples/LDAP/%{name}.schema ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema
chmod 0644 ${RPM_BUILD_ROOT}/etc/openldap/schema/%{name}.schema

# winbind krb5 locator
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5
cp samba-4.2.0/bin/shared/winbind_krb5_locator.so ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

# pkgconfig files
#list="smbclient smbsharemodes wbclient"
#for i in ${list} ; do
#    cp %{samba_source}/pkgconfig/${i}.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/
#done
cp samba-4.2.0/bin/default/source3/libsmb/smbclient.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/ 
cp samba-4.2.0/bin/default/source3/libnet/netapi.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/ 
cp samba-4.2.0/bin/default/nsswitch/libwbclient/wbclient.pc ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/

mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
cp %{SOURCE4} ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}
chmod 0644 ${RPM_BUILD_ROOT}/etc/sysconfig/%{name}

cp -r samba-4.2.0/source3/lib/netapi/examples/netdomjoin-gui ${RPM_BUILD_ROOT}%{_sbindir}/
chmod 0755 ${RPM_BUILD_ROOT}%{_sbindir}/netdomjoin-gui

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}
cp samba-4.2.0/source3/lib/netapi/examples/netdomjoin-gui/%{name}.ico ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/%{name}.ico
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/%{name}.ico

cp samba-4.2.0/source3/lib/netapi/examples/netdomjoin-gui/logo.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo.png
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo.png

cp samba-4.2.0/source3/lib/netapi/examples/netdomjoin-gui/logo-small.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo-small.png
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/%{name}/logo-small.png

# create additional directory structure
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d

# move the files into the structure
cp %{SOURCE7} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/smbd
cp %{SOURCE8} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/nmbd
cp %{SOURCE9} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/winbindd
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/*

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


%post
if [ "$1" -ge "1" ]; then
    /etc/rc.d/init.d/smbd condrestart >/dev/null 2>&1 || :
    /etc/rc.d/init.d/nmbd condrestart >/dev/null 2>&1 || :
fi
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
%doc examples/autofs examples/LDAP examples/libsmbclient examples/misc examples/printer-accounting
%doc examples/printing
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
#%{_mandir}/man7/%{name}.7*
#%{_mandir}/man8/eventlogadm.8*
#%{_mandir}/man8/nmbd.8*
#%{_mandir}/man8/smbd.8*
#%{_mandir}/man8/vfs_*.8*
%{_libdir}/%{name}/vfs
%{_libdir}/%{name}/auth
#%{_libdir}/%{name}/charset
%attr(1777,root,system) %dir /var/spool/%{name}
/etc/openldap/schema/%{name}.schema


%files swat
%defattr(-,root,system)
###%config(noreplace) /etc/xinetd.d/swat
%{_datadir}/swat


%files client
%defattr(-,root,system)
%{_bindir}/nmblookup
%{_bindir}/rpcclient
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbget
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbta-util
%{_bindir}/smbtar
%{_bindir}/smbtree


%files common
%defattr(-,root,system)
%doc WHATSNEW.txt Roadmap
%{_bindir}/net
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcquotas
%{_bindir}/smbcontrol
%{_bindir}/smbpasswd
%{_bindir}/tdb*
%{_bindir}/testparm
%attr(755,root,system) %{_libdir}/security/pam_smbpass.so
%dir %{_libdir}/%{name}
#%{_libdir}/%{name}/lowcase.dat
#%{_libdir}/%{name}/upcase.dat
#%{_libdir}/%{name}/valid.dat
#%{_libdir}/libnetapi.so*
#%{_libdir}/libtalloc.so*
#%{_libdir}/libtdb.so*
#%{_libdir}/libtevent.so*
%{_includedir}/netapi.h
#%{_includedir}/tevent.h
#%{_includedir}/tevent_internal.h
#%{_includedir}/talloc.h
#%{_includedir}/tdb.h
#/opt/freeware/src/packages/BUILD/samba-4.2.0/bin/default/source3/libnet/netapi.pc
%dir /var/lib/%{name}
%attr(700,root,system) %dir /var/lib/%{name}/private
%dir /var/lib/%{name}/scripts
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/smb.conf
%config(noreplace) /etc/%{name}/lmhosts
%config(noreplace) /etc/sysconfig/%{name}
%attr(0700,root,system) %dir /var/log/%{name}
%attr(0700,root,system) %dir /var/log/%{name}/old


%files winbind
%defattr(-,root,system)
%{_bindir}/ntlm_auth
%{_bindir}/wbinfo
%{_sbindir}/winbindd
%{_libdir}/%{name}/idmap
%{_libdir}/%{name}/nss_info
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
%{_libdir}/security/pam_winbind.so


%files winbind-devel
%defattr(-,root,system)
%{_includedir}/wbclient.h
%{_libdir}/pkgconfig/wbclient.pc


%files doc
%defattr(-,root,system)


%files -n libsmbclient
%defattr(-,root,system)
%{_libdir}/libsmbclient.so*
#%{_libdir}/libsmbsharemodes.so*


%files -n libsmbclient-devel
%defattr(-,root,system)
%{_includedir}/libsmbclient.h
%{_libdir}/pkgconfig/smbclient.pc
#%{_libdir}/pkgconfig/smbsharemodes.pc
#%{_mandir}/man7/libsmbclient.7*


%files domainjoin-gui
%defattr(-,root,system)
%{_sbindir}/netdomjoin-gui
%dir %{_datadir}/pixmaps/%{name}
%{_datadir}/pixmaps/%{name}/%{name}.ico
%{_datadir}/pixmaps/%{name}/logo.png
%{_datadir}/pixmaps/%{name}/logo-small.png


%changelog
* Wed Aug 12 2015 Hamza Sellami <hamza.sellami@aos.net> - 4.2.0-1
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
