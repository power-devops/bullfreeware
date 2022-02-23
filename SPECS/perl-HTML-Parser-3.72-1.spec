%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorarch32 %(eval "`%{perl32} -V:installvendorarch`"; echo $installvendorarch)
%define perl_vendorarch64 %(eval "`%{perl64} -V:installvendorarch`"; echo $installvendorarch)


Name:           perl-%{perl_version}-HTML-Parser
Summary:        Perl module for parsing HTML
Version:        3.72
Release:        1
License:        GPL+ or Artistic

URL:            https://metacpan.org/release/HTML-Parser
Source0:        https://cpan.metacpan.org/authors/id/G/GA/GAAS/HTML-Parser-%{version}.tar.gz 
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      ppc

Provides:       perl(HTML::Entities)             = 3.69
Provides:       perl(HTML::Filter)               = 3.72
Provides:       perl(HTML::HeadParser)           = 3.71
Provides:       perl(HTML::LinkExtor)            = 3.69
Provides:       perl(HTML::Parser)               = 3.72
Provides:       perl(HTML::PullParser)           = 3.57
Provides:       perl(HTML::TokeParser)           = 3.69

Requires:       perl(:MODULE_COMPAT_%{perl_version})
Requires:       perl(HTML::Tagset)              >= 3
Requires:       perl(XSLoader)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

BuildRequires:  perl(:MODULE_COMPAT_%{perl_version})
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)

# To test
BuildRequires:  perl(HTML::Tagset)              >= 3
BuildRequires:  perl(XSLoader)


%description
The HTML-Parser module for perl to parse and extract information from
HTML documents, including the HTML::Entities, HTML::HeadParser,
HTML::LinkExtor, HTML::PullParser, and HTML::TokeParser modules.


%prep
%setup -q -n HTML-Parser-%{version}
mkdir /tmp/perl-HTML-Parser-32bit
mv ./* /tmp/perl-HTML-Parser-32bit/
cp -r /tmp/perl-HTML-Parser-32bit/ ./64bit
mv /tmp/perl-HTML-Parser-32bit/ ./32bit


%build
cd 32bit
export OBJECT_MODE=32
export CFLAGS="-D_GNU_SOURCE -D_LARGEFILE_SOURCE -pthread -maix32"
export LDFLAGS="-pthread -Wl,-bmaxdata:0x80000000"
%perl32 Makefile.PL INSTALLDIRS="vendor" OPTIMIZE="-O3" NO_PACKLIST=1 verbose
gmake

cd ../64bit
export OBJECT_MODE=64
export CFLAGS="-D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -pthread -maix64"
export LDFLAGS="-pthread"
%perl64 Makefile.PL INSTALLDIRS="vendor" OPTIMIZE="-O3" NO_PACKLIST=1 verbose
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
cd 64bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
cd ../32bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

%{_fixperms} -c %{buildroot}

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
%doc 32bit/Changes 32bit/README
%{perl_vendorarch32}/HTML/*
%{perl_vendorarch64}/HTML/*
%{perl_vendorarch32}/auto/HTML/Parser/Parser.so
%{perl_vendorarch64}/auto/HTML/Parser/Parser.so
%{_mandir}/man3/*


%changelog
* Fri Dec 06 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 3.72-1
- Port on AIX.
