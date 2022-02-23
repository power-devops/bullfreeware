# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Mock-Config
%define desc This module can be for temporarily set Config or XSConfig values.
%define provide_list Mock::Config
# No requires # %%define require_list 

Name:           perl-%{meta_name}
Version:        0.03
Release:        2
Summary:        Temporarily set Config or XSConfig values
License:        Artistic 2.0
URL:            https://metacpan.org/release/Mock-Config
Source0:        https://cpan.metacpan.org/authors/id/R/RU/RURBAN/Mock-Config-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(Test::More)
# Configure requires
BuildRequires: perl(ExtUtils::MakeMaker)

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Mock-Config-%{version} 


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
%{perl_vendorlib}/Mock/Config.pm
#%%{_mandir}/man3/Mock::Config.3


%changelog
* Tue Oct 26 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 0.03-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
