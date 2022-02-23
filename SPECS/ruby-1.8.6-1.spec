Name:		ruby
Version:	1.8.6
Release:	1
License:	Distributable
URL:		http://www.ruby-lang.org/
Prefix:		%{_prefix}
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Provides:	%{name}-libs
Patch0:		%{name}-%{version}-aix.patch

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages
%define DEFCC cc

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.

%prep
%setup -q
%patch0 -p0 -b .aix

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else
       export CC=gcc
    fi
fi

./configure --prefix=%{_prefix} --enable-shared # --with-tcllib=tcl8.4 --with-tklib=tk8.4
make
make test


%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install prefix=$RPM_BUILD_ROOT%{prefix}

strip $RPM_BUILD_ROOT%{_bindir}/%{name}

# Link ruby into /usr/bin
(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{prefix}/bin/ruby .
 cd -
)

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/bin/*
%{_prefix}/lib/libruby*
%{_prefix}/lib/ruby
%doc %{_prefix}/share/man/man1/%{name}.1
%doc README COPYING LEGAL NEWS README.EXT


%changelog
* Tue Aug 14 2007 by Christophe BELLE <christophe.belle@bull.net> 1.8.6-1
- Version for AIX 52S
