%define gem_dir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitedir"]')/../gems
%define rb_ver %(ruby -rrbconfig -e 'puts Config::CONFIG["ruby_version"]')
%define gem_home %{gem_dir}/%{rb_ver}
%define ruby_sitelib %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')

Summary: The Ruby standard for packaging ruby libraries
Name: rubygems
Version: 0.9.4
Release: 1
Group: Development/Libraries
License: Ruby License/GPL
URL: http://rubyforge.org/projects/rubygems/
Source0: http://rubyforge.org/frs/download.php/11289/rubygems-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
Requires: ruby
BuildRequires: ruby
Provides: ruby(rubygems) = %{version}

%description
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%prep
%setup -q
# Some of the library files start with #! which rpmlint doesn't like
# and doesn't make much sense
for f in `find lib -name \*.rb` ; do
  head -1 $f | grep -q '^#!/usr/bin/env ruby' && sed -i -e '1d' $f
done

%build
ruby setup.rb config
ruby setup.rb setup
ruby doc/makedoc.rb || :

%install
rm -rf $RPM_BUILD_ROOT
GEM_HOME=$RPM_BUILD_ROOT%{gem_home} \
    ruby setup.rb install --prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system, -)
%doc README TODO ChangeLog Releases gemspecs
%{_bindir}/gem
%{_bindir}/gemlock
%{_bindir}/gem_mirror
%{_bindir}/gemri
%{_bindir}/gem_server
%{_bindir}/gemwhich
%{_bindir}/index_gem_repository.rb
%{_bindir}/update_rubygems

%{gem_dir}

%{ruby_sitelib}/gemconfigure.rb
%{ruby_sitelib}/ubygems.rb
%{ruby_sitelib}/rubygems.rb
%{ruby_sitelib}/rubygems
%{ruby_sitelib}/rbconfig/datadir.rb

%changelog
* Tue Aug 28 2007 Christophe BELLE <christophe.belle@bull.net> - 0.9.4-1
- Update to version 0.9.4

* Tue Jan  2 2007 David Lutterkort <dlutter redhat com> - 0.9.0-2
- Fix gem_dir to be arch independent
- Mention dual licensing in License field

* Fri Dec 22 2006 David Lutterkort <dlutter redhat com> - 0.9.0-1
- Updated to 0.9.0
- Changed to agree with Fedora Extras guidelines

* Mon Jan  9 2006 David Lutterkort <dlutter redhat com> - 0.8.11-1
- Updated for 0.8.11

* Sun Oct 10 2004 Omar Kilani <omar tinysofa org> 0.8.1-1ts
- First version of the package
