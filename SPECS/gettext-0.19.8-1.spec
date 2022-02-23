# rpm -ba --define 'dotests 0' gettext-0.19.7-1.spec ...
# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# Versions for version 0.19.8 :
%global	gettext_libintl_version		9
%global	gettext_libasprintf_version	0
%global	gettext_libgettextpo_version	1
# Was : 8 0 0 for version 0.19.7

Summary: 	GNU libraries and utilities for producing multi-lingual messages.
Name: 		gettext
Version: 	0.19.8
Release:	1
License: 	GPLv3 and LGPLv2+
Group: 		Development/Tools
URL: 		http://www.gnu.org/software/%{name}/
Source0: 	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Source1:	libgettextlib-0.17.so-aix32
Source2:	libgettextlib-0.17.so-aix64
Source3:	libgettextsrc-0.17.so-aix32
Source4:	libgettextsrc-0.17.so-aix64

Source5:	libgettextlib-0.18.3.so-aix32
Source6:	libgettextlib-0.18.3.so-aix64
Source7:	libgettextsrc-0.18.3.so-aix32
Source8:	libgettextsrc-0.18.3.so-aix64

Source9:	libgettextlib-0.19.7.so-aix32
Source10:	libgettextlib-0.19.7.so-aix64
Source11:	libgettextsrc-0.19.7.so-aix32
Source12:	libgettextsrc-0.19.7.so-aix64

Source101:	libintl.so.1-aix32
Source102:	libintl.so.1-aix64

Source103:	libintl.so.8-aix32
Source104:	libintl.so.8-aix64

Source201:	libgettextpo.so.0-aix32
Source202:	libgettextpo.so.0-aix64


Source1000:	%{name}-%{version}-%{release}.build.log


Patch0:		%{name}-%{version}-aixconf.patch
Patch1:		%{name}-%{version}-aixAddCast.patch

Requires:	ncurses
BuildRequires:	emacs, groff

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%define		_libdir64 %{_prefix}/lib64

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.

The library is available as 32-bit and 64-bit.


%package devel
Summary:	Development files for %{name}
Group:		Development/Tools
License:	LGPLv2+
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .aixconf
%patch1 -p1 -b .aixAddCast

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
# setup environment for 32-bit and 64-bit builds
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

export CONFIG_SHELL=/usr/bin/sh
CONFIG_ENV_ARGS=/usr/bin/sh

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"

# Required for compiling gettext WITH iconv in 64 bits ONLY, so that 33 tests succeed
export LIBS="-L/opt/freeware/lib /opt/freeware/lib/libiconv.a"

# That breaks: /usr/bin/perl -w -- ./help2man --include=./msgcmp.x ../src/msgcmp
#export CPPFLAGS="-I/opt/freeware/include"

export LDFLAGS="-Wl,-bmaxdata:0x80000000"

#CFLAGS_BASE="-g"
CFLAGS_BASE="-O2"
CFLAGS_BASE="$CFLAGS_BASE -qlanglvl=stdc99 -qaggrcopy=nooverlap -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15"

# first build the 64-bit version (-q64 for xlc, -maix64 for gcc)
export OBJECT_MODE=64
cd 64bit

# -I/opt/freeware/include is required in order to get the /opt/freeware version of iconv.h !!
CFLAGS="  $CFLAGS_BASE -q64" \
CXXFLAGS="$CFLAGS_BASE -q64" \
CPPFLAGS="-I/opt/freeware/include" \
 ./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static --with-included-gettext

gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


# now build the 32-bit version
export OBJECT_MODE=32
cd ../32bit

export CFLAGS="  $CFLAGS_BASE -q32"
export CXXFLAGS="$CFLAGS_BASE -q32"

# A specific LIBS is ALSO required for compiling gettext WITH iconv in 32 bits and WITH /opt/freeware/lib version !!
export LIBS="-L/opt/freeware/lib /opt/freeware/lib/libiconv.a"



# -I/opt/freeware/include is required in order to get the /opt/freeware version of iconv.h !!

CFLAGS="  $CFLAGS_BASE -q32" \
CXXFLAGS="$CFLAGS_BASE -q32" \
CPPFLAGS="-I/opt/freeware/include" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static --with-included-gettext


