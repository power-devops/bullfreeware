%bcond_without dotests

%define perl  %{_bindir}/perl_32
%define perl32  %{_bindir}/perl_32
%define perl64  %{_bindir}/perl_64
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")

%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

Name:           perl-HTTP-Daemon
Version:        6.06
Release:        1
Summary:        Simple HTTP server class
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/HTTP-Daemon
Source0:        https://cpan.metacpan.org/authors/id/O/OA/OALDERS/HTTP-Daemon-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Provides:       perl(HTTP::Daemon)            = %version

Requires:       perl(perl)                      >= 5.30
Requires:       perl(Carp)
Requires:       perl(HTTP::Date)                >= 6
Requires:       perl(HTTP::Request)             >= 6
Requires:       perl(HTTP::Response)            >= 6
Requires:       perl(HTTP::Status)              >= 6
Requires:       perl(IO::Socket::IP)
Requires:       perl(LWP::MediaTypes)           >= 6
Requires:       perl(Socket)
Requires:       perl(Sys::Hostname)
Requires:       perl(strict)
Requires:       perl(warnings)

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make

# Build
BuildRequires:  perl(perl) >= 5.30
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(URI)

# Configure
BuildRequires:  perl(Module::Build::Tiny)       >= 0.34
# Optionally, if no Module::Build::Tiny
# BuildRequires:  perl(ExtUtils::MakeMaker)


# To test
BuildRequires:  perl(Carp)
BuildRequires:  perl(HTTP::Date)                >= 6
BuildRequires:  perl(HTTP::Request)             >= 6
BuildRequires:  perl(HTTP::Response)            >= 6
BuildRequires:  perl(HTTP::Status)              >= 6
BuildRequires:  perl(IO::Socket::IP)
BuildRequires:  perl(LWP::MediaTypes)           >= 6
BuildRequires:  perl(Socket)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)


%description
Instances of the HTTP::Daemon class are HTTP/1.1 servers that listen on a
socket for incoming requests. The HTTP::Daemon is a subclass of
IO::Socket::IP, so you can perform socket operations directly on it too.


%prep
%setup -q -n HTTP-Daemon-%{version}


%build
%perl Build.PL --installdirs=vendor
./Build

# This works, but mainteners prefers Build.pl.
# Note Fedora packagers prefer this way.
#%perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
#gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
./Build install --destdir=%{buildroot} --create_packlist=0

#gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

%{_fixperms} -c %{buildroot}

# Move man files from share/man to man.
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man ${RPM_BUILD_ROOT}%{_mandir}

%check
%if %{with dotests}
./Build test
  #gmake test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc Changes CONTRIBUTING README LICENCE
%{perl_vendorlib}/HTTP/*
%{_mandir}/man3/*


%changelog
* Wed Dec 04 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 6.01-1
- Port on AIX.
