# Tests by default. No tests: rpm -ba --define 'dotests 0' nettle*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define sorevnettle 4
%define sorevhogweed 2

Name:           nettle
Version:        2.7.1
Release:        2
Summary:        A low-level cryptographic library
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
Source0:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz
#Source1:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz.asc
Source2:        http://www.lysator.liu.se/~nisse/archive/%{name}-%{version}.tar.gz.sig
Source3:        lib%{name}.so.1-aix32
Source4:        lib%{name}.so.1-aix64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  gmp-devel >= 4.3.2-1, m4
Requires:       /sbin/install-info, info, gmp >= 4.3.2-1

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
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CC="xlc"
export CXX="/usr/vac/bin/xlC_r -q64"
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# first build the 64-bit version
export OBJECT_MODE=64
export CFLAGS="-O2 -q64"

cd 64bit
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir64} \
    --disable-shared

make lib%{name}.a

for name in %{name} ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    ${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorevnettle} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevnettle}
done

make libhogweed.a

for name in hogweed ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    ${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorevhogweed} -bE:lib${name}.exp -L. -lnettle -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevhogweed}
done

make %{?_smp_mflags}


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi


# now build the 32-bit version
export OBJECT_MODE=32
export CFLAGS="-O2 -q32"

cd ../32bit
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir} \
    --disable-shared

make lib%{name}.a

for name in %{name} ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    ${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorevnettle} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevnettle}
done

make libhogweed.a

for name in hogweed ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    ${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorevhogweed} -bE:lib${name}.exp -L. -lnettle -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    /usr/bin/ar -rv lib${name}.a lib${name}.so.%{sorevhogweed}
done

make %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export OBJECT_MODE=64
cd 64bit
make DESTDIR=${RPM_BUILD_ROOT} install

export OBJECT_MODE=32
cd ../32bit
make DESTDIR=${RPM_BUILD_ROOT} install

cd ..

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :


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
          ln -s                      %{_libdir}/lib${lib}.a .
        )
    done
    for lib in hogweed
    do
        /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
        /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${lib}.a  lib${lib}.so.%{sorevhogweed}
        (
          rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/lib${lib}.a
          cd        ${RPM_BUILD_ROOT}%{_libdir64}
          ln -s                      %{_libdir}/lib${lib}.a .
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


rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


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
%doc 64bit/AUTHORS 64bit/ChangeLog 64bit/COPYING* 64bit/NEWS 64bit/README 64bit/TODO
%{_bindir}/*
%{_libdir}/lib*.a
%{_infodir}/%{name}.info.gz
/usr/bin/*
/usr/lib/lib*.a


%files devel
%defattr(-,root,system,-)
%doc 64bit/descore.README 64bit/nettle.html 64bit/nettle.pdf 64bit/COPYING*
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc
/usr/include/%{name}


%changelog
* Tue Jun 21 2016 Maximilien Faure <maximilien.faure@atos.net> - 2.7.1-1
- updated to version 2.7.1 with full 32/64

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
