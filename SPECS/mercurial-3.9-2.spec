%define __python /opt/freeware/bin/python2

%define _emacs_bytecompile  /opt/freeware/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
%define _emacs_sitelispdir  /opt/freeware/share/emacs/site-lisp
%define _emacs_sitestartdir /opt/freeware/share/emacs/site-lisp


%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define gcc_compiler 1

Summary: Mercurial -- a distributed SCM
Name: mercurial
Version: 3.9
Release: 2%{?dist}
# Release: 1.rc1%{?dist}

#% define upstreamversion %{version}-rc
%define upstreamversion %{version}


License: GPLv2+
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
#Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
Source0: http://www.selenic.com/mercurial/release/%{name}-%{upstreamversion}.tar.gz
Source1: mercurial-site-start.el

#Patch0: mercurial-i18n.patch
#Patch1: docutils-0.8.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: python python-devel bash-completion
BuildRequires: emacs-nox emacs-el pkgconfig gettext
#BuildRequires: python-docutils

# For tests
BuildRequires: unzip

Requires: python emacs-filesystem
Provides: hg = %{version}-%{release}
Obsoletes: emacs-mercurial <= 3.4.1, emacs-mercurial-el <= 3.4.1
Provides:  emacs-mercurial <= 3.4.1, emacs-mercurial-el <= 3.4.1

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: http://www.selenic.com/mercurial/wiki/index.cgi/QuickStart
Tutorial: http://www.selenic.com/mercurial/wiki/index.cgi/Tutorial
Extensions: http://www.selenic.com/mercurial/wiki/index.cgi/CategoryExtension

%define pkg mercurial

# If the emacs-el package has installed a pkgconfig file, use that to determine

%package hgk
Summary:	Hgk interface for mercurial
Group:		Development/Tools
Requires:	hg = %{version}-%{release}, tk


%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

Adds the "hg view" command.  See 
http://www.selenic.com/mercurial/wiki/index.cgi/UsingHgk for more
documentation.

%prep
#%setup -q
%setup -q -n %{name}-%{upstreamversion}
#%patch0 -p0
#%patch1 -p1


%build

export CONFIG_SHELL=%{_prefix}/bin/bash
export CONFIGURE_ENV_ARGS=%{_prefix}/bin/bash

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

#export CFLAGS="  -I/usr/include -I%{_prefix}/include"
#export CPPFLAGS="-I/usr/include -I%{_prefix}/include"

# -qinfo=als generate a XLC internal error when compiling Objects/typeobject.c
#export OPT="-g -O0 -qinfo=als"
#export OPT="-g -O0"
export OPT="-O2"



# Chose GCC or XLC
%if %{gcc_compiler} == 1

# -fno-strict-aliasing -fwrapv"
export CFLAGS="  $RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export OPT="     $RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC"
export LDFLAGS="$RPM_LD_FLAGS"

export  CC="/usr/bin/gcc"
export CXX="/usr/bin/gcc"

export FLAG32="-maix32"

export  CC_FOR_CONFIGURE="$CC"
export CXX_FOR_CONFIGURE="$CXX"

%else

#export XLCCPATH="/usr/vac/bin"
#export XLCXXPATH="/usr/vac/bin"
export XLCCPATH="/opt/IBM/xlc/13.1.3/bin"
export XLCXXPATH="/opt/IBM/xlC/13.1.3/bin"

export  CC="$XLCCPATH/xlc_r"
export CXX="$XLCXXPATH/xlC_r"
export FLAG32="-q32"

export  CC_FOR_CONFIGURE=" $CC  -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -q32 -qbitfields=signed -qmaxmem=70000 -qalloca -bmaxdata:0x80000000 -Wl,-brtl"
export CXX_FOR_CONFIGURE=" $CXX -DAIX_GENUINE_CPLUSCPLUS -D_LINUX_SOURCE_COMPAT -q32 -qbitfields=signed -qmaxmem=70000          -bmaxdata:0x80000000 -Wl,-brtl"

%endif


type $CC
type $CXX

