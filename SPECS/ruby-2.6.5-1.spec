%bcond_without dotests
# compiler defauft gcc
# To use xlc : --without gcc_compiler
%bcond_without gcc_compiler

%define optimize 2

# Define the right directory as a function of architecture
%define _libdir64 /opt/freeware/lib64

%define rb_ver  2.6
# ruby script
%define rb_libdir                         %{_datadir}/ruby
# ruby modules
%define rb_archdir32                      %{_libdir}/ruby
%define rb_archdir64                      %{_libdir64}/ruby
# external files
%define rb_libsitedir                     %{_datadir}/ruby/site_ruby
%define rb_archsitedir32                  %{_libdir}/ruby/site_ruby/%{rb_ver}
%define rb_archsitedir64                  %{_libdir64}/ruby/site_ruby/%{rb_ver}
%define rb_libvendordir                   %{_datadir}/ruby/vendor_ruby
%define rb_archvendordir32                %{_libdir}/ruby/vendor_ruby/%{rb_ver}
%define rb_archvendordir64                %{_libdir64}/ruby/vendor_ruby/%{rb_ver}
# gems
%define rb_libgemsdir                     %{_datadir}/ruby/gems
%define rb_archgemsdir32                  %{_libdir}/ruby/gems/%{rb_ver}
%define rb_archgemsdir64                  %{_libdir64}/ruby/gems/%{rb_ver}

%define AIX_name                          powerpc-aix6.1.0.0

Name:		ruby
Version:	%{rb_ver}.5
Release:	1
License:	Ruby or BSD
URL:		http://www.ruby-lang.org/

# From Fedora
# Some of them are useless. They change a configure.ac file, not used.
# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
# Patch0: ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
# Patch1: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
# Patch2: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
# Patch3: ruby-2.1.0-always-use-i386.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://bugs.ruby-lang.org/issues/5617
# Patch4: ruby-2.1.0-custom-rubygems-location.patch
# Make mkmf verbose by default
Patch5: ruby-1.9.3-mkmf-verbose.patch
# Adds support for '--with-prelude' configuration option. This allows to built
# in support for ABRT.
# http://bugs.ruby-lang.org/issues/8566
#Patch6: ruby-2.1.0-Allow-to-specify-additional-preludes-by-configuratio.patch
# Use miniruby to regenerate prelude.c.
# https://bugs.ruby-lang.org/issues/10554
Patch7: ruby-2.6.3-Generate-preludes-using-miniruby.patch


# Prevent test cannot load strcpy.o on AIX 64bits
# Load : strcpy_64.o  (test/fiddle/helper.rb)
Patch20: %{name}-2.3.0-test_helper.patch
# skip test aix 64 bits : TestTime#test_a (test/ruby/test_time.rb)
# skip test : TestPTY#test_commandline  (test/test_pty.rb)
# skip test : TestPTY#ttest_argv (test/test_pty.rb)
Patch21: %{name}-2.3.1-skip_test_aix.patch
Patch22: %{name}-2.7.0-configure64.patch
# do not check localtime (consum too much times)
Patch23: %{name}-2.6.5-configure_localtime.patch

Source:  https://cache.ruby-lang.org/pub/ruby/2.7/%{name}-%{version}.tar.xz
Source2: %{name}-%{version}-%{release}.build.log
# Source3: %{name}-%{version}.run_one_by_one-test.ksh
Source4: libruby.stp
Source5: rubyconfig.h

BuildRequires: libffi-devel >= 3.2.1
BuildRequires: gdbm-devel >= 1.12
BuildRequires: ncurses-devel  >= 6.1
BuildRequires: readline-devel >= 7.0
BuildRequires: zlib-devel >= 1.2.11
BuildRequires: gmp-devel >= 6.1
BuildRequires: gzip >= 1.8
BuildRequires: tar >= 1.29
BuildRequires: sed

