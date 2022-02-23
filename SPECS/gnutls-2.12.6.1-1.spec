Summary: A TLS protocol implementation
Name: gnutls
Version: 2.12.6.1
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
BuildRequires: nettle-devel >= 2.1-1
Requires: libgcrypt >= 1.2.4, gettext
Requires: zlib, libtasn1, lzo
Requires: readline >= 5.2
Requires: nettle >= 2.1-1

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

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
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --with-lzo \
    --disable-cxx
make %{?_smp_mflags}

cp libextra/.libs/libgnutls-extra.so.26 .
cp libextra/.libs/libgnutls-openssl.so.27 .
cp lib/.libs/libgnutls.so.26 .

make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --with-lzo \
    --disable-cxx
make %{?_smp_mflags}


%install
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
* Thu Jun 16 2011 Gerard Visiedo <gerard.visiedo@bull.net> -2.12.6.1
- Initial port on Aix5.3
