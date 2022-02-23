%define vimdir vim74
%define baseversion 7.4

Summary: The VIM editor
URL:     http://www.vim.org/
Name:    vim
Version: %{baseversion}
Release: 4
License: Vim
Group: Applications/Editors
Source0: ftp://ftp.vim.org/pub/vim/unix/%{name}-%{baseversion}.tar.bz2
Source3: gvim.desktop
Source4: vimrc
Source7: gvim16.png
Source8: gvim32.png
Source9: gvim48.png
Source10: gvim64.png
Source12: vi_help.txt
Source14: %{name}-spec-template
Source15: http://www.cvjb.de/comp/vim/forth.vim

Source100: %{name}-%{version}-%{release}.build.log


# patch to make python and perl work
Patch0: %{name}-%{baseversion}-aix-configure.patch

Patch2002: vim-7.0-fixkeys.patch
Patch2003: vim-6.2-specsyntax.patch
Patch2004: vim-7.4-crv.patch

Patch3000: vim-7.4-syntax.patch
Patch3002: vim-7.1-nowarnings.patch
Patch3003: vim-6.1-rh3.patch
Patch3006: vim-6.4-checkhl.patch
Patch3008: vim-7.0-warning.patch
Patch3009: vim-7.0-syncolor.patch
Patch3010: vim-7.0-specedit.patch
Patch3011: vim72-rh514717.patch

Patch5000: vim-7.3-utf8.patch

Buildroot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: python-devel >= 2.7.15-5, gettext, perl >= 5.8.8
BuildRequires: patch, make

BuildRequires: gtk2-devel >= 2.8.3, glib2-devel >= 2.8.1, pango-devel >= 1.10.0
Requires: gettext

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%define osplat aix5
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%define osplat aix6
%endif

%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.

This 7.4-4 release has been built with Python 2.7.15-5 using UCS2.
Previous release 7.4-3 was built with older Python using UCS4.


%package common
Summary: The common files needed by any version of the VIM editor
Group: Applications/Editors

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.


%package minimal
Summary: A minimal version of the VIM editor
Group: Applications/Editors
Provides: vi = %{version}-%{release}
Requires: gettext

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present. NOTE: The online help is only available when the vim-common
package is installed.


%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Group: Applications/Editors
Requires: %{name}-common = %{version}-%{release}
Provides: %{name} = %{version}-%{release}
Requires: gettext
#Requires: perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Requires: perl >= 5.8.8
Requires: python >= 2.7.15-5

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.


%package X11
Summary: The VIM version of the vi editor for the X Window System
Group: Applications/Editors
Requires: %{name}-common = %{version}-%{release}, gtk2 >= 2.8.3
Provides: gvim = %{version}-%{release}
BuildRequires: gtk2-devel >= 2.8.3, glib2-devel >= 2.8.1
BuildRequires: pango-devel >= 1.10.0
Requires: gtk2 >= 2.8.3, glib2 >= 2.8.1
Requires: pango >= 1.10.0
Requires: gettext
#Requires: perl(:MODULE_COMPAT_%(eval "`/usr/bin/perl -V:version`"; echo $version))
Requires: perl >= 5.8.8
Requires: python >= 2.7.15-5

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.


%prep
%setup -q -n %{vimdir}
# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk

export PATH=/opt/freeware/bin:$PATH

%patch2002 -p1
%patch2003 -p1
%patch2004 -p1
perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%patch3000 -p1
%patch3002 -p1
%patch3003 -p1
%patch3006 -p1
%patch3008 -p1
%patch3009 -p1
%patch3010 -p1
%patch3011 -p1

%patch5000 -p1 -b .utf8

%patch0


%build
export PATH=$PATH:/opt/freeware/bin

# for gtk2 we need this compiler
export CC="/usr/vac/bin/xlc_r -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES"

cd src

export PERL=/usr/bin/perl
export CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64"
export LIBPATH="/opt/freeware/lib:/usr/lib:/usr/opt/perl5/lib/5.8.8/aix-thread-multi/CORE"


export vi_cv_path_python_plibs='-L/opt/freeware/lib/python2.7/config -lpython2.7 -ldl -lm -Wl,-bE:/opt/freeware/lib/python2.7/config/App_python.exp -lld'

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --exec-prefix=%{_prefix} \
    --with-features=huge \
    --enable-pythoninterp \
    --enable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-x=yes \
    --enable-xim \
    --enable-multibyte \
    --enable-gui=gtk2 \
    --enable-gtk2-check \
    --with-compiledby="<bullfreeware@project.bull.net>"

gmake --trace
cp vim gvim

make clean

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --bindir=%{_bindir} \
    --exec-prefix=%{_prefix} \
    --with-features=huge \
    --enable-pythoninterp \
    --disable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-x=no \
    --enable-gui=no \
    --enable-multibyte \
    --enable-fontset \
    --with-compiledby="<bullfreeware@project.bull.net>"

