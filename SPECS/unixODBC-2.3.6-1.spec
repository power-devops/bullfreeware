Summary: ODBC driver manager and drivers for PostgreSQL, MySQL, etc.
Name: unixODBC
Version: 2.3.6
Release: 1

Copyright: LGPL and GPL
Group: Applications/Databases

Source0: %{name}-%{version}.tar.gz
Source1: unixodbc_conf.h
Source2: odbcinst.ini
URL: http://www.unixodbc.org/

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: readline-devel >= 5.2
BuildRequires: automake >= 1.14
Requires: readline >= 5.2

%define _libdir64 %{_prefix}/lib64

%description
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.
All libs are LGPL (except nn which is GPL?).


%package devel
Summary: Includes and static libraries for ODBC development
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
unixODBC aims to provide a complete ODBC solution for the Linux platform.
All programs are GPL.
All libs are LGPL (except nn which is GPL?).
This package contains the include files and static libraries
for development.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export RM="/usr/bin/rm -f"

# first build the 64-bit version
cd 64bit

export LDFLAGS="-Wl,-brtl -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

#export CC="/usr/vac/bin/xlc_r -q64"
#export CXX="/usr/vacpp/bin/xlC_r -q64"
export CC="gcc -maix64"
export CXX="g++ -maix64"

export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --disable-gui

gmake %{?_smp_mflags} -j16


# now build the 32-bit version
cd ../32bit

export LDFLAGS="-Wl,-brtl -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

#export CC="/usr/vac/bin/xlc_r -q32"
#export CXX="/usr/vacpp/bin/xlC_r -q32"
export CC="gcc -maix32"
export CXX="g++ -maix32"

export OBJECT_MODE=32

./configure \
    --prefix=%{_prefix} \
    --disable-gui

gmake %{?_smp_mflags} -j16


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install-strip
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done
mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc64.h

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install-strip
mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc32.h

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}

# create "real" AIX libraries
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.so ; do
    baselib=`basename ${f} .so`
    /usr/bin/ar -rv -X32 ${RPM_BUILD_ROOT}%{_libdir}/${baselib}.a ${f}
    strip -X32 -e ${f}
    lib64=`echo ${f} | sed 's|/opt/freeware/lib|/opt/freeware/lib64|g'`
    /usr/bin/ar -q  -X64 ${RPM_BUILD_ROOT}%{_libdir}/${baselib}.a ${lib64}
    strip -X64 -e ${lib64}
done

# Add symlinks from lib64 to lib
(
cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in libodbc.a libodbccr.a libodbcinst.a
do
	ln -sf %{_libdir}/$f .
done
)
	

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


%pre
if [ -f %{sysconfdir}/odbc.ini ]; then
    mv -f %{sysconfdir}/odbc.ini %{sysconfdir}/odbc.ini.rpmpresave
fi
if [ -f %{sysconfdir}/odbcinst.ini ]; then
    mv -f %{sysconfdir}/odbcinst.ini %{sysconfdir}/odbcinst.ini.rpmpresave
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog 32bit/NEWS 32bit/README 32bit/README.AIX 32bit/doc
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%defattr(-,root,system)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%changelog
* Wed Apr 25 2018 Tony Reix <tony.reix@atos.net> 2.3.6
- update to 2.3.6, initial port on AIX 6.1

* Mon Jun 11 2012 Patricia Cugny <patricia.cugny@bull.net> 2.3.1
- update to 2.3.1, initial port on AIX 6.1

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.3.0
- Initial port on Aix5.3
