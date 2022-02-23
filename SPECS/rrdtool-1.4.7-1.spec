%define _libdir64 %{_prefix}/lib64
%define python_sitearch %{_libdir}/python2.7/site-packages
%define python_sitearch64 %{_libdir64}/python2.7/site-packages

%define rrdcached_user rrdcache
%define rrdcached_group rrdcache

Name: rrdtool
Version: 1.4.7
Release: 1
Summary: Round Robin Database Tool to store and display time-series data
License: GPL
Group: Applications/Databases
URL: http://oss.oetiker.ch/rrdtool
Source0: http://oss.oetiker.ch/rrdtool/pub/%{name}-%{version}.tar.gz
Source1: librrd.so.2-aix32
Source2: librrd.so.2-aix64
Source3: librrd_th.so.2-aix32
Source4: librrd_th.so.2-aix64
Source10: rrdcached.aix.init
Source11: rrdcached.sysconfig
Patch0: %{name}-%{version}-aix.patch
Patch1: %{name}-%{version}-tcl-ldflags.patch
Patch2: %{name}-%{version}-aixconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: coreutils, make

BuildRequires: cairo-devel >= 1.8.8
BuildRequires: freetype2-devel >= 2.3.12
BuildRequires: gettext
BuildRequires: glib2-devel >= 2.22.5
BuildRequires: libart_lgpl-devel >= 2.3.20
BuildRequires: libdbi-devel >= 0.8.4
BuildRequires: libpng-devel >= 1.2.44
BuildRequires: libxml2-devel >= 2.6.32-2
BuildRequires: lua-devel >= 5.1.4
BuildRequires: openssl-devel >= 0.9.8
BuildRequires: pango-devel >= 1.24.5
BuildRequires: perl >= 5.8.8
BuildRequires: python >= 2.6.2
BuildRequires: tcl-devel >= 8.5.8-2
BuildRequires: zlib-devel

Requires: cairo >= 1.8.8
Requires: freetype2 >= 2.3.12
Requires: gettext
Requires: glib2 >= 2.22.5
Requires: libart_lgpl >= 2.3.20
Requires: libdbi >= 0.8.4
Requires: libpng >= 1.2.44
Requires: libxml2 >= 2.6.32-2
Requires: openssl >= 0.9.8
Requires: pango >= 1.24.5
Requires: zlib

Requires: dejavu-sans-mono-fonts, dejavu-lgc-sans-mono-fonts

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and 
display time-series data (i.e. network bandwidth, machine-room temperature, 
server load average). It stores the data in a very compact way that will not 
expand over time, and it presents useful graphs by processing the data to 
enforce a certain data density. It can be used either via simple wrapper 
scripts (from shell or Perl) or via frontends that poll network devices and 
put a friendly user interface on it.


%package devel
Summary: RRDtool static libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: cairo-devel >= 1.8.8
Requires: freetype2-devel >= 2.3.12
Requires: gettext
Requires: glib2-devel >= 2.22.5
Requires: libart_lgpl-devel >= 2.3.20
Requires: libdbi-devel >= 0.8.4
Requires: libpng-devel >= 1.2.44
Requires: libxml2-devel >= 2.6.32-2
Requires: openssl-devel >= 0.9.8
Requires: pango-devel >= 1.24.5
Requires: tcl-devel >= 8.5.8-2
Requires: zlib-devel

%description devel
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package allow you to use directly this library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64" or "gcc -maix64".


%package cached
Summary: Data caching daemon for RRDtool
Group: System/Servers
Requires: %{name} = %{version}-%{release}

%description cached
rrdcached is a daemon that receives updates to existing RRD files,
accumulates them and, if enough have been received or a defined time has
passed, writes the updates to the RRD file. The daemon was written with
big setups in mind which usually runs into I/O related problems. This
daemon was written to alleviate these problems.


%package perl
Summary: Perl RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: perl >= 5.8.8
Provides: %{name}-perl

