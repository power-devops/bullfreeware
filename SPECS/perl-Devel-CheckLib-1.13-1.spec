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

Name:           perl-Devel-CheckLib
Version:        1.13
Release:        1
Summary:        Check that a library is available
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Devel-CheckLib
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Devel::CheckLib) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Exporter)
Requires: perl(File::Spec)
Requires: perl(File::Temp) >= 0.16

# Build requires
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More) >= 0.62
## Not provided by perl base package
BuildRequires: perl(IO::CaptureOutput) >= 1.0801
BuildRequires: perl(Mock::Config) >= 0.02


%description
Devel::CheckLib is a perl module that checks whether a particular C library
and its headers are available.


%prep
%setup -q -n Devel-CheckLib-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1
# NO_PACKLIST from fedora.
gmake


%check
%if %{with dotests}
gmake -k test  TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*

find ${RPM_BUILD_ROOT} -type f -name .packlist -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type d -depth -exec rmdir {} 2>/dev/null ';'


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc CHANGES README TODO
%{_bindir}/use-devel-checklib
%{perl_vendorlib}/Devel/CheckLib.pm
%{_mandir}/man1/use-devel-checklib.1
%{_mandir}/man3/Devel::CheckLib.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.13-1
- Port to AIX
