%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

# For compiled modules
%define perl_vendorarch32 %(eval "`%{perl32} -V:installvendorarch`"; echo $installvendorarch)
%define perl_vendorarch64 %(eval "`%{perl64} -V:installvendorarch`"; echo $installvendorarch)


Name:           perl-%{perl_version}-String-CRC32
Version:        1.7
Release:        1
Summary:        Perl interface for cyclic redundancy check generation
License:        Public Domain
URL:            https://metacpan.org/release/String-CRC32
Source0:        https://cpan.metacpan.org/modules/by-module/String/String-CRC32-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      ppc

Provides:       perl(String::CRC32)       =  %version

Requires:       perl(:MODULE_COMPAT_%{perl_version})

BuildRequires:  coreutils
BuildRequires:  make

BuildRequires:  perl(perl)                >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)


%description
This packages provides a perl module to generate checksums from strings and
from files.

The checksums are the same as those calculated by ZMODEM, PKZIP, PICCHECK and
many others.

There is another perl module called String::CRC, which supports calculation of
CRC values of various widths (i.e. not just 32 bits), but the generated sums
differ from those of the programs mentioned above.


%prep
%setup -q -n String-CRC32-%{version}

mkdir ../32bit
mv *  ../32bit
mv    ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export AR="/usr/bin/ar -X32_64"

cd 64bit
%{perl64} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 verbose optimize="-O3"
gmake

cd ../32bit
# Beware, mariadb-connector-c only in 64. May not work.
%{perl32} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 verbose optimize="-O3"
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
cd ../32bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

%{_fixperms} -c %{buildroot}

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +


%check
%if %{with dotests}
  cd 64bit
  gmake -k test TEST_VERBOSE=1

  cd ../32bit
  gmake -k test TEST_VERBOSE=1
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc 64bit/LICENSE 64bit/README.md
%{perl_vendorarch32}/String/
%{perl_vendorarch32}/auto/String/
%{perl_vendorarch64}/String/
%{perl_vendorarch64}/auto/String/
%{_mandir}/man3/String::CRC32.3*


%changelog
* Wed Oct 23 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.7-1
- First port to AIX.
