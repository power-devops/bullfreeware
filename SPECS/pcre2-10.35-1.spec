%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Name:       pcre2
Version:    10.35
Release:    1 
Summary:    Perl-compatible regular expression library
Group:      System Environment/Libraries
License:    BSD
URL:        http://www.pcre.org/
Source0:    ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.bz2
Source1:    ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.bz2.sig
Source100:  %{name}-%{version}-%{release}.build.log

Patch0:     %{name}-10.30-aix.patch

BuildRequires: patch

Requires: AIX-rpm >= 6.1
Requires: libgcc >= 8.4.0


%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.


%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}
BuildRequires: bzip2-devel >= 1.0.6-1
BuildRequires: zlib-devel >= 1.2.11-1, readline-devel >= 6.0-1
Requires: bzip2 >= 1.0.6-1
Requires: zlib >= 1.2.11-1, readline >= 6.0-1

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIG_ENV_ARGS=/opt/freeware/bin/bash

#export RM="/usr/bin/rm -f"

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64 -O2"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --disable-debug \
    --enable-jit \
    --enable-pcre2grep-jit \
    --disable-rebuild-chartables \
    --enable-unicode \
    --disable-newline-is-cr \
    --enable-newline-is-lf \
    --disable-bsr-anycrlf \
    --disable-never-backslash-C \
    --disable-ebcdic \
    --enable-stack-for-recursion \
    --enable-pcre2grep-libz \
    --enable-pcre2grep-libbz2 \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-valgrind \
    --disable-coverage
gmake %{?_smp_mflags}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32 -O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --disable-debug \
    --enable-jit \
    --enable-pcre2grep-jit \
    --disable-rebuild-chartables \
    --enable-unicode \
    --disable-newline-is-cr \
    --enable-newline-is-lf \
    --disable-bsr-anycrlf \
    --disable-never-backslash-C \
    --disable-ebcdic \
    --enable-stack-for-recursion \
    --enable-pcre2grep-libz \
    --enable-pcre2grep-libbz2 \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-valgrind \
    --disable-coverage
gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
make install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    /usr/bin/ar -X64 -x ${f}
  done
)

# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-8.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-8.so*
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-16.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-16.so*
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-32.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-32.so*
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}-posix.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}-posix.so*

(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
    ln -sf ../lib/$f .
  done
)


%check
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
( gmake -k check || true )
cd ../32bit
export OBJECT_MODE=32
( gmake -k check || true )
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/COPYING 32bit/NEWS 32bit/README
%{_libdir}/*.a
%{_libdir64}/*.a

%files devel
%defattr(-,root,system)
%doc 32bit/doc/*.txt 32bit/doc/html
%doc 32bit/HACKING 32bit/src/pcre2demo.c
%{_bindir}/pcre2-config*
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*


%files tools
%defattr(-,root,system)
%{_bindir}/pcre2grep*
%{_bindir}/pcre2test*
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*


%changelog
* Tue Sep 08 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 10.35-1
- New version 10.35
- First port on Bullfreeware

* Mon Feb 24 2020 Rishita Saha <risaha16@in.ibm.com> - 10.34-1
- updated to version 10.34

* Tue Aug 22 2017 Michael Perzl <michael@perzl.org> - 10.30-1
- updated to version 10.30

* Thu Feb 23 2017 Michael Perzl <michael@perzl.org> - 10.23-1
- updated to version 10.23

* Thu Aug 25 2016 Michael Perzl <michael@perzl.org> - 10.22-1
- updated to version 10.22

* Tue Jul 05 2016 Michael Perzl <michael@perzl.org> - 10.21-1
- first version for AIX V5.1 and higher
