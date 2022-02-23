# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler


# By defautl, use libxml provided with gettext to avoid dependency.
# Use system libxml: rpmbuild -ba --with libxml *.spec
%bcond_with system-libxml


%global tarversion 0.20.1
%global archiveversion 0.20

# Versions for version 0.19.8 :
%global	gettext_libintl_version		8
%global	gettext_libasprintf_version	0
%global	gettext_libgettextpo_version	0
%global	gettext_libtextstyle_version	0

%define		_libdir64 %{_prefix}/lib64

Summary: 	GNU libraries and utilities for producing multi-lingual messages.
Name: 		gettext
Version:    %{tarversion}
Release:	2
License: 	GPLv3 and LGPLv2+ and GFDL
Group: 		Development/Tools
URL: 		http://www.gnu.org/software/%{name}/
Source0:    https://ftp.gnu.org/pub/gnu/gettext/%{name}-%{version}.tar.xz

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

# Add wrongly made libintl.so.9 to ensure compatibily
Source103:	libintl.so.9-aix32
Source104:	libintl.so.9-aix64

Source201:	libgettextpo.so.0-aix32
Source202:	libgettextpo.so.0-aix64


Source1000:	%{name}-%{version}-%{release}.build.log


Patch0:		%{name}-%{version}-aixconf.patch
Patch1:		%{name}-%{version}-aixAddCast.patch

# Fix linking with shared libraries
Patch2:   %{name}-%{version}-configure-fix-shrext-for-AIX-without-brtl.patch
Patch3:   %{name}-%{version}-configure-fix-disable-rpath.patch

# Fix the libpath for test.
# Without this patch, libtool will add /opt/freeware/lib before
# $GETTEXT_DIR/gettext-tools/intl/.libs. Therefore, the wrong libintl.a will be taken
Patch4:     %{name}-%{version}-libtool-remove-duplicates-opt-freeware-in-libpath.patch

# Fix dependencies of libgettextlib.
# Without this patch, libtool will add -L/opt/freeware/lib before -lintl, resulting
# in a dependency over /opt/freeware/lib/libintl.a instead of the newly built libintl.a.
# This is a workaround, the correct fix must be in libtool I guess.
Patch5:     %{name}-%{version}-fix-iconv-and-intl-order-for-libgettexlib.patch

# In 32bit with -Wl,-bmaxdata, configure programs about getline and getdelim will succeed
# even if they should and must fail. Therefore, this patch force the use of GNU provided
# getline and getdelim.
Patch6:     %{name}-%{version}-configure-force-GNU-getline-and-getdelim.patch

# This version of xalloc.h is not including xaloc-oversized.h but it should.
Patch7:     %{name}-%{version}-fix-xalloc-oversized-duplicates.patch

BuildRequires: gcc-c++
# To create info.gz
BuildRequires: gzip
%if %{with system-libxml}
BuildRequires: libxml2-devel
%endif

# Gettext is now compiled with libunistring made with GCC.
# Versions before 0.9.9 were built with xlc.
BuildRequires: libunistring-devel => 0.9.9
Requires: libunistring => 0.9.9


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


%package -n libtextstyle
Summary: Text styling library
License: GPLv3+

%description -n libtextstyle
Library for producing styled text to be displayed in a terminal
emulator.


%package -n libtextstyle-devel
Summary: Development files for libtextstyle
License: GPLv3+ and GFDL
Requires: libtextstyle%{?_isa} = %{version}-%{release}

%description -n libtextstyle-devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs text
styling.

%prep

%if %{with dotests}
# Check that bos.loc.iso.fr_FR is installed for tests
if ! lslpp -L | grep -q "bos.loc.iso.fr_FR" ; then
	echo "Error: lpp bos.loc.iso.fr_FR must be installed to launch tests"
	echo "Aborting..."
	exit 1
fi
%endif


export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .aixconf
%patch1 -p1 -b .aixAddCast
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_BASE="-O2"

%if %{with gcc_compiler}
export __CC="gcc"
export __CXX="g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="xlc_r"
export __CXX="xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"
# CFLAGS_BASE="$CFLAGS_BASE -qlanglvl=stdc99 -qaggrcopy=nooverlap -DSYSV -D_AIX -D_AIX32 -D_AIX41 -D_AIX43 -D_AIX51 -D_AIX61 -D_ALL_SOURCE -DFUNCPROTO=15"
export CFLAGS_BASE="$CFLAGS_BASE -qlanglvl=stdc99 -qaggrcopy=nooverlap"

%endif

# # Required for compiling gettext WITH iconv
# export LIBS="-L/opt/freeware/lib /opt/freeware/lib/libiconv.a"

# That breaks: /usr/bin/perl -w -- ./help2man --include=./msgcmp.x ../src/msgcmp
# -I/opt/freeware/include is required in order to get the /opt/freeware version of iconv.h !!
export CPPFLAGS="-I/opt/freeware/include"


