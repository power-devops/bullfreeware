%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-File-Listing
Version:        6.04
Release:        1
Summary:        Parse directory listing
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/File-Listing

Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/File-Listing-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(File::Listing)              = %version

Requires:       perl(perl)                      >= 5.30
Requires:       perl(HTTP::Date)                >= 6

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker) >= 5.30

# To test
BuildRequires:  perl(HTTP::Date)                >= 6


%description
This module exports a single function called parse_dir(), which can be used
to parse directory listings.


%prep
%setup -q -n File-Listing-%{version}


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
%{perl_vendorlib}/File/*
%{_mandir}/man3/*


%changelog
* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 6.04-1
- Port on AIX.
