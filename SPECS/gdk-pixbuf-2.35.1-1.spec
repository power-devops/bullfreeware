# Version with/without AIX X11
%{!?aixX11:%define AIXX11 0}
%{?aixX11:%define AIXX11 1}

%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define _libdir64 %{_libdir}64

Name:           gdk-pixbuf
Version:        2.35.1
Release:        1%{RELEASE_SUFFIX}
Summary:        An image loading library

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.gt.org
Source0:        https://git.gnome.org/browse/gdk-pixbuf/snapshot/%{name}-%{version}.tar.xz

Patch0:         gdk-pixbuf-%{version}-linked-resources-aix.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
#		/var/opt/freeware/tmp/gdk-pixbuf-2.35.1-1-root

# From NEWS:
#2.21.3
#======
#gdk-pixbuf has been turned back into a standalone library, after being
#shipped as part of GTK+ for a number of years. The changes in this
#version, compared to the version included in GTK+ 2.20 are the following:
#* The default location for loaders has been changed to
#  $libdir/gdk-pixbuf-2.0/2.10.0/loaders
#* The default location for the module file has been changed to
#  $libdir/gdk-pixbuf-2.0/2.10.0/loaders.cache
#  and gdk-pixbuf-query-loaders-2.0 will update that file when given
#  the --update-cache option.
# GDK_PIXBUF_BINARY_VERSION=2.10.0 appears in configure file

%define LOADERS_LOCATION 2.10.0


# When --disable-introspection is used by configure:
%define with_introspection 0

BuildRequires:  glib2-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires: shared-mime-info
BuildRequires:  gettext-devel
#BuildRequires:  jasper-devel
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires:  libX11-devel
%endif
%if %{with_introspection}
BuildRequires:  gobject-introspection-devel
%endif
Requires: glib2
Requires: libpng
Requires: libjpeg
Requires: libtiff
Requires:  gettext
Requires: shared-mime-info >= 1.6

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2 <= 2.21.2

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

The library is available as 32-bit and 64-bit.
%if %{AIXX11} == 1
This package requires AIX X11.
%else
This package requires Bull Freeware X11.
%endif


%package devel
Summary: Development files for gdk-pixbuf
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: glib2-devel

# gdk-pixbuf was included in gtk2 until 2.21.2
Conflicts: gtk2-devel <= 2.21.2


%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.

Please note that if you want to build a program with linked GRessources
with xlC, you need to compile the ressource XML without constructors
(glib-compile-resources --manual-register) and to use the -binitfini
option of ld to call resources_register_resource and
resources_unregister_resource whene required :
-binitfini:resources_register_resource:resources_unregister_resource


%prep
# Need tar from /opt/freeware to extract xz archive
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
echo "AIXX11=%{AIXX11}"
echo "DO_TESTS=%{DO_TESTS}"
%setup -q
%patch0 -p1 -b .p0.aix

# resources.c/.h need to be rebuilt without constructor
rm -rf tests/resources.c
rm -rf tests/resources.h
# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build

export PATH=/usr/bin:/opt/freeware/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

export CC32="/usr/vac/bin/xlc_r"
export CXX32="/usr/vacpp/bin/xlC_r"
export CC64="$CC32 -q64"
export CXX64="$CXX32 -q64"

#export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
#export CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES -D_LARGEFILE_SOURCE"
#export LDFLAGS="-Wl,-brtl
#export CFLAGS="-g -qfullpath"
export CFLAGS="-g -O2"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC=$CC64
export LDFLAGS="-Wl,-bmaxdata:0x06FFFFFFFFFFFFF8"

configure					\
	   --prefix=%{_prefix}			\
	   --mandir=%{_prefix}/man		\
	   --libdir=%{_libdir64}		\
%if %{with_introspection}
	   --enable-introspection      		\
%endif
           --disable-gtk-doc            	\
           --with-x11		            	\
           --disable-rebuilds           	\
           --without-libjasper          	\
	   --enable-shared --enable-static	\
           --with-included-loaders=png

gmake %{?_smp_mflags}
#There is an issue with gmake on AIX, which use sh instead of bash like on Linux.
# for subdir in $(SUBDIRS) ; do   fails with sh since SUBDIRS is empty !
# Fixed by patch #3 about SUBDIRS
if [ "%{DO_TESTS}" == 1 ]
then
    #export GDK_PIXBUF_MODULE_FILE=`pwd`/gdk-pixbuf/loaders.cache
    ( gmake -k check || true )
fi
/usr/sbin/slibclean
cd ..

# build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CC="$CC32 -D_LARGE_FILES"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

configure					\
	   --prefix=%{_prefix}			\
	   --mandir=%{_prefix}/man		\
%if %{with_introspection}
	   --enable-introspection      		\
%endif
           --disable-gtk-doc            	\
           --with-x11		            	\
           --disable-rebuilds           	\
	   --enable-shared --enable-static	\
           --without-libjasper          	\
           --with-included-loaders=png

gmake %{?_smp_mflags}

#There is an issue with gmake on AIX, which use sh instead of bash like on Linux.
# for subdir in $(SUBDIRS) ; do   fails with sh since SUBDIRS is empty !
# Fixed by patch #3 about SUBDIRS
if [ "%{DO_TESTS}" == 1 ]
then
    #export GDK_PIXBUF_MODULE_FILE=`pwd`/gdk-pixbuf/loaders.cache
    ( gmake -k check || true )
