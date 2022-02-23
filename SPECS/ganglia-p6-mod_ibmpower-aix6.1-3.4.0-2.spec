Summary: Ganglia Monitor daemon module ibmpower
Name: ganglia-p6-mod_ibmpower
Version: 3.4.0
URL: http://ganglia.info/
Release: 2
License: BSD
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base

Source0: ganglia-%{version}.tar.gz

Patch0: ganglia-%{version}-aix.patch
Patch1: ganglia-%{version}-aix2.patch
Patch2: ganglia-%{version}-%{release}-mod_ibmpower.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: AIX-rpm >= 6.1.0.0
BuildRequires: apr-devel >= 1.3.12
BuildRequires: libconfuse-devel
BuildRequires: expat-devel >= 2.0.0
BuildRequires: patch, make, autoconf, automake, libtool, m4

Requires: AIX-rpm >= 6.1.0.0
Requires: ganglia-lib = %{version}
Requires: ganglia-gmond = %{version}

Conflicts: ganglia-mod_ibmpower

%define conf_dir /etc/ganglia

%description
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond module provides POWER5 and POWER6 specific metrics on AIX.


##
## PREP
##
%prep 
%setup -q -n ganglia-%{version}
export PATH=/opt/freeware/bin:$PATH
# apply all necessary AIX patches
%patch0
%patch1
# apply the patch for the mod_ibmpower module
%patch2


##
## BUILD
##
%build
export CONFIG_SHELL=/usr/bin/sh
export APR_CONFIG=/opt/freeware/bin/apr-1-config
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r -U_AIX43 -DPOWER6_POOLS"
export CFLAGS="${CFLAGS} -I/opt/freeware/include/apr-1"
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-brtl"
autoreconf -fiv
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{conf_dir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --without-gmetad \
    --disable-python
gmake %{?_smp_mflags}


##
## INSTALL
##
%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

## Create the directory structure
%__mkdir -p ${RPM_BUILD_ROOT}%{conf_dir}/conf.d

## Move the files into the structure
%__cp -f gmond/modules/conf.d/* ${RPM_BUILD_ROOT}%{conf_dir}/conf.d

cp gmond/modules/ibmpower/.libs/modibmpower.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia


##
## CLEAN
##
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


##
## FILES
##
%files
%defattr(-,root,system)
%{_libdir}/ganglia/modibmpower.so
%config(noreplace) %{conf_dir}/conf.d/ibmpower.conf


##
## CHANGELOG
##
%changelog
* Fri Jul 27 2012 Patricia Cugny <patricia.cugny@bull.net> - 3.4.0-2
- built on AIX6.1

* Mon May 28 2012 Michael Perzl <michael@perzl.org> - 3.4.0-1
- updated to version 3.4.0

* Fri May 25 2012 Michael Perzl <michael@perzl.org> - 3.3.7-2
- adapted some settings in ibmpower.conf

* Sun May 06 2012 Michael Perzl <michael@perzl.org> - 3.3.7-1
- updated to version 3.3.7

* Fri Apr 20 2012 Michael Perzl <michael@perzl.org> - 3.3.6-1
- updated to version 3.3.6

* Wed Apr 11 2012 Michael Perzl <michael@perzl.org> - 3.3.5-1
- updated to version 3.3.5

* Thu Feb 09 2012 Michael Perzl <michael@perzl.org> - 3.3.1-1
- updated to version 3.3.1

* Thu Feb 09 2012 Michael Perzl <michael@perzl.org> - 3.2.0-2
- added cpu_pool_id metric

* Thu Oct 13 2011 Michael Perzl <michael@perzl.org> - 3.2.0-1
- updated to version 3.2.0

* Thu Oct 13 2011 Michael Perzl <michael@perzl.org> - 3.1.7-3
- changed collection times for cpu_used and cpu_pool_idle

* Thu Sep 02 2010 Michael Perzl <michael@perzl.org> - 3.1.7-2
- updated to version 3.1.7

* Thu Sep 02 2010 Michael Perzl <michael@perzl.org> - 3.1.2-6
- first version for AIX V5.1 and higher to build as a standalone module
