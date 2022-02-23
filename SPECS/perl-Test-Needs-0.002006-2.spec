%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-Test-Needs
Version:        0.002006
Release:        2
Summary:        Skip tests when modules not available
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/Test-Needs
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides:       perl(Test::Needs)         =  %version

Requires:       perl(perl)                >= 5.30

BuildRequires:  coreutils
BuildRequires:  make

BuildRequires:  perl(perl)                >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)          >= 0.45


%description
Skip test scripts if modules are not available. The requested modules will
be loaded, and optionally have their versions checked. If the module is
missing, the test script will be skipped. Modules that are found but fail
to compile will exit with an error rather than skip.


%prep
%setup -q -n Test-Needs-%{version}


%build
%perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
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
%{perl_vendorlib}/Test/*
%{_mandir}/man3/


%changelog
* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.002006-2
- No more provide perl_vendorlib/Test itself (compatibility with perl-Test-Fatal).

* Tue Oct 15 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.002006-1
- First port on AIX.
