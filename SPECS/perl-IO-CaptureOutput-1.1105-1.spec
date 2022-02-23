# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name IO-CaptureOutput
%define desc Capture STDOUT/STDERR from sub-processes and XS/C modules.
%define provide_list IO::CaptureOutput
%define require_list Carp Exporter File::Basename File::Temp Symbol strict vars warnings

Name:           perl-IO-CaptureOutput
Version: 1.1105
Release: 1
Summary:        Capture STDOUT/STDERR from sub-processes and XS/C modules
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/IO-CaptureOutput
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/IO-CaptureOutput-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(perl) >= 5.30
BuildRequires: perl(Test::More) >= 0.62
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec) >= 3.27
BuildRequires: perl(IO::File)

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n IO-CaptureOutput-%{version} 


%build
%__perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake


%check
%if %{with dotests}
gmake -k test TEST_VERBOSE=1
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc Changes README
%{perl_vendorlib}/IO/CaptureOutput.pm
#%%{_mandir}/man3/IO::CaptureOutput.3


%changelog
* Mon Nov 15 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.1105-1
- Update to 1.1105

* Tue Oct 19 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.1104-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.1104-1
- Port to AIX
