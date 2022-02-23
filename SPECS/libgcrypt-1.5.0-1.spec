Name: libgcrypt
Version: 1.5.0
Release: 1
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
#Source1: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0: %{name}-%{version}-aix.patch
Group: System Environment/Libraries
License: LGPL
Summary: A general-purpose cryptography library.
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: libgpg-error-devel pkg-config
Requires: libgpg-error

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development files for the %{name} package.
Group: Development/Libraries
PreReq: /sbin/install-info
Requires: info
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
%patch0 -p1 -b .aix


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib:/usr/lib64" \
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --disable-silent-rules \
    --enable-shared --enable-static \
    --disable-asm
make %{?_smp_mflags}

cp src/.libs/%{name}.so.11 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
CFLAGS="-D_LARGE_FILES -D_LARGEFILE_SOURCE" \
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --disable-silent-rules \
    --enable-static --enable-shared \
    --disable-asm
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/%{name}.a ./%{name}.so.11


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/gcrypt.info

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
/sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir


%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_libdir}/*.a
/usr/bin/dumpsexp
/usr/bin/hmac256
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/%{name}-config
%{_includedir}/*
%{_libdir}/*.la
%{_datadir}/aclocal/*
%{_infodir}/gcrypt.info*
/usr/bin/%{name}-config
/usr/include/*
/usr/lib/*.la


%changelog
* Tue Jul 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.10.5-1
- Initial port on Aix6.1

* Thu Oct 13 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 1.4.6-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net>  1.4.6-1
- Initial port on Aix5.3
