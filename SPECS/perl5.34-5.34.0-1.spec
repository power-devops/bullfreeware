#By default, 64bit mode
%define default_bits 64

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64     %{_prefix}/lib64

%define major_version 5
%define minor_version 34
%define bugfix_version 0

%define perlver %{major_version}.%{minor_version}

# Site: default location for modules installed by user
%define sitelibpath       %{_datadir}/perl5/%{perlver}/site_perl/
%define sitearchpath32    %{_libdir}/perl5/%{perlver}/site_perl/
%define sitearchpath64    %{_libdir64}/perl5/%{perlver}/site_perl/
# Vendor: default location for modules installed through packages
%define vendorlibpath     %{_datadir}/perl5/%{perlver}/vendor_perl/
%define vendorarchpath32  %{_libdir}/perl5/%{perlver}/vendor_perl/
%define vendorarchpath64  %{_libdir64}/perl5/%{perlver}/vendor_perl/
# privlib and archlib are default location fore Perl core modules
%define privlibpath       %{_datadir}/perl5/%{perlver}/
%define archlibpath32     %{_libdir}/perl5/%{perlver}/
%define archlibpath64     %{_libdir64}/perl5/%{perlver}/

Summary: The Perl programming language.
Name: perl%{perlver}
Version: %{major_version}.%{minor_version}.%{bugfix_version}
Release: 1
License: Artistic
URL: http://www.perl.com
Group: Development/Languages
# Alternativ source: http://www.perl.com/CPAN/src/
Source0: http://www.cpan.org/src/5.0/perl-%{version}.tar.gz
Source10: %{name}-%{version}-%{release}.build.log

BuildRequires: findutils, sed
BuildRequires: gdbm-devel >= 1.18
Requires: gdbm >= 1.18

# Patch0: %{name}-5.32.0-aix.patch
# Better way include by default
#Patch0: %{name}-5.28.0-aixmm.patch

%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%define osplat aix7
%endif
%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%define osplat aix7
%endif

# ----- Perl module provides.
%global perl_compat perl(:MODULE_COMPAT_%{perlver})
Provides: %perl_compat

# Nedded by packages itself
Provides: /opt/freeware/bin/perl%{version}

# --------------------------------
# This provides can be outdated. Last update, perl 5.32.

