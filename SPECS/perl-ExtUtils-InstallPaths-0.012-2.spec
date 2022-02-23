# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name ExtUtils-InstallPaths
%define desc This module tries to make install path resolution as easy as possible. \
\
When you want to install a module, it needs to figure out where to install\
things. The nutshell version of how this works is that default installation\
locations are determined from ExtUtils::Config, and they may be individually\
overridden by using the install_path attribute. An install_base attribute lets\
you specify an alternative installation root like /home/foo and prefix does\
something similar in a rather different (and more complicated) way. destdir\
lets you specify a temporary installation directory like /tmp/install in case\
you want to create bundled-up installable packages.
%define provide_list ExtUtils::InstallPaths
%define require_list Carp ExtUtils::Config File::Spec::Functions strict warnings

Name:           perl-ExtUtils-InstallPaths
Version:        0.012
Release: 2
Summary:        Build.PL install path logic made easy
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/ExtUtils-InstallPaths
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

# Build requires
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
## Not provided by Perl package itself
BuildRequires: perl(ExtUtils::Config)

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
%doc Changes LICENSE
%{perl_vendorlib}/ExtUtils/
#%%{_mandir}/man3/ExtUtils::InstallPaths.3*


%changelog
* Tue Oct 19 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 0.012-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.012-1
- Port to AIX
