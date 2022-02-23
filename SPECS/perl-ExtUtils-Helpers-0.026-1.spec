%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")
# For script modules
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)
# For compiled modules
%define perl_vendorarch32 %(eval "`%{perl32} -V:installvendorarch`"; echo $installvendorarch)
%define perl_vendorarch64 %(eval "`%{perl64} -V:installvendorarch`"; echo $installvendorarch)

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           perl-ExtUtils-Helpers
Version:        0.026
Release:        1
Summary:        Various portability utilities for module builders
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/ExtUtils-Helpers
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(ExtUtils::Helpers) = %{version}
Provides: perl(ExtUtils::Helpers::Unix) = %{version}
Provides: perl(ExtUtils::Helpers::VMS) = %{version}
Provides: perl(ExtUtils::Helpers::Windows) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Carp)
Requires: perl(Exporter) >= 5.57
Requires: perl(File::Basename)
Requires: perl(File::Copy)
Requires: perl(File::Spec::Functions)
Requires: perl(Text::ParseWords) >= 3.24
Requires: perl(strict)
Requires: perl(warnings)

# Build requires
BuildRequires: perl(Cwd)
BuildRequires: perl(lib)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)


%description
This module provides various portable helper functions for module building
modules.


%prep
%setup -q -n ExtUtils-Helpers-%{version}

# Don't include VMS and Windows helpers, which may pull in unwelcome dependencies
#rm -f lib/ExtUtils/Helpers/{VMS,Windows}.pm
#perl -ni -e 'print unless /^lib\/ExtUtils\/Helpers\/(VMS|Windows)\.pm$/;' MANIFEST


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake


%check
%if %{with dotests}
gmake -k test TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc Changes README LICENSE
%{perl_vendorlib}/ExtUtils/*
%{_mandir}/man3/ExtUtils::Helpers.3
%{_mandir}/man3/ExtUtils::Helpers::Unix.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