Provides: perl%{perlver}(Archive::Tar) = 2.36
Provides: perl%{perlver}(Attribute::Handlers) = 1.01
Provides: perl%{perlver}(AutoLoader) = 5.74
Provides: perl%{perlver}(CPAN) = 2.27
Provides: perl%{perlver}(CPAN::Meta) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Requirements) = 2.140
Provides: perl%{perlver}(CPAN::Meta::YAML) = 0.018
Provides: perl%{perlver}(Carp) = 1.50
Provides: perl%{perlver}(Compress::Raw::Bzip2) = 2.093
Provides: perl%{perlver}(Compress::Raw::Zlib) = 2.093
Provides: perl%{perlver}(Config::Perl::V) = 0.32
Provides: perl%{perlver}(Data::Dumper) = 2.174
Provides: perl%{perlver}(Devel::PPPort) = 3.57
Provides: perl%{perlver}(Devel::SelfStubber) = 1.06
Provides: perl%{perlver}(Digest) = 1.17_01
Provides: perl%{perlver}(Digest::MD5) = 2.55_01
Provides: perl%{perlver}(Digest::SHA) = 6.02
Provides: perl%{perlver}(Dumpvalue) = 1.21
Provides: perl%{perlver}(Encode) = 3.06
Provides: perl%{perlver}(Env) = 1.04
Provides: perl%{perlver}(Exporter) = 5.74
Provides: perl%{perlver}(ExtUtils::CBuilder) = 0.280234
Provides: perl%{perlver}(ExtUtils::Constant) = 0.25
Provides: perl%{perlver}(ExtUtils::Install) = 2.14
Provides: perl%{perlver}(ExtUtils::MakeMaker) = 7.44
Provides: perl%{perlver}(ExtUtils::Manifest) = 1.72
Provides: perl%{perlver}(ExtUtils::ParseXS) = 3.40
Provides: perl%{perlver}(File::Fetch) = 0.56
Provides: perl%{perlver}(File::Path) = 2.16
Provides: perl%{perlver}(File::Temp) = 0.2309
Provides: perl%{perlver}(Filter::Simple) = 0.96
Provides: perl%{perlver}(Getopt::Long) = 2.51
Provides: perl%{perlver}(HTTP::Tiny) = 0.076
Provides: perl%{perlver}(I18N::Collate) = 1.02
Provides: perl%{perlver}(IO) = 1.43
Provides: perl%{perlver}(IO::Socket::IP) = 0.39
Provides: perl%{perlver}(IO::Zlib) = 1.10
Provides: perl%{perlver}(IPC::Cmd) = 1.04
Provides: perl%{perlver}(IPC::SysV) = 2.07
Provides: perl%{perlver}(JSON::PP) = 4.04
Provides: perl%{perlver}(Locale::Maketext) = 1.29
Provides: perl%{perlver}(Locale::Maketext::Simple) = 0.21_01
Provides: perl%{perlver}(MIME::Base64) = 3.15
Provides: perl%{perlver}(Math::BigInt) = 1.999818
Provides: perl%{perlver}(Math::BigInt::FastCalc) = 0.5009
Provides: perl%{perlver}(Math::BigRat) = 0.2614
Provides: perl%{perlver}(Math::Complex) = 1.5901
Provides: perl%{perlver}(Memoize) = 1.03_01
Provides: perl%{perlver}(Module::CoreList) = 5.20200620
Provides: perl%{perlver}(Module::Load) = 0.34
Provides: perl%{perlver}(Module::Load::Conditional) = 0.70
Provides: perl%{perlver}(Module::Loaded) = 0.08
Provides: perl%{perlver}(Module::Metadata) = 1.000037
Provides: perl%{perlver}(NEXT) = 0.67_01
Provides: perl%{perlver}(Net::Ping) = 2.72
Provides: perl%{perlver}(Params::Check) = 0.38
Provides: perl%{perlver}(Perl::OSType) = 1.010
Provides: perl%{perlver}(PerlIO::via::QuotedPrint) = 0.08
Provides: perl%{perlver}(Pod::Checker) = 1.73
Provides: perl%{perlver}(Pod::Escapes) = 1.07
# Pod::Parser is no more provided
Provides: perl%{perlver}(Pod::Perldoc) = 3.2801
Provides: perl%{perlver}(Pod::Simple) = 3.40
Provides: perl%{perlver}(Pod::Usage) = 1.69
Provides: perl%{perlver}(Safe) = 2.41
Provides: perl%{perlver}(Search::Dict) = 1.07
Provides: perl%{perlver}(SelfLoader) = 1.26
Provides: perl%{perlver}(Socket) = 2.029
Provides: perl%{perlver}(Storable) = 3.21
Provides: perl%{perlver}(Sys::Syslog) = 0.36
Provides: perl%{perlver}(Term::ANSIColor) = 5.01
Provides: perl%{perlver}(Term::Cap) = 1.17
Provides: perl%{perlver}(Term::Complete) = 1.403
Provides: perl%{perlver}(Term::ReadLine) = 1.17
Provides: perl%{perlver}(Test) = 1.31
Provides: perl%{perlver}(Test::Harness) = 3.42
Provides: perl%{perlver}(Test::Simple) = 1.302175
Provides: perl%{perlver}(Text::Abbrev) = 1.02
Provides: perl%{perlver}(Text::Balanced) = 2.03
Provides: perl%{perlver}(Text::ParseWords) = 3.30
Provides: perl%{perlver}(Thread::Queue) = 3.14
Provides: perl%{perlver}(Thread::Semaphore) = 2.13
Provides: perl%{perlver}(Tie::File) = 1.06
Provides: perl%{perlver}(Tie::RefHash) = 1.39
Provides: perl%{perlver}(Time::HiRes) = 1.9764
Provides: perl%{perlver}(Time::Local) = 1.28
Provides: perl%{perlver}(Time::Piece) = 1.3401
Provides: perl%{perlver}(Unicode::Collate) = 1.27
Provides: perl%{perlver}(Unicode::Normalize) = 1.27
Provides: perl%{perlver}(XSLoader) = 0.30
Provides: perl%{perlver}(autodie) = 2.32
Provides: perl%{perlver}(autouse) = 1.11
Provides: perl%{perlver}(base) = 2.27
Provides: perl%{perlver}(bignum) = 0.51
Provides: perl%{perlver}(constant) = 1.33
Provides: perl%{perlver}(encoding::warnings) = 0.13
Provides: perl%{perlver}(experimental) = 0.020
Provides: perl%{perlver}(if) = 0.0608
Provides: perl%{perlver}(lib) = 0.65
Provides: perl%{perlver}(parent) = 0.238
Provides: perl%{perlver}(perlfaq) = 5.20200523
Provides: perl%{perlver}(threads) = 2.25
Provides: perl%{perlver}(threads::shared) = 1.61
Provides: perl%{perlver}(version) = 0.9924
Provides: perl%{perlver}(AnyDBM_File) = 1.01
Provides: perl%{perlver}(App::Cpan) = 1.675
Provides: perl%{perlver}(App::Prove) = 3.42
Provides: perl%{perlver}(App::Prove::State) = 3.42
Provides: perl%{perlver}(App::Prove::State::Result) = 3.42
Provides: perl%{perlver}(App::Prove::State::Result::Test) = 3.42
Provides: perl%{perlver}(Archive::Tar::Constant) = 2.36
Provides: perl%{perlver}(Archive::Tar::File) = 2.36
Provides: perl%{perlver}(AutoSplit) = 1.06
Provides: perl%{perlver}(B) = 1.80
Provides: perl%{perlver}(B::Concise) = 1.004
Provides: perl%{perlver}(B::Deparse) = 1.54
Provides: perl%{perlver}(B::Op_private) = 5.032000
Provides: perl%{perlver}(B::Showlex) = 1.05
Provides: perl%{perlver}(B::Terse) = 1.09
Provides: perl%{perlver}(B::Xref) = 1.07
Provides: perl%{perlver}(Benchmark) = 1.23
Provides: perl%{perlver}(CPAN::Author) = 5.5002
Provides: perl%{perlver}(CPAN::Bundle) = 5.5005
Provides: perl%{perlver}(CPAN::CacheMgr) = 5.5002
Provides: perl%{perlver}(CPAN::Complete) = 5.5001
Provides: perl%{perlver}(CPAN::Debug) = 5.5001
Provides: perl%{perlver}(CPAN::DeferredCode) = 5.50
Provides: perl%{perlver}(CPAN::Distribution) = 2.27
Provides: perl%{perlver}(CPAN::Distroprefs) = 6.0001
Provides: perl%{perlver}(CPAN::Distrostatus) = 5.5
Provides: perl%{perlver}(CPAN::Exception::RecursiveDependency) = 5.5001
Provides: perl%{perlver}(CPAN::Exception::blocked_urllist) = 1.001
Provides: perl%{perlver}(CPAN::Exception::yaml_not_installed) = 5.5
Provides: perl%{perlver}(CPAN::Exception::yaml_process_error) = 5.5
Provides: perl%{perlver}(CPAN::FTP) = 5.5012
Provides: perl%{perlver}(CPAN::FTP::netrc) = 1.01
Provides: perl%{perlver}(CPAN::FirstTime) = 5.5314
Provides: perl%{perlver}(CPAN::HTTP::Client) = 1.9601
Provides: perl%{perlver}(CPAN::HTTP::Credentials) = 1.9601
Provides: perl%{perlver}(CPAN::HandleConfig) = 5.5011
Provides: perl%{perlver}(CPAN::Index) = 2.12
Provides: perl%{perlver}(CPAN::InfoObj) = 5.5
Provides: perl%{perlver}(CPAN::Kwalify) = 5.50
Provides: perl%{perlver}(CPAN::LWP::UserAgent) = 1.9601
Provides: perl%{perlver}(CPAN::Meta::Converter) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Feature) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::History) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Merge) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Prereqs) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Spec) = 2.150010
Provides: perl%{perlver}(CPAN::Meta::Validator) = 2.150010
Provides: perl%{perlver}(CPAN::Mirrors) = 2.27
Provides: perl%{perlver}(CPAN::Module) = 5.5003
Provides: perl%{perlver}(CPAN::Nox) = 5.5001
Provides: perl%{perlver}(CPAN::Plugin) = 0.97
Provides: perl%{perlver}(CPAN::Plugin::Specfile) = 0.02
Provides: perl%{perlver}(CPAN::Prompt) = 5.5
Provides: perl%{perlver}(CPAN::Queue) = 5.5003
Provides: perl%{perlver}(CPAN::Shell) = 5.5009
Provides: perl%{perlver}(CPAN::Tarzip) = 5.5013
Provides: perl%{perlver}(CPAN::URL) = 5.5
Provides: perl%{perlver}(CPAN::Version) = 5.5003
Provides: perl%{perlver}(Carp::Heavy) = 1.50
Provides: perl%{perlver}(Class::Struct) = 0.66
Provides: perl%{perlver}(Compress::Zlib) = 2.093
Provides: perl%{perlver}(Config::Extensions) = 0.03
Provides: perl%{perlver}(Cwd) = 3.78
Provides: perl%{perlver}(DBM_Filter) = 0.06
Provides: perl%{perlver}(DBM_Filter::compress) = 0.03
Provides: perl%{perlver}(DBM_Filter::encode) = 0.03
Provides: perl%{perlver}(DBM_Filter::int32) = 0.03
Provides: perl%{perlver}(DBM_Filter::null) = 0.03
Provides: perl%{perlver}(DBM_Filter::utf8) = 0.03
Provides: perl%{perlver}(Devel::Peek) = 1.28
Provides: perl%{perlver}(Devel::Symdump::Export) = 2.18
Provides: perl%{perlver}(Digest::base) = 1.16
Provides: perl%{perlver}(Digest::file) = 1.16
Provides: perl%{perlver}(DirHandle) = 1.05
Provides: perl%{perlver}(DynaLoader) = 1.47
Provides: perl%{perlver}(Encode::Alias) = 2.24
Provides: perl%{perlver}(Encode::Byte) = 2.04
Provides: perl%{perlver}(Encode::CJKConstants) = 2.02
Provides: perl%{perlver}(Encode::CN) = 2.03
Provides: perl%{perlver}(Encode::CN::HZ) = 2.10
Provides: perl%{perlver}(Encode::Config) = 2.05
Provides: perl%{perlver}(Encode::EBCDIC) = 2.02
Provides: perl%{perlver}(Encode::Encoder) = 2.03
Provides: perl%{perlver}(Encode::Encoding) = 2.08
Provides: perl%{perlver}(Encode::GSM0338) = 2.07
Provides: perl%{perlver}(Encode::Guess) = 2.08
Provides: perl%{perlver}(Encode::JP) = 2.04
Provides: perl%{perlver}(Encode::JP::H2Z) = 2.02
Provides: perl%{perlver}(Encode::JP::JIS7) = 2.08
Provides: perl%{perlver}(Encode::KR) = 2.03
Provides: perl%{perlver}(Encode::KR::2022_KR) = 2.04
Provides: perl%{perlver}(Encode::MIME::Header) = 2.28
Provides: perl%{perlver}(Encode::MIME::Header::ISO_2022_JP) = 1.09
Provides: perl%{perlver}(Encode::MIME::Name) = 1.03
Provides: perl%{perlver}(Encode::Symbol) = 2.02
Provides: perl%{perlver}(Encode::TW) = 2.03
Provides: perl%{perlver}(Encode::Unicode) = 2.18
Provides: perl%{perlver}(Encode::Unicode::UTF7) = 2.10
Provides: perl%{perlver}(English) = 1.11
Provides: perl%{perlver}(Exporter::Heavy) = 5.74
Provides: perl%{perlver}(ExtUtils::CBuilder::Base) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::Unix) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::VMS) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::Windows) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::Windows::BCC) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::Windows::GCC) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::Windows::MSVC) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::aix) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::android) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::cygwin) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::darwin) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::dec_osf) = 0.280234
Provides: perl%{perlver}(ExtUtils::CBuilder::Platform::os2) = 0.280234
Provides: perl%{perlver}(ExtUtils::Command) = 7.44
Provides: perl%{perlver}(ExtUtils::Command::MM) = 7.44
Provides: perl%{perlver}(ExtUtils::Constant::Base) = 0.06
Provides: perl%{perlver}(ExtUtils::Constant::ProxySubs) = 0.09
Provides: perl%{perlver}(ExtUtils::Constant::Utils) = 0.04
Provides: perl%{perlver}(ExtUtils::Constant::XS) = 0.03
Provides: perl%{perlver}(ExtUtils::Embed) = 1.35
Provides: perl%{perlver}(ExtUtils::Installed) = 2.14
Provides: perl%{perlver}(ExtUtils::Liblist) = 7.44
Provides: perl%{perlver}(ExtUtils::Liblist::Kid) = 7.44
Provides: perl%{perlver}(ExtUtils::MM) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_AIX) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Any) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_BeOS) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Cygwin) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_DOS) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Darwin) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_MacOS) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_NW5) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_OS2) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_QNX) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_UWIN) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Unix) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_VMS) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_VOS) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Win32) = 7.44
Provides: perl%{perlver}(ExtUtils::MM_Win95) = 7.44
Provides: perl%{perlver}(ExtUtils::MY) = 7.44
Provides: perl%{perlver}(ExtUtils::MakeMaker::Config) = 7.44
Provides: perl%{perlver}(ExtUtils::MakeMaker::Locale) = 7.44
Provides: perl%{perlver}(ExtUtils::MakeMaker::version) = 7.44
Provides: perl%{perlver}(ExtUtils::Miniperl) = 1.09
Provides: perl%{perlver}(ExtUtils::Mkbootstrap) = 7.44
Provides: perl%{perlver}(ExtUtils::Mksymlists) = 7.44
Provides: perl%{perlver}(ExtUtils::Packlist) = 2.14
Provides: perl%{perlver}(ExtUtils::ParseXS::Constants) = 3.40
Provides: perl%{perlver}(ExtUtils::ParseXS::CountLines) = 3.40
Provides: perl%{perlver}(ExtUtils::ParseXS::Eval) = 3.40
Provides: perl%{perlver}(ExtUtils::ParseXS::Utilities) = 3.40
Provides: perl%{perlver}(ExtUtils::Typemaps) = 3.38
Provides: perl%{perlver}(ExtUtils::Typemaps::Cmd) = 3.38
Provides: perl%{perlver}(ExtUtils::Typemaps::InputMap) = 3.38
Provides: perl%{perlver}(ExtUtils::Typemaps::OutputMap) = 3.38
Provides: perl%{perlver}(ExtUtils::Typemaps::Type) = 3.38
Provides: perl%{perlver}(ExtUtils::testlib) = 7.44
Provides: perl%{perlver}(Fatal) = 2.32
Provides: perl%{perlver}(Fcntl) = 1.13
Provides: perl%{perlver}(File::Basename) = 2.85
Provides: perl%{perlver}(File::Compare) = 1.1006
Provides: perl%{perlver}(File::Copy) = 2.34
Provides: perl%{perlver}(File::DosGlob) = 1.12
Provides: perl%{perlver}(File::Find) = 1.37
Provides: perl%{perlver}(File::Glob) = 1.33
Provides: perl%{perlver}(File::GlobMapper) = 1.001
Provides: perl%{perlver}(File::Spec) = 3.78
Provides: perl%{perlver}(File::Spec::AmigaOS) = 3.78
Provides: perl%{perlver}(File::Spec::Cygwin) = 3.78
Provides: perl%{perlver}(File::Spec::Epoc) = 3.78
Provides: perl%{perlver}(File::Spec::Functions) = 3.78
Provides: perl%{perlver}(File::Spec::Mac) = 3.78
Provides: perl%{perlver}(File::Spec::OS2) = 3.78
Provides: perl%{perlver}(File::Spec::Unix) = 3.78
Provides: perl%{perlver}(File::Spec::VMS) = 3.78
Provides: perl%{perlver}(File::Spec::Win32) = 3.79
Provides: perl%{perlver}(File::stat) = 1.09
Provides: perl%{perlver}(FileCache) = 1.10
Provides: perl%{perlver}(FileHandle) = 2.03
Provides: perl%{perlver}(Filter::Util::Call) = 1.59
Provides: perl%{perlver}(FindBin) = 1.51
Provides: perl%{perlver}(GDBM_File) = 1.18
Provides: perl%{perlver}(Getopt::Std) = 1.12
Provides: perl%{perlver}(Hash::Util) = 0.23
Provides: perl%{perlver}(Hash::Util::FieldHash) = 1.20
Provides: perl%{perlver}(I18N::LangTags) = 0.44
Provides: perl%{perlver}(I18N::LangTags::Detect) = 1.08
Provides: perl%{perlver}(I18N::LangTags::List) = 0.40
Provides: perl%{perlver}(I18N::Langinfo) = 0.19
Provides: perl%{perlver}(IO::Compress::Adapter::Bzip2) = 2.093
Provides: perl%{perlver}(IO::Compress::Adapter::Deflate) = 2.093
Provides: perl%{perlver}(IO::Compress::Adapter::Identity) = 2.093
Provides: perl%{perlver}(IO::Compress::Base) = 2.093
Provides: perl%{perlver}(IO::Compress::Base::Common) = 2.093
Provides: perl%{perlver}(IO::Compress::Bzip2) = 2.093
Provides: perl%{perlver}(IO::Compress::Deflate) = 2.093
Provides: perl%{perlver}(IO::Compress::Gzip) = 2.093
Provides: perl%{perlver}(IO::Compress::Gzip::Constants) = 2.093
Provides: perl%{perlver}(IO::Compress::RawDeflate) = 2.093
Provides: perl%{perlver}(IO::Compress::Zip) = 2.093
Provides: perl%{perlver}(IO::Compress::Zip::Constants) = 2.093
Provides: perl%{perlver}(IO::Compress::Zlib::Constants) = 2.093
Provides: perl%{perlver}(IO::Compress::Zlib::Extra) = 2.093
Provides: perl%{perlver}(IO::Dir) = 1.41
Provides: perl%{perlver}(IO::File) = 1.41
Provides: perl%{perlver}(IO::Handle) = 1.42
Provides: perl%{perlver}(IO::Pipe) = 1.41
Provides: perl%{perlver}(IO::Poll) = 1.41
Provides: perl%{perlver}(IO::Seekable) = 1.41
Provides: perl%{perlver}(IO::Select) = 1.42
Provides: perl%{perlver}(IO::Socket) = 1.43
Provides: perl%{perlver}(IO::Socket::INET) = 1.41
Provides: perl%{perlver}(IO::Socket::UNIX) = 1.41
Provides: perl%{perlver}(IO::Uncompress::Adapter::Bunzip2) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Adapter::Identity) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Adapter::Inflate) = 2.093
Provides: perl%{perlver}(IO::Uncompress::AnyInflate) = 2.093
Provides: perl%{perlver}(IO::Uncompress::AnyUncompress) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Base) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Bunzip2) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Gunzip) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Inflate) = 2.093
Provides: perl%{perlver}(IO::Uncompress::RawInflate) = 2.093
Provides: perl%{perlver}(IO::Uncompress::Unzip) = 2.093
Provides: perl%{perlver}(IPC::Msg) = 2.07
Provides: perl%{perlver}(IPC::Open2) = 1.05
Provides: perl%{perlver}(IPC::Open3) = 1.21
Provides: perl%{perlver}(IPC::Semaphore) = 2.07
Provides: perl%{perlver}(IPC::SharedMem) = 2.07
Provides: perl%{perlver}(JSON::PP::Boolean) = 4.04
Provides: perl%{perlver}(List::Util) = 1.55
Provides: perl%{perlver}(List::Util::XS) = 1.55
Provides: perl%{perlver}(Locale::Maketext::Guts) = 1.20
Provides: perl%{perlver}(Locale::Maketext::GutsLoader) = 1.20
Provides: perl%{perlver}(MIME::QuotedPrint) = 3.13
Provides: perl%{perlver}(Math::BigFloat) = 1.999818
Provides: perl%{perlver}(Math::BigFloat::Trace) = 0.51
Provides: perl%{perlver}(Math::BigInt::Calc) = 1.999818
Provides: perl%{perlver}(Math::BigInt::Lib) = 1.999818
Provides: perl%{perlver}(Math::BigInt::Trace) = 0.51
Provides: perl%{perlver}(Math::Trig) = 1.23
Provides: perl%{perlver}(Memoize::AnyDBM_File) = 1.03
Provides: perl%{perlver}(Memoize::Expire) = 1.03
Provides: perl%{perlver}(Memoize::ExpireFile) = 1.03
Provides: perl%{perlver}(Memoize::ExpireTest) = 1.03
Provides: perl%{perlver}(Memoize::NDBM_File) = 1.03
Provides: perl%{perlver}(Memoize::SDBM_File) = 1.03
Provides: perl%{perlver}(Memoize::Storable) = 1.03
Provides: perl%{perlver}(Module::CoreList::Utils) = 5.20200620
Provides: perl%{perlver}(NDBM_File) = 1.15
Provides: perl%{perlver}(Net::Cmd) = 3.11
Provides: perl%{perlver}(Net::Config) = 3.11
Provides: perl%{perlver}(Net::Domain) = 3.11
Provides: perl%{perlver}(Net::FTP) = 3.11
Provides: perl%{perlver}(Net::FTP::A) = 3.11
Provides: perl%{perlver}(Net::FTP::E) = 3.11
Provides: perl%{perlver}(Net::FTP::I) = 3.11
Provides: perl%{perlver}(Net::FTP::L) = 3.11
Provides: perl%{perlver}(Net::FTP::dataconn) = 3.11
Provides: perl%{perlver}(Net::NNTP) = 3.11
Provides: perl%{perlver}(Net::Netrc) = 3.11
Provides: perl%{perlver}(Net::POP3) = 3.11
Provides: perl%{perlver}(Net::SMTP) = 3.11
Provides: perl%{perlver}(Net::Time) = 3.11
Provides: perl%{perlver}(Net::hostent) = 1.02
Provides: perl%{perlver}(Net::netent) = 1.01
Provides: perl%{perlver}(Net::protoent) = 1.01
Provides: perl%{perlver}(Net::servent) = 1.02
Provides: perl%{perlver}(O) = 1.03
Provides: perl%{perlver}(ODBM_File) = 1.16
Provides: perl%{perlver}(Opcode) = 1.47
Provides: perl%{perlver}(POSIX) = 1.94
Provides: perl%{perlver}(Parse::CPAN::Meta) = 2.150010
Provides: perl%{perlver}(PerlIO) = 1.11
Provides: perl%{perlver}(PerlIO::encoding) = 0.28
Provides: perl%{perlver}(PerlIO::mmap) = 0.016
Provides: perl%{perlver}(PerlIO::scalar) = 0.30
Provides: perl%{perlver}(PerlIO::via) = 0.18
# Pod::Find is no more provided
Provides: perl%{perlver}(Pod::Html) = 1.25
# Pod::InputObjects is no more provided
Provides: perl%{perlver}(Pod::Man) = 4.14
Provides: perl%{perlver}(Pod::ParseLink) = 4.14
# Pod::ParseUtils is no more provided
Provides: perl%{perlver}(Pod::Perldoc::BaseTo) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::GetOptsOO) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToANSI) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToChecker) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToMan) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToNroff) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToPod) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToRtf) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToTerm) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToText) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToTk) = 3.28
Provides: perl%{perlver}(Pod::Perldoc::ToXml) = 3.28
# Pod::PlainText is no more provided
# Pod::Select is no more provided
Provides: perl%{perlver}(Pod::Simple::BlackBox) = 3.40
Provides: perl%{perlver}(Pod::Simple::Checker) = 3.40
Provides: perl%{perlver}(Pod::Simple::Debug) = 3.40
Provides: perl%{perlver}(Pod::Simple::DumpAsText) = 3.40
Provides: perl%{perlver}(Pod::Simple::DumpAsXML) = 3.40
Provides: perl%{perlver}(Pod::Simple::HTML) = 3.40
Provides: perl%{perlver}(Pod::Simple::HTMLBatch) = 3.40
Provides: perl%{perlver}(Pod::Simple::HTMLLegacy) = 5.01
Provides: perl%{perlver}(Pod::Simple::JustPod) = 3.40
Provides: perl%{perlver}(Pod::Simple::LinkSection) = 3.40
Provides: perl%{perlver}(Pod::Simple::Methody) = 3.40
Provides: perl%{perlver}(Pod::Simple::Progress) = 3.40
Provides: perl%{perlver}(Pod::Simple::PullParser) = 3.40
Provides: perl%{perlver}(Pod::Simple::PullParserEndToken) = 3.40
Provides: perl%{perlver}(Pod::Simple::PullParserStartToken) = 3.40
Provides: perl%{perlver}(Pod::Simple::PullParserTextToken) = 3.40
Provides: perl%{perlver}(Pod::Simple::PullParserToken) = 3.40
Provides: perl%{perlver}(Pod::Simple::RTF) = 3.40
Provides: perl%{perlver}(Pod::Simple::Search) = 3.40
Provides: perl%{perlver}(Pod::Simple::SimpleTree) = 3.40
Provides: perl%{perlver}(Pod::Simple::Text) = 3.40
Provides: perl%{perlver}(Pod::Simple::TextContent) = 3.40
Provides: perl%{perlver}(Pod::Simple::TiedOutFH) = 3.40
Provides: perl%{perlver}(Pod::Simple::Transcode) = 3.40
Provides: perl%{perlver}(Pod::Simple::TranscodeDumb) = 3.40
Provides: perl%{perlver}(Pod::Simple::TranscodeSmart) = 3.40
Provides: perl%{perlver}(Pod::Simple::XHTML) = 3.40
Provides: perl%{perlver}(Pod::Simple::XMLOutStream) = 3.40
Provides: perl%{perlver}(Pod::Text) = 4.14
Provides: perl%{perlver}(Pod::Text::Color) = 4.14
Provides: perl%{perlver}(Pod::Text::Overstrike) = 4.14
Provides: perl%{perlver}(Pod::Text::Termcap) = 4.14
Provides: perl%{perlver}(SDBM_File) = 1.15
Provides: perl%{perlver}(Scalar::Util) = 1.55
Provides: perl%{perlver}(SelectSaver) = 1.02
Provides: perl%{perlver}(Sub::Util) = 1.55
Provides: perl%{perlver}(Symbol) = 1.08
Provides: perl%{perlver}(Sys::Hostname) = 1.23
Provides: perl%{perlver}(TAP::Base) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Base) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Color) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Console) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Console::ParallelSession) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Console::Session) = 3.42
Provides: perl%{perlver}(TAP::Formatter::File) = 3.42
Provides: perl%{perlver}(TAP::Formatter::File::Session) = 3.42
Provides: perl%{perlver}(TAP::Formatter::Session) = 3.42
Provides: perl%{perlver}(TAP::Harness) = 3.42
Provides: perl%{perlver}(TAP::Harness::Env) = 3.42
Provides: perl%{perlver}(TAP::Object) = 3.42
Provides: perl%{perlver}(TAP::Parser) = 3.42
Provides: perl%{perlver}(TAP::Parser::Aggregator) = 3.42
Provides: perl%{perlver}(TAP::Parser::Grammar) = 3.42
Provides: perl%{perlver}(TAP::Parser::Iterator) = 3.42
Provides: perl%{perlver}(TAP::Parser::Iterator::Array) = 3.42
Provides: perl%{perlver}(TAP::Parser::Iterator::Process) = 3.42
Provides: perl%{perlver}(TAP::Parser::Iterator::Stream) = 3.42
Provides: perl%{perlver}(TAP::Parser::IteratorFactory) = 3.42
Provides: perl%{perlver}(TAP::Parser::Multiplexer) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Bailout) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Comment) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Plan) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Pragma) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Test) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Unknown) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::Version) = 3.42
Provides: perl%{perlver}(TAP::Parser::Result::YAML) = 3.42
Provides: perl%{perlver}(TAP::Parser::ResultFactory) = 3.42
Provides: perl%{perlver}(TAP::Parser::Scheduler) = 3.42
Provides: perl%{perlver}(TAP::Parser::Scheduler::Job) = 3.42
Provides: perl%{perlver}(TAP::Parser::Scheduler::Spinner) = 3.42
Provides: perl%{perlver}(TAP::Parser::Source) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler::Executable) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler::File) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler::Handle) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler::Perl) = 3.42
Provides: perl%{perlver}(TAP::Parser::SourceHandler::RawTAP) = 3.42
Provides: perl%{perlver}(TAP::Parser::YAMLish::Reader) = 3.42
Provides: perl%{perlver}(TAP::Parser::YAMLish::Writer) = 3.42
Provides: perl%{perlver}(Test2) = 1.302175
Provides: perl%{perlver}(Test2::API) = 1.302175
Provides: perl%{perlver}(Test2::API::Breakage) = 1.302175
Provides: perl%{perlver}(Test2::API::Context) = 1.302175
Provides: perl%{perlver}(Test2::API::Instance) = 1.302175
Provides: perl%{perlver}(Test2::API::Stack) = 1.302175
Provides: perl%{perlver}(Test2::Event) = 1.302175
Provides: perl%{perlver}(Test2::Event::Bail) = 1.302175
Provides: perl%{perlver}(Test2::Event::Diag) = 1.302175
Provides: perl%{perlver}(Test2::Event::Encoding) = 1.302175
Provides: perl%{perlver}(Test2::Event::Exception) = 1.302175
Provides: perl%{perlver}(Test2::Event::Fail) = 1.302175
Provides: perl%{perlver}(Test2::Event::Generic) = 1.302175
Provides: perl%{perlver}(Test2::Event::Note) = 1.302175
Provides: perl%{perlver}(Test2::Event::Ok) = 1.302175
Provides: perl%{perlver}(Test2::Event::Pass) = 1.302175
Provides: perl%{perlver}(Test2::Event::Plan) = 1.302175
Provides: perl%{perlver}(Test2::Event::Skip) = 1.302175
Provides: perl%{perlver}(Test2::Event::Subtest) = 1.302175
Provides: perl%{perlver}(Test2::Event::TAP::Version) = 1.302175
Provides: perl%{perlver}(Test2::Event::V2) = 1.302175
Provides: perl%{perlver}(Test2::Event::Waiting) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::About) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Amnesty) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Assert) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Control) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Error) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Hub) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Info) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Info::Table) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Meta) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Parent) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Plan) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Render) = 1.302175
Provides: perl%{perlver}(Test2::EventFacet::Trace) = 1.302175
Provides: perl%{perlver}(Test2::Formatter) = 1.302175
Provides: perl%{perlver}(Test2::Formatter::TAP) = 1.302175
Provides: perl%{perlver}(Test2::Hub) = 1.302175
Provides: perl%{perlver}(Test2::Hub::Interceptor) = 1.302175
Provides: perl%{perlver}(Test2::Hub::Interceptor::Terminator) = 1.302175
Provides: perl%{perlver}(Test2::Hub::Subtest) = 1.302175
Provides: perl%{perlver}(Test2::IPC) = 1.302175
Provides: perl%{perlver}(Test2::IPC::Driver) = 1.302175
Provides: perl%{perlver}(Test2::IPC::Driver::Files) = 1.302175
Provides: perl%{perlver}(Test2::Tools::Tiny) = 1.302175
Provides: perl%{perlver}(Test2::Util) = 1.302175
Provides: perl%{perlver}(Test2::Util::ExternalMeta) = 1.302175
Provides: perl%{perlver}(Test2::Util::Facets2Legacy) = 1.302175
Provides: perl%{perlver}(Test2::Util::HashBase) = 1.302175
Provides: perl%{perlver}(Test2::Util::Trace) = 1.302175
Provides: perl%{perlver}(Test::Builder) = 1.302175
Provides: perl%{perlver}(Test::Builder::Formatter) = 1.302175
Provides: perl%{perlver}(Test::Builder::IO::Scalar) = 2.114
Provides: perl%{perlver}(Test::Builder::Module) = 1.302175
Provides: perl%{perlver}(Test::Builder::Tester) = 1.302175
Provides: perl%{perlver}(Test::Builder::Tester::Color) = 1.302175
Provides: perl%{perlver}(Test::Builder::TodoDiag) = 1.302175
Provides: perl%{perlver}(Test::More) = 1.302175
Provides: perl%{perlver}(Test::Tester) = 1.302175
Provides: perl%{perlver}(Test::Tester::Capture) = 1.302175
Provides: perl%{perlver}(Test::Tester::CaptureRunner) = 1.302175
Provides: perl%{perlver}(Test::Tester::Delegate) = 1.302175
Provides: perl%{perlver}(Test::use::ok) = 1.302175
Provides: perl%{perlver}(Text::Tabs) = 2013.0523
Provides: perl%{perlver}(Text::Wrap) = 2013.0523
Provides: perl%{perlver}(Thread) = 3.05
Provides: perl%{perlver}(Tie::Array) = 1.07
Provides: perl%{perlver}(Tie::Handle) = 4.2
Provides: perl%{perlver}(Tie::Hash) = 1.05
Provides: perl%{perlver}(Tie::Hash::NamedCapture) = 0.13
Provides: perl%{perlver}(Tie::Memoize) = 1.1
Provides: perl%{perlver}(Tie::Scalar) = 1.05
Provides: perl%{perlver}(Tie::StdHandle) = 4.6
Provides: perl%{perlver}(Tie::SubstrHash) = 1.00
Provides: perl%{perlver}(Time::Seconds) = 1.3401
Provides: perl%{perlver}(Time::gmtime) = 1.04
Provides: perl%{perlver}(Time::localtime) = 1.03
Provides: perl%{perlver}(Time::tm) = 1.00
Provides: perl%{perlver}(UNIVERSAL) = 1.13
Provides: perl%{perlver}(Unicode::Collate::CJK::Big5) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::GB2312) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::JISX0208) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::Korean) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::Pinyin) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::Stroke) = 1.27
Provides: perl%{perlver}(Unicode::Collate::CJK::Zhuyin) = 1.27
Provides: perl%{perlver}(Unicode::Collate::Locale) = 1.27
Provides: perl%{perlver}(Unicode::UCD) = 0.75
Provides: perl%{perlver}(User::grent) = 1.03
Provides: perl%{perlver}(User::pwent) = 1.01
Provides: perl%{perlver}(attributes) = 0.33
Provides: perl%{perlver}(autodie::Scope::Guard) = 2.32
Provides: perl%{perlver}(autodie::Scope::GuardStack) = 2.32
Provides: perl%{perlver}(autodie::Util) = 2.32
Provides: perl%{perlver}(autodie::exception) = 2.32
Provides: perl%{perlver}(autodie::exception::system) = 2.32
Provides: perl%{perlver}(autodie::hints) = 2.32
Provides: perl%{perlver}(autodie::skip) = 2.32
Provides: perl%{perlver}(bigint) = 0.51
Provides: perl%{perlver}(bigrat) = 0.51
Provides: perl%{perlver}(blib) = 1.07
Provides: perl%{perlver}(bytes) = 1.07
Provides: perl%{perlver}(charnames) = 1.48
Provides: perl%{perlver}(deprecate) = 0.04
Provides: perl%{perlver}(diagnostics) = 1.37
Provides: perl%{perlver}(encoding) = 3.00
Provides: perl%{perlver}(feature) = 1.58
Provides: perl%{perlver}(fields) = 2.24
Provides: perl%{perlver}(filetest) = 1.03
Provides: perl%{perlver}(integer) = 1.01
Provides: perl%{perlver}(less) = 0.03
Provides: perl%{perlver}(locale) = 1.09
Provides: perl%{perlver}(mro) = 1.23
Provides: perl%{perlver}(ok) = 1.302175
Provides: perl%{perlver}(open) = 1.12
Provides: perl%{perlver}(ops) = 1.02
Provides: perl%{perlver}(overload) = 1.31
Provides: perl%{perlver}(overload::numbers)
Provides: perl%{perlver}(overloading) = 0.02
Provides: perl%{perlver}(re) = 0.40
Provides: perl%{perlver}(sigtrap) = 1.09
Provides: perl%{perlver}(sort) = 2.04
Provides: perl%{perlver}(strict) = 1.11
Provides: perl%{perlver}(subs) = 1.03
Provides: perl%{perlver}(utf8) = 1.22
Provides: perl%{perlver}(vars) = 1.05
Provides: perl%{perlver}(version::regex) = 0.9924
Provides: perl%{perlver}(vmsish) = 1.04
Provides: perl%{perlver}(warnings) = 1.47
Provides: perl%{perlver}(warnings::register) = 1.04

