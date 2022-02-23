%bcond_without dotests

%bcond_with tcl


%define _libdir64 %{_prefix}/lib64
%define python3_version    %(python3_64 -V | sed "s|\.[0-9]*$||" | sed "s|Python ||")
%define python3_sitearch32   %{_libdir}/python%{python3_version}/site-packages
%define python3_sitearch64 %{_libdir64}/python%{python3_version}/site-packages

%define python_sitearch %{_libdir}/python2.7/site-packages
%define python_sitearch64 %{_libdir64}/python2.7/site-packages

# Current version of librrd.so is 8 (may have to include old versions 4 and 2)
# Previous package 1.4.7 builds version 4 and included older version 2
%global librrdver 8

%define rrdcached_user rrdcache
%define rrdcached_group rrdcache

%define perl_vendorlib %(eval "`/opt/freeware/bin/perl_32 -V:installvendorlib`"; echo $installvendorlib)

%global ruby_version %(ruby -v | /opt/freeware/bin/sed -e 's|ruby ||' | /opt/freeware/bin/sed -r -e 's|\([1-9]*\.[1-9]\)*\..*\$|\\1|')
%{!?ruby_vendorarchdir32: %global ruby_vendorarchdir32 %(ruby_32 -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}
%{!?ruby_vendorarchdir64: %global ruby_vendorarchdir64 %(ruby_64 -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}


Name: rrdtool
Version: 1.7.2
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
Source5: librrd.so.4-aix32
Source6: librrd.so.4-aix64
Source7: librrd_th.so.4-aix32
Source8: librrd_th.so.4-aix64
Source10: rrdcached.aix.init
Source11: rrdcached.sysconfig
# Packaged ruby config.h is 64 bit only - include a concatenated 32/64 version
Source12: rrdtool_ruby2.3.1_config.h

Source20: %{name}-%{version}-%{release}.build.log

Patch0: %{name}-1.7.2-aix.patch
Patch1: %{name}-1.7.0-tcl-ldflags.patch
# Patch2: %{name}-1.7.0-aixconf.patch
Patch3: %{name}-1.7.0-ruby-ldflags.patch
Patch4: rrdtool-1.7.2-syslog.patch

BuildRequires: coreutils, make, sed

BuildRequires: cairo-devel >= 1.8.8
BuildRequires: freetype2-devel >= 2.3.12
BuildRequires: gettext
BuildRequires: glib2-devel >= 2.22.5
BuildRequires: libart_lgpl-devel >= 2.3.20
BuildRequires: libdbi-devel >= 0.8.4
BuildRequires: libpng-devel >= 1.2.44
BuildRequires: libxml2-devel >= 2.6.32-2
BuildRequires: lua >= 5.1.4
BuildRequires: lua-devel >= 5.1.4
BuildRequires: pango-devel >= 1.24.5
BuildRequires: perl >= 5.24
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
Requires: pango >= 1.24.5
Requires: zlib
Requires: libgcc
Requires: xz-libs
Requires: libffi
Requires: expat

# Requires: dejavu-sans-mono-fonts, dejavu-lgc-sans-mono-fonts
Requires: dejavu-sans-mono-fonts

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
Requires: pango-devel >= 1.24.5
%if %{with tcl}
Requires: tcl-devel >= 8.5.8-2
%endif
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
Requires: glib2
Requires: libdbi
Requires: libxml2
Requires: xz-libs
Requires: libffi
Requires: expat

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
Requires: perl >= 5.24
Provides: %{name}-perl

%description perl
The Perl RRDtool bindings.


%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
%global lualibdir %{_libdir}/lua/%{luaver}
%global lualibdir64 %{_libdir64}/lua/%{luaver}
%global luapkgdir %{_datadir}/lua/%{luaver}

%package lua
Summary: Lua RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: lua >= %{luaver}
Requires: libgcc >= 6.3.0-1

%description lua
The %{name}-lua package includes RRDtool bindings for Lua.


%package python%{python3_version}
Summary: Python RRDtool bindings
Group: Development/Languages
BuildRequires: python3-devel >= 3.8
Requires: %{name} = %{version}-%{release}
Requires: python(abi) = %{python3_version}

Provides: python-%{name} = %{version}-%{release}

%description python%{python3_version}
The Python3 RRDtool bindings.


%package ruby%{ruby_version}
Summary: Ruby RRDtool bindings
Group: Development/Languages
BuildRequires: ruby, ruby-devel
Requires: %{name} = %{version}-%{release}
Requires: ruby >= 2.6.5
Requires: gmp

%description ruby%{ruby_version}
The %{name}-ruby package includes RRDtool bindings for Ruby.


%if %{with tcl}
%package tcl
Summary: Tcl RRDtool bindings
Group: Development/Languages
BuildRequires: tcl-devel >= 8.5.8-2
Requires: tcl >= 8.5.8-2
Requires: libgcc >= 6.3.0-1
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}

%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.
%endif


%prep
%setup -q
%patch0 -p1 -b .aix
# %patch2 -p1 -b .aixconf
# %patch103 -p1 -b .ruby-2-fix
%patch4 -p1 -b .syslog

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

# Patch tcl LDFLAGS for 32 and 64 bit versions of bindings/tcl/Makefile.in
%patch1 -p1 -b .tcl-ldflags
%patch3 -p1 -b .ruby-ldflags



%build
export LIBTOOLIZE_OPTIONS="--warnings=all"
export PERLCC=$CC
export PKG_CONFIG_PATH=/opt/freeware/lib/pkgconfig
export MAKE=gmake
export PKG_CONFIG=/opt/freeware/bin/pkg-config
export PATH=/opt/freeware/bin:$PATH
# export RM="/usr/bin/rm -f"

# export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include -I/opt/freeware/include/cairo -I/opt/freeware/include/pango-1.0/pango -I/opt/freeware/include/glib-2.0"

export CFLAGS="$CFLAGS -I/opt/freeware/include/cairo -I/opt/freeware/include/pango-1.0 -I/opt/freeware/include/glib-2.0"

cd 64bit
# first build the 64-bit version

export CC="gcc -maix64 -O2 -D_LARGE_FILES -D__64BIT__"
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64

export PERL=/opt/freeware/bin/perl_64
export PYTHON=/opt/freeware/bin/python3_64
export RUBY=/opt/freeware/bin/ruby_64

export LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib -lpango-1.0 -lcairo -lgobject-2.0 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib"

export NROFF=/usr/bin/nroff

# # The command ruby is a link to either 64 or 32 bit version
# ln -sf ruby_64 /opt/freeware/bin/ruby

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --disable-silent-rules \
    --disable-rpath \
    --enable-shared --disable-static \
    --disable-mmap \
    --enable-perl \
    --with-perl-options='INSTALLDIRS="vendor"' \
    --enable-python \
    --enable-lua \
%if %{with tcl}
    --enable-tcl \
    --enable-tcl-site \
    --with-tcllib=%{_libdir64} \
%else
    --disable-tcl \
    --disable-tcl-site \
%endif
    --enable-ruby \
    --with-pic

sed -i 's|-Wbreak||' doc/Makefile

gmake 

cd ../32bit
# now build the 32-bit version

export CC="gcc -maix32 -D_LARGE_FILES -O2"
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32

export PERL=/opt/freeware/bin/perl_32
export PYTHON=/opt/freeware/bin/python3_32
export RUBY=/opt/freeware/bin/ruby_32

export LDFLAGS="-L/opt/freeware/lib -lpango-1.0 -lgobject-2.0 -lcairo -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

# # The command ruby is a link to either 64 or 32 bit version
# ln -sf ruby_32 /opt/freeware/bin/ruby

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --disable-silent-rules \
    --disable-rpath \
    --enable-shared --disable-static \
    --disable-mmap \
    --enable-perl \
    --with-perl-options='INSTALLDIRS="vendor"' \
    --enable-python \
    --enable-lua \
%if %{with tcl}
    --enable-tcl \
    --enable-tcl-site \
    --with-tcllib=%{_libdir} \
%else
    --disable-tcl \
    --disable-tcl-site \
%endif
    --enable-ruby \
    --with-pic

sed -i 's|-Wbreak||' doc/Makefile

gmake

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
# export RM="/usr/bin/rm -f"

cd 64bit

export OBJECT_MODE=64
export CC="gcc -maix64 -D_LARGE_FILES -D__64BIT__ -O2"
export AR="/usr/bin/ar -X64"
export LIBTOOLFLAGS="--warnings=all"

# # The command ruby is a link to either 64 or 32 bit version
# ln -sf ruby_64 /opt/freeware/bin/ruby

gmake DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir64}
cp  bindings/ruby/RRD.so  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir64}/RRD.so

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done

  # mv -f ${RPM_BUILD_ROOT}%{_libdir}/lua ${RPM_BUILD_ROOT}%{_libdir64}
)

