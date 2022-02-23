Summary: libgpg-error
Name: libgpg-error
Version: 1.10
Release: 2
URL: ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0: %{name}-%{version}-mkstrtable.patch
Group: Development/Libraries
Copyright: LGPL
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: gettext, make
Requires: gettext

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future. This package
contains files necessary to develop applications using libgpg-error.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0 -p1 -b .mkstrtable


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
CC_prev="$CC"
export CC="$CC -q64"
export CFLAGS="-O2"
LIBPATH="%{_prefix}/lib64:%{_libdir}:/usr/lib64:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

cp src/.libs/libgpg-error.so.0 .
make distclean

# now build the 32-bit version
export CC="$CC_prev"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libgpg-error.a ./libgpg-error.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

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


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc COPYING COPYING.LIB AUTHORS README INSTALL NEWS ChangeLog
%{_bindir}/gpg-error
%{_libdir}/*.a
%{_datadir}/locale/*
%{_datadir}/common-lisp/*
/usr/bin/gpg-error
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/gpg-error-config
%{_libdir}/*.la
%{_includedir}/*
%{_datadir}/aclocal/gpg-error.m4
/usr/bin/gpg-error-config
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.10-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net>  1.10-1
- Initial port on Aix5.3
