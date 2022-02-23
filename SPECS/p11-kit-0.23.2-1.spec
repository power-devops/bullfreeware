# Tests by default. No tests: rpm -ba --define 'dotests 0' p11-kit-*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Name:           p11-kit
Version:        0.23.2
Release:        1
Summary:        Library to work with PKCS#11 modules
License:        BSD3c
Group:          Development/Libraries/C and C++
Url:            http://p11-glue.freedesktop.org/%{name}.html
Source0:        http://p11-glue.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1:        http://p11-glue.freedesktop.org/releases/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-%{version}-%{release}.build.log

Patch0:         %{name}-%{version}-aixconf.patch
Patch1:         %{name}-%{version}-dirfd.patch
Patch2:         %{name}-%{version}-getopt_long.patch
Patch3:         %{name}-%{version}-ifdef_OS_UNIX.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

BuildRequires:  gettext
BuildRequires:  pkg-config
Requires:       gettext

%define _libdir64 %{_prefix}/lib64


%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.

The library is available as 32-bit and 64-bit.


%package tools
License:        BSD3c
Summary:        Library to work with PKCS#11 modules -- Tools
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description tools
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.


%package devel
License:        BSD3c
Summary:        Library to work with PKCS#11 modules -- Development Files
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0
%patch1 -p1 -b .dirfd
%patch2 -p1 -b .getopt_long
%patch3 -p1 -b .ifdef_OS_UNIX

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
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CC="xlc"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CFLAGS="-O2 -q64"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --without-trust-paths \
    --enable-shared --disable-static

#gmake --trace %{?_smp_mflags}
gmake %{?_smp_mflags}


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
    /usr/sbin/slibclean
fi


cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export CFLAGS="-O2 -q32"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --without-trust-paths \
    --enable-shared --disable-static

gmake %{?_smp_mflags}


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so*

# Create pkcs11 config directory
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/pkcs11/modules

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
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/COPYING 32bit/NEWS 32bit/README
%dir %{_sysconfdir}/pkcs11/
%dir %{_sysconfdir}/pkcs11/modules/
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*


%files tools
%defattr(-,root,system)
%{_bindir}/p11-kit*
/usr/bin/p11-kit*


%files devel
%defattr(-,root,system)
%doc %dir %{_datadir}/gtk-doc
%doc %dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/gtk-doc/html/p11-kit/
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/include/*


%changelog
* Thu Jun 23 2016 Maximilien Faure <maximilien.faure@atos.net> - 0.23.2-2
- updated to version 0.23.2

* Wed Jun 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 0.14-2
- Initial port on Aix6.1

* Mon Sep 17 2012 Michael Perzl <michael@perzl.org> - 0.14-1
- updated to version 0.14

* Fri Mar 16 2012 Michael Perzl <michael@perzl.org> - 0.12-1
- updated to version 0.12

* Fri Mar 16 2012 Michael Perzl <michael@perzl.org> - 0.11-1
- updated to version 0.11

* Mon Nov 21 2011 Michael Perzl <michael@perzl.org> - 0.9-1
- updated to version 0.9

* Thu Oct 06 2011 Michael Perzl <michael@perzl.org> - 0.7-1
- updated to version 0.7

* Wed Sep 21 2011 Michael Perzl <michael@perzl.org> - 0.6-1
- updated to version 0.6

* Wed Sep 07 2011 Michael Perzl <michael@perzl.org> - 0.5-1
- updated to version 0.5

* Sun Aug 21 2011 Michael Perzl <michael@perzl.org> - 0.4-1
- updated to version 0.4

* Tue Aug 09 2011 Michael Perzl <michael@perzl.org> - 0.3-1
- first version for AIX V5.1 and higher
