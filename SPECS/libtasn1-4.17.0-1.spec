# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests


Summary:	This is the ASN.1 library used in GNUTLS
Name:		libtasn1
Version: 4.17.0
Release: 1

# The libtasn1 library is LGPLv2+, utilities are GPLv3+
License:	GPLv3+ and LGPLv2+
Group:		System Environment/Libraries
URL:		http://www.gnu.org/software/libtasn1/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Source2:	%{name}.so.3-aix32
Source3:	%{name}.so.3-aix64
Source1000:     %{name}-%{version}-%{release}.build.log

# Patch from Fedora, similar to gnutls rpath patch
Patch1:         libtasn1-3.4-rpath.patch

BuildRequires: bison
BuildRequires: compat-getopt-devel
Requires:      compat-getopt

%define _libdir64 %{_prefix}/lib64

%description
This is the ASN.1 library used in GNUTLS.  More up to date information can
be found at http://www.gnu.org/software/gnutls and http://www.gnutls.org.

The library provides Abstract Syntax Notation One (ASN.1, as specified by
the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding
functions.

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
License:	GPLv3+
Requires:	%{name} = %{version}-%{release}

%description tools
This is the ASN.1 library used in GNUTLS.  More up to date information can
be found at http://www.gnu.org/software/gnutls and http://www.gnutls.org.

This package contains tools that encode and decode ASN.1 data.


%prep
%setup -q

%patch1 -p1 -b .rpath

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
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export CFLAGS="-O2 -D_LARGE_FILES"

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
#export CC="/usr/vac/bin/xlc_r -q64"
export CC="/opt/freeware/bin/gcc -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -lcompat-getopt"
export OBJECT_MODE=64

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static
# --disable-gcc-warnings

# avoid libtasn1 regenerating docs
touch doc/stamp_docs

gmake %{?_smp_mflags}


# now build the 32-bit version
cd ../32bit
#export CC="/usr/vac/bin/xlc_r -q32"
export CC="/opt/freeware/bin/gcc -maix32"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 -lcompat-getopt"
export OBJECT_MODE=32

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --infodir=%{_prefix}/info \
    --libdir=%{_libdir} \
    --enable-shared --enable-static
#  --disable-gcc-warnings

# avoid libtasn1 regenerating docs
touch doc/stamp_docs

gmake %{?_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
      
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
make install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
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
rm -f       ${RPM_BUILD_ROOT}%{_infodir}/dir

(
    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f %{name}.a
    ln -sf ../lib/%{name}.a %{name}.a
)

#(
#  cd ${RPM_BUILD_ROOT}
#  for dir in bin include lib
#  do
#    mkdir -p usr/${dir}
#    cd usr/${dir}
#    ln -sf ../..%{_prefix}/${dir}/* .
#    cd -
#  done
#)

#TODO hack, can be removed in future version
%if "%{version}" == "4.10"
    cp COPYING* doc/
%endif

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


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
%doc 32bit/doc/TODO* 32bit/doc/COPYING*
%doc 32bit/AUTHORS* 32bit/ChangeLog* 32bit/NEWS* 32bit/README* 32bit/THANKS*
%{_libdir}/*.a
%{_libdir64}/*.a
#/usr/lib/*.a


%files tools
%defattr(-,root,system,-)
%{_bindir}/asn1*
%{_mandir}/man1/*
#/usr/bin/asn1*


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/*.pdf
#%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*.info.*
%{_mandir}/man3/*
#/usr/include/*
#/usr/lib/*.la


%changelog
* Fri May 28 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 4.17.0-1
- Update to 4.17.0

* Wed Oct 28 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 4.16.0-1
- Update to 4.16.0

* Wed Oct 28 2020 Étienne Guesnet <etienne.guesnet@atos.net> 4.10-2
- Update specfile for automated build

* Mon Apr 10 2017 Michael Wilson <michael.a.wilson@atos.net> 4.10-1
- Update to version 4.10, required by gnutls-3.5.10

* Fri Aug 19 2016 Maximilien Faure <maximilien.faure@atos.net> 4.8-2
- Initial port on AIX 6.1

* Thu Jun 23 2016 Maximilien Faure <maximilien.faure@atos.net> 3.3-1
- Update for compliance 

* Fri Jun 21 2013 Gerard Visiedo <gerard.visiedo@bull.net> 3.3-1
- Initial port on Aix6.1

* Wed Jun 15 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.9-1
- Initial port on Aix5.3
