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

Name:           perl-inc-latest
Version:        0.500
Release:        1
Summary:        Use modules bundled in inc/ if they are newer than installed ones
License:        ASL 2.0
URL:            https://metacpan.org/release/inc-latest
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/inc-latest-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(inc::latest) = %{version}
Provides: perl(inc::latest::private) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Carp)
Requires: perl(ExtUtils::Installed)
Requires: perl(ExtUtils::MakeMaker)
Requires: perl(File::Basename)
Requires: perl(File::Copy)
Requires: perl(File::Path)
Requires: perl(File::Spec)
Requires: perl(IO::File)
Requires: perl(strict)
Requires: perl(warnings)

# Build requires
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec)


%description
The inc::latest module helps bootstrap configure-time dependencies for CPAN
distributions. These dependencies get bundled into the inc directory within
a distribution and are used by Makefile.PL or Build.PL.


%prep
%setup -q -n inc-latest-%{version} 


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
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
%doc Changes README LICENSE
%{perl_vendorlib}/inc/*
%{_mandir}/man3/inc::latest.3
%{_mandir}/man3/inc::latest::private.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
