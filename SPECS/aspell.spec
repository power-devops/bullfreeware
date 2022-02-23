Summary: A spelling checker.
Name: aspell
Version: 0.33.6.3
Release: 5
License: LGPL
Group: Applications/Text
URL: http://aspell.sourceforge.net/
Source0: http://download.sourceforge.net/aspell/%{name}-.33.6.3.tar.gz
Source1: aspell-init.el
Patch0: aspell-.33.6.3-ltconf.patch
Patch1: aspell-.33.6.3-pspell.patch
Requires: pspell = 0.12.2
Buildrequires: pspell-devel = 0.12.2
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Obsoletes: ispell
Prefix: %{_prefix}

%description
Aspell is a spelling checker designed to eventually replace Ispell.
It also has support for checking (La)TeX and Html files, and run time
support for other non-English languages.

%package	devel
Summary: The static libraries and header files needed for Aspell development.
Group: Development/Libraries
Requires: pspell-devel aspell = %{version}

%description	devel
Aspell is a spelling checker. The aspell-devel package includes the
static libraries and header files needed for Aspell development.  Note
that the recommend way to use aspell is through the Pspell library.

%package en-gb
Summary: British dictionary for aspell
Group: Applications/Text
Requires: aspell

%description en-gb
A British dictionary for use with aspell, a spelling checker.

%package en-ca
Summary: Canadian dictionary
Group: Applications/Text
Requires: aspell

%description en-ca
A Canadian dictionary for use with aspell, a spelling checker.

%ifarch ia64
  %define stdlib lib/ia64l32
  %define stdlib64 lib/ia64l64
  %define liblink ../../..
  %define PKG64 %{name}-%{version}-ia64l64
  %define DEFCC cc
%else
  %define stdlib lib
  %define liblink ../..
  %define DEFCC gcc
%endif

%prep
rm -rf $RPM_BUILD_ROOT

%ifarch ia64
%setup -q -c -n %{PKG64}
%endif
%setup -q -n aspell-.33.6.3
%patch0 -p1 -b .ltpatch
%patch1 -p1 -b .pspell

%build
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi

configure --prefix=%{prefix}
make

%ifarch ia64
cd ../%{PKG64}/%{name}-%{version}
export CC64="$CC -q64"
export CC="$CC64"
configure --prefix=%{prefix}
make
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{prefix}
mkdir -p $RPM_BUILD_ROOT/usr/bin

make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/emacs/site-lisp/site-start.d
mkdir -p $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d
install -m 755 scripts/spell  $RPM_BUILD_ROOT%{prefix}/bin/spell
install -m 755 scripts/ispell $RPM_BUILD_ROOT%{prefix}/bin/ispell
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/share/emacs/site-lisp/site-start.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d

cp -pr $RPM_BUILD_ROOT%{prefix}/doc/aspell .
rm -f aspell/manual.aux

