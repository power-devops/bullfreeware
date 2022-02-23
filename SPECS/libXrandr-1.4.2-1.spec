# Version with/without AIX X11
%{!?aixX11:%define AIXX11 0}
%{?aixX11:%define AIXX11 1}

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

%define _libdir64 %{_libdir}64

%if %{AIXX11} == 1
%define RELEASE_SUFFIX waixX11
%else
%define RELEASE_SUFFIX wofX11
%endif

Summary: X.Org X11 libXrandr runtime library
Name: libXrandr
Version: 1.4.2
Release: 1%{RELEASE_SUFFIX}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Source0: http://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.gz

BuildRequires: autoconf automake libtool
BuildRequires: randrproto-devel >= 1.4.0
BuildRequires: libXrender-devel
BuildRequires: libXext-devel
%if %{AIXX11} == 1
BuildRequires: aix-x11-pc
%else
BuildRequires: xorg-x11-util-macros
BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel

Requires: libX11
%endif
Requires: libXrender

%description
X.Org X11 libXrandr runtime library

%package devel
Summary: X.Org X11 libXrandr development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXrandr development package

%prep
echo "AIXX11=%{AIXX11}"
echo "DO_TESTS=%{DO_TESTS}"
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
export LIBPATH=
export LDFLAGS=
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export CC32="/usr/vac/bin/xlc_r"
export CC64="$CC32 -q64"
export CFLAGS=

# first build the 64-bit version
cd 64bit
export CC=$CC64
export OBJECT_MODE=64
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --libdir=%{_libdir64} \
    --enable-shared --disable-static

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi
cd ..

# now build the 32-bit version
cd 32bit
export CC=$CC32
export OBJECT_MODE=32
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --disable-static

# Remove GCC flags to have a cleaner xlc output
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" Makefile > Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" Makefile.new > Makefile
sed -e "s/BASE_CFLAGS = .*/BASE_CFLAGS = /" src/Makefile > src/Makefile.new
sed -e "s/CWARNFLAGS = .*/CWARNFLAGS = /" src/Makefile.new > src/Makefile

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export RM="/usr/bin/rm -f"
# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# extract 64-bit shared object files from 64 bit libs
cd ${RPM_BUILD_ROOT}%{_libdir64}
/usr/bin/ar -X64 xv libXrandr.a  libXrandr.so.2
cd -

# install 32-bit version
export OBJECT_MODE=32
cd 32bit
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects and extract the 32 bit share objects
cd ${RPM_BUILD_ROOT}%{_libdir}
/usr/bin/ar -q -X64 libXrandr.a  ${RPM_BUILD_ROOT}%{_libdir64}/libXrandr.so.2
/usr/bin/ar -X32 xv libXrandr.a  libXrandr.so.2

# Create some symbolic links
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir usr/lib
mkdir -p usr/include/X11/extensions
LINKS="lib/libXrandr.a
include/X11/extensions/Xrandr.h
lib/libXrandr.la"
for LINK in $LINKS; do
    if [ ! -f /usr/$LINK -o "ls -l /usr/$LINK | grep '/opt/freeware/$LINK$'" != "" ]; then
        ln -sf /opt/freeware/$LINK ${RPM_BUILD_ROOT}/usr/$LINK
    fi
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc 32bit/AUTHORS 32bit/COPYING
%{_libdir}/libXrandr.a
%{_libdir}/libXrandr.so*
%{_libdir64}/libXrandr.so*
/usr/lib/*.a

%files devel
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/Xrandr.h
%{_libdir}/libXrandr.la
%{_libdir}/pkgconfig/xrandr.pc
%{_mandir}/man3/*.3*
/usr/lib/*.la
/usr/include/X11/extensions/Xrandr.h

%changelog
* Tue Apr 26 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 1.4.2-1
- Initial port to AIX 6.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Dave Airlie <airlied@redhat.com> 1.5.0-1
- libXrandr 1.5.0 - fixup requires/br

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.4.2-1%{?gitdate:.git}%{?dist}
- libXrandr 1.4.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.4.1-1
- libXrandr 1.4.1

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-5.20130524gitc90f74497
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.4.0-4.20130524gitc90f74497
- Update to git snapshot to fix CVEs listed below:
- CVE-2013-1986

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.0-3
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 26 2012 Dave Airlie <airlied@redhat.com> 1.4.0-1
- libXrandr 1.4.0 upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libXrandr 1.3.1

* Tue Nov 10 2009 Adam Jackson <ajax@redhat.com> 1.3.0-5
- randr-git.patch: Update to git

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.3.0-2
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Thu Jul 16 2009 Adam Jackson <ajax@redhat.com> 1.3.0-1
- libXrandr 1.3.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.99.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Adam Jackson <ajax@redhat.com> 1.2.99.4-2
- libXrandr-1.2.99.4-gop.patch: Fix encoding of GetOutputPrimary.

* Wed Dec 17 2008 Adam Jackson <ajax@redhat.com> 1.2.99.4-1
- libXrandr 1.2.99.4

* Tue Nov 11 2008 Adam Jackson <ajax@redhat.com> 1.2.3-3
- Fix Requires in -devel subpackage

* Mon Nov 10 2008 Adam Jackson <ajax@redhat.com> 1.2.3-2
- Fix BuildRequires.

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 1.2.3-1
- libXrandr 1.2.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> 1.2.2-2
- Merge-Review #226083
- Removed BR:pkgconfig 
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed zero-length README file

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.2.2-1
- libXrandr 1.2.2

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.2.0-5
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1.2.0-4
- Don't install INSTALL

* Thu Apr 12 2007 Adam Jackson <ajax@redhat.com> 1.2.0-3
- BuildRequire on the randrproto virtual instead of a magic x-x-p-d version.
- Fix -devel package to require sufficiently new randrproto.

* Wed Feb 28 2007 Adam Jackson <ajax@redhat.com> 1.2.0-2
- libXrandr-1.2.0-appease-cee-plus-plus.patch: don't use C++ keywords as
  function argument names.

* Wed Feb 21 2007 Adam Jackson <ajax@redhat.com> 1.2.0-1
- libXrandr 1.2.0

* Mon Nov 20 2006 Adam Jackson <ajax@redhat.com> 1.1.1-2.1
- Update to 1.1.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.1.1-3.1
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-3
- Added "Requires: xorg-x11-proto-devel" to devel pkg for xrandr.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.1.1-2
- Added "BuildRequires: pkgconfig" for (#193428)
- Replace "makeinstall" with "make install DESTDIR=..." for (#192724)
- Remove package ownership of mandir/libdir/etc.

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1
- Update to 1.1.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.0.2-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.0.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.1.0.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.1.0.2-1
- Updated libXrandr to version 1.1.0.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1.1.0.1-1
- Updated libXrandr to version 1.1.0.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXrandr to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'


* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXrandr to version 0.99.1 from X11R7 RC1
- Updated file manifest to find manpages in "man3x"

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
