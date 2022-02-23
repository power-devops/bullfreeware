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

Name:           perl-Test-Deep
Version:        1.128
Release:        1
Summary:        Extremely flexible deep comparison
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Test-Deep
Source0:        https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Test-Deep-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Test::Deep) = %{version}
Provides: perl(Test::Deep::All)
Provides: perl(Test::Deep::Any)
Provides: perl(Test::Deep::Array)
Provides: perl(Test::Deep::ArrayEach)
Provides: perl(Test::Deep::ArrayElementsOnly)
Provides: perl(Test::Deep::ArrayLength)
Provides: perl(Test::Deep::ArrayLengthOnly)
Provides: perl(Test::Deep::Blessed)
Provides: perl(Test::Deep::Boolean)
Provides: perl(Test::Deep::Cache)
Provides: perl(Test::Deep::Cache::Simple)
Provides: perl(Test::Deep::Class)
Provides: perl(Test::Deep::Cmp)
Provides: perl(Test::Deep::Code)
Provides: perl(Test::Deep::Hash)
Provides: perl(Test::Deep::HashEach)
Provides: perl(Test::Deep::HashElements)
Provides: perl(Test::Deep::HashKeys)
Provides: perl(Test::Deep::HashKeysOnly)
Provides: perl(Test::Deep::Ignore)
Provides: perl(Test::Deep::Isa)
Provides: perl(Test::Deep::ListMethods)
Provides: perl(Test::Deep::MM)
Provides: perl(Test::Deep::Methods)
Provides: perl(Test::Deep::NoTest)
Provides: perl(Test::Deep::None)
Provides: perl(Test::Deep::Number)
Provides: perl(Test::Deep::Obj)
Provides: perl(Test::Deep::Ref)
Provides: perl(Test::Deep::RefType)
Provides: perl(Test::Deep::Regexp)
Provides: perl(Test::Deep::RegexpMatches)
Provides: perl(Test::Deep::RegexpOnly)
Provides: perl(Test::Deep::RegexpRef)
Provides: perl(Test::Deep::RegexpRefOnly)
Provides: perl(Test::Deep::RegexpVersion)
Provides: perl(Test::Deep::ScalarRef)
Provides: perl(Test::Deep::ScalarRefOnly)
Provides: perl(Test::Deep::Set)
Provides: perl(Test::Deep::Shallow)
Provides: perl(Test::Deep::Stack)
Provides: perl(Test::Deep::String)

Requires: perl(perl) >= 5.30

Requires: perl(List::Util) >= 1.09
Requires: perl(Scalar::Util) >= 1.09
Requires: perl(Test::Builder)

# Build requires
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(Test::Tester) >= 0.04


%description
Test::Deep gives you very flexible ways to check that the result you
got is the result you were expecting. At its simplest it compares two
structures by going through each level, ensuring that the values
match, that arrays and hashes have the same elements and that
references are blessed into the correct class. It also handles
circular data structures without getting caught in an infinite loop.


%prep
%setup -q -n Test-Deep-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake


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
%doc Changes README TODO
%{perl_vendorlib}/Test/Deep.pm
%{perl_vendorlib}/Test/Deep/*
%{_mandir}/man3/Test::Deep.3
%{_mandir}/man3/Test::Deep::NoTest.3


%changelog

* Tue Jul 16 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.128-1
- Port to AIX.
