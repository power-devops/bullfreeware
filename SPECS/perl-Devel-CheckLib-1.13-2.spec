# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Devel-CheckLib
%define desc Devel::CheckLib is a perl module that checks whether a particular C library and its headers are available.
%define provide_list Devel::CheckLib
%define require_list Exporter File::Spec File::Temp

Name:           perl-Devel-CheckLib
Version:        1.13
Release:        2
Summary:        Check that a library is available
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Devel-CheckLib
Source0:        https://cpan.metacpan.org/modules/by-module/Devel/Devel-CheckLib-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More) >= 0.62
## Not provided by perl base package
BuildRequires: perl(IO::CaptureOutput) >= 1.0801
BuildRequires: perl(Mock::Config) >= 0.02

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Devel-CheckLib-%{version} 


%build
%__perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake


%check
%if %{with dotests}
gmake -k test  TEST_VERBOSE=1
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*

(
  cd $RPM_BUILD_ROOT%{_bindir}
  # Deal with binaries for parallel installation
  mv use-devel-checklib use-devel-checklib%{perl_version}
  ln -s use-devel-checklib%{perl_version} use-devel-checklib
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_bindir}/use-devel-checklib

%files -n %module_name
%defattr(-,root,system,-)
%doc CHANGES README TODO
%{_bindir}/use-devel-checklib%{perl_version}
%{perl_vendorlib}/Devel/CheckLib.pm
#%%{_mandir}/man1/use-devel-checklib.1
#%%{_mandir}/man3/Devel::CheckLib.3


%changelog
* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.13-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.13-1
- Port to AIX
