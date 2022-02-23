# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name ExtUtils-Config
%define desc ExtUtils::Config is an abstraction around the %%Config hash.
%define provide_list ExtUtils::Config
%define require_list Data::Dumper strict warnings

Name:           perl-%{meta_name}
Version:        0.008
Release: 2
Summary:        A wrapper for perl's configuration
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/%{meta_name}
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Config-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

BuildRequires: perl(perl)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(IPC::Open3)
BuildRequires: perl(ExtUtils::MakeMaker)

%perl_meta_provides
%perl_meta_requires

%description
%desc

%perl_module
%perl_module_desc

%prep
%setup -q -n %{meta_name}-%{version}

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
%doc Changes README LICENSE
%{perl_vendorlib}/ExtUtils/Config.pm
#%%{_mandir}/man3/ExtUtils::Config.3


%changelog
* Tue Oct 19 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 0.008-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.008-1
- Port to AIX
