Summary: The Perl programming language.
Name: perl
%define perlver 5.22.0
Version: %{perlver}
Release: 2
License: Artistic
URL: http://www.perl.com
Group: Development/Languages
Source0: http://www.perl.com/CPAN/src/perl-%{perlver}.tar.gz
Source10: %{name}-%{version}-%{release}.build.log
Buildroot: %{_tmppath}/%{name}-root
Prefix: %{_prefix}
BuildRequires: gdbm-devel >= 1.10
Requires: gdbm >= 1.10
Epoch: 1

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%define osplat aix7
%endif

# ----- Perl module provides.
Provides: perl(AnyDBM_File) = 1.01
Provides: perl(App::Cpan) = 1.63
Provides: perl(App::Prove) = 3.35
Provides: perl(App::Prove::State) = 3.35
Provides: perl(App::Prove::State::Result) = 3.35
Provides: perl(App::Prove::State::Result::Test) = 3.35
Provides: perl(Archive::Tar) = 2.04
Provides: perl(Archive::Tar::Constant) = 2.04
Provides: perl(Archive::Tar::File) = 2.04
Provides: perl(Attribute::Handlers) = 0.97
Provides: perl(AutoLoader) = 5.74
Provides: perl(AutoSplit) = 1.06
Provides: perl(B) = 1.58
# Provides: perl(B::Asmdata)
# Provides: perl(B::Assembler) = 0.04
# Provides: perl(B::Bblock)
# Provides: perl(B::Bytecode)
# Provides: perl(B::C)
# Provides: perl(B::C::InitSection)
# Provides: perl(B::C::Section)
# Provides: perl(B::CC)
Provides: perl(B::Concise) = 0.996
Provides: perl(B::Debug) = 1.23
Provides: perl(B::Deparse) = 1.35
# Provides: perl(B::Disassembler)
# Provides: perl(B::Disassembler::BytecodeStream)
# Provides: perl(B::Lint)
Provides: perl(B::OBJECT) = 1.58
Provides: perl(B::Op_private) = 5.022000
# Provides: perl(B::Pseudoreg)
Provides: perl(B::Section) = 1.58
# Provides: perl(B::Shadow)
Provides: perl(B::Showlex) = 1.05
# Provides: perl(B::Stackobj)
# Provides: perl(B::Stash)
Provides: perl(B::Terse) = 1.06
Provides: perl(B::Xref) = 1.05
Provides: perl(Benchmark) = 1.20
# Provides: perl(ByteLoader) = 0.04
# Provides: perl(CGI)
# Provides: perl(CGI::Carp)
# Provides: perl(CGI::Cookie)
# Provides: perl(CGI::Fast)
# Provides: perl(CGI::Pretty)
# Provides: perl(CGI::Push)
# Provides: perl(CGI::Util) = 1.3
# Provides: perl(CGITempFile)
Provides: perl(CPAN) = 2.11
Provides: perl(CPAN::Author) = 5.5002
Provides: perl(CPAN::Bundle) = 5.5001
Provides: perl(CPAN::CacheMgr) = 5.5002
Provides: perl(CPAN::Complete) = 5.5001
# Provides: perl(CPAN::Config) --> see HandleConfig
Provides: perl(CPAN::Debug) = 5.5001
Provides: perl(CPAN::DeferredCode) = 5.50
Provides: perl(CPAN::Distribution) = 2.04
Provides: perl(CPAN::Distroprefs) = 6.0001
Provides: perl(CPAN::Distroprefs::Iterator)
Provides: perl(CPAN::Distroprefs::Pref)
Provides: perl(CPAN::Distroprefs::Result)
Provides: perl(CPAN::Distroprefs::Result::Error)
Provides: perl(CPAN::Distroprefs::Result::Warning)
Provides: perl(CPAN::Distroprefs::Result::Fatal)
Provides: perl(CPAN::Distroprefs::Result::Success)
Provides: perl(CPAN::Distrostatus) = 5.5
Provides: perl(CPAN::Exception::RecursiveDependency) = 5.5
Provides: perl(CPAN::Exception::blocked_urllist) = 5.5
Provides: perl(CPAN::Exception::yaml_not_installed) = 5.5
Provides: perl(CPAN::Exception::yaml_process_error) = 5.5
# Provides: perl(CPAN::Eval)
Provides: perl(CPAN::FTP) = 5.5006
Provides: perl(CPAN::FTP::netrc) = 1.01
Provides: perl(CPAN::FirstTime) = 5.5307
Provides: perl(CPAN::HTTP::Client) = 1.9601
Provides: perl(CPAN::HTTP::Credentials) = 1.9601
Provides: perl(CPAN::HandleConfig) = 5.5006
Provides: perl(CPAN::Index) = 1.9601
Provides: perl(CPAN::InfoObj) = 5.5
Provides: perl(CPAN::Kwalify) = 5.50
Provides: perl(CPAN::LWP::UserAgent) = 1.9601
Provides: perl(CPAN::Meta) = 2.150001
Provides: perl(CPAN::Meta::Converter) = 2.150001
Provides: perl(CPAN::Meta::Feature) = 2.150001
Provides: perl(CPAN::Meta::History) = 2.150001
Provides: perl(CPAN::Meta::Merge) = 2.150001
Provides: perl(CPAN::Meta::Prereqs) = 2.150001
Provides: perl(CPAN::Meta::Requirements) = 2.132
Provides: perl(CPAN::Meta::Spec) = 2.150001
Provides: perl(CPAN::Meta::Validator) = 2.150001
Provides: perl(CPAN::Meta::YAML) = 0.012
Provides: perl(CPAN::Mirrored) = 1.9601
Provides: perl(CPAN::Mirrored::By)
Provides: perl(CPAN::Module) = 5.5002
Provides: perl(CPAN::Nox) = 5.5001
Provides: perl(CPAN::Plugin) = 0.95
Provides: perl(CPAN::Plugin::Specfile) = 0.01
Provides: perl(CPAN::Prompt) = 5.5
Provides: perl(CPAN::Queue) = 5.5002
Provides: perl(CPAN::Shell) = 5.5005
Provides: perl(CPAN::Tarzip) = 5.5012
Provides: perl(CPAN::URL) = 5.5
Provides: perl(CPAN::Version) = 5.5003
Provides: perl(Carp) = 1.36
Provides: perl(Carp::Heavy) = 1.36
Provides: perl(Class::Struct) = 0.65
Provides: perl(Class::ISA)
Provides: perl(Class::Struct::Tie_ISA)
Provides: perl(Compress::Raw::Bzip2) = 2.068
Provides: perl(Compress::Raw::Zlib) = 2.068
Provides: perl(Compress::Zlib) = 2.068
Provides: perl(Zlib::OldDeflate)
Provides: perl(Zlib::OldInflate)
Provides: perl(Config) = 5.022000
Provides: perl(Config::Extensions) = 0.01
Provides: perl(Config::Perl::V) = 0.24
Provides: perl(Cwd) = 3.56
# Provides: perl(DB) = 1.08 -- VERSION in DB.pm, following is in perl5db.pl
Provides: perl(DB) = 1.49
Provides: perl(DB::Obj) = 1.49
Provides: perl(DB::fake) = 1.49
Provides: perl(DB_File) = 1.835
Provides: perl(DB_File::BTREEINFO)
Provides: perl(DB_File::HASHINFO)
Provides: perl(DB_File::RECNOINFO)
Provides: perl(DBM_Filter) = 0.06
Provides: perl(DBM_Filter::compress) = 0.03
Provides: perl(DBM_Filter::encode) = 0.03
Provides: perl(DBM_Filter::int32) = 0.03
Provides: perl(DBM_Filter::null) = 0.03
Provides: perl(DBM_Filter::utf8) = 0.03
Provides: perl(Data::Dumper) = 2.158
# Provides: perl(Demo) = 1.00
# Provides: perl(Descriptions) = 1.00
# Provides: perl(Devel::DProf)
Provides: perl(Devel::PPPort) = 3.31
Provides: perl(Devel::Peek) = 1.22
Provides: perl(Devel::SelfStubber) = 1.05
Provides: perl(Digest) = 1.17
Provides: perl(Digest::MD5) = 2.54
Provides: perl(Digest::SHA) = 5.95
Provides: perl(Digest::base) = 1.16
Provides: perl(Digest::file) = 1.16
Provides: perl(DirHandle) = 1.04
Provides: perl(Dumpvalue) = 1.17
Provides: perl(DynaLoader) = 1.32
Provides: perl(EVERY) = 0.65
Provides: perl(EVERY::LAST) = 0.65
Provides: perl(Encode) = 2.72
Provides: perl(Encode::Alias) = 2.19
Provides: perl(Encode::Byte) = 2.4
Provides: perl(Encode::CJKConstants) = 2.2
Provides: perl(Encode::CN) = 2.3
Provides: perl(Encode::CN::HZ) = 2.7
Provides: perl(Encode::Config) = 2.5
Provides: perl(Encode::EBCDIC) = 2.2
Provides: perl(Encode::Encoder) = 2.3
Provides: perl(Encode::Encoding) = 2.7
Provides: perl(Encode::GSM0338) = 2.5
Provides: perl(Encode::Guess) = 2.6
Provides: perl(Encode::Internal) = 2.72
Provides: perl(Encode::JP) = 2.4
Provides: perl(Encode::JP::H2Z) = 2.2
Provides: perl(Encode::JP::JIS7) = 2.5
Provides: perl(Encode::KR) = 2.3
Provides: perl(Encode::KR::2022_KR) = 2.3
Provides: perl(Encode::MIME::Header) = 2.16
Provides: perl(Encode::MIME::Name) = 1.1
Provides: perl(Encode::Symbol) = 2.2
Provides: perl(Encode::TW) = 2.3
Provides: perl(Encode::UTF_EBCDIC) = 2.72
Provides: perl(Encode::Unicode) = 2.9
Provides: perl(Encode::Unicode::UTF7) = 2.8
Provides: perl(Encode::utf8) = 2.72
Provides: perl(English) = 1.09
Provides: perl(Env) = 1.04
Provides: perl(Env::Array) = 1.04
Provides: perl(Env::Array::VMS) = 1.04
Provides: perl(Errno) = 1.23
Provides: perl(Exporter) = 5.72
Provides: perl(Exporter::Heavy) = 5.72
Provides: perl(ExtUtils::CBuilder) = 0.280221
Provides: perl(ExtUtils::CBuilder::Base) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::Unix) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::VMS) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::Windows::BCC) = 0.280221
Provides: perl(ExtUtils:::CBuilder::Platform::Windows::GCC) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::Windows::MSVC) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::Windows) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::aix) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::android) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::cygwin) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::darwin) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::dec_osf) = 0.280221
Provides: perl(ExtUtils::CBuilder::Platform::os2) = 0.280221
Provides: perl(ExtUtils::Command) = 1.20
Provides: perl(ExtUtils::Command::MM) = 7.04_01
Provides: perl(ExtUtils::Constant) = 0.23
Provides: perl(ExtUtils::Constant::Base) = 0.05
Provides: perl(ExtUtils::Constant::ProxySubs) = 0.08
Provides: perl(ExtUtils::Constant::Utils) = 0.03
Provides: perl(ExtUtils::Constant::XS) = 0.03
Provides: perl(ExtUtils::Embed) = 1.32
Provides: perl(ExtUtils::Install) = 2.04
Provides: perl(ExtUtils::Install::Warn) = 2.04
Provides: perl(ExtUtils::Installed) = 2.04
Provides: perl(ExtUtils::Liblist) = 7.04_01
Provides: perl(ExtUtils::Liblist::Kid) = 7.04_01
Provides: perl(ExtUtils::MM) = 7.04_01
Provides: perl(ExtUtils::MM_AIX) = 7.04_01
Provides: perl(ExtUtils::MM_Any) = 7.04_01
Provides: perl(ExtUtils::MM_BeOS) = 7.04_01
Provides: perl(ExtUtils::MM_Cygwin) = 7.04_01
Provides: perl(ExtUtils::MM_DOS) = 7.04_01
Provides: perl(ExtUtils::MM_Darwin) = 7.04_01
Provides: perl(ExtUtils::MM_MacOS) = 7.04_01
Provides: perl(ExtUtils::MM_NW5) = 7.04_01
Provides: perl(ExtUtils::MM_OS2) = 7.04_01
Provides: perl(ExtUtils::MM_QNX) = 7.04_01
Provides: perl(ExtUtils::MM_UWIN) = 7.04_01
Provides: perl(ExtUtils::MM_Unix) = 7.04_01
Provides: perl(ExtUtils::MM_VMS) = 7.04_01
Provides: perl(ExtUtils::MM_VOS) = 7.04_01
Provides: perl(ExtUtils::MM_Win32) = 7.04_01
Provides: perl(ExtUtils::MM_Win95) = 7.04_01
Provides: perl(ExtUtils::MY) = 7.04_01
Provides: perl(ExtUtils::MakeMaker) = 6.03
# Provides: perl(ExtUtils::MakeMaker::_version)
Provides: perl(ExtUtils::MakeMaker::Config) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::FAQ) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::Locale) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::Tutorial) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::charstar) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::version) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::version::regex) = 7.04_01
Provides: perl(ExtUtils::MakeMaker::version::vpp) = 7.04_01
Provides: perl(ExtUtils::Manifest) = 1.70
Provides: perl(ExtUtils::Miniperl) = 1.05
Provides: perl(ExtUtils::Mkbootstrap) = 7.04_01
Provides: perl(ExtUtils::Mksymlists) = 7.04_01
Provides: perl(ExtUtils::Packlist) = 2.04
Provides: perl(ExtUtils::ParseXS) = 3.28
Provides: perl(ExtUtils::ParseXS::Constants) = 3.28
Provides: perl(ExtUtils::ParseXS::CountLines) = 3.28
Provides: perl(ExtUtils::ParseXS::Eval) = 3.28
Provides: perl(ExtUtils::ParseXS::Utilities) = 3.28
Provides: perl(ExtUtils::Typemaps) = 3.28
Provides: perl(ExtUtils::Typemaps::Cmd) = 3.28
Provides: perl(ExtUtils::Typemaps::InputMap) = 3.28
Provides: perl(ExtUtils::Typemaps::OutputMap) = 3.28
Provides: perl(ExtUtils::Typemaps::Type) = 3.28
Provides: perl(ExtUtils::testlib) = 7.04_01
Provides: perl(Fatal) = 2.26
Provides: perl(Fcntl) = 1.13
# Provides: perl(Fh)
Provides: perl(File::Basename) = 2.85
# Provides: perl(File::CheckTree)
Provides: perl(File::Compare) = 1.1006
Provides: perl(File::Copy) = 2.30
Provides: perl(File::DosGlob) = 1.12
Provides: perl(File::Fetch) = 0.48
Provides: perl(File::Find) = 1.29
Provides: perl(File::Glob) = 1.24
Provides: perl(File::GlobMapper) = 1.000
Provides: perl(File::Path) = 2.09
Provides: perl(File::Spec) = 0.83
Provides: perl(File::Spec::Cygwin) = 3.56
Provides: perl(File::Spec::Epoc) = 3.56
Provides: perl(File::Spec::Functions) = 3.56
Provides: perl(File::Spec::Mac) = 3.56
Provides: perl(File::Spec::OS2) = 3.56
Provides: perl(File::Spec::Unix) = 3.56
Provides: perl(File::Spec::VMS) = 3.56
Provides: perl(File::Spec::Win32) = 3.56
Provides: perl(File::Temp) = 0.2304
Provides: perl(File::Temp::Dir) = 0.2304
Provides: perl(File::stat) = 1.07
Provides: perl(FileCache) = 1.09
Provides: perl(FileHandle) = 2.02
Provides: perl(Filter::Simple) = 0.92
Provides: perl(Filter::Util::Call) = 1.54
Provides: perl(FindBin) = 1.51
# Provides: perl(GDBM_File) = 1.06
Provides: perl(Getopt::Long) = 2.45
Provides: perl(Getopt::Long::Parser) = 2.45
Provides: perl(Getopt::Long::CallBack) = 2.45
Provides: perl(Getopt::Std) = 1.11
Provides: perl(HTTP::Tiny) = 0.054
Provides: perl(Hash::Util) = 0.18
Provides: perl(Hash::Util::FieldHash) = 0.15
Provides: perl(I18N::Collate) = 1.02
Provides: perl(I18N::LangTags) = 0.40
Provides: perl(I18N::LangTags::Detect) = 1.05
Provides: perl(I18N::LangTags::List) = 0.39
Provides: perl(I18N::Langinfo) = 0.12
Provides: perl(IO) = 1.35
Provides: perl(IO::Compress::Adapter::Bzip2) = 2.068
Provides: perl(IO::Compress::Adapter::Deflate) = 2.068
Provides: perl(IO::Compress::Adapter::Identity) = 2.068
Provides: perl(IO::Compress::Base) = 2.068
Provides: perl(IO::Compress::Base::Common) = 2.068
Provides: perl(IO::Compress::Bzip2) = 2.068
Provides: perl(IO::Compress::Deflate) = 2.068
Provides: perl(IO::Compress::Gzip) = 2.068
Provides: perl(IO::Compress::Gzip::Constants) = 2.068
Provides: perl(IO::Compress::RawDeflate) = 2.068
Provides: perl(IO::Compress::Zip) = 2.068
Provides: perl(IO::Compress::Zip::Constants) = 2.068
Provides: perl(IO::Compress::Zlib::Constants) = 2.068
Provides: perl(IO::Compress::Zlib::Extra) = 2.068
#
Provides: perl(IO::Dir) = 1.10
Provides: perl(IO::File) = 1.16
Provides: perl(IO::Handle) = 1.35
Provides: perl(IO::Pipe) = 1.15
Provides: perl(IO::Pipe::End)
Provides: perl(IO::Poll) = 0.09
Provides: perl(IO::Seekable) = 1.10
Provides: perl(IO::Select) = 1.22
Provides: perl(IO::Socket) = 1.38
Provides: perl(IO::Socket::INET) = 1.35
Provides: perl(IO::Socket::UNIX) = 1.26
#
Provides: perl(IO::Socket::IP) = 0.37
Provides: perl(IO::Uncompress::Adapter::Bunzip2) = 2.068
Provides: perl(IO::Uncompress::Adapter::Identity) = 2.068
Provides: perl(IO::Uncompress::Adapter::Inflate) = 2.068
Provides: perl(IO::Uncompress::AnyInflate) = 2.068
Provides: perl(IO::Uncompress::AnyUncompress) = 2.068
Provides: perl(IO::Uncompress::Base) = 2.068
Provides: perl(IO::Uncompress::Bunzip2) = 2.068
Provides: perl(IO::Uncompress::Gunzip) = 2.068
Provides: perl(IO::Uncompress::Inflate) = 2.068
Provides: perl(IO::Uncompress::RawInflate) = 2.068
Provides: perl(IO::Uncompress::Unzip) = 2.068
Provides: perl(IO::Zlib) = 1.10
Provides: perl(IPC::Cmd) = 0.92
Provides: perl(IPC::Msg) = 2.04
Provides: perl(IPC::Msg::stat)
Provides: perl(IPC::Open2) = 1.04
Provides: perl(IPC::Open3) = 1.18
Provides: perl(IPC::Semaphore) = 2.04
Provides: perl(IPC::Semaphore::stat)
Provides: perl(IPC::SharedMem) = 2.04
Provides: perl(IPC::SysV) = 2.04
Provides: perl(JSON::PP) = 2.27300
Provides: perl(JSON::PP::Boolean)
Provides: perl(JSON::PP::IncrParser) = 1.01
Provides: perl(List::Util) = 1.41
Provides: perl(List::Util::XS) = 1.41
Provides: perl(Locale::Codes) = 3.34
Provides: perl(Locale::Codes::Constants) = 3.34
Provides: perl(Locale::Codes::Country) = 3.34
Provides: perl(Locale::Codes::Country_Codes) = 3.34
Provides: perl(Locale::Codes::Country_Retired) = 3.34
Provides: perl(Locale::Codes::Currency) = 3.34
Provides: perl(Locale::Codes::Currency_Codes) = 3.34
Provides: perl(Locale::Codes::Currency_Retired) = 3.34
Provides: perl(Locale::Codes::LangExt) = 3.34
Provides: perl(Locale::Codes::LangExt_Codes) = 3.34
Provides: perl(Locale::Codes::LangExt_Retired) = 3.34
Provides: perl(Locale::Codes::LangFam) = 3.34
Provides: perl(Locale::Codes::LangFam_Codes) = 3.34
Provides: perl(Locale::Codes::LangFam_Retired) = 3.34
Provides: perl(Locale::Codes::LangVar) = 3.34
Provides: perl(Locale::Codes::LangVar_Codes) = 3.34
Provides: perl(Locale::Codes::LangVar_Retired) = 3.34
Provides: perl(Locale::Codes::Language) = 3.34
Provides: perl(Locale::Codes::Language_Codes) = 3.34
Provides: perl(Locale::Codes::Language_Retired) = 3.34
Provides: perl(Locale::Codes::Script) = 3.34
Provides: perl(Locale::Codes::Script_Codes) = 3.34
Provides: perl(Locale::Codes::Script_Retired) = 3.34
# Provides: perl(Locale::Constants) = 2.1
Provides: perl(Locale::Country) = 3.34
Provides: perl(Locale::Currency) = 3.34
Provides: perl(Locale::Language) = 3.34
Provides: perl(Locale::Maketext) = 1.26
Provides: perl(Locale::Maketext::Guts) = 1.20
Provides: perl(Locale::Maketext::GutsLoader) = 1.20
Provides: perl(Locale::Maketext::Simple) = 0.21
Provides: perl(Locale::Script) = 3.34
Provides: perl(MIME::Base64) = 3.15
Provides: perl(MIME::QuotedPrint) = 3.13
Provides: perl(MM)
Provides: perl(MY)
Provides: perl(Math::BigFloat) = 1.9997
Provides: perl(Math::BigFloat::Trace) = 0.36
Provides: perl(Math::BigInt) = 1.9997
Provides: perl(Math::BigInt::Calc) = 1.9997
Provides: perl(Math::BigInt::CalcEmu) = 1.9997
Provides: perl(Math::BigInt::FastCalc) = 0.31
Provides: perl(Math::BigInt::Trace) = 0.36
Provides: perl(Math::BigRat) = 0.2608
Provides: perl(Math::Complex) = 1.59
Provides: perl(Math::Trig) = 1.23
Provides: perl(Memoize) = 1.03
Provides: perl(Memoize::AnyDBM_File) = 1.03
Provides: perl(Memoize::Expire) = 1.03
Provides: perl(Memoize::ExpireFile) = 1.03
Provides: perl(Memoize::ExpireTest) = 1.03
Provides: perl(Memoize::NDBM_File) = 1.03
Provides: perl(Memoize::SDBM_File) = 1.03
Provides: perl(Memoize::Storable) = 1.03
Provides: perl(Module::CoreList) = 5.20150520
Provides: perl(Module::CoreList::TieHashDelta) = 5.20150520
Provides: perl(Module::CoreList::Utils) = 5.20150520
Provides: perl(Module::Load) = 0.32
Provides: perl(Module::Load::Conditional) = 0.64
Provides: perl(Module::Loaded) = 0.08
Provides: perl(Module::Metadata) = 1.000026
# Provides: perl(MultipartBuffer)
# Provides: perl(MyClass) = 1.00
Provides: perl(NDBM_File) = 1.14
Provides: perl(NEXT) = 0.65
Provides: perl(NEXT::ACTUAL) = 0.65
Provides: perl(NEXT::ACTUAL::UNSEEN) = 0.65
Provides: perl(NEXT::ACTUAL::DISTINCT) = 0.65
Provides: perl(NEXT::DISTINCT) = 0.65
Provides: perl(NEXT::DISTINCT::ACTUAL) = 0.65
Provides: perl(NEXT::UNSEEN) = 0.65
Provides: perl(NEXT::UNSEEN::ACTUAL) = 0.65
Provides: perl(Net::Cmd) = 3.05
Provides: perl(Net::Config) = 3.05
Provides: perl(Net::Domain) = 3.05
Provides: perl(Net::FTP) = 3.05
Provides: perl(Net::FTP::A) = 3.05
Provides: perl(Net::FTP::E) = 3.05
Provides: perl(Net::FTP::I) = 3.05
Provides: perl(Net::FTP::L) = 3.05
Provides: perl(Net::FTP::dataconn) = 3.05
Provides: perl(Net::NNTP) = 3.05
Provides: perl(Net::Netrc) = 3.05
Provides: perl(Net::POP3) = 3.05
Provides: perl(Net::Ping) = 3.05
Provides: perl(Net::SMTP) = 3.05
Provides: perl(Net::Time) = 3.05
Provides: perl(Net::hostent) = 1.01
Provides: perl(Net::netent) = 1.01
Provides: perl(Net::protoent) = 1.01
Provides: perl(Net::servent) = 1.01
Provides: perl(O) = 1.01
Provides: perl(ODBM_File) = 1.12
Provides: perl(Opcode) = 1.32
Provides: perl(POSIX) = 1.53
Provides: perl(POSIX::SigAction) = 1.53
Provides: perl(POSIX::SigSet) = 1.53
Provides: perl(POSIX::SigRt) = 1.53
Provides: perl(Params::Check) = 0.38
Provides: perl(Parse::CPAN::Meta) = 1.4414
Provides: perl(Perl::OSType) = 1.008
Provides: perl(PerlIO) = 1.09
Provides: perl(PerlIO::encoding) = 0.21
Provides: perl(PerlIO::mmap) = 0.014
Provides: perl(PerlIO::scalar) = 0.22
Provides: perl(PerlIO::via) = 0.15
Provides: perl(PerlIO::via::QuotedPrint) = 0.08
Provides: perl(Pod::Cache) = 1.63
Provides: perl(Pod::Cache::Item) = 1.63
Provides: perl(Pod::Checker) = 1.60
Provides: perl(Pod::Escapes) = 1.07
Provides: perl(Pod::Find) = 1.63
Provides: perl(Pod::Functions) = 1.09
Provides: perl(Pod::Html) = 1.22
Provides: perl(Pod::Hyperlink) = 1.63
Provides: perl(Pod::InputObjects) = 1.63
Provides: perl(Pod::InputSource) = 1.63
Provides: perl(Pod::InteriorSequence) = 1.63
# Provides: perl(Pod::LaTeX) = 0.54
Provides: perl(Pod::List) = 1.63
Provides: perl(Pod::Man) = 2.28
Provides: perl(Pod::Paragraph) = 1.63
Provides: perl(Pod::ParseLink) = 1.10
Provides: perl(Pod::ParseTree) = 1.63
Provides: perl(Pod::ParseUtils) = 1.63
Provides: perl(Pod::Parser) = 1.63
Provides: perl(Pod::Perldoc) = 3.25
Provides: perl(Pod::Perldoc::BaseTo) = 3.25
Provides: perl(Pod::Perldoc::GetOptsOO) = 3.25
Provides: perl(Pod::Perldoc::ToANSI) = 3.25
Provides: perl(Pod::Perldoc::ToChecker) = 3.25
Provides: perl(Pod::Perldoc::ToMan) = 3.25
Provides: perl(Pod::Perldoc::ToNroff) = 3.25
Provides: perl(Pod::Perldoc::ToPod) = 3.25
Provides: perl(Pod::Perldoc::ToRtf) = 3.25
Provides: perl(Pod::Perldoc::ToTerm) = 3.25
Provides: perl(Pod::Perldoc::ToText) = 3.25
Provides: perl(Pod::Perldoc::ToTk) = 3.25
Provides: perl(Pod::Perldoc::ToXml) = 3.25
# Provides: perl(Pod::Plainer)
# Provides: perl(Pod::P) = 2.07
Provides: perl(Pod::Select) = 1.63
Provides: perl(Pod::Simple) = 3.29
Provides: perl(Pod::Simple::BlackBox) = 3.29
Provides: perl(Pod::Simple::Checker) = 3.29
Provides: perl(Pod::Simple::Debug) = 3.29
Provides: perl(Pod::Simple::DumpAsText) = 3.29
Provides: perl(Pod::Simple::DumpAsXML) = 3.29
Provides: perl(Pod::Simple::HTML) = 3.29
Provides: perl(Pod::Simple::HTMLBatch) = 3.29
Provides: perl(Pod::Simple::HTMLLegacy) = 5.01
Provides: perl(Pod::Simple::LinkSection) = 3.29
Provides: perl(Pod::Simple::Methody) = 3.29
Provides: perl(Pod::Simple::Progress) = 3.29
Provides: perl(Pod::Simple::PullParser) = 3.29
Provides: perl(Pod::Simple::PullParserEndToken) = 3.29
Provides: perl(Pod::Simple::PullParserStartToken) = 3.29
Provides: perl(Pod::Simple::PullParserTextToken) = 3.29
Provides: perl(Pod::Simple::PullParserToken) = 3.29
Provides: perl(Pod::Simple::RTF) = 3.29
Provides: perl(Pod::Simple::Search) = 3.29
Provides: perl(Pod::Simple::SimpleTree) = 3.29
Provides: perl(Pod::Simple::Text) = 3.29
Provides: perl(Pod::Simple::TextContent) = 3.29
Provides: perl(Pod::Simple::TiedOutFH) = 3.29
Provides: perl(Pod::Simple::Transcode) = 3.29
Provides: perl(Pod::Simple::TranscodeDumb) = 3.29
Provides: perl(Pod::Simple::TranscodeSmart) = 3.29
Provides: perl(Pod::Simple::XHTML) = 3.29
Provides: perl(Pod::Simple::XMLOutStream) = 3.29
Provides: perl(Pod::Simple::XHTML::LocalPodLinks) = 3.29
Provides: perl(Pod::Text) = 3.18
Provides: perl(Pod::Text::Color) = 2.07
Provides: perl(Pod::Text::Overstrike) = 2.05
Provides: perl(Pod::Text::Termcap) = 2.08
Provides: perl(Pod::Usage) = 1.64
Provides: perl(SDBM_File) = 1.13
Provides: perl(Safe) = 2.39
Provides: perl(Scalar::Util) = 1.41
Provides: perl(Search::Dict) = 1.07
Provides: perl(SelectSaver) = 1.02
Provides: perl(SelfLoader) = 1.22
# Provides: perl(Shell) = 0.4
Provides: perl(Socket) = 2.018
Provides: perl(Storable) = 2.53
Provides: perl(Sub::Util) = 1.41
Provides: perl(Switch) = 2.09
Provides: perl(Symbol) = 1.07
Provides: perl(Sys::Hostname) = 1.20
Provides: perl(Sys::Syslog) = 0.33

