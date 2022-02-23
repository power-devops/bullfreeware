%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Summary:        Incredibly simple helpers for testing code with exceptions 
Name:           perl-Test-Fatal
Version:        0.014
Release:        2
License:        GPL+ or Artistic
Url:            https://metacpan.org/release/Test-Fatal
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Test-Fatal-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides:       perl(Test::Fatal)           =  %version

Requires:       perl(perl)                  >= 5.30
Requires:       perl(Carp)
Requires:       perl(Exporter)              >= 5.57
Requires:       perl(Test::Builder)
Requires:       perl(Try::Tiny)             >= 0.07
Requires:       perl(strict)
Requires:       perl(warnings)

BuildRequires:  coreutils, make

BuildRequires:  perl(perl)                  >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)            >= 0.96
BuildRequires:  perl(overload)

# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)              >= 5.57
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Try::Tiny)             >= 0.07
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
Test::Fatal is an alternative to the popular Test::Exception. It does much
less, but should allow greater flexibility in testing exception-throwing code
with about the same amount of typing.


%prep
%setup -q -n Test-Fatal-%{version}
find ./examples -exec /opt/freeware/bin/sed -i 's|/usr/bin/perl|/usr/bin/env perl|g' {} \;


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
%doc LICENSE
%doc Changes README examples/
%{perl_vendorlib}/Test/*
%{_mandir}/man3/Test::Fatal.3*


%changelog
* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.014-2
- No more provide perl_vendorlib/Test itself (compatibility with perl-Test-Needs).
- /usr/bin/perl is no more a requirement.

* Mon Oct 14 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.014-1
- First port on AIX.
