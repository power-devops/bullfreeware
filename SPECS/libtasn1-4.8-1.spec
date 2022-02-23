# Tests by default. No tests: rpm -ba --define 'dotests 0' libtasn1*.spec

Summary:	This is the ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	4.8
Release: 	1

License:	LGPL
Group:		System Environment/Libraries
URL:		http://www.gnu.org/software/gnutls/download.html
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Source2:	%{name}.so.3-aix32
Source3:	%{name}.so.3-aix64
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	bison

%define _libdir64 %{_prefix}/lib64

%description
This is the ASN.1 library used in GNUTLS.  More up to date information can
be found at http://www.gnu.org/software/gnutls and http://www.gnutls.org.

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Files for development of applications which will use libtasn1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	info
Requires:	/sbin/install-info

%description devel
This is the ASN.1 library used in GNUTLS.  More up to date information can
be found at http://www.gnu.org/software/gnutls and http://www.gnutls.org.

This package contains files for development of applications which will
use libtasn1.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%package tools
Summary:	Some ASN.1 tools
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description tools
This is the ASN.1 library used in GNUTLS.  More up to date information can
be found at http://www.gnu.org/software/gnutls and http://www.gnutls.org.

This package contains tools using the libtasn library.


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
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CFLAGS="-O2"

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit

export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static
make %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    (gmake -k check || true)
fi


# now build the 32-bit version
cd ../32bit

export CC="/usr/vac/bin/xlc_r -q32"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --libdir=%{_libdir} \
    --enable-shared --enable-static
make %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    (gmake -k check || true)
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
      
export AR="/usr/bin/ar -X32_64"

cd 64bit
make install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
make install DESTDIR=${RPM_BUILD_ROOT}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -x ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.a 
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a  %{name}.so*

# Add the older 2.1.X version shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} %{name}.so.3
/usr/bin/strip -X32 -e %{name}.so.3
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.3
cp %{SOURCE3} %{name}.so.3
/usr/bin/strip -X64 -e %{name}.so.3
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/%{name}.a %{name}.so.3

rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/%{name}.a
cd        ${RPM_BUILD_ROOT}%{_libdir64}
ln -s                      %{_libdir}/%{name}.a .
cd -

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

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
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc doc/TODO
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS
%{_libdir}/*.a
%{_libdir64}/*.a
/usr/lib/*.a


%files tools
%defattr(-,root,system,-)
%{_bindir}/asn1*
%{_mandir}/man1/*
/usr/bin/asn1*


%files devel
%defattr(-,root,system,-)
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*.info.*
%{_mandir}/man3/*
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Jun 23 2016 Maximilien Faure <maximilien.faure@atos.net> 3.3-1
- Update for compliance 

* Wed Jun 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.3-1
- Initial port on Aix6.1

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.9-1
- Initial port on Aix5.3