# LIBPATH is required for building version 0.19.8 when version 0.19.7 is installed
#   Plus: ar -q /opt/freeware/lib/libgettextlib.a /opt/freeware/src/packages/BUILD/gettext-0.19.8/32bit/gettext-tools/gnulib-lib/.libs/libgettextlib-0.19.8.so
# Issue when building, in 32bit only:
#	 ../src/recode-sr-latin --help
#	Could not load program /opt/freeware/src/packages/BUILD/gettext-0.19.8/32bit/gettext-tools/src/.libs/lt-recode-sr-latin:
#	Could not load module /opt/freeware/lib/libglib-2.0.a(libglib-2.0.so.0).
#        	Dependent module /opt/freeware/src/packages/BUILD/gettext-0.19.8/32bit/gettext-tools/intl/.libs/libintl.a(libintl.so.8) could not be loaded.
#        	Member libintl.so.8 is not found in archive 

LIBPATH=/opt/freeware/lib:/usr/lib:/opt/freeware/src/packages/BUILD/gettext-%{version}/32bit/gettext-tools/intl/.libs \
gmake %{?_smp_mflags}

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# install 64-bit version

export OBJECT_MODE=64
cd 64bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install


# install 32-bit version

export OBJECT_MODE=32
cd ../32bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install


cd ${RPM_BUILD_ROOT}%{_libdir64}
for f in ${RPM_BUILD_ROOT}%{_libdir64}/lib*.a ; do
    /usr/bin/ar -X64 -x ${f}
done
cd -

# Add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libasprintf.a              ${RPM_BUILD_ROOT}%{_libdir64}/libasprintf.so.%{gettext_libasprintf_version}
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextpo.a             ${RPM_BUILD_ROOT}%{_libdir64}/libgettextpo.so.%{gettext_libgettextpo_version}

/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib-%{version}.a ${RPM_BUILD_ROOT}%{_libdir64}/libgettextlib-%{version}.so
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc-%{version}.a ${RPM_BUILD_ROOT}%{_libdir64}/libgettextsrc-%{version}.so

/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a                  ${RPM_BUILD_ROOT}%{_libdir64}/libintl.so.%{gettext_libintl_version}


# Now libgettextlib.a and libgettextsrc.a are no more symbolic links to libgettext???-%{version}.a
#   in order to add the older versions to the .a

rm -f                                                     ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a
cp ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib-%{version}.a ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a
rm -f                                                     ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a
cp ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc-%{version}.a ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a

# libgettextlib 32bits
cp %{SOURCE1}                                                      libgettextlib-0.17.so
/usr/bin/strip -X32 -e                                             libgettextlib-0.17.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.17.so
cp %{SOURCE5}                                                      libgettextlib-0.18.3.so
/usr/bin/strip -X32 -e                                             libgettextlib-0.18.3.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.18.3.so
cp %{SOURCE9}                                                      libgettextlib-0.19.7.so
/usr/bin/strip -X32 -e                                             libgettextlib-0.19.7.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.19.7.so

# libgettextlib 64bits
cp %{SOURCE2}                                                      libgettextlib-0.17.so
/usr/bin/strip -X64 -e                                             libgettextlib-0.17.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.17.so
cp %{SOURCE6}                                                      libgettextlib-0.18.3.so
/usr/bin/strip -X64 -e                                             libgettextlib-0.18.3.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.18.3.so
cp %{SOURCE10}                                                     libgettextlib-0.19.7.so
/usr/bin/strip -X64 -e                                             libgettextlib-0.19.7.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextlib.a libgettextlib-0.19.7.so

# libgettextsrc 32bits
cp %{SOURCE3}                                                      libgettextsrc-0.17.so
/usr/bin/strip -X32 -e                                             libgettextsrc-0.17.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.17.so
cp %{SOURCE7}                                                      libgettextsrc-0.18.3.so
/usr/bin/strip -X32 -e                                             libgettextsrc-0.18.3.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.18.3.so
cp %{SOURCE11}                                                     libgettextsrc-0.19.7.so
/usr/bin/strip -X32 -e                                             libgettextsrc-0.19.7.so
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.19.7.so

