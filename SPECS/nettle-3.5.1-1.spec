%bcond_without dotests

%define sorevnettle 6
%define sorevhogweed 4

Name:           nettle
Version:        3.5.1
Release:        1
Summary:        A low-level cryptographic library
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/

Source0:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz
Source2:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz.sig
Source3:        lib%{name}.so.1-aix32
Source4:        lib%{name}.so.1-aix64
Source5:        lib%{name}.so.4-aix32
Source6:        lib%{name}.so.4-aix64
Source7:        libhogweed.so.2-aix32
Source8:        libhogweed.so.2-aix64
Source9:        lib%{name}.so.2-aix32
Source10:       lib%{name}.so.2-aix64
#Source11:        nettle-3.2-3.spec.res3
Source1000: %{name}-%{version}-%{release}.build.log

BuildRequires:  gmp-devel >= 4.3.2-1, m4
BuildRequires:  texinfo
Requires:       /sbin/install-info, info, gmp >= 4.3.2-1
Requires:       libgcc >= 6.3.0

%define _libdir64 %{_prefix}/lib64


%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

The library is available as 32-bit and 64-bit.


%package devel
Summary:        Development headers for a low-level cryptographic library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains kernel headers.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
# hardcode the shared library search patch
export CC="gcc -maix64" 
export CFLAGS="-O2"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

cd 64bit

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir64} \
    --disable-shared

gmake lib%{name}.a

for name in %{name} ; do
    `echo /usr/bin/nm -X32_64 | /usr/bin/sed -e 's/B\([^B]*\)$/P\1/'` -PCpgl lib${name}.a | \
    /usr/bin/awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) \
    && (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } \
    else { print $ 1 } } }' | /usr/bin/sort -u > lib${name}.exp
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorevnettle} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib64 -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevnettle}
done

gmake libhogweed.a

for name in hogweed ; do
    `echo /usr/bin/nm -X32_64 | /usr/bin/sed -e 's/B\([^B]*\)$/P\1/'` -PCpgl lib${name}.a | \
    /usr/bin/awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) \
    && (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } \
    else { print $ 1 } } }' | /usr/bin/sort -u > lib${name}.exp 
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorevhogweed} -Wl,-bE:lib${name}.exp -L. -lnettle -L/opt/freeware/lib64 -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevhogweed}
done

gmake %{?_smp_mflags}

# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-O2"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

cd ../32bit

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir} \
    --disable-shared

gmake lib%{name}.a

for name in %{name} ; do
    `echo /usr/bin/nm -X32_64 | /usr/bin/sed -e 's/B\([^B]*\)$/P\1/'` -PCpgl lib${name}.a | \
    /usr/bin/awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) \
    && (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } \
    else { print $ 1 } } }' | /usr/bin/sort -u > lib${name}.exp
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorevnettle} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevnettle}
done

gmake libhogweed.a

for name in hogweed ; do
    `echo /usr/bin/nm -X32_64 | /usr/bin/sed -e 's/B\([^B]*\)$/P\1/'` -PCpgl lib${name}.a | \
    /usr/bin/awk '{ if ((($ 2 == "T") || ($ 2 == "D") || ($ 2 == "B") || ($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) \
    && (substr($ 1,1,1) != ".")) { if (($ 2 == "W") || ($ 2 == "V") || ($ 2 == "Z")) { print $ 1 " weak" } \
    else { print $ 1 } } }' | /usr/bin/sort -u > lib${name}.exp
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorevhogweed} -Wl,-bE:lib${name}.exp -L. -lnettle -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevhogweed}
done

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

#installing 64bit

export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

#stripping 64bit binaries
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

#renaming 64bit 
(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_64
    done
)

#installing  32bit 
export OBJECT_MODE=32
cd ../32bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ..

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
        mv $fic "$fic"_32
        ln -sf "$fic"_64 $fic
    done
)



# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
(
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for lib in %{name}
    do
    /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
        /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${lib}.a  lib${lib}.so.%{sorevnettle}
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
          cd        ${RPM_BUILD_ROOT}%{_libdir64}
          ln -s                      ../lib/lib${lib}.a .
        )
    done
    for lib in hogweed
    do
        /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
        /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${lib}.a  lib${lib}.so.%{sorevhogweed}
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
          cd        ${RPM_BUILD_ROOT}%{_libdir64}
          ln -s                      ../lib/lib${lib}.a .
        )
    done
)


