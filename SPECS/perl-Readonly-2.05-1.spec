%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")
# For script modules
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)
# For compiled modules
%define perl_vendorarch32 %(eval "`%{perl32} -V:installvendorarch`"; echo $installvendorarch)
%define perl_vendorarch64 %(eval "`%{perl64} -V:installvendorarch`"; echo $installvendorarch)

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           perl-Readonly
Version:        2.05
Release:        1
Summary:        Facility for creating read-only scalars, arrays, hashes
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Readonly
Source0:        https://cpan.metacpan.org/authors/id/S/SA/SANKO/Readonly-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Readonly) = %{version}
Provides: perl(Readonly::Array)
Provides: perl(Readonly::Hash)
Provides: perl(Readonly::Scalar)

Requires: perl(perl) >= 5.30

# Build requires
BuildRequires: perl(Test::More)
BuildRequires: perl(Module::Build::Tiny)
BuildRequires: gcc
BuildRequires: make


%description
Readonly provides a facility for creating non-modifiable scalars,
arrays, and hashes. Any attempt to modify a Readonly variable throws
an exception.

Readonly:
* Creates scalars, arrays (not lists), and hashes
* Creates variables that look and work like native perl variables
* Creates global or lexical variables
* Works at run-time or compile-time
* Works with deep or shallow data structures
* Prevents reassignment of Readonly variables


%prep
%setup -q -n Readonly-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Build.PL --installdirs=vendor
./Build


%check
%if %{with dotests}
./Build test
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

./Build install --destdir=%{buildroot} --create_packlist=0

%{_fixperms} $RPM_BUILD_ROOT/*

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc LICENSE Changes README.md eg/benchmark.pl t/
%{perl_vendorlib}/Readonly.pm
%{_mandir}/man3/Readonly.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
