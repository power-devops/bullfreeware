%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-URI
Version:        1.76
Release:        1
Summary:        A Perl module implementing URI parsing and manipulation
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/URI
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/URI-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

# !! BEWARE !!
# Some URI::... version is NOT the main version.
# See https://cpants.cpanauthors.org/release/OALDERS/URI-%version at each release
Provides:       perl(URI)              = %version
Provides:       perl(URI::Escape)      = 3.31
Provides:       perl(URI::Heuristic)   = 4.20
Provides:       perl(URI::IRI)         = %version
Provides:       perl(URI::QueryParam)  = %version
Provides:       perl(URI::Split)       = %version
Provides:       perl(URI::URL)         = 5.04
Provides:       perl(URI::WithBase)    = 2.20
Provides:       perl(URI::data)        = %version
Provides:       perl(URI::file)        = 4.21
Provides:       perl(URI::file::Base)  = %version
Provides:       perl(URI::file::FAT)   = %version
Provides:       perl(URI::file::Mac)   = %version
Provides:       perl(URI::file::OS2)   = %version
Provides:       perl(URI::file::QNX)   = %version
Provides:       perl(URI::file::Unix)  = %version
Provides:       perl(URI::file::Win32) = %version
Provides:       perl(URI::ftp)         = %version
Provides:       perl(URI::gopher)      = %version
Provides:       perl(URI::http)        = %version
Provides:       perl(URI::https)       = %version
Provides:       perl(URI::ldap)        = %version
Provides:       perl(URI::ldapi)       = %version
Provides:       perl(URI::ldaps)       = %version
Provides:       perl(URI::mailto)      = %version
Provides:       perl(URI::mms)         = %version
Provides:       perl(URI::news)        = %version
Provides:       perl(URI::nntp)        = %version
Provides:       perl(URI::pop)         = %version
Provides:       perl(URI::rlogin)      = %version
Provides:       perl(URI::rsync)       = %version
Provides:       perl(URI::rtsp)        = %version
Provides:       perl(URI::rtspu)       = %version
Provides:       perl(URI::sftp)        = %version
Provides:       perl(URI::sip)         = %version
Provides:       perl(URI::sips)        = %version
Provides:       perl(URI::snews)       = %version
Provides:       perl(URI::ssh)         = %version
Provides:       perl(URI::telnet)      = %version
Provides:       perl(URI::tn3270)      = %version
Provides:       perl(URI::urn)         = %version
Provides:       perl(URI::urn::isbn)   = %version
Provides:       perl(URI::urn::oid)    = %version


Requires:       perl(perl)            >= 5.30
Requires:       perl(Carp)
Requires:       perl(Cwd)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(Exporter)        >= 5.57
Requires:       perl(MIME::Base64)
Requires:       perl(Net::Domain)
Requires:       perl(Scalar::Util)
Requires:       perl(constant)
Requires:       perl(integer)
Requires:       perl(overload)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(utf8)
Requires:       perl(warnings)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl)            >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)       >= 0.96
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(utf8)

# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)        >= 5.57
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Net::Domain)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(constant)
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)


%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).


%prep
%setup -q -n URI-%{version}


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
%defattr(-,root,system,-)
%doc Changes CONTRIBUTING.md
%{perl_vendorlib}/URI.pm
%{perl_vendorlib}/URI/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.76-1
- Port on AIX.
