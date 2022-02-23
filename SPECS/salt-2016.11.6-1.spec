%global with_explicit_python27 1
%global pybasever 2.7
# __python_ver Could be 3 if/when ported to Python 3.5/3.6/...
%global __python %{_bindir}/python%{?pybasever}
%global __python2 %{_bindir}/python%{?pybasever}

%global python2_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
%global python2_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%{!?pythonpath: %global pythonpath %(%{__python} -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

# Following not recognised by setup.py
# %global __inst_layout --install-layout=unix


%global include_tests 0
# The tests are performed by default
# rpm -ba --define 'dotests 0' salt-2016.11.2-1.spec ...
%{!?dotests:%define include_tests 1}
%{?dotests:%define include_tests 0}


%define fish_dir %{_datadir}/fish/vendor_functions.d

%define _salttesting SaltTesting
%define _salttesting_ver 2016.10.26

Name: salt
Version: 2016.11.6
Release: 1
Summary: A parallel remote execution system

Group:   System Environment/Daemons
License: ASL 2.0
URL:     http://saltstack.org/
Source0: https://pypi.io/packages/source/s/%{name}/%{name}-%{version}.tar.gz
Source1: https://pypi.io/packages/source/S/%{_salttesting}/%{_salttesting}-%{_salttesting_ver}.tar.gz
Source2: %{name}-master
Source3: %{name}-syndic
Source4: %{name}-minion
Source5: %{name}-api
# Source6: %{name}-master.service
# Source7: %{name}-syndic.service
# Source8: %{name}-minion.service
# Source9: %{name}-api.service
Source10: salt_README.aix
Source11: %{name}-common.logrotate
Source12: salt.bash
Source13: salt.fish
Source14: salt_common.fish
Source15: salt-call.fish
Source16: salt-cp.fish
Source17: salt-key.fish
Source18: salt-master.fish
Source19: salt-minion.fish
Source20: salt-run.fish
Source21: salt-syndic.fish
# Source22: %{name}-proxy@.service

## Patch0:  salt-%%{version}-tests.patch
## Patch0:  salt-%{version}-fix-nameserver.patch


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# man files are in /opt/freeware/share
%global _mandir /opt/freeware/share/man
# service start/stop scripts are in /etc
%global _initrddir /etc/rc.d/init.d

# Requires: pciutils
# Requires: which
Requires: yum-utils


# %if ( 0%{?include_tests} )
%if %{include_tests}
BuildRequires: python-tornado >= 4.2.1
BuildRequires: python-futures >= 2.0
BuildRequires: python-pycrypto >= 2.6.1
BuildRequires: python-jinja2
BuildRequires: python-msgpack > 0.3
BuildRequires: python-pip
# BuildRequires: python-zmq
BuildRequires: zeromq
BuildRequires: python-PyYAML
BuildRequires: python-requests
BuildRequires: python-unittest2
# this BR causes windows tests to happen
# clearly, that's not desired
# https://github.com/saltstack/salt/issues/3749
BuildRequires: python-mock
BuildRequires: git
BuildRequires: python-libcloud
BuildRequires: python-six

# argparse now a salt-testing requirement
BuildRequires: python-argparse


BuildRequires: python%{?__python_ver}-devel
Requires: python%{?__python_ver}-pycrypto >= 2.6.1
Requires: python%{?__python_ver}-jinja2
Requires: python%{?__python_ver}-msgpack > 0.3
# %if ( "0%{?dist}" == "0.amzn1" )
# Requires: python27-PyYAML
# %else
Requires: python-PyYAML
# %endif
Requires: python%{?__python_ver}-requests >= 1.0.0
# Requires: python%{?__python_ver}-zmq
Requires: zeromq
Requires: python%{?__python_ver}-markupsafe
Requires: python%{?__python_ver}-tornado >= 4.2.1
Requires: python%{?__python_ver}-futures >= 2.0
Requires: python%{?__python_ver}-six

%endif

%description
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.

%package master
Summary: Management component for salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}

%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name}-master = %{version}-%{release}

%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name}-master = %{version}-%{release}
Requires: python%{?__python_ver}-cherrypy


