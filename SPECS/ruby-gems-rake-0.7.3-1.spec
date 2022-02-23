Name:		ruby-gems-rake
Version:	0.7.3
Release:	1
License:	Distributable
URL:		http://rubyforge.org/projects/rubygems/
Prefix:		%{_prefix}
Source0:	http://rubyforge.vm.bytemark.co.uk/gems/rake-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Provides:	ruby(rake)
Summary:	rake is a ruby build facility, similar to make
Group:		Development/Languages
%define rubyver	1.8

%description
rake is a ruby build facility, similar to make.

Instead of using this package, if you have ruby installed, you can
simply run:   gem --install rake
This will download and install the latest version from rubyforge.org

%prep
# Nothing to setup

%build
# Nothing to build


%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver}

/opt/freeware/bin/gem install --local --install-dir $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver} %{SOURCE0}

mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
ln -s ../lib/ruby/gems/%{rubyver}/bin/rake \
	$RPM_BUILD_ROOT%{prefix}/bin/rake 

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/lib/ruby/gems/%{rubyver}/bin/*
%{_prefix}/lib/ruby/gems/%{rubyver}/cache/*
%{_prefix}/lib/ruby/gems/%{rubyver}/doc/*
%{_prefix}/lib/ruby/gems/%{rubyver}/gems/*
%{_prefix}/lib/ruby/gems/%{rubyver}/specifications/*
%{_prefix}/bin/*


%changelog
* Tue Aug 28 2007 Christophe BELLE <christophe.belle@bull.net> - 0.7.3-1
- Update to version 0.7.3 for AIX 52S