# libgettextsrc 64bits
cp %{SOURCE4}                                                      libgettextsrc-0.17.so
/usr/bin/strip -X64 -e                                             libgettextsrc-0.17.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.17.so
cp %{SOURCE8}                                                      libgettextsrc-0.18.3.so
/usr/bin/strip -X64 -e                                             libgettextsrc-0.18.3.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.18.3.so
cp %{SOURCE12}                                                     libgettextsrc-0.19.7.so
/usr/bin/strip -X64 -e                                             libgettextsrc-0.19.7.so
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextsrc.a libgettextsrc-0.19.7.so

# libintl       32bits v1
cp %{SOURCE101}                                                    libintl.so.1
/usr/bin/strip -X32 -e                                             libintl.so.1
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.1

# libintl       64bits v1
cp %{SOURCE102}                                                    libintl.so.1
/usr/bin/strip -X64 -e                                             libintl.so.1
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.1

# libintl       32bits v8
cp %{SOURCE103}                                                    libintl.so.8
/usr/bin/strip -X32 -e                                             libintl.so.8
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.8

# libintl       64bits v8
cp %{SOURCE104}                                                    libintl.so.8
/usr/bin/strip -X64 -e                                             libintl.so.8
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.8

# libgettextpo  32bits v8
cp %{SOURCE201}                                                    libgettextpo.so.0
/usr/bin/strip -X32 -e                                             libgettextpo.so.0
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextpo.a  libgettextpo.so.0

# libgettextpo  64bits v8
cp %{SOURCE202}                                                    libgettextpo.so.0
/usr/bin/strip -X64 -e                                             libgettextpo.so.0
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextpo.a  libgettextpo.so.0


# (non-blocking) issue with:
#	opt/freeware/bin/autopoint	: missing (in -devel package)
#	opt/freeware/bin/gettextize	: missing (in -devel package)
#	opt/freeware/bin/gettext.sh	: not executable
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

# Fix relink issue ????????????
#cp -p -f ./gettext-runtime/intl/.libs/libintl.a			 ${RPM_BUILD_ROOT}%{_libdir}
#cp -p -f ./gettext-runtime/libasprintf/.libs/libasprintf.a		 ${RPM_BUILD_ROOT}%{_libdir}
#cp -p -f ./gettext-tools/libgettextpo/.libs/libgettextpo.a		 ${RPM_BUILD_ROOT}%{_libdir}
#cp -p -f ./gettext-tools/gnulib-lib/.libs/libgettextlib-%{version}.a	 ${RPM_BUILD_ROOT}%{_libdir}
#cp -p -f ./gettext-tools/src/.libs/libgettextsrc-%{version}.a		 ${RPM_BUILD_ROOT}%{_libdir}
#cp -p -f ./gettext-tools/intl/.libs/libintl.a				 ${RPM_BUILD_ROOT}%{_libdir}

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


%post

# That creates an issue with libintl.a busy.
#
#	# include old libintl.so.1 members for compatibility
#	cd /tmp/libintl.tmp
#	if test -e /tmp/libintl.tmp/libintl.so.1-32;then
#		cp -p libintl.so.1-32 libintl.so.1
#		echo "add libintl.so.1 (32bits) shared member to %{_libdir}/libintl.a"
#		/usr/bin/ar -X32 -q %{_libdir}/libintl.a /tmp/libintl.tmp/libintl.so.1
#	fi
#	
#	if test -e /tmp/libintl.tmp/libintl.so.1-64;then
#		cp -p libintl.so.1-64 libintl.so.1
#		echo "add libintl.so.1 (64bits) shared member to  %{_libdir}/libintl.a"
#		/usr/bin/ar -X64 -q %{_libdir}/libintl.a /tmp/libintl.tmp/libintl.so.1
#	fi
#	cd -
#	/usr/bin/rm -rf /tmp/libintl.tmp

/sbin/install-info %{_infodir}/gettext.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gettext.info.gz %{_infodir}/dir || :
fi


# That creates an issue with libintl.a busy.
#
#	%pre
#	if test -e %{_libdir}/libintl.a; then
#		cp -p %{_libdir}/libintl.a %{_libdir}/libintl.a.savgettext
#	fi
#	# extract old libintl.so.1 members for compatibility
#	/usr/bin/mkdir -p /tmp/libintl.tmp
#	cd /tmp/libintl.tmp
#	/usr/bin/ar -X32 -x %{_libdir}/libintl.a libintl.so.1
#	if test -e libintl.so.1; then
#		cp -p libintl.so.1 libintl.so.1-32
#	fi
#	/usr/bin/ar -X64 -x %{_libdir}/libintl.a libintl.so.1
#	if test -e libintl.so.1; then
#		cp -p libintl.so.1 libintl.so.1-64
#	fi
#	cd -
#	
#	
#	%postun
#	if test -e %{_libdir}/libintl.a.savgettext; then
#		cp -p %{_libdir}/libintl.a.savgettext %{_libdir}/libintl.a
#	fi


