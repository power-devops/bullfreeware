%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-IO-HTML
Version:        1.001
Release:        1
Summary:        Open an HTML file with automatic charset detection
License:        Artistic Licence
URL:            https://metacpan.org/pod/IO::HTML
Source0:        https://cpan.metacpan.org/authors/id/C/CJ/CJM/IO-HTML-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides:       perl(IO::HTML)              =  %version

Requires:       perl(perl)                  >= 5.30
Requires:       perl(Carp)
Requires:       perl(Encode)                >= 2.10
Requires:       perl(Exporter)              >= 5.57

BuildRequires:  coreutils, make

BuildRequires:  perl(perl)                  >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)   >= 6.30
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)            >= 0.88

# To test
BuildRequires: perl(Carp)
BuildRequires: perl(Encode)                >= 2.10
BuildRequires: perl(Exporter)              >= 5.57


%description
IO::HTML provides an easy way to open a file containing HTML while
automatically determining its encoding. It uses the HTML5 encoding
sniffing algorithm specified in section 8.2.2.2 of the draft
standard.


%prep
%setup -q -n IO-HTML-%{version}


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
%doc LICENSE Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Mon Oct 14 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.014-1
- First port on AIX.