fi
/usr/sbin/slibclean

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT
# This is required since libtool makes use of $RM in:
#      $RM ${realname}U
# where ${realname}U files may NOT exist
export RM="/usr/bin/rm -f"

# RPM_BUILD_ROOT depends on the value of: Buildroot
#echo "RPM_BUILD_ROOT         : " ${RPM_BUILD_ROOT}
#echo "RPM_BUILD_ROOT{_libdir}: " ${RPM_BUILD_ROOT}%{_libdir}
#echo "Buildroot:             : " %{_tmppath}/%{name}-%{version}-%{release}-root

# install 64-bit version
cd 64bit
export OBJECT_MODE=64

# trace : -d
gmake install DESTDIR=$RPM_BUILD_ROOT	\
             RUN_QUERY_LOADER_TEST=false
cd ..


# Rename 64 bits binaries
for f in ${RPM_BUILD_ROOT}%{_bindir}/* ; do
    mv ${f} ${f}_64
done

# # Save 64 bits shared objects to add them later to the 32_64 bits archives
cd ${RPM_BUILD_ROOT}/%{_libdir64}
for ARCHIVE in `ls -1 *.a`; do
    SO=`basename $ARCHIVE | sed -e "s/a\$/so.0/"`
    /usr/bin/ar -X64 xv $ARCHIVE $SO
done
cd -

# Extract loaders shared object, as they need to be in the package
cd ${RPM_BUILD_ROOT}/%{_libdir64}/gdk-pixbuf-2.0/2.10.0/loaders
for ARCHIVE in `ls -1 *.a`; do
    SO=`basename $ARCHIVE | sed -e "s/a\$/so/"`
    /usr/bin/ar -X64 xv $ARCHIVE $SO
done
cd -

# install 32-bit version
cd 32bit
export OBJECT_MODE=32

# trace : -d
gmake install DESTDIR=$RPM_BUILD_ROOT	\
             RUN_QUERY_LOADER_TEST=false
	     
# Add 64 bits shared object to archives and extract 32 bit shared objects
cd ${RPM_BUILD_ROOT}/%{_libdir}
for ARCHIVE in `ls -1 *.a`; do
    SO=`basename $ARCHIVE | sed -e "s/a\$/so.0/"`
    /usr/bin/ar -q -X64 $ARCHIVE ${RPM_BUILD_ROOT}/%{_libdir64}/$SO
    /usr/bin/ar -X32 xv $ARCHIVE $SO
done
cd -

cd ${RPM_BUILD_ROOT}/%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
# Extract loaders shared object, as they need to be in the package
for ARCHIVE in `ls -1 *.a`; do
    SO=`basename $ARCHIVE | sed -e "s/a\$/so/"`
    /usr/bin/ar -X32 xv $ARCHIVE $SO
done
cd -

touch ${RPM_BUILD_ROOT}%{_prefix}/lib64/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders.cache
touch ${RPM_BUILD_ROOT}%{_libdir}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders.cache

%find_lang gdk-pixbuf


%post
# Not on AIX:
#/sbin/ldconfig
#gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache
%{_bindir}/gdk-pixbuf-query-loaders     --update-cache


%postun
# Not on AIX:
#/sbin/ldconfig
if [ $1 -gt 0 ]; then
#  gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache
   %{_bindir}/gdk-pixbuf-query-loaders    --update-cache
fi


%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files -f 32bit/gdk-pixbuf.lang
%defattr(-,root,root,-)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/NEWS
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.so*
%{_bindir}/gdk-pixbuf-query-loaders*
%{_bindir}/gdk-pixbuf-pixdata*
%{_libdir}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.a
%{_libdir}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.so*
%{_libdir64}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.a
%{_libdir64}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.so*
%{_libdir}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.la
%{_libdir64}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders/*.la
%ghost %{_libdir}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders.cache
%ghost %{_libdir64}/gdk-pixbuf-2.0/%{LOADERS_LOCATION}/loaders.cache

%if %{with_introspection}
# When configure --enable-introspection
%{_libdir}/girepository-1.0
%endif

# _mandir  : /opt/freeware/man
# _datadir : /opt/freeware/share
# /opt/freeware/share/man/man1/
%{_mandir}/man1/gdk-pixbuf-query-loaders.1


%files devel
%defattr(-,root,root,-)
%{_includedir}/gdk-pixbuf-2.0
%{_libdir}/*.la
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-2.0.pc
%{_bindir}/gdk-pixbuf-csource*

%if %{with_introspection}
# When configure --enable-introspection
%{_datadir}/gir-1.0
%endif

%{_datadir}/gtk-doc/html/*

# ./docs/reference/gdk-pixbuf/Makefile :
#   datarootdir = ${prefix}/share
#   datadir = ${datarootdir}
#   mandir = ${datarootdir}/man
#   man1dir = $(mandir)/man1
%{_mandir}/man1/gdk-pixbuf-csource.1*


%changelog
* Tue May 03 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> 2.35.1-1
- Update to 2.35.1
- Build against AIX X11 or Bull Freeware X11

* Fri Apr 08 2016 Tony Reix <tony.reix@atos.net> 2.21.7-3
- Take into account 32 & 64 bits

* Wed Oct 08 2015 Tony Reix <tony.reix@atos.net> 2.21.7-1
- Update to 2.21.7 for AIX 6.1

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-2
- Rename to gdk-pixbuf2 to avoid conflict with the
  existing gdk-pixbuf package

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-1
- Update to 2.21.4
- Incorporate package review feedback

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.3-1
- Initial packaging
