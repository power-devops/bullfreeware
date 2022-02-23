%define ver      1.2.2
%define subver   1.2
%define rel      2

Summary: The GNU Image Manipulation Program.
Name: gimp
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/Multimedia
URL: http://www.gimp.org/
Source: ftp://ftp.gimp.org/pub/gimp/v%{subver}/v%{ver}/gimp-%{ver}.tar.gz
Patch0: gimp-%{ver}-aix.patch
#BuildRoot: %{_tmppath}/gimp-root
BuildRoot: /opt/freeware/src/packages/BUILD/gimp-root
Obsoletes: gimp-data-min
BuildRequires: libtool >= 1.3.5
Requires: gtk+ >= 1.2
Prefix: %{_prefix}

%ifarch ia64
  %define DEFCCIA xlc
  %define DEFCC %{DEFCCIA}
%else
  %define DEFCC xlc
%endif

%description
The GIMP (GNU Image Manipulation Program) is a powerful image
composition and editing program, which can be extremely useful for
creating logos and other graphics for Web pages.  The GIMP has many of
the tools and filters you would expect to find in similar commercial
offerings, and some interesting extras as well. The GIMP provides a
large image manipulation toolbox, including channel operations and
layers, effects, sub-pixel imaging and anti-aliasing, and conversions,
all with multi-level undo.

The GIMP includes a scripting facility, but many of the included
scripts rely on fonts that we cannot distribute.  The GIMP FTP site
has a package of fonts that you can install by yourself, which
includes all the fonts needed to run the included scripts.  Some of
the fonts have unusual licensing requirements; all the licenses are
documented in the package.  Get
ftp://ftp.gimp.org/pub/gimp/fonts/freefonts-0.10.tar.gz and
ftp://ftp.gimp.org/pub/gimp/fonts/sharefonts-0.10.tar.gz if you are so
inclined.  Alternatively, choose fonts which exist on your system
before running the scripts.

Install the GIMP if you need a powerful image manipulation
program. You may also want to install other GIMP packages:
gimp-libgimp if you're going to use any GIMP plug-ins and
gimp-data-extras, which includes various extra files for the GIMP.

%package devel
Summary: The GIMP plug-in and extension development kit.
Group: Development/Libraries
Requires: gtk+-devel
Prereq: /sbin/install-info
%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.

Install gimp-devel if you're going to create plug-ins and/or
extensions for the GIMP.  You'll also need to install gimp-limpgimp
and gimp, and you may want to install gimp-data-extras.

%package libgimp
Summary: Libraries for the GIMP (GNU Image Manipulation Program).
Group: System Environment/Libraries
Copyright: LGPL
%description libgimp
The gimp-libgimp package contains libraries which are used to
communicate between the GIMP (GNU Image Manipulation Program) and
other programs which function as GIMP plug-ins.

If you are going to develop or use plug-ins for the GIMP, you'll need
to install the gimp-libgimp package.  You'll also need to install the
gimp and gimp-devel.  If you plan on using the GIMP, you'll probably
also want to install gimp-data-extras, which is not required but
contains a lot of extras which will be useful to GIMP users.

%prep
%setup -q
%patch -p1  -b .aix

# v1.2.2-1 patched libgimp/Makefile.am, must regen libgimp/Makefile.in
automake -i libgimp/Makefile
automake -i Makefile


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
       export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -qmaxmem=8192 -Wl,-bexpall"
%ifarch ia64
       export RPM_OPT_FLAGS=
%endif
       export CFLAGS="$RPM_OPT_FLAGS"
fi

%ifarch ppc rs6000
  export LDFLAGS="-Wl,-brtl"
%endif

libtoolize --force
if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh --prefix=%{prefix}
else
  autoconf
  CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix} --disable-perl
fi

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make CC="$CC" LD="$CC"
else
  make CC="$CC" LD="$CC"
fi

#cd docs
#make
#cd ..

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/info $RPM_BUILD_ROOT%{prefix}/include \
	$RPM_BUILD_ROOT/usr/lib $RPM_BUILD_ROOT%{prefix}/bin \
	$RPM_BUILD_ROOT/etc/X11/applnk/Graphics \
	$RPM_BUILD_ROOT%{prefix}/share/icons/mini \
	$RPM_BUILD_ROOT%{prefix}/share/pixmaps