# Provides for non *.pm files
Provides: perl%{perlver}(abbrev.pl) 
Provides: perl%{perlver}(assert.pl) 
Provides: perl%{perlver}(bigfloat.pl) 
Provides: perl%{perlver}(bigint.pl) 
Provides: perl%{perlver}(bigrat.pl) 
Provides: perl%{perlver}(bytes_heavy.pl) 
Provides: perl%{perlver}(cacheout.pl) 
Provides: perl%{perlver}(complete.pl) 
Provides: perl%{perlver}(ctime.pl) 
Provides: perl%{perlver}(dotsh.pl) 
Provides: perl%{perlver}(dumpvar.pl) 
Provides: perl%{perlver}(exceptions.pl) 
Provides: perl%{perlver}(fastcwd.pl) 
Provides: perl%{perlver}(find.pl) 
Provides: perl%{perlver}(finddepth.pl) 
Provides: perl%{perlver}(flush.pl) 
Provides: perl%{perlver}(ftp.pl) 
Provides: perl%{perlver}(getcwd.pl) 
Provides: perl%{perlver}(getopt.pl) 
Provides: perl%{perlver}(getopts.pl) 
Provides: perl%{perlver}(hostname.pl) 
Provides: perl%{perlver}(importenv.pl) 
Provides: perl%{perlver}(look.pl) 
Provides: perl%{perlver}(newgetopt.pl) 
Provides: perl%{perlver}(open2.pl) 
Provides: perl%{perlver}(open3.pl) 
Provides: perl%{perlver}(pwd.pl) 
Provides: perl%{perlver}(shellwords.pl) 
Provides: perl%{perlver}(stat.pl) 
Provides: perl%{perlver}(syslog.pl) 
Provides: perl%{perlver}(tainted.pl) 
Provides: perl%{perlver}(termcap.pl) 
Provides: perl%{perlver}(timelocal.pl) 
Provides: perl%{perlver}(utf8_heavy.pl) 
Provides: perl%{perlver}(validate.pl) 
#
# These modules appear to be missing or break assumptions made by the
# dependency analysis tools.  Typical problems include refering to
# CGI::Apache as Apache and having no package line in CPAN::Nox.pm. I
# hope that the perl people fix these to work with our dependency
# engine or give us better dependency tools.
#
Provides: perl%{perlver}(Apache)
Provides: perl%{perlver}(ExtUtils::MM_Mac)
Provides: perl%{perlver}(ExtUtils::XSSymSet)
Provides: perl%{perlver}(FCGI)
Provides: perl%{perlver}(LWP::UserAgent)
Provides: perl%{perlver}(Mac::Files)
Provides: perl%{perlver}(URI::URL)
Provides: perl%{perlver}(VMS::Filespec)

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.

