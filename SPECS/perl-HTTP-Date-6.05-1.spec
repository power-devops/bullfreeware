%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-HTTP-Date
Version:        6.05
Release:        1
Summary:        Date conversion routines
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/HTTP-Date
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTTP-Date-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(HTTP::Date)               = %version

Requires:       perl(perl)                    >= 5.30
Requires:       perl(Exporter)
Requires:       perl(Time::Local)             >= 1.28
Requires:       perl(Time::Zone)
Requires:       perl(strict)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)

# To test
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Time::Local)             >= 1.28
BuildRequires:  perl(Time::Zone)
BuildRequires:  perl(strict)


%description
This module provides functions that deal the date formats used by the HTTP
protocol (and then some more). Only the first two functions, time2str() and
str2time(), are exported by default.


%prep
%setup -q -n HTTP-Date-%{version}


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
%doc Changes README.md LICENSE
%{perl_vendorlib}/HTTP/*
%{_mandir}/man3/*


%changelog
* Thu Dec 05 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 6.05-1
- Port on AIX.
