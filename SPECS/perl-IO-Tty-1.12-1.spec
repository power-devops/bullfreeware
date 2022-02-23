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

Name:           perl-%{perl_version}-IO-Tty
Version:        1.12
Release:        1
Summary:        Perl interface to pseudo tty's
License:        (GPL+ or Artistic) and BSD
URL:            https://metacpan.org/release/IO-Tty
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/IO-Tty-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      ppc

Provides: perl(IO::Pty) = %{version}
Provides: perl(IO::Tty) = %{version}

Requires: perl(:MODULE_COMPAT_%{perl_version})
Requires: perl(perl) >= 5.30

# Build requires
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: gcc
BuildRequires: make


%description
IO::Tty and IO::Pty provide an interface to pseudo tty's.


%prep
%setup -q -n IO-Tty-%{version} 
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

cd 32bit
%perl32 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake

cd ../64bit
%perl64 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake


%check
%if %{with dotests}
cd 32bit
gmake -k test TEST_VERBOSE=1
cd ../64bit
gmake -k test TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 32bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

cd ../64bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc 32bit/ChangeLog 32bit/README
%{perl_vendorarch32}/auto/IO/
%{perl_vendorarch32}/IO/
%{perl_vendorarch64}/auto/IO/
%{perl_vendorarch64}/IO/
%{_mandir}/man3/IO::Pty.3
%{_mandir}/man3/IO::Tty.3
%{_mandir}/man3/IO::Tty::Constant.3


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
