%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: The zlib compression and decompression library.
Name: zlib
Version: 1.2.3 
Release: 4 
Group: System Environment/Libraries
Source0: ftp://ftp.uu.net/graphics/png/zlib-%{version}.tar.bz2

Patch0:		zlib-1.2.3-aix.patch

URL: http://www.gzip.org/zlib/
License: BSD
BuildRoot: %{_tmppath}/%{name}-%{version}-root
%define DEFCC xlc

# Use --define 'enable64 1' on the command line to enable 64bit build
%{!?enable64:%define BUILD64 0}
%{?enable64:%define BUILD64 1}
%define prefix64 %{_prefix}/64

%description
The zlib compression library provides in-memory compression and decompression
functions, including integrity checks of the uncompressed data.  This version
of the library supports only one compression method (deflation), but other
algorithms may be added later, which will have the same stream interface.  The
zlib library is used by many different system programs.

%package devel
Summary: Header files and libraries for developing apps which will use zlib.
Group: Development/Libraries
Requires: zlib

%description devel
The zlib-devel package contains the header files and libraries needed to
develop programs that use the zlib compression and decompression library.

Install the zlib-devel package if you want to develop applications that will
use the zlib library.

%prep
%setup -q -n %{name}-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/zlib-1.2.3-aix.patch


%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
bzip2 -dc %{SOURCE0} |tar -xf -
cd %{name}-%{version}

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/zlib-1.2.3-aix.patch

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
export CFLAGS="-DHAS_vsnprintf -DHAS_snprintf"
export OBJECT_MODE=32   #just to be sure

./configure --shared --prefix=%{_prefix}
make libz.a
make

# We just want the shared library
mv libz.a libz-static.a
/usr/bin/ar -q libz.a libz.so.1

%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64
./configure --shared --prefix=%{prefix64}
make libz.a
make

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../..
/usr/bin/ar -q libz.a 64bit/%{name}-%{version}/libz.so.1

%endif #BUILD64


%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi
mkdir -p $RPM_BUILD_ROOT%{_prefix}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

install -m644 zutil.h ${RPM_BUILD_ROOT}%{prefix}/include/zutil.h
mkdir -p $RPM_BUILD_ROOT%{_prefix}/man/man3
install -m644 zlib.3 $RPM_BUILD_ROOT%{prefix}/man/man3
install -m755 libz.a $RPM_BUILD_ROOT%{prefix}/lib/libz.a

( cd $RPM_BUILD_ROOT/%{prefix}/lib
  rm libz.so*

  # Create a compatibility member to mitigate differences with Bull Freeware
  # offering
  COMPATMEMBER=shr.o
  for lib in *.a
  do
    /usr/bin/dump -X32 -Tv $lib |/usr/bin/awk 'match($4,"EXP|Exp") { print $NF }' > tmp.exp
    libbase=`print $lib | sed  -e 's/.a$//' -e 's/^lib//'`
    ld -L. -bI:tmp.exp -bE:tmp.exp -l$libbase -bM:SRE -bnoentry -o $COMPATMEMBER
    /usr/bin/strip -e $COMPATMEMBER   # Make shr.o a load-only module
    /usr/bin/ar -r $lib $COMPATMEMBER
    rm -f $COMPATMEMBER tmp.exp
  done
)

( cd $RPM_BUILD_ROOT
 mkdir -p usr/include
 cd usr/include
 ln -sf ../..%{prefix}/include/* .
 cd -

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
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
%defattr(-,root,system)
%{_prefix}/lib/libz*
%{_prefix}/64/lib/libz.a
/usr/lib/libz*
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif


%files devel
%defattr(-,root,system)
%doc README ChangeLog algorithm.txt FAQ
%{_includedir}/*
/usr/include/*
%{_mandir}/man3/zlib*
%changelog
*  Mon Sep 18 2006  BULL
 - Release  4
 - support 64 bits

*  Tue May 16 2006  BULL
 - Release  3

*  Fri Dec 23 2005  BULL
 - Release  2 
 - Prototype support gtk 64 bit

*  Wed Dec 07 2005  BULL
 - Release  1
 - New version  version: 1.2.3

