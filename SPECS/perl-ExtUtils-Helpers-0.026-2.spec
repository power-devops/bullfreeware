# Name of the packae, without perl or perl version
%define meta_name ExtUtils-Helpers
# Description of the package
%define desc This module provides various portable helper functions for module building modules.
# List of perl provides, without perl(...), separated by spaces
# Version used is package version
%define provide_list ExtUtils::Helpers ExtUtils::Helpers::Unix ExtUtils::Helpers::VMS ExtUtils::Helpers::Windows
# List of perl requires, without perl(...), separated by spaces
# No version!
%define require_list Carp Exporter File::Basename File::Copy File::Spec::Functions Text::ParseWords strict warnings

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           perl-%{meta_name}
Version:        0.026
Release: 2
Summary:        Various portability utilities for module builders
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/%{meta_name}
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-Helpers-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

BuildRequires: perl(perl)

# Macros to create automatically perl provides and requires from provide_list and require_list.
%perl_meta_provides
%perl_meta_requires

%description
%desc

# Create perl<PERL_VER>-%%{name} subpackage.
%perl_module
%perl_module_desc

%prep
%setup -q -n %{meta_name}-%{version}


%build
%__perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1
gmake %{?_smp_mflags}


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
%defattr(-,root,system,-)

# Module subpackage. %%module_name is initialized by %%perl_module
%files -n %module_name
%defattr(-,root,system,-)
%doc Changes README LICENSE
%{perl_vendorlib}/ExtUtils/*
#%%{_mandir}/man3/ExtUtils::Helpers.3
#%%{_mandir}/man3/ExtUtils::Helpers::Unix.3


%changelog
* Tue Oct 19 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 0.026-2
- Mass rebuild for new version of perl.
- Update for new perl
- Creation of metapackage

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.026-1
- Port to AIX