build_gettext() {
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--infodir=%{_infodir} \
		--mandir=%{_mandir} \
		--enable-shared --disable-static --with-included-gettext \
		--disable-rpath \
%if %{without system-libxml}
	    --with-included-libxml \
%endif

	gmake %{?_smp_mflags}
}


# first build the 64-bit version (-q64 for xlc, -maix64 for gcc)
cd 64bit
export OBJECT_MODE=64
export CC="$__CC $FLAG64"
export CXX="$__CXX $FLAG64"
export CFLAGS="$CFLAGS_BASE"
export CXXFLAGS="$CFLAGS_BASE"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_gettext %{_libdir64}



# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32

export CC="$__CC $FLAG32"
export CXX="$__CXX $FLAG32"
export CFLAGS="$CFLAGS_BASE"
export CXXFLAGS="$CFLAGS_BASE"

export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_gettext %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 64bit binaries' name
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)
cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 32bit binaries' name and make default link towards 64bit
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in $(ls | grep -v -e _32 -e _64)
	do
		mv ${f} ${f}_32
		ln -sf ${f}_64 ${f}
	done
)

(
	# Remove version in archives' name. It won't allow compatibility
	cd ${RPM_BUILD_ROOT}%{_libdir}
	mv libgettextlib-%{version}.a libgettextlib.a
	mv libgettextsrc-%{version}.a libgettextsrc.a
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	mv libgettextlib-%{version}.a libgettextlib.a
	mv libgettextsrc-%{version}.a libgettextsrc.a
)

(
	# Extract .so from 64bit .a libraries and create links from /lib64 to /lib
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	for f in lib*.a ; do
		${AR} -x ${f}
		rm -f ${f}
		ln -sf ../lib/${f} ${f}
	done
)

(
	# Add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
	cd ${RPM_BUILD_ROOT}%{_libdir}
	/usr/bin/ar -X64 -q libasprintf.a    ${RPM_BUILD_ROOT}%{_libdir64}/libasprintf.so.%{gettext_libasprintf_version}
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libasprintf.so.%{gettext_libasprintf_version}

	/usr/bin/ar -X64 -q libgettextpo.a   ${RPM_BUILD_ROOT}%{_libdir64}/libgettextpo.so.%{gettext_libgettextpo_version}
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libgettextpo.so.%{gettext_libgettextpo_version}

	/usr/bin/ar -X64 -q libgettextlib.a  ${RPM_BUILD_ROOT}%{_libdir64}/libgettextlib-%{version}.so
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libgettextlib-%{version}.so

	/usr/bin/ar -X64 -q libgettextsrc.a  ${RPM_BUILD_ROOT}%{_libdir64}/libgettextsrc-%{version}.so
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libgettextsrc-%{version}.so

	/usr/bin/ar -X64 -q libintl.a        ${RPM_BUILD_ROOT}%{_libdir64}/libintl.so.%{gettext_libintl_version}
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libintl.so.%{gettext_libintl_version}

	/usr/bin/ar -X64 -q libtextstyle.a   ${RPM_BUILD_ROOT}%{_libdir64}/libtextstyle.so.%{gettext_libtextstyle_version}
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libtextstyle.so.%{gettext_libtextstyle_version}
)

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

# libintl       32bits v9 -> to ensure compatibility
cp %{SOURCE103}                                                    libintl.so.9
/usr/bin/strip -X32 -e                                             libintl.so.9
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.9

# libintl       64bits v9 -> to ensure compatibility
cp %{SOURCE104}                                                    libintl.so.9
/usr/bin/strip -X64 -e                                             libintl.so.9
/usr/bin/ar    -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libintl.a       libintl.so.9

# libgettextpo  32bits
cp %{SOURCE201}                                                    libgettextpo.so.0
/usr/bin/strip -X32 -e                                             libgettextpo.so.0
/usr/bin/ar    -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libgettextpo.a  libgettextpo.so.0

# libgettextpo  64bits
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

# own this directory for third-party *.its files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/its


