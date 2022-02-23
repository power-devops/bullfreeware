# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Test-Deep
%define desc Test::Deep gives you very flexible ways to check that the result you \
got is the result you were expecting. At its simplest it compares two \
structures by going through each level, ensuring that the values \
match, that arrays and hashes have the same elements and that \
references are blessed into the correct class. It also handles \
circular data structures without getting caught in an infinite loop.
%define provide_list Test::Deep Test::Deep::All Test::Deep::Any Test::Deep::Array Test::Deep::ArrayEach \
Test::Deep::ArrayElementsOnly Test::Deep::ArrayLength Test::Deep::ArrayLengthOnly Test::Deep::Blessed \
Test::Deep::Boolean  Test::Deep::Cache::Simple Test::Deep::Class Test::Deep::Cmp Test::Deep::Code Test::Deep::Hash \
Test::Deep::HashEach Test::Deep::HashElements Test::Deep::HashKeys Test::Deep::HashKeysOnly Test::Deep::Ignore \
Test::Deep::Isa Test::Deep::ListMethods Test::Deep::MM Test::Deep::Methods Test::Deep::NoTest \
Test::Deep::None Test::Deep::Number Test::Deep::Obj Test::Deep::Ref Test::Deep::RefType Test::Deep::Regexp \
Test::Deep::RegexpMatches  Test::Deep::RegexpRef Test::Deep::RegexpRefOnly Test::Deep::RegexpVersion \
Test::Deep::ScalarRef Test::Deep::ScalarRefOnly Test::Deep::Set Test::Deep::Shallow Test::Deep::Stack \
Test::Deep::String
%define require_list List::Util Scalar::Util Test::Builder

Name:           perl-%{meta_name}
Version: 1.130
Release: 1
Summary:        Extremely flexible deep comparison
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-Deep
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Test-Deep-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Test::Tester) >= 0.04

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Test-Deep-%{version} 


%build
%__perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
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
%doc Changes README TODO
%{perl_vendorlib}/Test/Deep.pm
%{perl_vendorlib}/Test/Deep/*
#%%{_mandir}/man3/Test::Deep.3
#%%{_mandir}/man3/Test::Deep::NoTest.3


%changelog
* Mon Nov 15 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.130-1
- Update to 1.130

* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.128-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Tue Jul 16 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.128-1
- Port to AIX.
