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

Name:           perl-Error
Version:        0.17027
Release:        1
Summary:        Error/exception handling in an OO-ish way
License:        (GPL+ or Artistic) and MIT
URL:            https://metacpan.org/release/Error
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Error-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Error) = %{version}
Provides: perl(Error::Simple) = %{version}
Provides: perl(Error::WarnDie) = %{version}
Provides: perl(Error::subs) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(Scalar::Util)
Requires: perl(overload)
Requires: perl(strict)
Requires: perl(vars)
Requires: perl(warnings)

# Build requires
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::Handle)
BuildRequires: perl(IPC::Open3)
BuildRequires: perl(Module::Build) >= 0.28
BuildRequires: perl(Test::More) >= 0.88
BuildRequires: perl(base)
BuildRequires: perl(lib)


%description
The Error package provides two interfaces. Firstly Error provides a
procedural interface to exception handling. Secondly Error is a base class
for errors/exceptions that can either be thrown, for subsequent catch, or
can simply be recorded.


%prep
%setup -q -n Error-%{version} 


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
%doc LICENSE
# GPL+ or Artistic
%doc ChangeLog Changes README examples/
%{perl_vendorlib}/Error.pm
%{_mandir}/man3/Error.3
# MIT
%{perl_vendorlib}/Error/Simple.pm
%{_mandir}/man3/Error::Simple.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