%{compiler_msg}


%package db
Summary: Perl DB module.

BuildRequires: db-devel >= 5.3.28 
Requires: perl%{perlver} = %{version}-%{release}
Requires: db >= 5.3.28
Provides: perl%{perlver}(perl5db.pl)

Provides: perl%{perlver}(DB_File) = 1.853
Provides: DB_File.so

%description db
This package contains perl module to work with
Berkeley DB.


%prep
# export PATH=/opt/freeware/bin:$PATH

%setup -q -n perl-%{major_version}.%{minor_version}.%{bugfix_version}

mkdir modules
# Add license info
cat Artistic > LICENSE

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit


%build

export PATH=/opt/freeware/bin:$PATH
export LD="/usr/bin/ld"
export AR="/usr/bin/ar"
export ARFLAGS="-X32_64"
export NM="/usr/bin/nm"
export NMFLAGS="-X32_64 -B"
export MAKE="gmake"

#export OPT="-g -O0"
#export OPT="-g -O2"
#export OPT="   -O2"


# Choose GCC or XLC
#%if %{gcc_compiler} == 1

export CC="gcc"
#don't use full pathname -/opt/freeware- but $cc needs to begin with gcc for Makefile.sh
#export CXX="/opt/freeware/bin/g++"
export CFLAGS32="-maix32"
export CFLAGS64="-maix64"

