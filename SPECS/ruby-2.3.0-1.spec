Name:		ruby
Version:	2.3.0
Release:	1
License:	Distributable
URL:		http://www.ruby-lang.org/
Prefix:		%{_prefix}
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Provides:	%{name}-libs

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages

#%define DEFCC gcc
%define DEFCC xlc

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.

%prep
%setup -q -n %{name}-%{version}

%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=/opt/freeware/lib:/usr/lib:/lib
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export LDFLAGS="-L/opt/freeware/lib"
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE=gmake

autoconf
./configure \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
	--prefix=%{_prefix}

gmake
gmake test

%install
echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
gmake DESTDIR=$RPM_BUILD_ROOT install prefix=$RPM_BUILD_ROOT%{prefix}


strip $RPM_BUILD_ROOT%{_bindir}/%{name}


# Link ruby into /usr/bin and /usr/lib
( cd $RPM_BUILD_ROOT
  for dir in bin lib include
  do
     mkdir -p usr/${dir}
     cd usr/${dir}
     ln -sf ../..%{prefix}/${dir}/* .
     cd -
  done
)

# Run the tests
#export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
#export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
#export LIBPATH=/opt/freeware/lib:/usr/lib:/lib
#export PKG_CONFIG_PATH=
#export CPPFLAGS=""
#export LDFLAGS="-L/opt/freeware/lib"
#export CONFIG_SHELL=/usr/bin/bash
#export LDR_CNTRL=MAXDATA=0x80000000
#export MAKE=gmake
#export LANG=en_US.utf-8
#gmake test-all

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/bin/*
%{_prefix}/include/ruby*
%{_prefix}/lib/libruby*
%{_prefix}/lib/ruby
%{_prefix}/lib/pkgconfig
%{_prefix}/share/ri
/usr/bin/*
/usr/lib/libruby*
/usr/lib/ruby
/usr/include/*

%doc %{_prefix}/share/man/man1/*.1
%doc README.md COPYING LEGAL NEWS README.EXT


%changelog
* Wed Feb 10 2016 Laurent GAY <tony.reix@bull.net> 2.3.0-1
- Adaptation for 2.3.0

* Tue Jan 07 2016 Tony Reix <tony.reix@bull.net> 2.3.0-1
- Update to version 2.3.0

* Tue Sep 17 2015 Tony Reix <tony.reix@bull.net> 2.2.3-1
- Update to version 2.2.3

* Wed Apr 23 2014 Gerard Visiedo <gerard.viseido@bull.net> 2.1.1-1
- Update to version 2.1.1

* Wed Jan 30 2013 by Bernard CAHEN <bernard.cahen@bull.net> 1.9.3-1
- Version for AIX 61

* Tue Aug 14 2007 by Christophe BELLE <christophe.belle@bull.net> 1.8.6-1
- Version for AIX 52S