Provides: perl(TAP::Base) = 3.35

Provides: perl(Term::ANSIColor) = 4.03
Provides: perl(Term::Cap) = 1.15
Provides: perl(Term::Complete) = 1.403
Provides: perl(Term::ReadLine) = 1.15
Provides: perl(Term::ReadLine::Stub) = 1.15
Provides: perl(Term::ReadLine::TermCap) = 1.15
Provides: perl(Term::ReadLine::Tk) = 1.15
Provides: perl(Test) = 1.26
Provides: perl(Test::Builder) = 1.001014
Provides: perl(Test::Builder::IO::Scalar) = 2.113
Provides: perl(Test::Builder::Module) = 1.001014
Provides: perl(Test::Builder::Tester::Color) = 1.290001
Provides: perl(Test::Builder::Tester) = 1.28
Provides: perl(Test::Builder::Tester::Tie) = 1.28
Provides: perl(Test::Harness) = 3.35
# Provides: perl(Test::Harness::Assert) = 0.01
# Provides: perl(Test::Harness::Iterator) = 0.01
# Provides: perl(Test::Harness::Iterator::ARRAY)
# Provides: perl(Test::Harness::Iterator::FH)
# Provides: perl(Test::Harness::Straps) = 0.14
Provides: perl(Test::More) = 1.001014
Provides: perl(Test::Simple) = 1.001014
Provides: perl(Test::Tester) = 0.114
Provides: perl(Test::Tester::Capture)
Provides: perl(Test::Tester::CaptureRunner)
Provides: perl(Test::Tester::Delegate)

