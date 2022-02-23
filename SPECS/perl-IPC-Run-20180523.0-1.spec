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

Name:           perl-IPC-Run
Version:        20180523.0
Release:        1
Summary:        Perl module for interacting with child processes
# the rest:                     GPL+ or Artistic
# The Win32* modules are not part of the binary RPM package
# lib/IPC/Run/Win32Helper.pm:   GPLv2 or Artistic
# lib/IPC/Run/Win32Pump.pm:     GPLv2 or Artistic
# lib/IPC/Run/Win32IO.pm:       GPLv2 or Artistic
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/IPC-Run
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/IPC-Run-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

BuildArch:      noarch

Provides: perl(Mock::Config) = %{version}
Provides: perl(IPC::Run) = %{version}
Provides: perl(IPC::Run::Debug) = %{version}
Provides: perl(IPC::Run::IO) = %{version}
Provides: perl(IPC::Run::Timer) = %{version}
Provides: perl(IPC::Run::Win32Helper) = %{version}
Provides: perl(IPC::Run::Win32IO) = %{version}
Provides: perl(IPC::Run::Win32Pump) = %{version}

Requires: perl(perl) >= 5.30

Requires: perl(IO::Pty) >= 1.08
Requires: perl(Test::More) >= 0.47

# Build requires
BuildRequires: perl(Readonly)
BuildRequires: perl(Readonly::Array)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)


%description
IPC::Run allows you run and interact with child processes using files,
pipes, and pseudo-ttys. Both system()-style and scripted usages are
supported and may be mixed. Likewise, functional and OO API styles are
both supported and may be mixed.

Various redirection operators reminiscent of those seen on common Unix
and DOS command lines are provided.


%prep
%setup -q -n IPC-Run-%{version}

# Remove Windows-only features that could add unnecessary dependencies
rm -f lib/IPC/Run/Win32*
sed -i -e '/^lib\/IPC\/Run\/Win32.*/d' MANIFEST
rm -f t/win32_*
sed -i -e '/^t\/win32_.*/d' MANIFEST


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

%perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake


%check
%if %{with dotests}
gmake -k test TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc Changes README TODO LICENSE
%doc abuse/ eg/
%{perl_vendorlib}/IPC/
%{_mandir}/man3/IPC::Run.3*
%{_mandir}/man3/IPC::Run::Debug.3*
%{_mandir}/man3/IPC::Run::IO.3*
%{_mandir}/man3/IPC::Run::Timer.3*


%changelog
* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 0.03-1
- Port to AIX
