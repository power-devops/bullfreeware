# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name IO-Tty
%define desc IO::Tty and IO::Pty provide an interface to pseudo tty's.
%define provide_list IO::Pty IO::Tty
#%%define require_list # No require

Name:           perl-%{meta_name}
Version: 1.16
Release: 2
Epoch:          1
Summary:        Perl interface to pseudo tty's
License:        (GPL+ or Artistic) and BSD
URL:            https://metacpan.org/release/IO-Tty
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/IO-Tty-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

%perl_meta_provides
%perl_meta_requires

# Build requires
BuildRequires: perl(Test::More)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: gcc
BuildRequires: make

Obsoletes: perl-5.32-IO-Tty, perl-5.30-IO-Tty

# Reported. See issue https://github.com/toddr/IO-Tty/issues/32

Patch1: IO-Tty-1.16_winsize.patch

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n IO-Tty-%{version} 
%patch1 -p1

mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
export CC=gcc

cd 32bit
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export CFLAGS="-D_LARGE_FILES"
%__perl32 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake

cd ../64bit
export LDFLAGS=""
export CFLAGS=""
%__perl64 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake


%check
%if %{with dotests}
cd 32bit
gmake -k test TEST_VERBOSE=1
cd ../64bit
gmake -k test TEST_VERBOSE=1
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 32bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

cd ../64bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc 32bit/ChangeLog 32bit/README
%{perl_vendorarch32}/auto/IO/
%{perl_vendorarch32}/IO/
%{perl_vendorarch64}/auto/IO/
%{perl_vendorarch64}/IO/
#%%{_mandir}/man3/IO::Pty.3
#%%{_mandir}/man3/IO::Tty.3
#%%{_mandir}/man3/IO::Tty::Constant.3


%changelog
* Tue Nov 16 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16-2
- Rebuild 1.16

* Mon Nov 15 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.16-1
- Update to 1.16

* Tue Oct 19 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.12-3
- Mass rebuild for new version of perl.
- Update for new perl.

* Tue Jul 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.12-2
- Add defattr
- Rebuild with perl 5.32

* Mon Jul 15 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.12-1
- Port to AIX