%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name}-master = %{version}-%{release}
Requires: python%{?__python_ver}-libcloud

%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   Applications/System
Requires: %{name} = %{version}-%{release}

%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%prep
%setup -q -c
%setup -q -T -D -a 1

cd %{name}-%{version}
## %patch0 -p1

%build


%install
rm -rf %{buildroot}
cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
# %{__python} setup.py install -O1 %{?__inst_layout } --root %{buildroot}
%{__python} setup.py install -O1  --root %{buildroot}

# Add some directories
install -d -m 0755 %{buildroot}%{_var}/log/salt
touch %{buildroot}%{_var}/log/salt/minion
touch %{buildroot}%{_var}/log/salt/master
install -d -m 0755 %{buildroot}%{_var}/cache/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/master.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/minion.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki/master
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki/minion
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.providers.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/proxy.d

# Add the config files
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/salt/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/salt/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/salt/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/salt/roster
install -p -m 0640 conf/proxy %{buildroot}%{_sysconfdir}/salt/proxy

# %if ! (0%{?rhel} >= 7 || 0%{?fedora} >= 15)
mkdir -p %{buildroot}%{_initrddir}
install -p %{SOURCE2} %{buildroot}%{_initrddir}/
install -p %{SOURCE3} %{buildroot}%{_initrddir}/
install -p %{SOURCE4} %{buildroot}%{_initrddir}/
install -p %{SOURCE5} %{buildroot}%{_initrddir}/
# %else
# Add the unit files
# mkdir -p %{buildroot}%{_unitdir}
# install -p -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/
# install -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/
# install -p -m 0644 %{SOURCE8} %{buildroot}%{_unitdir}/
# install -p -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/
# %endif


# Logrotate
install -p %{SOURCE10} .
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/logrotate.d/salt

# Bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/bash_completion.d/salt.bash

# Fish completion (TBD remove -v)
mkdir -p %{buildroot}%{fish_dir}
install -p -m 0644  %{SOURCE13} %{buildroot}%{fish_dir}/salt.fish
install -p -m 0644  %{SOURCE14} %{buildroot}%{fish_dir}/salt_common.fish
install -p -m 0644  %{SOURCE15} %{buildroot}%{fish_dir}/salt-call.fish
install -p -m 0644  %{SOURCE16} %{buildroot}%{fish_dir}/salt-cp.fish
install -p -m 0644  %{SOURCE17} %{buildroot}%{fish_dir}/salt-key.fish
install -p -m 0644  %{SOURCE18} %{buildroot}%{fish_dir}/salt-master.fish
install -p -m 0644  %{SOURCE19} %{buildroot}%{fish_dir}/salt-minion.fish
install -p -m 0644  %{SOURCE20} %{buildroot}%{fish_dir}/salt-run.fish
install -p -m 0644  %{SOURCE21} %{buildroot}%{fish_dir}/salt-syndic.fish


%preun master
# Stop salt-master process
  # if [ $1 -eq 0 ] ; then
  #     /sbin/service salt-master stop >/dev/null 2>&1
  #     /sbin/chkconfig --del salt-master
  # fi
  # if [ $1 -eq 0 ] ; then
  #     %{_initrddir}/salt-master stop >/dev/null 2>&1
  # fi

%preun syndic
# Stop salt-syndic process
  # if [ $1 -eq 0 ] ; then
  #     /sbin/service salt-syndic stop >/dev/null 2>&1
  #     /sbin/chkconfig --del salt-syndic
  # fi
  # if [ $1 -eq 0 ] ; then
  #     %{_initrddir}/salt-syndic stop >/dev/null 2>&1
  # fi

%preun minion
# Stop salt-minion process
  # if [ $1 -eq 0 ] ; then
  #     /sbin/service salt-minion stop >/dev/null 2>&1
  #     /sbin/chkconfig --del salt-minion
  # fi
  # if [ $1 -eq 0 ] ; then
  #     %{_initrddir}/salt-minion stop >/dev/null 2>&1
  # fi

%post master
test ! -e /etc/salt && ln -s %{_sysconfdir}/salt /etc/salt
# Launch salt-master process
  # /sbin/chkconfig --add salt-master
  # %{_initrddir}/salt-master start >/dev/null 2>&1