Requires: libffi >= 3.2.1
Requires: gdbm >= 1.12
Requires: ncurses >= 6.1
Requires: readline >= 7.0
Requires: zlib >= 1.2.11
Requires: gmp >= 6.1
Requires: libgcc >= 6.3.0

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages

Requires: %{name}-stdlib = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Provides:ruby(ruby) = %{rb_ver}

# %ifos aix6.1
# %define buildhost powerpc-ibm-aix6.1.0.0
# %endif

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.


%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
Requires:   %{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.


%package stdlib
Summary:        The Ruby standard library
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}-%{release}

%description stdlib
The Ruby standard library


%package libs
Summary:        Dynamic runtime library for Ruby
Group:          System/Libraries

%description libs
Dynamic runtime library for Ruby


%package doc
Summary:        Documentation and samples for Ruby
Group:          Development/Languages/Ruby
BuildArch:      noarch

%description doc
Documentation and samples for Ruby


%package doc-ri
Summary:        Ruby Interactive Documentation
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc-ri
This package contains the RI docs for ruby


%prep
# AIX tar fails
export PATH=/opt/freeware/bin:/usr/bin

%setup -q -n %{name}-%{version}

cp -p  ./test/ruby/test_time.rb ./test/ruby/test_time.rb.origine
cp -p ./test/test_pty.rb ./test/test_pty.rb.origine

%patch5 -p1
%patch7 -p0
%patch20 -p1
%patch21 -p1
%patch23 -p1 -b .localtime
# %patch24 -p1 -b .rubygems

# cp configure configure.save
# echo sed -e 's;-blibpath:${_prefix}/lib;&64;' -e 's;blibpath:%1\\$-s:${_prefix}/lib;&64;' -e ';-O3;-O%{optimize};' 
# sed -e 's;-O3;-O%{optimize};'    <configure.save > configure

# Some PaxHeader can cause trouble during compilation
find . -name "PaxHeader" | xargs rm -r

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

cd 64bit
%patch22 -p1 -b .configure64
# cp configure configure.save2
# sed -e 's;-blibpath:${prefix}/lib;&64;' -e 's;blibpath:%1\\$-s:${prefix}/lib;&64;' <configure.save2 > configure
# cd ..


%build
export PATH=/opt/freeware/bin:/usr/bin
# Needed to generate the doc
ulimit -d unlimited

# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh
# Ruby options
# export MINIRUBYOPT="-v "

export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export GLOBAL_CC_OPTIONS="-O2"

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# Choose XLC or GCC
%if %{with gcc_compiler}
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32 -D_LARGE_FILES  "
export FLAG64="-maix64 "

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"

export CXX__="/usr/vacpp/bin/xlC"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"


# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

# autoconf
./configure \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    \
    --with-archlibdir='%{rb_archdir64}' \
    --with-ruby-version=minor \
    --with-rubylibprefix='%{rb_libdir}' \
    --with-rubylibdir='%{rb_libdir}' \
    --with-rubyarchprefix='%{rb_archdir64}' \
    --with-sitedir='%{rb_libsitedir}' \
    --with-sitearchdir='%{rb_archsitedir64}' \
    --with-vendordir='%{rb_libvendordir}' \
    --with-vendorarchdir='%{rb_archvendordir64}' \
    \
    --with-rubyhdrdir='%{_includedir}' \
    --with-rubyarchhdrdir='%{_includedir}' \
    --with-sitehdrdir='%{_includedir}' \
    --with-sitearchhdrdir='%{_includedir}' \
    --with-vendorhdrdir='%{_includedir}' \
    --with-vendorarchhdrdir='%{_includedir}' \
    \
    --disable-rpath \
    --enable-pthread \
    --enable-shared \
    --disable-static \
    --disable-jit-support \
    --enable-multiarch
#    --with-rubygemsdir='%{rb_archgemsdir64}' \
#    --with-arch=AIX64

