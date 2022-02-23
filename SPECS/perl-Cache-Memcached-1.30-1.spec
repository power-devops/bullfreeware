%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-Cache-Memcached
Version:        1.30
Release:        1
Summary:        Perl client for memcached
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Cache-Memcached
Source0:        https://cpan.metacpan.org/authors/id/D/DO/DORMANDO/Cache-Memcached-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(Cache::Memcached)            =  %version
Provides:       perl(Cache::Memcached::GetParser) =  %version

Requires:       perl(perl)                >= 5.30
Requires:       perl(Encode)
Requires:       perl(Storable)
Requires:       perl(String::CRC32)
Requires:       perl(Time::HiRes)

BuildRequires:  coreutils
BuildRequires:  make

BuildRequires:  perl(perl)                >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
# Runtime requires for test.
BuildRequires:  perl(Encode)
BuildRequires:  perl(Storable)
BuildRequires:  perl(String::CRC32)
BuildRequires:  perl(Time::HiRes)


%description
Cache::Memcached - client library for memcached (memory cache daemon)


%prep
%setup -q -n Cache-Memcached-%{version}


%build
%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} -c %{buildroot}


%check
%if %{with dotests}
  gmake test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README ChangeLog
%dir %{perl_vendorlib}/Cache/
%dir %{perl_vendorlib}/Cache/Memcached/
%{perl_vendorlib}/Cache/Memcached.pm
%{perl_vendorlib}/Cache/Memcached/GetParser.pm
%{_mandir}/man3/Cache::Memcached.3*


%changelog
* Wed Oct 23 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.7-1
- First port to AIX.
