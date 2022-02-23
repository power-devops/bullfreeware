%define _libdir64 %{_prefix}/lib64

Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 0.82
Release: 1
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/
Source0: ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz
Source1: freetds-tds_sysdep_public.h
Patch0: ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/cspublic.BLK_VERSION_150.patch
Patch1: freetds-0.82-shared-libtds.patch
Patch2: freetds-0.82-libtool.patch
Patch3: %{name}-%{version}-aix.patch
Patch4: %{name}-%{version}-gnutls.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: unixODBC-devel >= 2.2.14, readline-devel >= 5.2
BuildRequires: gnutls-devel >= 2.6.6
BuildRequires: autoconf, automake, libtool, m4, make
Requires: unixODBC >= 2.2.14, readline >= 5.2, gnutls >= 2.6.6

%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%package doc
Summary: Development documentation for %{name}
Group: Documentation

%description doc
This package contains the development documentation for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-doc.


%prep 
%setup -q
export PATH=/opt/freeware/bin:$PATH
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


# required to make shared libraries work for all libs
autoreconf

# correct perl path
sed -i '1 s,#!.*/perl,#!%{_bindir}/perl,' samples/*.pl

chmod -x samples/*.sh

# eemove bogus libtool-related macros
rm -f m4/lib-*.m4

# needed after patch0 ...
autoreconf -f -i

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
CC_prev=$CC
export CC="$CC -q64 -Dinline=__inline"

# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
cd 64bit
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-odbc \
    --enable-msdblib \
    --enable-sybase-compat \
    --with-tdsver="4.2" \
    --with-unixodbc=%{_prefix} \
    --with-gnutls
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export CC="$CC_prev -Dinline=__inline"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-odbc \
    --enable-msdblib \
    --enable-sybase-compat \
    --with-tdsver="4.2" \
    --with-unixodbc=%{_prefix} \
    --with-gnutls
gmake %{?_smp_mflags}

 
%install 
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

# move architecture-dependent header file
mv -f ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h \
      ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public-ppc64.h

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

# move architecture-dependent header file
mv -f ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h \
      ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public-ppc32.h

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
export AR="ar -X64"
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libct.a ../64bit/src/ctlib/.libs/libct.so.4
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libsybdb.a ../64bit/src/dblib/.libs/libsybdb.so.5
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libtds-0.82.a ../64bit/src/tds/.libs/libtds-0.82.so
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libtdsodbc.a ../64bit/src/odbc/.libs/libtdsodbc.so.0

rm -f samples/Makefile* samples/*.in samples/README

mv -f samples/unixodbc.freetds.driver.template \
      samples/unixodbc.freetds.driver.template-64bit

# install the wrapper tds_sysdep_public.h header file
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h
chmod 0644 ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h

(
  cd ${RPM_BUILD_ROOT}%{_libdir}

  for f in *.a ; do
      /usr/bin/ar -X32 -x ${f}
  done
  for f in lib*.so.* ; do
      fn=`echo ${f} | awk '{ print substr($1,1,index($1,"\.so")+2) }'`
      ln -sf ${f} ${fn}
  done

  cd ../lib64
  rm -f *
  for f in ../lib/*.a ; do
      /usr/bin/ar -X64 -x ${f}
  done
  for f in lib*.so.* ; do
      fn=`echo ${f} | awk '{ print substr($1,1,index($1,"\.so")+2) }'`
      ln -sf ${f} ${fn}
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


%clean 
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,system, -) 
%doc 32bit/AUTHORS 32bit/BUGS 32bit/COPYING* 32bit/NEWS 32bit/README
%doc 32bit/TODO 32bit/doc/*.html
%doc 32bit/doc/doc/freetds-%{version}/userguide 32bit/doc/images
%config(noreplace) %{_sysconfdir}/*.conf
%{_bindir}/*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_mandir}/man?/*
/usr/bin/*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*

 
%files devel 
%defattr (-,root,system,-) 
%doc 32bit/samples
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la


%files doc
%defattr (-,root,system,-) 
%doc 32bit/doc/doc/%{name}-%{version}/reference
 

%changelog
* Wed Jun 22 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 0.82-1
- Initial port on Aix5.3 
