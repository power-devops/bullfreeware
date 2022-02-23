Summary: Rotates, compresses, removes and mails system log files
Name: logrotate
Version: 3.8.3
Release: 1
License: GPL+
Group: System Environment/Base
Source0: https://fedorahosted.org/releases/l/o/%{name}/%{name}-%{version}.tar.gz
Patch0: %{name}-3.8.2-aix.patch
Patch1: %{name}-aix-missing-asprintf.patch
Patch2: %{name}-aix-missing-vasprintf.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: popt, make, patch
Requires: coreutils, popt

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.  Normally,
logrotate runs as a daily cron job.

Install the logrotate package if you need a utility to deal with the
log files on your system.


%prep
%setup -q
PATH=/opt/freeware/bin:$PATH
%patch0
%patch1
%patch2


%build
export LIBPATH="/opt/freeware/lib:/usr/lib"
export RPM_OPT_FLAGS="-O" CFLAGS="-qlanglv=extended"
gmake %{?_smp_mflags}


%install
export PATH=/opt/freeware/bin:$PATH
rm -f .depend

gmake PREFIX=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib

install -p -m 644 examples/logrotate-default ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.conf
install -p -m 755 examples/logrotate.cron ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/logrotate
touch ${RPM_BUILD_ROOT}%{_localstatedir}/lib/logrotate.status

cd ${RPM_BUILD_ROOT}
mkdir -p usr/sbin
cd usr/sbin
ln -sf ../..%{_sbindir}/* .


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGES COPYING
%attr(0755,root,system) %{_sbindir}/logrotate
%attr(0644,root,system) %{_mandir}/man8/logrotate.8*
%attr(0644,root,system) %{_mandir}/man5/logrotate.conf.5*
%attr(0755,root,system) %{_sysconfdir}/cron.daily/logrotate
%attr(0644,root,system) %config(noreplace) %{_sysconfdir}/logrotate.conf
%attr(0755,root,system) %dir %{_sysconfdir}/logrotate.d
%attr(0644,root,system) %verify(not size md5 mtime) %config(noreplace) %{_localstatedir}/lib/logrotate.status
/usr/sbin/*


%changelog
* Wed Nov 20 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.8.3-1
- Update to version 3.8.3

* Tue Nov 19 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.8.2-2
- Built on Aix6.1

* Mon Aug 13 2012 Michael Perzl <michael@perzl.org> - 3.8.2-1
- updated to version 3.8.2

* Tue Apr 12 2012 Michael Perzl <michael@perzl.org> - 3.8.1-2
- add missing mbrtowc patch again

* Fri Dec 23 2011 Michael Perzl <michael@perzl.org> - 3.8.1-1
- updated to version 3.8.1

* Mon Aug 29 2011 Michael Perzl <michael@perzl.org> - 3.7.9-2
- add missing mbrtowc patch again

* Thu Dec 02 2010 Michael Perzl <michael@perzl.org> - 3.7.9-1
- updated to version 3.7.9

* Tue Oct 20 2009 Jeremy W. Chalfant <jeremy.w.chalfant@spiritaero.com> - 3.7.8-3
- added -D_LARGE_FILES to CFLAGS in support of rotating files larger than 2GB
  and changed c compiler from xlc to cc as it gave "Initializer must be a
  valid constant expression" errors

* Fri Jun 26 2009 Michael Perzl <michael@perzl.org> - 3.7.8-2
- included olddir option fix

* Wed Jun 17 2009 Michael Perzl <michael@perzl.org> - 3.7.8-1
- updated to version 3.7.8

* Tue Jun 24 2008 Michael Perzl <michael@perzl.org> - 3.7.7-1
- first version for AIX V5.1 and higher
