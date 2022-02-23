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

#: See Fedora specfile or https://metacpan.org
Name:           perl-Test-Harness
Version:        3.42
Release:        1
Summary:        Run Perl standard test scripts with statistics
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-Harness
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Test-Harness-3.42.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(App::Prove) = %{version}
Provides: perl(App::Prove::State) = %{version}
Provides: perl(App::Prove::State::Result) = %{version}
Provides: perl(App::Prove::State::Result::Test) = %{version}
Provides: perl(TAP::Base) = %{version}
Provides: perl(TAP::Formatter::Base) = %{version}
Provides: perl(TAP::Formatter::Color) = %{version}
Provides: perl(TAP::Formatter::Console) = %{version}
Provides: perl(TAP::Formatter::Console::ParallelSession) = %{version}
Provides: perl(TAP::Formatter::Console::Session) = %{version}
Provides: perl(TAP::Formatter::File) = %{version}
Provides: perl(TAP::Formatter::File::Session) = %{version}
Provides: perl(TAP::Formatter::Session) = %{version}
Provides: perl(TAP::Harness) = %{version}
Provides: perl(TAP::Harness::Env) = %{version}
Provides: perl(TAP::Object) = %{version}
Provides: perl(TAP::Parser) = %{version}
Provides: perl(TAP::Parser::Aggregator) = %{version}
Provides: perl(TAP::Parser::Grammar) = %{version}
Provides: perl(TAP::Parser::Iterator) = %{version}
Provides: perl(TAP::Parser::Iterator::Array) = %{version}
Provides: perl(TAP::Parser::Iterator::Process) = %{version}
Provides: perl(TAP::Parser::Iterator::Stream) = %{version}
Provides: perl(TAP::Parser::IteratorFactory) = %{version}
Provides: perl(TAP::Parser::Multiplexer) = %{version}
Provides: perl(TAP::Parser::Result) = %{version}
Provides: perl(TAP::Parser::Result::Bailout) = %{version}
Provides: perl(TAP::Parser::Result::Comment) = %{version}
Provides: perl(TAP::Parser::Result::Plan) = %{version}
Provides: perl(TAP::Parser::Result::Pragma) = %{version}
Provides: perl(TAP::Parser::Result::Test) = %{version}
Provides: perl(TAP::Parser::Result::Unknown) = %{version}
Provides: perl(TAP::Parser::Result::Version) = %{version}
Provides: perl(TAP::Parser::Result::YAML) = %{version}
Provides: perl(TAP::Parser::ResultFactory) = %{version}
Provides: perl(TAP::Parser::Scheduler) = %{version}
Provides: perl(TAP::Parser::Scheduler::Job) = %{version}
Provides: perl(TAP::Parser::Scheduler::Spinner) = %{version}
Provides: perl(TAP::Parser::Source) = %{version}
Provides: perl(TAP::Parser::SourceHandler) = %{version}
Provides: perl(TAP::Parser::SourceHandler::Executable) = %{version}
Provides: perl(TAP::Parser::SourceHandler::File) = %{version}
Provides: perl(TAP::Parser::SourceHandler::Handle) = %{version}
Provides: perl(TAP::Parser::SourceHandler::Perl) = %{version}
Provides: perl(TAP::Parser::SourceHandler::RawTAP) = %{version}
Provides: perl(TAP::Parser::YAMLish::Reader) = %{version}
Provides: perl(TAP::Parser::YAMLish::Writer) = %{version}
Provides: perl(Test::Harness) = %{version}

Requires: perl(perl) >= 5.30

BuildRequires: perl(ExtUtils::MakeMaker)


%description
This package allows tests to be run and results automatically aggregated and
output to STDOUT.

Although, for historical reasons, the Test-Harness distribution takes its name
from this module it now exists only to provide TAP::Harness with an interface
that is somewhat backwards compatible with Test::Harness 2.xx. If you're
writing new code consider using TAP::Harness directly instead.


%prep
%setup -q -n Test-Harness-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
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
%doc Changes Changes-2.64 examples README
%{perl_vendorlib}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*


%changelog
* Tue Jul 23 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1
- Port to AIX