# To have the right JIT compiler
sed -i -e 's|^MJIT_CC.*$|MJIT_CC = /opt/freeware/bin/gcc|' Makefile
# # We do not want arch=powerpc-aix6.1.0.0
# sed -i -e 's|^arch = .*$|arch = |' Makefile

${MAKE}  %{?_smp_mflags} COPY="cp -p" Q=

# build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

./configure \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir} \
    \
    --with-archlibdir='%{rb_archdir32}' \
    --with-ruby-version=minor \
    --with-rubylibprefix='%{rb_libdir}' \
    --with-rubylibdir='%{rb_libdir}' \
    --with-rubyarchprefix='%{rb_archdir32}' \
    --with-sitedir='%{rb_libsitedir}' \
    --with-sitearchdir='%{rb_archsitedir32}' \
    --with-vendordir='%{rb_libvendordir}' \
    --with-vendorarchdir='%{rb_archvendordir32}' \
    \
    --with-rubyhdrdir='%{_includedir}' \
    --with-rubyarchhdrdir='%{_includedir}' \
    --with-sitehdrdir='%{_includedir}' \
    --with-sitearchhdrdir='%{_includedir}' \
    --with-vendorhdrdir='%{_includedir}' \
    --with-vendorarchhdrdir='%{_includedir}' \
    \
    --disable-rpath \
    --enable-pthread \
    --enable-shared \
    --disable-static \
    --disable-jit-support \
    --enable-multiarch
#    --with-rubygemsdir='%{rb_archgemsdir32}' \

# To have the right JIT compiler
sed -i -e 's|^MJIT_CC.*$|MJIT_CC = /opt/freeware/bin/gcc|' Makefile
# # We do not want arch=powerpc-aix6.1.0.0
# sed -i -e 's|^arch = .*$|arch = |' Makefile

${MAKE} %{?_smp_mflags} COPY="cp -p" Q=

# cp ./ext/tk/extconf.h ./ext/tk/extconf.h.save
# sed -e '/TCL_WIDE_INT_TYPE/d'  < ./ext/tk/extconf.h.save > ./ext/tk/extconf.h
# ${MAKE}  %{?_smp_mflags} COPY="cp -p" Q=


%install
export PATH=/opt/freeware/bin:/usr/bin
# save script for debugging
ls -lrtd $0
cp $0 %{name}-%{version}_script_install.ksh

# Ruby options
export MINIRUBYOPT="-v "

export RBUILD=$PWD
export INSTALL=/opt/freeware/bin/install
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export GLOBAL_CC_OPTIONS="-O2 -D_LARGE_FILES"
export MAKE="gmake --trace"

echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
# building in 32bit mode

mkdir -p $RPM_BUILD_ROOT/%{rb_libgemsdir}
mkdir -p $RPM_BUILD_ROOT/%{rb_archgemsdir32}
mkdir -p $RPM_BUILD_ROOT/%{rb_archgemsdir64}

# Choose XLC or GCC
%if %{with gcc_compiler}
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"

export CXX__="/usr/vacpp/bin/xlC"
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

cd 32bit

export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"

${MAKE} DESTDIR=$RPM_BUILD_ROOT install

strip $RPM_BUILD_ROOT%{_bindir}/%{name}

# move <files> (/opt/freeware/) bin to <files>_32
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in bin
  do
    cd $dir
    for fic in *;
    do
    [ -L "$fic" ] && continue;
    [ -f "$fic" ] || continue;
    echo  $fic | grep -e _32 -e _64 && continue;
    mv $fic $fic"_32"
    sed -i -e 's|#!/opt/freeware/bin/ruby|#!/usr/bin/env ruby_32|' $fic"_32"
    done
    cd -
  done
)

# config.h is different on 32 and 64 bits
(
  cd $RPM_BUILD_ROOT/%{_includedir}
  mv ruby/config.h ruby/config-ppc32.h
)

# Installing in 64bit mode
cd '%{_builddir}'/%{name}-%{version}/64bit

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

${MAKE} DESTDIR=$RPM_BUILD_ROOT install

