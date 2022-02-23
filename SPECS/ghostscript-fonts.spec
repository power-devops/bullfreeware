Summary: Fonts for the Ghostscript PostScript(TM) interpreter.
Name: ghostscript-fonts
Version: 6.0
Release: 1
License: GPL
Group: Applications/Publishing
BuildRoot: /var/tmp/gsfonts-root
URL: http://gnu-gs.sourceforge.net/
Source0: ftp://ftp.gnu.org/pub/gnu/ghostscript/gnu-gs-fonts-std-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/ghostscript/gnu-gs-fonts-other-%{version}.tar.gz
Prefix: %{_prefix}
BuildArchitectures: noarch

%description
Ghostscript-fonts contains a set of fonts that Ghostscript, a
PostScript interpreter, uses to render text. These fonts are in
addition to the fonts shared by Ghostscript and the X Window System.

You'll need to install ghostscript-fonts if you're installing
ghostscript.

%prep
%setup -q -c ghostscript-fonts-%{version} -b 1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/fonts/default/ghostscript
cp fonts/* $RPM_BUILD_ROOT%{prefix}/share/fonts/default/ghostscript

mkdir -p $RPM_BUILD_ROOT%{prefix}/share/ghostscript
ln -s ../fonts/default/ghostscript $RPM_BUILD_ROOT%{prefix}/share/ghostscript/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/share/fonts/default/ghostscript
%{prefix}/share/ghostscript/fonts

%changelog
* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.50

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- renamed package to be consistent with new ghostscript.

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- removed the std fonts...now shared between X11 and gs with URW fonts pkg.

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.03.

* Mon May 04 1998 Erik Troan <ewt@redhat.com>
- set the owner and group of all of the files to 0.0

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