gmake --trace
cp vim enhanced-vim

make clean

$PERL -pi -e "s/help.txt/vi_help.txt/" os_unix.h ex_cmds.c
$PERL -pi -e "s/\/etc\/vimrc/\/etc\/virc/" os_unix.h

LIBS=" -L/opt/freeware/lib -L/usr/lib" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --exec-prefix=%{_prefix} \
    --with-features=tiny \
    --with-x=no \
    --disable-pythoninterp \
    --disable-perlinterp \
    --disable-tclinterp \
    --disable-rubyinterp \
    --with-tlib=curses \
    --enable-multibyte \
    --enable-gui=no \
    --disable-gpm \
    --with-compiledby="<bullfreeware@project.bull.net>"

LIBS=" -L/opt/freeware/lib -L/usr/lib" gmake --trace


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export LIBPATH="/opt/freeware/lib:/usr/lib"
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles
cp %{SOURCE14} ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles/template.spec
chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/%{name}/vimfiles/template.spec

cp runtime/doc/uganda.txt LICENSE

# Those aren't GNU info files but some binary files for Amiga:
rm -f README*.info

cd src
gmake --trace install DESTDIR=${RPM_BUILD_ROOT}

cp gvim enhanced-vim ${RPM_BUILD_ROOT}%{_bindir}
chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

# install icons
for i in 16x16 32x32 48x48 64x64 ; do
    mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/${i}/apps
done

cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
cp %{SOURCE8} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
cp %{SOURCE9} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
cp %{SOURCE10} ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/64x64/apps/gvim.png

