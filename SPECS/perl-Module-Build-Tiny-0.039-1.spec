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

Name:           perl-Module-Build-Tiny
Version:        0.039
Release:        1
Summary:        A tiny replacement for Module::Build
License:        GPL+ or Artistic
URL:            https://github.com/Leont/module-build-tiny
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Module::Build::Tiny) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(CPAN::Meta)
Requires: perl(DynaLoader)
Requires: perl(Exporter) >= 5.57
Requires: perl(ExtUtils::CBuilder)
Requires: perl(ExtUtils::Config) >= 0.003
Requires: perl(ExtUtils::Helpers) >= 0.020
Requires: perl(ExtUtils::Install)
Requires: perl(ExtUtils::InstallPaths) >= 0.002
Requires: perl(ExtUtils::ParseXS)
Requires: perl(File::Basename)
Requires: perl(File::Find)
Requires: perl(File::Path)
Requires: perl(File::Spec::Functions)
Requires: perl(Getopt::Long) >= 2.5
Requires: perl(JSON::PP)
Requires: perl(Pod::Man)
Requires: perl(TAP::Harness::Env)
Requires: perl(strict)
Requires: perl(warnings)

#Buildrequires
BuildRequires: perl(Carp)
BuildRequires: perl(Cwd)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(File::Spec)
BuildRequires: perl(File::Temp)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(IPC::Open3)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(XSLoader)
BuildRequires: perl(blib)
BuildRequires: perl(lib)

BuildRequires: perl(CPAN::Meta)
BuildRequires: perl(DynaLoader)
BuildRequires: perl(Exporter) >= 5.57
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(ExtUtils::Config) >= 0.003
BuildRequires: perl(ExtUtils::Helpers) >= 0.020
BuildRequires: perl(ExtUtils::Install)
BuildRequires: perl(ExtUtils::InstallPaths) >= 0.002
BuildRequires: perl(ExtUtils::ParseXS)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Find)
BuildRequires: perl(File::Path)
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(Getopt::Long) >= 2.5
BuildRequires: perl(JSON::PP)
BuildRequires: perl(Pod::Man)
BuildRequires: perl(TAP::Harness::Env)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)


%description
Many Perl distributions use a Build.PL file instead of a Makefile.PL file to drive distribution configuration, build, test and installation. Traditionally, Build.PL uses Module::Build as the underlying build system. This module provides a simple, lightweight, drop-in replacement.

Whereas Module::Build has over 6,700 lines of code; this module has less than 120, yet supports the features needed by most distributions.


%prep
%setup -q -n Module-Build-Tiny-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Build.PL --installdirs=vendor
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

./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} %{buildroot}/*

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc Changes
# contrib README LICENSE
%{perl_vendorlib}/Module/Build/*
%{_mandir}/man3/Module::Build*


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
