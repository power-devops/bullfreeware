%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-TimeDate
Version:        2.30
Release:        1
Summary:        A Perl module for time and date manipulation
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/TimeDate
Source0:        https://cpan.metacpan.org/authors/id/G/GB/GBARR/TimeDate-%{version}.tar.gz

Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch


# Beware, not the same version for all... And no one link to module version...
Provides:       perl(Date::Format)                        = 2.24
Provides:       perl(Date::Language)                      = 1.10
Provides:       perl(Date::Language::Afar)                = 0.99
Provides:       perl(Date::Language::Amharic)             = 1.00
Provides:       perl(Date::Language::Austrian)            = 1.01
Provides:       perl(Date::Language::Brazilian)           = 1.01
Provides:       perl(Date::Language::Bulgarian)           = 1.01
Provides:       perl(Date::Language::Chinese)             = 1.00
Provides:       perl(Date::Language::Chinese_GB)          = 1.01
Provides:       perl(Date::Language::Czech)               = 1.01
Provides:       perl(Date::Language::Danish)              = 1.01
Provides:       perl(Date::Language::Dutch)               = 1.02
Provides:       perl(Date::Language::English)             = 1.01
Provides:       perl(Date::Language::Finnish)             = 1.01
Provides:       perl(Date::Language::French)              = 1.04
Provides:       perl(Date::Language::Gedeo)               = 0.99
Provides:       perl(Date::Language::German)              = 1.02
Provides:       perl(Date::Language::Greek)               = 1.00
Provides:       perl(Date::Language::Hungarian)           = 1.01
Provides:       perl(Date::Language::Icelandic)           = 1.01
Provides:       perl(Date::Language::Italian)             = 1.01
Provides:       perl(Date::Language::Norwegian)           = 1.01
Provides:       perl(Date::Language::Oromo)               = 0.99
Provides:       perl(Date::Language::Romanian)            = 1.01
Provides:       perl(Date::Language::Russian)             = 1.01
Provides:       perl(Date::Language::Russian_cp1251)      = 1.01
Provides:       perl(Date::Language::Russian_koi8r)       = 1.01
Provides:       perl(Date::Language::Sidama)              = 0.99
Provides:       perl(Date::Language::Somali)              = 0.99
Provides:       perl(Date::Language::Spanish)             = 1.00
Provides:       perl(Date::Language::Swedish)             = 1.01
Provides:       perl(Date::Language::Tigrinya)            = 1.00
Provides:       perl(Date::Language::TigrinyaEritrean)    = 1.00
Provides:       perl(Date::Language::TigrinyaEthiopian)   = 1.00
Provides:       perl(Date::Language::Turkish)             = 1.0
Provides:       perl(Date::Parse)                         = 2.30
Provides:       perl(Time::Zone)                           = 2.24

Requires:       perl(perl)                      >= 5.30

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)


%description
This module includes a number of smaller modules suited for
manipulation of time and date strings with Perl. In particular, the
Date::Format and Date::Parse modules can display and read times and
dates in various formats, providing a more reliable interface to
textual representations of points in time.


%prep
%setup -q -n TimeDate-%{version}


%build
%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} -c %{buildroot}


%check
%if %{with dotests}
  gmake test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc ChangeLog README
%{perl_vendorlib}/Date/*
%{perl_vendorlib}/Time/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 2.30-1
- Port on AIX.
