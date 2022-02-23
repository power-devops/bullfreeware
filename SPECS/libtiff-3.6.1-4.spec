%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: A library of functions for manipulating TIFF format image files.
Name: libtiff
Version: 3.6.1
Release: 4
License: distributable
Group: System Environment/Libraries
Source0: http://www.libtiff.org/tiff-%{version}.tar.bz2

Patch0:		tiff-3.6.1-aix.patch

URL: http://www.libtiff.org/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildRequires: zlib-devel zlib libjpeg-devel libjpeg
%define DEFCC cc

%description
The libtiff package contains a library of functions for manipulating 
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary: Development tools for programs which will use the libtiff library.
Group: Development/Libraries
Requires: libtiff

%description devel
This package contains the header files and static libraries for developing
programs which will manipulate TIFF format image files using the libtiff
library.  This package also requires the libtiff package.

%prep
%setup -q

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/tiff-3.6.1-aix.patch


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
       export CFLAGS="$RPM_OPT_FLAGS -qcpluscmt -DUSING_VISUALAGE"
fi
INSTDIR=%{_prefix}

./configure --with-GCOPTS="-s $CFLAGS" << EOF
no
$RPM_BUILD_ROOT/%{prefix}/bin
$RPM_BUILD_ROOT/%{prefix}/lib
$RPM_BUILD_ROOT/%{prefix}/include
$RPM_BUILD_ROOT/%{prefix}/man
$RPM_BUILD_ROOT/var/local/httpd/htdocs/tiff
bsd-source-cat
yes
EOF
make 

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi

INSTDIR=%{_prefix}
for dir in usr/lib usr/include usr/bin \
           .$INSTDIR/lib .$INSTDIR/include .$INSTDIR/bin .$INSTDIR/man/man1
do
   mkdir -p $RPM_BUILD_ROOT/$dir
done

make install
cd libtiff
install -m644 libtiff.a $RPM_BUILD_ROOT$INSTDIR/lib

strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

( cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)

%post
# Prototype support gtk 64 bit
mkdir -p /opt/freeware/64/lib
cd /opt/freeware/64/lib
ln -sf /opt/freeware/lib/libtiff.a .

%files
%defattr(0755,root,system)
%{_bindir}/*
/usr/bin/*
%{_libdir}/libtiff.a
/usr/lib/libtiff.a

%files devel
%defattr(-,root,system)
%doc COPYRIGHT README TODO VERSION html/*
%{_includedir}/*
/usr/include/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Mon May 25 2005  BULL
 - Release  1
 - New version  version: 3.6.1
