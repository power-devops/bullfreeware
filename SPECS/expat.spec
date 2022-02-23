%define _prefix /opt/freeware

Summary: A library for parsing XML.
Name: expat
Version: 1.95.7
Release: 4 
License: BSD
Group: System Environment/Libraries

Patch0:		expat-1.95.7-aix.patch
Patch1:		expat-1.95.7-autotools.patch

Source:         %{name}-%{version}.tar.bz2
URL: http://sourceforge.net/projects/expat
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libtool >= 1.3.5
%define DEFCC xlc
                                                                         
# Use --define 'enable64 1' on the command line to disable 64bit build
%{!?enable64:%define BUILD64 0}
%{?enable64:%define BUILD64 1}
%define prefix64 %{_prefix}/64

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed.
A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and include files to develop XML applications with expat.
Group: Development/Libraries
Requires:       %{name} = %{version}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.
 
%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/expat-1.95.7-aix.patch
$PATCH -p2 -s < %{_sourcedir}/expat-1.95.7-autotools.patch


%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gzip -dc %{SOURCE0} |tar -xf -
cd %{name}-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/expat-1.95.7-aix.patch
$PATCH -p2 -s < %{_sourcedir}/expat-1.95.7-autotools.patch

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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
else
        export CFLAGS64="-maix64"
fi
export CFLAGS="$RPM_OPT_FLAGS"
OBJECT_MODE=32  #just to make sure
 
libtoolize --copy --force
aclocal -I conftools
autoconf
%configure --disable-static
make
 
# Strip the binary if unstripped
/usr/bin/strip xmlwf/.libs/xmlwf || :
 
%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64
export CC="$CC $CFLAGS64"
libtoolize --copy --force
aclocal -I conftools
autoconf
%configure --prefix=%{prefix64} --disable-static
make
 
/usr/bin/strip xmlwf/.libs/xmlwf || :
 
# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../../.libs
/usr/bin/ar -q \
  libexpat.a ../64bit/%{name}-%{version}/.libs/libexpat.so.0
 
%endif #BUILD64
 
%install
rm -rf ${RPM_BUILD_ROOT}
 
make DESTDIR=$RPM_BUILD_ROOT install
 
( cd $RPM_BUILD_ROOT
 for dir in include bin
 do
    mkdir -p usr/$dir || :
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
 
 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{_prefix}/lib/* .
 cd -
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif
 
%files
%defattr(-,root,root)
%doc README COPYING LICENSE
%{_prefix}/lib/*.a
/usr/lib/*.a
%{_prefix}/bin/*
/usr/bin/*
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif
 
%files devel
%defattr(-,root,root)
%doc doc examples LICENSE
%{_prefix}/lib/lib*.la
%{_includedir}/*.h
/usr/lib/*.la
/usr/include/*.h

%changelog
*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
