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

Name:           perl-Module-Build
Version:        0.4229
Release:        1
Summary:        Build and install Perl modules
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Module-Build
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Module::Build) = %{version}
Provides: perl(Module::Build::Base) = %{version}
Provides: perl(Module::Build::Compat) = %{version}
Provides: perl(Module::Build::Config) = %{version}
Provides: perl(Module::Build::Cookbook) = %{version}
Provides: perl(Module::Build::Dumper) = %{version}
Provides: perl(Module::Build::Notes) = %{version}
Provides: perl(Module::Build::PPMMaker) = %{version}
Provides: perl(Module::Build::Platform::Default) = %{version}
Provides: perl(Module::Build::Platform::MacOS) = %{version}
Provides: perl(Module::Build::Platform::Unix) = %{version}
Provides: perl(Module::Build::Platform::VMS) = %{version}
Provides: perl(Module::Build::Platform::VOS) = %{version}
Provides: perl(Module::Build::Platform::Windows) = %{version}
Provides: perl(Module::Build::Platform::aix) = %{version}
Provides: perl(Module::Build::Platform::cygwin) = %{version}
Provides: perl(Module::Build::Platform::darwin) = %{version}
Provides: perl(Module::Build::Platform::os2) = %{version}
Provides: perl(Module::Build::PodParser) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(CPAN::Meta) >= 2.142060
Requires: perl(Cwd)
Requires: perl(Data::Dumper)
Requires: perl(ExtUtils::CBuilder) >= 0.27
Requires: perl(ExtUtils::Install)
Requires: perl(ExtUtils::Manifest)
Requires: perl(ExtUtils::Mkbootstrap)
Requires: perl(ExtUtils::ParseXS) >= 2.21
Requires: perl(File::Basename)
Requires: perl(File::Compare)
Requires: perl(File::Copy)
Requires: perl(File::Find)
Requires: perl(File::Path)
Requires: perl(File::Spec) >= 0.82
Requires: perl(Getopt::Long)
Requires: perl(Module::Metadata) >= 1.000002
Requires: perl(Perl::OSType) >= 1
Requires: perl(Pod::Man) >= 2.17
Requires: perl(TAP::Harness) >= 3.29
Requires: perl(Text::Abbrev)
Requires: perl(Text::ParseWords)
Requires: perl(version) >= 0.87

# Build requires
BuildRequires: perl(CPAN::Meta::YAML) >= 0.003
BuildRequires: perl(File::Temp) >= 0.15
BuildRequires: perl(Parse::CPAN::Meta) >= 1.4401
BuildRequires: perl(TAP::Harness) >= 3.29
BuildRequires: perl(Test::More) >= 0.49
# Config requires
BuildRequires: perl(CPAN::Meta) >= 2.142060
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec) >= 0.82
BuildRequires: perl(Module::Metadata) >= 1.000002
BuildRequires: perl(Perl::OSType) >= 1
BuildRequires: perl(version) >= 0.87

# Not in cpan list, but needed
BuildRequires: perl(inc::latest)


%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.
Developers may alter the behavior of the module through sub-classing in a
much more straightforward way than with MakeMaker. It also does not require
a make on your system - most of the Module::Build code is pure-perl and
written in a very cross-platform way. In fact, you don't even need a shell,
so even platforms like MacOS (traditional) can use it fairly easily. Its
only prerequisites are modules that are included with perl 5.6.0, and it
works fine on perl 5.005 if you can install a few additional modules.


%prep
%setup -q -n Module-Build-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Build.PL installdirs=vendor
./Build


%check
%if %{with dotests}
# rm t/signature.t
#LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 
./Build test
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc Changes contrib README LICENSE
%{perl_vendorlib}/Module/Build.pm
%{perl_vendorlib}/Module/Build/*
%{_mandir}/man3/Module::Build*


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