Provides: perl(Text::Abbrev) = 1.02
Provides: perl(Text::Balanced) = 2.03
Provides: perl(Text::Balanced::ErrorMsg)
Provides: perl(Text::Balanced::Extractor)
Provides: perl(Text::ParseWords) = 3.30
# Provides: perl(Text::Soundex) = 1.01
Provides: perl(Text::Tabs) = 2013.0523
Provides: perl(Text::Wrap) = 2013.0523
Provides: perl(Thread) = 3.04
Provides: perl(Thread::Queue) = 3.05
Provides: perl(Thread::Semaphore) = 2.12
Provides: perl(Tie::Array) = 1.06
Provides: perl(Tie::ExtraHash) = 1.05
Provides: perl(Tie::File) = 1.01
Provides: perl(Tie::File::Cache) = 1.01
Provides: perl(Tie::File::Heap) = 1.01
Provides: perl(Tie::Handle) = 4.2
Provides: perl(Tie::Hash) = 1.05
Provides: perl(Tie::Hash::NamedCapture) = 0.09
Provides: perl(Tie::Memoize) = 1.1
Provides: perl(Tie::RefHash) = 1.39
Provides: perl(Tie::RefHash::Nestable) = 1.39
Provides: perl(Tie::Scalar) = 1.03
Provides: perl(Tie::StdArray) = 1.03
Provides: perl(Tie::StdHandle) = 4.4
Provides: perl(Tie::StdHash) = 1.05
Provides: perl(Tie::StdScalar) = 1.03
Provides: perl(Tie::SubstrHash) = 1.00
Provides: perl(Time::HiRes) = 1.9726
Provides: perl(Time::Local) = 1.2300
Provides: perl(Time::Piece) = 1.29
Provides: perl(Time::Seconds) = 1.29
Provides: perl(Time::gmtime) = 1.03
Provides: perl(Time::localtime) = 1.02
Provides: perl(Time::tm) = 1.00
Provides: perl(UNIVERSAL) = 1.12
Provides: perl(Unicode::Collate) = 1.12
Provides: perl(Unicode::Collate:::CJK::Big5) = 1.12
Provides: perl(Unicode::Collate::CJK::GB2312) = 1.12
Provides: perl(Unicode::Collate::CJK::JISX0208) = 1.12
Provides: perl(Unicode::Collate::CJK::Korean) = 1.12
Provides: perl(Unicode::Collate::CJK::Pinyin) = 1.12
Provides: perl(Unicode::Collate::CJK::Stroke) = 1.12
Provides: perl(Unicode::Collate::CJK::Zhuyin) = 1.12
Provides: perl(Unicode::Collate::Locale) = 1.12
Provides: perl(Unicode::Normalize) = 1.18
Provides: perl(Unicode::UCD) = 0.61
Provides: perl(User::grent) = 1.01
Provides: perl(User::pwent) = 1.00
# Provides: perl(XS::APItest)
# Provides: perl(XS::Typemap) = 0.01
Provides: perl(XSLoader) = 0.20
Provides: perl(arybase) = 0.10
Provides: perl(attributes) = 0.27
# Provides: perl(attrs) = 1.01
Provides: perl(autodie) = 2.26
Provides: perl(autodie::Scope::Guard) = 2.26
Provides: perl(autodie::Scope::GuardStack) = 2.26
Provides: perl(autodie::ScopeUtil) = 2.26
Provides: perl(autodie::exception) = 2.26
Provides: perl(autodie::exception::system) = 2.26
Provides: perl(autodie::hints) = 2.26
Provides: perl(autodie::skip) = 2.26
Provides: perl(autouse) = 1.08
Provides: perl(base) = 2.22
Provides: perl(bigint) = 0.39
Provides: perl(bignum) = 0.39
Provides: perl(bigrat) = 0.39
Provides: perl(blib) = 1.06
Provides: perl(bytes) = 1.04
Provides: perl(charnames) = 1.43
Provides: perl(constant) = 1.33
Provides: perl(deprecate) = 0.03
Provides: perl(diagnostics) = 1.34
Provides: perl(dumpvar)
Provides: perl(encoding) = 2.14
Provides: perl(encoding::warnings)
Provides: perl(experimental)
Provides: perl(feature) = 1.40
Provides: perl(fields) = 2.17
Provides: perl(filetest) = 1.03
Provides: perl(if) = 0.0604
Provides: perl(integer) = 1.01
Provides: perl(less) = 0.03
Provides: perl(lib) = 0.63
Provides: perl(locale) = 1.06
Provides: perl(main)
Provides: perl(mro) = 1.17
Provides: perl(ok) = 0.16
Provides: perl(open) = 1.10
Provides: perl(ops) = 1.02
Provides: perl(overload) = 1.26
Provides: perl(overloading) = 0.02
Provides: perl(parent) = 0.232
Provides: perl(re) = 0.32
Provides: perl(sigtrap) = 1.08
Provides: perl(sort) = 2.02
Provides: perl(strict) = 1.09
Provides: perl(subs) = 1.02
Provides: perl(threads) = 2.01
Provides: perl(threads::shared) = 1.48
Provides: perl(utf8) = 1.17
Provides: perl(vars) = 1.03
Provides: perl(version) = 0.9909
Provides: perl(version::regex) = 0.9909
Provides: perl(version::vpp) = 0.9909
Provides: perl(vmsish) = 1.04
Provides: perl(warnings) = 1.32
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

