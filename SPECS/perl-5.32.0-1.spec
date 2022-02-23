#By default, 64bit mode
%define default_bits 64

# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64     %{_prefix}/lib64

%define perlver 5.32

# Site: default location for modules installed by user
%define sitelibpath       %{_datadir}/perl5/site_perl/
%define sitearchpath32    %{_libdir}/perl5/%{perlver}/site_perl/
%define sitearchpath64    %{_libdir64}/perl5/%{perlver}/site_perl/
# Vendor: default location for modules installed through packages
%define vendorlibpath     %{_datadir}/perl5/vendor_perl/
%define vendorarchpath32  %{_libdir}/perl5/%{perlver}/vendor_perl/
%define vendorarchpath64  %{_libdir64}/perl5/%{perlver}/vendor_perl/
# privlib and archlib are default location fore Perl core modules
%define privlibpath       %{_datadir}/perl5/%{perlver}/
%define archlibpath32     %{_libdir}/perl5/%{perlver}/
%define archlibpath64     %{_libdir64}/perl5/%{perlver}/

Summary: The Perl programming language.
Name: perl
Version: %{perlver}.0
Release: 1
License: Artistic
URL: http://www.perl.com
Group: Development/Languages
Source0: http://www.perl.com/CPAN/src/perl-%{version}.tar.gz
Source10: %{name}-%{version}-%{release}.build.log
Prefix: %{_prefix}
BuildRequires: gdbm-devel >= 1.18
Requires: gdbm >= 1.18
Epoch: 1

# Patch0: %{name}-%{version}-aix.patch
# Better way include by default
#Patch0: %{name}-5.28.0-aixmm.patch

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%define osplat aix7
%endif
%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%define osplat aix7
%endif

# compat macro needed for rebuild
%global perl_compat perl(:MODULE_COMPAT_%{perlver})

# ----- Perl module provides.

Provides: %perl_compat
Provides: perl(perl) = %{perlver}
Provides: perl = %{perlver}

# --------------------------------

