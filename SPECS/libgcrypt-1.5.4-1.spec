Name: libgcrypt
Version: 1.5.4
Release: 1
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0: %{name}-%{version}-aix.patch
Group: System Environment/Libraries
License: LGPL
Summary: A general-purpose cryptography library.
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
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
%patch0


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="/usr/bin/rm -f"

# first build the 64-bit version
export CC="cc -q64"
export CC="gcc -maix64"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static \
    --disable-asm

gmake %{?_smp_mflags}

gmake check

cp src/.libs/%{name}.so.11 .
make distclean
slibclean

# now build the 32-bit version
export CC="cc"
export CC="gcc -maix32"

./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --enable-static --enable-shared \
    --disable-asm

gmake %{?_smp_mflags}

gmake check

slibclean

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
* Thu Nov 09 2017 Tony Reix <tony.reix@atos.net> - 1.5.4-1
- port on AIX 6.1

* Fri Aug 15 2014 Michael Perzl <michael@perzl.org> - 1.5.4-1
- updated to version 1.5.4

* Sat Jul 27 2013 Michael Perzl <michael@perzl.org> - 1.5.3-1
- updated to version 1.5.3

* Fri May 03 2013 Michael Perzl <michael@perzl.org> - 1.5.2-1
- updated to version 1.5.2

* Fri Apr 05 2013 Michael Perzl <michael@perzl.org> - 1.5.1-1
- updated to version 1.5.1

* Sat Jul 30 2011 Michael Perzl <michael@perzl.org> - 1.5.0-1
- updated to version 1.5.0

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 1.4.6-1
- updated to version 1.4.6

* Tue Dec 22 2009 Michael Perzl <michael@perzl.org> - 1.4.5-1
- updated to version 1.4.5

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 1.4.4-1
- updated to version 1.4.4

* Thu Oct 23 2008 Michael Perzl <michael@perzl.org> - 1.4.3-1
- updated to version 1.4.3

* Fri May 16 2008 Michael Perzl <michael@perzl.org> - 1.4.1-1
- updated to version 1.4.1

* Fri Mar 28 2008 Michael Perzl <michael@perzl.org> - 1.4.0-2
- corrected some SPEC file errors

* Fri Feb 22 2008 Michael Perzl <michael@perzl.org> - 1.4.0-1
- updated to version 1.4.0

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 1.2.4-2
- included both 32-bit and 64-bit shared objects

* Fri Oct 05 2007 Michael Perzl <michael@perzl.org> - 1.2.4-1
- first version for AIX V5.1 and higher