# By definition of 'do' (see 'man perlfunc') this package provides all
# versions of perl previous to it.
Provides: perl <= %{version}

# These modules appear to be missing or break assumptions made by the
# dependency analysis tools.  Typical problems include refering to
# CGI::Apache as Apache and having no package line in CPAN::Nox.pm. I
# hope that the perl people fix these to work with our dependency
# engine or give us better dependency tools.
#
# Provides: perl(Apache)
# Provides: perl(ExtUtils::MM_Mac)
# Provides: perl(ExtUtils::XSSymSet)
# Provides: perl(FCGI)
# Provides: perl(LWP::UserAgent)
# Provides: perl(Mac::Files)
# Provides: perl(URI::URL)
# Provides: perl(VMS::Filespec)

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

#Default compiler we will look for
%define DEFCC /usr/vac/bin/xlc_r

%prep
%setup -q
mkdir modules

mkdir -p ../64bit
cp -r .dir-locals.el * ../64bit/
mv ../64bit .

# Add license info
cat Artistic > LICENSE

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else 
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS="$RPM_OPT_FLAGS"

# build 32bit mode
export OBJECT_MODE=32
export CC='/usr/vac/bin/xlc_r -q32'
export LDFLAGS="-s -Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib -L/usr/lib"
./Configure -desr -Doptimize="$RPM_OPT_FLAGS" \
	-d \
	-Dcc="$CC" -Dldflags="$LDFLAGS" \
	-Dinstallprefix=$RPM_BUILD_ROOT%{_prefix} \
	-Dprefix=%{_prefix} \
	-Duselargefiles \
	-Duseshrplib \
	-Dusethreads \
	-Darchname=%{_arch}-%{_os} \
	-A define:ld='/usr/vac/bin/xlc_r -q32' \
	-A define:ccdlflags='-brtl -bdynamic' \
	-A define:lddlflags='-bexpall -G -L/opt/freeware/lib'