%post minion
test ! -e /etc/salt && ln -s %{_sysconfdir}/salt /etc/salt
# Launch salt-minion process
  # /sbin/chkconfig --add salt-minion
  # %{_initrddir}/salt-minion start >/dev/null 2>&1

%postun master
  # if [ "$1" -ge "1" ] ; then
  #     /sbin/service salt-master condrestart >/dev/null 2>&1 || :
  # fi
  # if [ "$1" -ge "1" ] ; then
  #     %{_initrddir}/salt-master condrestart >/dev/null 2>&1 || :
  # fi

#%%postun syndic
#  if [ "$1" -ge "1" ] ; then
#      /sbin/service salt-syndic condrestart >/dev/null 2>&1 || :
#  fi
#  if [ "$1" -ge "1" ] ; then
#      %{_initrddir}/salt-syndic condrestart >/dev/null 2>&1 || :
#  fi

%postun minion
  # if [ "$1" -ge "1" ] ; then
  #     /sbin/service salt-minion condrestart >/dev/null 2>&1 || :
  # fi
  # if [ "$1" -ge "1" ] ; then
  #     %{_initrddir}/salt-minion condrestart >/dev/null 2>&1 || :
  # fi


# %if ( 0%{?include_tests} )
# %if %{include_tests}
# %check
# cd $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}
# mkdir %{_tmppath}/salt-test-cache
# PYTHONPATH=%{pythonpath}:$RPM_BUILD_DIR/%{name}-%{version}/%{_salttesting}-%{_salttesting_ver} %{__python} setup.py test --runtests-opts=-u
# %endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/LICENSE
%{python2_sitelib}/%{name}/*
%{python2_sitelib}/%{name}-%{version}-py?.?.egg-info

%{_sysconfdir}/logrotate.d/salt
%{_sysconfdir}/bash_completion.d/salt.bash
%{_var}/cache/salt
%{_var}/log/salt
%doc $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{version}/salt_README.aix
%{_bindir}/spm
%doc %{_mandir}/man1/spm.1*
# %config(noreplace) %{_sysconfdir}/salt/
# %config(noreplace) %{_sysconfdir}/salt/pki
# %config(noreplace) %{fish_dir}/salt*.fish

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7*
%doc %{_mandir}/man1/salt.1*
%doc %{_mandir}/man1/salt-cp.1*
%doc %{_mandir}/man1/salt-key.1*
%doc %{_mandir}/man1/salt-master.1*
%doc %{_mandir}/man1/salt-run.1*
%doc %{_mandir}/man1/salt-unity.1*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_bindir}/salt-unity
%attr(0755, root, root) /%{_initrddir}/salt-master

%config(noreplace) %{_sysconfdir}/salt/master
%config(noreplace) %{_sysconfdir}/salt/master.d
%config(noreplace) %{_sysconfdir}/salt/pki/master
%config(noreplace) %{_var}/log/salt/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1*
%doc %{_mandir}/man1/salt-minion.1*
%doc %{_mandir}/man1/salt-proxy.1*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%{_bindir}/salt-proxy
%attr(0755, root, root) /%{_initrddir}/salt-minion

%config(noreplace) %{_sysconfdir}/salt/minion
%config(noreplace) %{_sysconfdir}/salt/proxy
%config(noreplace) %{_sysconfdir}/salt/minion.d
%config(noreplace) %{_sysconfdir}/salt/pki/minion
%config(noreplace) %{_var}/log/salt/minion

%files syndic
%doc %{_mandir}/man1/salt-syndic.1*
%{_bindir}/salt-syndic
%attr(0755, root, root) /%{_initrddir}/salt-syndic

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1*
%{_bindir}/salt-api
%attr(0755, root, root) /%{_initrddir}/salt-api

%files cloud
%doc %{_mandir}/man1/salt-cloud.1*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%doc %{_mandir}/man1/salt-ssh.1*
%{_bindir}/salt-ssh
%config(noreplace) %{_sysconfdir}/salt/roster




%changelog
* Wed Feb 01 2017 Michael Wilson <michael.a.wilson@atos.net> - 2016.11.2-1
- Initial version

