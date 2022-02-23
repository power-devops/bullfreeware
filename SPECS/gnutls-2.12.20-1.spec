Summary: A TLS protocol implementation
Name: gnutls
Version: 2.12.20
Release: 1
License: LGPL
Group: System Environment/Libraries
URL: http://www.gnutls.org/
Source0: ftp://ftp.gnutls.org/pub/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnutls.org/pub/%{name}/%{name}-%{version}.tar.bz2.sig
Source2: libgnutls-openssl.so.26-aix32
Source3: libgnutls-openssl.so.26-aix64
Patch0: %{name}-%{version}-aix.patch
BuildRequires: libgcrypt-devel >= 1.2.4, gettext
BuildRequires: zlib-devel, libtasn1-devel, lzo-devel
BuildRequires: readline-devel >= 5.2
BuildRequires: nettle-devel >= 2.1-2
BuildRequires: p11-kit-devel >= 0.11-1
Requires: libgcrypt >= 1.2.4, gettext
Requires: zlib, libtasn1, lzo
Requires: readline >= 5.2
Requires: nettle >= 2.1-2
Requires: p11-kit >= 0.11-1

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


%prep
%setup -q
%patch0


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

export CC="/usr/vac/bin/xlc -D_LARGE_FILES"

# first build the 64-bit version
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --with-lzo \
    --with-libnettle-prefix=/opt/freeware \
    --disable-cxx

make %{?_smp_mflags}

cp libextra/.libs/libgnutls-extra.so.26 .
cp libextra/.libs/libgnutls-openssl.so.27 .
cp lib/.libs/libgnutls.so.26 .

make distclean

# now build the 32-bit version
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --with-lzo \
    --with-libnettle-prefix=/opt/freeware \
    --disable-cxx
make %{?_smp_mflags}


%install
export RM="/usr/bin/rm -f"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
export AR="ar -X32_64"
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-extra.a ./libgnutls-extra.so.26
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-openssl.a ./libgnutls-openssl.so.27
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls.a ./libgnutls.so.26

# Add the older (< 2.12.0 version) shared members with different major numbers
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libgnutls-openssl.so.26
/usr/bin/strip -X32 -e libgnutls-openssl.so.26
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-openssl.a libgnutls-openssl.so.26
cp %{SOURCE3} libgnutls-openssl.so.26
/usr/bin/strip -X64 -e libgnutls-openssl.so.26
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgnutls-openssl.a libgnutls-openssl.so.26

cd doc
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info*

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
%doc AUTHORS COPYING README
%{_libdir}/*.a
%{_datadir}/locale/*/*/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/%{name}*
%{_infodir}/pkcs11*
/usr/include/*
/usr/lib/*.la


%files utils
%defattr(-,root,system,-)
%{_bindir}/certtool
%{_bindir}/%{name}*
%{_bindir}/p11tool
%{_bindir}/psktool
%{_bindir}/srptool
%{_mandir}/man1/*
/usr/bin/certtool
/usr/bin/%{name}*
/usr/bin/p11tool
/usr/bin/psktool
/usr/bin/srptool


%changelog
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
