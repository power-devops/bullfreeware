# Tests by default. No tests: rpm -ba --define 'dotests 0' gnutls*.spec
%{!?dotests: %define dotests 1}


%define srp 1

# Files not built...
%define guile 0

Summary: A TLS protocol implementation
Name: gnutls
Version: 3.4.17
Release: 1
License: LGPL
Group: System Environment/Libraries
URL: http://www.gnutls.org/
Source0: ftp://ftp.gnutls.org/gcrypt/gnutls/%{name}-%{version}.tar.xz
Source1: ftp://ftp.gnutls.org/gcrypt/gnutls/%{name}-%{version}.tar.xz.sig
Source2: libgnutls-openssl.so.26-aix32
Source3: libgnutls-openssl.so.26-aix64
Source4: libgnutls.so.26-aix32 
Source5: libgnutls.so.26-aix64

Source100: %{name}-%{version}-%{release}.build.log


Patch0: %{name}-2.12.20-aix.patch 
Patch1: %{name}-3.4.17-netstat.patch
# Patches from 3.4.12-1.fc24
Patch2: %{name}-3.2.7-rpath.patch
Patch3: %{name}-3.1.11-nosrp.patch
Patch4: %{name}-3.4.1-default-policy.patch
Patch5: %{name}-3.4.2-no-now-guile.patch
# Patches from 3.4.17-1.fc24
Patch6: %{name}-3.4.17-various-flaws1.patch

%define _libdir64 %{_prefix}/lib64

BuildRequires: libgcrypt-devel >= 1.2.4, gettext
BuildRequires: zlib-devel, libtasn1-devel >= 4.3, lzo-devel
BuildRequires: readline-devel >= 5.2
BuildRequires: nettle-devel >= 3.1.1
BuildRequires: p11-kit-devel >= 0.21.3
BuildRequires: autogen-libopts-devel >= 5.18 autogen >= 5.18

%if %{guile} == 1
BuildRequires: guile-devel
%endif

Requires: libgcrypt >= 1.2.4, gettext
Requires: zlib, libtasn1 >= 4.3, lzo
Requires: readline >= 5.2
Requires: nettle >= 3.1.1
Requires: p11-kit >= 0.21.3

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development files for the %{name} package.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel, zlib-devel
Requires: libtasn1-devel, lzo-devel
Requires: pkg-config, info, gettext
Requires: /sbin/install-info

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%package utils
Summary: Command line tools for TLS protocol.
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description utils
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains command line TLS client and server and certificate
manipulation tools.


%if %{guile} == 1
%package guile
Summary: Guile bindings for the GNUTLS library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: guile

%description guile
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS
protocols and technologies around them. It provides a simple C language
application programming interface (API) to access the secure communications
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and
other required structures.
This package contains Guile bindings for the library.
%endif


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0
%patch1 -p1 -b .netstat
%patch2 -p1 -b .rpath
%patch3 -p1 -b .nosrp
%patch4 -p1 -b .default-policy
%patch5 -p1 -b .guile
%patch6 -p1 -b .various-flaws

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
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CFLAGS="-D_LINUX_SOURCE_COMPAT -g -O2"

# first build the 64-bit version
cd 64bit

#export CC="xlc -q64 -D_LARGE_FILES"
export CC="gcc -maix64 -D_LARGE_FILES"
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static \
%if %{srp} == 0
    --disable-srp-authentication \
%endif
    --with-p11-kit \
    --with-default-trust-store-pkcs11="pkcs11:model=p11-kit-trust;manufacturer=PKCS%2311%20Kit" \
    --without-tpm \
    --disable-cxx \
    --disable-libdane \
    --disable-rpath \
%if %{guile} == 1
           --enable-guile \
%else
           --disable-guile \
%endif
    --enable-openssl-compatibility

gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    (gmake -k check || true)
fi


# now build the 32-bit version
cd ../32bit

#export CC="xlc -q32 -D_LARGE_FILES"
export CC="gcc -maix32 -D_LARGE_FILES"
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32

echo "GCC: "
gcc --version

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --libdir=%{_libdir} \
    --enable-shared --enable-static \
%if %{srp} == 0
    --disable-srp-authentication \
%endif
    --with-p11-kit \
    --with-default-trust-store-pkcs11="pkcs11:model=p11-kit-trust;manufacturer=PKCS%2311%20Kit" \
    --without-tpm \
    --disable-cxx \
    --disable-libdane \
    --disable-rpath \
%if %{guile} == 1
           --enable-guile \
%else
           --disable-guile \
%endif
    --enable-openssl-compatibility

gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    (gmake -k check || true)
fi


%install

export RM="/usr/bin/rm -f"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in certtool gnutls-cli gnutls-cli-debug gnutls-serv psktool srptool
  do
    mv ${f} ${f}_64
  done
)


cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in certtool gnutls-cli gnutls-cli-debug gnutls-serv psktool srptool
  do
    mv ${f} ${f}_32
  done
)


# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in certtool gnutls-cli gnutls-cli-debug gnutls-serv psktool srptool
  do
    ln -sf ${f}_64 ${f}
  done
)


# Add the older (< 2.12.0 version) shared members with different major numbers
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libgnutls-openssl.so.26
/usr/bin/strip -X32 -e                                                 libgnutls-openssl.so.26
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-openssl.a libgnutls-openssl.so.26
cp %{SOURCE3}                                                          libgnutls-openssl.so.26
/usr/bin/strip -X64 -e                                                 libgnutls-openssl.so.26
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-openssl.a libgnutls-openssl.so.26

cp %{SOURCE4}                                                          libgnutls.so.26
/usr/bin/strip -X32 -e                                                 libgnutls.so.26
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls.a         libgnutls.so.26
cp %{SOURCE5}                                                          libgnutls.so.26
/usr/bin/strip -X64 -e                                                 libgnutls.so.26
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls.a         libgnutls.so.26

#add 64bit to libgnutls.a
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libgnutls.a          libgnutls.so.30
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir  }/libgnutls.a          libgnutls.so.30

#add 64bit to libgnutls-openssl.a
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libgnutls-openssl.a  libgnutls-openssl.so.27 
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir  }/libgnutls-openssl.a  libgnutls-openssl.so.27


# Make 64bit .a a symlink of 32bit .a
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  rm -f *.a
  ln -sf %{_libdir}/libgnutls.a .
  ln -sf %{_libdir}/libgnutls-openssl.a .
)


cd doc
gmake DESTDIR=${RPM_BUILD_ROOT} install

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*

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


%post devel
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 -eq 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/README
%{_libdir}/*.a
%{_datadir}/locale/*/*/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/%{name}*
%{_infodir}/pkcs11*
/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


