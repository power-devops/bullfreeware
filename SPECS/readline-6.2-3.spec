Summary: A library for editing typed command lines
Name: readline
Version: 6.2
Release: 3
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
Patch1: ftp://ftp.gnu.org/gnu/readline/readline-6.2-patches/readline62-001
Patch2:  %{name}-%{version}-aixconf.patch

BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
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
%patch2 -p1 -b .aixconf


%build
# setup environment for 32-bit and 64-bit builds
export AR="ar -X32_64"
export NM="nm -X32_64"
export LDFLAGS="-L/opt/freeware/lib"

# first build the 64-bit version
export OBJECT_MODE="64"
CC_prev="$CC"
export CC="$CC -q64"
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
export CC="$CC_prev"
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
* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> 6.2-3
- Initial port on Aix6.1

* Fri Jun 10 2011 Gerard Viseido <gerard.visiedo@bull.net> 6.2-2Ã2
- Initial port on Aix5.3

