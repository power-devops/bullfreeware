%define _libdir64 %{_prefix}/lib64
%define python_sitearch %{_libdir}/python2.7/site-packages
%define python_sitearch64 %{_libdir64}/python2.7/site-packages

# Current version of librrd.so is 8 (may have to include old versions 4 and 2)
# Previous package 1.4.7 builds version 4 and included older version 2
%global librrdver 8

%define rrdcached_user rrdcache
%define rrdcached_group rrdcache

# Interference between LPP and RPM packages
# %define perl_vendorarch /usr/opt/perl5/lib/site_perl

# The version depends on /usr/bin/perl or /opt/freeware/bin/perl
%define perl_vendorlib /opt/freeware/lib/perl5/site_perl/%(eval "`/opt/freeware/bin/perl -V:version`"; echo $version)

%define perl_vendorarch %{perl_vendorlib}/ppc-aix-thread-multi

Name: rrdtool
Version: 1.7.0
Release: 2
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

Patch0: %{name}-%{version}-aix.patch
Patch1: %{name}-%{version}-tcl-ldflags.patch
Patch2: %{name}-%{version}-aixconf.patch
Patch3: %{name}-%{version}-ruby-ldflags.patch

# Fedora 28 patches (not currently used in build)
Patch101: rrdtool-1.4.4-php54.patch
# disable logo for php 5.5.
Patch102: rrdtool-1.4.7-php55.patch
Patch103: rrdtool-1.6.0-ruby-2-fix.patch
# enable php bindings on ppc
Patch104: rrdtool-1.4.8-php-ppc-fix.patch
# Header files are under directory cairo
Patch105: rrdtool-7.1.0-cairo_H.patch

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
BuildRequires: lua >= 5.1.4
BuildRequires: lua-devel >= 5.1.4
BuildRequires: openssl-devel >= 0.9.8
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
Requires: openssl >= 0.9.8
Requires: pango >= 1.24.5
Requires: zlib

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

%description lua
The %{name}-lua package includes RRDtool bindings for Lua.


%package python
Summary: Python RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: python >= 2.6.2
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}

%description python
The Python RRDtool bindings.


%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby_32 -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}
%{!?ruby_vendorarchdir64: %global ruby_vendorarchdir64 %(ruby_64 -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}

%package ruby
Summary: Ruby RRDtool bindings
Group: Development/Languages
BuildRequires: ruby, ruby-devel
Requires: %{name} = %{version}-%{release}

%description ruby
The %{name}-ruby package includes RRDtool bindings for Ruby.


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
# %patch103 -p1 -b .ruby-2-fix


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

export PATH=/opt/freeware/bin:$PATH
export RM="/usr/bin/rm -f"

# export CFLAGS="-DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX53 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15 -O -I/opt/freeware/include -I/usr/include -I/opt/freeware/include/cairo -I/opt/freeware/include/pango-1.0/pango -I/opt/freeware/include/glib-2.0"

export CFLAGS="$CFLAGS -I/opt/freeware/include/cairo -I/opt/freeware/include/pango-1.0/pango -I/opt/freeware/include/glib-2.0"

cd 64bit
# first build the 64-bit version

export CC="gcc -maix64 -D_LARGE_FILES -D__64BIT__"
export AR="/usr/bin/ar -X64"
export RM="/usr/bin/rm -f"
export OBJECT_MODE=64

export LIBTOOLIZE_OPTIONS="--warnings=all"
export PERLCC=$CC
export PKG_CONFIG_PATH=/opt/freeware/lib/pkgconfig
export MAKE=gmake
export PKG_CONFIG=/opt/freeware/bin/pkg-config

export PERL=/opt/freeware/bin/perl_64bit
export PYTHON=/usr/bin/python_64

# export LDFLAGS="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib"

export NROFF=/usr/bin/nroff

# The command ruby is a link to either 64 or 32 bit version
ln -sf ruby_64 /opt/freeware/bin/ruby

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_prefix}/share/man \
    --disable-silent-rules \
    --disable-rpath \
    --enable-shared --disable-static \
    --disable-mmap \
    --enable-perl \
    --with-perl-options='INSTALLDIRS="site"' \
    --enable-python \
    --enable-lua \
    --enable-tcl \
    --enable-tcl-site \
    --with-tcllib=%{_libdir64} \
    --enable-ruby \
    --with-pic
gmake 

cd ../32bit
# now build the 32-bit version

export CC="gcc -maix32 -D_LARGE_FILES"
export AR="/usr/bin/ar -X32"
export RM="/usr/bin/rm -f"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

export LIBTOOLIZE_OPTIONS="--warnings=all"
export PERLCC=$CC
export PKG_CONFIG_PATH=/opt/freeware/lib/pkgconfig
export MAKE=gmake
export PKG_CONFIG=/opt/freeware/bin/pkg-config

export PERL=/opt/freeware/bin/perl
export PYTHON=/usr/bin/python
# export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

# The command ruby is a link to either 64 or 32 bit version
ln -sf ruby_32 /opt/freeware/bin/ruby

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/share/man \
    --disable-silent-rules \
    --disable-rpath \
    --enable-shared --disable-static \
    --disable-mmap \
    --enable-perl \
    --with-perl-options='INSTALLDIRS="site"' \
    --enable-python \
    --enable-lua \
    --enable-tcl \
    --enable-tcl-site \
    --with-tcllib=%{_libdir} \
    --enable-ruby \
    --with-pic
