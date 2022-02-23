# Tests by default. No tests: rpm -ba --define 'dotests 0' libidn*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.33
Release: 1

URL: http://www.gnu.org/software/libidn
License: LGPLv2+
Source0: http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries

Source1: %{name}-%{version}-%{release}.build.log

BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: pkg-config, gettext
Requires: info, gettext
Requires: /sbin/install-info

%define _libdir64 %{_prefix}/lib64


%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Development files for the libidn library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This package includes header files and libraries necessary for
developing programs which use the GNU libidn library.


%prep
%setup -q

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
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit version
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CC=gcc
export OPT=-O2

# first build the 64-bit version
cd 64bit

export OBJECT_MODE=64

CFLAGS="$OPT -maix64" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

#cp lib/.libs/libidn.so.11 ..
#mv -f doc/libidn.html ..


if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi

slibclean


cd ../32bit

export OBJECT_MODE=32

# now build the 32-bit version
CFLAGS="$OPT -maix32" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=%{_libdir} \
    --infodir=%{_infodir} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

#mv -f ../64bit/libidn.html doc/

if [ "%{DO_TESTS}" == 1 ]
then
    (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install


# setup environment for 32-bit and 64-bit version
export AR="/usr/bin/ar -X32_64"
export RM="/usr/bin/rm -f"

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
(
  cd            ${RPM_BUILD_ROOT}%{_libdir64}
  ${AR} -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.a
  ${AR} -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ./%{name}.so.11
)

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/%{name}.info
rm -f     ${RPM_BUILD_ROOT}%{_infodir}/dir

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

cd examples
make clean
rm -rf .deps


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/ChangeLog 32bit/NEWS 32bit/FAQ 32bit/README 32bit/THANKS 32bit/COPYING*
%{_bindir}/*
%{_mandir}/man1/*
%{_libdir}/*.a
%{_infodir}/libidn*
%{_datadir}/locale/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/libidn.html 32bit/examples
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Aug 19 2016 Tony Reix <tony.reix@bull.net> - 1.33-1
- Update to version 1.33-1
- Build for AIX 6.1

* Thu Feb 04 2012 Patricia Cugny <patricia.cugny@bull.net> - 1.24-1
- Update to version 1.24-1
- Build for AIX 6.1

* Fri Mar 04 2011 Patricia Cugny <patricia.cugny@bull.net> - 1.19-2
- first version for AIX V5.3 and higher
