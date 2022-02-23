%define aprver 1
%define contentdir /var/www
%define localstatedir /var

%bcond_without dotests

# Fail if LFS support isn't present in a 32-bit build, since this
# breaks ABI and the soname doesn't change: see #254241


Summary:    Apache Portable Runtime library
Name:       apr
Version:    1.7.0
Release:    1
License:    Apache Software License
Group:      System Environment/Libraries
URL:        http://apr.apache.org/
Source0:    apr-%{version}.tar.bz2
Source1:    apr.h
Source2:    libapr-1.so.0.5.2_32bit
Source3:    libapr-1.so.0.5.2_64bit
Source1000: %{name}-%{version}-%{release}.build.log 

Patch0:  %{name}-1.5.2-aixconf.patch
Patch1:  %{name}-1.5.2-aix.patch
Patch2:  %{name}-1.7.0-LFS-32bit.patch

BuildRequires: bash
Requires: bash
Requires:libgcc >= 6.3.0-1

Conflicts: httpd <= 2.4.38-1

%define _libdir64 %{_prefix}/lib64


%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

The library is available as 32-bit and 64-bit.


%package devel
Group: Development/Libraries
Summary: APR library development kit
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

Conflicts: httpd-devel <= 2.4.38-1

%description devel
This package provides the support files which can be used to 
build applications using the APR library.  The mission of the
Apache Portable Runtime (APR) is to provide a free library of 
C data structures and routines.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .aixconf
%patch1 -p0

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

cd 32bit
%patch2 -p1 -b .32bits


%build
export CC="/opt/freeware/bin/gcc"
export LTFLAGS="--tag=CC --silent"
export AR="/usr/bin/ar -X32_64"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export CFLAGS="-maix64 -fsigned-char -O2"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
./configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --includedir=%{_includedir}/apr-1 \
    --localstatedir=%{localstatedir} \
    --datadir=%{contentdir} \
    --with-installbuilddir=%{_libdir64}/%{name}-%{aprver}/build \
    --enable-static=no

gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CFLAGS="-maix32 -fsigned-char -D_LARGE_FILES -O2"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure \
    --prefix=%{_sysconfdir}/httpd \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir}/apr-1 \
    --localstatedir=%{localstatedir} \
    --datadir=%{contentdir} \
    --with-installbuilddir=%{_libdir}/%{name}-%{aprver}/build \
    --enable-static=no

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar -X32_64"

#install on 64bit mode
cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}-ppc64.h 

# Archive
cd .libs
$AR -qc -X32_64 libapr-1.a libapr-1.so.0.7.0
mv ../libapr-1.la .
cd ..
ln -s .libs/libapr-1.a .

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

#install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}-ppc32.h 
# Archive
cd .libs
$AR -qc -X32_64 libapr-1.a libapr-1.so.0.7.0
mv ../libapr-1.la .
cd ..
ln -s .libs/libapr-1.a .

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)
cd ..

(
    cp 64bit/.libs/libapr-1.a ${RPM_BUILD_ROOT}/%{_libdir64}
    cp 32bit/.libs/libapr-1.a ${RPM_BUILD_ROOT}/%{_libdir}
    cd ${RPM_BUILD_ROOT}/%{_libdir}
    $AR -xv ../lib64/libapr-1.a
    $AR -qc libapr-1.a  libapr-1.so.0.7.0
    cd ../lib64
    rm libapr-1.a
    ln -s ../lib/libapr-1.a libapr-1.a
)

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_includedir}/%{name}-%{aprver}/%{name}.h


%check
export AR="/usr/bin/ar -X32_64"
%if %{with dotests}

cd 64bit
export OBJECT_MODE=64
export LIBPATH=.libs:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib
( gmake -k check || true )

cd ../32bit
export OBJECT_MODE=32
export LIBPATH=.libs:/opt/freeware/lib:/usr/lib
( gmake -k check || true )

%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/CHANGES 32bit/LICENSE 32bit/NOTICE
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/docs/APRDesign.html 32bit/docs/canonical_filenames.html
%doc 32bit/docs/incomplete_types 32bit/docs/non_apr_programs
%{_bindir}/*
%{_includedir}/*
# %{_libdir}/%{name}.exp
# %{_libdir64}/%{name}.exp
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_libdir}/apr-1/build/*
%{_libdir64}/apr-1/build/*


%changelog
* Mon Feb 10 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.7.0
- New version 1.7.0
- No more provide static library
- Binaries are now on 64 bits by default
- No more provides .so and .la
- Archive .a file now contains shared library
- 32 bits no more use 64 bit variable

* Mon Mar 04 2019 Reshma V Kumar<reskumar@in.ibm.com> 1.5.2-1
- Build for AIX toolbox

* Thu Aug 10 2017 Tony Reix <tony.reix@atos.net> 1.5.2-2
- Remove -bmaxdata for 64bit
- Add build.log file
- Add tests
- Move from xlc to gcc

* Wed Jul 06 2016 Laurent GAY <laurent.gay@atos.net> & Matthieu Sarter <matthieu.sarter.external@atos.net> 1.5.2-1
- Update to version 1.5.2
- improved build environment to fix crashes

* Tue Dec 09 2014 Gerard Visiedo <Gerard.Visiedo@bull;net> 1.5.1-1
- Update to version 1.5.1

* Tue Jul 24 2012 Patricia Cugny <Patricia.Cugny@bull.net> 1.4.6-1
-  Update to version 1.4.6

* Tue Mar 27 2012 Gerard Visiedo <Gerard.Visiedo@bull.net> 1.3.9-3
- Add .pc file into apr-devel package

* Thu Feb 17 2011 Gerard Visiedo <Gerard.Visiedo@bull;net> 1.3.9-2
- Add patch for aix6.1

* Wed Jan 20 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.3.9
- Update to version 1.3.9

* Fri Jul 31 2009 BULL 1.3.7
- Fisrt port for AIX
