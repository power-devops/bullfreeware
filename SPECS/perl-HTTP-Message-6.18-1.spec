%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-HTTP-Message
Version:        6.18
Release:        1
Summary:        HTTP style message
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/HTTP-Message
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Message-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(HTTP::Config)               = %version
Provides:       perl(HTTP::Headers)              = %version
Provides:       perl(HTTP::Headers::Auth)        = %version
Provides:       perl(HTTP::Headers::ETag)        = %version
Provides:       perl(HTTP::Headers::Util)        = %version
Provides:       perl(HTTP::Message)              = %version
Provides:       perl(HTTP::Request)              = %version
Provides:       perl(HTTP::Request::Common)      = %version
Provides:       perl(HTTP::Response)             = %version
Provides:       perl(HTTP::Status)               = %version


Requires:       perl(perl)                      >= 5.30
Requires:       perl(Carp)
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(Encode)                    >= 2.21
Requires:       perl(Encode::Locale)            >= 1
Requires:       perl(Exporter)                  >= 5.57
Requires:       perl(HTTP::Date)                >= 6
Requires:       perl(IO::Compress::Bzip2)       >= 2.21
Requires:       perl(IO::Compress::Deflate)
Requires:       perl(IO::Compress::Gzip)
Requires:       perl(IO::HTML)
Requires:       perl(IO::Uncompress::Bunzip2)   >= 2.21
Requires:       perl(IO::Uncompress::Gunzip)
Requires:       perl(IO::Uncompress::Inflate)
Requires:       perl(IO::Uncompress::RawInflate)
Requires:       perl(LWP::MediaTypes)
Requires:       perl(MIME::Base64)              >= 2.1
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(Storable)
Requires:       perl(URI)                       >= 1.1
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(warnings)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(PerlIO::encoding)
BuildRequires:  perl(Test::More)                >= 0.88
BuildRequires:  perl(Time::Local)
BuildRequires:  perl(Try::Tiny)

# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Raw::Zlib)
BuildRequires:  perl(Encode)                    >= 2.21
BuildRequires:  perl(Encode::Locale)            >= 1
BuildRequires:  perl(Exporter)                  >= 5.57
BuildRequires:  perl(HTTP::Date)                >= 6
BuildRequires:  perl(IO::Compress::Bzip2)       >= 2.21
BuildRequires:  perl(IO::Compress::Deflate)
BuildRequires:  perl(IO::Compress::Gzip)
BuildRequires:  perl(IO::HTML)
BuildRequires:  perl(IO::Uncompress::Bunzip2)   >= 2.21
BuildRequires:  perl(IO::Uncompress::Gunzip)
BuildRequires:  perl(IO::Uncompress::Inflate)
BuildRequires:  perl(IO::Uncompress::RawInflate)
BuildRequires:  perl(LWP::MediaTypes)
BuildRequires:  perl(MIME::Base64)              >= 2.1
BuildRequires:  perl(MIME::QuotedPrint)
BuildRequires:  perl(Storable)
BuildRequires:  perl(URI)                       >= 1.1
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
The HTTP-Message distribution contains classes useful for representing the
messages passed in HTTP style communication.  These are classes representing
requests, responses and the headers contained within them.


%prep
%setup -q -n HTTP-Message-%{version}


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
%doc Changes README.md CONTRIBUTING.md
%{perl_vendorlib}/HTTP/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.05-1
- Port on AIX.