make 
#make test
( make -k check || true )

# build 64bit mode
export OBJECT_MODE=64
cd 64bit
export CC='/usr/vac/bin/xlc_r -q64'
export LDFLAGS="-s -Wl,-bmaxdata:0x80000000 -L/opt/freeware/lib64 -L/usr/lib64 -L/opt/freeware/lib"

./Configure -desr -Doptimize="$RPM_OPT_FLAGS" \
	-d \
	-Dcc="$CC" -Dldflags="$LDFLAGS" \
	-Dinstallprefix=$RPM_BUILD_ROOT%{_prefix} \
	-Dprefix=%{_prefix} \
	-Duselargefiles \
	-Duseshrplib \
	-Dusethreads \
 	-Duse64bitall \
	-Darchname=%{_arch}-%{_os} \
	-A define:ld='/usr/vac/bin/xlc_r -q64' \
	-A define:ccdlflags='-brtl -bdynamic' \
	-A define:lddlflags='-bexpall -G -L/opt/freeware/lib64  -L/usr/lib64 -L/opt/freeware/lib'

make
#make test
( make -k check || true )

# add the 64-bit libperl.o to the shared library containing already the
# 32-bit libperl.o
cd ..
slibclean
ar -X32_64 -q libperl.a 64bit/libperl.o

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

