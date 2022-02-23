Summary: Ganglia Web Frontend
Name: ganglia-web
Version: 3.4.2
URL: http://ganglia.info
Release: 1
License: BSD
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: %{name}-%{version}.tar.gz
Source1: conf.php
Buildroot: %{_tmppath}/%{name}-%{version}-buildroot
Obsoletes: ganglia-webfrontend
Requires: php >= 5.2
%define web_prefixdir  /opt/freeware/apache2/htdocs/ganglia
BuildArch: noarch

%description
This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP5 language and uses the Dwoo templating engine.

%prep
%setup -n %{name}-%{version}

%build
# nothing to be done here

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%{__mkdir} -p $RPM_BUILD_ROOT/%{web_prefixdir}
%{__cp} -rf * $RPM_BUILD_ROOT/%{web_prefixdir}
# custom conf.php: no authentification set and default metrics set to cpu_used
%{__cp} -f %{SOURCE1}  $RPM_BUILD_ROOT/%{web_prefixdir}
%{__rm} -rf $RPM_BUILD_ROOT/%{web_prefixdir}/conf


%{__mkdir} -p ${RPM_BUILD_ROOT}/var/lib/ganglia/filters
%{__chmod} 0755 ${RPM_BUILD_ROOT}/var/lib/ganglia/filters
%{__chown} nobody.nobody ${RPM_BUILD_ROOT}/var/lib/ganglia/filters
%{__mkdir} -p ${RPM_BUILD_ROOT}/var/lib/ganglia/conf
%{__chmod} 0755 ${RPM_BUILD_ROOT}/var/lib/ganglia/conf
%{__chown} nobody.nobody ${RPM_BUILD_ROOT}/var/lib/ganglia/conf
%{__cp} -rf conf/* $RPM_BUILD_ROOT/var/lib/ganglia/conf

%{__mkdir} -p ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo
%{__chmod} 0755 ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo
%{__chown} nobody.nobody ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo

%{__mkdir} -p ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/compiled
%{__chmod} 0755 ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/compiled
%{__chown} nobody.nobody ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/compiled

%{__mkdir} -p ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/cache
%{__chmod} 0755 ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/cache
%{__chown} nobody.nobody ${RPM_BUILD_ROOT}/var/lib/ganglia/dwoo/cache


%files
%defattr(-,root,system)
%attr(0755,nobody,nobody)/var/lib/ganglia/filters
%attr(0755,nobody,nobody) %dir /var/lib/ganglia/conf
%attr(0755,nobody,nobody) %dir /var/lib/ganglia/dwoo
%attr(0755,nobody,nobody)/var/lib/ganglia/dwoo/compiled
%attr(0755,nobody,nobody)/var/lib/ganglia/dwoo/cache
%{web_prefixdir}/*
/var/lib/ganglia/conf/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Thu May 24 2012 Patricia Cugny <patricia.cugny@bull.net> - 3.4.2-1
- built for AIX 6.1

* Thu Mar 17 2011 Bernard Li <bernard@vanhpc.org>
- Renamed conf.php -> conf_default.php
* Fri Dec 17 2010 Bernard Li <bernard@vanhpc.org>
- Spec file for gweb which is split from ganglia-web subpackage