echo "GCC version=`$CC --version | head -1`"

# %else
# 
# export CC="/usr/vac/bin/xlc_r"
# export CC="/opt/IBM/xlc/13.1.3/bin/xlc"
# export CXX="/usr/vacpp/bin/xlC_r"
# export CFLAGS32="-q32 -qcpluscmt"
# export CFLAGS64="-q64 -qcpluscmt"
# echo "XLC Version:"
# $CC -qversion
# 
# %endif

#if [[ "$CC" != "gcc" ]]
#then
#       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
#fi


build_perl()
{
set -x
ulimit -a

echo "CC=" $CC
echo "CFLAGS=" $CFLAGS
echo "LD=" $LD
echo "LDFLAGS=" $LDFLAGS
echo "AR=" $AR
echo "ARFLAGS=" $ARFLAGS

#Look at hints/aix.sh to know flags set for AIX
#        -Dlibperl=libperl.a \
#        -Dso=a \
#        -Dalignbytes=8 \
#	-Dld='/usr/bin/ld' \
#	-A define:ld='$CC' \
#        -Dlddlflags="$LDFLAGS -Wl,-H512 -WL,-T512 -Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bI:$(PERL_INC)/perl.exp -Wl,-bE:perl.exp -Wl,-bnoentry" \
#        -Dlddlflags='-Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bI:$(PERL_INC)/perl.exp -Wl,-bE:$(BASEEXT).exp -Wl,-bnoentry -lpthreads' \
#	-A define:ccdlflags='-Wl,-brtl -Wl,-bdynamic' \
#        -Dshrpldflags='-Wl,-H512 -Wl,-T512 -Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bE:perl.exp' \
#        -Dshrpldflags="$LDFLAGS -Wl,-H512 -Wl,-T512 -Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bE:perl.exp -Wl,-bnoentry" \
#        -Doptimize="$RPM_OPT_FLAGS" \
#        -Doptimize="-O" \

./Configure -des \
	-Dprefix=%{_prefix} \
        -Dversion=%{version} \
        -Dmyhostname=aix60 \
	-Darchname=%{_arch}-%{_os} \
	-Dperladmin=bullfreeware@atos.net \
        -Dcf_by='Bullfreeware BULL-ATOS' \
        -Dcf_email='bullfreeware@atos.net' \
	-Dcc="$CC" \
	-Dccflags="$CFLAGS -D_ALL_SOURCE -D_ANSI_C_SOURCE -D_POSIX_SOURCE -DUSE_NATIVE_DLOPEN -DNEED_PTHREAD_INIT -I/opt/freeware/include -D_LARGE_FILES" \
	-Dccflags_uselargefiles='-D_LARGE_FILES' \
	-Dldflags="$LDFLAGS" \
        -Dlddlflags="$LDDLFLAGS" \
	-Duseshrplib \
        -Dshrpldflags='-H512 -T512 -bhalt:4 -bM:SRE -bE:perl.exp' \
	-Dar="$AR" \
        -Dfull_ar="$AR" \
        -Darflags="$ARFLAGS" \
	-Dnm="$NM $NMFLAGS" \
	-Dinstallprefix=%{_prefix} \
        -Dvendorprefix=%{_prefix} \
        -Dvendorlib=%{vendorlibpath} \
        -Dvendorarch=$VENDORARCHPATH \
        -Dsiteprefix=%{_prefix} \
        -Dsitelib=%{sitelibpath} \
        -Dsitearch=$SITEARCHPATH \
        -Dprivlib=%{privlibpath} \
        -Darchlib=$ARCHLIBPATH \
	-Dusethreads \
	-Duseithreads \
	-Duselargefiles \
        -Dd_semctl_semun \
        -Di_syslog \
        -Dman3ext=3 \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dscriptdir='%{_bindir}' \
        $*

$MAKE  --trace --print-directory %{?_smp_mflags}
/usr/sbin/slibclean
}

