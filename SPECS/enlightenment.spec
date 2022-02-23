# Note that this is NOT a relocatable package
%define prefix   %{_prefix}

Summary: The Enlightenment window manager.
Name: enlightenment
Version: 0.16.5
Release: 3
License: IBM_ILA
Group: User Interface/Desktops
Source: ftp://ftp.enlightenment.org/enlightenment/enlightenment/%{name}-%{version}.tar.gz
Source1: IBM_ILA
Patch0: %{name}-%{version}-lintl.patch
BuildRoot: /var/tmp/e-%{version}-root
URL: http://www.enlightenment.org/
Provides: windowmanager
Docdir: %{prefix}/doc
%define DEFCC cc

%description
Enlightenment is an X Window System window manager that is designed to
be powerful, extensible, configurable and attractive. It is one of the
more graphically intense window managers.

Enlightenment goes beyond managing windows by providing a useful and
appealing graphical shell from which to work. It is open in design and
instead of dictating a policy, allows the user to define their own
policy, down to every last detail.

Install enlightenment if you want to use a powerful and configurable
window manager.

%prep
%setup -q
%patch0 -p1 -b .lintl

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat COPYING >> LICENSE

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
export CFLAGS="-I/usr/include/freetype $RPM_OPT_FLAGS"

autoconf
CFLAGS="-I/usr/include/freetype $RPM_OPT_FLAGS" LDFLAGS="-Wl,-brtl" ./configure --prefix=%prefix
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{prefix} install

(cd $RPM_BUILD_ROOT
 for dir in bin
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/enlightenment/$dir/* .
    cd -
 done

 mkdir -p usr/share/enlightenment
 ln -sf ../..%prefix/enlightenment/themes usr/share/enlightenment
 ln -sf ../..%prefix/enlightenment/E-docs usr/share/enlightenment
 ln -sf ../..%prefix/enlightenment/config usr/share/enlightenment
)

# strip binaries
/usr/bin/strip $RPM_BUILD_ROOT/%{prefix}/%{name}/bin/* 2>/dev/null || :

# remove backup file
rm -f $RPM_BUILD_ROOT/%{prefix}/share/enlightenment/E-docs/MAIN~ 

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-, root, root)
%attr(-, root, root) %{prefix}/enlightenment/*
/usr/share/enlightenment
/usr/bin/*
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README LICENSE

%changelog
* Wed Feb 25 2004 David Clissold <cliss@austin.ibm.com> 0.16.5-3
- Rebuild with IBM VAC compiler.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Thu Oct 04 2001 David Clissold <cliss@austin.ibm.com>
- Update to 0.16.5; ensure binaries are stripped.

* Wed Mar 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb 21 2000 Havoc Pennington <hp@redhat.com>
- change SOURCES/control.cfg instead of patching the one
  that comes with E

* Tue Feb 15 2000 Preston Brown <pbrown@redhat.com>
- provide windowmanager

* Wed Feb 3 2000 Havoc Pennington <hp@redhat.com>
- remove backup documentation file.

* Wed Feb 3 2000 Havoc Pennington <hp@redhat.com>
- Change default focus behavior to be less surprising

* Tue Aug 31 1999 Elliot Lee <sopwith@redhat.com>
- Add patch 24, to fix bugzilla #1934 - don't warn about sound.

* Tue Jul 27 1999 Michael Fulbright <drmike@redhat.com>
- dont chown 0.0 files!

* Wed Jul 21 1999 Owen Taylor <otaylor@redhat.com>
- release 36; fix incorrect WM_STATE patch from last update.

* Tue Jul 20 1999 Owen Taylor <otaylor@redhat.com>
- Patch to set WM_STATE properly atom when withdrawing window

* Tue May 25 1999 Michael Fulbright <drmike@redhat.com>
- added raster's patch to handle focus issues when switching desktops

* Mon May 10 1999 Michael Fulbright <drmike@redhat.com>
- added raster's patch to raise windows when gnomepager tasklist clicked
- added raster's patch to handle x11r5 sm apps more completely

* Mon Apr 19 1999 Michael Fulbright <drmike@redhat.com>
- fixed leak in enlightenment when titles change
- fixed language handling so tooltip time ok with lang change
- fixed bug where windows are corrupted if moved while resized

* Thu Apr 15 1999 Michael FUlbright <drmike@redhat.com>
- fixed bug involved click to focus and switching desktops

* Wed Apr 14 1999 Michael Fulbright <drmike@redhat.com>
- CleanBig has resize border on top now

* Mon Apr 12 1999 Michael Fulbright <drmike@redhat.com>
- fixed applix iconization bug

* Sat Apr 10 1999 Michael Fulbright <drmike@redhat.com>
- removed ShinyMetal theme - crashes when I try it.
  Raster will take a look at it later.

* Fri Apr 09 1999 Michael Fulbright <drmike@redhat.com>
- fixed focus/emacs bug

* Thu Apr 08 1999 Michael Fulbright <drmike@redhat.com>
- fixed cleanbig theme tooltips and font size

* Mon Apr 05 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.5 plus semisolid drag fix
- made CleanBig the default theme

* Wed Mar 31 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.5

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- strip binaries

* Wed Mar 17 1999 Michael Fulbright <drmike@redhat.com>
- added patch to fix panel orientation drawing problems
- removed the CNTL-ALT-K binding, which killed a window nasty
  This conflicts with emacs and possible other app bindings

* Sun Mar 14 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.2

* Wed Feb 24 1999 The Rasterman <raster@redhat.com>
- updated to latest source and upped release (rel 35)

* Wed Feb 24 1999 The Rasterman <raster@redhat.com>
- updated to latest source and upped release

* Tue Feb 23 1999 The Rasterman <raster@redhat.com>
- updated to latest source and upped release

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- removed libtoolize from build

* Tue Feb 11 1999 Michael Fulbright <drmike@redhat.com>
- update to 0.15.0-19990210, rpm release 21

* Mon Feb 08 1999 Michael Fulbright <drmike@redhat.com>
- update to 0.15.0-19990208, rpm release 20

* Mon Feb 08 1999 Michael Fulbright <drmike@redhat.com>
- update to 0.15.0-19990207, rpm release 19

* Sat Feb 06 1999 Michael Fulbright <drmike@redhat.com>
- update to 0.15.0-19990206

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- update to 0.15.0-19990205

* Wed Feb 04 1999 Michael Fulbright <drmike@redhat.com>
- fixed symlink for clean theme

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.0-19990203.tar.gz

* Wed Jan 28 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.0-19990128.tar.gz

* Tue Jan 27 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.0-19990127.tar.gz
- new Classic theme version 0.5

* Mon Jan 25 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15.0-19990125.tar.gz
- new Classic theme version 0.4

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15-19990120

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15-990119

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 0.15-990115

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- incoporated version 0.3 of Classic theme
- latest snapshot of e from CVS

* Fri Dec 18 1998 Michael Fulbright <drmike@redhat.com>
- incoporated version 0.2 of Classic theme, incorporating wanger fixes

* Thu Dec 17 1998 Michael Fulbright <drmike@redhat.com>
- fixed menu button on window to not have 'Close' as first entry
- added Rasters fix for desktop areas and losing windows

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- hacked in conservative theme
- preparing for GNOME freeze

* Fri Nov 20 1998 Michael Fulbright <drmike@redhat.com>
- updated for pre-dr15

* Fri Sep 11 1998 Mandrake <mandrake@mandrake.net>
- changed rev num, also incremented imlib requirement to 1.8

* Tue Jun 2 1998 The Rasterman <raster@redhat.com>
- wrote .spec file


