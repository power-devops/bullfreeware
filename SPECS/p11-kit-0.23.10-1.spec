# Tests by default. No tests: rpm -ba --define 'dotests 0' p11-kit-*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Name:           p11-kit
Version:        0.23.10
Release:        1
Summary:        Library for loading and sharing PKCS#11 modules
License:        BSD
Group:          Development/Libraries/C and C++
URL:            http://p11-glue.freedesktop.org/%{name}.html

Source0:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/p11-glue/p11-kit/releases/download/%{version}/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-%{version}-%{release}.build.log

Patch0:         %{name}-0.23.10-aixconf.patch
Patch1:         %{name}-0.23.2-dirfd.patch
Patch2:         %{name}-0.23.2-getopt_long.patch
Patch3:         %{name}-0.23.2-ifdef_OS_UNIX.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

BuildRequires:  gettext
BuildRequires:  pkg-config
Requires:       gettext

Obsoletes:      p11-kit-tools

%define _libdir64 %{_prefix}/lib64


%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they are discoverable.

The library is available as 32-bit and 64-bit.


# %package tools
# License:        BSD
# Summary:        Library to work with PKCS#11 modules -- Tools
# Group:          Development/Libraries/C and C++
# Requires:       %{name} = %{version}
# 
# %description tools
# p11-kit provides a way to load and enumerate PKCS#11 modules, as well
# as a standard configuration setup for installing PKCS#11 modules in
# such a way that they're discoverable.


%package devel
License:        BSD
Summary:        Development files for p11-kit
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
The p11-kit-devel package contains libraries and header files for
developing applications that use p11-kit.

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
export LDFLAGS="-lp11-kit -L./p11-kit/.libs -L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
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
export LDFLAGS="-lp11-kit -L./p11-kit/.libs -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
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
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
unset LDFLAGS

make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)
(
  cd ${RPM_BUILD_ROOT}%{_libexecdir}/p11-kit
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
unset LDFLAGS

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

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}/pkcs11
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done

  cd ${RPM_BUILD_ROOT}%{_libdir}/pkcs11
  for f in *.a ; do
    /usr/bin/ar -X32 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so*

/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/pkcs11/%{name}-client.a ${RPM_BUILD_ROOT}%{_libdir64}/pkcs11/%{name}-client.so*

/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/pkcs11/%{name}-trust.a ${RPM_BUILD_ROOT}%{_libdir64}/pkcs11/%{name}-trust.so*

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
# [ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/COPYING 32bit/NEWS 32bit/README
%doc 32bit/p11-kit/pkcs11.conf.example
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit/
%dir %{_datadir}/p11-kit/modules/
%dir %{_libexecdir}/p11-kit
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.so*
%{_libexecdir}/p11-kit/p11-kit-remote*
%{_libexecdir}/p11-kit/p11-kit-server*
%{_libexecdir}/p11-kit/trust-extract-compat
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libdir}/pkcs11/p11-kit-trust.a
%{_libdir}/pkcs11/p11-kit-client.a


# %files tools - fold into the main p11-kit RPM
# %defattr(-,root,system)
%{_bindir}/p11-kit*
/usr/bin/p11-kit*


%files devel
%defattr(-,root,system)
%doc %dir %{_datadir}/gtk-doc
%doc %dir %{_datadir}/gtk-doc/html
%doc %{_datadir}/gtk-doc/html/p11-kit/
# %{_includedir}/*
%{_includedir}/p11-kit-1
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
/usr/include/*


%changelog
* Tue Apr 17 2018 Michael Wilson <michael.a.wilson@atos.net> - 0.23.10-1
- updated to version 0.23.10
- required by package ca-certificates-2018.03.26 for creating bundles
- inspired by Fedora packaging, without p11-kit-trust and p11-kit-server RPMs
- inspired by Fedora packaging to move p11-kit-tools content into p11-kit RPM

* Thu Jun 23 2016 Maximilien Faure <maximilien.faure@atos.net> - 0.23.2-1
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
