%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: Ganglia Distributed Monitoring System
Name: ganglia
Version: 3.7.2
URL: http://ganglia.info/
Release: 3
License: BSD
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base

Source0: %{name}-%{version}.tar.gz
Source1: %{name}-%{version}-gmond.conf
Source2: gmetad.aix.init
Source3: gmond.aix.init

Source10: %{name}-aix-metrics-20130712.c
Source1000: %{name}-%{version}-%{release}.build.log 

Patch0: %{name}-%{version}-2-aix.patch

Patch1: %{name}-%{version}-register.patch
# Patch2: %{name}-%{version}-gmetad.patch

BuildRequires: apr-devel >= 1.7.0
BuildRequires: expat-devel 
BuildRequires: glib2-devel
BuildRequires: libconfuse-devel
BuildRequires: pcre-devel >= 8.43-2
BuildRequires: python-devel
BuildRequires: rrdtool-devel
BuildRequires: zlib-devel
BuildRequires: patch, autoconf, automake, libtool, m4
BuildRequires: compat-getopt-devel

%define conf_dir /etc/%{name}

%description
Ganglia is a scalable, real-time monitoring and execution environment


%package libs
Summary: Ganglia Meta daemon http://ganglia.sourceforge.net/
Group: System Environment/Base

Requires: apr >= 1.7.0
Requires: expat
Requires: libconfuse
Requires: pcre >= 8.43-2
Requires: libgcc
Requires: compat-getopt
# Standard is -libs, but old version of ganglia used -lib
Provides: %{name}-lib
Obsoletes: %{name}-lib

%description libs
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

The Ganglia shared libraries contain common libraries required by both gmond
and gmetad packages.


%package gmetad
Summary: Ganglia Meta daemon http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: ganglia-monitor-core-gmetad < %{version}
Obsoletes: ganglia-monitor-core < %{version}
Provides: ganglia-monitor-core-gmetad = %{version}
Provides: ganglia-monitor-core = %{version}

Requires: %{name}-libs = %{version}
Requires: glib2
Requires: rrdtool
Requires: zlib
Requires: libdbi
Requires: libffi
Requires: xz-libs
Requires: pango
Requires: libxml2


%description gmetad
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters
to form a monitoring grid. It also keeps metric history using rrdtool.


%package gmond
Summary: Ganglia Monitor daemon http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: ganglia-monitor-core-gmond < %{version}
Obsoletes: ganglia-monitor-core < %{version}
Provides: ganglia-monitor-core-gmond = %{version}
Provides: ganglia-monitor-core = %{version}

Requires: %{name}-libs = %{version}
Requires: zlib

%description gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond daemon provides the ganglia service within a single cluster or
Multicast domain.


%package gmond-python
Summary:  Ganglia Monitor daemon python DSO and metric modules
Group:    System Environment/Base
Requires: ganglia-gmond = %{version}
Requires: python >= 2.7.15

%description gmond-python
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This package provides the gmond python DSO.


%package gmond-python-examples
Summary:  Ganglia Monitor daemon python metric modules (Linux examples)
Group:    System Environment/Base
Requires: ganglia-gmond-python = %{version}

%description gmond-python-examples
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This package provides python gmond modules, which can be loaded via the DSO
at gmond daemon start time.
These modules are Linux-centric so you will have to adapt them to AIX.


%package devel
Summary: Ganglia Library http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: ganglia-monitor-core-lib 

Requires: %{name}-libs = %{version}
Requires: apr-devel >= 1.7.0
Requires: expat-devel
Requires: libconfuse-devel
Requires: pcre-devel >= 8.43-2

%description devel
The Ganglia Monitoring Core library provides a set of functions that
programmers can use to build scalable cluster or grid applications.


##
## PREP
##
%prep 
%setup -q
# use the new libmetrics AIX implementation
cp %{SOURCE10} libmetrics/aix/metrics.c
%patch0
%patch1

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

##
## BUILD
##
%build


