# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define meta_name DBI
%define desc DBI is a database access Application Programming Interface (API) for\
the Perl Language. The DBI API Specification defines a set of\
functions, variables and conventions that provide a consistent\
database interface independent of the actual database being used.
# DBI provides various version for different provides.
# We do not take this into account.
%define provide_list DBI Bundle::DBI DBD::DBM DBD::ExampleP DBD::File \
DBD::Gofer DBD::Gofer::Policy::Base DBD::Gofer::Policy::classic DBD::Gofer::Policy::pedantic DBD::Gofer::Policy::rush \
DBD::Gofer::Transport::Base DBD::Gofer::Transport::corostream DBD::Gofer::Transport::null DBD::Gofer::Transport::pipeone DBD::Gofer::Transport::stream \
DBD::Mem DBD::NullP DBD::Proxy DBD::Sponge \
DBI::Const::GetInfo::ANSI DBI::Const::GetInfo::ODBC DBI::Const::GetInfoReturn DBI::Const::GetInfoType \
DBI::DBD DBI::DBD::Metadata DBI::DBD::SqlEngine \
DBI::Gofer::Execute DBI::Gofer::Request DBI::Gofer::Response DBI::Gofer::Serializer::Base DBI::Gofer::Serializer::DataDumper \
DBI::Gofer::Serializer::Storable DBI::Gofer::Transport::Base DBI::Gofer::Transport::pipeone DBI::Gofer::Transport::stream \
DBI::Profile DBI::ProfileData DBI::ProfileDumper DBI::ProfileDumper::Apache DBI::ProfileSubs \
DBI::ProxyServer DBI::SQL::Nano DBI::Util::CacheMemory DBI::Util::_accessor
#%%define require_list # No require

Name:           perl-%{meta_name}
Version:        1.643
Release: 2
Epoch:          1
Summary:        A database access API for perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
Source0:        http://www.cpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
Source1000: %{name}-%{version}-%{release}.build.log

%perl_meta_provides
%perl_meta_requires

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.48
BuildRequires: perl(Test::Simple) >= 0.9
BuildRequires: make
BuildRequires: gcc

Obsoletes: perl-5.32-DBI, perl-5.30-DBI

%description 
%desc

%perl_module
%perl_module_desc

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
export AR=/usr/bin/ar

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
cp          ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.a ${RPM_BUILD_ROOT}%{perl_vendorarch32}/auto/DBI/DBI.a

find $RPM_BUILD_ROOT%{perl_vendorarch32} -name "*.so" -exec strip -X32 -e {} +
find $RPM_BUILD_ROOT%{perl_vendorarch64} -name "*.so" -exec strip -X64 -e {} +

dump -X32 -ov ${RPM_BUILD_ROOT}%{perl_vendorarch32}/auto/DBI/DBI.so | grep LOADONLY
dump -X64 -ov ${RPM_BUILD_ROOT}%{perl_vendorarch64}/auto/DBI/DBI.so | grep LOADONLY

(
  cd $RPM_BUILD_ROOT%{_bindir}
  # Deal with binaries for parallel installation
  for bin in dbilogstrip dbiprof dbiproxy
  do
      mv ${bin} ${bin}%{perl_version}
      ln -s ${bin}%{perl_version} ${bin}
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%{_bindir}/dbilogstrip
%{_bindir}/dbiprof
%{_bindir}/dbiproxy

%files -n %module_name
%defattr(-,root,system,-)
%doc 32bit/README* 32bit/ex/
%{_bindir}/dbilogstrip%{perl_version}
%{_bindir}/dbiprof%{perl_version}
%{_bindir}/dbiproxy%{perl_version}
%{perl_vendorarch32}/* 
%{perl_vendorarch64}/*
#%%{_mandir}/man1/*.1
#%%{_mandir}/man3/*.3


%changelog
* Tue Oct 19 2021 Étienne Guesnet <etienne.guesnet@atos.net> - 1.643-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Tue Jul 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.643-1
- Updated to version 1.643
- Perl version used is 5.32.0


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