%description perl
The Perl RRDtool bindings.


%package lua
Summary: Lua RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: lua >= 5.1.4

%description lua
The Lua RRDtool bindings.


%package python
Summary: Python RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: python >= 2.6.2
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}

%description python
The Python RRDtool bindings.


%package tcl
Summary: Tcl RRDtool bindings
Group: Development/Languages
BuildRequires: tcl-devel >= 8.5.8-2
Requires: tcl >= 8.5.8-2
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}

%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.


%prep
%setup -q
%patch0 -p1 -b .aix
%patch2 -p1 -b .aixconf
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)
cd ..
%patch1

%build
export PATH=/opt/freeware/bin:$PATH
export PERLCC="/usr/vac/bin/xlc_r"
export RM="/usr/bin/rm -f"
export CC="/usr/vac/bin/xlc_r"
export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include -I/opt/freeware/include/cairo -I/opt/freeware/include/pango-1.0/pango -I/opt/freeware/include/glib-2.0"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export PERL=/usr/bin/perl64
export PYTHON=/usr/bin/python_64
export LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --disable-silent-rules \
    --enable-shared --disable-static \
    --enable-pthread \
    --disable-mmap \
    --enable-perl \
    --enable-python \
    --enable-lua \
    --enable-tcl \
    --with-tcllib=%{_libdir64} \
    --disable-ruby
%ifos aix6.1
cat rrd_config.h | grep -v "HAVE_ISFINITE" > rrd_config.tmp
mv -f rrd_config.tmp rrd_config.h
%endif
make 

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export PERL=/usr/bin/perl
export PYTHON=/usr/bin/python
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --disable-silent-rules \
    --enable-shared --disable-static \
    --enable-pthread \
    --disable-mmap \
    --enable-perl \
    --enable-python \
    --enable-lua \
    --enable-tcl \
    --with-tcllib=%{_libdir} \
    --disable-ruby
%ifos aix6.1
cat rrd_config.h | grep -v "HAVE_ISFINITE" > rrd_config.tmp
mv -f rrd_config.tmp rrd_config.h
%endif
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done

  mv -f ${RPM_BUILD_ROOT}%{_libdir}/lua ${RPM_BUILD_ROOT}%{_libdir64}
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir64}/lua/5.1
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}/lua/5.1
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a ${RPM_BUILD_ROOT}%{_libdir64}/librrd.so.4
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a ${RPM_BUILD_ROOT}%{_libdir64}/librrd_th.so.4
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lua/5.1/rrd.a ${RPM_BUILD_ROOT}%{_libdir64}/lua/5.1/rrd.so.0

# add the older version 1.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} librrd.so.2
/usr/bin/strip -X32 librrd.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2

cp %{SOURCE2} librrd.so.2
/usr/bin/strip -X64 librrd.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2

cp %{SOURCE3} librrd_th.so.2
/usr/bin/strip -X32 -e librrd_th.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.2

cp %{SOURCE4} librrd_th.so.2
/usr/bin/strip -X64 -e librrd_th.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.2

