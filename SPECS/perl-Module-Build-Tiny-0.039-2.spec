# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Module-Build-Tiny
%define desc Many Perl distributions use a Build.PL file instead of a Makefile.PL file to drive distribution configuration, build, test and installation.\
Traditionally, Build.PL uses Module::Build as the underlying build system. This module provides a simple, lightweight, drop-in replacement.\
\
Whereas Module::Build has over 6,700 lines of code; this module has less than 120, yet supports the features needed by most distributions.
%define provide_list Module::Build::Tiny
%define require_list CPAN::Meta DynaLoader Exporter ExtUtils::CBuilder ExtUtils::Config ExtUtils::Helpers ExtUtils::Install ExtUtils::InstallPaths ExtUtils::ParseXS File::Basename File::Find File::Path File::Spec::Functions Getopt::Long JSON::PP Pod::Man TAP::Harness::Env strict warnings

Name:           perl-%{meta_name}
Version:        0.039
Release: 2
Summary:        A tiny replacement for Module::Build
License:        GPL+ or Artistic
URL:            https://github.com/Leont/module-build-tiny
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-Tiny-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

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
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Module-Build-Tiny-%{version} 


%build
%__perl Build.PL --installdirs=vendor
./Build


%check
%if %{with dotests}
./Build test
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} %{buildroot}/*

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc Changes
# contrib README LICENSE
%{perl_vendorlib}/Module/Build/*
#%%{_mandir}/man3/Module::Build*


%changelog
* Tue Oct 19 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 0.039-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.039-1
- Port to AIX