ulimit -d 4000000

#export CFLAGS="$RPM_OPT_FLAGS"


#LDFLAGS : -Wl if the linker is being invoked indirectly, via a compiler driver (e.g. gcc)
#    then all the linker command line options should be prefixed by -Wl like this:
#     gcc -Wl,--start-group foo.o bar.o -Wl,--end-group
#     This is important, because otherwise the compiler driver program 
#     may silently drop the linker options, resulting in a bad link.
# -s to strip
export LDFLAGS3264="-Wl,-s"
export LDFLAGS3264="$LDFLAGS3264 -Wl,-lpthreads"
export LDFLAGS3264="$LDFLAGS3264 -Wl,-brtl -Wl,-bdynamic"
#export LDFLAGS="$LDFLAGS -shared -Wl,-H512 -Wl,-T512 -Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bnoentry"

#for AIX, MAKEFILE.sh set shrpldflags with "-shared -Wl,-H512 -Wl,-T512 -Wl,-bhalt:4 -Wl,-bM:SRE -Wl,-bE:perl.exp -Wl,-bnoentry"

# LDDLFLAG is LDFLAG used for modules.
# By default, add -L/usr/lib on 32 bits and /usr/lib64 on 64 bits.
# These directory are really different, so modules use AIX lib on 32 bits and freeware lib on 64 bits.
# We define lddlflags using default option + right -L
# -bhalt:4 is default, we do not add it
# -G is bad, but we keep it...
export LDDLFLAGS3264="-G -bI:\$(PERL_INC)/perl.exp -bE:\$(BASEEXT).exp -bnoentry -lc -lm"

# build 32bit mode

(
  cd 32bit
  export OBJECT_MODE=32
  # /usr/lib is unused, and we want to be sure lib are used from /opt/freeware/lib by default.
  # rpm lpp provides some .so, we provide less and less .so, and -G flag may .so with higher priority.
  # If needed, restore -L/usr/lib, but check carrefully which lib are used.
  export LIBS32="-L/opt/freeware/lib"
  export CFLAGS="${CFLAGS32} ${LIBS32}"
  export CXXFLAGS="${CFLAGS}"

  export LDFLAGS32="-Wl,-b32"
  export LDFLAGS32="$LDFLAGS32 -Wl,-blibpath:%{archlibpath32}CORE:%{_libdir}:/usr/lib:/lib"
  export LDFLAGS32="$LDFLAGS32 -Wl,-bmaxdata:0x80000000"
  export LDFLAGS="$LDFLAGS3264 $LDFLAGS32 $LIBS32"

  export LDDLFLAGS="$LDDLFLAGS3264 $LIBS32"

  export LIBPATH=`pwd`
  export VENDORARCHPATH=%{vendorarchpath32}
  export SITEARCHPATH=%{sitearchpath32}
  export ARCHLIBPATH=%{archlibpath32}
  
  # From INSTALL file
  #To build a shared libperl with -Duseshrplib, 
  #the environment variable controlling shared library search (LIBPATH for AIX)
  #must be set up to include the Perl build directory 
  #because that's where the shared libperl will be created.

  build_perl
  cd ..
)