strip $RPM_BUILD_ROOT%{_bindir}/%{name}

# move <files> (/opt/freeware/) bin to <files>_64
( cd $RPM_BUILD_ROOT/%{_prefix}
  for dir in bin
  do
    cd $dir
    for fic in *;
    do
    [ -L "$fic" ] && continue;
    [ -f "$fic" ] || continue;
    echo  $fic | grep -e _32 -e _64 && continue;
    mv $fic $fic"_64"
    sed -i -e 's|#!/opt/freeware/bin/ruby|#!/usr/bin/env ruby_64|' $fic"_64"
    ln -s $fic"_64" $fic
    done
    cd -
  done
)

# config.h is different on 32 and 64 bits
(
  cd $RPM_BUILD_ROOT/%{_includedir}
  mv ruby/config.h ruby/config-ppc64.h
)

# Some libraries are saved in a bad path. Deplace them to the right.
(
  cd $RPM_BUILD_ROOT/%{_libdir}/%{AIX_name}
  mv ./* ..
  cd $RPM_BUILD_ROOT/%{_libdir64}/%{AIX_name}
  mv ./* ..
)

# libruby.a must be created mannually (for compiled modules by gem)
(
    cd $RPM_BUILD_ROOT%{_libdir}
    $AR -qc libruby.a libruby.so.%{version}
    $AR -qc libruby.a ../lib64/libruby.so.%{version}
    cd ../lib64
    ln -sf ../lib/libruby.a libruby.a
)

# Copy config.h
(
    cd $RPM_BUILD_ROOT%{_includedir}/ruby
    cp %{SOURCE5} config.h
)

# gem_32 does not work.
# Even on 32 bits, gem compiles modules as 64 bit modules.
# Moreover, gem_32 and gem_64 install modules on the same location.
# So, we unactivate gem_32.
(
    cd $RPM_BUILD_ROOT%{_bindir}
    echo '#!/usr/bin/sh
    echo gem does not work on 32bit.
    echo Please using ruby and gem on 64 bit only,
    echo or copy and compile yourself script and module.
    echo You can install them on 
    echo /opt/freeware/lib/ruby/site_ruby/2.6/ for modules and 
    echo /opt/freeware/share/ruby/site_ruby/ for script.' > gem_32
    chmod +x gem_32
)


%check
%if %{with dotests}
ulimit -d unlimited
export MINIRUBYOPT="-v "
export INSTALL=/opt/freeware/bin/install
export PATH=%{buildroot}/%{_bindir}:/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export GLOBAL_CC_OPTIONS="-O2 -D_LARGE_FILES"
export MAKE="gmake --trace"
export LANG=en_US.utf-8

cd 64bit
export OBJECT_MODE=64
export LIBPATH="%{buildroot}/%{rb_archdir64}:%{buildroot}/%{rb_libdir}/%{rb_ver}:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export RUBYLIB="%{buildroot}/%{rb_archdir64}:%{buildroot}/%{rb_libdir}/%{rb_ver}:./gems/test-unit-3.2.9/lib"
${MAKE} DESTDIR=$RPM_BUILD_ROOT -k test     | tee traces_test.log     || true
${MAKE} DESTDIR=$RPM_BUILD_ROOT -k test-all | tee traces_test-all.log || true
cd ../32bit
export OBJECT_MODE=32
export LIBPATH="%{buildroot}/%{rb_archdir32}:%{buildroot}/%{rb_libdir}/%{rb_ver}:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export RUBYLIB="%{buildroot}/%{rb_archdir32}:%{buildroot}/%{rb_libdir}/%{rb_ver}:./gems/test-unit-3.2.9/lib"
${MAKE} DESTDIR=$RPM_BUILD_ROOT -k test     | tee traces_test.log     || true
${MAKE} DESTDIR=$RPM_BUILD_ROOT -k test-all | tee traces_test-all.log || true
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja

%doc 32bit/README.md 32bit/README.EXT 32bit/NEWS

%dir %{rb_libdir}
%dir %{rb_archdir32}
%dir %{rb_archdir64}
%dir %{rb_libsitedir}
%dir %{rb_archsitedir32}
%dir %{rb_archsitedir64}
%dir %{rb_libvendordir}
%dir %{rb_archvendordir32}
%dir %{rb_archvendordir64}
%dir %{rb_libgemsdir}
%dir %{rb_archgemsdir32}
%dir %{rb_archgemsdir64}

%{_bindir}/*


%files doc
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja
%doc %{_prefix}/share/man/man1/*.1


%files doc-ri
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja
%{_datadir}/ri


%files devel
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja
# %{_rpmconfigdir}/macros.d/macros.ruby
%{_includedir}/*


%files libs
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja
%{_libdir}/libruby.*
%{_libdir64}/libruby.*
%{rb_libdir}/%{rb_ver}/*
%{rb_archdir32}/*
%{rb_archdir64}/*
%exclude %{rb_libdir}/%{rb_ver}/rdoc/generator/template/darkfish/fonts/Lato-Regular*.ttf


%files stdlib
%defattr(-,root,system)
%doc 32bit/BSDL 32bit/COPYING 32bit/GPL 32bit/LEGAL
%lang(ja) %doc 32bit/COPYING.ja
# Ruby gems
%{rb_libgemsdir}/*
# %{rb_archgemsdir32}/*
# %{rb_archgemsdir64}/*


%changelog
* Mon Feb 24 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 2.6.5-1
- Merge Toolbox, Bullfreeware and Fedora specfiles
- Correct ruby path
- Unactivate JIT
- Separate ruby binaries, libs, stdlib, doc and doc-ri
- Create a fake gem_32 (original gem_32 does not work correctly)

* Wed Oct 23 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.6.3-1
- Update  to latest version

* Mon Sep 03 2018 Reshma V Kumar <reskumar@in.ibm.com> 2.5.1-1
- Update  to latest version

* Fri May 11 2018 Reshma V Kumar <reskumar@in.ibm.com> 2.4.4-1
- Update  to latest version to fix security vulnerability

* Fri Jun 30 2017 Reshma V Kumar <reskumar@in.ibm.com> 2.4.0-1
- Update  to latest version

* Wed Jun 21 2017 Tony Reix <tony.reix@atos.net> 2.3.1-6
- Remove dependency on libssl.so and libcrypto.so .
  Rather : libssl.a(libssl.so.1.0.2) libcrypto.a(libcrypto.so.1.0.2)

* Tue Nov 29 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1-5
- correct this erreur  echo "print 'toto'" | ruby  ==>   <internal:gem_prelude>:4:in require: cannot load such file -- rubygems.rb (LoadError)

* Mon Nov 14 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1
- Add ruby-2.3.1.run_one_by_one-test.ksh test script for test failed

* Thu Sep 29 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1-3
- Adaptation for 2.3.1 and add devel package

* Thu Mar 10 2016 Laurent GAY <laurent.gay@atos.net> 2.3.0-2
- Correction of GC randomize bug

* Wed Feb 10 2016 Laurent GAY <laurent.gay@atos.net> 2.3.0-1
- Adaptation for 2.3.0

* Thu Jan 07 2016 Tony Reix <tony.reix@bull.net> 2.3.0-1
- Update to version 2.3.0

* Thu Sep 17 2015 Tony Reix <tony.reix@bull.net> 2.2.3-1
- Update to version 2.2.3

* Wed Apr 23 2014 Gerard Visiedo <gerard.viseido@bull.net> 2.1.1-1
- Update to version 2.1.1

* Wed Jan 30 2013 by Bernard CAHEN <bernard.cahen@bull.net> 1.9.3-1
- Version for AIX 61

* Tue Aug 14 2007 by Christophe BELLE <christophe.belle@bull.net> 1.8.6-1
- Version for AIX 52S
