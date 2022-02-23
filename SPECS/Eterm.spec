%define ver      0.8.10
%define rel      5
Summary: An xterm replacement for Enlightenment users.
Name: Eterm 
Version: %ver
Release: %rel
Copyright: GPL
Group: User Interface/X
Source0: ftp://ftp.eterm.org/pub/Eterm/Eterm-%{ver}.tar.gz
Source1: ftp://ftp.eterm.org/pub/Eterm/Eterm-bg-scale-1.tar.gz
Source2: ftp://ftp.eterm.org/pub/Eterm/Eterm-bg-scale-2.tar.gz
Source3: ftp://ftp.eterm.org/pub/Eterm/Eterm-bg-tile.tar.gz
%define prefix	 %{_prefix}
Patch0: Eterm-%{ver}-utempter-theme.patch
URL: http://www.eterm.org/
BuildRoot: /var/tmp/Eterm-root
BuildRequires: libtool >= 1.3.5
Requires: imlib
%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
# Tied up with autodependency rot
%define DEFCC gcc
%endif

%description
Eterm is a color vt102 terminal emulator with enhanced graphical
capabilities.  Eterm is intended to be a replacement for xterm for
Enlightenment window manager users, but it can also be used as a
replacement for xterm by users without Enlightenment.  Eterm supports
various themes and is very configurable, in keeping with the
philosophy of Enlightenment. If you install Eterm, you'll also need to
have the Imlib library installed.

%package backgrounds
Summary: Backgrounds for Eterm
Group: User Interface/X
Requires: Eterm = %{ver}
%description backgrounds
Install this package if you want additional backgrounds for Eterm

%prep
%setup -q -n Eterm-%{ver} 1 
%patch0 -p1

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

export LDFLAGS="-Wl,-brtl"
./autogen.sh --prefix=%{prefix}
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig/

cat > $RPM_BUILD_ROOT/etc/X11/wmconfig/Eterm <<EOF
Eterm name "Eterm"
Eterm description "An xterm replacement for Enlightenment users."
Eterm exec "Eterm &"
Eterm group Utilities/Shells
EOF

chmod 0644 $RPM_BUILD_ROOT/etc/X11/wmconfig/Eterm

