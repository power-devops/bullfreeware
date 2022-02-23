Summary: A library for editing typed command lines
Name: readline
Version: 6.3
Release: 1
License: GPLv2+
Group: System Environment/Libraries
URL: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Source2: libreadline.so.4-aix32
Source3: libreadline.so.4-aix64
Source4: libhistory.so.4-aix32
Source5: libhistory.so.4-aix64
Source6: libreadline.so.5-aix32
Source7: libreadline.so.5-aix64
Source8: libhistory.so.5-aix32
Source9: libhistory.so.5-aix64

# Official upstream patches
Patch1: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-001.patch
Patch2: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-002.patch
Patch3: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-003.patch
Patch4: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-004.patch
Patch5: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-005.patch
Patch6: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-006.patch
Patch7: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-007.patch
Patch8: ftp://ftp.gnu.org/gnu/readline/readline-6.3-patches/readline63-008.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%define major 6

BuildRequires: patch
Requires: /sbin/install-info, info

%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Files needed to develop programs which use the readline library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: /sbin/install-info, info

%description devel
The Readline library provides a set of functions that allow users to
edit typed command lines. If you want to develop programs that will
use the readline library, you need to have the readline-devel package
installed. You also need to have the readline package installed.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc -q64" or "gcc -maix64".


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
# Official upstream patches
%patch1 -p0 -b .001
%patch2 -p0 -b .002
%patch3 -p0 -b .003
%patch4 -p0 -b .004
%patch5 -p0 -b .005
%patch6 -p0 -b .006


%build
export PATH=/usr/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
#export AR="ar -X32_64"
export AR="/usr/bin/ar -X32_64"
export NM="nm -X32_64"
export LDFLAGS="-L/opt/freeware/lib"

# first build the 64-bit version
export OBJECT_MODE="64"
export CC="xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static
make %{?_smp_mflags}

mkdir 64bit

cp shlib/libhistory.so.6 64bit/
cp shlib/libreadline.so.6 64bit/
make distclean

# now build the 32-bit version
export OBJECT_MODE="32"
export CC="xlc_r"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static
make %{?_smp_mflags}

# Create the archives
rm -f libhistory.a libreadline.a
${AR} -rv libhistory.a  shlib/libhistory.so.%{major}
${AR} -rv libreadline.a shlib/libreadline.so.%{major}

# add 64-bit shared objects to library
${AR} -q libhistory.a  64bit/libhistory.so.%{major}
${AR} -q libreadline.a 64bit/libreadline.so.%{major}

# Add the older version 4 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libreadline.so.4
/usr/bin/strip -X32 libreadline.so.4
/usr/bin/ar -X32 -q libreadline.a libreadline.so.4

cp %{SOURCE3} libreadline.so.4
/usr/bin/strip -X64 libreadline.so.4
/usr/bin/ar -X64 -q libreadline.a libreadline.so.4

cp %{SOURCE4} libhistory.so.4
/usr/bin/strip -X32 -e libhistory.so.4
/usr/bin/ar -X32 -q libhistory.a libhistory.so.4

cp %{SOURCE5} libhistory.so.4
/usr/bin/strip -X64 -e libhistory.so.4
/usr/bin/ar -X64 -q libhistory.a libhistory.so.4

# Add the older version 5 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE6} libreadline.so.5
/usr/bin/strip -X32 libreadline.so.5
/usr/bin/ar -X32 -q libreadline.a libreadline.so.5

cp %{SOURCE7} libreadline.so.5
/usr/bin/strip -X64 libreadline.so.5
/usr/bin/ar -X64 -q libreadline.a libreadline.so.5

cp %{SOURCE8} libhistory.so.5
/usr/bin/strip -X32 -e libhistory.so.5
/usr/bin/ar -X32 -q libhistory.a libhistory.so.5

cp %{SOURCE9} libhistory.so.5
/usr/bin/strip -X64 libhistory.so.5
/usr/bin/ar -X64 -q libhistory.a libhistory.so.5


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*so.%{major}
cp lib*.a ${RPM_BUILD_ROOT}%{_libdir}
chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

cd doc
make info
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

(
  cd ${RPM_BUILD_ROOT}
  for dir in include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%post
/sbin/install-info %{_infodir}/history.info.gz %{_infodir}/dir
/sbin/install-info %{_infodir}/rluserman.info.gz %{_infodir}/dir
exit 0


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/history.info.gz %{_infodir}/dir
   /sbin/install-info --delete %{_infodir}/rluserman.info.gz %{_infodir}/dir
fi
exit 0


%post devel
/sbin/install-info %{_infodir}/readline.info.gz %{_infodir}/dir || :


%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/readline.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc CHANGES COPYING NEWS README USAGE
%{_libdir}/*.a
%{_infodir}/history.info*
%{_infodir}/rluserman.info*
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc examples/*.c examples/*.h examples/rlfe
%{_includedir}/readline
%{_mandir}/man3/*
%{_infodir}/readline.info*
/usr/include/*


%changelog
* Wed Mar 16 2016 Tony Reix <tony.reix@atos.net> - 6.3-1
- Version 6.3 patch level 8

* Fri Aug 15 2014 Michael Perzl <michael@perzl.org> - 6.3-5
- updated to version 6.3 patch level 8

* Mon May 19 2014 Michael Perzl <michael@perzl.org> - 6.3-4
- updated to version 6.3 patch level 6

* Sun Apr 27 2014 Michael Perzl <michael@perzl.org> - 6.3-3
- updated to version 6.3 patch level 5

* Fri Mar 27 2014 Michael Perzl <michael@perzl.org> - 6.3-2
- updated to version 6.3 patch level 3

* Wed Feb 26 2014 Michael Perzl <michael@perzl.org> - 6.3-1
- updated to version 6.3

* Wed Nov 20 2013 Michael Perzl <michael@perzl.org> - 6.2-5
- updated to version 6.2 patch level 5

* Wed Jul 18 2012 Michael Perzl <michael@perzl.org> - 6.2-4
- updated to version 6.2 patch level 4

* Tue Jan 31 2012 Michael Perzl <michael@perzl.org> - 6.2-3
- updated to version 6.2 patch level 2

* Tue Mar 01 2011 Michael Perzl <michael@perzl.org> - 6.2-2
- updated to version 6.2 patch level 1

* Tue Feb 15 2011 Michael Perzl <michael@perzl.org> - 6.2-1
- updated to version 6.2

* Wed Feb 24 2010 Michael Perzl <michael@perzl.org> - 6.1-3
- updated to version 6.1 patch level 2

* Tue Jan 19 2010 Michael Perzl <michael@perzl.org> - 6.1-2
- updated to version 6.1 patch level 1

* Mon Jan 11 2010 Michael Perzl <michael@perzl.org> - 6.1-1
- updated to version 6.1

* Tue Sep 01 2009 Michael Perzl <michael@perzl.org> - 6.0-2
- updated to latest fixes for version 6.0

* Mon Mar 30 2009 Michael Perzl <michael@perzl.org> - 6.0-1
- update to version 6.0

* Fri Mar 27 2009 Michael Perzl <michael@perzl.org> - 5.2-2
- fixed shared library symbol export and added version 4 compatibility members

* Mon Mar 31 2008 Michael Perzl <michael@perzl.org> - 5.2-1
- first version for AIX V5.1 and higher
