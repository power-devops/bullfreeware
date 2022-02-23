Summary: FreeType library
Name: freetype
Version: 1.3.1
Release: 9
Source0: ftp://ftp.freetype.org/pub/freetype/freetype-%{version}.tar.gz
Source1: IBM_ILA
URL: http://www.freetype.org/
License: IBM_ILA
Group: System Environment/Libraries
BuildRoot: /var/tmp/freetype
BuildRequires: libtool >= 1.3.5
#Built with libtool 1.3.5, autoconf 2.13, automake 1.4
Prefix:%{_prefix}
%define DEFCC cc

# Use --define 'no64 1' on the command line to disable 64bit build
%{!?no64:%define BUILD64 1}
%{?no64:%define BUILD64 0}
%define prefix64 %{prefix}/64

%description
The FreeType engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TrueType support to a
great variety of platforms and environments.

Note that FreeType is a *library*.  It is not a font server for your
favorite platform, even though it was designed to be used in many of
them.  Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as
load, hint and render individual glyphs efficiently.  You can also
see it as a `TrueType driver' for a higher-level library, though
rendering text with it is extremely easy, as demo-ed by the test
programs.

This package contains the files needed to run programs that use the
FreeType engine.

%package devel
Summary: FreeType development headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The FreeType engine is a free and portable TrueType font rendering
engine.  It has been developed to provide TrueType support to a
great variety of platforms and environments.

Note that FreeType is a *library*.  It is not a font server for your
favorite platform, even though it was designed to be used in many of
them.  Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as
load, hint and render individual glyphs efficiently.  You can also
see it as a `TrueType driver' for a higher-level library, though
rendering text with it is extremely easy, as demo-ed by the test
programs.

This package contains all supplementary files you need to develop
your own programs using the FreeType engine.

%package demo
Summary: FreeType test and demo programs
Group: Applications/Graphics
Requires: %{name} = %{version}

%description demo
The FreeType engine is a free and portable TrueType font rendering engine.
It has been developed to provide TT support to a great variety of platforms
and environments.

Note that FreeType is a *library*. It is not a font server for your favorite
platform, even though it was designed to be used in many of them. Note also 
that it is *not* a complete text-rendering library. Its purpose is simply to
open and manage font files, as well as load, hint and render individual 
glyphs efficiently. You can also see it as a "TrueType driver" for a 
higher-level library, though rendering text with it is extremely easy, as 
demo-ed by the test programs.

This package contains several programs bundled with the FreeType engine for
testing and demonstration purposes.

%prep 
%setup -q
find . -name CVS -type d | xargs rm -rf

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat license.txt >> LICENSE

%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gzip -dc %{SOURCE0} |tar -xf -
%endif


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
export OBJECT_MODE=32  #just to be sure

rm -f ltconfig || :
libtoolize --force
aclocal
autoconf
./configure --prefix=%{_prefix} --enable-static
make all

%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/freetype-%{version}
export OBJECT_MODE=64

rm -f ltconfig || :
libtoolize --force
aclocal
autoconf
./configure --prefix=%{_prefix}/64 --enable-static
make all

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../../lib/.libs
/usr/bin/ar -q libttf.a ../../64bit/freetype-%{version}/lib/.libs/libttf.so.*
%endif #BUILD64

%install
INSTDIR=%{_prefix}
make install prefix=$RPM_BUILD_ROOT$INSTDIR

