# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name Term-ReadKey
%define desc Term::ReadKey is a compiled perl module dedicated to providing simple \
control over terminal driver modes (cbreak, raw, cooked, etc.) \
support for non-blocking reads, if the architecture allows, and some \
generalized handy functions for working with terminals.  One of the \
main goals is to have the functions as portable as possible, so you \
can just plug in "use Term::ReadKey" on any architecture and have a \
good likelyhood of it working.
%define provide_list Term::ReadKey
# No requires # %%define require_list 

Name:           perl-Term-ReadKey
Version:        2.38
Release:        3
Epoch:          1
Summary:        A perl module for simple terminal control
License:        Perl5
URL:            https://metacpan.org/pod/Term::ReadKey
Source0:        https://cpan.metacpan.org/authors/id/J/JS/JSTOWE/TermReadKey-2.38.tar.gz
Source1000:     %{name}-%{version}-%{release}.build.log

BuildArch:      ppc

%perl_meta_provides
%perl_meta_requires

BuildRequires:  findutils, sed
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl(perl)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.58
BuildRequires:  perl(Expect)

Obsoletes: perl-5.32-Term-ReadKey, perl-5.30-Term-ReadKey

%description
%desc

%perl_module
%perl_module_desc


%prep
%setup -q -n TermReadKey-%{version} 
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/

%build
export CC=gcc
export AR="/usr/bin/ar"

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
export OBJECT_MODE=64
gmake -k test TEST_VERBOSE=1
cd ../64bit
export OBJECT_MODE=32
gmake -k test TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"
export PATH="/opt/freeware/bin:$PATH"
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 32bit
# Bad perl called.
sed -i 's|#!/usr/bin/perl|#!/usr/bin/env perl|g' example/test.pl
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

cd ../64bit
sed -i 's|#!/usr/bin/perl|#!/usr/bin/env perl|g' example/test.pl
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)

%files -n %module_name
%defattr(-,root,system,-)
%doc 32bit/Changes 32bit/README 32bit/example/test.pl
%{perl_vendorarch32}/Term/ReadKey.pm
%{perl_vendorarch32}/auto/Term/ReadKey/ReadKey.so
%{perl_vendorarch64}/Term/ReadKey.pm
%{perl_vendorarch64}/auto/Term/ReadKey/ReadKey.so
#%%{_mandir}/man3/*


%changelog
* Tue Oct 26 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 2.38-3
- Mass rebuild for new version of perl.
- Update for new perl.
- Add metapackage.

* Tue Jul 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 2.38-2
- Add defattr
- Rebuild with perl 5.32

* Fri Oct 11 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.38-1
- First port on AIX
