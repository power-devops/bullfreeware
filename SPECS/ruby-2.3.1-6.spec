# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}
# compiler defauft gcc
# To use xlc : --define 'gcc_compiler=0'

%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler:%define gcc_compiler 1}

%{!?optimize:%define optimize 2}

Name:		ruby
Version:	2.3.1
Release:	6
License:	Distributable
URL:		http://www.ruby-lang.org/
Prefix:		%{_prefix}

%define libdir64 /opt/freeware/lib64


# This is due in order to don't depend on libssl.so rather libssl.a(libssl.so.1.0.2) .
# When the build stops in the middle, files are not put back at their original place
# This is done at beg and end of %build
# Run:
# ln -s /opt/freeware/lib64/libssl.so.1.0.2 /opt/freeware/lib64/libssl.so ; ln -s /opt/freeware/lib64/libcrypto.so.1.0.2 /opt/freeware/lib64/libcrypto.so
# ln -s /opt/freeware/lib/libssl.so.1.0.2   /opt/freeware/lib/libssl.so ;   ln -s /opt/freeware/lib/libcrypto.so.1.0.2   /opt/freeware/lib/libcrypto.so



# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
Patch0: ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
Patch1: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
Patch2: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
#Patch3: ruby-2.1.0-always-use-i386.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://bugs.ruby-lang.org/issues/5617
#Patch4: ruby-2.1.0-custom-rubygems-location.patch
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
# Prevent test cannot load strcpy.o on AIX 64bits
# Load : strcpy_64.o  (test/fiddle/helper.rb)
Patch20: ruby-2.3.0-test_helper.patch
# skip test aix 64 bits : TestTime#test_a (test/ruby/test_time.rb)
# skip test : TestPTY#test_commandline  (test/test_pty.rb)
# skip test : TestPTY#ttest_argv (test/test_pty.rb)
Patch22: ruby-2.3.1-skip_test_aix.patch

Source:		%{name}-%{version}.tar.gz
Source2: %{name}-%{version}-%{release}.build.log
Source3: %{name}-%{version}.run_one_by_one-test.ksh

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Provides:	%{name}-libs

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Languages

%define _libdir64 %{_prefix}/lib64


BuildRequires: openssl
Requires: openssl

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%description
Ruby is an interpreted scripting language for quick and easy object-oriented
programming.  It has many features to process text files and to do system
management tasks.  It is simple, straight-forward, and extensible.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif



%package devel
Summary:    A Ruby development environment
Group:      Development/Languages
Requires:   %{name}%{?_isa} = %{version}-%{release}
# Requires:   rubypick
# Requires:   rubygems

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.


%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "optimize=%{optimize}"

%setup -q -n %{name}-%{version}

cp -p  ./test/ruby/test_time.rb ./test/ruby/test_time.rb.origine
cp -p ./test/test_pty.rb ./test/test_pty.rb.origine

%patch0 -p1
%patch1 -p1
%patch2 -p1
# %patch3 -p1
# %patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch20 -p1
%patch22 -p1

cp configure.in configure.in.save
echo sed -e 's;-blibpath:${prefix}/lib;&64;' -e 's;blibpath:%1\\$-s:${prefix}/lib;&64;' -e ';-O3;-O%{optimize};' 
sed -e 's;-O3;-O%{optimize};'    <configure.in.save > configure.in

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

cd 64bit

cp configure.in configure.in.save2
sed -e 's;-blibpath:${prefix}/lib;&64;' -e 's;blibpath:%1\\$-s:${prefix}/lib;&64;' <configure.in.save2 > configure.in
cd ..


%build

###############################################
# for linking with openssl archive (not soname)
###############################################
if [ -f %{_libdir}/libcrypto.so ]; then
    mv %{_libdir}/libcrypto.so /tmp/libcrypto.so.32
fi
if [ -f %{_libdir}/libssl.so ]; then
    mv %{_libdir}/libssl.so /tmp/libssl.so.32
