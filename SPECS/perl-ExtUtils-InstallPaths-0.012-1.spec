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

Name:           perl-ExtUtils-InstallPaths
Version:        0.012
Release:        1
Summary:        Build.PL install path logic made easy
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/ExtUtils-InstallPaths
Source0:        http://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(ExtUtils::InstallPaths) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Carp)
Requires: perl(ExtUtils::Config) >= 0.002
Requires: perl(File::Spec::Functions)
Requires: perl(strict)
Requires: perl(warnings)

# Build requires
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(File::Temp)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
## Not provided by Perl package itself
BuildRequires: perl(ExtUtils::Config)


%description
This module tries to make install path resolution as easy as possible.

When you want to install a module, it needs to figure out where to install
things. The nutshell version of how this works is that default installation
locations are determined from ExtUtils::Config, and they may be individually
overridden by using the install_path attribute. An install_base attribute lets
you specify an alternative installation root like /home/foo and prefix does
something similar in a rather different (and more complicated) way. destdir
lets you specify a temporary installation directory like /tmp/install in case
you want to create bundled-up installable packages.


%prep
%setup -q -n ExtUtils-InstallPaths-%{version}

# Don't include VMS and Windows helpers, which may pull in unwelcome dependencies
#rm -f lib/ExtUtils/Helpers/{VMS,Windows}.pm
#perl -ni -e 'print unless /^lib\/ExtUtils\/Helpers\/(VMS|Windows)\.pm$/;' MANIFEST


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
%doc Changes LICENSE
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/ExtUtils::InstallPaths.3*



%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