# Add the older v1.15 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE4}                                                   lib%{name}.so.1
/usr/bin/strip -X64 -e                                          lib%{name}.so.1
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.1

cp %{SOURCE3}                                                   lib%{name}.so.1
/usr/bin/strip -X32 -e                                          lib%{name}.so.1
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.1

cp %{SOURCE6}                                                   lib%{name}.so.4
/usr/bin/strip -X64 -e                                          lib%{name}.so.4
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.4

cp %{SOURCE5}                                                   lib%{name}.so.4
/usr/bin/strip -X32 -e                                          lib%{name}.so.4
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.4

cp %{SOURCE10}                                                  lib%{name}.so.2
/usr/bin/strip -X64 -e                                          lib%{name}.so.2
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.2

cp %{SOURCE9}                                                   lib%{name}.so.2
/usr/bin/strip -X32 -e                                          lib%{name}.so.2
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a lib%{name}.so.2

cp %{SOURCE8}                                                   libhogweed.so.2
/usr/bin/strip -X64 -e                                          libhogweed.so.2
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libhogweed.a libhogweed.so.2

cp %{SOURCE7}                                                   libhogweed.so.2
/usr/bin/strip -X32 -e                                          libhogweed.so.2
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libhogweed.a libhogweed.so.2

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info || :

%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
export LIBPATH=${RPM_BUILD_ROOT}%{_libdir64}
(gmake -k check LDFLAGS="-L${RPM_BUILD_ROOT}%{_libdir64}" || true)

cd ../32bit
export OBJECT_MODE=32
export LIBPATH=${RPM_BUILD_ROOT}%{_libdir}
(gmake -k check LDFLAGS="-L${RPM_BUILD_ROOT}%{_libdir64}" || true)
%endif


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 64bit/AUTHORS 64bit/ChangeLog 64bit/COPYING* 64bit/NEWS 64bit/README
%{_bindir}/*
%{_libdir}/lib*.a
%{_libdir64}/lib*.a
%{_infodir}/%{name}.info.gz


%files devel
%defattr(-,root,system,-)
%doc 64bit/descore.README 64bit/nettle.html 64bit/nettle.pdf 64bit/COPYING*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_includedir}/%{name}



%changelog
* Mon Mar 30 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.5.1-1
- Updated to 3.5.1
- No more provide link to /usr
- Provide %{_libdir64}

* Mon Apr 29 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 3.4.1
- Updated to 3.4.1 to fix security vulnerability
- Built with gcc
- Made 64bit as default
- Removed libnettle.so.1, as it is not required for any package

* Tue Feb 06 2018 Ravi Hirekurabar<rhirekur@in.ibm.com> - 3.4.0
- Updated to 3.4.0

* Wed Aug 10 2016 Tony Reix <tony.reix@atos.net> - 3.2-4
- Add libnettle.so.2 from version 2.7-2

* Tue Jun 21 2016 Maximilien Faure <maximilien.faure@atos.net> - 3.2
- updated to version 3.2 with full 32/64

* Wed May 29 2013 Michael Perzl <michael@perzl.org> - 2.7.1-1
- updated to version 2.7.1

* Fri Apr 26 2013 Michael Perzl <michael@perzl.org> - 2.7-1
- updated to version 2.7

* Thu Jan 17 2013 Michael Perzl <michael@perzl.org> - 2.6-1
- updated to version 2.6

* Sat Jul 07 2012 Michael Perzl <michael@perzl.org> - 2.5-1
- updated to version 2.5

* Wed Sep 07 2011 Michael Perzl <michael@perzl.org> - 2.4-1
- updated to version 2.4

* Wed Jul 13 2011 Michael Perzl <michael@perzl.org> - 2.2-1
- updated to version 2.2

* Wed Apr 13 2011 Michael Perzl <michael@perzl.org> - 2.1-2
- missed to include libhogweed

* Tue Mar 29 2011 Michael Perzl <michael@perzl.org> - 2.1-1
- updated to version 2.1

* Tue Mar 29 2011 Michael Perzl <michael@perzl.org> - 1.15-2
- fixed shared library search path in binaries

* Fri Apr 17 2009 Michael Perzl <michael@perzl.org> - 1.15-1
- first version for AIX V5.1 and higher
