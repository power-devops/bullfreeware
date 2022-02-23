%define	tclvers		8.4
%define	tclfullvers	8.4.19
%define expvers         5.42
%define expfullvers     5.42.1

Summary: A Tcl/Tk development environment: tcl and tk
Name: tcltk
Version: %{tclfullvers}
Release: 1
Source0: ftp://ftp.scriptics.com/pub/tcl/tcl8_4/tcl%{tclfullvers}-src.tar.gz
Source1: ftp://ftp.scriptics.com/pub/tcl/tcl8_4/tk%{tclfullvers}-src.tar.gz
License: GPL
Group: Development/Languages
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root
%define DEFCC cc

Buildroot: /var/tmp/%{name}-root
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif


%description
Tcl is a simple scripting language designed to be embedded into other
applications.  Tcl is designed to be used with Tk, a widget set.

%package -n tcl
Summary: An embeddable scripting language.
Group: Development/Languages
URL: http://www.tcl.tk

%description -n tcl
Tcl is a simple scripting language designed to be embedded into other
applications.  Tcl is designed to be used with Tk, a widget set, which is
provided in the tk package.  This package also includes tclsh, a simple example
of a Tcl application.

If you're installing the tcl package and you want to use Tcl for development,
you should also install the tk package.

%package -n tk
Summary: The Tk GUI toolkit for Tcl, with shared libraries.
Group: Development/Languages
URL: http://www.tcl.tk

%description -n tk
Tk is a widget set for the X Window System that is designed to work closely
with the Tcl scripting language.  It allows you to write simple programs with
full featured GUI's in only a little more time then it takes to write a text
based interface.  Tcl/Tk applications can also be run on Windows and Macintosh
platforms.

%prep
%setup -q -c -a 1


%build

# Tcl
cd tcl%{tclfullvers}/unix
./configure --prefix=%{_prefix} --enable-shared \
		--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
make
/usr/bin/ar -qv libtcl%{tclvers}.a  libtcl%{tclvers}.so
cd ../..

# Tk
cd tk%{tclfullvers}/unix
./configure --prefix=%{_prefix} --enable-shared \
		--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}

make
/usr/bin/ar -qv libtk%{tclvers}.a libtk%{tclvers}.so
cd ../..

%install

rm -rf $RPM_BUILD_ROOT
rm -fv *.files*

mkdir -p $RPM_BUILD_ROOT%{_prefix}

# Tcl
cd tcl%{tclfullvers}/unix
make INSTALL_ROOT=$RPM_BUILD_ROOT install
ln -sf libtcl%{tclvers}.so $RPM_BUILD_ROOT%{_prefix}/lib/libtcl.so
ln -sf tclsh%{tclvers} $RPM_BUILD_ROOT%{_prefix}/bin/tclsh
cp  libtcl%{tclvers}.a $RPM_BUILD_ROOT%{_prefix}/lib/
cd ..
mkdir -p $RPM_BUILD_ROOT%{_prefix}/doc/tcl-%{tclfullvers}
cp license.terms README $RPM_BUILD_ROOT%{_prefix}/doc/tcl-%{tclfullvers}
cd ..


( cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)


