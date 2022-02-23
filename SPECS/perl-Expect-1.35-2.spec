# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Expect
%define desc This module provides Expect-like functionality to Perl. Expect is \
a tool for automating interactive applications such as telnet, ftp, \
passwd, fsck, rlogin, tip, etc.
%define provide_list Expect
%define require_list Carp Exporter Fcntl IO::Handle IO::Pty IO::Tty POSIX
# Provides by perl but not found
# Requires:       perl(Errno)


Name:           perl-Expect
Version:        1.35
Release: 2
Summary:        Expect for Perl
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Expect
Source0:        https://cpan.metacpan.org/authors/id/J/JA/JACOBY/Expect-%{version}.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log
BuildArch:      noarch

Patch1:         perl-Expect-1.35-test.patch

%perl_meta_provides
%perl_meta_requires

BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  sed

BuildRequires:  perl(perl)                >= 5.30
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More)          >= 1.00
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.64
# Runtime requires for test.
BuildRequires:  perl(Carp)
BuildRequires:  perl(IO::Pty)
#BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Pty)             >= 1.11
BuildRequires:  perl(IO::Tty)             >= 1.11
BuildRequires:  perl(POSIX)


%description
%desc

%perl_module
%perl_module_desc

%prep
%setup -q -n Expect-%{version}

%patch1 -p1 -b .test


%build
%__perl Makefile.PL INSTALLDIRS="vendor"  NO_PACKLIST=1 verbose
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} -c %{buildroot}

sed -i 's|/usr/bin/perl|/usr/bin/env perl|g' examples/ssh.pl
sed -i 's|/usr/bin/perl|/usr/bin/env perl|g' tutorial/*
sed -i 's|/usr/local/bin/perl|/usr/bin/env perl|g' examples/kibitz/kibitz
sed -i 's|/usr/local/bin/perl|/usr/bin/env perl|g' tutorial/*


%check
%if %{with dotests}
  gmake test
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc LICENSE
%doc Changes README.md examples/ tutorial/
%{perl_vendorlib}/Expect.pm
#%%{_mandir}/man3/Expect.3*


%changelog
* Tue Oct 19 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.35-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Tue Oct 22 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 1.35-1
- First port to AIX.