cd 64bit
make install 

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_bindir}/pl2pm

# a2p is no longer in the Perl core
# find2perl, s2p and a2p are now separate CPAN packages
# (App-find2perl, App-s2p, App-a2p)

for f in perl perl%{version}
do
    mv ${RPM_BUILD_ROOT}%{_bindir}/${f} ${RPM_BUILD_ROOT}%{_bindir}/${f}_64bit
done

cd ..

make install 

# Patch Config_heavy.pl to remove $RPM_BUILD_ROOT from -bE:  "-e ldopts" output
# In previous versions this was not explicitly necessary, may be covered by
# an earlier catch or under case os == aix

mv ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi-64all/Config_heavy.pl ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi-64all/copy.Config_heavy.pl.copy

cat ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi-64all/copy.Config_heavy.pl.copy | sed -e 's@-bE:.*tmp/perl-root@-bE:@' > ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi-64all/Config_heavy.pl

rm ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi-64all/copy.Config_heavy.pl.copy

mv ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi/Config_heavy.pl ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi/copy.Config_heavy.pl.copy

cat ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi/copy.Config_heavy.pl.copy | sed -e 's@-bE:.*tmp/perl-root@-bE:@' > ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi/Config_heavy.pl

rm ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perlver}/ppc-aix-thread-multi/copy.Config_heavy.pl.copy