# build on 64bit mode
export OBJECT_MODE=64
cd 64bit
#export CC="/usr/vac/bin/xlc_r -U_AIX43 -D_AIX53 -I/opt/freeware/include -q64 -O2"
export CC="/opt/freeware/bin/gcc -U_AIX43 -D_AIX53 -I/opt/freeware/include -maix64 -O2"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lcompat-getopt"
#autoreconf -fiv
#patch -p0 < %{PATCH2}
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --sysconfdir=%{conf_dir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-gmetad \
    --enable-php=no \
    --enable-python
make %{?_smp_mflags}

# build on 32bit mode
export OBJECT_MODE=32
cd ../32bit
#export CC="/usr/vac/bin/xlc_r -U_AIX43 -D_AIX53 -I/opt/freeware/include -O2 -D_LARGE_FILES"
export CC="/opt/freeware/bin/gcc -U_AIX43 -D_AIX53 -I/opt/freeware/include -O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -lcompat-getopt"
#autoreconf -fiv
#patch -p0 < %{PATCH2}
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --sysconfdir=%{conf_dir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-gmetad \
    --enable-php=no \
    --enable-python
make %{?_smp_mflags}

slibclean
/usr/bin/ar -X64 -q lib/.libs/libganglia.a ../64bit/lib/.libs/libganglia.so.0

##
## INSTALL
##
%install

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# install on 64bit mode
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

%__mkdir -p ${RPM_BUILD_ROOT}/var/lib64/ganglia/rrds
%__mkdir -p ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/python_modules

cp -p gmond/python_modules/*/*.py ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/python_modules/

# Remove execute bit
chmod 0644 ${RPM_BUILD_ROOT}%{_libdir64}/%{name}/python_modules/*.py

cp gmond/modules/cpu/.libs/modcpu.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/disk/.libs/moddisk.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/cpu/.libs/modload.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/memory/.libs/modmem.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/network/.libs/modnet.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/system/.libs/modproc.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/system/.libs/modsys.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia
cp gmond/modules/python/.libs/modpython.so ${RPM_BUILD_ROOT}%{_libdir64}/ganglia

# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32

make DESTDIR=${RPM_BUILD_ROOT} install

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/sbin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
    cd ${RPM_BUILD_ROOT}/%{_libdir64}
    ln -sf ../lib/*.a .
)

## Create the directory structure
%__mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
%__mkdir -p ${RPM_BUILD_ROOT}%{conf_dir}
%__mkdir -p ${RPM_BUILD_ROOT}%{conf_dir}/conf.d
%__mkdir -p ${RPM_BUILD_ROOT}/var/lib/ganglia/rrds
%__mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{name}/python_modules

## Move the files into the structure
%__cp -f %{SOURCE2} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gmetad
%__cp -f %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gmond
chmod 0755 $RPM_BUILD_ROOT/etc/rc.d/init.d/gm*
## Copy our modified gmond.conf file
%__cp -f %{SOURCE1} ${RPM_BUILD_ROOT}%{conf_dir}/gmond.conf
%__cp -f %{_builddir}/%{name}-%{version}/32bit/gmond/modules/conf.d/* ${RPM_BUILD_ROOT}%{conf_dir}/conf.d
%__cp -f %{_builddir}/%{name}-%{version}/32bit/gmetad/gmetad.conf ${RPM_BUILD_ROOT}%{conf_dir}/gmetad.conf

## Python bits
# Copy the python metric modules and .conf files
cp -p gmond/python_modules/conf.d/*.pyconf ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/
cp -p gmond/modules/conf.d/*.conf ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/
cp -p gmond/python_modules/*/*.py ${RPM_BUILD_ROOT}%{_libdir}/%{name}/python_modules/

# Remove execute bit
chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/%{name}/python_modules/*.py

# Don't install the example modules
%__rm -f ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/example.conf
%__rm -f ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/example.pyconf

# Don't install the status modules
%__rm -f ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/modgstatus.conf

# Clean up the .conf.in files
%__rm -f ${RPM_BUILD_ROOT}%{conf_dir}/conf.d/*.conf.in

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/
ln -sf '../init.d/gmond' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Sgmond
ln -sf '../init.d/gmond' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Kgmond
ln -sf '../init.d/gmond' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Sgmond
ln -sf '../init.d/gmond' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Kgmond
ln -sf '../init.d/gmetad' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Sgmetad
ln -sf '../init.d/gmetad' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Kgmetad
ln -sf '../init.d/gmetad' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Sgmetad
ln -sf '../init.d/gmetad' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Kgmetad


cp gmond/modules/cpu/.libs/modcpu.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/disk/.libs/moddisk.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/cpu/.libs/modload.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/memory/.libs/modmem.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/network/.libs/modnet.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/system/.libs/modproc.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/system/.libs/modsys.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia
cp gmond/modules/python/.libs/modpython.so ${RPM_BUILD_ROOT}%{_libdir}/ganglia


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
gmake check || true

cd ../32bit
export OBJECT_MODE=32
gmake check || true
%endif


##
## POST GMETAD
##
%post gmetad
if [ "$1" -gt "1" ]; then
   # Upgrading ganglia package - restart gmetad
      echo "Type '/etc/rc.d/init.d/gmetad restart' to restart gmetad."
fi


##
## POST GMOND
##
%post gmond
if [ "$1" -gt "1" ]; then
   # Upgrading ganglia package - restart gmond
      echo "Type '/etc/rc.d/init.d/gmond restart' to restart gmond."
fi


##
## CLEAN
##
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


##
## FILES LIBS
##
%files libs
%defattr(-,root,system)
%{_libdir}/libganglia*.a
%{_libdir64}/libganglia*.a


##
## FILES GMETAD
##
%files gmetad
%defattr(-,root,system)
%attr(0755,nobody,nobody) /var/lib/ganglia/rrds
%attr(0755,nobody,nobody) /var/lib64/ganglia/rrds
%{_sbindir}/gmetad*
%config(noreplace) %{conf_dir}/gmetad.conf
%{_mandir}/man1/gmetad.1*
/etc/rc.d/init.d/gmetad
/etc/rc.d/rc2.d/Sgmetad
/etc/rc.d/rc2.d/Kgmetad
/etc/rc.d/rc3.d/Sgmetad
/etc/rc.d/rc3.d/Kgmetad


##
## FILES GMOND
##
%files gmond
%defattr(-,root,system)
%attr(0500,root,system) %{_bindir}/gmetric*
%attr(0555,root,system) %{_bindir}/gstat*
%{_sbindir}/gmond*
%{_mandir}/man1/gmetric.1*
%{_mandir}/man1/gmond.1*
%{_mandir}/man1/gstat.1*
%{_mandir}/man5/gmond.conf.5*
%config(noreplace) %{conf_dir}/gmond.conf
%dir %{conf_dir}
%dir %{conf_dir}/conf.d/
%dir %{_libdir}/ganglia/
%dir %{_libdir64}/ganglia/
%{_libdir}/%{name}/modcpu.so
%{_libdir}/%{name}/moddisk.so
%{_libdir}/%{name}/modload.so
%{_libdir}/%{name}/modmem.so
%{_libdir}/%{name}/modnet.so
%{_libdir}/%{name}/modproc.so
%{_libdir}/%{name}/modsys.so
%{_libdir64}/%{name}/modcpu.so
%{_libdir64}/%{name}/moddisk.so
%{_libdir64}/%{name}/modload.so
%{_libdir64}/%{name}/modmem.so
%{_libdir64}/%{name}/modnet.so
%{_libdir64}/%{name}/modproc.so
%{_libdir64}/%{name}/modsys.so
/etc/rc.d/init.d/gmond
/etc/rc.d/rc2.d/Sgmond
/etc/rc.d/rc2.d/Kgmond
/etc/rc.d/rc3.d/Sgmond
/etc/rc.d/rc3.d/Kgmond


##
## FILES GMOND-PYTHON
##
%files gmond-python
%defattr(-,root,system,-)
%{_libdir}/%{name}/modpython.so
%{_libdir64}/%{name}/modpython.so
%dir %{_libdir}/%{name}/python_modules
%dir %{_libdir64}/%{name}/python_modules
%config(noreplace) %{conf_dir}/conf.d/modpython.conf


##
## FILES GMOND-PYTHON-EXAMPLES
##
%files gmond-python-examples
%defattr(-,root,system,-)
%{_libdir}/%{name}/python_modules/*.py
%{_libdir64}/%{name}/python_modules/*.py
%config(noreplace) %{conf_dir}/conf.d/*.pyconf*


##
## FILES DEVEL
##
%files devel
%defattr(-,root,system)
%{_bindir}/ganglia-config*
%{_includedir}/ganglia_gexec.h
%{_includedir}/ganglia.h
%{_includedir}/gm_file.h
%{_includedir}/gm_metric.h
%{_includedir}/gm_mmn.h
%{_includedir}/gm_msg.h
%{_includedir}/gm_protocol.h
%{_includedir}/gm_value.h


##
## CHANGELOG
##
%changelog
* Mon Apr 06 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.7.2-3
- Rebuild for new apr
- Remove brtl flag
- Stop providing .la
- libs subpackage and not lib subpackage
- No more %preun (resp. %post) install /etc/rc.d/init.d/gmond stop (resp. restart)
- No more %preun (resp. %post) install /etc/rc.d/init.d/gmetad stop (resp. restart)

* Tue Apr 30 2019 Reshma V Kumar <reskumar@in.ibm.com> - 3.7.2-2
- Rebuild to remove dependency on httpd

* Tue Jan 08 2019 Reshma V Kumar <reskumar@in.ibm.com> - 3.7.2-1
- Update to latest version

* Thu Apr 16 2015 Michael Perzl <michael@perzl.org> - 3.6.0-3
- rebuilt against newest versions of dependencies

* Fri Jul 12 2013 Michael Perzl <michael@perzl.org> - 3.6.0-2
- added the missing cpu_steal_func to AIX libmetrics file

* Tue Jun 11 2013 Michael Perzl <michael@perzl.org> - 3.6.0-1
- updated to version 3.6.0

* Tue Jun 11 2013 Michael Perzl <michael@perzl.org> - 3.5.0-1
- updated to version 3.5.0

* Mon Jun 10 2013 Michael Perzl <michael@perzl.org> - 3.4.0-2
- new implementation of AIX libmetrics file
- rebuilt against newer RRDTool version
- enabled Python gmond modules

* Mon May 28 2012 Michael Perzl <michael@perzl.org> - 3.4.0-1
- updated to version 3.4.0

* Sun May 06 2012 Michael Perzl <michael@perzl.org> - 3.3.7-1
- updated to version 3.3.7

* Fri Apr 20 2012 Michael Perzl <michael@perzl.org> - 3.3.6-1
- updated to version 3.3.6

* Wed Apr 11 2012 Michael Perzl <michael@perzl.org> - 3.3.5-1
- updated to version 3.3.5

* Thu Feb 09 2012 Michael Perzl <michael@perzl.org> - 3.3.1-1
- updated to version 3.3.1

* Thu Feb 09 2012 Michael Perzl <michael@perzl.org> - 3.2.0-2
- fixed the termination signal in the gmond and gmetad startup scripts

* Thu Oct 13 2011 Michael Perzl <michael@perzl.org> - 3.2.0-1
- updated to version 3.2.0

* Wed Oct 12 2011 Michael Perzl <michael@perzl.org> - 3.1.7-4
- fixed the cpu properties (user, sys, idle, wait)

* Wed Nov 17 2010 Michael Perzl <michael@perzl.org> - 3.1.7-3
- fixed an error in the gmond init.d script

* Thu Sep 02 2010 Michael Perzl <michael@perzl.org> - 3.1.7-2
- moved all additional modules into separate RPM files
- improved gmetad and gmond start/stop scripts

* Fri May 07 2010 Michael Perzl <michael@perzl.org> - 3.1.7-1
- updated to version 3.1.7

* Tue Apr 27 2010 Michael Perzl <michael@perzl.org> - 3.1.2-5
- added sanity check for cpu_pool_idle_func()
- added firmware version metric (--> fwversion_func() )

* Fri Apr 16 2010 Michael Perzl <michael@perzl.org> - 3.1.2-4
- added IO ops/sec metric (--> disk_iops_func() )
- changed metric type from GANGLIA_VALUE_FLOAT to GANGLIA_VALUE_DOUBLE for
  disk_read_func() and disk_write_func()
- added the mod_ibmrperf module with "rperf" and "specint" metrics

* Thu Jan 21 2010 Michael Perzl <michael@perzl.org> - 3.1.2-3
- improved cpu_used for non micropartitioned systems
- fixed defuncts caused by open pipes (--> popen() without pclose() )
- added checks for possible libperfstat counter resets

* Sun Oct 04 2009 Michael Perzl <michael@perzl.org> - 3.1.2-2
- added the mod_ibmams module für IBM AMS (Active Memory Sharing)

* Fri Feb 20 2009 Michael Perzl <michael@perzl.org> - 3.1.2-1
- updated to Ganglia v3.1.2, enabled DSOs on AIX

* Tue Mar 25 2008 Michael Perzl <michael@perzl.org> - 3.0.7-1
- updated for Ganglia v3.0.7

* Tue Mar 25 2008 Michael Perzl <michael@perzl.org> - 3.0.6-1
- updated for Ganglia v3.0.6

* Mon Oct 08 2007 Michael Perzl <michael@perzl.org> - 3.0.5-1
- updated for Ganglia v3.0.5

* Wed Jul 11 2007 Michael Perzl <michael@perzl.org> - 3.0.4-2
- fixed the network counter overflow error on AIX

* Wed Jan 10 2007 Michael Perzl <michael@perzl.org> - 3.0.4-1
- adapted for Ganglia v3.0.4

* Fri Apr 21 2006 Michael Perzl <michael@perzl.org> - 3.0.3-1
- adapted for Ganglia v3.0.3

* Thu Feb 23 2006 Michael Perzl <michael@perzl.org>
- first version for AIX V5.1 and higher, based on the original Ganglia SPEC file
