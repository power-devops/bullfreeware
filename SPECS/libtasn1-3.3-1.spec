Summary:	This is the ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	3.3
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


%build
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --enable-shared --enable-static
make %{?_smp_mflags}

cp lib/.libs/%{name}.so.6 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --enable-shared --enable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q lib/.libs/%{name}.a ./%{name}.so.6

# Add the older 2.1.X version shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} %{name}.so.3
/usr/bin/strip -X32 -e %{name}.so.3
/usr/bin/ar -X32 -q lib/.libs/%{name}.a %{name}.so.3
cp %{SOURCE3} %{name}.so.3
/usr/bin/strip -X64 -e %{name}.so.3
/usr/bin/ar -X64 -q lib/.libs/%{name}.a %{name}.so.3


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT}

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
* Wed Jun 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.3-1
- Initial port on Aix6.1

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.9-1
- Initial port on Aix5.3
