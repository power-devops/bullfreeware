Summary: 	GNU libraries and utilities for producing multi-lingual messages.
Name: 		gettext
Version: 	0.17
Release:	7 
License: 	GPLv3 and LGPLv2+
Group: 		Development/Tools
URL: 		http://www.gnu.org/software/%{name}/
Source0: 	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}-ltaix.patch
Patch1:		%{name}-%{version}-aixconf.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

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
# Fix an issue during make install, when libtool was trying to relink  
# with a lib which doesn't exist
%patch0 -p1 -b .ltaix
%patch1 -p1 -b .aixconf

%build
# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export LIBPATH="/opt/freeware/lib:/usr/lib"

# first build the 64-bit version (-q64 for xlc, -maix64 for gcc)
# CC="/usr/vacpp/bin/xlc_r" defined in environment
# CXX="/usr/vacpp/bin/xlC" defined in environment


CFLAGS="-q64" \
CPPFLAGS="-I/opt/freeware/include" \
CXXFLAGS=" -q64" \
 ./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static --with-included-gettext
make %{?_smp_mflags}

cp ./gettext-runtime/intl/.libs/libintl.so.8 runtime-libintl.so.8
cp ./gettext-runtime/libasprintf/.libs/libasprintf.so.0 .
cp ./gettext-tools/libgettextpo/.libs/libgettextpo.so.0 .
cp ./gettext-tools/intl/.libs/libintl.so.8 tools-libintl.so.8
cp ./gettext-tools/gnulib-lib/.libs/libgettextlib-0.17.so .
cp ./gettext-tools/src/.libs/libgettextsrc-0.17.so .

make distclean

# now build the 32-bit version
#export CC="/usr/vacpp/bin/xlc_r"
#export CXX="/usr/vacpp/bin/xlC"
CPPFLAGS=" -I/opt/freeware/include" \
./configure \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static --with-included-gettext
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
mv ./runtime-libintl.so.8 ./libintl.so.8
${AR} -q ./gettext-runtime/intl/.libs/libintl.a ./libintl.so.8
${AR} -q ./gettext-runtime/libasprintf/.libs/libasprintf.a ./libasprintf.so.0
${AR} -q ./gettext-tools/libgettextpo/.libs/libgettextpo.a ./libgettextpo.so.0
mv ./tools-libintl.so.8 ./libintl.so.8
${AR} -q ./gettext-tools/intl/.libs/libintl.a ./libintl.so.8
${AR} -q ./gettext-tools/gnulib-lib/.libs/libgettextlib-0.17.a ./libgettextlib-0.17.so
${AR} -q ./gettext-tools/src/.libs/libgettextsrc-0.17.a ./libgettextsrc-0.17.so

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

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
# include old libintl.so.1 members for compatibility
cd /tmp/libintl.tmp
if test -e /tmp/libintl.tmp/libintl.so.1-32;then
cp -p libintl.so.1-32 libintl.so.1
echo "add libintl.so.1 (32bits) shared member to %{_libdir}/libintl.a"

	/usr/bin/ar -X32 -q %{_libdir}/libintl.a /tmp/libintl.tmp/libintl.so.1
fi
if test -e /tmp/libintl.tmp/libintl.so.1-64;then
cp -p libintl.so.1-64 libintl.so.1
	echo "add libintl.so.1 (64bits) shared member to  %{_libdir}/libintl.a"
	/usr/bin/ar -X64 -q %{_libdir}/libintl.a /tmp/libintl.tmp/libintl.so.1
fi
cd -
/usr/bin/rm -rf /tmp/libintl.tmp

/sbin/install-info %{_infodir}/gettext.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gettext.info.gz %{_infodir}/dir || :
fi

%pre
if test -e %{_libdir}/libintl.a; then
	cp -p %{_libdir}/libintl.a %{_libdir}/libintl.a.savgettext
fi
# extract old libintl.so.1 members for compatibility
/usr/bin/mkdir -p /tmp/libintl.tmp
cd /tmp/libintl.tmp
/usr/bin/ar -X32 -x %{_libdir}/libintl.a libintl.so.1
if test -e libintl.so.1; then
	cp -p libintl.so.1 libintl.so.1-32
fi
/usr/bin/ar -X64 -x %{_libdir}/libintl.a libintl.so.1
if test -e libintl.so.1; then
	cp -p libintl.so.1 libintl.so.1-64
fi
cd -

%postun
if test -e %{_libdir}/libintl.a.savgettext; then
	cp -p %{_libdir}/libintl.a.savgettext %{_libdir}/libintl.a
fi

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
%doc gettext-runtime/ABOUT-NLS AUTHORS gettext-runtime/BUGS
%doc COPYING gettext-tools/misc/DISCLAIM README
%doc NEWS THANKS
%doc gettext-runtime/man/*.1.html
%doc gettext-runtime/intl/COPYING*
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
%{_datadir}/locale/*
/usr/bin/[emnrx]*
/usr/bin/gettext
/usr/bin/gettext.sh
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc gettext-runtime/man/*.3.html ChangeLog
%doc gettext-runtime/intl-java/javadoc*
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
