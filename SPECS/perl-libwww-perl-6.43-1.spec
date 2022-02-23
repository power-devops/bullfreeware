%bcond_without dotests

%define perl  %{_bindir}/perl_64
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)


Name:           perl-libwww-perl
Version:        6.43
Release:        1
Summary:        A Perl interface to the World-Wide Web
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/libwww-perl
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/libwww-perl-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(LWP)                        = %version
Provides:       perl(LWP::Authen::Basic)         = %version
Provides:       perl(LWP::Authen::Digest)        = %version
Provides:       perl(LWP::Authen::Ntlm)          = %version
Provides:       perl(LWP::ConnCache)             = %version
Provides:       perl(LWP::Debug)                 = %version
Provides:       perl(LWP::Debug::TraceHTTP)      = %version
Provides:       perl(LWP::DebugFile)             = %version
Provides:       perl(LWP::MemberMixin)           = %version
Provides:       perl(LWP::Protocol)              = %version
Provides:       perl(LWP::Protocol::cpan)        = %version
Provides:       perl(LWP::Protocol::data)        = %version
Provides:       perl(LWP::Protocol::file)        = %version
Provides:       perl(LWP::Protocol::ftp)         = %version
Provides:       perl(LWP::Protocol::gopher)      = %version
Provides:       perl(LWP::Protocol::http)        = %version
Provides:       perl(LWP::Protocol::loopback)    = %version
Provides:       perl(LWP::Protocol::mailto)      = %version
Provides:       perl(LWP::Protocol::nntp)        = %version
Provides:       perl(LWP::Protocol::nogo)        = %version
Provides:       perl(LWP::RobotUA)               = %version
Provides:       perl(LWP::Simple)                = %version
Provides:       perl(LWP::UserAgent)             = %version

Requires:       perl(perl)                      >= 5.30
Requires:       perl(Digest::MD5)
Requires:       perl(Encode)                    >= 2.12
Requires:       perl(Encode::Locale)
Requires:       perl(File::Listing)             >= 6
Requires:       perl(HTML::Entities)
Requires:       perl(HTML::HeadParser)
Requires:       perl(HTTP::Cookies)             >= 6
Requires:       perl(HTTP::Daemon)              >= 6
Requires:       perl(HTTP::Date)                >= 6
Requires:       perl(HTTP::Negotiate)           >= 6
Requires:       perl(HTTP::Request)             >= 6
Requires:       perl(HTTP::Request::Common)     >= 6
Requires:       perl(HTTP::Response)            >= 6
Requires:       perl(HTTP::Status)              >= 6
Requires:       perl(IO::Select)
Requires:       perl(IO::Socket)
Requires:       perl(LWP::MediaTypes)           >= 6
Requires:       perl(MIME::Base64)              >= 2.1
Requires:       perl(Net::FTP)                  >= 2.58
Requires:       perl(Net::HTTP)                 >= 6.18
Requires:       perl(Scalar::Util)
Requires:       perl(Try::Tiny)
Requires:       perl(URI)                       >= 1.10
Requires:       perl(URI::Escape)
Requires:       perl(WWW::RobotRules)           >= 6
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

BuildRequires:  coreutils
BuildRequires:  make

BuildRequires:  perl(perl)                      >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(Test::RequiresInternet)
# perl(CPAN::Meta::Requirements) >= 2.120620
# but our perl(CPAN::Meta::Requirements) does not provide version.
BuildRequires:  perl(CPAN::Meta::Requirements)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Module::Metadata)

# To test
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Encode)                    >= 2.12
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(File::Listing)             >= 6
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::HeadParser)
BuildRequires:  perl(HTTP::Cookies)             >= 6
BuildRequires:  perl(HTTP::Daemon)              >= 6
BuildRequires:  perl(HTTP::Date)                >= 6
BuildRequires:  perl(HTTP::Negotiate)           >= 6
BuildRequires:  perl(HTTP::Request)             >= 6
BuildRequires:  perl(HTTP::Request::Common)     >= 6
BuildRequires:  perl(HTTP::Response)            >= 6
BuildRequires:  perl(HTTP::Status)              >= 6
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::MediaTypes)           >= 6
BuildRequires:  perl(MIME::Base64)              >= 2.1
BuildRequires:  perl(Net::FTP)                  >= 2.58
BuildRequires:  perl(Net::HTTP)                 >= 6.18
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI)                       >= 1.10
BuildRequires:  perl(URI::Escape)
BuildRequires:  perl(WWW::RobotRules)           >= 6
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
The libwww-perl collection is a set of Perl modules which provides a simple and
consistent application programming interface to the World-Wide Web.  The main
focus of the library is to provide classes and functions that allow you to
write WWW clients. The library also contain modules that are of more general
use and even classes that help you implement simple HTTP servers.


%prep
%setup -q -n libwww-perl-%{version} 


%build
%perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

%{_fixperms} -c %{buildroot}


%check
%if %{with dotests}
  gmake test TEST_VERBOSE=1
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc Changes README.SSL
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/LWP/*
%{perl_vendorlib}/libwww/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*


%changelog
* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 6.19-1
- Port on AIX.
