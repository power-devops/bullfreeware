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

Name:           perl-IO-CaptureOutput
Version:        1.1104
Release:        1
Summary:        Capture STDOUT/STDERR from sub-processes and XS/C modules
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/IO-CaptureOutput
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/IO-CaptureOutput-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(IO::CaptureOutput) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(File::Basename)
Requires: perl(File::Temp) >= 0.16
Requires: perl(Symbol)
Requires: perl(strict)
Requires: perl(vars)
Requires: perl(warnings)

# Build requires
BuildRequires: perl(perl) >= 5.30
BuildRequires: perl(Test::More) >= 0.62
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec) >= 3.27
BuildRequires: perl(IO::File)

%description
Capture STDOUT/STDERR from sub-processes and XS/C modules.


%prep
%setup -q -n IO-CaptureOutput-%{version} 


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
%doc Changes README
%{perl_vendorlib}/IO/CaptureOutput.pm
%{_mandir}/man3/IO::CaptureOutput.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
