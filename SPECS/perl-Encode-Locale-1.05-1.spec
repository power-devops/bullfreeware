%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-Encode-Locale
Version:        1.05
Release:        1
Summary:        Determine the locale encoding
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/Encode-Locale
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/Encode-Locale-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(Encode::Locale)     = %version

Requires:       perl(perl)          >= 5.30
Requires:       perl(Encode)        >= 2.00
Requires:       perl(Encode::Alias)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)

# To test
BuildRequires:  perl(Encode)        >= 2.00
BuildRequires:  perl(Encode::Alias)


%description
In many applications it's wise to let Perl use Unicode for the strings
it processes.  Most of the interfaces Perl has to the outside world is
still byte based.  Programs therefore needs to decode byte strings
that enter the program from the outside and encode them again on the
way out.


%prep
%setup -q -n Encode-Locale-%{version}


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
%doc Changes README
%{perl_vendorlib}/Encode/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.05-1
- Port on AIX.