(cd $RPM_BUILD_ROOT
#binaries files are already stripped
#for f in perl perl%{version}
#do
#    /usr/bin/strip .%{prefix}/bin/${f}
#done

 mvdir .%{prefix}/share/man .%{prefix}/man
 # The Thread.3 manpage duplicates the same file in the tcl package.
 rm .%{prefix}/man/man3/Thread.3
)

# Generate *.ph files with a trick. Is this sick or what ?
make all -f - <<EOF
PKGS	= glibc-devel gdbm-devel gpm-devel libgr-devel libjpeg-devel \
	  libpng-devel libtiff-devel ncurses-devel popt \
	  zlib-devel binutils libelf e2fsprogs-devel pam pwdb \
	  rpm-devel
STDH	= \$(filter %{_includedir}/include/%%, \$(shell rpm -q --queryformat '[%%{FILENAMES}\n]' \$(PKGS)))
STDH	+=\$(wildcard %{_includedir}/linux/*.h) \$(wildcard %{_includedir}/asm/*.h) \
	  \$(wildcard %{_includedir}/scsi/*.h)
GCCDIR	= \$(shell gcc --print-file-name include)
GCCH	= \$(filter \$(GCCDIR)/%%, \$(shell rpm -q --queryformat '[%%{FILEMODES} %%{FILENAMES}\n]' gcc | grep -v ^4 | awk '{print $NF}'))

PERLLIB = \$(RPM_BUILD_ROOT)%{_libdir}/perl5/%{perlver}
PERL	= PERL5LIB=\$(PERLLIB) \$(RPM_BUILD_ROOT)%{_bindir}/perl
PHDIR	= \$(PERLLIB)/\${RPM_ARCH}-aix*
H2PH	= \$(PERL) \$(RPM_BUILD_ROOT)%{_bindir}/h2ph -d \$(PHDIR)/

all: std-headers gcc-headers fix-config

std-headers: \$(STDH)
	cd %{_includedir} && \$(H2PH) \$(STDH:%{_includedir}/%%=%%)

gcc-headers: \$(GCCH)
	cd \$(GCCDIR) && \$(H2PH) \$(GCCH:\$(GCCDIR)/%%=%%) || true

fix-config: \$(PHDIR)/Config.pm
	\$(PERL) -i -p -e "s|\$(RPM_BUILD_ROOT)||g;" \$<

EOF

# fix the rest of the stuff
find $RPM_BUILD_ROOT%{_libdir}/perl* -name .packlist -o -name perllocal.pod | \
xargs ./perl -i -p -e "s|$RPM_BUILD_ROOT||g;" $packlist


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc Artistic AUTHORS Changes* README LICENSE
%{_bindir}/*
%{_libdir}/*
%{_mandir}/*/*

%changelog
* Thu Nov 10 2016 Michael Wilson <michael.wilson@bull.net> 5.22.0-2
- Include make test for 32 and 64 bit builds
- Patch Config_heavy.pl to remove $RPM_BUILD_ROOT from -bE:  "-e ldopts" output

* Wed Aug 31 2015 Michael Wilson <michael.wilson@bull.net> 5.22.0-1
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

* Fri Aug 04 2001 David Clissold <cliss@austin.ibm.com>
- Strip of binaries was missed.

* Thu Jul 12 2001 David Clissold <cliss@austin.ibm.com>
- initial build for AIX Toolbox

* Mon Jun 19 2001 Nalin Dahyabhai <nalin@redhat.com>
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

* Tue Jun 12 1998 Christopher McCrory <chrismcc@netus.com
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
