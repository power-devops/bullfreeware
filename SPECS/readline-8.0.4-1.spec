%bcond_without dotests

# Upstream provides official patches
# Bug fix is the number of patches, but archive name is baseversion
%define major_version 8
%define minor_version 0
%define bugfix_version 4

%define baseversion %{major_version}.%{minor_version}

%define _libdir64 %{_libdir}64

Summary: A library for editing typed command lines
Name: readline
Version: %{major_version}.%{minor_version}.%{bugfix_version}
Release: 1
License: GPLv2+
Group: System Environment/Libraries
URL: https://tiswww.case.edu/php/chet/readline/rltop.html
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{baseversion}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{baseversion}.tar.gz.sig
Source2: libreadline.so.4-aix32
Source3: libreadline.so.4-aix64
Source4: libhistory.so.4-aix32
Source5: libhistory.so.4-aix64
Source6: libreadline.so.5-aix32
Source7: libreadline.so.5-aix64
Source8: libhistory.so.5-aix32
Source9: libhistory.so.5-aix64
Source10: libreadline.so.6-aix32
Source11: libreadline.so.6-aix64
Source12: libhistory.so.6-aix32
Source13: libhistory.so.6-aix64
Source14: libreadline.so.7-aix32
Source15: libreadline.so.7-aix64
Source16: libhistory.so.7-aix32
Source17: libhistory.so.7-aix64

Source999: create_exp_file.sh

Source1000: %{name}-%{version}-%{release}.build.log

# Official upstream patches
%{lua:for i=1,rpm.expand("%{bugfix_version}") do print(string.format("Patch%u: readline-%s-patch-%u.patch\n", i, rpm.expand("%{baseversion}"), i)) end}

Patch100: readline-remove-bexpall.patch
Patch101: readline_exports_file.patch

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
%setup -q -n %{name}-%{baseversion}

# Official upstream patches
%{lua:for i=1,rpm.expand("%{bugfix_version}") do print(string.format("%%patch%u -p0\n", i, i)) end}

%patch100 -p1 -b .bexpall
%patch101 -p1 -b .exports_file

cp %{SOURCE999} shlib

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/usr/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="nm -X32_64"
export LDFLAGS="-L/opt/freeware/lib"

cd 64bit
# first build the 64-bit version
export OBJECT_MODE=64
#export CC="xlc_r -q64"
export CC="gcc -maix64"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

# Check the bcopy issue
/usr/bin/nm -X64 shlib/libreadline.so.%{major_version} | grep bcopy

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
#export CC="xlc_r"
export CC="gcc -maix32"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared --disable-static

gmake %{?_smp_mflags}

# Check the bcopy issue
/usr/bin/nm -X32 shlib/libreadline.so.%{major_version} | grep bcopy

# Create the archives
rm -f libhistory.a libreadline.a
${AR} -rv libhistory.a  shlib/libhistory.so.%{major_version}
${AR} -rv libreadline.a shlib/libreadline.so.%{major_version}

# add 64-bit shared objects to library
${AR} -q libhistory.a  ../64bit/shlib/libhistory.so.%{major_version}
${AR} -q libreadline.a ../64bit/shlib/libreadline.so.%{major_version}

# Add the older version 4 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} libreadline.so.4
/usr/bin/strip -X32 -e libreadline.so.4
/usr/bin/ar -X32 -q libreadline.a libreadline.so.4

cp %{SOURCE3} libreadline.so.4
/usr/bin/strip -X64 -e libreadline.so.4
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
/usr/bin/strip -X32 -e libreadline.so.5
/usr/bin/ar -X32 -q libreadline.a libreadline.so.5

cp %{SOURCE7} libreadline.so.5
/usr/bin/strip -X64 -e libreadline.so.5
/usr/bin/ar -X64 -q libreadline.a libreadline.so.5

cp %{SOURCE8} libhistory.so.5
/usr/bin/strip -X32 -e libhistory.so.5
/usr/bin/ar -X32 -q libhistory.a libhistory.so.5

