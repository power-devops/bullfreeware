Summary: ODBC driver manager and drivers for PostgreSQL, MySQL, etc.
Name: unixODBC
Version: 2.3.0
Release: 1
Copyright: LGPL and GPL
Group: Applications/Databases
Source0: %{name}-%{version}.tar.gz
Source1: unixodbc_conf.h
Source2: odbcinst.ini
URL: http://www.unixodbc.org/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: readline-devel >= 5.2
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
mkdir -p ../64bit
cp -r * ../64bit/
mv ../64bit .


%build
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"
export LDFLAGS="-Wl,-brtl"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --disable-gui
make %{?_smp_mflags}
cd ..

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
./configure \
    --prefix=%{_prefix} \
    --disable-gui
make %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install-strip
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done
mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc64.h

cd ..
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install-strip
mv ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf-ppc32.h

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/unixodbc_conf.h

cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}

# create "real" AIX libraries
for f in ${RPM_BUILD_ROOT}%{_libdir}/lib*.so ; do
    baselib=`basename ${f} .so`
    /usr/bin/ar -rv -X32 ${RPM_BUILD_ROOT}%{_libdir}/${baselib}.a ${f}
    lib64=`echo ${f} | sed 's|/opt/freeware/lib|/opt/freeware/lib64|g'`
    /usr/bin/ar -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${baselib}.a ${lib64}
done

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
%doc AUTHORS COPYING ChangeLog NEWS README README.AIX doc
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*
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
* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.3.0
- Initial port on Aix5.3
