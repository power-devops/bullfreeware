%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch32 %(eval "`%{perl32} -V:installvendorarch`"; echo $installvendorarch)
%define perl_vendorarch64 %(eval "`%{perl64} -V:installvendorarch`"; echo $installvendorarch)

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Name:           perl-%{perl_version}-DBD-MySQL
Version:        4.050
Release:        2
Summary:        A MySQL interface for perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-mysql/
Source0:        https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/DBD-mysql-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      ppc

Provides: perl(Bundle::DBD::mysql) = %{version}
Provides: perl(DBD::mysql) = %{version}
Provides: perl(DBD::mysql::GetInfo)

Requires: perl(:MODULE_COMPAT_%{perl_version})

Requires: perl(DBI) >= 1.609

# Build requires
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::Simple) >= 0.90
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(bigint)
## Not provided by perl base package
BuildRequires: perl(Test::Deep)

# Configure requires
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(ExtUtils::MakeMaker)
## Not provided by perl base package
BuildRequires: perl(DBI) >= 1.609
BuildRequires: perl(Devel::CheckLib) >= 1.09

BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  mariadb-connector-c
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel


%description 
An implementation of DBI for MySQL for Perl.


%prep
%setup -q -n DBD-mysql-%{version}
# Correct file permissions
find . -type f | xargs chmod -x
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cd 32bit && tar cf - . | (cd ../64bit ; tar xpf -)


%build
env | sort

export AR="/usr/bin/ar"

cd 64bit
%{perl64} Makefile.PL INSTALLDIRS=vendor --ssl  NO_PACKLIST=1 verbose optimize="-O3"
gmake
cd ../32bit
# Beware, mariadb-connector-c only in 64. May not work.
%{perl32} Makefile.PL INSTALLDIRS=vendor --ssl  NO_PACKLIST=1 verbose optimize="-O3"
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar"

cd 64bit
make pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT}
cd ../32bit
make pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT}

%{_fixperms} $RPM_BUILD_ROOT/*

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}


%check
%if %{with dotests}
cd 64bit
gmake -k test TEST_VERBOSE=1

cd ../32bit
gmake -k test TEST_VERBOSE=1
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc 64bit/Changes 64bit/README.md 64bit/LICENSE
%{perl_vendorarch32}/Bundle/*
%{perl_vendorarch64}/Bundle/*
%{perl_vendorarch32}/DBD/*
%{perl_vendorarch64}/DBD/*
%{perl_vendorarch32}/auto/DBD/*
%{perl_vendorarch64}/auto/DBD/*
%{_mandir}/man3/*.3*


%changelog
* Fri Oct 11 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.050-2
- Rebuild with right library.

* Tue Jul 16 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.050-1
- Update to version 4.050-1

* Mon Dec 08 2014 Michael Perzl <michael@perzl.org> - 4.028-1
- updated to version 4.028-1

* Fri Feb 22 2013 Michael Perzl <michael@perzl.org> - 4.022-1
- first version for AIX V5.1 and higher
