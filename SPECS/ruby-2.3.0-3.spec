Name:		ruby
Version:	2.3.0
Release:	3
License:	Distributable
URL:		http://www.ruby-lang.org/
Prefix:		%{_prefix}
Patch00:     %{name}-%{version}-pthread_gc.patch

# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
# Patch0: ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
Patch1: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
Patch2: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3: ruby-2.1.0-always-use-i386.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://bugs.ruby-lang.org/issues/5617
Patch4: ruby-2.1.0-custom-rubygems-location.patch
# Make mkmf verbose by default
Patch5: ruby-1.9.3-mkmf-verbose.patch
# Adds support for '--with-prelude' configuration option. This allows to built
# in support for ABRT.
# http://bugs.ruby-lang.org/issues/8566
Patch6: ruby-2.1.0-Allow-to-specify-additional-preludes-by-configuratio.patch
# Use miniruby to regenerate prelude.c.
# https://bugs.ruby-lang.org/issues/10554
Patch7: ruby-2.2.3-Generate-preludes-using-miniruby.patch
# Prevent test failures on ARM.
# https://bugs.ruby-lang.org/issues/12331
Patch8: ruby-2.4.0-increase-timeout-for-ARMv7.patch
Source:		%{name}-%{version}.tar.gz
Source2: %{name}-%{version}-%{release}.build.log
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Provides:	%{name}-libs

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages

#%define DEFCC gcc
# %define DEFCC xlc

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.

%prep
%setup -q -n %{name}-%{version}

%patch00



# echo    :  %patch0 -p1
# %patch0 -p 1
# %patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
# echo    :  %patch8 -p1
# %patch8 -p1 


%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=/opt/freeware/lib:/usr/lib:/lib
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export LDFLAGS="-L/opt/freeware/lib"
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"

export OBJECT_MODE=32

export CC="/opt/freeware/bin/gcc  -maix32 -O2 "
export CXX="/opt/freeware/bin/g++ -maix32 -O2 "

autoconf
./configure \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
	--prefix=%{_prefix}

$MAKE || true

cp ./ext/tk/extconf.h ./ext/tk/extconf.h.save
sed -e '/TCL_WIDE_INT_TYPE/d'  < ./ext/tk/extconf.h.save > ./ext/tk/extconf.h
$MAKE

$MAKE test


%install
echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export CC="/opt/freeware/bin/gcc  -maix32 -O2 "
export CXX="/opt/freeware/bin/g++ -maix32 -O2 "
export OBJECT_MODE=32
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

# Run the tests => to execute manualy
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
* Thu Oct 06 2016 jean Girardet <jean.girardet@atos.net> 2.3.0-3
- Integrate fedora patchs 2.3.0

* Tue Mar 10 2016 Laurent GAY <laurent.gay@atos.net> 2.3.0-2
- Correction of GC randomize bug

* Wed Feb 10 2016 Laurent GAY <laurent.gay@atos.net> 2.3.0-1
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
