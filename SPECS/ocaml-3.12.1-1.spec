%define build_ocamlopt	1
%ifarch ppc64 %mips %arm
%define build_ocamlopt	0
%endif
# To avoid the TARGET_none issue
%define build_ocamlopt	0


%define build_labltk	1
%define name	ocaml
%define major	3.12
%define minor	0
%define version	3.12.1
%define release	1

# we don't want the auto require to add require on the currently installed ocaml
%define _requires_exceptions ocaml

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Objective Caml compiler and programming environment
URL:		http://caml.inria.fr
License:	QPL with exceptions and LGPLv2 with exceptions
Group:		Development/Other
Source0:	http://caml.inria.fr/pub/distrib/ocaml-%{major}/%{name}-%{version}.tar.bz2
Source1:	http://caml.inria.fr/pub/distrib/ocaml-%{major}/%{name}-%{major}-refman.html.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

# IMPORTANT:
# The contents (META's files) of this tarball comes from findlib
# This tarball have to be updated when findlib or ocaml are updated to a new version
# these META's files are only generated by the ./configure in the findlib source directory
# (camlp4 and ocaml-labltk have to be installed for this operation)
# then just:
# tar cfj  findlib-1.2.8-ocaml-3.12.1-meta-files.tar.bz2  site-lib-src/*/META
Source5:	findlib-1.2.8-ocaml-3.12.1-meta-files.tar.bz2

Patch3:		ocaml-3.11.0-ocamltags-no-site-start.patch
Patch6:		ocaml-3.04-do-not-add-rpath-X11R6_lib-when-using-option-L.patch
Patch7:		ocaml-3.11.0-no-opt-for-debug-and-profile.patch
Patch8:		ocaml-3.04-larger-buffer-for-uncaught-exception-messages.patch
Patch9:		ocaml-3.12.0-handle-tk-8.6.patch
Patch16:	ocaml-3.09.2-lib64.patch
Patch17:	ocaml-3.11.0-db4.patch
Patch18:	ocaml-3.09.3-compile-emacs-files-in-build-dir.patch

Patch19:	ocaml-3.12.1-byterun.Makefile.patch

#BuildRequires:	libx11-devel
BuildRequires:	ncurses-devel
BuildRequires:	tcl
BuildRequires:	tcl-devel
BuildRequires:	tk
BuildRequires:	tk-devel
BuildRequires:	emacs
# Berkeley db4 is db on BullFreeware
#BuildRequires:	db4-devel
BuildRequires:	db-devel

#Requires:	libx11-devel
#Requires:	db4-devel
Requires:	db-devel
Requires:	ncurses-devel

Obsoletes:	ocaml-emacs < %{version}
Provides:	ocaml-emacs = %{version}

%package	doc
Summary:	Documentation for OCaml
Group:		Books/Computer books
Requires:	%{name} = %{version}

%package -n	camlp4
Summary:	Preprocessor for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}

%package -n	camlp4-devel
Summary:	Development files for camlp4
Group:		Development/Other
Requires:	%{name} = %{version}

%package labltk
Summary:	Tk toolkit binding for OCaml
Group:		Development/Other
Requires:	%{name} = %{version}
Requires:	tk-devel
Obsoletes:	ocamltk < %{version}

%package sources
Summary:	OCaml sources
Group:		Development/Other
# don't add crazy deps
AutoReqProv: No

%description
Objective Caml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast byte-code compiler and an
optimizing native-code compiler), an interactive top-level system, Lex&Yacc
tools, a replay debugger, and a comprehensive library.

%description	doc
Documentation for OCaml

%description -n	camlp4
Preprocessor for OCaml

%description -n	camlp4-devel
This package contains the development files needed to build applications
using camlp4.

%description labltk
Tk toolkit binding for OCaml

%description sources
OCaml sources

%prep
%setup -q -T -b 0
%setup -q -T -D -a 1
%setup -q -T -D -a 5
%patch3 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1 -b .tk
%patch16 -p1 -b .lib64
%patch17 -p1 -b .db4
#patch18 -p1 -b .emacs

%patch19 -p1 -b .byterun

rm -rf `/opt/freeware/bin/find -name .cvsignore`

# fix incorrect reference in camlp4 META file
/opt/freeware/bin/sed -ri -e 's|directory = "/opt/freeware/lib.*/ocaml/camlp4"|directory = "%{_libdir}/ocaml/camlp4"|g' site-lib-src/camlp4/META


%build
export MAKE=/opt/freeware/bin/make
export AR=/usr/bin/ar
export ARCH=power-aix

%ifarch alpha
echo %{optflags} | grep -q mieee || { echo "on alpha you need -mieee to compile ocaml"; exit 1; }
%endif

./configure -bindir %{_bindir} -libdir %{_libdir}/ocaml -mandir %{_mandir}/man1

gmake --trace world

# It breaks in TARGET_none because ARCH is not recognized (none)
%if %{build_ocamlopt}
gmake --trace opt opt.opt
%endif

# Tests. Breaks due to pervasives.cmi not found (though exists)
cd testsuite
(gmake all || true)



%install
[ -d "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export MAKE=/opt/freeware/bin/make

gmake install BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir}/ocaml MANDIR=%{buildroot}%{_mandir}


cd emacs; gmake install install-ocamltags BINDIR=%{buildroot}%{_bindir} EMACSDIR=%{buildroot}%{_datadir}/emacs/site-lisp; cd -

# fix
perl -pi -e "s|%{buildroot}||" %{buildroot}%{_libdir}/ocaml/ld.conf

%if %{build_ocamlopt}
# only keep the binary versions, which are much faster, except for camlp4
# as native code cannot do a dynamic load
for i in %{buildroot}%{_bindir}/*.opt ; do
  [[ $i == %{buildroot}%{_bindir}/camlp4* ]] && continue
  ln -sf `basename $i` ${i%.opt}
done
%endif


/opt/freeware/bin/install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
cat <<EOF >%{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
(require 'caml-font)
(autoload 'caml-mode "caml" "Caml editing mode" t)
(add-to-list 'auto-mode-alist '("\\\\.mli?$" . caml-mode))
EOF

# don't package mano man pages since we have the html files
rm -rf %{buildroot}%{_mandir}/mano

# install findlib META files
cp -pr site-lib-src/* %{buildroot}%{_libdir}/ocaml/

rm -f %{name}.list
n="labltk|camlp4|ocamlbrowser|tkanim"
(cd %{buildroot} ; /opt/freeware/bin/find opt/freeware/bin ! -type d -printf "/%%p\n" | grep -v -E $n) >> %{name}.list
(cd %{buildroot} ; /opt/freeware/bin/find opt/freeware/%{_lib}/ocaml ! -type d -printf "/%%p\n" | grep -v -E $n) >> %{name}.list
(cd %{buildroot} ; /opt/freeware/bin/find opt/freeware/%{_lib}/ocaml   -type d -printf "%%%%dir /%%p\n" | grep -v -E $n) >> %{name}.list

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=OCaml
Comment=%{summary}
Exec=%{name}
Icon=interpreters_section
Terminal=true
Type=Application
Categories=Development;
EOF


# install sources
/opt/freeware/bin/install -d -m 755 %{buildroot}%{_prefix}/src
/opt/freeware/bin/tar xvjf %{SOURCE0} -C %{buildroot}%{_prefix}/src
mv %{buildroot}%{_prefix}/src/%{name}-%{version} %{buildroot}%{_prefix}/src/%{name}


%files -f %{name}.list
%doc Changes LICENSE README
%{_mandir}/man1/*
%{_datadir}/applications/*
%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*

%files doc
%doc htmlman/* 
%if %build_ocamlopt
%{_mandir}/man3/*
%endif

%if %{build_labltk}
%files labltk
%doc otherlibs/labltk/README otherlibs/labltk/example*
%{_bindir}/*labltk*
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/*labltk*
#%{_libdir}/ocaml/stublibs/dlllabltk.so
%endif

%files -n camlp4
%{_bindir}/*camlp4*
%dir %{_libdir}/ocaml/camlp4
%dir %{_libdir}/ocaml/camlp4/Camlp4Filters
%dir %{_libdir}/ocaml/camlp4/Camlp4Parsers
%dir %{_libdir}/ocaml/camlp4/Camlp4Printers
%dir %{_libdir}/ocaml/camlp4/Camlp4Top
%{_libdir}/ocaml/camlp4/META
%{_libdir}/ocaml/camlp4/*.cma
%{_libdir}/ocaml/camlp4/*.cmi
%{_libdir}/ocaml/camlp4/*.cmo
%{_libdir}/ocaml/camlp4/*/*.cmi
%{_libdir}/ocaml/camlp4/*/*.cmo

%files -n camlp4-devel
# Missing !
#%{_libdir}/ocaml/camlp4/*.a
#%{_libdir}/ocaml/camlp4/*.o
#%{_libdir}/ocaml/camlp4/*.cmxa
#%{_libdir}/ocaml/camlp4/*.cmx
#%{_libdir}/ocaml/camlp4/*/*.o
#%{_libdir}/ocaml/camlp4/*/*.cmx


%files sources
%{_prefix}/src/%{name}



%changelog

* Fri Aug 24 2018 Tony Reix <tony.reix@atos.net> 3.12.1-1
- First port on AIX 6.1

* Thu Mar 08 2012 malo <malo> 3.12.1-4.mga2
+ Revision: 221439
- fix desktop file (mga#3635)

  + blue_prawn <blue_prawn>
    - updated META files from new findlib 1.2.8
    - Mageia SPEC syntax policy

* Sun Dec 04 2011 malo <malo> 3.12.1-3.mga2
+ Revision: 176299
- missing requires to libx11-devel, db4-devel, ncurses-devel
- splitting camlp4 with devel package, per Ocaml policy

* Sat Dec 03 2011 malo <malo> 3.12.1-2.mga2
+ Revision: 175622
- Fix file duplication in ocaml, camlp4 and ocaml-labltk
- spec cleanup

* Sat Oct 01 2011 shlomif <shlomif> 3.12.1-1.mga2
+ Revision: 150784
- Version 3.12.1 - thanks to Malo.

* Sat Jul 02 2011 fwang <fwang> 3.12.0-3.mga2
+ Revision: 117454
- Adding upstream patch fixing bad interactions between ocaml and binutils 2.21 (see http://caml.inria.fr/mantis/view.php?id=5237)

* Tue Apr 12 2011 ennael <ennael> 3.12.0-2.mga1
+ Revision: 83719
- add missing provides

  + ahmad <ahmad>
    - imported package ocaml


* Sat Aug 28 2010 Florent Monnier <blue_prawn@mandriva.org> 3.12.0-1mdv2011.0
+ Revision: 573767
- updated to last version 3.12.0

* Mon Aug 23 2010 Florent Monnier <blue_prawn@mandriva.org> 3.11.2-4mdv2011.0
+ Revision: 572373
- updated META files provided by findlib version 1.2.6

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.11.2-3mdv2010.1
+ Revision: 512981
- fix camlp4 META file correctly

* Mon Mar 01 2010 Guillaume Rousse <guillomovitch@mandriva.org> 3.11.2-2mdv2010.1
+ Revision: 512910
- emacs is insufficient to compile bytecode, switch to full emacs
- fix incorrect META file for camlp4 on x86_64
- new version

* Fri Jan 01 2010 Oden Eriksson <oeriksson@mandriva.com> 3.11.1-5mdv2010.1
+ Revision: 484726
- rebuilt against bdb 4.8

* Sun Sep 27 2009 Olivier Blin <oblin@mandriva.com> 3.11.1-4mdv2010.0
+ Revision: 450174
- disable ocaml.opt* on mips & arm, not supported
  (from Arnaud Patard)

* Fri Sep 11 2009 Florent Monnier <blue_prawn@mandriva.org> 3.11.1-3mdv2010.0
+ Revision: 438520
- restore the previous solution to manage META files (sync for the tarball)
- restore the previous solution to manage META files

* Wed Sep 09 2009 Florent Monnier <blue_prawn@mandriva.org> 3.11.1-2mdv2010.0
+ Revision: 435818
- this tarball was not updated when ocaml and ocaml-findlib was updated,
  and there are currently things broken with this old tarball,
  instead of updating it, I think it's better to keep it in findlib where it's easier to keep it maintained

* Thu Jun 25 2009 Frederik Himpe <fhimpe@mandriva.org> 3.11.1-1mdv2010.0
+ Revision: 389199
- update to new version 3.11.1

* Wed Dec 24 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.11.0-2mdv2009.1
+ Revision: 318162
- rediff fuzzy patches
- site-lib hierarchy doesn't exist anymore

* Mon Dec 08 2008 Pixel <pixel@mandriva.com> 3.11.0-1mdv2009.1
+ Revision: 311906
- 3.11.0
- rediff/adapt patch9 (tk)

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 3.10.2-5mdv2009.1
+ Revision: 310971
- rebuild for new tcl
- update tcl handling patch for 8.6
- new license policy

* Mon Sep 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.10.2-4mdv2009.0
+ Revision: 284872
- keep both bytecode and native versions for camlp4, as native ones have troubles with dynamic loading

* Mon Sep 01 2008 Guillaume Rousse <guillomovitch@mandriva.org> 3.10.2-3mdv2009.0
+ Revision: 278643
- re-enable optimized versions of camlp4

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 3.10.2-2mdv2009.0
+ Revision: 223356
- rebuild

* Sun Mar 02 2008 Stefan van der Eijk <stefan@mandriva.org> 3.10.2-1mdv2008.1
+ Revision: 177752
- 3.10.2, as per bug 37508

* Thu Dec 27 2007 Oden Eriksson <oeriksson@mandriva.com> 3.10.0-5mdv2008.1
+ Revision: 138206
- rebuilt against bdb 4.6.x libs

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Sep 07 2007 Anssi Hannula <anssi@mandriva.org> 3.10.0-4mdv2008.0
+ Revision: 82024
- rebuild for new soname of tcl

* Sun Sep 02 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.10.0-3mdv2008.0
+ Revision: 78255
- disable automatic dependencies for source package

* Sat Sep 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.10.0-2mdv2008.0
+ Revision: 77694
- add an ocaml-sources subpackage for cduce

* Tue May 29 2007 Pixel <pixel@mandriva.com> 3.10.0-1mdv2008.0
+ Revision: 32452
- new release, 3.10.0
- handle tk 8.5


* Tue Feb 20 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.09.3-5mdv2007.0
+ Revision: 123095
- use relative directory notation for camlp4 META file, so as to fix x86_64 usage

* Tue Feb 20 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.09.3-4mdv2007.1
+ Revision: 123047
- minor spec cleanup
- make sure shared libs under site-lib are available for loading

* Thu Jan 25 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.09.3-3mdv2007.1
+ Revision: 113230
- only ships META files for standard library, not findlib library itself

* Wed Jan 24 2007 Guillaume Rousse <guillomovitch@mandriva.org> 3.09.3-2mdv2007.1
+ Revision: 112752
- ensure emacs bytecode file are compiled in build dir, to avoid wrong files in install dir
- oops, increment release, not minor version
- spec file cleanup
- ship META files for findlib
- rename ocamltk package to ocaml-labltk

  + Crispin Boylan <crisb@mandriva.org>
    - Add patch to use db4 (closes #27858)

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - ppc64 fixes
    - 3.09.3
    - Import ocaml

* Thu Sep 21 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.09.2-4mdv2007.0
- improve lib64 patch for X.org 7.1 paths

* Thu Sep 21 2006 Nicolas L?cureuil <neoclust@mandriva.org> 3.09.2-3mdv2007.0
-  Rebuild against ncurse

* Sat May 20 2006 Guillaume Rousse <guillomovitch@mandriva.org> 3.09.2-2mdk
- ocaml-camltk requires tk-devel

* Tue Apr 25 2006 Pixel <pixel@mandriva.com> 3.09.2-1mdk
- new release

* Fri Jan 13 2006 Pixel <pixel@mandriva.com> 3.09.1-2mdk
- fix typo :-(

* Fri Jan 13 2006 Pixel <pixel@mandriva.com> 3.09.1-1mdk
- new release

* Mon Jan 02 2006 Oden Eriksson <oeriksson@mandriva.com> 3.09.0-2mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Thu Nov 03 2005 Pixel <pixel@mandriva.com> 3.09.0-1mdk 
- new release
- drop add-warning-for-unused-local-variables patch
  (included upstream, neatly called warning "Z" :)

* Wed Apr 27 2005 Per ??yvind Karlsen <peroyvind@mandriva.org> 3.08.3-2mdk
- fix buildrequires
- %%mkrel

* Wed Apr 27 2005 Per ??yvind Karlsen <peroyvind@mandriva.org> 3.08.3-1mdk
- 3.08.3
- cosmetics

* Wed Dec 01 2004 Guillaume Rousse <guillomovitch@mandrake.org> 3.08.2-1mdk 
- new release
- removed packager tag
- rpmbuildupdate aware

* Tue Nov 09 2004 Pixel <pixel@mandrakesoft.com> 3.08.1-1mdk
- new release

* Fri Jul 16 2004 Pixel <pixel@mandrakesoft.com> 3.08-3mdk
- new release

* Tue Jun 29 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.07.2-3mdk
- BuildRequires: tcl

* Sat Apr 17 2004 Pixel <pixel@mandrakesoft.com> 3.07.2-2mdk
- don't modify BYTECCCOMPOPTS and NATIVECCCOMPOPTS, otherwise
  -D_FILE_OFFSET_BITS=64 is dropped (bugzilla #9502)
  => don't pass optflags (hope it won't break AXP which needs -mieee)
- have less warnings when compiling