( cd $RPM_BUILD_ROOT
   /usr/bin/strip ./%{prefix}/bin/* || :
  cd -
)

( cd $RPM_BUILD_ROOT
 for dir in bin include share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 # Remove conflict with /usr/bin/spell from bos.txt.spell
 rm -f usr/bin/spell
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf %{prefix}/bin/spell .
 cd -

 mkdir -p usr/%{stdlib}
 cd usr/%{stdlib}
 ln -sf %{liblink}%{prefix}/lib/* .
 cd -
 rm -f usr/%{stdlib}/xemacs   # The xemacs package owns this link
)

%ifos linux
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif
    
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README TODO aspell/*
%{prefix}/bin/*
%{prefix}/lib/aspell/american*
%{prefix}/lib/aspell/english*
%{prefix}/lib/lib*aspell.a
%{prefix}/share/aspell
%{prefix}/share/pspell
%{prefix}/share/emacs/site-lisp/site-start.d/*
%{prefix}/lib/xemacs/xemacs-packages/lisp/site-start.d/*
/usr/bin/*
/usr/linux/bin/*
/usr/lib/aspell
/usr/lib/*.a
/usr/share/aspell

%files		devel
%defattr(-,root,root)
%{prefix}/include/aspell
/usr/include/aspell/*
%{prefix}/lib/*.la
/usr/lib/*.la

%files en-ca
%defattr(-,root,root)
%{prefix}/lib/aspell/canadian*
/usr/lib/aspell/canadian*

%files en-gb
%defattr(-,root,root)
%{prefix}/lib/aspell/british*
/usr/lib/aspell/british*

%changelog
* Mon Nov 05 2001 Marc Stephenson <marc@austin.ibm.com>
- Squash /usr/bin link

* Tue Sep 04 2001 David Clissold <cliss@austin.ibm.com>
- Rev. 4; the /usr/lib/*.la files were symlinked to nowhere.
-   And they should be in the devel package, not the main package.

* Tue Jul 03 2001 David Clissold <cliss@austin.ibm.com>
- Rev. 3; aspell and word-list-compress were not stripped.

* Thu Jun 14 2001 David Clissold <cliss@austin.ibm.com>
- Rev. 2; aspell should not own the /usr/lib/xemacs link

* Mon Jun 04 2001 David Clissold <cliss@austin.ibm.com>
- Initial build for AIX Toolbox (using 0.33.6.3)

* Sun May 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.6
- use standard %%configure macro - it works now.

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.33.5-2
- Rebuild with new libltdl

* Mon Apr 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.33.5

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use new emacs init scheme for Emacs and XEmacs

* Wed Nov 22 2000 Trond Eivind Glomsrød <teg@redhat.com>
-  .32.6

* Sat Aug 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.5 bugfix release (also contains improved documentation),
  obsolete old patch
- the compatibility scripts are now part of the package itself
- clean up build procedure
- remove manual.aux file from docs (#16424)

* Sun Aug 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32.1 bugfix release, obsolete old patch
- rename to 0.32.1
- add patch from author to change his email address
- add spell and ispell compatibility scripts

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Aug 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remember to obsolete ispell
- build the Canadian and British dictionaries here now,
  as part of the main package. Same package names and 
  descriptions.

* Mon Jul 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- .32
- remove old patches, add a patch since namespace isn't 
  polluted as much anymore (as opposed to older toolchain)

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use RPM_OPT_FLAGS, not just -O0
- dont include .la-files

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- excludearch ia64

* Fri Jun 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patch to work around compiler bug(?) wrt. inline functions
- use CFLAGS and CXXFLAGS
- set them to -O0 to work around YACB
- copy libtool files for IA64 support

* Sun Jun 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update to .31.1. My patch was upstreamed and is no longer needed.
- new patch added so DESTDIR works properly

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- (this entry includes some old ones...)
- update to .31
- added patch to make it compile with a pickier compiler
- include /usr/share/pspell

* Mon May 1 2000 Tim Powers <timp@redhat.com>
- updated to .30.1
- used build fixes from Ryan Weaver's 0.30.1-1 package on sourceforge
- updated URL, download/ftp location
- removed redundant define's at top of spec file

* Thu Jul 8 1999 Tim Powers <timp@redhat.com>
- built for Powertools 6.1
- removed %serial definitions from spec file to make versioning
  consistant with the other packages we ship.
- changed build root path
- general spec file cleanups

* Tue Mar  2 1999 Ryan Weaver <ryanw@infohwy.com>
  [aspell-.27.2-2]
- Changes from .27.1 to .27.2 (Mar 1, 1999)
- Fixed a major bug that caused aspell to dump core when used
  without any arguments
- Fixed another major bug that caused aspell to do nothing when used
  in interactive mode.
- Added an option to exit in Aspell's interactive mode.
- Removed some old documentation files from the distribution.
- Minor changes on to the section on using Aspell with egcs.
- Minor changes to remove -Wall warnings.