%files utils
%defattr(-,root,system,-)
%{_bindir}/certtool*
%{_bindir}/%{name}*
%{_bindir}/p11tool*
%{_bindir}/psktool*
%if %{srp} == 1
%{_bindir}/srptool*
%endif
%{_mandir}/man1/*
/usr/bin/certtool*
/usr/bin/%{name}*
/usr/bin/p11tool*
/usr/bin/psktool*
%if %{srp} == 1
/usr/bin/srptool*
%endif


%if %{guile} == 1
%files guile
%defattr(-,root,root,-)
%{_libdir}/guile/2.0/guile-gnutls*.so*
%{_libdir64}/guile/2.0/guile-gnutls*.so*
%{_datadir}/guile/site/gnutls
%{_datadir}/guile/site/gnutls.scm
%{_libdir}/guile/2.0/site-ccache/gnutls.go
%{_libdir}/guile/2.0/site-ccache/gnutls/extra.go
%endif


%changelog
* Thu Apr 06 2017 Michael Wilson <michael.a.wilson@atos.net> - 3.4.17-1
- Updated to version 3.4.17
- Issue with exit functions and gnutls_rnd_ctx in previous versions

* Thu Oct 13 2016 Tony Reix <tony.reix@atos.net> - 3.4.16-1
- Updated to version 3.4.16

* Wed Sep 14 2016 Tony Reix <tony.reix@atos.net> - 3.4.15-3
- Fix issue with compatibility of libgnutls.so.26

* Wed Sep 14 2016 Tony Reix <tony.reix@atos.net> - 3.4.15-2
- Update/Improve Requires based on 3.4.12-1.fc24
- Add %package guile
- Add patches from 3.4.12-1.fc24
- Update configure based on 3.4.12-1.fc24
- Add With p11-kit
- With srp
- No guile package for now
- Add X.build.log to src.rpm
- Use autogen 5.18.7
- Add 32.64 bit executables

* Tue Sep 13 2016 Tony Reix <tony.reix@atos.net> - 3.4.15-1
- Updated to version 3.4.15
- Fix issue with missing 32bit libgnutls.so.30 in libgnutls.a .

* Thu Jun 23 2016 Maximilien Faure <maximilien.faure@atos.net> - 3.4.13-1
- updated to version 3.4.13

* Wed May 04 2016 Tony Reix <tony.reix@bull.net> - 3.4.11-1
- updated to version 3.4.11

* Sun Jun 10 2012 Michael Perzl <michael@perzl.org> - 2.12.20-1
- updated to version 2.12.20

* Sun May 06 2012 Michael Perzl <michael@perzl.org> - 2.12.19-1
- updated to version 2.12.19

* Fri Mar 16 2012 Michael Perzl <michael@perzl.org> - 2.12.18-1
- updated to version 2.12.18

* Fri Jan 27 2012 Michael Perzl <michael@perzl.org> - 2.12.16-1
- updated to version 2.12.16

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 2.12.14-1
- updated to version 2.12.14

* Tue Nov 08 2011 Michael Perzl <michael@perzl.org> - 2.12.13-1
- updated to version 2.12.13

* Fri Oct 21 2011 Michael Perzl <michael@perzl.org> - 2.12.12-1
- updated to version 2.12.12

* Wed Sep 21 2011 Michael Perzl <michael@perzl.org> - 2.12.11-1
- updated to version 2.12.11

* Wed Sep 07 2011 Michael Perzl <michael@perzl.org> - 2.12.10-1
- updated to version 2.12.10

* Sun Aug 21 2011 Michael Perzl <michael@perzl.org> - 2.12.9-1
- updated to version 2.12.9

* Mon Aug 08 2011 Michael Perzl <michael@perzl.org> - 2.12.8-1
- updated to version 2.12.8

* Mon Jun 20 2011 Michael Perzl <michael@perzl.org> - 2.12.7-1
- updated to version 2.12.7

* Sun Jun 05 2011 Michael Perzl <michael@perzl.org> - 2.12.6.1-1
- updated to version 2.12.6.1

* Sat May 14 2011 Michael Perzl <michael@perzl.org> - 2.12.5-1
- updated to version 2.12.5

* Fri May 06 2011 Michael Perzl <michael@perzl.org> - 2.12.4-1
- updated to version 2.12.4

* Fri Apr 22 2011 Michael Perzl <michael@perzl.org> - 2.12.3-1
- updated to version 2.12.3

* Sun Apr 10 2011 Michael Perzl <michael@perzl.org> - 2.12.2-1
- updated to version 2.12.2

* Sat Apr 02 2011 Michael Perzl <michael@perzl.org> - 2.12.1-1
- updated to version 2.12.1

* Fri Mar 25 2011 Michael Perzl <michael@perzl.org> - 2.12.0-1
- updated to version 2.12.0

* Tue Mar 01 2011 Michael Perzl <michael@perzl.org> - 2.10.5-1
- updated to version 2.10.5

* Mon Dec 06 2010 Michael Perzl <michael@perzl.org> - 2.10.4-1
- updated to version 2.10.4

* Fri Nov 19 2010 Michael Perzl <michael@perzl.org> - 2.10.3-1
- updated to version 2.10.3

* Thu Sep 30 2010 Michael Perzl <michael@perzl.org> - 2.10.2-1
- updated to version 2.10.2

* Mon Jul 26 2010 Michael Perzl <michael@perzl.org> - 2.10.1-1
- updated to version 2.10.1

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 2.10.0-1
- updated to version 2.10.0

* Tue Jul 06 2010 Michael Perzl <michael@perzl.org> - 2.8.6-2
- removed dependency on gettext >= 0.17

* Tue Mar 23 2010 Michael Perzl <michael@perzl.org> - 2.8.6-1
- updated to version 2.8.6

* Fri Nov 06 2009 Michael Perzl <michael@perzl.org> - 2.8.5-1
- updated to version 2.8.5

* Wed Sep 23 2009 Michael Perzl <michael@perzl.org> - 2.8.4-1
- updated to version 2.8.4

* Tue Aug 18 2009 Michael Perzl <michael@perzl.org> - 2.8.3-1
- updated to version 2.8.3

* Fri Jun 05 2009 Michael Perzl <michael@perzl.org> - 2.6.6-1
- updated to version 2.6.6

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 2.6.4-1
- updated to version 2.6.4

* Sat Nov 08 2008 Michael Perzl <michael@perzl.org> - 2.6.0-1
- updated to version 2.6.0

* Sat Nov 08 2008 Michael Perzl <michael@perzl.org> - 2.4.2-1
- updated to version 2.4.2

* Wed Oct 01 2008 Michael Perzl <michael@perzl.org> - 2.4.1-1
- updated to version 2.4.1

* Tue Jun 24 2008 Michael Perzl <michael@perzl.org> - 2.2.5-1
- updated to version 2.2.5

* Tue Jun 24 2008 Michael Perzl <michael@perzl.org> - 2.2.4-1
- updated to version 2.2.4

* Fri May 16 2008 Michael Perzl <michael@perzl.org> - 2.2.3-1
- updated to version 2.2.3

* Tue Apr 01 2008 Michael Perzl <michael@perzl.org> - 2.2.2-3
- linked against new version of readline

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 2.2.2-2
- corrected some SPEC file errors

* Mon Mar 03 2008 Michael Perzl <michael@perzl.org> - 2.2.2-1
- updated to version 2.2.2

* Wed Feb 20 2008 Michael Perzl <michael@perzl.org> - 2.2.1-1
- updated to version 2.2.1

* Mon Jan 07 2008 Michael Perzl <michael@perzl.org> - 2.2.0-2
- included both 32-bit and 64-bit shared objects

* Tue Dec 18 2007 Michael Perzl <michael@perzl.org> - 2.2.0-1
- First version for AIX5L v5.1 and higher
