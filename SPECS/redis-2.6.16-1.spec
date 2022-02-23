Name:             redis
Version:          2.6.16
Release:          1
Summary:          A persistent key-value database
Group:            Applications/Databases
License:          BSD
URL:              http://redis.io/
Source0:          http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
Patch0:           %{name}-%{version}-aix.patch
Patch1:           %{name}-%{version}-AIX_hz.patch
# update configuration for Fedora
Patch2:           %{name}-2.6.7-redis.conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:    gcc >= 4.2.3-2
BuildRequires:    patch, make
BuildRequires:    AIX-rpm >= 5.2.0.0
Requires:         AIX-rpm >= 5.2.0.0
Requires:         logrotate

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch0
%patch1
%patch2 -p1


%build
export CC='gcc'
export CFLAGS='-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX52 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include'
export LDFLAGS='-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000'
gmake %{?_smp_mflags} CC="${CC}" DEBUG="" CCLINK="-Wl,-bmaxdata:0x80000000 -lm -lpthread" all


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export CC='gcc -D_LARGE_FILES=1'
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX52 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
gmake install PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
    CC="${CC}" DEBUG="" CCLINK="-Wl,-bmaxdata:0x80000000 -lm -lpthread"

# Ensure redis-server location doesn't change
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mv ${RPM_BUILD_ROOT}%{_bindir}/%{name}-server ${RPM_BUILD_ROOT}%{_sbindir}/%{name}-server

# strip binaries
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_sbindir}/* || :

# install misc other
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp %{name}.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}.conf
chmod 0644 %{name}.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}.conf

mkdir -p ${RPM_BUILD_ROOT}/var/lib/%{name}
chmod 0755 ${RPM_BUILD_ROOT}/var/lib/%{name}

mkdir -p ${RPM_BUILD_ROOT}/var/log/%{name}
chmod 0755 ${RPM_BUILD_ROOT}/var/log/%{name}

mkdir -p ${RPM_BUILD_ROOT}/var/run/%{name}
chmod 0755 ${RPM_BUILD_ROOT}/var/run/%{name}

# create the /etc/rc.d/init.d/ scripts and symlinks
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d
cp %{SOURCE2} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/%{name}
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/%{name}

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/
ln -sf '../init.d/redis' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/S%{name}
ln -sf '../init.d/redis' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/K%{name}
ln -sf '../init.d/redis' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/S%{name}
ln -sf '../init.d/redis' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/K%{name}

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%preun
if [ $1 = 0 ] ; then
    /etc/rc.d/init.d/%{name} stop > /dev/null 2>&1
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 00-RELEASENOTES BUGS COPYING README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %attr(0755,root,system) /var/lib/%{name}
%dir %attr(0755,root,system) /var/log/%{name}
%dir %attr(0755,root,system) /var/run/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
/etc/rc.d/init.d/%{name}
/etc/rc.d/rc?.d/?%{name}
/usr/bin/%{name}-*
/usr/sbin/%{name}-*


%changelog
* Tue Nov 12 2013 Michael Perzl <michael@perzl.org> - 2.6.16-1
- updated to version 2.6.16

* Mon Jun 24 2013 Michael Perzl <michael@perzl.org> - 2.6.14-1
- updated to version 2.6.14

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 2.6.13-1
- updated to version 2.6.13

* Thu Apr 04 2013 Michael Perzl <michael@perzl.org> - 2.6.12-1
- updated to version 2.6.12

* Thu Apr 04 2013 Michael Perzl <michael@perzl.org> - 2.6.7-1
- updated to version 2.6.7

* Thu Apr 04 2013 Michael Perzl <michael@perzl.org> - 2.4.18-1
- updated to version 2.4.18

* Thu Apr 04 2013 Michael Perzl <michael@perzl.org> - 2.4.17-1
- updated to version 2.4.17

* Tue Jun 12 2012 Michael Perzl <michael@perzl.org> - 2.4.14-1
- updated to version 2.4.14

* Thu Apr 19 2012 Michael Perzl <michael@perzl.org> - 2.4.11-1
- updated to version 2.4.11

* Mon Nov 21 2011 Michael Perzl <michael@perzl.org> - 2.4.2-1
- updated to version 2.4.2

* Mon Nov 21 2011 Michael Perzl <michael@perzl.org> - 2.2.15-1
- updated to version 2.2.15

* Thu Jul 07 2011 Michael Perzl <michael@perzl.org> - 2.2.11-1
- updated to version 2.2.11

* Mon Nov 29 2010 Michael Perzl <michael@perzl.org> - 2.0.4-1
- first version for AIX V5.1 and higher
