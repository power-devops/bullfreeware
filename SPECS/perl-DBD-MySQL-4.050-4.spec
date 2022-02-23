# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name DBD-MySQL
%define desc An implementation of DBI for MySQL for Perl.
%define provide_list Bundle::DBD::mysql DBD::mysql DBD::mysql::GetInfo
%define require_list DBI

Name:           perl-%{meta_name}
Version:        4.050
Release:        4
Epoch:          1
Summary:        A MySQL interface for perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-mysql/
Source0:        https://cpan.metacpan.org/authors/id/D/DV/DVEEDEN/DBD-mysql-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      ppc

%perl_meta_provides
%perl_meta_requires

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
BuildRequires:  mariadb-connector-c       >= 3.1.4-3
BuildRequires:  mariadb-connector-c-devel >= 3.1.4-3
#BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Obsoletes: perl-5.32-DBD-MySQL, perl-5.30-DBD-MySQL

%description
%desc

%perl_module
%perl_module_desc


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
export AR="/usr/bin/ar"

cd 64bit
export OBJECT_MODE=64
export CFLAGS="-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -pthread -maix64"
export LDFLAGS="-pthread"
%{__perl64} Makefile.PL INSTALLDIRS=vendor --ssl  NO_PACKLIST=1 verbose optimize="-O3" --mysql_config=%{_bindir}/mariadb_config_64
gmake
cd ../32bit
export OBJECT_MODE=32
export CFLAGS="-D_GNU_SOURCE -D_LARGEFILE_SOURCE -pthread -maix32 -D_LARGE_FILES"
export LDFLAGS="-pthread -Wl,-bmaxdata:0x80000000"
%{__perl32} Makefile.PL INSTALLDIRS=vendor --ssl  NO_PACKLIST=1 verbose optimize="-O3" --mysql_config=%{_bindir}/mariadb_config_32
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar"

cd 64bit
make pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
cd ../32bit
make pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

%{_fixperms} $RPM_BUILD_ROOT/*

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +


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
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc 64bit/Changes 64bit/README.md 64bit/LICENSE
%{perl_vendorarch32}/Bundle/*
%{perl_vendorarch64}/Bundle/*
%{perl_vendorarch32}/DBD/*
%{perl_vendorarch64}/DBD/*
%{perl_vendorarch32}/auto/DBD/*
%{perl_vendorarch64}/auto/DBD/*
#%%{_mandir}/man3/*.3*


%changelog
* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 4.050-4
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Tue Jul 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.050-3
- Add defattr
- Rebuild with perl 5.32

* Fri Oct 11 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.050-2
- Rebuild with right library.

* Tue Jul 16 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 4.050-1
- Update to version 4.050-1

* Mon Dec 08 2014 Michael Perzl <michael@perzl.org> - 4.028-1
- updated to version 4.028-1

* Fri Feb 22 2013 Michael Perzl <michael@perzl.org> - 4.022-1
- first version for AIX V5.1 and higher