Provides: perl(Archive::Tar) = 2.36
Provides: perl(Attribute::Handlers) = 1.01
Provides: perl(AutoLoader) = 5.74
Provides: perl(CPAN) = 2.27
Provides: perl(CPAN::Meta) = 2.150010
Provides: perl(CPAN::Meta::Requirements) = 2.140
Provides: perl(CPAN::Meta::YAML) = 0.018
Provides: perl(Carp) = 1.50
Provides: perl(Compress::Raw::Bzip2) = 2.093
Provides: perl(Compress::Raw::Zlib) = 2.093
Provides: perl(Config::Perl::V) = 0.32
Provides: perl(DB_File) = 1.853
Provides: perl(Data::Dumper) = 2.174
Provides: perl(Devel::PPPort) = 3.57
Provides: perl(Devel::SelfStubber) = 1.06
Provides: perl(Digest) = 1.17_01
Provides: perl(Digest::MD5) = 2.55_01
Provides: perl(Digest::SHA) = 6.02
Provides: perl(Dumpvalue) = 1.21
Provides: perl(Encode) = 3.06
Provides: perl(Env) = 1.04
Provides: perl(Exporter) = 5.74
Provides: perl(ExtUtils::CBuilder) = 0.280234
Provides: perl(ExtUtils::Constant) = 0.25
Provides: perl(ExtUtils::Install) = 2.14
Provides: perl(ExtUtils::MakeMaker) = 7.44
Provides: perl(ExtUtils::Manifest) = 1.72
Provides: perl(ExtUtils::ParseXS) = 3.40
Provides: perl(File::Fetch) = 0.56
Provides: perl(File::Path) = 2.16
Provides: perl(File::Temp) = 0.2309
Provides: perl(Filter::Simple) = 0.96
Provides: perl(Getopt::Long) = 2.51
Provides: perl(HTTP::Tiny) = 0.076
Provides: perl(I18N::Collate) = 1.02
Provides: perl(IO) = 1.43
Provides: perl(IO::Socket::IP) = 0.39
Provides: perl(IO::Zlib) = 1.10
Provides: perl(IPC::Cmd) = 1.04
Provides: perl(IPC::SysV) = 2.07
Provides: perl(JSON::PP) = 4.04
Provides: perl(Locale::Maketext) = 1.29
Provides: perl(Locale::Maketext::Simple) = 0.21_01
Provides: perl(MIME::Base64) = 3.15
Provides: perl(Math::BigInt) = 1.999818
Provides: perl(Math::BigInt::FastCalc) = 0.5009
Provides: perl(Math::BigRat) = 0.2614
Provides: perl(Math::Complex) = 1.5901
Provides: perl(Memoize) = 1.03_01
Provides: perl(Module::CoreList) = 5.20200620
Provides: perl(Module::Load) = 0.34
Provides: perl(Module::Load::Conditional) = 0.70
Provides: perl(Module::Loaded) = 0.08
Provides: perl(Module::Metadata) = 1.000037
Provides: perl(NEXT) = 0.67_01
Provides: perl(Net::Ping) = 2.72
Provides: perl(Params::Check) = 0.38
Provides: perl(Perl::OSType) = 1.010
Provides: perl(PerlIO::via::QuotedPrint) = 0.08
Provides: perl(Pod::Checker) = 1.73
Provides: perl(Pod::Escapes) = 1.07
# Pod::Parser is no more provided
Provides: perl(Pod::Perldoc) = 3.2801
Provides: perl(Pod::Simple) = 3.40
Provides: perl(Pod::Usage) = 1.69
Provides: perl(Safe) = 2.41
Provides: perl(Search::Dict) = 1.07
Provides: perl(SelfLoader) = 1.26
Provides: perl(Socket) = 2.029
Provides: perl(Storable) = 3.21
Provides: perl(Sys::Syslog) = 0.36
Provides: perl(Term::ANSIColor) = 5.01
Provides: perl(Term::Cap) = 1.17
Provides: perl(Term::Complete) = 1.403
Provides: perl(Term::ReadLine) = 1.17
Provides: perl(Test) = 1.31
Provides: perl(Test::Harness) = 3.42
Provides: perl(Test::Simple) = 1.302175
Provides: perl(Text::Abbrev) = 1.02
Provides: perl(Text::Balanced) = 2.03
Provides: perl(Text::ParseWords) = 3.30
Provides: perl(Thread::Queue) = 3.14
Provides: perl(Thread::Semaphore) = 2.13
Provides: perl(Tie::File) = 1.06
Provides: perl(Tie::RefHash) = 1.39
Provides: perl(Time::HiRes) = 1.9764
Provides: perl(Time::Local) = 1.28
Provides: perl(Time::Piece) = 1.3401
Provides: perl(Unicode::Collate) = 1.27
Provides: perl(Unicode::Normalize) = 1.27
Provides: perl(XSLoader) = 0.30
Provides: perl(autodie) = 2.32
Provides: perl(autouse) = 1.11
Provides: perl(base) = 2.27
Provides: perl(bignum) = 0.51
Provides: perl(constant) = 1.33
Provides: perl(encoding::warnings) = 0.13
Provides: perl(experimental) = 0.020
Provides: perl(if) = 0.0608
Provides: perl(lib) = 0.65
Provides: perl(parent) = 0.238
Provides: perl(perlfaq) = 5.20200523
Provides: perl(threads) = 2.25
Provides: perl(threads::shared) = 1.61
Provides: perl(version) = 0.9924
Provides: perl(AnyDBM_File) = 1.01
Provides: perl(App::Cpan) = 1.675
Provides: perl(App::Prove) = 3.42
Provides: perl(App::Prove::State) = 3.42
Provides: perl(App::Prove::State::Result) = 3.42
Provides: perl(App::Prove::State::Result::Test) = 3.42
Provides: perl(Archive::Tar::Constant) = 2.36
Provides: perl(Archive::Tar::File) = 2.36
Provides: perl(AutoSplit) = 1.06
Provides: perl(B) = 1.80
Provides: perl(B::Concise) = 1.004
Provides: perl(B::Deparse) = 1.54
Provides: perl(B::Op_private) = 5.032000
Provides: perl(B::Showlex) = 1.05
Provides: perl(B::Terse) = 1.09
Provides: perl(B::Xref) = 1.07
Provides: perl(Benchmark) = 1.23
Provides: perl(CPAN::Author) = 5.5002
Provides: perl(CPAN::Bundle) = 5.5005
Provides: perl(CPAN::CacheMgr) = 5.5002
Provides: perl(CPAN::Complete) = 5.5001
Provides: perl(CPAN::Debug) = 5.5001
Provides: perl(CPAN::DeferredCode) = 5.50
Provides: perl(CPAN::Distribution) = 2.27
Provides: perl(CPAN::Distroprefs) = 6.0001
Provides: perl(CPAN::Distrostatus) = 5.5
Provides: perl(CPAN::Exception::RecursiveDependency) = 5.5001
Provides: perl(CPAN::Exception::blocked_urllist) = 1.001
Provides: perl(CPAN::Exception::yaml_not_installed) = 5.5
Provides: perl(CPAN::Exception::yaml_process_error) = 5.5
Provides: perl(CPAN::FTP) = 5.5012
Provides: perl(CPAN::FTP::netrc) = 1.01
Provides: perl(CPAN::FirstTime) = 5.5314
Provides: perl(CPAN::HTTP::Client) = 1.9601
Provides: perl(CPAN::HTTP::Credentials) = 1.9601
Provides: perl(CPAN::HandleConfig) = 5.5011
Provides: perl(CPAN::Index) = 2.12
Provides: perl(CPAN::InfoObj) = 5.5
Provides: perl(CPAN::Kwalify) = 5.50
Provides: perl(CPAN::LWP::UserAgent) = 1.9601
Provides: perl(CPAN::Meta::Converter) = 2.150010
Provides: perl(CPAN::Meta::Feature) = 2.150010
Provides: perl(CPAN::Meta::History) = 2.150010
Provides: perl(CPAN::Meta::Merge) = 2.150010
Provides: perl(CPAN::Meta::Prereqs) = 2.150010
Provides: perl(CPAN::Meta::Spec) = 2.150010
Provides: perl(CPAN::Meta::Validator) = 2.150010
Provides: perl(CPAN::Mirrors) = 2.27
Provides: perl(CPAN::Module) = 5.5003
Provides: perl(CPAN::Nox) = 5.5001
Provides: perl(CPAN::Plugin) = 0.97
Provides: perl(CPAN::Plugin::Specfile) = 0.02
Provides: perl(CPAN::Prompt) = 5.5
Provides: perl(CPAN::Queue) = 5.5003
Provides: perl(CPAN::Shell) = 5.5009
Provides: perl(CPAN::Tarzip) = 5.5013
Provides: perl(CPAN::URL) = 5.5
Provides: perl(CPAN::Version) = 5.5003
Provides: perl(Carp::Heavy) = 1.50
Provides: perl(Class::Struct) = 0.66
Provides: perl(Compress::Zlib) = 2.093
Provides: perl(Config::Extensions) = 0.03
Provides: perl(Cwd) = 3.78
Provides: perl(DBM_Filter) = 0.06
Provides: perl(DBM_Filter::compress) = 0.03
Provides: perl(DBM_Filter::encode) = 0.03
Provides: perl(DBM_Filter::int32) = 0.03
Provides: perl(DBM_Filter::null) = 0.03
Provides: perl(DBM_Filter::utf8) = 0.03
Provides: perl(Devel::Peek) = 1.28
Provides: perl(Devel::Symdump::Export) = 2.18
Provides: perl(Digest::base) = 1.16
Provides: perl(Digest::file) = 1.16
Provides: perl(DirHandle) = 1.05
Provides: perl(DynaLoader) = 1.47
Provides: perl(Encode::Alias) = 2.24
Provides: perl(Encode::Byte) = 2.04
Provides: perl(Encode::CJKConstants) = 2.02
Provides: perl(Encode::CN) = 2.03
Provides: perl(Encode::CN::HZ) = 2.10
Provides: perl(Encode::Config) = 2.05
Provides: perl(Encode::EBCDIC) = 2.02
Provides: perl(Encode::Encoder) = 2.03
Provides: perl(Encode::Encoding) = 2.08
Provides: perl(Encode::GSM0338) = 2.07
Provides: perl(Encode::Guess) = 2.08
Provides: perl(Encode::JP) = 2.04
Provides: perl(Encode::JP::H2Z) = 2.02
Provides: perl(Encode::JP::JIS7) = 2.08
Provides: perl(Encode::KR) = 2.03
Provides: perl(Encode::KR::2022_KR) = 2.04
Provides: perl(Encode::MIME::Header) = 2.28
Provides: perl(Encode::MIME::Header::ISO_2022_JP) = 1.09
Provides: perl(Encode::MIME::Name) = 1.03
Provides: perl(Encode::Symbol) = 2.02
Provides: perl(Encode::TW) = 2.03
Provides: perl(Encode::Unicode) = 2.18
Provides: perl(Encode::Unicode::UTF7) = 2.10
Provides: perl(English) = 1.11
Provides: perl(Exporter::Heavy) = 5.74
Provides: perl(ExtUtils::CBuilder::Base) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::Unix) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::VMS) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::Windows) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::Windows::BCC) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::Windows::GCC) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::Windows::MSVC) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::aix) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::android) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::cygwin) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::darwin) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::dec_osf) = 0.280234
Provides: perl(ExtUtils::CBuilder::Platform::os2) = 0.280234
Provides: perl(ExtUtils::Command) = 7.44
Provides: perl(ExtUtils::Command::MM) = 7.44
Provides: perl(ExtUtils::Constant::Base) = 0.06
Provides: perl(ExtUtils::Constant::ProxySubs) = 0.09
Provides: perl(ExtUtils::Constant::Utils) = 0.04
Provides: perl(ExtUtils::Constant::XS) = 0.03
Provides: perl(ExtUtils::Embed) = 1.35
Provides: perl(ExtUtils::Installed) = 2.14
Provides: perl(ExtUtils::Liblist) = 7.44
Provides: perl(ExtUtils::Liblist::Kid) = 7.44
Provides: perl(ExtUtils::MM) = 7.44
Provides: perl(ExtUtils::MM_AIX) = 7.44
Provides: perl(ExtUtils::MM_Any) = 7.44
Provides: perl(ExtUtils::MM_BeOS) = 7.44
Provides: perl(ExtUtils::MM_Cygwin) = 7.44
Provides: perl(ExtUtils::MM_DOS) = 7.44
Provides: perl(ExtUtils::MM_Darwin) = 7.44
Provides: perl(ExtUtils::MM_MacOS) = 7.44
Provides: perl(ExtUtils::MM_NW5) = 7.44
Provides: perl(ExtUtils::MM_OS2) = 7.44
Provides: perl(ExtUtils::MM_QNX) = 7.44
Provides: perl(ExtUtils::MM_UWIN) = 7.44
Provides: perl(ExtUtils::MM_Unix) = 7.44
Provides: perl(ExtUtils::MM_VMS) = 7.44
Provides: perl(ExtUtils::MM_VOS) = 7.44
Provides: perl(ExtUtils::MM_Win32) = 7.44
Provides: perl(ExtUtils::MM_Win95) = 7.44
Provides: perl(ExtUtils::MY) = 7.44
Provides: perl(ExtUtils::MakeMaker::Config) = 7.44
Provides: perl(ExtUtils::MakeMaker::Locale) = 7.44
Provides: perl(ExtUtils::MakeMaker::version) = 7.44
Provides: perl(ExtUtils::Miniperl) = 1.09
Provides: perl(ExtUtils::Mkbootstrap) = 7.44
Provides: perl(ExtUtils::Mksymlists) = 7.44
Provides: perl(ExtUtils::Packlist) = 2.14
Provides: perl(ExtUtils::ParseXS::Constants) = 3.40
Provides: perl(ExtUtils::ParseXS::CountLines) = 3.40
Provides: perl(ExtUtils::ParseXS::Eval) = 3.40
Provides: perl(ExtUtils::ParseXS::Utilities) = 3.40
Provides: perl(ExtUtils::Typemaps) = 3.38
Provides: perl(ExtUtils::Typemaps::Cmd) = 3.38
Provides: perl(ExtUtils::Typemaps::InputMap) = 3.38
Provides: perl(ExtUtils::Typemaps::OutputMap) = 3.38
Provides: perl(ExtUtils::Typemaps::Type) = 3.38
Provides: perl(ExtUtils::testlib) = 7.44
Provides: perl(Fatal) = 2.32
Provides: perl(Fcntl) = 1.13
Provides: perl(File::Basename) = 2.85
Provides: perl(File::Compare) = 1.1006
Provides: perl(File::Copy) = 2.34
Provides: perl(File::DosGlob) = 1.12
Provides: perl(File::Find) = 1.37
Provides: perl(File::Glob) = 1.33
Provides: perl(File::GlobMapper) = 1.001
Provides: perl(File::Spec) = 3.78
Provides: perl(File::Spec::AmigaOS) = 3.78
Provides: perl(File::Spec::Cygwin) = 3.78
Provides: perl(File::Spec::Epoc) = 3.78
Provides: perl(File::Spec::Functions) = 3.78
Provides: perl(File::Spec::Mac) = 3.78
Provides: perl(File::Spec::OS2) = 3.78
Provides: perl(File::Spec::Unix) = 3.78
Provides: perl(File::Spec::VMS) = 3.78
Provides: perl(File::Spec::Win32) = 3.79
Provides: perl(File::stat) = 1.09
Provides: perl(FileCache) = 1.10
Provides: perl(FileHandle) = 2.03
Provides: perl(Filter::Util::Call) = 1.59
Provides: perl(FindBin) = 1.51
Provides: perl(GDBM_File) = 1.18
Provides: perl(Getopt::Std) = 1.12
Provides: perl(Hash::Util) = 0.23
Provides: perl(Hash::Util::FieldHash) = 1.20
Provides: perl(I18N::LangTags) = 0.44
Provides: perl(I18N::LangTags::Detect) = 1.08
Provides: perl(I18N::LangTags::List) = 0.40
Provides: perl(I18N::Langinfo) = 0.19
Provides: perl(IO::Compress::Adapter::Bzip2) = 2.093
Provides: perl(IO::Compress::Adapter::Deflate) = 2.093
Provides: perl(IO::Compress::Adapter::Identity) = 2.093
Provides: perl(IO::Compress::Base) = 2.093
Provides: perl(IO::Compress::Base::Common) = 2.093
Provides: perl(IO::Compress::Bzip2) = 2.093
Provides: perl(IO::Compress::Deflate) = 2.093
Provides: perl(IO::Compress::Gzip) = 2.093
Provides: perl(IO::Compress::Gzip::Constants) = 2.093
Provides: perl(IO::Compress::RawDeflate) = 2.093
Provides: perl(IO::Compress::Zip) = 2.093
Provides: perl(IO::Compress::Zip::Constants) = 2.093
Provides: perl(IO::Compress::Zlib::Constants) = 2.093
Provides: perl(IO::Compress::Zlib::Extra) = 2.093
Provides: perl(IO::Dir) = 1.41
Provides: perl(IO::File) = 1.41
Provides: perl(IO::Handle) = 1.42
Provides: perl(IO::Pipe) = 1.41
Provides: perl(IO::Poll) = 1.41
Provides: perl(IO::Seekable) = 1.41
Provides: perl(IO::Select) = 1.42
Provides: perl(IO::Socket) = 1.43
Provides: perl(IO::Socket::INET) = 1.41
Provides: perl(IO::Socket::UNIX) = 1.41
Provides: perl(IO::Uncompress::Adapter::Bunzip2) = 2.093
Provides: perl(IO::Uncompress::Adapter::Identity) = 2.093
Provides: perl(IO::Uncompress::Adapter::Inflate) = 2.093
Provides: perl(IO::Uncompress::AnyInflate) = 2.093
Provides: perl(IO::Uncompress::AnyUncompress) = 2.093
Provides: perl(IO::Uncompress::Base) = 2.093
Provides: perl(IO::Uncompress::Bunzip2) = 2.093
Provides: perl(IO::Uncompress::Gunzip) = 2.093
Provides: perl(IO::Uncompress::Inflate) = 2.093
Provides: perl(IO::Uncompress::RawInflate) = 2.093
Provides: perl(IO::Uncompress::Unzip) = 2.093
Provides: perl(IPC::Msg) = 2.07
Provides: perl(IPC::Open2) = 1.05
Provides: perl(IPC::Open3) = 1.21
Provides: perl(IPC::Semaphore) = 2.07
Provides: perl(IPC::SharedMem) = 2.07
Provides: perl(JSON::PP::Boolean) = 4.04
Provides: perl(List::Util) = 1.55
Provides: perl(List::Util::XS) = 1.55
Provides: perl(Locale::Maketext::Guts) = 1.20
Provides: perl(Locale::Maketext::GutsLoader) = 1.20
Provides: perl(MIME::QuotedPrint) = 3.13
Provides: perl(Math::BigFloat) = 1.999818
Provides: perl(Math::BigFloat::Trace) = 0.51
Provides: perl(Math::BigInt::Calc) = 1.999818
Provides: perl(Math::BigInt::Lib) = 1.999818
Provides: perl(Math::BigInt::Trace) = 0.51
Provides: perl(Math::Trig) = 1.23
Provides: perl(Memoize::AnyDBM_File) = 1.03
Provides: perl(Memoize::Expire) = 1.03
Provides: perl(Memoize::ExpireFile) = 1.03
Provides: perl(Memoize::ExpireTest) = 1.03
Provides: perl(Memoize::NDBM_File) = 1.03
Provides: perl(Memoize::SDBM_File) = 1.03
Provides: perl(Memoize::Storable) = 1.03
Provides: perl(Module::CoreList::Utils) = 5.20200620
Provides: perl(NDBM_File) = 1.15
Provides: perl(Net::Cmd) = 3.11
Provides: perl(Net::Config) = 3.11
Provides: perl(Net::Domain) = 3.11
Provides: perl(Net::FTP) = 3.11
Provides: perl(Net::FTP::A) = 3.11
Provides: perl(Net::FTP::E) = 3.11
Provides: perl(Net::FTP::I) = 3.11
Provides: perl(Net::FTP::L) = 3.11
Provides: perl(Net::FTP::dataconn) = 3.11
Provides: perl(Net::NNTP) = 3.11
Provides: perl(Net::Netrc) = 3.11
Provides: perl(Net::POP3) = 3.11
Provides: perl(Net::SMTP) = 3.11
Provides: perl(Net::Time) = 3.11
Provides: perl(Net::hostent) = 1.02
Provides: perl(Net::netent) = 1.01
Provides: perl(Net::protoent) = 1.01
Provides: perl(Net::servent) = 1.02
Provides: perl(O) = 1.03
Provides: perl(ODBM_File) = 1.16
Provides: perl(Opcode) = 1.47
Provides: perl(POSIX) = 1.94
Provides: perl(Parse::CPAN::Meta) = 2.150010
Provides: perl(PerlIO) = 1.11
Provides: perl(PerlIO::encoding) = 0.28
Provides: perl(PerlIO::mmap) = 0.016
Provides: perl(PerlIO::scalar) = 0.30
Provides: perl(PerlIO::via) = 0.18
# Pod::Find is no more provided
Provides: perl(Pod::Html) = 1.25
# Pod::InputObjects is no more provided
Provides: perl(Pod::Man) = 4.14
Provides: perl(Pod::ParseLink) = 4.14
# Pod::ParseUtils is no more provided
Provides: perl(Pod::Perldoc::BaseTo) = 3.28
Provides: perl(Pod::Perldoc::GetOptsOO) = 3.28
Provides: perl(Pod::Perldoc::ToANSI) = 3.28
Provides: perl(Pod::Perldoc::ToChecker) = 3.28
Provides: perl(Pod::Perldoc::ToMan) = 3.28
Provides: perl(Pod::Perldoc::ToNroff) = 3.28
Provides: perl(Pod::Perldoc::ToPod) = 3.28
Provides: perl(Pod::Perldoc::ToRtf) = 3.28
Provides: perl(Pod::Perldoc::ToTerm) = 3.28
Provides: perl(Pod::Perldoc::ToText) = 3.28
Provides: perl(Pod::Perldoc::ToTk) = 3.28
Provides: perl(Pod::Perldoc::ToXml) = 3.28
# Pod::PlainText is no more provided
# Pod::Select is no more provided
Provides: perl(Pod::Simple::BlackBox) = 3.40
Provides: perl(Pod::Simple::Checker) = 3.40
Provides: perl(Pod::Simple::Debug) = 3.40
Provides: perl(Pod::Simple::DumpAsText) = 3.40
Provides: perl(Pod::Simple::DumpAsXML) = 3.40
Provides: perl(Pod::Simple::HTML) = 3.40
Provides: perl(Pod::Simple::HTMLBatch) = 3.40
Provides: perl(Pod::Simple::HTMLLegacy) = 5.01
Provides: perl(Pod::Simple::JustPod) = 3.40
Provides: perl(Pod::Simple::LinkSection) = 3.40
Provides: perl(Pod::Simple::Methody) = 3.40
Provides: perl(Pod::Simple::Progress) = 3.40
Provides: perl(Pod::Simple::PullParser) = 3.40
Provides: perl(Pod::Simple::PullParserEndToken) = 3.40
Provides: perl(Pod::Simple::PullParserStartToken) = 3.40
Provides: perl(Pod::Simple::PullParserTextToken) = 3.40
Provides: perl(Pod::Simple::PullParserToken) = 3.40
Provides: perl(Pod::Simple::RTF) = 3.40
Provides: perl(Pod::Simple::Search) = 3.40
Provides: perl(Pod::Simple::SimpleTree) = 3.40
Provides: perl(Pod::Simple::Text) = 3.40
Provides: perl(Pod::Simple::TextContent) = 3.40
Provides: perl(Pod::Simple::TiedOutFH) = 3.40
Provides: perl(Pod::Simple::Transcode) = 3.40
Provides: perl(Pod::Simple::TranscodeDumb) = 3.40
Provides: perl(Pod::Simple::TranscodeSmart) = 3.40
Provides: perl(Pod::Simple::XHTML) = 3.40
Provides: perl(Pod::Simple::XMLOutStream) = 3.40
Provides: perl(Pod::Text) = 4.14
Provides: perl(Pod::Text::Color) = 4.14
Provides: perl(Pod::Text::Overstrike) = 4.14
Provides: perl(Pod::Text::Termcap) = 4.14
Provides: perl(SDBM_File) = 1.15
Provides: perl(Scalar::Util) = 1.55
Provides: perl(SelectSaver) = 1.02
Provides: perl(Sub::Util) = 1.55
Provides: perl(Symbol) = 1.08
Provides: perl(Sys::Hostname) = 1.23
Provides: perl(TAP::Base) = 3.42
Provides: perl(TAP::Formatter::Base) = 3.42
Provides: perl(TAP::Formatter::Color) = 3.42
Provides: perl(TAP::Formatter::Console) = 3.42
Provides: perl(TAP::Formatter::Console::ParallelSession) = 3.42
Provides: perl(TAP::Formatter::Console::Session) = 3.42
Provides: perl(TAP::Formatter::File) = 3.42
Provides: perl(TAP::Formatter::File::Session) = 3.42
Provides: perl(TAP::Formatter::Session) = 3.42
Provides: perl(TAP::Harness) = 3.42
Provides: perl(TAP::Harness::Env) = 3.42
Provides: perl(TAP::Object) = 3.42
Provides: perl(TAP::Parser) = 3.42
Provides: perl(TAP::Parser::Aggregator) = 3.42
Provides: perl(TAP::Parser::Grammar) = 3.42
Provides: perl(TAP::Parser::Iterator) = 3.42
Provides: perl(TAP::Parser::Iterator::Array) = 3.42
Provides: perl(TAP::Parser::Iterator::Process) = 3.42
Provides: perl(TAP::Parser::Iterator::Stream) = 3.42
Provides: perl(TAP::Parser::IteratorFactory) = 3.42
Provides: perl(TAP::Parser::Multiplexer) = 3.42
Provides: perl(TAP::Parser::Result) = 3.42
Provides: perl(TAP::Parser::Result::Bailout) = 3.42
Provides: perl(TAP::Parser::Result::Comment) = 3.42
Provides: perl(TAP::Parser::Result::Plan) = 3.42
Provides: perl(TAP::Parser::Result::Pragma) = 3.42
Provides: perl(TAP::Parser::Result::Test) = 3.42
Provides: perl(TAP::Parser::Result::Unknown) = 3.42
Provides: perl(TAP::Parser::Result::Version) = 3.42
Provides: perl(TAP::Parser::Result::YAML) = 3.42
Provides: perl(TAP::Parser::ResultFactory) = 3.42
Provides: perl(TAP::Parser::Scheduler) = 3.42
Provides: perl(TAP::Parser::Scheduler::Job) = 3.42
Provides: perl(TAP::Parser::Scheduler::Spinner) = 3.42
Provides: perl(TAP::Parser::Source) = 3.42
Provides: perl(TAP::Parser::SourceHandler) = 3.42
Provides: perl(TAP::Parser::SourceHandler::Executable) = 3.42
Provides: perl(TAP::Parser::SourceHandler::File) = 3.42
Provides: perl(TAP::Parser::SourceHandler::Handle) = 3.42
Provides: perl(TAP::Parser::SourceHandler::Perl) = 3.42
Provides: perl(TAP::Parser::SourceHandler::RawTAP) = 3.42
Provides: perl(TAP::Parser::YAMLish::Reader) = 3.42
Provides: perl(TAP::Parser::YAMLish::Writer) = 3.42
Provides: perl(Test2) = 1.302175
Provides: perl(Test2::API) = 1.302175
Provides: perl(Test2::API::Breakage) = 1.302175
Provides: perl(Test2::API::Context) = 1.302175
Provides: perl(Test2::API::Instance) = 1.302175
Provides: perl(Test2::API::Stack) = 1.302175
Provides: perl(Test2::Event) = 1.302175
Provides: perl(Test2::Event::Bail) = 1.302175
Provides: perl(Test2::Event::Diag) = 1.302175
Provides: perl(Test2::Event::Encoding) = 1.302175
Provides: perl(Test2::Event::Exception) = 1.302175
Provides: perl(Test2::Event::Fail) = 1.302175
Provides: perl(Test2::Event::Generic) = 1.302175
Provides: perl(Test2::Event::Note) = 1.302175
Provides: perl(Test2::Event::Ok) = 1.302175
Provides: perl(Test2::Event::Pass) = 1.302175
Provides: perl(Test2::Event::Plan) = 1.302175
Provides: perl(Test2::Event::Skip) = 1.302175
Provides: perl(Test2::Event::Subtest) = 1.302175
Provides: perl(Test2::Event::TAP::Version) = 1.302175
Provides: perl(Test2::Event::V2) = 1.302175
Provides: perl(Test2::Event::Waiting) = 1.302175
Provides: perl(Test2::EventFacet) = 1.302175
Provides: perl(Test2::EventFacet::About) = 1.302175
Provides: perl(Test2::EventFacet::Amnesty) = 1.302175
Provides: perl(Test2::EventFacet::Assert) = 1.302175
Provides: perl(Test2::EventFacet::Control) = 1.302175
Provides: perl(Test2::EventFacet::Error) = 1.302175
Provides: perl(Test2::EventFacet::Hub) = 1.302175
Provides: perl(Test2::EventFacet::Info) = 1.302175
Provides: perl(Test2::EventFacet::Info::Table) = 1.302175
Provides: perl(Test2::EventFacet::Meta) = 1.302175
Provides: perl(Test2::EventFacet::Parent) = 1.302175
Provides: perl(Test2::EventFacet::Plan) = 1.302175
Provides: perl(Test2::EventFacet::Render) = 1.302175
Provides: perl(Test2::EventFacet::Trace) = 1.302175
Provides: perl(Test2::Formatter) = 1.302175
Provides: perl(Test2::Formatter::TAP) = 1.302175
Provides: perl(Test2::Hub) = 1.302175
Provides: perl(Test2::Hub::Interceptor) = 1.302175
Provides: perl(Test2::Hub::Interceptor::Terminator) = 1.302175
Provides: perl(Test2::Hub::Subtest) = 1.302175
Provides: perl(Test2::IPC) = 1.302175
Provides: perl(Test2::IPC::Driver) = 1.302175
Provides: perl(Test2::IPC::Driver::Files) = 1.302175
Provides: perl(Test2::Tools::Tiny) = 1.302175
Provides: perl(Test2::Util) = 1.302175
Provides: perl(Test2::Util::ExternalMeta) = 1.302175
Provides: perl(Test2::Util::Facets2Legacy) = 1.302175
Provides: perl(Test2::Util::HashBase) = 1.302175
Provides: perl(Test2::Util::Trace) = 1.302175
Provides: perl(Test::Builder) = 1.302175
Provides: perl(Test::Builder::Formatter) = 1.302175
Provides: perl(Test::Builder::IO::Scalar) = 2.114
Provides: perl(Test::Builder::Module) = 1.302175
Provides: perl(Test::Builder::Tester) = 1.302175
Provides: perl(Test::Builder::Tester::Color) = 1.302175
Provides: perl(Test::Builder::TodoDiag) = 1.302175
Provides: perl(Test::More) = 1.302175
Provides: perl(Test::Tester) = 1.302175
Provides: perl(Test::Tester::Capture) = 1.302175
Provides: perl(Test::Tester::CaptureRunner) = 1.302175
Provides: perl(Test::Tester::Delegate) = 1.302175
Provides: perl(Test::use::ok) = 1.302175
Provides: perl(Text::Tabs) = 2013.0523
Provides: perl(Text::Wrap) = 2013.0523
Provides: perl(Thread) = 3.05
Provides: perl(Tie::Array) = 1.07
Provides: perl(Tie::Handle) = 4.2
Provides: perl(Tie::Hash) = 1.05
Provides: perl(Tie::Hash::NamedCapture) = 0.13
Provides: perl(Tie::Memoize) = 1.1
Provides: perl(Tie::Scalar) = 1.05
Provides: perl(Tie::StdHandle) = 4.6
Provides: perl(Tie::SubstrHash) = 1.00
Provides: perl(Time::Seconds) = 1.3401
Provides: perl(Time::gmtime) = 1.04
Provides: perl(Time::localtime) = 1.03
Provides: perl(Time::tm) = 1.00
Provides: perl(UNIVERSAL) = 1.13
Provides: perl(Unicode::Collate::CJK::Big5) = 1.27
Provides: perl(Unicode::Collate::CJK::GB2312) = 1.27
Provides: perl(Unicode::Collate::CJK::JISX0208) = 1.27
Provides: perl(Unicode::Collate::CJK::Korean) = 1.27
Provides: perl(Unicode::Collate::CJK::Pinyin) = 1.27
Provides: perl(Unicode::Collate::CJK::Stroke) = 1.27
Provides: perl(Unicode::Collate::CJK::Zhuyin) = 1.27
Provides: perl(Unicode::Collate::Locale) = 1.27
Provides: perl(Unicode::UCD) = 0.75
Provides: perl(User::grent) = 1.03
Provides: perl(User::pwent) = 1.01
Provides: perl(attributes) = 0.33
Provides: perl(autodie::Scope::Guard) = 2.32
Provides: perl(autodie::Scope::GuardStack) = 2.32
Provides: perl(autodie::Util) = 2.32
Provides: perl(autodie::exception) = 2.32
Provides: perl(autodie::exception::system) = 2.32
Provides: perl(autodie::hints) = 2.32
Provides: perl(autodie::skip) = 2.32
Provides: perl(bigint) = 0.51
Provides: perl(bigrat) = 0.51
Provides: perl(blib) = 1.07
Provides: perl(bytes) = 1.07
Provides: perl(charnames) = 1.48
Provides: perl(deprecate) = 0.04
Provides: perl(diagnostics) = 1.37
Provides: perl(encoding) = 3.00
Provides: perl(feature) = 1.58
Provides: perl(fields) = 2.24
Provides: perl(filetest) = 1.03
Provides: perl(integer) = 1.01
Provides: perl(less) = 0.03
Provides: perl(locale) = 1.09
Provides: perl(mro) = 1.23
Provides: perl(ok) = 1.302175
Provides: perl(open) = 1.12
Provides: perl(ops) = 1.02
Provides: perl(overload) = 1.31
Provides: perl(overload::numbers)
Provides: perl(overloading) = 0.02
Provides: perl(re) = 0.40
Provides: perl(sigtrap) = 1.09
Provides: perl(sort) = 2.04
Provides: perl(strict) = 1.11
Provides: perl(subs) = 1.03
Provides: perl(utf8) = 1.22
Provides: perl(vars) = 1.05
Provides: perl(version::regex) = 0.9924
Provides: perl(vmsish) = 1.04
Provides: perl(warnings) = 1.47
Provides: perl(warnings::register) = 1.04