fi
if [ -f %{_libdir64}/libcrypto.so ]; then
    mv %{libdir64}/libcrypto.so /tmp/libcrypto.so.64
fi
if [ -f %{_libdir64}/libssl.so ]; then
    mv %{libdir64}/libssl.so /tmp/libssl.so.64
fi


# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh
# Ruby options
export MINIRUBYOPT="-v "

export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export PKG_CONFIG_PATH=
export CPPFLAGS=""
export CONFIG_SHELL=/usr/bin/bash
export LDR_CNTRL=MAXDATA=0x80000000
export MAKE="gmake --trace"
export GLOBAL_CC_OPTIONS=" "

export CONFIG_SHELL=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# Choose XLC or GCC
%if %{gcc_compiler} == 1
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


# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

autoconf
./configure \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    --disable-rpath \
    --enable-pthread \
    --enable-shared

${MAKE}  %{?_smp_mflags} COPY="cp -p" Q=

if [ "%{dotests}" == 1 ]
then
    [ -L /usr/local/bin/ruby ] && rm /usr/local/bin/ruby
#    ln -s $RPM_BUILD_DIR/%{name}-%{version}/64bit/ruby /usr/local/bin/ruby
    export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
    export LANG=en_US.utf-8
    ${MAKE} -k test     | tee traces_test.log     || true
    ${MAKE} -k test-all | tee traces_test-all.loc || true
fi

# build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"

autoconf
./configure \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir} \
    --disable-rpath \
    --enable-pthread \
    --enable-shared

${MAKE} %{?_smp_mflags} COPY="cp -p" Q=  || true

cp ./ext/tk/extconf.h ./ext/tk/extconf.h.save
sed -e '/TCL_WIDE_INT_TYPE/d'  < ./ext/tk/extconf.h.save > ./ext/tk/extconf.h

${MAKE}  %{?_smp_mflags} COPY="cp -p" Q=

if [ "%{dotests}" == 1 ]
then
    [ -L /usr/local/bin/ruby ] && rm /usr/local/bin/ruby
#    ln -s $RPM_BUILD_DIR/%{name}-%{version}/32bit/ruby /usr/local/bin/ruby
    export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
    export LANG=en_US.utf-8
    ${MAKE} -k test     | tee traces_test.log     || true
    ${MAKE} -k test-all | tee traces_test-all.loc || true
fi


##################################################################
# revert previous move - linking with openssl archive (not soname)
##################################################################

if [ -f /tmp/libcrypto.so.32 ]; then
    mv /tmp/libcrypto.so.32 %{_libdir}/libcrypto.so
fi
if [ -f /tmp/libssl.so.32 ]; then
    mv /tmp/libssl.so.32 %{_libdir}/libssl.so
fi
if [ -f /tmp/libcrypto.so.64 ]; then
    mv /tmp/libcrypto.so.64 %{libdir64}/libcrypto.so
fi
if [ -f /tmp/libssl.so.64 ]; then
    mv /tmp/libssl.so.64 %{libdir64}/libssl.so
fi



%install
# save script for debugging
ls -lrtd $0
cp $0 %{name}-%{version}_script_install.ksh

# Ruby options
export MINIRUBYOPT="-v "

export RBUILD=$PWD
export INSTALL=/opt/freeware/bin/install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export GLOBAL_CC_OPTIONS="-O2 "
export MAKE="gmake --trace"

echo "RPM_BUILD_ROOT = $RPM_BUILD_ROOT"
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
# building in 32bit mode


# Choose XLC or GCC
%if %{gcc_compiler} == 1
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

export LD_LIBRARY_PATH=/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=""

${MAKE} DESTDIR=$RPM_BUILD_ROOT install prefix=$RPM_BUILD_ROOT%{prefix}

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
      done
      cd -
  done
)


# building in 64bit mode
cd '%{_builddir}'/%{name}-%{version}/64bit

