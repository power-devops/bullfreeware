Summary: A free and portable font rendering engine
Name: freetype2
Version: 2.4.4
Release: 3
License: BSD/GPL dual license
Group: System Environment/Libraries
URL: http://www.freetype.org

Source0: http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2.sig
Source2: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Source3: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2.sig
Source4: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
Source5: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2.sig

BuildRequires: zlib-devel, coreutils
Requires: zlib

Buildroot: /var/tmp/%{name}-%{version}-%{release}-root

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
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.


%package devel
Summary: FreeType development libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: zlib-devel
Requires: pkg-config

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
%setup -q -n freetype-%{version} -b 2 -a 4


%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export RM="/usr/bin/rm -f"
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"

# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
## VSD export CC="cc -q64"
CC_prev="$CC"
export CC="$CC -q64"

GNUMAKE=gmake ./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
gmake %{?_smp_mflags}

cp objs/.libs/libfreetype.so.6 .
gmake distclean

# now build the 32-bit version
export CC="$CC_prev"
GNUMAKE=gmake ./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
gmake %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q objs/.libs/libfreetype.a ./libfreetype.so.6

# Build demos
cd ft2demos-%{version}
gmake TOP_DIR=".." %{?_smp_mflags}


%install
export RM="/usr/bin/rm -f"
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

for f in ftbench ftdiff ftdump ftgamma ftgrid ftlint \
         ftmulti ftstring ftvalid ftview ; do
    builds/unix/libtool --mode=install install -m 755 ft2demos-%{version}/bin/${f} ${RPM_BUILD_ROOT}%{_bindir}
done

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc ChangeLog README
%{_libdir}/*.a
/usr/lib/*.a


%files demos
%defattr(-,root,system)
%{_bindir}/ft*
/usr/bin/ft*


%files devel
%defattr(-,root,system)
%{_bindir}/freetype-config
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*
/usr/bin/freetype-config
/usr/include/*
/usr/lib/*.la


%changelog
* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.4.4-3
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.4.4-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.4
- Update to version 2.4.4

* Tue Nov 16 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.2
- Update to version 2.4.2
