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

Name:           perl-%{perl_version}-DBI
Version:        1.642
Release:        1
Summary:        A database access API for perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
Source0:        http://www.cpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

Provides: perl(DBI) = %{version}
Provides: perl(Bundle::DBI) = 12.008696
Provides: perl(DBD::DBM) = 0.08
Provides: perl(DBD::ExampleP) = 12.014311
Provides: perl(DBD::File) = 0.44
Provides: perl(DBD::Gofer) = 0.015327
Provides: perl(DBD::Gofer::Policy::Base) = 0.010088
Provides: perl(DBD::Gofer::Policy::classic) = 0.010088
Provides: perl(DBD::Gofer::Policy::pedantic) = 0.010088
Provides: perl(DBD::Gofer::Policy::rush) = 0.010088
Provides: perl(DBD::Gofer::Transport::Base) = 0.014121
Provides: perl(DBD::Gofer::Transport::corostream)
Provides: perl(DBD::Gofer::Transport::null) = 0.010088
Provides: perl(DBD::Gofer::Transport::pipeone) = 0.010088
Provides: perl(DBD::Gofer::Transport::stream) = 0.014599
Provides: perl(DBD::Mem) = 0.001
Provides: perl(DBD::NullP) = 12.014715
Provides: perl(DBD::Proxy) = 0.2004
Provides: perl(DBD::Sponge) = 12.010003
Provides: perl(DBI::Const::GetInfo::ANSI) = 2.008697
Provides: perl(DBI::Const::GetInfo::ODBC) = 2.011374
Provides: perl(DBI::Const::GetInfoReturn) = 2.008697
Provides: perl(DBI::Const::GetInfoType) = 2.008697
Provides: perl(DBI::DBD) = 12.015129
Provides: perl(DBI::DBD::Metadata) = 2.014214
Provides: perl(DBI::DBD::SqlEngine) = 0.06
Provides: perl(DBI::Gofer::Execute) = 0.014283
Provides: perl(DBI::Gofer::Request) = 0.012537
Provides: perl(DBI::Gofer::Response) = 0.011566
Provides: perl(DBI::Gofer::Serializer::Base) = 0.009950
Provides: perl(DBI::Gofer::Serializer::DataDumper) = 0.009950
Provides: perl(DBI::Gofer::Serializer::Storable) = 0.015586
Provides: perl(DBI::Gofer::Transport::Base) = 0.012537
Provides: perl(DBI::Gofer::Transport::pipeone) = 0.012537
Provides: perl(DBI::Gofer::Transport::stream) = 0.012537
Provides: perl(DBI::Profile) = 2.015065
Provides: perl(DBI::ProfileData) = 2.010008
Provides: perl(DBI::ProfileDumper) = 2.015325
Provides: perl(DBI::ProfileDumper::Apache) = 2.014121
Provides: perl(DBI::ProfileSubs) = 0.009396
Provides: perl(DBI::ProxyServer) = 0.3005
Provides: perl(DBI::SQL::Nano) = 1.015544
Provides: perl(DBI::Util::CacheMemory) = 0.010315
Provides: perl(DBI::Util::_accessor) = 0.009479

Requires: perl(:MODULE_COMPAT_%{perl_version})

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.48
BuildRequires: perl(Test::Simple) >= 0.9
BuildRequires: make
BuildRequires: gcc


%description 
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.


%prep
%setup -q -n DBI-%{version} 
chmod 644 ex/*
mkdir ../32bit
mv * ../32bit
mv ../32bit .
mkdir 64bit
cp -r 32bit/* 64bit/


%build
export CC=gcc
export AR="/usr/bin/ar"

env | sort

$CC --version

cd 32bit
%perl32 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake

cd ../64bit
%perl64 Makefile.PL INSTALLDIRS="vendor" NO_PACKLIST=1 verbose optimize="-O3"
gmake


%check
%if %{with dotests}
cd 32bit
gmake -k test TEST_VERBOSE=1
cd ../64bit
gmake -k test TEST_VERBOSE=1
%endif


%install
export AR="/usr/bin/ar"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 32bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3

cd ../64bit
gmake pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT} INSTALLVENDORMAN1DIR=%{_mandir}/man1 INSTALLVENDORMAN3DIR=%{_mandir}/man3
%{_fixperms} $RPM_BUILD_ROOT/*

# Remove Win32 specific files and man pages to avoid unwanted dependencies
rm -rf ${RPM_BUILD_ROOT}%{perl_vendorarch32}/Win32
rm -rf ${RPM_BUILD_ROOT}%{perl_vendorarch32}/DBI/W32ODBC.pm
rm -rf ${RPM_BUILD_ROOT}%{perl_vendorarch64}/Win32
rm -rf ${RPM_BUILD_ROOT}%{perl_vendorarch64}/DBI/W32ODBC.pm
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man3/DBI::W32ODBC.3

$AR -X64 qc ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.a ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.so
$AR -X32 qc ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.a ${RPM_BUILD_ROOT}%{perl_vendorarch32}/auto/DBI/DBI.so
cp         ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.a ${RPM_BUILD_ROOT}%{perl_vendorarch32}/auto/DBI/DBI.a

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +

dump -X32 -ov ${RPM_BUILD_ROOT}%{perl_vendorarch32}/auto/DBI/DBI.so | grep LOADONLY
dump -X64 -ov ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.so | grep LOADONLY


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/README* 32bit/ex/
%{_bindir}/dbilogstrip
%{_bindir}/dbiprof
%{_bindir}/dbiproxy
%{perl_vendorarch32}/* 
%{perl_vendorarch64}/*
%{_mandir}/man1/*.1
%{_mandir}/man3/*.3


%changelog
* Fri Jun 07 2019 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.642-1
- Port to AIX
- Updated to version 1.642

* Mon Dec 08 2014 Michael Perzl <michael@perzl.org> - 1.632-1
- updated to version 1.632

* Thu Feb 21 2013 Michael Perzl <michael@perzl.org> - 1.623-1
- updated to version 1.623

* Mon Jun 25 2012 Michael Perzl <michael@perzl.org> - 1.622-1
- updated to version 1.622

* Wed Oct 15 2008 Michael Perzl <michael@perzl.org> - 1.607-1
- first version for AIX V5.1 and higher