# We only want .txt and .html files for the main documentation
mkdir -p rpm-doc/docs/
/opt/freeware/bin/cp -ap doc/*.txt doc/*.html rpm-doc/docs/

rm -f examples/Makefile* examples/*.in

# install rrdcached files
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d
mkdir -p ${RPM_BUILD_ROOT}/var/lib/rrdcached
mkdir -p ${RPM_BUILD_ROOT}/var/run/rrdcached
ln -sf '../init.d/rrdcached' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Srrdcached
ln -sf '../init.d/rrdcached' ${RPM_BUILD_ROOT}/etc/rc.d/rc2.d/Krrdcached
ln -sf '../init.d/rrdcached' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Srrdcached
ln -sf '../init.d/rrdcached' ${RPM_BUILD_ROOT}/etc/rc.d/rc3.d/Krrdcached

cp %{SOURCE10} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rrdcached
chmod 0755 ${RPM_BUILD_ROOT}/etc/rc.d/init.d/rrdcached

cp %{SOURCE11} ${RPM_BUILD_ROOT}/etc/sysconfig/rrdcached
chmod 0644 ${RPM_BUILD_ROOT}/etc/sysconfig/rrdcached

# clean up buildroot
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/perl/5.8.*/ppc-aix*/*/*/.packlist

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%pre cached
# add the "%{rrdcached_group}" group only if it does not yet exist
result=`/usr/sbin/lsgroup %{rrdcached_group} | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [[ "${result}" != "%{rrdcached_group}" ]] ; then
    /usr/bin/mkgroup %{rrdcached_group} 2> /dev/null || :
fi
# add the "%{rrdcached_user}" user only if it does not yet exist
result=`/usr/sbin/lsuser %{rrdcached_user} | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [[ "${result}" != "%{rrdcached_user}" ]] ; then
    /usr/bin/mkuser pgrp=%{rrdcached_group} gecos='RRDcached User' \
        login='false' rlogin='false' %{rrdcached_user} 2> /dev/null || :
fi

%preun cached
/etc/rc.d/init.d/rrdcached stop > /dev/null 2>&1

%postun cached
# remove "rrdcache" user and group
/usr/sbin/rmuser -p %{rrdcached_user} || :
/usr/sbin/rmgroup %{rrdcached_group} || :

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/CONTRIBUTORS 32bit/COPYING 32bit/COPYRIGHT
%doc 32bit/NEWS 32bit/README 32bit/THREADS 32bit/TODO
%doc 32bit/rpm-doc/docs/
%{_bindir}/rrdcgi*
%{_bindir}/rrdtool*
%{_bindir}/rrdupdate*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man1/[b,c]*
%{_mandir}/man1/rpn*
%{_mandir}/man1/rrd-beginners.1
%{_mandir}/man1/rrd[a-b,d-i,r-x]*
%{_mandir}/man1/rrdcgi.1
%{_mandir}/man1/rrdcreate.1
%{_mandir}/man1/rrdlast*.1
/usr/bin/rrdcgi*
/usr/bin/rrdtool*
/usr/bin/rrdupdate*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*

%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_mandir}/man3/librrd.3
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la

%files cached
%defattr(-,root,system,-)
%{_bindir}/rrdcached
%config /etc/sysconfig/rrdcached
/etc/rc.d/init.d/rrdcached
/etc/rc.d/rc2.d/Srrdcached
/etc/rc.d/rc2.d/Krrdcached
/etc/rc.d/rc3.d/Srrdcached
/etc/rc.d/rc3.d/Krrdcached
%{_mandir}/man1/rrdcached*.1
%attr(0755,%{rrdcached_user},%{rrdcached_group}) %dir /var/lib/rrdcached
%attr(0755,%{rrdcached_user},%{rrdcached_group}) %dir /var/run/rrdcached
/usr/bin/rrdcached

%files perl
%defattr(-,root,system,-)
%doc 32bit/examples/
%{_libdir}/perl/5.*/*
%{_mandir}/man3/RRD*.3
%{_datadir}/%{name}

%files lua
%defattr(-,root,system,-)
%doc 32bit/rpm-doc/docs/*lua*
%{_libdir}/lua/5.*/*
%{_libdir64}/lua/5.*/*
%{_mandir}/man1/rrdlua.1

%files python
%defattr(-,root,system,-)
%doc 32bit/bindings/python/AUTHORS 32bit/bindings/python/COPYING
%doc 32bit/bindings/python/README
%{python_sitearch}/*
%{python_sitearch64}/*

%files tcl
%defattr(-,root,system,-)
%doc 32bit/bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir64}/tclrrd*.so
%{_libdir}/%{name}/*.tcl
%{_libdir64}/%{name}/*.tcl

%changelog
* Tue Mar 27 2012 Gerard Visiedo <gerard.visido@bull.net> 3.2.0-1
- Initial port on Aix6.1
