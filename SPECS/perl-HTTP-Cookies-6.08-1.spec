%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-HTTP-Cookies
Version:        6.08
Release:        1
Summary:        HTTP cookie jars
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/HTTP-Cookies
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Cookies-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(HTTP::Cookies)              = %version
Provides:       perl(HTTP::Cookies::Microsoft)   = %version
Provides:       perl(HTTP::Cookies::Netscape)    = %version

Requires:       perl(perl)                      >= 5.30
Requires:       perl(Carp)
Requires:       perl(HTTP::Date)                >= 6
Requires:       perl(HTTP::Headers::Util)       >= 6
Requires:       perl(HTTP::Request)
Requires:       perl(locale)
Requires:       perl(strict)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI)
BuildRequires:  perl(warnings)

# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date)                >= 6
BuildRequires:  perl(HTTP::Headers::Util)       >= 6
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(locale)
BuildRequires:  perl(strict)


%description
This class is for objects that represent a "cookie jar" -- that is, a
database of all the HTTP cookies that a given LWP::UserAgent object
knows about.


%prep
%setup -q -n HTTP-Cookies-%{version}


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
%doc Changes CONTRIBUTORS README.md LICENSE
%{perl_vendorlib}/HTTP/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.05-1
- Port on AIX.
