%define sorev 2

Name:           nettle
Version:        2.7
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


%build

#export CC=/usr/vac/bin/xlc_r
export CC=/usr/bin/gcc
export CC_FOR_BUILD="/usr/bin/gcc -maix64"
export CXX=/usr/bin/gcc
export CFLAGS="$CFLAGS -maix64"

export AR="/usr/bin/ar -X32_64"

# hardcode the shared library search patch
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --disable-shared
make lib%{name}.a

for name in %{name} ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    #${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorev} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    ${CC} -maix64 -shared lib${name}.a -o lib${name}.so.%{sorev} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    ${AR} -rv lib${name}.a lib${name}.so.%{sorev}
done

make libhogweed.a

for name in hogweed ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    #${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorev} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp -L. -lnettle
    ${CC} -maix64 -shared lib${name}.a -o lib${name}.so.%{sorev} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib -lgmp -L. -lnettle
    rm -f lib${name}.exp lib${name}.a
    ${AR} -rv lib${name}.a lib${name}.so.%{sorev}
done

make %{?_smp_mflags}

mkdir -p 64
mv lib%{name}.so.%{sorev} libhogweed.so.%{sorev} 64/
make clean

# now build the 32-bit version
export OBJECT_MODE=32
export CC=/usr/bin/gcc
export CC_FOR_BUILD="/usr/bin/gcc"
unset CFLAGS
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --disable-shared
make lib%{name}.a

for name in %{name} ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    #${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorev} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorev} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib -lgmp
    rm -f lib${name}.exp lib${name}.a
    ${AR} -rv lib${name}.a lib${name}.so.%{sorev}
done

make libhogweed.a

for name in hogweed ; do
    /usr/vac/bin/CreateExportList lib${name}.exp lib${name}.a
    #${CC} -qmkshrobj lib${name}.a -o lib${name}.so.%{sorev} -bE:lib${name}.exp -L/opt/freeware/lib -lgmp -L. -lnettle
    ${CC} -shared lib${name}.a -o lib${name}.so.%{sorev} -Wl,-bE:lib${name}.exp -L/opt/freeware/lib -lgmp -L. -lnettle
    rm -f lib${name}.exp lib${name}.a
    ${AR} -rv lib${name}.a lib${name}.so.%{sorev}
done

make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
for name in %{name} hogweed ; do
    /usr/bin/ar -X64 -q lib${name}.a 64/lib${name}.so.%{sorev}
done

# Add the older v1.15 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE3} lib%{name}.so.1
/usr/bin/strip -X32 -e lib%{name}.so.1
/usr/bin/ar -X32 -q lib%{name}.a lib%{name}.so.1

cp %{SOURCE4} lib%{name}.so.1
/usr/bin/strip -X64 -e lib%{name}.so.1
/usr/bin/ar -X64 -q lib%{name}.a lib%{name}.so.1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

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
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%{_bindir}/*
%{_libdir}/lib*.a
%{_infodir}/%{name}.info.gz
/usr/bin/*
/usr/lib/lib*.a


%files devel
%defattr(-,root,system,-)
%doc descore.README nettle.html nettle.pdf COPYING*
%{_includedir}/%{name}
/usr/include/%{name}


%changelog
* Wed Jun 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.7-2
- Initial port on Aix6.1

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