export  CC32="${CC}  ${FLAG32}"
export CXX32="${CXX} ${FLAG32}"
export  CC64="${CC}  ${FLAG64}"
export CXX64="${CXX} ${FLAG64}"

# build 32-bit version
export OBJECT_MODE=32
export CC=${CC32}
export CXX=${CXX32}
export LDFLAGS="-L. -L/usr/lib/threads -L%{libdir} -L%{_libdir} -L/usr/lib/lib -L/usr/lib"

gmake build
#gmake doc


%install
rm -rf $RPM_BUILD_ROOT

set -x

%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT --prefix %{_prefix} --record=%{name}.files

#gmake install-doc DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

grep -v -e 'hgk.py*' -e %{python_sitearch}/mercurial/ -e %{python_sitearch}/hgext/ < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

install -D -m 755 contrib/hgk       $RPM_BUILD_ROOT%{_libexecdir}/mercurial/hgk
install    -m 755 contrib/hg-ssh    $RPM_BUILD_ROOT%{_bindir}

bash_completion_dir=$RPM_BUILD_ROOT$(pkg-config --variable=completionsdir bash-completion)
mkdir -p $bash_completion_dir
install -m 644 contrib/bash_completion $bash_completion_dir/hg

zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 contrib/zsh_completion $zsh_completion_dir/_mercurial

mkdir -p $RPM_BUILD_ROOT%{_emacs_sitelispdir}/mercurial

cd contrib
for file in mercurial.el mq.el; do
  #emacs -batch -l mercurial.el --no-site-file -f batch-byte-compile $file
  %{_emacs_bytecompile} $file
  install -p -m 644 $file ${file}c $RPM_BUILD_ROOT%{_emacs_sitelispdir}/mercurial
  rm ${file}c
done
cd -

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

mkdir -p $RPM_BUILD_ROOT%{_emacs_sitestartdir} && install -m644 %SOURCE1 $RPM_BUILD_ROOT%{_emacs_sitestartdir}

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=

[hgk]
path=%{_libexecdir}/mercurial/hgk
EOF
install -m 644 hgk.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

cat > certs.rc <<EOF
# see: http://mercurial.selenic.com/wiki/CACertificates
[web]
cacerts = /etc/pki/tls/certs/ca-bundle.crt
EOF
install -m 644 certs.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

mv     $RPM_BUILD_ROOT%{python_sitearch}/mercurial/locale $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{python_sitearch}/mercurial/locale


%find_lang hg