(
	tar xvfz %{SOURCE1}
	tar xvfz %{SOURCE2}
	tar xvfz %{SOURCE3}
	cd Eterm/bg
	mv -f scale/* ../../bg/scale/
	mv -f tile/* ../../bg/tile/
	cd ../..
	rm -rf Eterm
)

make prefix=$RPM_BUILD_ROOT%{prefix} install

( cd $RPM_BUILD_ROOT
  mv .%{prefix}/bin/Eterm .%{prefix}/bin/Eterm-%{ver}
  /usr/bin/strip .%{prefix}/bin/* || :
  cd $RPM_BUILD_ROOT%{prefix}/bin
  ln -sf Eterm-%{ver} Eterm
  cd $RPM_BUILD_ROOT
  chmod +x .%{prefix}/lib/lib*so* || :
)

strip -s $RPM_BUILD_ROOT%{prefix}/bin/* || :

gzip $RPM_BUILD_ROOT%{prefix}/man/man1/*

#get the package listing for Eterm-backgrounds
echo "%defattr(-,root,root)" > rpm-Eterm-bg-files
find $RPM_BUILD_ROOT%{prefix}/share/Eterm/pix/ -not -name 014.png \
	-not -name 40.png \
	-not -name 6.png \
	-not -name backwave.jpg \
	-not -name circuit.png \
	-not -name nebula.jpg \
	-not -name fourthday.jpg \
	-not -name gaia.jpg \
	-not -name galleon.jpg \
	-not -name night_of_the_dragon.jpg \
	-not -name pixmaps.list \
	-type f | sed -e "s#^$RPM_BUILD_ROOT##g" >> rpm-Eterm-bg-files

(cd $RPM_BUILD_ROOT
 for dir in bin lib share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)
%ifos linux
%post
/sbin/ldconfig

%postun
/sbin/ldconfig
%endif

%post backgrounds
#move the old pixmaps.list out and the new in so that the new backgrounds can be selected
mv %{prefix}/share/Eterm/pix/pixmaps.list %{prefix}/share/Eterm/pix/pixmaps.list.rpmsave
cp %{prefix}/doc/Eterm-backgrounds-%{ver}/rh-pixmaps.list %{prefix}/share/Eterm/pix/pixmaps.list

%postun backgrounds
#move pixmaps.list.rpmsave back to its origional filename so that when Eterm
#gets uninstalled it doesn't throw fits because the dir isn't empty, and also
#so that Eterm has something to use if the backgrounds package isn't wanted
#anymore
mv %{prefix}/share/Eterm/pix/pixmaps.list.rpmsave %{prefix}/share/Eterm/pix/pixmaps.list

%clean
rm -rf $RPM_BUILD_ROOT

%files  
%defattr(-,root,root)
%doc  doc/Eterm_reference.html doc/Eterm.1.html
%doc COPYING README ChangeLog 
%config(missingok) %{prefix}/share/Eterm/pix/pixmaps.list
/etc/X11/wmconfig/Eterm
%{prefix}/bin/*
%{prefix}/lib/*
/usr/bin/*
/usr/lib/*
/usr/share/Eterm
%{prefix}/man/man1/*
%{prefix}/share/Eterm/themes
%{prefix}/share/Eterm/pix/014.png
%{prefix}/share/Eterm/pix/40.png
%{prefix}/share/Eterm/pix/6.png
%{prefix}/share/Eterm/pix/backwave.jpg
%{prefix}/share/Eterm/pix/circuit.png
%{prefix}/share/Eterm/pix/nebula.jpg
%{prefix}/share/Eterm/pix/fourthday.jpg
%{prefix}/share/Eterm/pix/gaia.jpg
%{prefix}/share/Eterm/pix/galleon.jpg
%{prefix}/share/Eterm/pix/night_of_the_dragon.jpg
%dir %{prefix}/share/Eterm
%dir %{prefix}/share/Eterm/pix

%files backgrounds -f rpm-Eterm-bg-files
%doc $RPM_SOURCE_DIR/rh-pixmaps.list

%changelog
* Mon Oct 08 2001 David Clissold <cliss@austin.ibm.com>
- rev 5: minor change; strip the binaries

* Wed Jun 20 2001 Marc Stephenson <marc@austin.ibm.com>
- Adapted for AIX Toolbox

* Wed Dec 8 1999 Tim Powers <timp@redhat.com>
- using unified patch for utempter and themes from Michael Jennings

* Tue Dec 7 1999 Tim Powers <timp@redhat.com>
- added wmconfig entry
- split up into 2 packages, Eterm proper, and Eterm-backgrounds
- thanks to ewt, we no longer have to make Eterm suid root, uses utempter
	instead

* Mon Dec 6 1999 Tim Powers <timp@redhat.com>
- updated to 0.8.10
- patched so that Eterm finds pix/themes in the right place
- new version fixes problems with utmp, conforms to Eterm docs.
- added RedHat.Eterm_suid which includes instructions on how to run Eterm in
	order to have it seen by "w" and "who" as a regular user
	
* Fri Aug 20 1999 Tim Powers <timp@redhat.com>
- fixed roblem with removing all files when uninstalling Eterm.

* Tue Jul 27 1999 Tim Powers <timp@redhat.com>
- updated version to 0.8.9
- cleaned up spec
- updated patch
- includes new backgrounds
- built for 6.1

* Mon Apr 05 1999 Michael Maher <mike@redhat.com>
- update to 0.8.8

* Fri Oct 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.8.7.

* Fri Oct 08 1998 Michael Maher <mike@redhat.com>
- built eterm
