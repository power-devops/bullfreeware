%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 1.1.26
Release: 1
Group: System Environment/Libraries
License: LGPLv2+ and GPLv2+
URL: http://www.freetds.org/
Source0: ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.gz
Source2: freetds-tds_sysdep_public.h
Source1000: %{name}-%{version}-%{release}.build.log

BuildRequires: sed
BuildRequires: unixODBC-devel, readline-devel
BuildRequires: gnutls-devel, krb5-devel
BuildRequires: autoconf, automake, libtool, m4, make
Requires: unixODBC, readline, gnutls, krb5-libs


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


# # Do not provide doc (generate with doxygen we do not have)
# %package doc
# Summary: Development documentation for %{name}
# Group: Documentation
# 
# %description doc
# This package contains the development documentation for %{name}.
# If you like to develop programs using %{name}, you will need to install
# %{name}-doc.


%prep 
%setup -q
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export PATH=/opt/freeware/bin:$PATH

# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lgcrypt"
cd 64bit
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-tdsver="auto" \
    --enable-odbc \
    --enable-msdblib \
    --enable-sybase-compat \
    --with-unixodbc=%{_prefix} \
    --with-gnutls \
    --enable-krb5
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lgcrypt"

# odbc_config is 64 bits and add /opt/freeware/lib64 on path.
# Use odbc_config_32 instead
sed -i 's|odbc_config|odbc_config_32|g' configure

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --with-tdsver="auto" \
    --enable-odbc \
    --enable-msdblib \
    --enable-sybase-compat \
    --with-unixodbc=%{_prefix} \
    --with-gnutls \
    --enable-krb5
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

(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls -1 | grep -v -e _32 -e _64) ; do
        mv ${f} ${f}_32
        ln -sf ${f}_64 ${f}
    done
)

# move architecture-dependent header file
mv -f ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h \
      ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public-ppc32.h

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
export AR="ar -X64"
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libct.a ../64bit/src/ctlib/.libs/libct.so.4
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libsybdb.a ../64bit/src/dblib/.libs/libsybdb.so.5
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libtdsodbc.a ../64bit/src/odbc/.libs/libtdsodbc.so.0

(
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/*.a .
)

rm -f samples/Makefile* samples/*.in samples/README

mv -f samples/unixodbc.freetds.driver.template \
      samples/unixodbc.freetds.driver.template-64bit

# install the wrapper tds_sysdep_public.h header file
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h
chmod 0644 ${RPM_BUILD_ROOT}%{_includedir}/tds_sysdep_public.h

# (
#   cd ${RPM_BUILD_ROOT}%{_libdir}
# 
#   for f in *.a ; do
#       /usr/bin/ar -X32 -x ${f}
#   done
#   for f in lib*.so.* ; do
#       fn=`echo ${f} | awk '{ print substr($1,1,index($1,"\.so")+2) }'`
#       ln -sf ${f} ${fn}
#   done
# 
#   cd ../lib64
#   rm -f *
#   for f in ../lib/*.a ; do
#       /usr/bin/ar -X64 -x ${f}
#   done
#   for f in lib*.so.* ; do
#       fn=`echo ${f} | awk '{ print substr($1,1,index($1,"\.so")+2) }'`
#       ln -sf ${f} ${fn}
#   done
# )

# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin include lib lib64
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
gmake check || true

cd ../32bit
export OBJECT_MODE=32
gmake check || true
%endif


%clean 
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,system,-)
%doc 32bit/AUTHORS* 32bit/BUGS* 32bit/COPYING* 32bit/NEWS 32bit/README*
%config(noreplace) %{_sysconfdir}/*.conf
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man?/*


%files devel 
%defattr(-,root,system,-)
%doc 32bit/samples
%{_includedir}/*


# %files doc
# %defattr(-,root,system,-)
# # %doc 32bit/doc/doc/freetds-%{version}/userguide
# # %doc 32bit/doc/doc/%{name}-%{version}/reference
# %doc 32bit/doc/userguide
# %doc 32bit/doc/reference
# %doc 32bit/doc/images
# %doc 32bit/TODO 32bit/doc/*.html


%changelog
* Mon Mar 30 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.1.26-1
- New version 1.1.26
- Build with new unixODBC
- Add check
- No more provide link to /usr
- Binaries are 64 bits by default
- Do not provide doc (generate with doxygen we do not have)

* Mon Nov 12 2012 Michael Perzl <michael@perzl.org> - 0.92.79-1
- updated to version 0.92.47

* Mon Nov 12 2012 Michael Perzl <michael@perzl.org> - 0.91.49-1
- updated to version 0.91.49

* Fri Dec 03 2010 Michael Perzl <michael@perzl.org> - 0.82-2
- fixed 64-bit issue

* Fri Nov 05 2010 Michael Perzl <michael@perzl.org> - 0.82-1
- first version for AIX5L v5.1 and higher