make DESTDIR=$RPM_BUILD_ROOT install
#cd docs
#make prefix=$RPM_BUILD_ROOT/usr install
#gzip -9 $RPM_BUILD_ROOT/usr/info/*
#install RPM/wilbur.xpm $RPM_BUILD_ROOT%{prefix}/share/icons/
#install RPM/mini-wilbur.xpm $RPM_BUILD_ROOT%{prefix}/share/icons/mini/
#install $RPM_SOURCE_DIR/gnome-gimp.png $RPM_BUILD_ROOT%{prefix}/share/pixmaps/gnome-gimp.png

cat > $RPM_BUILD_ROOT/etc/X11/applnk/Graphics/gimp.desktop << EOF
[Desktop Entry]
Name=The GIMP
Name[ca]=El GIMP
Name[da]=GIMP
Name[de]=GIMP
Name[es]=El GIMP
Name[et]=GIMP
Name[eu]=GIMPa
Name[fi]=GIMP
Name[fr]=The GIMP
Name[hu]=A GIMP
Name[it]=GIMP
Name[ja]=GIMP
Name[ko]=±èÇÁ
Name[nl]=GIMP
Name[no]=GIMP
Name[pl]=GIMP
Name[pt]=O GIMP
Name[pt_BR]=O GIMP
Name[ru]=GIMP
Name[sv]=GIMP
Comment=GNU Image Manipulation Program
Comment[ca]=El programa de manipulació d'imatges GNU
Comment[da]=GNU Image Manipulation Program
Comment[de]=Das GNU-Bildbearbeitungsprogramm
Comment[es]=Programa de manipulación de imágenes GNU
Comment[et]=GNU pilditöötlusprogramm
Comment[eu]=GNU imaginak eraldatzeko programa
Comment[fi]=Kuvankäsittelyohjelma
Comment[fr]=Le Programme de Manipulation d'Images GNU
Comment[hr]=Program za obradu forografija pod GNU licencom
Comment[hu]=GNU képfeldolgozó program
Comment[it]=Programma di Manipolazione Immagini GNU
Comment[ja]=GNU²èÁüÊÔ½¸¥×¥í¥°¥é¥à
Comment[ko]=GNU ±×¸² ÆíÁý ÇÁ·Î±×·¥
Comment[nl]=GNU beeldverwerkingsprogramma
Comment[no]=GNU bildehåndterings-program
Comment[pl]=Zaawansowany edytor grafiki bitmapowej na licencji GNU
 for dir in bin lib include
Comment[pt_BR]=Programa de Edição de Imagens GNU 
Comment[ru]=ðÒÏÇÒÁÍÍÁ ÍÁÎÉÐÕÌÑÃÉÉ ÉÚÏÂÒÁÖÅÎÉÑ GNU
Comment[sv]=GNU Image Manipulation Program
TryExec=gimp
Exec=gimp
Icon=gnome-gimp.png
Terminal=0
Type=Application
EOF

(cd $RPM_BUILD_ROOT
 for dir in bin lib include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)

(cd $RPM_BUILD_ROOT/opt/freeware/bin
  for binfile in `file * | grep 'not strip' | awk -F ':' '{print $1}'`
  do
     strip $binfile
  done
)


%clean
rm -rf $RPM_BUILD_ROOT

%post devel
#/sbin/install-info --section="GIMP" --entry="* PDB: (pdb).          The GIMP procedural database." /usr/info/pdb.info.gz /usr/info/dir

%preun devel
#if [ $1 = 0 ]; then
#   /sbin/install-info --delete --section="GIMP" --entry="* PDB: (pdb).          The GIMP procedural database." /usr/info/pdb.info.gz /usr/info/dir
#fi

%ifos linux
%post libgimp -p /sbin/ldconfig
%postun libgimp -p /sbin/ldconfig
%endif