# build 64bit mode
(
  cd 64bit
  export OBJECT_MODE=64
  # See comment about /usr/lib in 32 bits section.
  export LIBS64="-L/opt/freeware/lib64 -L/opt/freeware/lib"
  export CFLAGS="${CFLAGS64} ${LIBS64}"
  export CXXFLAGS="${CFLAGS}"
  
  #perl ld
  export LDFLAGS64="-Wl,-b64"
  export LDFLAGS64="$LDFLAGS64 -Wl,-blibpath:%{archlibpath64}CORE:%{archlibpath32}CORE:%{_libdir64}:%{_libdir}:/usr/lib:/lib"
  #no -bmaxdata for 64bit
  export LDFLAGS="$LDFLAGS3264 $LDFLAGS64 $LIBS64"

  export LDDLFLAGS="$LDDLFLAGS3264 $LIBS64"

# with -Duse64bitall
# What is the size of a pointer (in bytes)? [4]  
#*** You have chosen a maximally 64-bit build,
#*** but your pointers are only 4 bytes wide.
#*** Please rerun Configure without -Duse64bitall.
#*** Since you have quads, you could possibly try with -Duse64bitint.


  export LIBPATH=`pwd`
  export VENDORARCHPATH=%{vendorarchpath64}
  export SITEARCHPATH=%{sitearchpath64}
  export ARCHLIBPATH=%{archlibpath64}
  
  build_perl -Duse64bitint
  cd ..
)

# 32-bit libperl.o
# Add the 64 bit object to the 32/64 bits archive
$AR -X32_64 -q 32bit/libperl.a 64bit/libperl.o


%install
set -x
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar"
export ARFLAGS="-X32_64"
export NM="/usr/bin/nm"
export NMFLAGS="$NMFLAGS -X32_64 -B"
export MAKE="gmake --trace --print-directory -d"

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT

cd 64bit
$MAKE DESTDIR=${RPM_BUILD_ROOT} install 


mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
/opt/freeware/bin/install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_bindir}/pl2pm

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    # Scripts
    for bin in $(ls -1| grep -v -e _32 -e _64 -e perl5)
    do
        mv ${bin} ${bin}%{perlver}
    done

    # Perl binary
    mv perl%{version} perl%{version}_64    
)
cd ..

#Install on 32bit mode
cd 32bit
#$MAKE install 
$MAKE DESTDIR=${RPM_BUILD_ROOT} install 

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    # Scripts
    for bin in $(ls -1| grep -v -e _32 -e _64 -e perl5 -e %{perlver})
    do
        mv ${bin} ${bin}%{perlver}
    done

    # Perl binary
    mv  perl%{version} perl%{version}_32

    # Default version
    ln -sf perl%{version}_%{default_bits} perl%{perlver}
    ln -sf perl%{version}_%{default_bits} perl%{version}
)
cd ..

# Create (empty) vendor_perl and sitelib_perl libs
mkdir -p ${RPM_BUILD_ROOT}%{sitelibpath}
mkdir -p ${RPM_BUILD_ROOT}%{vendorlibpath}
mkdir -p ${RPM_BUILD_ROOT}%{vendorarchpath32}
mkdir -p ${RPM_BUILD_ROOT}%{vendorarchpath64}

# Generate *.ph files with a trick. Is this sick or what ?
gmake all -f - <<EOF
PKGS	= glibc-devel gdbm-devel gpm-devel libgr-devel libjpeg-devel \
	  libpng-devel libtiff-devel ncurses-devel popt \
	  zlib-devel binutils libelf e2fsprogs-devel pam pwdb \
	  rpm-devel