%post devel
/sbin/install-info %{_infodir}/autosprintf.info.gz %{_infodir}/dir || :


%preun devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/autosprintf.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/gettext-runtime/ABOUT-NLS 32bit/AUTHORS 32bit/gettext-runtime/BUGS
%doc 32bit/COPYING 32bit/gettext-tools/misc/DISCLAIM 32bit/README
%doc 32bit/NEWS 32bit/THANKS
%doc 32bit/gettext-runtime/man/*.1.html
%doc 32bit/gettext-runtime/intl/COPYING*
%{_bindir}/[emnrx]*
%{_bindir}/gettext
%{_bindir}/gettext.sh
%{_libdir}/libintl.a
%{_libdir}/libgettextlib*.a
%{_libdir}/libgettextsrc*.a
%{_libdir}/%{name}
%{_infodir}/gettext*
%{_mandir}/man1/[emnrx]*
%{_mandir}/man1/gettext.1
%{_datadir}/locale/*/LC_MESSAGES/*
/usr/bin/[emnrx]*
/usr/bin/gettext
/usr/bin/gettext.sh
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/gettext-runtime/man/*.3.html 32bit/ChangeLog
%doc 32bit/gettext-runtime/intl-java/javadoc*
%{_bindir}/autopoint
%{_bindir}/gettextize
%{_includedir}/*
%{_libdir}/libasprintf.a
%{_libdir}/libgettextpo.a
%{_libdir}/*.la
%{_mandir}/man1/autopoint.1
%{_mandir}/man1/gettextize.1
%{_mandir}/man3/*
%{_infodir}/autosprintf*
%{_datadir}/aclocal/*
%{_datadir}/%{name}
/usr/bin/autopoint
/usr/bin/gettextize
/usr/include/*
/usr/lib/libasprintf.a
/usr/lib/libgettextpo.a
/usr/lib/*.la


%changelog
* Wed Mar 08 2017 Tony Reix <tony.reix@atos.net> 0.19.8-1
- Update to version 0.19.8
- Manage issue with libiconv.a (/usr/lib vs /opt/freeware/lib)
- Manage compatibility with version 0.19.7 : libintl.so.8 & Co
- Add libintl.so.1 to the compatibility managed .so files

* Tue May 10 2016 Tony Reix <tony.reix@atos.net> 0.19.7-2
- Add old .so files in .a for compatibility.

* Tue Apr 26 2016 Tony Reix <tony.reix@atos.net> 0.19.7-1
- Update to version 0.19.7

* Mon Oct 19 2015 Tony Reix <tony.reix@atos.net> 0.19.6-1
- Update to version 0.19.6

* Wed Sep 11 2013 Gerard Visiedo <gerard.visiedo@bull.net> 0.18.3.1-1
- Update to version 0.18.3.1

* Mon Jan 30 2012 Patricia Cugny <patricia.cugny@bull.net> 0.17-7
- Add patch for building on aix 6.1

* Wed Aug 31 2011 Patricia Cugny <patricia.cugny@bull.net> 0.17-6
- Add installed libintl.so.1 to libintl.a lib

* Wed May 04 2011 Patricia Cugny <patricia.cugny@bull.net> 0.17-5
- Add 64bits library and older libintl.so.1

* Mon Mar 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> 0.17-4
- Add patches for workaround bugs on aix6

* Thu Jan 27 2011 Jean-noel Cordenner <jean-noel.cordenner@bull.net> 0.17-3
- add missing files

* Thu Apr 23 2009 Jean-noel Cordenner <jean-noel.cordenner@bull.net> 0.17-2
- add %pre and %postun scripts to preserve previous version of libintl.a

* Wed Mar 18 2009 Jean-noel Cordenner <jean-noel.cordenner@bull.net> 0.17
- port to AIX
