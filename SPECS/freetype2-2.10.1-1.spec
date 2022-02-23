# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# Keep package name freetype2 for now  - not sure why Fedora names it freetype

%define with_xfree86 1

Summary: A free and portable font rendering engine
Name: freetype2
Version: 2.10.1
Release: 1
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
URL: http://www.freetype.org
Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.xz
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.xz
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.xz
Source3: ftconfig.h

Source10: %{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64

# Enable subpixel rendering (ClearType)
Patch0:  freetype-2.3.0-enable-spr.patch
# Enable otvalid and gxvalid modules
Patch1:  freetype-2.2.1-enable-valid.patch
# Enable additional demos
Patch2:  freetype-2.5.2-more-demos.patch

Patch3:  freetype-2.6.5-libtool.patch

Patch4:  freetype-2.8-multilib.patch

Patch5:  freetype-2.10.0-internal-outline.patch
# Revert ABI/API change
Patch6:  freetype-2.10.1-debughook.patch

BuildRequires:  gcc
# AIX LPP X11 BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

Provides: %{name}-bytecode
Provides: %{name}-subpixel
# Obsoletes: freetype-freeworld < 2.9.1-2

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

The library is available as 32-bit and 64-bit.


%package demos
Summary: A collection of FreeType demos
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.


%package devel
Summary: FreeType development libraries and header files
Requires: %{name} = %{version}-%{release}
# Requires: pkgconf%{?_isa}

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.
 If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep

echo "dotests=%{dotests}"

# %setup -q -b 1 -a 2
%setup -q -n freetype-%{version} -b 1 -a 2

%patch0  -p1 -b .enable-spr
%patch1  -p1 -b .enable-valid

cd ft2demos-%{version}
%patch2  -p1 -b .more-demos
cd ..

%patch3 -p1 -b .libtool
%patch4 -p1 -b .multilib
%patch5 -p1 -b .internal-outline
%patch6 -p1 -b .debughook


# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/




%build

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/opt/freeware/bin/gcc -maix32"
export CC64="/opt/freeware/bin/gcc -maix64"


# first build the 64-bit version

cd 64bit

export CC="$CC64"
export OBJECT_MODE=64
# export LDFLAGS=""
gmake LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"


%configure --prefix=%{_prefix} \
           --libdir=%{_libdir64} \
           --enable-shared --enable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --enable-freetype-config \
           --with-harfbuzz=no

# sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool

# sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool

gmake %{?_smp_mflags}


%if %{with_xfree86}
# Build demos
cd ft2demos-%{version}
# The libtool orders _libdir before ../objs/.libs and new libfreetype not linked
# also blibpath does not include /opt/freeware/lib, no pthreads so no gcc path
# gmake LDFLAGS="-L../objs/.libs -L/opt/freeware/lib" TOP_DIR=".."
gmake LDFLAGS="-L../objs/.libs -L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib" TOP_DIR=".."
cd ..
%endif


# Now build the 32-bit version

cd ../32bit

export CC="$CC32"
export OBJECT_MODE=32
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

%configure --prefix=%{_prefix} \
           --enable-shared --enable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --enable-freetype-config \
           --with-harfbuzz=no

# sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool

# sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool

gmake %{?_smp_mflags}

# Add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q objs/.libs/libfreetype.a ../64bit/objs/.libs/libfreetype.so.6



%if %{with_xfree86}
# Build demos
cd ft2demos-%{version}
# The libtool orders _libdir before ../objs/.libs and new libfreetype not linked
gmake LDFLAGS="-Wl,-bmaxdata:0x80000000 -L../objs/.libs -L/opt/freeware/lib" TOP_DIR=".."
cd ..
%endif

# Convert FTL.txt and example3.cpp to UTF-8
cd docs
iconv -f latin1 -t utf-8 < FTL.TXT > FTL.TXT.tmp && \
touch -r FTL.TXT FTL.TXT.tmp && \
mv FTL.TXT.tmp FTL.TXT

iconv -f iso-8859-1 -t utf-8 < "tutorial/example3.cpp" > "tutorial/example3.cpp.utf8"
touch -r tutorial/example3.cpp tutorial/example3.cpp.utf8 && \
mv tutorial/example3.cpp.utf8 tutorial/example3.cpp
cd ..


%install

export RM="/usr/bin/rm -f"
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# install 64-bit version
export OBJECT_MODE=64
cd 64bit

# This following is wrong  - it installs to / !  It may work for Fedora, not AIX
# gmake install gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale
gmake DESTDIR=${RPM_BUILD_ROOT} install

{
  for ftdemo in ftbench ftchkwd ftmemchk ftpatchk fttimer ftdump ftlint ftmemchk ftvalid ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%if %{with_xfree86}
{
  for ftdemo in ftdiff ftgamma ftgrid ftmulti ftstring fttimer ftview ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}

# Reset the libpath because the graph.a part injected /usr/lib64 in the
# second -blibpath which took precedence
(
  cd ${RPM_BUILD_ROOT}/%{_bindir}
  for  ftdemo in ftdiff ftgamma ftgrid ftmulti ftstring ftview
  do

  OBJECT_MODE=64 ld  -L/opt/freeware/src/packages/BUILD/freetype-2.10.1/64bit/objs/.libs -L/opt/freeware/lib -lfreetype -lbz2 -lpng16 -lz -lc /opt/freeware/src/packages/BUILD/freetype-2.10.1/64bit/ft2demos-2.10.1/objs/graph.a -lX11 -lm -blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib   $ftdemo -o $ftdemo

  done
)

%endif

# Rename executables
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

# Header ftconfig.h SIZEOF_LONG is 8 in 64 bit env - save in temporary site
# because 32 bit install starts by an rm of include directory
# %define wordsize %{__isa_bits}
%define wordsize 64

mv $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h \
   ./ftconfig-%{wordsize}.h



# install 32-bit version
export OBJECT_MODE=32
cd ../32bit

# This following is wrong  - it installs to / !  It may work for Fedora, not AIX
# gmake install gnulocaledir=$RPM_BUILD_ROOT%{_datadir}/locale
gmake DESTDIR=${RPM_BUILD_ROOT} install


{
  for ftdemo in ftbench ftchkwd ftmemchk ftpatchk fttimer ftdump ftlint ftmemchk ftvalid ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%if %{with_xfree86}
{
  for ftdemo in ftdiff ftgamma ftgrid ftmulti ftstring fttimer ftview ; do
      builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/$ftdemo $RPM_BUILD_ROOT/%{_bindir}
  done
}
%endif

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# Create links
(
  cd ${RPM_BUILD_ROOT}
  mkdir -p %{_libdir64}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)

# Create symlink to lib/libfreetype.a where 64 bit .so has been archived
rm $RPM_BUILD_ROOT/%{_libdir64}/libfreetype.a
ln -s  ../lib/libfreetype.a  $RPM_BUILD_ROOT/%{_libdir64}/libfreetype.a


# Header ftconfig.h SIZEOF_LONG is 4 in 32 bit env
# fix multilib issues
# %define wordsize %{__isa_bits}
%define wordsize 32

mv $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h \
   $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig-%{wordsize}.h
cp ../64bit/ftconfig-64.h \
   $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig-64.h

install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_includedir}/freetype2/freetype/config/ftconfig.h

# Don't package static .a or .la files
# rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}



# %%triggerpostun -- freetype < 2.0.5-3
#{
#  # ttmkfdir updated - as of 2.0.5-3, on upgrades we need xfs to regenerate
#  # things to get the iso10646-1 encoding listed.
#  for I in %{_datadir}/fonts/*/TrueType /usr/share/X11/fonts/TTF; do
#      [ -d $I ] && [ -f $I/fonts.scale ] && [ -f $I/fonts.dir ] && touch $I/fonts.scale
#  done
#  exit 0
#}



%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# There are no tests currently
# Displays message "There is no validation suite for this package."
echo "*** No tests defined"

export CC32="/opt/freeware/bin/gcc -maix32"
export CC64="/opt/freeware/bin/gcc -maix64"

export CC=$CC64
export OBJECT_MODE=64

(VERBOSE=1 gmake -k check || true )
/usr/sbin/slibclean

export CC=$CC32
export OBJECT_MODE=32
(VERBOSE=1 gmake -k check || true )
/usr/sbin/slibclean


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
# %license docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc 32bit/docs/LICENSE.TXT 32bit/docs/FTL.TXT 32bit/docs/GPLv2.TXT
# %{_libdir}/libfreetype.so.*
%{_libdir}/libfreetype.a
%{_libdir64}/libfreetype.a
%doc 32bit/README
/usr/lib/libfreetype.a
/usr/lib64/libfreetype.a

%files demos
%defattr(-,root,system)
%{_bindir}/ftbench*
%{_bindir}/ftchkwd*
%{_bindir}/ftmemchk*
%{_bindir}/ftpatchk*
%{_bindir}/fttimer*
%{_bindir}/ftdump*
%{_bindir}/ftlint*
%{_bindir}/ftvalid*
%if %{with_xfree86}
%{_bindir}/ftdiff*
%{_bindir}/ftgamma*
%{_bindir}/ftgrid*
%{_bindir}/ftmulti*
%{_bindir}/ftstring*
%{_bindir}/ftview*
%endif
%doc 32bit/ChangeLog 32bit/README
/usr/bin/*

%files devel
%defattr(-,root,system)
%doc 32bit/docs/CHANGES 32bit/docs/formats.txt 32bit/docs/ft2faq.html
%dir %{_includedir}/freetype2
%{_datadir}/aclocal/freetype2.m4
%{_includedir}/freetype2/*
# %{_libdir}/libfreetype.so
%{_bindir}/freetype-config
%{_libdir}/pkgconfig/freetype2.pc
%doc 32bit/docs/design
%doc 32bit/docs/glyphs
%doc 32bit/docs/reference
%doc 32bit/docs/tutorial
%{_mandir}/man1/*
/usr/include/freetype2
/usr/bin/freetype-config

%changelog
* Thu Apr 16 2020 Michael Wilson <michael.a.wilson@atos.net> - 2.10.1-1
- Update to version 2.10.1
- Largely based on Fedora 32
- Gcc build only

* Thu Apr 16 2020 Michael Wilson <michael.a.wilson@atos.net> 2.4.4-4
- Rebuild on laurel2 and remove libfreetype.la from RPM
- XLC build only

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.4.4-3
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.4.4-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.4
- Update to version 2.4.4

* Tue Nov 16 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.2
- Update to version 2.4.2