gmake

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"

cd 64bit

export OBJECT_MODE=64
export CC="gcc -maix64 -D_LARGE_FILES -D__64BIT__"
export AR="/usr/bin/ar -X64"
export RM="/usr/bin/rm -f"
export LIBTOOLFLAGS="--warnings=all"

# The command ruby is a link to either 64 or 32 bit version
ln -sf ruby_64 /opt/freeware/bin/ruby

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
export RM="/usr/bin/rm -f"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export LIBTOOLFLAGS="--warnings=all"

# The command ruby is a link to either 64 or 32 bit version
ln -sf ruby_32 /opt/freeware/bin/ruby

gmake DESTDIR=${RPM_BUILD_ROOT} install

mkdir -p  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir}
cp  ./bindings/ruby/RRD.so  ${RPM_BUILD_ROOT}%{ruby_vendorarchdir}/RRD.so

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
/usr/bin/strip -X32 librrd.so.2
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2
/usr/bin/strip -X32 librrd.so.4
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.4

cp %{SOURCE2} librrd.so.2
cp %{SOURCE6} librrd.so.4
/usr/bin/strip -X64 librrd.so.2
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/librrd.a librrd.so.2
/usr/bin/strip -X64 librrd.so.4
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
mv $RPM_BUILD_ROOT%{perl_vendorlib}/RRDp.pm $RPM_BUILD_ROOT%{perl_vendorarch}/
mkdir -p $RPM_BUILD_ROOT%{perl_vendorarch}/auto/RRDs/



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

cp %{SOURCE12} ${RPM_BUILD_ROOT}%{ruby_vendorarchdir}/rrdtool_ruby2.3.1_config.h
chmod 0644 ${RPM_BUILD_ROOT}%{ruby_vendorarchdir}/rrdtool_ruby2.3.1_config.h

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
%doc 32bit/LICENSE
%doc 32bit/CHANGES 32bit/CONTRIBUTORS 32bit/COPYRIGHT
%doc 32bit/NEWS 32bit/THREADS 32bit/TODO
%doc 32bit/rpm-doc/docs/
%{_bindir}/rrdcgi*
%{_bindir}/rrdtool*
%{_bindir}/rrdupdate*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_prefix}/share/man/man1/[b,c]*
%{_prefix}/share/man/man1/rpn*
%{_prefix}/share/man/man1/rrd-beginners.1
%{_prefix}/share/man/man1/rrd[a-b,d-i,r-x]*
%{_prefix}/share/man/man1/rrdcgi.1
%{_prefix}/share/man/man1/rrdcreate.1
%{_prefix}/share/man/man1/rrdlast*.1
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
%{_prefix}/share/man/man3/librrd.3
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
%{_prefix}/share/man/man1/rrdcached*.1
%attr(0755,%{rrdcached_user},%{rrdcached_group}) %dir /var/lib/rrdcached
%attr(0755,%{rrdcached_user},%{rrdcached_group}) %dir /var/run/rrdcached
/usr/bin/rrdcached

%files perl
%defattr(-,root,system,-)
%doc 32bit/examples/
# %{_libdir}/perl5/5.*/*
%{perl_vendorarch}/*.pm
%attr(0755,root,root) %{perl_vendorarch}/auto/RRDs/
%{_prefix}/share/man/man3/RRD*.3
%{_datadir}/%{name}

%files lua
%defattr(-,root,system,-)
%doc 32bit/bindings/lua/README
%doc 32bit/rpm-doc/docs/*lua*
%{lualibdir}/*
%{lualibdir64}/*
%{_prefix}/share/man/man1/rrdlua.1

%files python
%defattr(-,root,system,-)
%doc 32bit/bindings/python/COPYING
%doc 32bit/bindings/python/README.md
# %{python_sitearch}/*
# %{python_sitearch64}/*
%{python_sitearch}/rrdtool.so
%{python_sitearch}/rrdtool-*.egg-info
%{python_sitearch64}/rrdtool.so
%{python_sitearch64}/rrdtool-*.egg-info

%files ruby
%doc 32bit/bindings/ruby/README
%{ruby_vendorarchdir}/RRD.so
%{ruby_vendorarchdir64}/RRD.so
%{ruby_vendorarchdir}/rrdtool_ruby2.3.1_config.h

%files tcl
%defattr(-,root,system,-)
%doc 32bit/bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir64}/tclrrd*.so
%{_libdir}/%{name}/*.tcl
%{_libdir64}/%{name}/*.tcl

%changelog
* Tue Feb 20 2018 Michael Wilson <michael.a.wilson@atos.net> 1.7.0-2
- Add Ruby bindings

* Wed Feb 14 2018 Michael Wilson <michael.a.wilson@atos.net> 1.7.0-1
- Update to 1.7.0
- Modifications inspired by Fedora SPEC file

* Tue Mar 27 2012 Gerard Visiedo <gerard.visido@bull.net> 3.2.0-1
- Initial port on Aix6.1

