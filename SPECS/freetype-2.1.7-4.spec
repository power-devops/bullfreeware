# @(#)$Id: freetype.spec.in,v 1.1.2.4 2004/09/16 09:08:11 vanderms Exp $
# @BULL_COPYRIGHT@

%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc
%define _make %(if test x$MAKE = x ; then echo make ; else echo $MAKE ; fi)

Summary: A free and portable TrueType font rendering engine.
Name: freetype2
Version: 2.1.7
Release: 4
License: BSD/GPL dual license
Source0: freetype-%{version}.tar.bz2
URL: http://www.freetype.org/
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libtool >= 1.4.2
Prefix:%{_prefix}
%define prefix64 %{_prefix}/64
%define DEFCC cc
                                                                                                                                                                
# Use --define 'enable64 1' on the command line to disable 64bit build
%{!?enable64:%define BUILD64 0}
%{?enable64:%define BUILD64 1}
                                                                                                                                                                
%description
FreeType 2 is a software font engine that is designed to be small,
efficient, highly customizable and portable while capable of producing
high-quality output (glyph images). It can be used in graphics
libraries, display servers, font conversion tools, text image
generation tools, and many other products as well..
                                                                                                                                                                
Note that FreeType 2 is a font service and doesn't provide APIs to
perform higher-level features, like text layout or graphics processing
(e.g. colored text rendering, "hollowing", etc..). However, it greatly
simplifies these tasks by providing a simple, easy to use and uniform
interface to access the content of font files.
                                                                                                                                                                
%package devel
Summary: FreeType development headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Headers and documentation for the FreeType 2 software font engine.

%prep
%setup -q -n freetype-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/freetype-2.1.7-autotools.patch

                                                                                                                                                                
%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
bzip2 -dc %{SOURCE0} |tar -xf -
cd freetype-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/freetype-2.1.7-autotools.patch

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
export OBJECT_MODE=32   #just in case
                                                                                                                                                                
make setup CFG="--prefix=%{_prefix} --disable-static"
make
                                                                                                                                                                
%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/freetype-%{version}
export OBJECT_MODE=64
                                                                                                                                                                
make setup CFG="--prefix=%{prefix64} --disable-static"
make
                                                                                                                                                                
# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../../objs/.libs
/usr/bin/ar -q libfreetype.a ../../64bit/freetype-%{version}/objs/.libs/libfreetype.so.*
%endif #BUILD64
                                                                                                                                                                
%install
INSTDIR=%{_prefix}
make install prefix=$RPM_BUILD_ROOT$INSTDIR
                                                                                                                                                                
/usr/bin/strip $RPM_BUILD_ROOT$INSTDIR/bin/* 2>/dev/null || :
                                                                                                                                                                
(cd $RPM_BUILD_ROOT
                                                                                                                                                                
 mkdir -p usr/include
 cd usr/include
 ln -sf ../..%{_prefix}/include/* .
 cd -
                                                                                                                                                                
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf ../../..%{_prefix}/bin/* .
 cd -
                                                                                                                                                                
 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{_prefix}/lib/libfreetype.la .
 cd -
                                                                                                                                                                
 mkdir -p usr/linux/lib
 cd usr/linux/lib
 ln -sf ../../..%{_prefix}/lib/libfreetype.a .
 cd -
)
                                                                                                                                                                
( cd $RPM_BUILD_ROOT/%{_prefix}/lib
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
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif

%post
# Prototype support gtk 64 bit
mkdir -p /opt/freeware/64/lib
cd /opt/freeware/64/lib
ln -sf /opt/freeware/lib/libfreetype.a .
                                                                                                                                                                
%files
%defattr(644, root, root, 755)
%doc docs/license.txt docs/FTL.txt docs/GPL.txt docs/PATENTS
%{_prefix}/lib/libfreetype.a
/usr/linux/lib/libfreetype.a
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/libfreetype.a
%endif
                                                                                                                                                                
%files devel
%defattr(644, root, root, 755)
%doc README* docs/
%{_prefix}/include/*
%attr(0755, root, system) %{_prefix}/bin/*
/usr/include/freetype2
/usr/include/ft2build.h
/usr/linux/bin/*
%{_prefix}/lib/libfreetype.la
/usr/lib/libfreetype.la

%changelog
*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