# Provides for non *.pm files
Provides: perl(abbrev.pl) 
Provides: perl(assert.pl) 
Provides: perl(bigfloat.pl) 
Provides: perl(bigint.pl) 
Provides: perl(bigrat.pl) 
Provides: perl(bytes_heavy.pl) 
Provides: perl(cacheout.pl) 
Provides: perl(complete.pl) 
Provides: perl(ctime.pl) 
Provides: perl(dotsh.pl) 
Provides: perl(dumpvar.pl) 
Provides: perl(exceptions.pl) 
Provides: perl(fastcwd.pl) 
Provides: perl(find.pl) 
Provides: perl(finddepth.pl) 
Provides: perl(flush.pl) 
Provides: perl(ftp.pl) 
Provides: perl(getcwd.pl) 
Provides: perl(getopt.pl) 
Provides: perl(getopts.pl) 
Provides: perl(hostname.pl) 
Provides: perl(importenv.pl) 
Provides: perl(look.pl) 
Provides: perl(newgetopt.pl) 
Provides: perl(open2.pl) 
Provides: perl(open3.pl) 
Provides: perl(perl5db.pl) 
Provides: perl(pwd.pl) 
Provides: perl(shellwords.pl) 
Provides: perl(stat.pl) 
Provides: perl(syslog.pl) 
Provides: perl(tainted.pl) 
Provides: perl(termcap.pl) 
Provides: perl(timelocal.pl) 
Provides: perl(utf8_heavy.pl) 
Provides: perl(validate.pl) 
#
# These modules appear to be missing or break assumptions made by the
# dependency analysis tools.  Typical problems include refering to
# CGI::Apache as Apache and having no package line in CPAN::Nox.pm. I
# hope that the perl people fix these to work with our dependency
# engine or give us better dependency tools.
#
Provides: perl(Apache)
Provides: perl(ExtUtils::MM_Mac)
Provides: perl(ExtUtils::XSSymSet)
Provides: perl(FCGI)
Provides: perl(LWP::UserAgent)
Provides: perl(Mac::Files)
Provides: perl(URI::URL)
Provides: perl(VMS::Filespec)
Provides: B.so
Provides: Base64.so
Provides: Byte.so
Provides: Bzip2.so
Provides: CN.so
Provides: Call.so
Provides: Collate.so
Provides: Cwd.so
Provides: DB_File.so
Provides: DosGlob.so
Provides: Dumper.so
Provides: EBCDIC.so
Provides: Encode.so
Provides: FastCalc.so
Provides: Fcntl.so
Provides: FieldHash.so
Provides: GDBM_File.so
Provides: Glob.so
Provides: HiRes.so
Provides: Hostname.so
Provides: IO.so
Provides: JP.so
Provides: KR.so
Provides: Langinfo.so
Provides: MD5.so
Provides: NDBM_File.so
Provides: NamedCapture.so
Provides: Normalize.so
Provides: ODBM_File.so
Provides: Opcode.so
Provides: POSIX.so
Provides: Peek.so
Provides: Piece.so
Provides: SDBM_File.so
Provides: SHA.so
Provides: Socket.so
Provides: Storable.so
Provides: Symbol.so
Provides: SysV.so
Provides: Syslog.so
Provides: TW.so
Provides: Unicode.so
Provides: Util.so
Provides: Zlib.so
Provides: arybase.so
Provides: attributes.so
Provides: encoding.so
Provides: libperl.a(libperl.o)
Provides: libperl.o
Provides: mmap.so
Provides: mro.so
Provides: re.so
Provides: scalar.so
Provides: shared.so
Provides: threads.so
Provides: via.so

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

%prep
# export PATH=/opt/freeware/bin:$PATH

%setup -q
# %patch0

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


echo "BUILD ENVIRONMENT:"
/usr/bin/env | /usr/bin/sort | grep -v _proxy | grep -v SSH_

ulimit -a
ulimit -d unlimited
# ulimit -s unlimited
ulimit -m unlimited
ulimit -a

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


# build 32bit mode

(
  cd 32bit
  export OBJECT_MODE=32
  export LIBS32="-L/opt/freeware/lib -L/usr/lib"
  export CFLAGS="${CFLAGS32} ${LIBS32}"
  export CXXFLAGS="${CFLAGS}"

  export LDFLAGS32="-Wl,-b32"
  export LDFLAGS32="$LDFLAGS32 -Wl,$LIBS32"
  export LDFLAGS32="$LDFLAGS32 -Wl,-blibpath:%{archlibpath32}CORE:%{_libdir}:/usr/lib:/lib"
  export LDFLAGS32="$LDFLAGS32 -Wl,-bmaxdata:0x80000000"
  export LDFLAGS="$LDFLAGS3264 $LDFLAGS32"

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
  export LIBS64="-L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib -L/usr/lib"
  export CFLAGS="${CFLAGS64} ${LIBS64}"
  export CXXFLAGS="${CFLAGS}"
  
  #perl ld
  export LDFLAGS64="-Wl,-b64"
  export LDFLAGS64="$LDFLAGS64 -Wl,$LIBS64"
  export LDFLAGS64="$LDFLAGS64 -Wl,-blibpath:%{archlibpath64}CORE:%{archlibpath32}CORE:%{_libdir64}:%{_libdir}:/usr/lib:/lib"
  #no -bmaxdata for 64bit
  export LDFLAGS="$LDFLAGS3264 $LDFLAGS64"

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

# a2p is no longer in the Perl core
# find2perl, s2p and a2p are now separate CPAN packages
# (App-find2perl, App-s2p, App-a2p)

(
   cd  ${RPM_BUILD_ROOT}/%{_bindir}
   for f in perl perl%{version}
   do
       mv ${f} ${f}_64
   done

)
cd ..

#Install on 32bit mode
cd 32bit
#$MAKE install 
$MAKE DESTDIR=${RPM_BUILD_ROOT} install 

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for f in perl perl%{version}
    do
        mv ${f} ${f}_32
#       /usr/bin/strip ${f}_32 || :
        ln -sf ${f}_%{default_bits} ${f}
    done
)

cd ..

# Create (empty) vendor_perl libs
mkdir -p ${RPM_BUILD_ROOT}%{vendorlibpath}
mkdir -p ${RPM_BUILD_ROOT}%{vendorarchpath32}
mkdir -p ${RPM_BUILD_ROOT}%{vendorarchpath64}

# Useless for Perl 5.26
## Patch Config_heavy.pl to remove $RPM_BUILD_ROOT from -bE:  "-e ldopts" output
## In previous versions this was not explicitly necessary, may be covered by
## an earlier catch or under case os == aix
## Add another sed for removing $RPM_BUILD_ROOT (/var/opt/freeware/tmp/perl-root)
#
#mv ${RPM_BUILD_ROOT}%{vendorarchpath64}/Config_heavy.pl ${RPM_BUILD_ROOT}%{vendorarchpath64}/copy.Config_heavy.pl.copy
#
#cat ${RPM_BUILD_ROOT}%{vendorarchpath64}/copy.Config_heavy.pl.copy \
#	| sed -e 's@-bE:.*tmp/perl-root@-bE:@' \
#	| sed -e "s|$RPM_BUILD_ROOT||g" \
#> ${RPM_BUILD_ROOT}%{vendorarchpath64}/Config_heavy.pl
#
#rm ${RPM_BUILD_ROOT}%{vendorarchpath64}/copy.Config_heavy.pl.copy
#
#mv ${RPM_BUILD_ROOT}%{vendorarchpath32}/Config_heavy.pl ${RPM_BUILD_ROOT}%{vendorarchpath32}/copy.Config_heavy.pl.copy
#
#cat ${RPM_BUILD_ROOT}%{vendorarchpath32}/copy.Config_heavy.pl.copy \
#	| sed -e 's@-bE:.*tmp/perl-root@-bE:@' \
#	| sed -e "s|$RPM_BUILD_ROOT||g" \
#> ${RPM_BUILD_ROOT}%{vendorarchpath32}/Config_heavy.pl
#
#rm ${RPM_BUILD_ROOT}%{vendorarchpath32}/copy.Config_heavy.pl.copy
#

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
PERL	= PERL5LIB=\$(PERLLIB) LIBPATH=\$(RPM_BUILD_ROOT)%{archlibpath64}CORE:%{_libdir}:/usr/lib \$(RPM_BUILD_ROOT)%{_bindir}/perl_64
PHDIR   = \$(RPM_BUILD_ROOT)%{archlibpath64}/
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph -d \$(PHDIR)/

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
PERL	= PERL5LIB=\$(PERLLIB) LIBPATH=\$(RPM_BUILD_ROOT)%{archlibpath32}CORE:%{_libdir}:/usr/lib \$(RPM_BUILD_ROOT)%{_bindir}/perl_32
PHDIR   = \$(RPM_BUILD_ROOT)%{archlibpath32}/
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph -d \$(PHDIR)/

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
 #binaries files are already stripped
 #for f in perl perl%{version}
 #do
 #    /usr/bin/strip .%{prefix}/bin/${f}
 #done

 mvdir .%{prefix}/share/man .%{prefix}/man
 # The Thread.3 manpage duplicates the same file in the tcl package.
 rm .%{prefix}/man/man3/Thread.3
 
 # Replace 64 bits libperl.a by a link to the 32 bit (containing both .so).
 rm -f .%{archlibpath64}CORE/libperl.a
 ln -s %{archlibpath32}CORE/libperl.a ${RPM_BUILD_ROOT}%{archlibpath64}CORE/libperl.a
)

# useless in 5.26.2 : fix the rest of the stuff
#find $RPM_BUILD_ROOT%{_libdir}/perl* -name .packlist -o -name perllocal.pod | \
#xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist

%check
# For 64 bits tests.
# ulimit -s unlimited
# ulimit -f unlimited
ulimit -d unlimited

export PATH=/opt/freeware/bin:$PATH
export MAKE="gmake"
export AR="/usr/bin/ar"
export ARFLAGS="-X32_64"

%if %{with dotests}
cd 32bit
export OBJECT_MODE=32
( $MAKE  --trace --print-directory -k check || true )
/usr/sbin/slibclean
cd ../64bit
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
%{_libdir64}/perl5/*
%exclude %{archlibpath64}/CORE/libperl_nonshr.a
%{_datadir}/perl5/*
%{_mandir}/*/*


%changelog
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
