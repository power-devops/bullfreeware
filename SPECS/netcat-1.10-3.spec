Name:         netcat
License:      distributable, Other License(s), see package
Group:        Productivity/Networking/Other
Autoreqprov:  on
Summary:      A simple but powerful network tool
Version:      1.10
Release:      1
URL:	      ftp://coast.cs.purdue.edu/pub/tools/unix/netutils/netcat
Source0:      %{name}-%{version}.tar.gz
Source1:      %{name}.1
Patch0:       %{name}-%{version}-aix.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root

Conflicts:    nc

%description
Netcat is a simple Unix utility that reads and writes data across
network connections, using TCP or UDP protocols. It is designed to be a
reliable "back-end" tool that can be used directly or easily driven by
other programs and scripts.  At the same time, it is a feature-rich
network debugging and exploration tool, since it can create almost any
kind of connection you may need and has several interesting built-in
capabilities.

You can find the documentation in
/opt/freeware/share/doc/packages/netcat/README.

Authors:
--------
    hobbit@avian.org


%prep
%setup -q
%patch0

%build

/usr/vac/bin/xlc_r -O -DGAPING_SECURITY_HOLE -DAIX %{name}.c -o %{name}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1

cp %{name} ${RPM_BUILD_ROOT}%{_bindir}/%{name}
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/%{name}
ln -sf 'netcat' ${RPM_BUILD_ROOT}%{_bindir}/nc

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,755)
%doc Changelog
%doc README
%doc data
%doc scripts
%{_bindir}/*
%{_mandir}/man1/*
/usr/bin/*


%changelog -n netcat
* Wed Mar 13 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-1
- Initial port on Aix 6.1