%files
%attr(644,root,root) %config(missingok) /etc/X11/applnk/Graphics/gimp.desktop
%attr(-, root, root) %doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%attr(-, root, root) %doc docs/*.txt docs/*.eps
%attr(-, root, root) %{prefix}/share/*
%attr(-, root, root) %{prefix}/bin/gimp
%attr(-, root, root) %{prefix}/lib/gimp/*
%attr(-, root, root) %{prefix}/etc/gimp/*
/usr/lib/gimp
/usr/bin/gimp
#%attr(-, root, root) /usr/man

%files devel
%ifos linux
%attr(-, root, root) %{prefix}/include/*
%attr(-, root, root) %{prefix}/lib/lib*a
%endif
#%attr(-, root, root) %{prefix}/info/pdb.info*
%attr(-, root, root) %{prefix}/bin/gimptool
/usr/bin/gimptool
/usr/include/*

%files libgimp
%attr(-, root, root) %{prefix}/lib/lib*.so.*
%attr(-, root, root) %{prefix}/lib/lib*.so
/usr/lib/lib*.so.*
/usr/lib/lib*.so
%ifnos linux
%attr(-, root, root) %{prefix}/lib/lib*a
/usr/lib/lib*a
%endif
%attr(-, root, root) %{prefix}/include/*
/usr/include/*


%changelog
* Wed Apr 24 2002 David Clissold <cliss@austin.ibm.com>
- NO functional change.  Minor correction to a source comment
- for political reasons.  Only affects the SRPM.

* Fri Oct 05 2001 Dan Nguyen <dnn@austin.ibm.com>
- Upgrade to 1.2.2

* Fri May 18 2001 Marc Stephenson <marc@austin.ibm.com>
- Upgrade to 1.2.1
- Use libtoolize

* Fri Mar 09 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Tue Jan 16 2001 Marc Stephenson <aixtoolbox-l@austin.ibm.com>
- Modified for AIX Toolbox distribution
  - removed hard-coded prefix

* Mon Feb 07 2000 Preston Browm <pbrown@redhat.com>
- wmconfig gone.

* Thu Feb  3 2000 Matt Wilson <msw@redhat.com>
- update translations for .desktop entry
- use GNOME's icon for The GIMP
- brp-strip libs

* Sat Sep 25 1999 Preston Brown <pbrown@redhat.com>
- red hat .desktop entry

* Tue May 11 1999 Matt Wilson <msw@redhat.com>
- added gimptool to gimp-devel's file list

* Thu Apr  8 1999 Bill Nottingham <notting@redhat.com>
- fix prefix

* Mon Apr  5 1999 Matt Wilson <msw@redhat.com>
- install binaries stripped by default

* Mon Apr  5 1999 Matt Wilson <msw@redhat.com>
- updated to official 1.0.4 release

* Wed Mar 31 1999 Matt Wilson <msw@redhat.com>
- updated for 1.0.4 release
- requires gtk+ >= 1.2

* Sun Mar 14 1999 Matt Wilson <msw@redhat.com>
- updated for 1.0.3 release
- updated group

* Mon Apr 20 1998 Marc Ewing <marc@redhat.com>
- include *.xpm and .wmconfig in CVS source
- removed explicit glibc require

* Thu Apr 16 1998 Marc Ewing <marc@redhat.com>
- Handle builds using autogen.sh
- SMP builds
- put in CVS, and tweak for automatic CVS builds

* Sun Apr 12 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Upgraded to 0.99.26

* Sat Apr 11 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Upgraded to 0.99.25

* Wed Apr 08 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Upgraded to version 0.99.24

* Sun Apr 05 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Stop building the docs - they require emacs and
  (even worse), you must run X.

* Fri Mar 27 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- upgraded to 0.99.23

* Sat Mar 21 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- No longer requires xdelta, that was a bug on my part
- spec cleanup, changed libgimp copyright, can now be
  built by non-root users, removed some lines in the description

* Fri Mar 20 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- upgraded to 0.99.22

* Sun Mar 15 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- upgraded to 0.99.21

* Thu Mar 12 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Upgraded to 0.99.20

* Mon Mar 09 1998 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- Recompiled with gtk+ 0.99.5
- Now requires gtk+ >= 0.99.5 instead of gtk+ 0.99.4
