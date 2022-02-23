# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Readonly
%define desc Readonly provides a facility for creating non-modifiable scalars, \
arrays, and hashes. Any attempt to modify a Readonly variable throws \
an exception. \
\
Readonly: \
* Creates scalars, arrays (not lists), and hashes \
* Creates variables that look and work like native perl variables \
* Creates global or lexical variables \
* Works at run-time or compile-time \
* Works with deep or shallow data structures \
* Prevents reassignment of Readonly variables
%define provide_list Readonly Readonly::Array Readonly::Hash Readonly::Scalar
# No requires # %%define require_list 

Name:           perl-%{meta_name}
Version:        2.05
Release: 2
Summary:        Facility for creating read-only scalars, arrays, hashes
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Readonly
Source0:        https://cpan.metacpan.org/authors/id/S/SA/SANKO/Readonly-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(Test::More)
BuildRequires: perl(Module::Build::Tiny)
BuildRequires: gcc
BuildRequires: make

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n Readonly-%{version} 


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
%{_fixperms} $RPM_BUILD_ROOT/*

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc LICENSE Changes README.md eg/benchmark.pl t/
%{perl_vendorlib}/Readonly.pm
#%%{_mandir}/man3/Readonly.3


%changelog
* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 2.05-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.05-1
- Port to AIX
