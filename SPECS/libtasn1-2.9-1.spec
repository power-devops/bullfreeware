Summary:	This is the ASN.1 library used in GNUTLS
Name:		libtasn1
Version:	2.9
Release: 	1

License:	LGPL
Group:		System Environment/Libraries
URL:		http://www.gnu.org/software/gnutls/download.html
Source0:	ftp://ftp.gnutls.org/pub/gnutls/%{name}/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.gnutls.org/pub/gnutls/%{name}/%{name}-%{version}.tar.gz.sig
BuildRoot:	/var/tmp/%{name}-%{version}-%{release}-root
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
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --enable-shared --enable-static
make %{?_smp_mflags}

cp lib/.libs/libtasn1.so.3 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --enable-shared --enable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q lib/.libs/libtasn1.a ./libtasn1.so.3


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
* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.9
- Initial port on Aix5.3
