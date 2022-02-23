%define sbindir /sbin

Name:             syslog-ng
Version:          3.2.5
Release:          2
Summary:          Next generation system logging daemon

Group:            System Environment/Daemons
License:          GPL
URL:              http://www.balabit.com/products/syslog_ng/
Source0:	  http://www.balabit.com/downloads/files/%{name}/open-source-edition/%{version}/source/%{name}_%{version}.tar.gz
Patch0:           %{name}_%{version}-aix.patch
Patch1:           %{name}_%{version}-aixconffile.patch
BuildRoot:        /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires:    flex, make
BuildRequires:    glib2-devel >= 2.22.5
BuildRequires:    eventlog-devel >= 0.2.12
BuildRequires:    openssl-devel >= 0.9.8
BuildRequires:    pcre-devel >= 7.9

Requires:         glib2 >= 2.22.5
Requires:         eventlog >= 0.2.12
Requires:         openssl >= 0.9.8
Requires:         pcre >= 7.9

Provides:         syslog

%description
syslog-ng, as the name shows, is a syslogd replacement, but with new
functionality for the new generation. The original syslogd allows
messages only to be sorted based on priority/facility pairs; syslog-ng
adds the possibility to filter based on message contents using regular
expressions. The new configuration scheme is intuitive and powerful.
Forwarding logs over TCP and remembering all forwarding hops makes it
ideal for firewalled environments.


%prep
%setup -q
%patch0 -p1 -b .aix
%patch1 -p1 -b .aixconffile

# fake a <stdbool.h> as AIX5L V5.1 and XLC/C++ V7 doesn't have one
cat > stdbool.h << EOF
#ifndef stdbool_h_wrapper
#define stdbool_h_wrapper

typedef enum {false = 0, true = 1} bool;

#endif
EOF

cat contrib/relogger.pl | \
%{__sed} -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' contrib/relogger.pl > contrib/relogger.new
mv contrib/relogger.new contrib/relogger.pl
chmod a+x contrib/relogger.pl
chmod a+x contrib/syslog2ng


%build
export CC="/usr/vac/bin/xlc_r"
export CFLAGS="-O"
./configure \
    --prefix=%{_prefix} \
    --sbindir=%{sbindir} \
    --datadir=%{_datadir}/%{name} \
    --mandir=%{_mandir} \
    --sysconfdir=/etc/%{name} \
    --localstatedir=/var/lib/%{name} \
    --disable-spoof-source \
    --enable-dynamic-linking
cd lib
make
cd ..
cd modules
make LIBS="-L%{_libdir} -lglib-2.0 -levtlog ../../lib/libsyslog-ng.la"
cd ..
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# strip the binaries/ libraries
strip ${RPM_BUILD_ROOT}/%{sbindir}/%{name}
./install-sh -d ${RPM_BUILD_ROOT}/etc/%{name}

./install-sh -o root -g bin -m 0644 contrib/aix-packaging/%{name}.conf \
    ${RPM_BUILD_ROOT}/etc/%{name}/%{name}.conf

(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
      /usr/bin/ar -X32 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}/%{name}
  for f in *.a ; do
      /usr/bin/ar -X32 -x ${f}
  done
)


#
# Post-Installation
#

%post
[ -d /var/lib/syslog-ng ] || mkdir -p /var/lib/syslog-ng
printf "Checking whether the syslog-ng service is already registered... "
if ! /usr/bin/lssrc -s syslogng >/dev/null 2>&1; then
    echo "NO"
    printf "Registering syslog-ng service... "
    if /usr/bin/mkssys -s syslogng -p /sbin/syslog-ng -u 0 \
            -a '-F -p /etc/syslog-ng.pid' -O -d -Q -S -n 15 -f 9 -E 20 -G ras -w 2 \
            >/dev/null 2>&1; then
        echo "SUCCESSFUL"
    else
        echo "FAILED"
    fi
else
    echo "YES"
fi

printf "Checking whether the syslogd service is registered..."
if /usr/bin/lssrc -s syslogd >/dev/null 2>&1; then
    echo "YES"
    if /usr/bin/lssrc -s syslogd|grep -E "^ syslogd.*active" > /dev/null 2>&1; then
        printf "Stopping the syslogd service... "
        if /usr/bin/stopsrc -s syslogd >/dev/null 2>&1; then
            echo "SUCCESSFUL"
        else
            echo "FAILED, continuing anyway"
        fi
    fi
    printf "Disabling syslogd service... "
    if /usr/bin/rmssys -s syslogd >/dev/null 2>&1; then
        echo "SUCCESSFUL"
    else
        echo "FAILED"
    fi
else
    echo "NO"
fi

if /usr/bin/lssrc -s syslogng|grep -E "^ syslogng.*active" >/dev/null 2>&1; then
    echo "Stopping syslog-ng"
    /usr/bin/stopsrc -s syslogng
fi
echo "Starting syslog-ng"
/usr/bin/startsrc -s syslogng


#
# Pre-Uninstallation
#

%preun
if /usr/bin/lssrc -s syslogng >/dev/null 2>&1; then
    if /usr/bin/lssrc -s syslogng|grep -E "^ syslogng.*active" > /dev/null 2>&1; then
        echo "Stopping syslog-ng"
        /usr/bin/stopsrc -s syslogng
    fi
    printf "Unregistering syslog-ng... "
    if /usr/bin/rmssys -s syslogng >/dev/null 2>&1; then
        echo "SUCCESSFUL"
    else
        echo "FAILED"
    fi
fi
[ -d /var/lib/syslog-ng ] && rm -rf /var/lib/syslog-ng
# re-enable the standard syslogd subsystem
#subsysname:synonym:cmdargs:path:uid:auditid:standin:standout:standerr:action:multi:contact:svrkey:svrmtype:priority:sig norm:sigforce:display:waittime:grpname:
# syslogd:::/usr/sbin/syslogd:0:0:/dev/console:/dev/console:/dev/console:-O:-Q:-K:0:0:20:0:0:-d:20:ras:

if ! /usr/bin/lssrc -s syslogd >/dev/null 2>&1; then
    printf "Registering syslogd service... "
    if /usr/bin/mkssys -s syslogd -p /usr/sbin/syslogd -u 0 -O -Q -K -E 20 -d -G ras >/dev/null 2>&1; then
        echo "SUCCESSFUL"
    else
        echo "FAILED"
    fi
fi

if /usr/bin/lssrc -s syslogd >/dev/null 2>&1; then
    if ! /usr/bin/lssrc -s syslogd | grep -E "^ syslogd.*active" >/dev/null 2>&1; then
        echo "Starting syslogd"
        /usr/bin/startsrc -s syslogd
    fi
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%doc doc/security/*.txt
%doc contrib/relogger.pl
%doc contrib/syslog2ng
%doc contrib/%{name}.conf.doc
%{_bindir}/loggen
%{_bindir}/pdbtool
%{_bindir}/update-patterndb
%{sbindir}/%{name}
%{sbindir}/%{name}-ctl
%dir /etc/%{name}
%config(noreplace) /etc/%{name}/modules.conf
%config(noreplace) /etc/%{name}/scl.conf
%config(noreplace) /etc/%{name}/%{name}.conf
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*


%changelog
* Thu Jan 05 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 3.2.5-2
- Insert version number into configuration file

* Wed Jan 04 2012 Gerard Visiedo <gerard.visiedo@bull.net> -  3.2.5-1
- Initial port on Aix5.3
