Name:		ruby-gems-rails
Version:	1.2.3
Release:	1
License:	Distributable
URL:		http://rubyforge.org/projects/rubygems/
Prefix:		%{_prefix}
Source0:	http://rubyforge.vm.bytemark.co.uk/gems/rails-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Provides:	ruby(rails)
Requires:	ruby
Requires:	ruby(rake)
Requires:	ruby(activesupport)
Requires:	ruby(activerecord)
Requires:	ruby(actionpack)
Requires:	ruby(actionmailer)
Requires:	ruby(actionwebservice)
Summary:	ruby on rails
Group:		Development/Languages
%define rubyver	1.8

%description
ruby-on-rails is a web programming framework for rails.

Instead of using this package, if you have ruby installed, you can
simply run:   gem --install rails
This will download and install the latest version from rubyforge.org

%prep
# Nothing to setup

%build
# Nothing to build


%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver}

#make sure we have gem and rake in the path
export PATH=$PATH:/opt/freeware/bin

/opt/freeware/bin/gem install --local --install-dir $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver} %{SOURCE0}

mkdir -p $RPM_BUILD_ROOT%{prefix}/bin
ln -s ../lib/ruby/gems/%{rubyver}/bin/rails \
	$RPM_BUILD_ROOT%{prefix}/bin/rails 

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
* Tue Aug 28 2007 Christophe BELLE <christophe.belle@bull.net> 1.2.3-1
- Version 1.2.3 for AIX 52S