export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

${MAKE} DESTDIR=$RPM_BUILD_ROOT install prefix=$RPM_BUILD_ROOT%{prefix}

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
	  ln -s $fic"_64" $fic
      done
      cd -
  done
)


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
# echo "ruby     .2.3.0 "  > input.lib.$$.tmp
#
# cat input.lib.$$.tmp | while read lib number pad;
# do
#     [ $number == "NULL" ] && { number=""; }
#
     # extract then add the 64-bit shared object to the shared library containing already the
     # 32-bit shared object
#     $AR -X64 -x  ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
#     $AR -X64 -q  ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a   lib"$lib".so"$number"
#     (
	# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
# 	$RM ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
# 	cd  ${RPM_BUILD_ROOT}%{_libdir64}
# 	ln -s ../lib/lib"$lib".a lib"$lib".a
#     )
# done
# rm -f input.lib.$$.tmp


# Link ruby into /usr/bin /usr/lib /usr/lib64 ans /usr/include
( cd $RPM_BUILD_ROOT
  for dir in bin lib lib64 include
  do
      mkdir -p usr/${dir}
      cd usr/${dir}
      ln -sf ../..%{prefix}/${dir}/* .
      cd -
  done
)

# replace lib64 duplicate files by a link
(
    cd $RPM_BUILD_ROOT%{_libdir64}
    for fic in $(find . -type f);
    do
	f=$(echo $fic| sed -e 's|^\./||')
	[ -f ../lib/$f  ] || continue;
	cmp $f ../lib/$f >/dev/null  || continue;
	dn=$(dirname $f)
	bn=$(basename $f)
	(
	    cd $dn
	    rm $bn
	    c=$(echo $f|awk -F/ '{printf "%s",substr ("../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../",1,(NF)*3)}')
	    s=$c"lib/"$f;
	    ln -s $s $bn
	)
    done
)



%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, system)
%{_prefix}/bin/*
%{_prefix}/include/ruby*

%{_prefix}/lib/libruby*.so*
%{_prefix}/lib/ruby
%{_prefix}/lib/pkgconfig

%{_prefix}/lib64/libruby*.so*
%{_prefix}/lib64/ruby
%{_prefix}/lib64/pkgconfig

%{_prefix}/share/ri

/usr/bin/*
/usr/lib/libruby*.so*
/usr/lib/ruby

/usr/lib64/libruby*.so*
/usr/lib64/ruby

/usr/include/*

%doc %{_prefix}/share/man/man1/*.1
%doc 32bit/README.md 32bit/COPYING 32bit/LEGAL 32bit/NEWS 32bit/README.EXT


%files devel
%doc 32bit/BSDL
%doc 32bit/COPYING
%lang(ja) %doc 32bit/COPYING.ja
%doc 32bit/GPL
%doc 32bit/LEGAL

# %{_rpmconfigdir}/macros.d/macros.ruby

%{_prefix}/lib/libruby*.a
%{_prefix}/lib64/libruby*.a
%{_includedir}/*
%{_libdir}/libruby.so*
%{_libdir64}/libruby.so*
%{_libdir}/pkgconfig/%{name}-2.3.pc


%changelog
* Wed Jun 21 2017 Tony Reix <tony.reix@atos.net> 2.3.1-6
- Remove dependency on libssl.so and libcrypto.so .
  Rather : libssl.a(libssl.so.1.0.2) libcrypto.a(libcrypto.so.1.0.2)

* Tue Nov 29 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1-5
- correct this erreur  echo "print 'toto'" | ruby  ==>   <internal:gem_prelude>:4:in require: cannot load such file -- rubygems.rb (LoadError)

* Thu Nov 14 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1
- Add ruby-2.3.1.run_one_by_one-test.ksh test script for test failed

* Thu Sep 29 2016 Jean Girardet <jean.girardet@atos.net> 2.3.1-3
- Adaptation for 2.3.1 and add devel package

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
