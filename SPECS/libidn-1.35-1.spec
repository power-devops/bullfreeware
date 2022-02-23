# Tests by default. No tests: rpm -ba --define 'dotests 0' libidn*.spec
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define soname 12

# Do not include Java binding
%define enable_libidn_java 0

Summary: Internationalized Domain Name support library
Name: libidn
Version: 1.35
Release: 1

URL: https://www.gnu.org/software/libidn
License: LGPLv2+ and GPLv3+ and GFDL
Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Group: System Environment/Libraries

# Library version for libidn-1.33  is a dep for gnutls-3.5.10-1/libgnutls.so.30
Source1: libidn.so.11-aix32
Source2: libidn.so.11-aix64

Source10: %{name}-%{version}-%{release}.build.log

# Patch to implement --disable-emacs
Patch0: libidn-1.33-Allow-disabling-Emacs-support.patch

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



# Currently the C# binding is not included  --disable-csharp

# Package currently includes emacs-libidn with the main package/RPM libidn
# Fedora SRPM includes a patch to implement option  --disable-emacs
# To build emacs requires --enable-emacs
# and   --with-lispdir=%{_emacs_sitelispdir}/libidn
# If the emacs binding is not required, must include the patch

# Fedora build includes libidn-java and libidn-javadoc
%if %{enable_libidn_java}
%package java
Summary:       Java port of the GNU Libidn library
BuildRequires: java-devel
BuildRequires: javapackages-local
BuildRequires: mvn(com.google.code.findbugs:annotations)
BuildRequires: mvn(com.google.guava:guava)
BuildRequires: mvn(junit:junit)
BuildArch:     noarch

%description java
GNU Libidn is a fully documented implementation of the Stringprep,
Punycode and IDNA specifications. Libidn's purpose is to encode
and decode internationalized domain names.

This package contains the native Java port of the library.

%package javadoc
Summary:       Javadoc for %{name}-java
BuildArch:     noarch

%description javadoc
This package contains javadoc for %{name}-java.
%endif



%prep
%setup -q

# %patch0 -p1 -b .disable_emacs
# 
# autoconf

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

export CONFIG_SHELL=/usr/bin/bash
export CONFIG_ENV_ARGS=/usr/bin/bash

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
    --enable-shared --enable-static \
    --disable-csharp \
%if %{enable_libidn_java}
    --enable-java
%else
    --disable-java
%endif


gmake --trace %{?_smp_mflags}

#cp lib/.libs/libidn.so.%{soname} ..
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
    --enable-shared --enable-static \
    --disable-csharp \
%if %{enable_libidn_java}
    --enable-java
%else
    --disable-java
%endif


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
  ${AR} -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a ./%{name}.so.%{soname}
)

# Manage compatibility with version libidn.so.11

cp %{SOURCE1} libidn.so.11
/usr/bin/strip -X32 -e                                    libidn.so.11
${AR}    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a    libidn.so.11

cp %{SOURCE2} libidn.so.11
/usr/bin/strip -X64 -e                                    libidn.so.11
${AR}    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a    libidn.so.11


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
%doc 32bit/COPYING*
%doc 32bit/ChangeLog 32bit/NEWS 32bit/FAQ 32bit/README 32bit/THANKS
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
* Tue May 30 2017 Michael Wilson <michael.a.wilson@atos.net> - 1.35-1
- Update to version 1.35
-  Force use of bash due to conv of  xx\"yyy\" to 'xx"yyy"' in param expansions
-  The soname is 12.6.0 (was 11.6.16 for libidn-1.33)
-  Library libgnutls.a(libgnutls.so.30) has dependency on libidn.a(libidn.so.11)
-  For initial release exclude C#, emacs and Java
- Fedora 30 used as reference

* Fri Aug 19 2016 Tony Reix <tony.reix@bull.net> - 1.33-1
- Update to version 1.33-1
- Build for AIX 6.1

* Thu Feb 04 2012 Patricia Cugny <patricia.cugny@bull.net> - 1.24-1
- Update to version 1.24-1
- Build for AIX 6.1

* Fri Mar 04 2011 Patricia Cugny <patricia.cugny@bull.net> - 1.19-2
- first version for AIX V5.3 and higher
