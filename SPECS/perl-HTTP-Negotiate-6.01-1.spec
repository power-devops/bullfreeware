%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-HTTP-Negotiate
Version:        6.01
Release:        1
Summary:        Choose a variant to serve
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/HTTP-Negotiate
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTTP-Negotiate-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(HTTP::Negotiate)            = %version

Requires:       perl(perl)                      >= 5.30
Requires:       perl(HTTP::Headers)             >= 6

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)

# To test
BuildRequires:  perl(HTTP::Headers)             >= 6


%description
This module provides a complete implementation of the HTTP content
negotiation algorithm specified in draft-ietf-http-v11-spec-00.ps chapter
12. Content negotiation allows for the selection of a preferred content
representation based upon attributes of the negotiable variants and the
value of the various Accept* header fields in the request.


%prep
%setup -q -n HTTP-Negotiate-%{version}


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
%doc  Changes README
%{perl_vendorlib}/HTTP/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 6.01-1
- Port on AIX.