cp %{SOURCE9} libhistory.so.5
/usr/bin/strip -X64 -e libhistory.so.5
/usr/bin/ar -X64 -q libhistory.a libhistory.so.5

# Add the older version 6 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE10} libreadline.so.6
/usr/bin/strip -X32 -e libreadline.so.6
/usr/bin/ar -X32 -q libreadline.a libreadline.so.6

cp %{SOURCE11} libreadline.so.6
/usr/bin/strip -X64 -e libreadline.so.6
/usr/bin/ar -X64 -q libreadline.a libreadline.so.6

cp %{SOURCE12} libhistory.so.6
/usr/bin/strip -X32 -e libhistory.so.6
/usr/bin/ar -X32 -q libhistory.a libhistory.so.6

cp %{SOURCE13} libhistory.so.6
/usr/bin/strip -X64 -e libhistory.so.6
/usr/bin/ar -X64 -q libhistory.a libhistory.so.6

# Add the older version 7 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE14} libreadline.so.7
/usr/bin/strip -X32 -e libreadline.so.7
/usr/bin/ar -X32 -q libreadline.a libreadline.so.7

cp %{SOURCE15} libreadline.so.7
/usr/bin/strip -X64 -e libreadline.so.7
/usr/bin/ar -X64 -q libreadline.a libreadline.so.7

cp %{SOURCE16} libhistory.so.7
/usr/bin/strip -X32 -e libhistory.so.7
/usr/bin/ar -X32 -q libhistory.a libhistory.so.7

cp %{SOURCE17} libhistory.so.7
/usr/bin/strip -X64 -e libhistory.so.7
/usr/bin/ar -X64 -q libhistory.a libhistory.so.7


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 32bit
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*so.%{major_version}
cp lib*.a ${RPM_BUILD_ROOT}%{_libdir}
chmod 0644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

cd doc
make info
make DESTDIR=${RPM_BUILD_ROOT} install
cd ..

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*info*

#(
#  cd ${RPM_BUILD_ROOT}
#  for dir in include lib
#  do
#    mkdir -p usr/${dir}
#    cd usr/${dir}
#    ln -sf ../..%{_prefix}/${dir}/* .
#    cd -
#  done
#)

#Add links for 64-bit library members
(
  mkdir -p $RPM_BUILD_ROOT/%{_libdir64}
  cd $RPM_BUILD_ROOT/%{_libdir64}
  ln -s ../lib/*.a .
)


%check
%if %{with dotests}
cd 64bit
( gmake -k check || true )
cd ../32bit
( gmake -k check || true )
%endif



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
%doc 32bit/CHANGES* 32bit/COPYING* 32bit/NEWS* 32bit/README* 32bit/USAGE*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_infodir}/history.info*
%{_infodir}/rluserman.info*


%files devel
%defattr(-,root,system,-)
%doc 32bit/examples/*.c 32bit/examples/*.h 32bit/examples/rlfe
%{_includedir}/readline
%{_mandir}/man3/*
%{_infodir}/readline.info*


%changelog
* Tue Oct 27 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 8.0.4-1
- New version 8.0
- Generalise way to apply upstream patches
- Stop providing link to /usr

* Wed Jul 04 2018 Tony Reix <tony.reix@atos.net> - 7.0-1
- Version 7.0

* Wed Jul 04 2018 Tony Reix <tony.reix@atos.net> - 6.3-2
- Use patches 7 & 8
- Move to GCC

* Wed Mar 16 2016 Tony Reix <tony.reix@atos.net> - 6.3-1
- Version 6.3 patch level 8

* Fri Aug 15 2014 Michael Perzl <michael@perzl.org> - 6.3-5
- updated to version 6.3 patch level 8

* Mon May 19 2014 Michael Perzl <michael@perzl.org> - 6.3-4
- updated to version 6.3 patch level 6

* Sun Apr 27 2014 Michael Perzl <michael@perzl.org> - 6.3-3
- updated to version 6.3 patch level 5

* Fri Mar 28 2014 Michael Perzl <michael@perzl.org> - 6.3-2
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
