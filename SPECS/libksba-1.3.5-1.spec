Summary: X.509 library
Name:    libksba
Version: 1.3.5
Release: 1
License: GPL
Group:   System Environment/Libraries
URL:     http://www.gnupg.org/
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2.sig

# Patch0: %{name}-%{version}-aix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: libgpg-error-devel >= 1.2 
BuildRequires: libgcrypt-devel >= 1.2.0
Requires: libgpg-error >= 1.2 
Requires: libgcrypt >= 1.2.0

%description
KSBA is a library designed to build software based on the X.509 and
CMS protocols.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development headers and libraries for %{name}
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: info
Requires: /sbin/install-info

%description devel
%{summary}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
%setup -q
#%patch0


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export RM="rm -f"

# first build the 64-bit version
export CC="xlc -q64"
export CC="gcc -maix64"
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_prefix}/info \
    --enable-static --enable-shared

make %{?_smp_mflags}

cp src/.libs/libksba.so.8 .
make check
make distclean
slibclean

# now build the 32-bit version
export CC="xlc"
export CC="gcc -maix32"
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_prefix}/info \
    --enable-static --enable-shared

make %{?_smp_mflags}

make check
slibclean

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q src/.libs/libksba.a ./libksba.so.8


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

export RM="rm -f"

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/ksba.info

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


%post devel
install-info %{_infodir}/ksba.info.gz %{_infodir}/dir


%postun devel
if [ $1 -eq 0 ]; then
    install-info --delete %{_infodir}/ksba.info.gz %{_infodir}/dir
fi


%files
%defattr(-,root,system,-)
%doc AUTHORS ChangeLog COPYING NEWS README* THANKS TODO
%{_libdir}/lib*.a
/usr/lib/lib*.a


%files devel
%defattr(-,root,system,-)
%{_bindir}/ksba-config
%{_libdir}/lib*.la
%{_includedir}/*
%{_datadir}/aclocal/*
%{_infodir}/*
/usr/bin/ksba-config
/usr/lib/lib*.la


%changelog
* Tue Nov 07 2017 Tony Reix <tony.reix@atos.net> - 1.3.5-1
- updated to version 1.3.5

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.3.0-1
- updated to version 1.3.0

* Tue Mar 29 2011 Michael Perzl <michael@perzl.org> - 1.2.0-1
- updated to version 1.2.0

* Wed Nov 17 2010 Michael Perzl <michael@perzl.org> - 1.1.0-1
- updated to version 1.1.0

* Thu Jul 22 2010 Michael Perzl <michael@perzl.org> - 1.0.8-1
- updated to version 1.0.8

* Tue Sep 08 2009 Michael Perzl <michael@perzl.org> - 1.0.7-1
- updated to version 1.0.7

* Tue Mar 10 2009 Michael Perzl <michael@perzl.org> - 1.0.5-1
- updated to version 1.0.5

* Fri Sep 26 2008 Michael Perzl <michael@perzl.org> - 1.0.4-1
- updated to version 1.0.4

* Wed Apr 23 2008 Michael Perzl <michael@perzl.org> - 1.0.3-1
- updated to version 1.0.3

* Thu Jan 03 2008 Michael Perzl <michael@perzl.org> - 1.0.2-2
- included both 32-bit and 64-bit shared objects

* Fri Oct 05 2007 Michael Perzl <michael@perzl.org> - 1.0.2-1
- first version for AIX V5.1 and higher
