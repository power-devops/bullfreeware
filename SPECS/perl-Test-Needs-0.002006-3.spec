# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Test-Needs
%define desc Skip test scripts if modules are not available. The requested modules will \
be loaded, and optionally have their versions checked. If the module is \
missing, the test script will be skipped. Modules that are found but fail \
to compile will exit with an error rather than skip.
%define provide_list Test::Needs
# No require #%%define require_list 

Name:           perl-%{meta_name}
Version:        0.002006
Release:        3
Summary:        Skip tests when modules not available
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/Test-Needs
Source0:        https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

BuildRequires:  coreutils
BuildRequires:  make

BuildRequires:  perl(perl)                >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)          >= 0.45

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Test-Needs-%{version}


%build
%__perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} -c %{buildroot}


%check
%if %{with dotests}
  gmake test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc Changes README
%{perl_vendorlib}/Test/*
#%%{_mandir}/man3/


%changelog
* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 0.002006-3
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.002006-2
- No more provide perl_vendorlib/Test itself (compatibility with perl-Test-Fatal).

* Tue Oct 15 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 0.002006-1
- First port on AIX.