# doc relocations
for i in gettext-runtime/man/*.html; do
	rm ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/`basename $i`
done
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/javadoc*

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/* ${RPM_BUILD_ROOT}/%{_datadir}/doc/libasprintf/* htmldoc
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/libtextstyle ${RPM_BUILD_ROOT}%{_docdir}


# Create link for /usr/lib/libintl.a.
# It's needed by older python3's libraries which don't have a correct LIBPATH.
# Fixed after python3-3.7.4-4
# TODO: remove one day
(
	mkdir -p ${RPM_BUILD_ROOT}/usr/lib
	cd ${RPM_BUILD_ROOT}/usr/lib
	ln -sf ../..%{_prefix}/lib/libintl.a .
)


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)

%post

/sbin/install-info %{_infodir}/gettext.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gettext.info.gz %{_infodir}/dir || :
fi

# The gettext version provided by AIXToolbox in their yum_bundle.tar
# is saving the original AIX libintl.a into libintl.a.savgettext and
# restoring in their %postun. It was meant to avoid breakages of RPMs
# when removing gettext.
# However, the script is no longer needed and handles the same way
# upgrading and removing. Thus, if libintl.a.savgettext is presented
# when upgrading to a new gettext, the new libintl.a will be overridden
# by the old save (because %postun is the last script being run during
# an upgrade).
# Thus, removing libintl.a.savgettext avoids the restoration of the old
# libintl.a.
if test -e %{_libidr}/libintl.a.savgettext; then
	rm -f %{_libdir}/libintl.a.savgettext
fi


%post devel
/sbin/install-info %{_infodir}/autosprintf.info.gz %{_infodir}/dir || :


%preun devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/autosprintf.info.gz %{_infodir}/dir || :
fi

%post -n libtextstyle-devel
/sbin/install-info %{_infodir}/libtextstyle.info.gz %{_infodir}/dir || :


%preun -n libtextstyle-devel
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/libtextstyle.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/gettext-runtime/ABOUT-NLS 32bit/AUTHORS 32bit/gettext-runtime/BUGS
%doc 32bit/COPYING 32bit/gettext-tools/misc/DISCLAIM 32bit/README
%doc 32bit/NEWS 32bit/THANKS
%doc 32bit/gettext-runtime/man/*.1.html
%doc 32bit/gettext-runtime/intl/COPYING*
%{_bindir}/envsubst*
%{_bindir}/gettext*
%{_bindir}/gettext.sh*
%{_bindir}/msgattrib*
%{_bindir}/msgcat*
%{_bindir}/msgcmp*
%{_bindir}/msgcomm*
%{_bindir}/msgconv*
%{_bindir}/msgen*
%{_bindir}/msgexec*
%{_bindir}/msgfilter*
%{_bindir}/msgfmt*
%{_bindir}/msggrep*
%{_bindir}/msginit*
%{_bindir}/msgmerge*
%{_bindir}/msgunfmt*
%{_bindir}/msguniq*
%{_bindir}/ngettext*
%{_bindir}/recode-sr-latin*
%{_bindir}/xgettext*

%{_libdir}/%{name}
%{_libdir}/libintl.a
%{_libdir}/libasprintf.a
%{_libdir}/libgettextpo.a
%{_libdir}/libgettextlib*.a
%{_libdir}/libgettextsrc*.a

%{_libdir64}/%{name}
%{_libdir64}/libintl.a
%{_libdir64}/libasprintf.a
%{_libdir64}/libgettextpo.a
%{_libdir64}/libgettextlib*.a
%{_libdir64}/libgettextsrc*.a

/usr/lib/libintl.a

%exclude %{_mandir}/man1/autopoint.1*
%exclude %{_mandir}/man1/gettextize.1*
%{_mandir}/man1/*
%{_infodir}/gettext*

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/its
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/po
%{_datadir}/%{name}/styles
%dir %{_datadir}/%{name}-%{archiveversion}
%{_datadir}/%{name}-%{archiveversion}/its

%{_datadir}/locale/*/LC_MESSAGES/*


%files devel
%defattr(-,root,system,-)
%doc 32bit/gettext-runtime/man/*.3.html 32bit/ChangeLog
%doc 32bit/gettext-runtime/intl-java/javadoc*
%{_bindir}/autopoint*
%{_bindir}/gettextize*
%{_includedir}/autosprintf.h
%{_includedir}/gettext-po.h
%{_includedir}/libintl.h
%{_mandir}/man1/autopoint.1
%{_mandir}/man1/gettextize.1
%{_mandir}/man3/*
%{_infodir}/autosprintf*
%{_datadir}/aclocal/*
%{_datadir}/%{name}/javaversion.class

%files -n libtextstyle
%defattr(-,root,system,-)
%{_libdir}/libtextstyle.a

%files -n libtextstyle-devel
%defattr(-,root,system,-)
%{_docdir}/libtextstyle/
%{_includedir}/textstyle/
%{_includedir}/textstyle.h
%{_infodir}/libtextstyle*


%changelog
* Thu Jul 09 2020 Clément Chigot <clement.chigot@atos.net - 0.20.1-2
- Add handler in %pre when installing BullFreeware gettext other old
  AIXToolbox version.

* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net - 0.20.1-1
- BullFreeware Compatibility Improvements
- Build with gcc
- Move tests to %check section
- Fix compatibility issue with libintl.so.9. Now, the default is libintl.so.8 and libintl.so.9 is provided to ensure compatibility with programs made with the wrong libintl.so.9.
- Rename libgettext(src|lib)-%{version}.a by libgettext(src|lib).a in order to improve compatibility.
- Add libtextstyle{,-devel} subpackages
- Improve files delivered
- own .../gettext/its for third-party *.its files
- Remove dependency on libxml
- Fix configure for AIX shared libraries
- Fix info.gz installation
- Remove /usr links expect /usr/lib/libintl.a which is used by older releases of python3.

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
