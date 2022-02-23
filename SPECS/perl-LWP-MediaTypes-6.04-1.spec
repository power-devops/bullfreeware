%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-LWP-MediaTypes
Version:        6.04
Release:        1
Summary:        Guess media type for a file or a URL
# lib/LWP/media.types:      Public Domain
# lib/LWP/MediaTypes.pm:    GPL+ or Artistic
License:        (GPL+ or Artistic) and Public Domain
URL:            https://metacpan.org/release/LWP-MediaTypes
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/LWP-MediaTypes-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides:       perl(LWP::MediaTypes)       =  %version

Requires:       perl(perl)                  >= 5.30
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(File::Basename)
Requires:       perl(Scalar::Util)
Requires:       perl(strict)

BuildRequires:  coreutils, make

BuildRequires:  perl(perl)                  >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(overload)
BuildRequires:  perl(warnings)

# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)


%description
This module provides functions for handling media (also known as MIME)
types and encodings. The mapping from file extensions to media types is
defined by the media.types file. If the ~/.media.types file exists it is
used instead. For backwards compatibility we will also look for
~/.mime.types.


%prep
%setup -q -n LWP-MediaTypes-%{version}


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
