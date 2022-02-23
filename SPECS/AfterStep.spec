Summary: An X window manager which emulates the look and feel of NEXTSTEP(R).
Name: AfterStep
Version: 1.8.10
Release: 1
Copyright: GPL
Group: User Interface/Desktops
Source0: ftp://ftp.afterstep.org/stable/AfterStep-%{version}.tar.bz2
Patch0: %{name}-%{version}-png.patch
BuildRoot: /var/tmp/afterstep-root
%ifarch ia64
%define DEFCC bcc
%else
%define DEFCC cc
%endif

%description
The AfterStep window manager combines convenient, useful features 
with the attractive look of the NEXTSTEP(R) interface. NEXTSTEP(R)-style 
features include the the title bar, title buttons, borders, icons and 
menus.  The most prominent addition to the interface is AfterStep's 
Wharf, a customized version of the GoodStuff panel (an fvwm window 
manager bar of application icons).  AfterStep's Wharf is a free-floating 
application loader which can swallow running programs and contain 
folders of more applications.  AfterStep also includes easy to use
'look' files, so you can share your desktop appearance.

You need to install AfterStep if you want to use the AfterStep window
manager.  You should also install AfterStep and try it out if you haven't
decided which X Window System window manager you want to use, or just to
keep your window management options open.

%prep
%setup -q
%patch0 -p1 -b .png

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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} \
	--with-imageloader="xv -root -quit" \
	--with-helpcommand="xterm -e man" \
	--with-desktops=1 \
	--with-deskgeometry=2x3 \
	--disable-availability \
	--enable-makemenusonboot \
	--with-xpm
make CCFLAGS="$RPM_OPT_FLAGS"
#sgml2html doc/afterstep.sgml

%install
rm -rf $RPM_BUILD_ROOT
make install install.man DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/sessreg
rm -f $RPM_BUILD_ROOT%{_prefix}/bin/xpmroot

/usr/bin/strip $RPM_BUILD_ROOT/%{_prefix}/bin/* 2>/dev/null || :

(cd $RPM_BUILD_ROOT
    mkdir -p usr/lpp/X11/bin
    cd usr/lpp/X11/bin
    ln -sf ../../../..%{_prefix}/bin/* .
)
	
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/bin/*
/usr/lpp/X11/bin/*
%{_prefix}/share/afterstep
%{_prefix}/man/*/*
%doc doc/code doc/languages doc/licences NEW README TEAM
%doc UPGRADE TODO

%changelog
* Thu Oct 04 2001 David Clissold <cliss@austin.ibm.com>
- 1.8.10

* Thu May 17 2001 Marc Stephenson <marc@austin.ibm.com>
- 1.8.8

* Sat Apr 07 2001 David Clissold <cliss@austin.ibm.com>
- Patch needed for as_png.c to build with cc.

* Tue Mar 13 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Rebuild with default compiler

* Mon Mar 05 2001 David Clissold <cliss@austin.ibm.com>
- Ensure binaries are stripped.

* Tue Feb 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.8.0 (1.7.* is beta)

* Wed Feb  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.7.172

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Thu Jan 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.7.164
- handle RPM_OPT_FLAGS
- BuildPrereq sgml-tools

* Fri Sep 03 1999 Cristian Gafton <gafton@redhat.com>
- version 1.7.142 and the four patches available integrated

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- optimizations are making it sick

* Sun Apr 11 1999 Preston Brown <pbrown@redhat.com>
- fixed up menus from 5.2 to work with new AfterStep

* Thu Apr 08 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.7.90 (bugfix release), now 99 percent GNOME compliant.

* Wed Mar 24 1999 Bill Nottingham <notting@redhat.com>
- don't require xterm-color

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- Fixed problem with the Feels menu showing the bacjkground change entries

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5
- requires AfterStep-APPS for the cool dockable applications

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- 1.4.5.3 is out
- wmconfig hacks
- can start AnotherLevel

* Fri Apr 17 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.4.5.1
- went through the sources and fixed some of the bugs

* Fri Mar 27 1998 Cristian Gafton <gafton@redhat.com>
- packaged 1.4.4 with a patch to better support BuildRoot.

