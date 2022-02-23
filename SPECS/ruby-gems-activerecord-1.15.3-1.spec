Name:		ruby-gems-activerecord
Version:	1.15.3
Release:	1
License:	Distributable
URL:		http://rubyforge.org/projects/rubygems/
Prefix:		%{_prefix}
Source0:	http://rubyforge.vm.bytemark.co.uk/gems/activerecord-%{version}.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Provides:	ruby(activerecord)
Requires:	ruby
Summary:	ruby activerecord
Group:		Development/Languages
%define rubyver	1.8

%description
ruby activerecord

Instead of using this package, if you have ruby installed, you can
simply run:   gem --install %{name}
This will download and install the latest version from rubyforge.org

%prep
# Nothing to setup

%build
# Nothing to build


%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver}

export PATH=$PATH:/opt/freeware/bin

/opt/freeware/bin/gem install --local \
   --install-dir $RPM_BUILD_ROOT%{prefix}/lib/ruby/gems/%{rubyver} %{SOURCE0}

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/lib/ruby/gems/%{rubyver}/cache/*
%{_prefix}/lib/ruby/gems/%{rubyver}/doc/*
%{_prefix}/lib/ruby/gems/%{rubyver}/gems/*
%{_prefix}/lib/ruby/gems/%{rubyver}/specifications/*


%changelog
* Tue Aug 28 2007 Christophe BELLE <christophe.belle@bull.net> 1.15.3-1
- Version 1.15.3 for AIX 52S
