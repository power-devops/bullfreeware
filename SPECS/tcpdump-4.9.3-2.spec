%bcond_without dotests

Summary: A tool for network monitoring and data acquisition.
Name: tcpdump
Version: 4.9.3
Release: 2
License: BSD
URL: http://www.tcpdump.org
Group: Applications/Networking
Source: http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

BuildRequires: libpcap-devel >= 1.9.1-1
BuildRequires: sed
Requires: libpcap >= 1.9.1-1

%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces.  Tcpdump can display all of
the packet headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build

export AR="/usr/bin/ar -X32_64"
#first build 64-bit version
cd 64bit
export CC="gcc -maix64 -O2"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

#    --disable-ipv6 is no more an option of TCPDUMP configure

make %{?_smp_mflags}


#now build 32-bit version
cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES -O2"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir}

#    --disable-ipv6 is no more an option of TCPDUMP configure

make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

(
	cd ${RPM_BUILD_ROOT}%{_sbindir}
	for f in *
	do
	    mv ${f} ${f}_64
  	done
)
mv -f ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_mandir}/man8

# fix section numbers
/opt/freeware/bin/sed -i 's/\(\.TH[a-zA-Z ]*\)[1-9]\(.*\)/\18\2/' \
    ${RPM_BUILD_ROOT}%{_mandir}/man8/*

cd ../32bit
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}
strip -X32_64 ${RPM_BUILD_ROOT}%{_sbindir}/* || :
(
	cd ${RPM_BUILD_ROOT}%{_sbindir}
        for f in tcpdump tcpdump.4.9.3 
        do
            mv ${f} ${f}_32
        done
)
# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_sbindir}
  for f in tcpdump tcpdump.4.9.3
  do
    ln -sf ${f}_64 ${f}
  done
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
( gmake -k check || true )
cd ../32bit
export OBJECT_MODE=32
( gmake -k check || true )
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/LICENSE 32bit/README.md 32bit/CHANGES 32bit/CREDITS
%{_sbindir}/*
%{_mandir}/man8/*


%changelog
* Wed Feb 19 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.9.3-2
- Bullfreeware OpenSSL removal
- BullFreeware Compatibility Improvements
- No more provide link on /usr
- Add check section

* Thu Nov 28 2019 Reshma V Kumar <reskumar@in.ibm.com> - 4.9.3-1
- Update to fix CVE-2018-16451 CVE-2018-16452, CVE-2018-16230, CVE-2019-15166,
- CVE-2018-14879, CVE-2018-16228, CVE-2018-16229, CVE-2018-16227, CVE-2018-14882,
- CVE-2018-16300, CVE-2018-14467, CVE-2018-14463, CVE-2018-14464

* Fri Dec 7 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 4.9.2-2
- Rebuilt due to compatibility issue with libpcap built with gcc

* Mon Nov 6 2017 Reshma V Kumar <reskumar@in.ibm.com>
- Update to 4.9.2 to fix security vulnerability

* Wed Mar 15 2017 Reshma V Kumar <reskumar@in.ibm.com>
- Update to 4.9.0 to fix security vulnerability

* Tue Dec 13 2016 Reshma V Kumar <reskumar@in.ibm.com> 4.8.1-1
- Update to latest version

* Thu Apr 14 2016 Ravi Hirekurabar <rhirekur@in.ibm.com> 4.7.4
- Update to version 4.7.4
 
* Mon Jan 19 2004 David Clissold <cliss@austin.ibm.com> 3.8.1-1
- Update to version 3.8.1

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri Jul 19 2002 Chris Tysor <cjtysor@us.ibm.com>
- Update to version 3.7.1, add missing %doc files.

* Mon Feb 11 2002 David Clissold <cliss@austin.ibm.com>
- Strip the binary.

* Wed May 30 2001 Marc Stephenson <marc@austin.ibm.com>
- Corrected summary and description

* Tue May 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Minor modifications

* Mon May 21 2001 Olof Johansson
- First version