(cd $RPM_BUILD_ROOT;
find .%{_prefix}/bin .%{_prefix}/include \
	.%{_prefix}/man \
	.%{_prefix}/doc \
	./usr/bin \
	./usr/include \
	./usr/lib \
        .%{_prefix}/lib/* \
            -type f -o -type l | sed 's/^\.//';
 find .%{_prefix}/lib/* -type d | sed 's/^\./%dir /' ) | sort > tcl.files

# Tk
cd tk%{tclfullvers}/unix
make INSTALL_ROOT=$RPM_BUILD_ROOT install
ln -sf libtk%{tclvers}.so $RPM_BUILD_ROOT%{_prefix}/lib/libtk.so
ln -sf wish%{tclvers} $RPM_BUILD_ROOT%{_prefix}/bin/wish
cp  libtk%{tclvers}.a $RPM_BUILD_ROOT%{_prefix}/lib/
cd ..
mkdir -p $RPM_BUILD_ROOT%{_prefix}/doc/tk-%{tclfullvers}
cp license.terms README $RPM_BUILD_ROOT%{_prefix}/doc/tk-%{tclfullvers}
cd ..

( cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)

(cd $RPM_BUILD_ROOT;
 find .%{_prefix}/bin .%{_prefix}/include \
	.%{_prefix}/man \
	.%{_prefix}/doc \
	./usr/bin \
	./usr/include \
	./usr/lib \
        .%{_prefix}/lib/* \
            -type f -o -type l | sed 's/^\.//';
 find .%{_prefix}/lib/* -type d | sed 's/^\./%dir /' ) | \
	cat - tcl.files | sort | uniq -u  > tk.files

#Strip the binaries
/usr/bin/strip $RPM_BUILD_ROOT%{_prefix}/bin/* || :

%clean
rm -rf $RPM_BUILD_ROOT
rm -f *.files*

%files -f tcl.files -n tcl
%defattr(-,root,system)

%files -f tk.files -n tk
%defattr(-,root,system)

%changelog
* Mon Oct  27 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 8.4.19
- Update to Tcl/Tk 8.4.19

* Mon Oct  2 2006 Reza Arbab <arbab@austin.ibm.com> 8.4.7-3
- Add %%defattr.

* Wed Sep  6 2006 Reza Arbab <arbab@austin.ibm.com> 8.4.7-2
- Fix broken symlinks for tclsh, wish, libtcl.so, and libtk.so.

* Thu Jul 13 2006 Reza Arbab <arbab@austin.ibm.com> 8.4.7-1
- Update to Tcl/Tk 8.4.7 and expect 5.42.1.

* Tue Mar 22 2005 David Clissold <cliss@austin.ibm.com> 8.3.3-9
- Add patch for Unix write of 0 bytes.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Thu Feb 14 2002 Marc Stephenson <marc@austin.ibm.com>
- Fix configure bugs for AIX 5

* Fri Feb 08 2002 Marc Stephenson <marc@austin.ibm.com>
- New version

* Wed Jun 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 8.3.3

* Fri Apr 06 2001 David Clissold <cliss@austin.ibm.com>
- Modifications required to build on AIX5.1 on IA64

* Thu Apr 05 2001 David Clissold <cliss@austin.ibm.com>
- Add sections for Expect to build
- Add patch for configure & m4 files (so tcl will build on AIX/ia64)

* Fri Mar 09 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Tue Feb 20 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make changes from bug number 7602
- Apply patch from bug number 7537
- Apply fix from bug number 7157
- Add fixes from bug #7601 to the runtcl patch

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions
- man pages are compressed (whatapain)

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- fix tclX symlinks.
- compile on systems where SIGPWR == SIGLOST.

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update tcl/tk to 8.0.5.
- avoid "containing" in Tix (#2332).

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- use /usr/bin/write in kibitz (#1320).
- use cirrus.sprl.umich.edu in weather (#1926).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 28)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- whoops, exec-prefix for itcl was set to '/foo', changed to '/usr'.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- expect does unaligned access on alpha (#989)
- upgrade tcl/tk/tclX to 8.0.4
- upgrade expect to 5.28.
- add itcl 3.0.1

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow building on the arm
- build for glibc 2.1
- strip binaries

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- expect: mkpasswd needs delay before sending password (problem #576)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed expect binaries exec permissions

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated to Tix 4.1.0.006
- updated version numbers of tcl/tk to relflect includsion of p2

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tcl/tk to patch level 2
- updated tclX to 8.0.2

* Thu Oct 30 1997 Otto Hammersmith <otto@redhat.com>
- fixed filelist for tix... replacing path to the expect binary in scripts
  was leaving junk files around.

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- added patch to remove libieee test in configure.in for tcl and tk.
  Shoudln't be needed anymore for glibc systems, but this isn't the "proper" 
  solution for all systems
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks
