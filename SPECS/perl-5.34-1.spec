# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define major_version 5
%define minor_version 34

%define perlver %{major_version}.%{minor_version}

%define macro_location /usr/opt/rpm/lib/rpm/macros.d

Summary: The Perl programming language.
Name: perl
Epoch: 1
Version: %{major_version}.%{minor_version}
Release: 1
License: Artistic
URL: http://www.perl.com
Group: Development/Languages
Source1:  macros.perl
Source10: %{name}-%{version}-%{release}.build.log

Requires: perl%{perlver}

# ----- Perl module provides.
Provides: perl(perl) = %{perlver}

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


%package db
Summary: Perl DB module.

Requires: perl = %{epoch}:%{version}-%{release}
Requires: perl%{version}-db

%description db
This package contains perl module to work with
Berkeley DB.


%prep

%build

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_bindir}

cd $RPM_BUILD_ROOT%{_bindir}
for bin in corelist cpan enc2xs encguess h2ph h2xs instmodsh json_pp libnetcfg \
    perl perlbug perldoc perlivp perlthanks piconv pl2pm pod2html pod2man \
    pod2text pod2usage podchecker prove ptar ptardiff ptargrep shasum splain \
    streamzip xsubpp zipdetails
do
    ln -s ${bin}%{version} ${bin}
done

# Install macros
mkdir -p ${RPM_BUILD_ROOT}%{macro_location}
cp %SOURCE1 ${RPM_BUILD_ROOT}%{macro_location}

%check
%if %{with dotests}
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_bindir}/*
%{macro_location}/macros.perl

%files db

%changelog
* Tue Oct 12 2021 Etienne Guesnet <etienne.guesnet@atos.net> 5.34-1
- Creation of metapackage
- perl 32 bits is ghosted
