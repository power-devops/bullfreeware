# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name IPC-Run
%define desc IPC::Run allows you run and interact with child processes using files, \
pipes, and pseudo-ttys. Both system()-style and scripted usages are \
supported and may be mixed. Likewise, functional and OO API styles are \
both supported and may be mixed. \
\
Various redirection operators reminiscent of those seen on common Unix \
and DOS command lines are provided.
%define provide_list IPC::Run IPC::Run::Debug IPC::Run::IO IPC::Run::Timer
# Removed IPC::Run::Win32Helper IPC::Run::Win32IO IPC::Run::Win32Pump)
%define require_list IO::Pty Test::More

Name:           perl-IPC-Run
Version: 20200505.0
Release: 1
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

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(Readonly)
BuildRequires: perl(Readonly::Array)
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: sed

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n IPC-Run-%{version}

# Remove Windows-only features that could add unnecessary dependencies
rm -f lib/IPC/Run/Win32*
sed -i -e '/^lib\/IPC\/Run\/Win32.*/d' MANIFEST
rm -f t/win32_*
sed -i -e '/^t\/win32_.*/d' MANIFEST


%build
%__perl Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose
gmake


%check
%if %{with dotests}
gmake -k test TEST_VERBOSE=1
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc Changes README TODO LICENSE
%doc abuse/ eg/
%{perl_vendorlib}/IPC/
#%%{_mandir}/man3/IPC::Run.3*
#%%{_mandir}/man3/IPC::Run::Debug.3*
#%%{_mandir}/man3/IPC::Run::IO.3*
#%%{_mandir}/man3/IPC::Run::Timer.3*


%changelog
* Mon Nov 15 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 20200505.0-1
- Update to 20200505.0

* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 20180523.0-2
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.
- Stop erroneously providing perl(IPC::Run::Win*)
- Stop erroneously providing perl(Mock::Config)

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 20180523.0-1
- Port to AIX
