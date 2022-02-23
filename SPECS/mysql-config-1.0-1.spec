
# No tests
%bcond_without dotests

Name:           mysql-config
Version:        1.0
Release:        1
Summary:        Development files for mariadb-connector-c
Group:          config
License:        LGPLv2+
BuildArch:      noarch
Source:         mysql-config-%version.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

Obsoletes:      mariadb-connector-c-config <= 3.1.4
Obsoletes:      community-mysql-config     <= 8.0.17


%description
This package delivers /etc/my.cnf that includes other configuration files
from the /etc/my.cnf.d directory and ships this directory as well.
Other packages should only put their files into /etc/my.cnf.d directory
and require this package, so the /etc/my.cnf file is present.


%prep
%setup -q


%build
# No build


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%check
%if %{with dotests}
# No check
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Install config files
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf.d/
install -D -p -m 0644 my.cnf                   ${RPM_BUILD_ROOT}%{_sysconfdir}/
install -D -p -m 0644 client.cnf               ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf.d/
install -D -p -m 0644 mysql_client.cnf         ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf.d/
install -D -p -m 0644 server.cnf               ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf.d/
install -D -p -m 0644 enable_encryption.preset ${RPM_BUILD_ROOT}%{_sysconfdir}/my.cnf.d/

# /etc/my.cnf(.d) is /opt/freeware/my.cnf(.d)
mkdir ${RPM_BUILD_ROOT}/etc
ln -s %{_sysconfdir}/my.cnf.d ${RPM_BUILD_ROOT}/etc/my.cnf.d
ln -s %{_sysconfdir}/my.cnf   ${RPM_BUILD_ROOT}/etc/my.cnf


%files
%dir %{_sysconfdir}/my.cnf.d
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/*
%config(noreplace) /etc/my.cnf
%config(noreplace) /etc/my.cnf.d

%changelog
* Tue Oct 29 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> - 1.0-1
- Package creation.