/usr/bin/strip $RPM_BUILD_ROOT$INSTDIR/bin/* 2>/dev/null || :

(cd $RPM_BUILD_ROOT

 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/libttf.la .
 cd -

 mkdir -p usr/linux/lib
 cd usr/linux/lib
 ln -sf ../../..%{prefix}/lib/libttf.a .
 cd -
)

( cd $RPM_BUILD_ROOT/%{prefix}/lib
  # Create a compatibility member to mitigate differences with Bull Freeware
  # offering
  COMPATMEMBER=shr.o
  for lib in *.a
  do
    /usr/bin/dump -Tv $lib |/usr/bin/awk 'match($4,"EXP|Exp") { print $NF }' > tmp.exp
    libbase=`print $lib | sed  -e 's/.a$//' -e 's/^lib//'`
    ld -L. -bI:tmp.exp -bE:tmp.exp -l$libbase -bM:SRE -bnoentry -o $COMPATMEMBER
    /usr/bin/strip -e $COMPATMEMBER   # Make shr.o a load-only module
    /usr/bin/ar -r $lib $COMPATMEMBER
    rm -f $COMPATMEMBER tmp.exp
  done
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc announce LICENSE
%{_prefix}/lib/libttf.a
/usr/linux/lib/libttf.a
%{_prefix}/lib/libttf.la
/usr/lib/libttf.la
%{_prefix}/share/locale/
%if %{BUILD64} == 1
%dir %{prefix64}
%dir %{prefix64}/lib
%{prefix64}/lib/libttf.a
%endif

%files devel
%defattr(644, root, root, 755)
%doc INSTALL README PATENTS announce readme.1st LICENSE
%doc docs/ howto/
%{_prefix}/include/*
/usr/include/freetype

%files demo
%defattr(755, root, root, 755)
%doc announce LICENSE
%{_prefix}/bin/ftdump
%{_prefix}/bin/fterror
%{_prefix}/bin/ftlint
%{_prefix}/bin/ftmetric
%{_prefix}/bin/ftsbit
%{_prefix}/bin/ftstring
%{_prefix}/bin/ftstrpnm
%{_prefix}/bin/ftstrtto
%{_prefix}/bin/fttimer
%{_prefix}/bin/ftview
%{_prefix}/bin/ftzoom
/usr/bin/ftdump
/usr/bin/fterror
/usr/bin/ftlint
/usr/bin/ftmetric
/usr/bin/ftsbit
/usr/bin/ftstring
/usr/bin/ftstrpnm
/usr/bin/ftstrtto
/usr/bin/fttimer
/usr/bin/ftview
/usr/bin/ftzoom

%changelog
* Wed Feb 11 2004 David Clissold <cliss@austin.ibm.com> 1.3.1-9
- Build 64-bit version.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Apr 23 2002 David Clissold <cliss@austin.ibm.com>
- No functional change.  Remove political statement from the original
- gzipped tarball.  Only affects the source RPM.

* Mon Nov 12 2001 David Clissold <cliss@austin.ibm.com>
- No functional change.  Modify SPEC for compat w/ newer libtool.

* Wed Apr 11 2001 David Clissold <cliss@austin.ibm.com>
- Link into /usr/linux/lib instead of /usr/lib

* Thu Mar 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Build both 32- and 64-bit libraries

* Sun Mar 18 2001 Marc Stephenson <marc@austin.ibm.com>
- Use libtool 1.3.5a via libtoolize

* Fri Mar 09 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Use libtool 1.3.5a
- Insert Bull freeware compatibility member

* Thu Feb 15 2001 David Clissold <cliss@austin.ibm.com>
- Strip the executable binaries

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Wed Jun 16 1999  Werner Lemberg <werner.lemberg@freetype.org>
- Updated to version 1.3.

* Sun Oct 25 1998  Pavel Kankovsky <peak@kerberos.troja.mff.cuni.cz>
- libttf.so version number updated again.
- Default localedir based on prefix.
- File list adjustments (howto/).

* Sun Oct 16 1998  Pavel Kankovsky <peak@kerberos.troja.mff.cuni.cz>
- Source filename fixed.
- HOWTO removed.
- libttf.so version number updated.

* Tue Sep 29 1998  Robert Wilhelm <robert@freetype.org>
- Updated to version 1.2.

* Thu Sep  9 1998  Pavel Kankovsky <peak@kerberos.troja.mff.cuni.cz>
- Simplified (and fixed) file list.

* Tue Jul 14 1998  Alexander Zimmermann <Alexander.Zimmermann@fmi.uni-passau.de>
- Added missing files.
- Added %defattr tags.

* Thu Jun 18 1998  Robert Wilhelm <robert@freetype.org>
- Added lots of attr(-,root,root).

* Wed May 27 1998  Pavel Kankovsky <peak@kerberos.troja.mff.cuni.cz>
- Changed group attr of freetype and freetype-devel package.
- Fixed misc glitches.

* Sun May 24 1998  Pavel Kankovsky <peak@kerberos.troja.mff.cuni.cz>
- Split the package into three parts (runtime library, development
  tools, and demo programs).
- Added missing files (headers, NLS).
- Added ldconfing upon (de)installation.

* Thu Mar 12 1998  Bruno Lopes F. Cabral <bruno@openline.com.br>
- NLS for Portuguese language is missing, sorry (may be in a near future)
  (please note the workaround using --with-locale-dir and gnulocaledir.
  NLS Makefile needs a bit more rework but again I'll not patch it here).