cd ../32bit

export OBJECT_MODE=32
export CC="gcc -maix32 -D_LARGE_FILES"
export AR="/usr/bin/ar -X32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export LIBTOOLFLAGS="--warnings=all"

# # The command ruby is a link to either 64 or 32 bit version
# ln -sf ruby_32 /opt/freeware/bin/ruby

gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)

mkdir -p  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir32}
cp  ./bindings/ruby/RRD.so  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir32}/RRD.so

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{lualibdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{lualibdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a ${RPM_BUILD_ROOT}%{_libdir64}/librrd.so.%{librrdver}
# librrd_th no longer in rrdtool ?
# /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a ${RPM_BUILD_ROOT}%{_libdir64}/librrd_th.so.%{librrdver}
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{lualibdir}/rrd.a ${RPM_BUILD_ROOT}%{lualibdir64}/rrd.so.0

# add the older version 1.2 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE1} librrd.so.2
cp %{SOURCE5} librrd.so.4
/usr/bin/strip -X32 -e librrd.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2
/usr/bin/strip -X32 -e librrd.so.4
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.4

cp %{SOURCE2} librrd.so.2
cp %{SOURCE6} librrd.so.4
/usr/bin/strip -X64 -e librrd.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2
/usr/bin/strip -X64 -e librrd.so.4
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.4

cp %{SOURCE3} librrd_th.so.2
cp %{SOURCE7} librrd_th.so.4
/usr/bin/strip -X32 -e librrd_th.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.2
/usr/bin/strip -X32 -e librrd_th.so.4
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.4

cp %{SOURCE4} librrd_th.so.2
cp %{SOURCE8} librrd_th.so.4
/usr/bin/strip -X64 -e librrd_th.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.2
/usr/bin/strip -X64 -e librrd_th.so.4
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd_th.a librrd_th.so.4


# Move perl modules RRDp.pm, etc
# mv $RPM_BUILD_ROOT%{perl_vendorlib}/RRDp.pm $RPM_BUILD_ROOT%{perl_vendorarch}/
# mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RRDs/


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

cp %{SOURCE12} ${RPM_BUILD_ROOT}%{ruby_vendorarchdir32}/rrdtool_ruby2.3.1_config.h
chmod 0644 ${RPM_BUILD_ROOT}%{ruby_vendorarchdir32}/rrdtool_ruby2.3.1_config.h

# clean up buildroot
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/perl/5.8.*/ppc-aix*/*/*/.packlist

# Dependencies on /usr/bin/perl or python
find ${RPM_BUILD_ROOT}%{_datadir}/%{name}/examples/ -name "*.py" | xargs sed -i 's|#! /usr/bin/python|#! /usr/bin/env python3|'
find ${RPM_BUILD_ROOT}%{_datadir}/%{name}/examples/ -name "*.pl" | xargs sed -i 's|#!/usr/bin/perl|#!/opt/freeware/bin/perl|'

# perl man location
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3/* ${RPM_BUILD_ROOT}%{_mandir}/man3


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
gmake check || true

cd ../32bit
export OBJECT_MODE=32
gmake check || true
%endif


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
%doc 32bit/LICENSE
%doc 32bit/CHANGES 32bit/CONTRIBUTORS 32bit/COPYRIGHT
%doc 32bit/NEWS 32bit/THREADS 32bit/TODO
%doc 32bit/rpm-doc/docs/
%{_bindir}/rrdcgi*
%{_bindir}/rrdtool*
%{_bindir}/rrdupdate*
%{_libdir}/*.a
%{_mandir}/man1/[b,c]*
%{_mandir}/man1/rpn*
%{_mandir}/man1/rrd-beginners.1
%{_mandir}/man1/rrd[a-b,d-i,r-x]*
%{_mandir}/man1/rrdcgi.1
%{_mandir}/man1/rrdcreate.1
%{_mandir}/man1/rrdlast*.1
%{_datadir}/%{name}/examples/*.cgi

%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_mandir}/man3/librrd.3

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
%{_datadir}/%{name}/examples/rrdcached

%files perl
%defattr(-,root,system,-)
# %{_libdir}/perl5/5.*/*
%{perl_vendorlib}/*.pm
# %attr(0755,root,root) %{perl_vendorlib}/auto/RRDs/
%{_mandir}/man3/RRD*.3
%{_datadir}/%{name}/examples/*.pl

%files lua
%defattr(-,root,system,-)
%doc 32bit/bindings/lua/README
%doc 32bit/rpm-doc/docs/*lua*
%{lualibdir}/*
%{lualibdir64}/*
%{_mandir}/man1/rrdlua.1

%files python%{python3_version}
%defattr(-,root,system,-)
%doc 32bit/bindings/python/COPYING
%doc 32bit/bindings/python/README.md
# %{python_sitearch}/*
# %{python_sitearch64}/*
%{python3_sitearch32}/rrdtool.so
%{python3_sitearch32}/rrdtool-*.egg-info
%{python3_sitearch64}/rrdtool.so
%{python3_sitearch64}/rrdtool-*.egg-info
%{_datadir}/%{name}/examples/*.py

%files ruby%{ruby_version}
%defattr(-,root,system,-)
%doc 32bit/bindings/ruby/README
%{ruby_vendorarchdir32}/RRD.so
%{ruby_vendorarchdir64}/RRD.so
%{ruby_vendorarchdir32}/rrdtool_ruby2.3.1_config.h

%if %{with tcl}
%files tcl
%defattr(-,root,system,-)
%doc 32bit/bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir64}/tclrrd*.so
%{_libdir}/%{name}/*.tcl
%{_libdir64}/%{name}/*.tcl
%endif


%changelog
* Mon Apr 06 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.7.2-1
- Bullfreeware OpenSSL removal
- Update python bindings to python3
- Tcl bindings do not work
- Add checks

* Tue Feb 20 2018 Michael Wilson <michael.a.wilson@atos.net> 1.7.0-2
- Add Ruby bindings

* Wed Feb 14 2018 Michael Wilson <michael.a.wilson@atos.net> 1.7.0-1
- Update to 1.7.0
- Modifications inspired by Fedora SPEC file

* Tue Mar 27 2012 Gerard Visiedo <gerard.visido@bull.net> 3.2.0-1
- Initial port on Aix6.1

