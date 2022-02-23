Summary: A network traffic monitoring tool
Name: tcpdump
Version: 4.7.4.20160311
# Since version 4.7.4/1.7.4 of tcpdump/libpcap has 38 FAILED tests out
# of 165 tests, both on AIX and on Ubuntu/Intel, master of 2016 March 11th
# is used instead, waiting for official 4.7.5/1.7.5 .
Release: 1
License: BSD with advertising
URL: http://www.tcpdump.org
Group: Applications/Internet
Source0: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
# Removed because I've built the .tar.gz from GitHub
#Source1: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig

# This version is named 4.7.4.1 , but it is an extract (gzip) from TCPDUMP GitHub
# Done the 11th of March, 2016
# Results of tests:
# - Ubuntu / Intel :
#   (./configure && make -s && make check) > ../tcpdump-master.BuiltTest.res1 2>&1
# 
# - AIX 6.1 :
#   pcap-invalid-version-2        : TEST FAILED
#   pcap-ng-invalid-vers-1        : passed
#   pcap-ng-invalid-vers-2        : TEST FAILED
#   lmp-v                         : TEST SKIPPED (compiler is not GCC)
#   ----------------------------------------------
#      2 tests failed
#    183 tests passed


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel >= 1.0.1i-1
BuildRequires: libpcap-devel >= 1.4.0
BuildRequires: libsmi-devel >= 0.4.8-1
BuildRequires: sed
Requires: openssl >= 1.0.1i-1
Requires: libpcap >= 1.7.4
Requires: libsmi >= 0.4.8-1

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.


%prep
%setup -q


%build

export CC="cc -qcpluscmt"
export AR="/usr/bin/ar -X32_64"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

#    --disable-ipv6 is no more an option of TCPDUMP configure

make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

mv -f ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_mandir}/man8

# fix section numbers
/opt/freeware/bin/sed -i 's/\(\.TH[a-zA-Z ]*\)[1-9]\(.*\)/\18\2/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man8/*

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
cd usr/linux/bin
ln -sf ../../..%{_sbindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc LICENSE README.md CHANGES CREDITS
%{_sbindir}/*
%{_mandir}/man8/*
/usr/linux/bin/*


%changelog
* Tue Jan 21 2016 Tony Reix <tony.reix@atos.net - 4.7.4.1-1
- updated to version 4.7.4.1 which is GitHub 2016 January 16 version

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