chmod 0644 ${RPM_BUILD_ROOT}%{_datadir}/icons/hicolor/*/apps/gvim.png

(
  cd ${RPM_BUILD_ROOT}
  mv -f .%{_bindir}/vim .%{_bindir}/vi
  mv -f .%{_bindir}/enhanced-vim .%{_bindir}/vim
  ln -sf vi .%{_bindir}/ex
  ln -sf vi .%{_bindir}/rvi
  ln -sf vim .%{_bindir}/vimdiff
  ln -sf gvim .%{_bindir}/gview
  ln -sf gvim .%{_bindir}/gex
  ln -sf gvim .%{_bindir}/evim
  ln -sf gvim .%{_bindir}/gvimdiff
  ln -sf gvim .%{_bindir}/vimx
  ln -sf vimtutor .%{_bindir}/gvimtutor
  ln -sf vim.1 .%{_mandir}/man1/vi.1
  ln -sf vim.1 .%{_mandir}/man1/rvi.1
  mkdir -p ./etc/X11/applnk/Applications
  cp %{SOURCE3} ./etc/X11/applnk/Applications/gvim.desktop
)

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d
cat >${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/vim.sh <<EOF
if [ -n "\$BASH_VERSION" -o -n "\$KSH_VERSION" -o -n "\$ZSH_VERSION" ]; then
  [ -x %{_bindir}/id ] || return
  [ \`%{_bindir}/id -u\` -le 200 ] && return
  # for bash and zsh, only if no alias is already set
  alias vi >/dev/null 2>&1 || alias vi=vim
fi
EOF
cat >${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/vim.csh <<EOF
[ -x %{_bindir}/id ] || exit
[ \`%{_bindir}/id -u\` -gt 200 ] && alias vi vim
EOF
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/profile.d/*
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/vimrc
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/virc
chmod 0644 ${RPM_BUILD_ROOT}%{_sysconfdir}/vi*rc
(
 mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}/doc
 cd ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}/doc
 cp %{SOURCE12} .
 cat tags | sed -e 's/\t\(.*.txt\)\t/\t\1.gz\t/;s/\thelp.txt.gz\t/\thelp.txt\t/;s/\tversion7.txt.gz\t/\tversion7.txt\t/;s/\tsponsor.txt.gz\t/\tsponsor.txt\t/' > tags.new; mv -f tags.new tags
cat >> tags << EOF
vi_help.txt	vi_help.txt	/*vi_help.txt*
vi-author.txt	vi_help.txt	/*vi-author*
vi-Bram.txt	vi_help.txt	/*vi-Bram*
vi-Moolenaar.txt	vi_help.txt	/*vi-Moolenaar*
vi-credits.txt	vi_help.txt	/*vi-credits*
EOF
 )
rm -f ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/tools
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f ${RPM_BUILD_ROOT}%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~

for i in rvim gvim.1 gvimdiff.1 ; do 
  echo ".so man1/vim.1" > ${RPM_BUILD_ROOT}%{_mandir}/man1/$i
done

cd ${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{vimdir}
cp menu.vim plugin/

# make symlinks
cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
mkdir -p usr/linux/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .
rm -f ex vi view
cd ../../usr/linux/bin
for f in ex vi view ; do
  ln -sf ../../..%{_bindir}/${f} .
done
%post X11
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi


%postun X11
touch -c %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  gtk-update-icon-cache --ignore-theme-index -q %{_datadir}/icons/hicolor
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files common
%defattr(-,root,system)
%config(noreplace) %{_sysconfdir}/vimrc
%doc README* LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{vimdir}
%dir %{_datadir}/%{name}/vimfiles
%{_datadir}/%{name}/vimfiles/template.spec
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
%{_bindir}/xxd
%{_mandir}/man1/vim.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/vi.*
%{_mandir}/man1/view.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/xxd.*
%lang(fr) %{_mandir}/fr*/man1/*
%lang(it) %{_mandir}/it*/man1/*
%lang(pl) %{_mandir}/pl*/man1/*
%lang(ru) %{_mandir}/ru*/man1/*
/usr/bin/xxd


%files minimal
%defattr(-,root,system)
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvi
%{_bindir}/rview
/usr/linux/bin/ex
/usr/linux/bin/vi
/usr/linux/bin/view
/usr/bin/rvi
/usr/bin/rview


%files enhanced
%defattr(-,root,system)
%{_bindir}/vim
%{_bindir}/rvim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%config(noreplace) %{_sysconfdir}/profile.d/vim.*
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*
/usr/bin/vim
/usr/bin/rvim
/usr/bin/vimdiff
/usr/bin/vimtutor


%files X11
%defattr(-,root,system)
/etc/X11/applnk/*/gvim.desktop
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimx
%{_bindir}/evim
%{_mandir}/man1/evim.*
%{_mandir}/man1/gvim*
%{_datadir}/icons/hicolor/*/apps/*
/usr/bin/gvimtutor
/usr/bin/gvim
/usr/bin/gvimdiff
/usr/bin/gview
/usr/bin/gex
/usr/bin/vimx
/usr/bin/evim


%changelog
* Tue Mar 26 2019 Tony Reix <tony.reix@atos.net> 7.4-4
- Rebuilt with Python 2.7.15-5 installed which uses UCS2 symbols (like: PyUnicodeUCS2_RichCompare)

* Wed Aug 08 2018 Michael Wilson <michael.a.wilson@atos.net> 7.4-3
- Rebuild using application usable Python .exp without "_Py" internal symbols

* Wed Feb 22 2017 Tony Reix <tony.reix@atos.net> 7.4-2
- Rebuild with Python 2.7.12 and fix for perl/$PERL.

* Fri Jan 22 2016 Tony Reix <tony.reix@atos.net> 7.4-1
- Build on AIX 6.1

* Wed Apr 26 2012 Gerard Visiedo <gerard.visiedo@bull.net> 7.3.475-2
- Build on Aix6.1

* Tue Mar 20 2012 Michael Perzl <michael@perzl.org> - 7.3.475-1
- updated to version 7.3 patchlevel 7.3.475

* Sun Nov 20 2011 Michael Perzl <michael@perzl.org> - 7.3.353-1
- updated to version 7.3 patchlevel 7.3.353

* Sun Jun 26 2011 Michael Perzl <michael@perzl.org> - 7.3.237-1
- updated to version 7.3 patchlevel 7.3.237
- fixed perl and python inclusion, thus introduced a dependency on those

* Tue Mar 08 2011 Michael Perzl <michael@perzl.org> - 7.3.138-1
- updated to version 7.3 patchlevel 7.3.138

* Tue Jan 11 2011 Michael Perzl <michael@perzl.org> - 7.3.099-1
- updated to version 7.3 patchlevel 7.3.099

* Mon Dec 13 2010 Michael Perzl <michael@perzl.org> - 7.3.081-1
- updated to version 7.3 patchlevel 7.3.081

* Wed Nov 24 2010 Michael Perzl <michael@perzl.org> - 7.3.069-1
- updated to version 7.3 patchlevel 7.3.069

* Wed Sep 01 2010 Michael Perzl <michael@perzl.org> - 7.2.446-1
- updated to latest patchlevel 7.2.446

* Mon Jul 12 2010 Michael Perzl <michael@perzl.org> - 7.2.444-2
- removed dependency on gettext >= 0.17
- rebuilt with original AIX Linux Toolbox RPM files

* Tue Jun 29 2010 Michael Perzl <michael@perzl.org> - 7.2.444-1
- updated to latest patchlevel 7.2.444

* Thu May 20 2010 Michael Perzl <michael@perzl.org> - 7.2.436-1
- updated to latest patchlevel 7.2.436

* Thu Apr 01 2010 Michael Perzl <michael@perzl.org> - 7.2.411-1
- updated to latest patchlevel 7.2.411

* Mon Feb 22 2010 Michael Perzl <michael@perzl.org> - 7.2.368-1
- updated to latest patchlevel 7.2.368

* Thu Feb 11 2010 Michael Perzl <michael@perzl.org> - 7.2.356-1
- first version for AIX V5.1 and higher