grep -v locale %{name}-base.files > %{name}-base-filtered.files


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}-base-filtered.files -f hg.lang
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README *.cgi contrib/*.fcgi contrib/*.wsgi
#%doc doc/hg*.txt doc/hg*.html 
#%doc %attr(644,root,root) %{_mandir}/man?/hg*.gz
%doc %attr(644,root,root) contrib/*.svg
%dir %{_datadir}/zsh/
%{_datadir}/zsh/site-functions/
#%{_datadir}/zsh/site-functions/_mercurial Twice ?!?
%{_bindir}/hg-ssh
%{_datadir}/bash-completion/
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%{python_sitearch}/mercurial
%{python_sitearch}/hgext
%{_emacs_sitelispdir}/mercurial
%{_emacs_sitestartdir}/*.el

%config(noreplace) %{_sysconfdir}/mercurial/hgrc.d/certs.rc


%files hgk -f %{name}-hgk.files
%defattr(-,root,root,-)
%{_libexecdir}/mercurial/
%{_sysconfdir}/mercurial/hgrc.d/hgk.rc

##%%check
##cd tests && %{__python} run-tests.py

%changelog
* Thu Aug 18 2016 Tony Reix <tony.reix@atos.net> - 3.9-2
- -O2

* Tue Aug 16 2016 Tony Reix <tony.reix@atos.net> - 3.9-1
- Initial port on AIX 6.1

* Tue Aug 16 2016 Tony Reix <tony.reix@atos.net> - 3.7.3-1
- Initial port on AIX 6.1

* Tue Mar 29 2016 Neal Becker <ndbecker2@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Fri Feb 25 2016 Neal Becker <ndbecker2@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Neal Becker <ndbecker2@gmail.com> - 3.6.3-1
- Update to 3.6.3

* Thu Dec 24 2015 Neal Becker <ndbecker2@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Fri Sep 11 2015 Neal Becker <ndbecker2@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Wed Aug 12 2015 Neal Becker <ndbecker2@gmail.com> - 3.5-1
- Update to 3.5

* Tue Jun 23 2015 Neal Becker <ndbecker2@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Obsolete emacs-mercurial{-el}
- own _emacs_sitelispdir/mercurial
- use standard emacs macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr  3 2015 Neal Becker <ndbecker2@gmail.com> - 3.3.3-1
- update to 3.3.3

* Mon Mar 16 2015 Neal Becker <ndbecker2@gmail.com> - 3.3.2-1
- Update to 3.3.2
- upstream dropped mergetools.rc

* Sat Jan 24 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.2.3-2
- Install bash completion to %%{_datadir}/bash-completion/completions

* Sun Dec 21 2014 nbecker <ndbecker2@gmail.com> - 3.2.3-1
- Fixes CVE-2014-9390

* Tue Dec 16 2014 nbecker <ndbecker2@gmail.com> - 3.2-1
- Update to 3.2.2

* Sun Oct 19 2014 nbecker <ndbecker2@gmail.com> - 3.2-1.rc
- Patch0 no longer needed?
- Drop sample.hgrc (from upstream)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 nbecker <ndbecker2@gmail.com> - 3.0-1
- fix Release

* Fri May 30 2014 nbecker <ndbecker2@gmail.com> - 3.0-
- Update to 3.0

* Wed Feb  5 2014 nbecker <ndbecker2@gmail.com> - 2.9-1
- Update to 2.9

* Fri Nov  8 2013 nbecker <ndbecker2@gmail.com> - 2.8-1
- Update to 2.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 nbecker <ndbecker2@gmail.com> - 2.6.3-1
- Update to 2.6.3


* Thu Jun 6 2013 nbecker <ndbecker2@gmail.com> - 2.6.2-1
- Update to 2.6.2

* Wed May  8 2013 nbecker <ndbecker2@gmail.com> - 2.6-1
- Update to 2.6

* Mon Mar 18 2013 nbecker <ndbecker2@gmail.com> - 2.5.2-2
- Add hgweb.wsgi

* Sat Mar  2 2013 nbecker <ndbecker2@gmail.com> - 2.5.2-1
- Update to 2.5.2

* Sat Feb  9 2013 Neal Becker <ndbecker2@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Tue Feb  5 2013 Neal Becker <ndbecker2@gmail.com> - 2.5-1
- Update to 2.5

* Sun Dec 16 2012 Neal Becker <ndbecker2@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Sun Nov  4 2012 Neal Becker <ndbecker2@gmail.com> - 2.4-1
- Update to 2.4

* Wed Sep  5 2012 Neal Becker <ndbecker2@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Mon Aug 13 2012 Neal Becker <ndbecker2@gmail.com> - 2.3-1
- Update to 2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.3-1
- Update to 2.2.3

* Sun Jun  3 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.2-1
- Update to 2.2.2

* Fri May 25 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.1-2
- Add certs.rc

* Fri May  4 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.1-1
- update to 2.2.1

* Wed May  2 2012 Neal Becker <ndbecker2@gmail.com> - 2.2-1
- Update to 2.2

* Fri Apr  6 2012 Neal Becker <ndbecker2@gmail.com> - 2.1.2-1
- Update to 2.1.2

* Sat Mar 10 2012 Neal Becker <ndbecker2@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan  1 2012 Neal Becker <ndbecker2@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Wed Nov 16 2011 Neal Becker <ndbecker2@gmail.com> - 2.0-1
- Update to 2.0

* Tue Oct 11 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.3-2
- Fix br 744931 (unowned dir)

* Sun Oct  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.3-1
- update to 1.9.3

* Sat Aug 27 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.2-1
- Update to 1.9.2

* Wed Aug  3 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Fri Jul  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.9-2
- Remove docutils patch

* Fri Jul  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.9-1
- Update to 1.9

* Thu Jun  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.4-2
- Add docutils-0.8 patch

* Wed Jun  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.4-1
- Update to 1.8.4

* Sat Apr  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.2-1
- update to 1.8.2

* Mon Mar 14 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.1-2
- Try BR emacs-nox

* Mon Mar 14 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Wed Mar  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8-1
- Update to 1.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Neal Becker <ndbecker2@gmail.com> - 1.7.5-1
- Update to 1.7.5

* Sun Jan  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.7.3-1
- Update to 1.7.3

* Thu Dec  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Mon Nov 15 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7-3
- BR python-docutils

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7-2
- Make that 1.7

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 21 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-4
- Try another way to own directories

* Wed Oct 20 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-3
- Fixup unowned directories

* Wed Oct  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-3
- patch i18n.py so hg will find moved locale files

* Fri Oct  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-1
- Update to 1.6.4

* Fri Aug 27 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.3-1
- Fix some rpmlint issues

* Thu Aug 26 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Mon Aug  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul  4 2010 Neal Becker <ndbecker2@gmail.com> - 1.6-2
- Remove hg-viz, git-rev-tree

* Sun Jul  4 2010 Neal Becker <ndbecker2@gmail.com> - 1.6-1
- Update to 1.6
- git-viz is removed

* Fri Jun 25 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.4-1
- Don't install mercurial-convert-repo (use hg convert instead)

* Wed Jun  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Fri May 14 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Mon May  3 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.2-1
- update to 1.5.2

* Mon Apr  5 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Sat Mar  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.5-2
- doc/ja seems to be gone

* Sat Mar  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.5-1
- Update to 1.5

* Fri Feb  5 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.3-2
- License changed to gplv2+

* Mon Feb  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Sat Jan  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Wed Dec  2 2009 Neal Becker <ndbecker2@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Mon Nov 16 2009 Neal Becker <ndbecker2@gmail.com> - 1.4-1.1
- Bump to 1.4-1.1

* Mon Nov 16 2009 Neal Becker <ndbecker2@gmail.com> - 1.4-1
- Update to 1.4

* Fri Jul 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.3.1-3
- Disable self-tests

* Fri Jul 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.3.1-2
- Update to 1.3.1

* Wed Jul  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.3-2
- Re-enable tests since they now pass

* Wed Jul  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.3-1
- Update to 1.3

* Sat Mar 21 2009 Neal Becker <ndbecker2@gmail.com> - 1.2.1-1
- Update to 1.2.1
- Tests remain disabled due to failures

* Wed Mar  4 2009 Neal Becker <ndbecker2@gmail.com> - 1.2-2
- patch0 for filemerge bug should not be needed

* Wed Mar  4 2009 Neal Becker <ndbecker2@gmail.com> - 1.2-1
- Update to 1.2

* Tue Feb 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-7
- Use noreplace option on config

* Mon Feb 23 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-6
- Fix typo

* Mon Feb 23 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-5
- Own directories bash_completion.d and zsh/site-functions
  https://bugzilla.redhat.com/show_bug.cgi?id=487015

* Mon Feb  9 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-4
- Mark mergetools.rc as config

* Sat Feb  7 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-3
- Patch mergetools.rc to fix filemerge bug

* Thu Jan  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-2
- Rename mergetools.rc -> mergetools.rc.sample

* Thu Jan  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-1
- Update to 1.1.2

* Wed Dec 24 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-3
- Install mergetools.rc as mergetools.rc.sample

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-2
- Fix typo

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1-2
- Rebuild for Python 2.6

* Tue Dec  2 2008 Neal Becker <ndbecker2@gmail.com> - 1.1-1
- Update to 1.1

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-4
- Bump tag

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-3
- Remove BR asciidoc
- Use macro for python executable

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.2-2
- Rebuild for Python 2.6

* Fri Aug 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-4
- Bitten by expansion of commented out macro (again)

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-3
- Add BR pkgconfig

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-2
- Update to 1.0.1
- Fix emacs_version, etc macros (need expand)
- Remove patch0

* Mon Jun  2 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-15
- Bump release tag

* Thu Apr 17 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-14
- Oops, fix %%files due to last change

* Wed Apr 16 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-13
- install mergetools.hgrc as mergetools.rc

* Sat Apr 12 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-12
- Remove xemacs pkg - this is moved to xemacs-extras
- Own %{python_sitearch}/{mercurial,hgext} dirs

* Thu Apr 10 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-11
- Use install -p to install .el{c} files
- Don't (load mercurial) by default.

* Wed Apr  9 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-10
- Patch to hgk from Mads Kiilerich <mads@kiilerich.com>

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-9
- Add '-l mercurial.el' for emacs also

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-8
- BR xemacs-packages-extra

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-7
- Various fixes

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-6
- fix to comply with emacs packaging guidelines

* Thu Mar 27 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-5
- Move hgk-related py files to hgk
- Put mergetools.hgrc in /etc/mercurial/hgrc.d
- Add hgk.rc and put in /etc/mercurial/hgrc.d

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-4
- Rename mercurial-site-start -> mercurial-site-start.el

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-3
- Incorprate suggestions from hopper@omnifarious.org

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-2
- Add site-start

* Tue Mar 25 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-1
- Update to 1.0
- Disable check for now - 1 test fails
- Move emacs to separate package
- Add check

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-7
- Autorebuild for GCC 4.3

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-6
- rpmlint fixes

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-5
- /etc/mercurial/hgrc.d missing

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-3
- Fix to last change

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-2
- mkdir /etc/mercurial/hgrc.d for plugins

* Tue Oct 23 2007  <ndbecker2@gmail.com> - 0.9.5-2
- Bump tag to fix confusion

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-1
- Sync with spec file from mercurial

* Sat Sep 22 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-8
- Just cp contrib tree.
- Revert install -O2

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-7
- Change setup.py install to -O2 to get bytecompile on EL-4

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-6
- Revert last change.

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-5
- Use {ghost} on contrib, otherwise EL-4 build fails

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-4
- remove {_datadir}/contrib stuff for now

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-3
- Fix mercurial-install-contrib.patch (/usr/share/mercurial->/usr/share/mercurial/contrib)

* Wed Aug 29 2007 Jonathan Shapiro <shap@eros-os.com> - 0.9.4-2
- update to 0.9.4-2
- install contrib directory
- set up required path for hgk
- install man5 man pages

* Thu Aug 23 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-1
- update to 0.9.4

* Wed Jan  3 2007 Jeremy Katz <katzj@redhat.com> - 0.9.3-1
- update to 0.9.3
- remove asciidoc files now that we have them as manpages

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 0.9.2-1
- update to 0.9.2

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-2
- rebuild

* Tue Jul 25 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-1
- update to 0.9.1

* Fri May 12 2006 Mihai Ibanescu <misa@redhat.com> - 0.9-1
- update to 0.9

* Mon Apr 10 2006 Jeremy Katz <katzj@redhat.com> - 0.8.1-1
- update to 0.8.1
- add man pages (#188144)

* Fri Mar 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-3
- rebuild

* Fri Feb 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-2
- rebuild

* Mon Jan 30 2006 Jeremy Katz <katzj@redhat.com> - 0.8-1
- update to 0.8

* Thu Sep 22 2005 Jeremy Katz <katzj@redhat.com> 
- add contributors to %%doc

* Tue Sep 20 2005 Jeremy Katz <katzj@redhat.com> - 0.7
- update to 0.7

* Mon Aug 22 2005 Jeremy Katz <katzj@redhat.com> - 0.6c
- update to 0.6c

* Tue Jul 12 2005 Jeremy Katz <katzj@redhat.com> - 0.6b
- update to new upstream 0.6b

* Fri Jul  1 2005 Jeremy Katz <katzj@redhat.com> - 0.6-1
- Initial build.