STDH	= \$(filter %{_includedir}/include/%%, \$(shell rpm -q --queryformat '[%%{FILENAMES}\n]' \$(PKGS)))
STDH	+=\$(wildcard %{_includedir}/linux/*.h) \$(wildcard %{_includedir}/asm/*.h) \
	  \$(wildcard %{_includedir}/scsi/*.h)
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%, \$(shell rpm -q --queryformat '[%%{FILEMODES} %%{FILENAMES}\n]' gcc | grep -v ^4 | awk '{print $NF}'))

PERLLIB = \$(RPM_BUILD_ROOT)%{privlibpath}:\$(RPM_BUILD_ROOT)%{archlibpath64}
PERL	= PERL5LIB=\$(PERLLIB) LIBPATH=\$(RPM_BUILD_ROOT)%{archlibpath64}CORE:%{_libdir}:/usr/lib \$(RPM_BUILD_ROOT)%{_bindir}/perl%{version}_64
PHDIR   = \$(RPM_BUILD_ROOT)%{archlibpath64}/
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph%{perlver} -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	cd %{_includedir} && \$(H2PH) \$(STDH:%{_includedir}/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%) || true

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<
EOF

# 32 bits
gmake all -f - <<EOF
PKGS	= glibc-devel gdbm-devel gpm-devel libgr-devel libjpeg-devel \
	  libpng-devel libtiff-devel ncurses-devel popt \
	  zlib-devel binutils libelf e2fsprogs-devel pam pwdb \
	  rpm-devel
STDH	= \$(filter %{_includedir}/include/%%, \$(shell rpm -q --queryformat '[%%{FILENAMES}\n]' \$(PKGS)))
STDH	+=\$(wildcard %{_includedir}/linux/*.h) \$(wildcard %{_includedir}/asm/*.h) \
	  \$(wildcard %{_includedir}/scsi/*.h)
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%, \$(shell rpm -q --queryformat '[%%{FILEMODES} %%{FILENAMES}\n]' gcc | grep -v ^4 | awk '{print $NF}'))

PERLLIB = \$(RPM_BUILD_ROOT)%{privlibpath}:\$(RPM_BUILD_ROOT)%{archlibpath32}
PERL	= PERL5LIB=\$(PERLLIB) LIBPATH=\$(RPM_BUILD_ROOT)%{archlibpath32}CORE:%{_libdir}:/usr/lib \$(RPM_BUILD_ROOT)%{_bindir}/perl%{version}_32
PHDIR   = \$(RPM_BUILD_ROOT)%{archlibpath32}/
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph%{perlver} -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	cd %{_includedir} && \$(H2PH) \$(STDH:%{_includedir}/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%) || true

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<
EOF

(
  cd $RPM_BUILD_ROOT

  mvdir .%{_datadir}/man .%{_mandir}
  # The Thread.3 manpage duplicates the same file in the tcl package.
  rm .%{_mandir}/man3/Thread.3

  # Deal with multiple version
  cd $RPM_BUILD_ROOT%{_mandir}/man1
  for man in $(ls -1)
  do
    mv ${man} `basename ${man} .1`%{perlver}.1
  done
  cd $RPM_BUILD_ROOT%{_mandir}/man3
  for man in $(ls -1)
  do
    mv ${man} `basename ${man} .3`%{perlver}.3
  done
)

(
 cd $RPM_BUILD_ROOT
 # Replace 64 bits libperl.a by a link to the 32 bit (containing both .so).
 rm -f .%{archlibpath64}CORE/libperl.a
 ln -s %{archlibpath32}CORE/libperl.a ${RPM_BUILD_ROOT}%{archlibpath64}CORE/libperl.a
)

# Replace perl to perl%{version} in installed scripts
(
  cd $RPM_BUILD_ROOT
  /opt/freeware/bin/find . -type f | xargs /opt/freeware/bin/sed -i 's|#!/opt/freeware/bin/perl|#!/opt/freeware/bin/perl%{version}|g'
)

%check
# For 64 bits tests.
ulimit -d 4000000

export PATH=/opt/freeware/bin:$PATH
export MAKE="gmake"
export AR="/usr/bin/ar"
export ARFLAGS="-X32_64"

%if %{with dotests}
cd 32bit
export LIBPATH=`pwd`:/opt/freeware/lib:/usr/lib
export OBJECT_MODE=32
( $MAKE  --trace --print-directory -k check || true )
/usr/sbin/slibclean
cd ../64bit
export LIBPATH=`pwd`:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib
export OBJECT_MODE=64
( $MAKE  --trace --print-directory -k check || true )
/usr/sbin/slibclean
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/Artistic 32bit/AUTHORS 32bit/Changes* 32bit/README 32bit/LICENSE
%{_bindir}/*
%{_libdir}/perl5/*
%exclude %{archlibpath32}/CORE/libperl_nonshr.a
%exclude %{archlibpath32}/auto/DB_File/DB_File.so

%{_libdir64}/perl5/*
%exclude %{archlibpath64}/CORE/libperl_nonshr.a
%exclude %{archlibpath64}/auto/DB_File/DB_File.so

%{_datadir}/perl5/%{perlver}/*
%exclude %{privlibpath}/perl5db.pl

%{_mandir}/*/*


%files db
%defattr(-,root,system)
%doc 32bit/Artistic 32bit/AUTHORS 32bit/Changes* 32bit/README 32bit/LICENSE
%{archlibpath32}/auto/DB_File/DB_File.so
%{archlibpath64}/auto/DB_File/DB_File.so
%{privlibpath}/perl5db.pl


%changelog
* Mon Oct 11 2021 Etienne Guesnet <etienne.guesnet@atos.net> 5.34.0-1
- New version 5.34.0

* Mon Oct 11 2021 Etienne Guesnet <etienne.guesnet@atos.net> 5.32.1-1
- Parallel installation
- Remove explicit .so Provides.
- New version 5.32.1

* Thu Nov 19 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 5.32.0-6
- Rebuild 5.32.0

* Tue Nov 17 2020 Étienne Guesnet <etienne.guesnet@atos.net> 5.32.0-5
- Update specfile for automated build
- Change ulimit
- Remove manual %{prefix}
- Do not use /usr/lib to link modules (was used on 32 bits only)

* Fri Oct 23 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 5.32.0-4
- Rebuild 5.32.0

* Thu Oct 22 2020 Étienne Guesnet <etienne.guesnet@atos.net> 5.32.0-3
- Put DB dependency in a subpackage

* Mon Jul 06 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> 5.32.0-1
- New version 5.32.0

* Wed Feb 26 2020 Etienne Guesnet <etienne.guesnet.external@atos.net> 5.30.1-1
- New version 5.30.2

* Thu Jan 02 2020 Clément Chigot <clement.chigot@atos.net> 5.30.0-2
- Fix link for 64bit libperl.a

* Mon Jul 15 2019 Etienne Guesnet <etienne.guesnet.external@atos.net> 5.30.0-1
- Udate to version  5.30.0
- Change lib, vendor and site path.

* Fri Jul 27 2018 Daniele Silvestre <daniele.silvestre@atos.net> 5.26.2-2
- Fix vendor_perl directory not created

* Wed May 30 2018 Tony Reix <tony.reix@bull.net> 5.26.2-1
- Move to: MODULE_COMPAT_5.26.2

* Fri May 25 2018 Daniele Silvestre <daniele.silvestre@atos.net> 5.26.1-1
- Move to: MODULE_COMPAT_5.26.1
- Build with GCC instead of XLC

* Mon Nov 13 2017 Tony Reix <tony.reix@bull.net> 5.24.0-3
- Move to: MODULE_COMPAT_5.24.0
- Fix issue with "install -m 755 ...".

* Wed Feb 22 2017 Tony Reix <tony.reix@bull.net> 5.24.0-2
- Fix /var/opt/freeware/tmp/perl-root issue in files:
   /opt/freeware/lib/perl5/5.24.0/ppc-aix-thread-multi-64all/Config_heavy.pl
   /opt/freeware/lib/perl5/5.24.0/ppc-aix-thread-multi/Config_heavy.pl
- Add: MODULE_COMPAT_5.22.0

* Fri Dec 02 2016 Michael Wilson <michael.wilson@bull.net> 5.24.0-1
- Udate to version  5.24.0

* Thu Nov 10 2016 Michael Wilson <michael.wilson@bull.net> 5.22.0-2
- Include make test for 32 and 64 bit builds
- Patch Config_heavy.pl to remove $RPM_BUILD_ROOT from -bE:  "-e ldopts" output

* Mon Aug 31 2015 Michael Wilson <michael.wilson@bull.net> 5.22.0-1
- Udate to version  5.22.0

* Wed Nov 06 2013 Gerard Visiedo <gerard.visiedo@bull.net> 5.18.1-1
- Udate to version  5.18.1

* Thu Apr 05 2012 BULL 5.10.1-1
- Update to 5.10.1

* Thu Jul 16 2009 BULL 5.10.0-1
- Update to 5.10.0

* Thu Jun 03 2004 David Clissold <cliss@austin.ibm.com> 5.8.3-1
- Update to 5.8.2.

* Tue Feb 17 2004 Philip K. Warren <pkw@us.ibm.com> 5.8.0-2
- Update Provides for Perl 5.8.0.

* Mon Nov 03 2003 David Clissold <cliss@austin.ibm.com>
- Update to 5.8.0.

* Fri Apr 25 2003 David Clissold <cliss@austin.ibm.com>
- Add dlopen/dlclose patch from Brad Elkin, IBM Minneapolis.

* Tue Mar 18 2003 David Clissold <cliss@austin.ibm.com>
- Undo Nov 22 change; no ILA, just Artistic, as per README.

* Fri Dec 13 2002 David Clissold <cliss@austin.ibm.com>
- Build with -bmaxdata:0x80000000 (tzy@us.ibm.com).

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Sat Aug 04 2001 David Clissold <cliss@austin.ibm.com>
- Strip of binaries was missed.

* Thu Jul 12 2001 David Clissold <cliss@austin.ibm.com>
- initial build for AIX Toolbox

* Tue Jun 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- unbundle the Digest-MD5 module (noted by Charlie Brady) -- perl
  dependency checking RPM will do most of the heavy lifting
- mark License as GPL or Artistic

* Thu Jun 14 2001 Nalin Dahyabhai <nalin@redhat.com>
- use /usr/lib/rpm/findprovides.perl to complete the list of perl provides
- change Copyright: GPL to License: GPL
- include some of the text documentation files

* Wed Jun 13 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added provides to close bug #43081

* Fri Jun 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x change to specfile from Oliver Paukstadt
  <oliver.paukstadt@millenux.com>

* Fri Mar 23 2001 Preston Brown <pbrown@redhat.com>
- bzip2 source, save some space.

* Thu Dec  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- initial rebuild for 7.1

* Tue Sep 12 2000 Bill Nottingham <notting@redhat.com>
- fix dependencies on ia64/sparc64

* Mon Aug  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- replace the deprecated MD5 with Digest::MD5 (has to be here for cleanfeed)
- obsolete: perl-Digest-MD5
- use syslog instead of mail to report possible attempts to break into suidperl
- force syslog on at build-time

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Owen's fix for #14779/#14863
- specify cc=%{__cc}; continue to let cpp sort itself out
- switch shadow support on (#8646)
- release 7

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- strip buildroot from perl pods (#14040)
- release 6

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild (release 5)

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- don't require tcsh to install, only to build
- release 4

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild against new db3 package
- release 3

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable 64-bit file support
- change name of package that Perl expects gcc to be in from "egcs" to "gcc"
- move man pages to /usr/share via hints/linux.sh and MM_Unix.pm
- fix problems prefixifying with empty prefixes
- disable long doubles on sparc (they're the same as doubles anyway)
- add an Epoch to make sure we can upgrade from perl-5.00503
- release 2

* Thu Mar 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.6.0

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan 14 2000 Jeff Johnson <jbj@redhat.com>
- add provides for perl modules (from kestes@staff.mail.com).

* Mon Oct 04 1999 Cristian Gafton <gafton@redhat.com>
- fix the %install so that the MD5 module gets actually installed correctly

* Mon Aug 30 1999 Cristian Gafton <gafton@redhat.com>
- make sure the package builds even when we don't have perl installed on the
  system

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- merged with perl-MD5
- get rid of the annoying $RPM_BUILD_ROOT paths in the installed tree

* Mon Jul 26 1999 Cristian Gafton <gafton@redhat.com>
- do not link anymore against the system db library (and make each module
  link against it separately, so that we can have Berkeley db1 and db2 mixed
  up)

* Wed Jun 16 1999 Cristian Gafton <gafton@redhat.com>
- use wildcards for files in /usr/bin and /usr/man

* Tue Apr 06 1999 Cristian Gafton <gafton@redhat.com>
- version 5.00503
- make the default man3 install dir be release independent
- try to link against db1 to preserve compatibility with older databases;
  abandoned idea because perl is too broken to allow such an easy change
  (hardcoded names *everywhere* !!!)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- guilty of the inlined Makefile in the spec file
- adapted for the arm build

* Wed Sep 09 1998 Preston Brown <pbrown@redhat.com>
- added newer CGI.pm to the build
- changed the version naming scheme around to work with RPM

* Sun Jul 19 1998 Jeff Johnson <jbj@redhat.com>
- attempt to generate *.ph files reproducibly

* Mon Jun 15 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.004_04-m4 (pre-5.005 maintenance release)

* Fri Jun 12 1998 Christopher McCrory <chrismcc@netus.com
- need stdarg.h from gcc shadow to fix "use Sys::Syslog" (problem #635)

* Fri May 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to correct the .ph constructs unless defined (foo) to read
  unless(defined(foo))

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- fixed strftime problem

* Sun Mar 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to fix a security race
- do not use setres[ug]id - those are not implemented on 2.0.3x kernels

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 5.004_04 - 5.004_01 had some nasty memory leaks.
- fixed the spec file to be version-independent

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- Config.pm wasn't right do to the builtrooting

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- fixed arch-specfic part of spec file

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to perl 5.004_01
- users a build root

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Erik Troan <ewt@redhat.com>
- Incorporated security patch from Chip Salzenberg <salzench@nielsenmedia.com>

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Use -Darchname=i386-linux 
- Require csh (for glob)
- Use RPM_ARCH during configuration and installation for arch independence
