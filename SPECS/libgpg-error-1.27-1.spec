Summary: libgpg-error
Name: libgpg-error
Version: 1.27
Release: 1
URL: ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig
Group: Development/Libraries
Copyright: LGPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gettext, make, sed
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
application with "xlc_r -q64" or "gcc -maix64".


%prep
%setup -q


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

export CFLAGS="-O3 -qstrict"
export CFLAGS="-O2"

# first build the 64-bit version
export CC="xlc_r -q64"
export CC="gcc -maix64"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

gmake check
cp src/.libs/libgpg-error.so.0 .
gmake distclean
slibclean


# now build the 32-bit version
export CC="xlc_r"
export CC="gcc -maix32"

./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

gmake check
slibclean

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libgpg-error.a ./libgpg-error.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

# patch /opt/freeware/include/gpg-error.h for AIX5L V5.1
/opt/freeware/bin/sed -i 's|#include <stdint.h>|#if defined(_AIX) \&\& !defined(_AIX52)\n#include <inttypes.h>\n#else\n#include <stdint.h>\n#endif|g' ${RPM_BUILD_ROOT}%{_includedir}/gpg-error.h

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
* Wed Nov 08 2017 Tony Reix <tony.reix@atos.net> - 1.27-1
- Re-port

* Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.27-1
- updated to version 1.27

* Tue Jan 31 2017 Michael Perzl <michael@perzl.org> - 1.26-1
- updated to version 1.26

* Tue Jan 31 2017 Michael Perzl <michael@perzl.org> - 1.25-1
- updated to version 1.25

* Tue Jan 31 2017 Michael Perzl <michael@perzl.org> - 1.24-1
- updated to version 1.24

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 1.23-1
- updated to version 1.23

* Wed Dec 23 2015 Michael Perzl <michael@perzl.org> - 1.21-1
- updated to version 1.21

* Wed Dec 23 2015 Michael Perzl <michael@perzl.org> - 1.20-1
- updated to version 1.20

* Wed Dec 23 2015 Michael Perzl <michael@perzl.org> - 1.19-1
- updated to version 1.19

* Tue Feb 03 2015 Michael Perzl <michael@perzl.org> - 1.18-1
- updated to version 1.18

* Mon Dec 08 2014 Michael Perzl <michael@perzl.org> - 1.17-1
- updated to version 1.17

* Mon Dec 08 2014 Michael Perzl <michael@perzl.org> - 1.16-1
- updated to version 1.16

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 1.15-1
- updated to version 1.15

* Fri Aug 15 2014 Michael Perzl <michael@perzl.org> - 1.13-1
- updated to version 1.13

* Mon Jul 08 2013 Michael Perzl <michael@perzl.org> - 1.12-1
- updated to version 1.12

* Fri Apr 05 2013 Michael Perzl <michael@perzl.org> - 1.11-1
- updated to version 1.11

* Wed Nov 17 2010 Michael Perzl <michael@perzl.org> - 1.10-1
- updated to version 1.10

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 1.9-1
- updated to version 1.9

* Mon Jul 05 2010 Michael Perzl <michael@perzl.org> - 1.8-2
- removed dependency on gettext >= 0.17

* Wed May 26 2009 Michael Perzl <michael@perzl.org> - 1.8-1
- updated to version 1.8

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 1.7-1
- updated to version 1.7

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 1.6-3
- corrected some SPEC file errors

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 1.6-2
- included both 32-bit and 64-bit shared objects

* Tue Nov 27 2007 Michael Perzl <michael@perzl.org> - 1.6-1
- updated to v1.6

* Thu Aug 16 2007 Michael Perzl <michael@perzl.org> - 1.5-1
- updated to v1.5

* Tue Jan 03 2006 Michael Perzl <michael@perzl.org> - 1.1-1
- first version for AIX V5.1 and higher
