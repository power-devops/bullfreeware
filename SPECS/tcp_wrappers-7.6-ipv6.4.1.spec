Summary: A security tool which acts as a wrapper for TCP daemons
Name: tcp_wrappers
Version: 7.6
Release: ipv6.4.1

#%define LIB_MAJOR 0
#%define LIB_MINOR 7
#%define LIB_REL 6

License: BSD
Group: System Environment/Daemons

Source0: ftp://ftp.porcupine.org/pub/security/%{name}_%{version}-ipv6.4.tar.gz
Source1: ftp://ftp.porcupine.org/pub/security/%{name}_%{version}-ipv6.4.tar.gz.sig
URL: ftp://ftp.porcupine.org/pub/security/index.html
Patch0: tcp_wrappers_7.6-ipv6-config_aix.patch
Patch1: tcp_wrappers_7.6-ipv6.4-setenv.patch
Patch2: tcp_wrappers_7.6-ipv6.4-netgroup.patch
Patch3: tcp_wrappers-7.6-bug11881.patch
Patch4: tcp_wrappers-7.6-bug17795.patch
Patch5: tcp_wrappers_7.6-ipv6.4-bug17847.patch
Patch6: tcp_wrappers-7.6-ipv6.4-fixgethostbyname.patch
Patch7: tcp_wrappers_7.6-ipv6.4-docu.patch
Patch12: tcp_wrappers-7.6-sig.patch
Patch13: tcp_wrappers_7.6-ipv6.4-strerror.patch
Patch14: tcp_wrappers-7.6-ldflags.patch
Patch15: tcp_wrappers-7.6-fix_sig-bug141110.patch
Patch16: tcp_wrappers-7.6-162412.patch
Patch19: tcp_wrappers-7.6-siglongjmp.patch
Patch20: tcp_wrappers-7.6-sigchld.patch
Patch21: tcp_wrappers-7.6-196326.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: tcp_wrappers-libs = %{version}-%{release}

%description
The tcp_wrappers package provides small daemon programs which can
monitor and filter incoming requests for systat, finger, FTP, telnet,
rlogin, rsh, exec, tftp, talk and other network services.

Install the tcp_wrappers program if you need a security tool for
filtering incoming network services requests.

This version also supports IPv6.

%package libs
Summary: tcp_wrappers libraries
Group: System Environment/Libraries

%description libs
tcp_wrappers-libs contains the libraries of the tcp_wrappers package.

%package devel
Summary: tcp_wrappers development libraries and headers
Group: Development/Libraries
Requires: tcp_wrappers-libs = %{version}-%{release}

%description devel
tcp_wrappers-devel contains the libraries and header files needed to
develop applications with tcp_wrappers support.

%prep
%setup -q -n %{name}_%{version}-ipv6.4

%patch0 -p1 -b .config_aix
%patch1 -p1 -b .setenv 
%patch2 -p1 -b .netgroup
%patch3 -p1 -b .bug11881
%patch4 -p1 -b .bug17795
%patch5 -p1 -b .bug17847
%patch6 -p1 -b .fixgethostbyname
%patch7 -p1 -b .docu
%patch12 -p1 -b .sig
%patch13 -p1 -b .strerror
%patch14 -p1 -b .cflags
%patch15 -p1 -b .fix_sig
%patch16 -p1 -b .162412
%patch19 -p1 -b .siglongjmp
%patch20 -p1 -b .sigchld
%patch21 -p1 -b .196326

%build
make aix

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

install -p -m644 hosts_access.3 ${RPM_BUILD_ROOT}%{_mandir}/man3
install -p -m644 hosts_access.5 hosts_options.5 ${RPM_BUILD_ROOT}%{_mandir}/man5
install -p -m644 tcpd.8 tcpdchk.8 tcpdmatch.8 ${RPM_BUILD_ROOT}%{_mandir}/man8
ln -sf hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.allow.5
ln -sf hosts_access.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/hosts.deny.5
cp -a libwrap.a ${RPM_BUILD_ROOT}%{_libdir}
#cp -a libwrap.so* ${RPM_BUILD_ROOT}/%{_lib}
install -p -m644 tcpd.h ${RPM_BUILD_ROOT}%{_includedir}
install -m755 safe_finger ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 tcpd ${RPM_BUILD_ROOT}%{_sbindir}
install -m755 try-from ${RPM_BUILD_ROOT}%{_sbindir}

# XXX remove utilities that expect /etc/inetd.conf (#16059).
#install -m755 tcpdchk ${RPM_BUILD_ROOT}%{_sbindir}
#install -m755 tcpdmatch ${RPM_BUILD_ROOT}%{_sbindir}
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdmatch.*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man8/tcpdchk.*

(
  cd $RPM_BUILD_ROOT
  for dir in sbin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)
#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
%{_sbindir}/*
%{_mandir}/man8/*
/usr/sbin/*

%files libs
%defattr(-,root,system,-)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
#/%{_lib}/*.so.*
%{_libdir}/*.a
%{_mandir}/man5/*
/usr/lib/*.a

%files devel
%defattr(-,root,system,-)
%{_includedir}/*
/usr/include/*
#%{_libdir}/*.a
#/%{_lib}/*.so
%{_mandir}/man3/*

%changelog
* Tue Mar 19 2013 Gerard Visiedo <gerard.visiedo@bull.net>  - 7.6-ipv6.4.1
- Initial port on Aix6.1
- More information in http://www.ibmsystemsmag.com/aix/administrator/security/TCP-Wrappers-Provide-Robust-Logs

