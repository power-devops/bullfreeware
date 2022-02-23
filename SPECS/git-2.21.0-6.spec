# Tests by default. No tests: rpm -ba --define 'dotests 0' git*.spec
%{!?dotests: %define dotests 1}

# Default compiler gcc
# To use xlc : --define 'gcc_compiler=0'
%{!?gcc_compiler:%define gcc_compiler 1}

# 64-bit version by default
%{!?default_bits: %define default_bits 64}

%{!?optimize:%define optimize 2}

%define _libdir64 %{_libdir}64

%define perl_version %(eval "`perl -V:version`"; echo $version)
# - Include prebuilt documentation - pbs xmlto/asciidoc & access to network URLs
%global use_prebuilt_docs   1

Name: 		git
Version: 	2.21.0
Release: 	6
Summary:  	Core git tools
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source0: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source2: 	%{name}.conf.httpd
Source3: 	gitweb.conf.in
Source4: 	https://www.kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.xz
Source5: 	https://www.kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.sign
Source6: 	https://www.kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.xz
Source7: 	https://www.kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.sign
Source8:	%{name}-%{version}-%{release}.build.log

Source9:	git-2.21.0-AR-L.patch
Source10:	git-2.21.0-SED-20190419.patch

Source99:	git-print-failed-test-output.sh

Patch1:		%{name}-2.21.0-mk-aix.patch
Patch2:		%{name}-2.21.0-aix.patch
Patch3:		%{name}-2.21.0-64-libexec-v2.patch
Patch4:		%{name}-2.21.0-32-bmaxdata.patch

# Merged
Patch5:		%{name}-2.21.0-Makefile-declare-FILENO_IS_A_MACRO-on-AIX-20190418.patch

# Patch6 not enough. Requires also: export TAR=...........
Patch6:		%{name}-2.21.0-TAR.patch

# Don't merged
Patch7:		%{name}-2.21.0-SIGCHLD-handler-v2.patch

# To merge
Patch8:     %{name}-2.21.0-Makefile-add-a-root-handler-for-access-on-AIX-v2.patch

Patch9:		%{name}-2.21.0-t9300-fast-import.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%if ! %{use_prebuilt_docs}
BuildRequires:	asciidoc >= 8.6.3
BuildRequires:	xmlto >= 0.0.24-1
%endif

BuildRequires:	coreutils
BuildRequires:	curl-devel >= 7.19.7-1
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	gettext
BuildRequires:	sed
#BuildRequires:	openssl >= 1.0.1-g
#BuildRequires:	openssl-devel >= 1.0.1-g
BuildRequires:	perl >= 5.8.8
BuildRequires:	zlib-devel >= 1.2.3

Requires:	bash
Requires:	curl >= 7.19.7-1
Requires:	expat >= 2.0.1
Requires:	gettext
Requires:	less
#Requires:	openssl >= 1.0.1-g
Requires:	perl >= 5.8.8
Requires:	python >= 2.6.2
Requires:	rsync
Requires:	zlib >= 1.2.3

# Needed for:
#   git difftool --tool=vimdiff
#   # git difftool
#   Viewing (1/1): .......
#   Launch 'vimdiff' [Y/n]? Y
Requires:	vim vim-enhanced


%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.


%package all
Summary:        Meta-package to pull in all git tools
Group:          Development/Tools
Requires:       git = %{version}-%{release}
Requires:       git-arch = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.


%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5.8.8
Requires:       tla

%description arch
Git tools for importing Arch repositories.


%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       cvs
Requires:       cvsps
Requires:       perl >= 5.8.8

%description cvs
Git tools for importing CVS repositories.


%package daemon
Summary:        Git protocol dæmon
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description daemon
The git daemon for supporting git:// access to git repositories


%package email
Summary:        Git tools for sending email
Group:          Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	perl >= 5.8.8
#Requires: 	perl-Net-SMTP-SSL
#Requires: 	perl-Authen-SASL
%description email
Git tools for sending email.


%package gui
Summary:        Git GUI tool
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
#Requires:       tcl >= 8.4
#Requires:       tk >= 8.4

%description gui
Git GUI tool.


%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5.8.8
Requires:       subversion
## Requires:     perl(Term::Readkey)

%description svn
Git tools for importing Subversion repositories.


%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
#Requires:       tk >= 8.4

%description -n gitk
Git revision tree visualiser.


%package -n gitweb
Summary:        Simple web interface to git repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       httpd
Requires:       perl >= 5.8.8

%description -n gitweb
Simple web interface to track changes in git repositories


%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
# this is contained in our base perl packag
# BuildRequires:  perl(ExtUtils::MakeMaker)
# this we don't have yet
# BuildRequires:  perl(Error)
Requires:       %{name} = %{version}-%{release}
#Requires:       perl(:MODULE_COMPAT_%(eval "`%{_bindir}/perl -V:version`"; echo $version))
Requires:       perl >= 5.8.8
#Requires:       perl(Error)

%description -n perl-Git
Perl interface to Git.


%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}
%{!?python_sitelib: %global python_sitelib %(%{_bindir}/python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "default_bits=%{default_bits}"
echo "optimize=%{optimize}"

# to use /opt/freeware/bin/tar
export PATH=/opt/freeware/bin:$PATH

%setup -q

%patch1
%patch5 -p1
%patch6
%patch7
%patch8 -p1

%if %{use_prebuilt_docs}
mkdir -p prebuilt_docs/html
mkdir -p prebuilt_docs/man
xz -dc %{SOURCE4} | tar xf - -C prebuilt_docs/html
xz -dc %{SOURCE6} | tar xf - -C prebuilt_docs/man
# Remove non-html files
find prebuilt_docs/html -type f ! -name '*.html' | xargs rm
find prebuilt_docs/html -type d | xargs rmdir --ignore-fail-on-non-empty
%endif

# Install print-failed-test-output script
install -p -m 755 %{SOURCE99} git-print-failed-test-output.sh

# Replace sh=ksh by bash inside all test files
# In addition to: SHELL_PATH=/usr/bin/bash
# Maybe can be speed up 
change_binsh_by_usrbinbash() {

  for f in `find .`
  do
    if [ -x $f ]
    then
	EXECUTABLE=1
    else
	EXECUTABLE=0
    fi
    if [ -f $f ]
    then
      ( (grep "#\! /bin/sh"    $f > /dev/null 2>&1 ; echo $? > /tmp/git-sh-$$) || true )
      RES=`cat /tmp/git-sh-$$`
      if [ $RES -eq 0 ]
      then
      	cat $f | sed "s|#! /bin/sh|#!/usr/bin/bash|" > /tmp/f$$
      	mv /tmp/f$$ $f
      fi
      ( (grep "#\!/usr/bin/sh" $f > /dev/null 2>&1 ; echo $? > /tmp/git-sh-$$) || true )
      RES=`cat /tmp/git-sh-$$`
      if [ $RES -eq 0 ]
      then
      	cat $f | sed "s|/usr/bin/sh|#!/usr/bin/bash|" > /tmp/f$$
      	mv /tmp/f$$ $f
      fi
      ( (grep "#\!/bin/sh"     $f > /dev/null 2>&1 ; echo $? > /tmp/git-sh-$$) || true )
      RES=`cat /tmp/git-sh-$$`
      if [ $RES -eq 0 ]
      then
      	cat $f | sed "s|#!/bin/sh|#!/usr/bin/bash|" > /tmp/f$$
      	mv /tmp/f$$ $f
      fi
      if [ EXECUTABLE -eq 1 ]
      then
        chmod +x $f
      fi
    fi
  done
  rm -f /tmp/f$$ /tmp/git-sh-$$
}
change_binsh_by_usrbinbash

# Must change back to /bin/sh for testing t9300-fast-import.sh
%patch9


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%patch2

cd 64bit
%patch3 -p0

cd ../32bit
%patch4 -p0


%build

env
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export SED="/opt/freeware/bin/sed"
export MAKE="/opt/freeware/bin/gmake --trace"

# to use /opt/freeware/bin/grep
export PATH=/opt/freeware/bin:$PATH

export GLOBAL_CC_OPTIONS=" -O%{optimize}"

# Choose XLC or GCC
%if %{gcc_compiler} == 1

# -R : see Makefile
#	CC_LD_DYNPATH = -L

export CC_LD_DYNPATH="-L"
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32 -D_LARGE_FILES"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc_r"
export CXX__="/usr/vacpp/bin/xlC_r"
#export CC="/usr/vac/bin/xlc_r"
#export XLCCPATH="/opt/IBM/xlc/13.1.3/bin"
#export  CC="$XLCCPATH/xlc_r"
export FLAG32="-q32  -D_LARGE_FILES"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

# Default:
#export export GLOBAL_CC_OPTIONS=-O2
export export GLOBAL_CC_OPTIONS=-O0
export CC32=" ${CC__}  ${FLAG32} ${GLOBAL_CC_OPTIONS}"
export CXX32="${CXX__} ${FLAG32} ${GLOBAL_CC_OPTIONS}"
export CC64=" ${CC__}  ${FLAG64} ${GLOBAL_CC_OPTIONS}"
export CXX64="${CXX__} ${FLAG64} ${GLOBAL_CC_OPTIONS}"


build_git() {
   set -x

# Not enough...
# Stupid "trash directory" is hard-coded in several files...
#export TEST_DIRECTORY=trash_directory

# Required for test t5000-tar-tree.sh 
#   config.mak.autogen:TAR = ....../bin/tar
export TAR=/opt/freeware/bin/tar

# Required for testing
export   SHELL_PATH=/usr/bin/bash
export        SHELL=/usr/bin/bash
export CONFIG_SHELL=/usr/bin/bash

chmod +x ./configure
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --libdir=$1 \
    --with-perl=%{_prefix}/bin/perl \
    --with-openssl=%{_prefix}

# En désespoir de cause...
patch -p1 < %{SOURCE9}
patch -p1 < %{SOURCE10}

$MAKE --trace --print-directory \
       %{?_smp_mflags} \
       %{path_settings} \
       NO_REGEX=NeedsStartEnd	-j8


# No doc !
#$MAKE --trace --print-directory \
#       %{?_smp_mflags} \
#       %{path_settings} \
#       doc

if [ "%{dotests}" == 1 ]
then
# Required for testing
export   SHELL_PATH=/usr/bin/bash
export        SHELL=/usr/bin/bash
export CONFIG_SHELL=/usr/bin/bash

      ($MAKE %{?_smp_mflags} \
          %{path_settings} \
          NO_REGEX=NeedsStartEnd \
          -i test || true)

pwd
#./git-print-failed-test-output.sh

# Run contrib/credential/netrc tests
#mkdir -p contrib/credential
#mv netrc contrib/credential/
(gmake -C contrib/credential/netrc/ test || \
 gmake -C contrib/credential/netrc/ testverbose || \
 true)

fi
}


#Build on 64bit mode
cd 64bit
export OBJECT_MODE=64

export CC="${CC64}"
export CXX="${CXX64}"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

#$MAKE %{?_smp_mflags} \
#      %{path_settings} \
#       NO_REGEX=NeedsStartEnd
#export CFLAGS="-O2 -maix64"
#PATH=/opt/freeware/bin:$PATH CFLAGS="$CFLAGS" gmake %{?_smp_mflags} NO_REGEX=NeedsStartEnd
#if [ "%{dotests}" == 1 ]
#then
#    (make -i test NO_REGEX=NeedsStartEnd ||true)
#fi

build_git \
    %{_libdir64}
cd ..


#Build on 32bit mode
cd 32bit
export OBJECT_MODE=32

export CC="${CC32}"
export CXX="${CXX32}"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x8000000"

build_git \
    %{_libdir}
cd ..


%install
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace"
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#Install on 64bit mode
cd 64bit
export OBJECT_MODE=64
LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib" \
$MAKE install DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor NO_REGEX=NeedsStartEnd

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
	/usr/bin/strip "$fic"_64 || :
    done
    cd  ${RPM_BUILD_ROOT}/%{_libexecdir}/git-core
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
	/usr/bin/strip "$fic"_64 || :
    done
)

mkdir -p ${RPM_BUILD_ROOT}/var/lib64/git
#sed "s|@PROJECTROOT@|/var/lib64/git|g" \
#    %{SOURCE3} > ${RPM_BUILD_ROOT}%{_sysconfdir}/gitweb.conf

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64/perl5/%{perl_version}

mv ${RPM_BUILD_ROOT}%{_prefix}/share/perl5/FromCPAN/Error.pm ${RPM_BUILD_ROOT}%{_libdir}64/perl5/%{perl_version}
mv ${RPM_BUILD_ROOT}%{_prefix}/share/perl5/Git               ${RPM_BUILD_ROOT}%{_libdir}64/perl5/%{perl_version}

#Install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
LIBPATH="/opt/freeware/lib:/usr/lib" \
$MAKE install DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor NO_REGEX=NeedsStartEnd

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	/usr/bin/strip "$fic"_32 || :
	ln -sf "$fic"_64 $fic
    done
    cd  ${RPM_BUILD_ROOT}/%{_libexecdir}/git-core
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	/usr/bin/strip "$fic"_32 || :
	ln -sf "$fic"_64 $fic
    done
)


%if ! %{use_prebuilt_docs}
$MAKE install-doc DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor
%else
mkdir -p %{buildroot}%{_mandir}
cp -a prebuilt_docs/man/* %{buildroot}%{_mandir}
cp -a prebuilt_docs/html/* Documentation/
%endif


mkdir -p ${RPM_BUILD_ROOT}/var/www/git
cp ${RPM_BUILD_ROOT}%{_datadir}/gitweb/gitweb.cgi ${RPM_BUILD_ROOT}/var/www/git
cp ${RPM_BUILD_ROOT}%{_datadir}/gitweb/static/* ${RPM_BUILD_ROOT}/var/www/git

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d/git.conf

mkdir -p ${RPM_BUILD_ROOT}/var/lib/git
sed "s|@PROJECTROOT@|/var/lib/git|g" \
    %{SOURCE3} > ${RPM_BUILD_ROOT}%{_sysconfdir}/gitweb.conf

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3

mv ${RPM_BUILD_ROOT}%{_prefix}/share/perl5/FromCPAN/Error.pm ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version}
mv ${RPM_BUILD_ROOT}%{_prefix}/share/perl5/Git               ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version}

mv ${RPM_BUILD_ROOT}%{_prefix}/share/perl5/Git*              ${RPM_BUILD_ROOT}%{_mandir}/man3


find ${RPM_BUILD_ROOT} -type f -name .packlist     -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name '*.bs'        -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -exec rm -f {} ';'

(find ${RPM_BUILD_ROOT}%{_bindir}     -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >  bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_libexecdir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_libexecdir} -type l | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files

(find ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version} -type f | sed -e s@^${RPM_BUILD_ROOT}@@) > perl-files

(find ${RPM_BUILD_ROOT}%{_mandir}     -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool|git-daemon|Git" | sed -e s@^${RPM_BUILD_ROOT}@@ -e 's/$/*/' ) >> bin-man-doc-files

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

(find ${RPM_BUILD_ROOT}/usr/bin -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files
(find ${RPM_BUILD_ROOT}/usr/bin -type l | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f 32bit/bin-man-doc-files
%defattr(-,root,system)
%doc 32bit/README.md 32bit/COPYING 32bit/contrib/
%doc 32bit/Documentation/RelNotes
%doc 32bit/Documentation/howto 32bit/Documentation/technical
%doc 32bit/Documentation/*.txt 32bit/Documentation/*.html
%{_datadir}/git-core/
%dir %{_libexecdir}/git-core/
%{_bindir}/git
%{_bindir}/git-receive-pack
%{_bindir}/git-shell
%{_bindir}/git-upload-archive
%{_bindir}/git-upload-pack
/usr/bin/git-receive-pack*
/usr/bin/git-shell*
/usr/bin/git-upload-archive*
/usr/bin/git-upload-pack*
/usr/bin/git
/usr/bin/git_32
/usr/bin/git_64
#%{_sysconfdir}/bash_completion.d


%files arch
%defattr(-,root,system)
%doc 32bit/Documentation/git-archimport.txt
%doc 32bit/Documentation/git-archimport.html
%{_libexecdir}/git-core/git-archimport


%files cvs
%defattr(-,root,system)
%doc 32bit/Documentation/*git-cvs*.txt
%doc 32bit/Documentation/*git-cvs*.html
%{_mandir}/man1/*cvs*.1*
%{_bindir}/*cvsserver*
%{_libexecdir}/git-core/*cvs*
/usr/bin/*cvsserver*


%files daemon
%defattr(-,root,system)
%doc 32bit/Documentation/*daemon*.txt
%doc 32bit/Documentation/*daemon*.html
%{_mandir}/man1/*daemon*.1*
%{_libexecdir}/git-core/*daemon*
/var/lib/git
/var/lib64/git
# %if %{use_systemd}
# %{_unitdir}/git.socket
# %{_unitdir}/git@.service
# %else
# %config(noreplace)%{_sysconfdir}/xinetd.d/git
# %endif


%files email
%defattr(-,root,system)
%doc 32bit/Documentation/*email*.txt
%doc 32bit/Documentation/*email*.html
%{_mandir}/man1/*email*.1*
%{_libexecdir}/git-core/*email*


%files gui
%defattr(-,root,system)
%doc 32bit/Documentation/git-gui.txt
%doc 32bit/Documentation/git-gui.html
%doc 32bit/Documentation/git-citool.txt
%doc 32bit/Documentation/git-citool.html
%{_mandir}/man1/git-gui.1*
%{_mandir}/man1/git-citool.1*
%{_libexecdir}/git-core/git-gui*
%{_libexecdir}/git-core/git-citool
#%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui


%files -n gitk
%defattr(-,root,system)
%doc 32bit/Documentation/*gitk*.txt
%doc 32bit/Documentation/*gitk*.html
%{_mandir}/man1/*gitk*.1*
%{_bindir}/*gitk*
%{_datadir}/gitk
/usr/bin/*gitk*


%files -n gitweb
%defattr(-,root,system)
%doc 32bit/gitweb/INSTALL 32bit/gitweb/README
#%doc 32bit/Documentation/*.gitweb
%doc 32bit/Documentation/gitweb*.txt
%doc 32bit/Documentation/gitweb*.html
%{_mandir}/man1/*gitweb*.1*
%{_mandir}/man5/*gitweb*.5*
%{_datadir}/gitweb
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
/var/www/git/

%files -n perl-Git -f 32bit/perl-files
%defattr(-,root,system)
#%exclude %{_mandir}/man3/*Git*SVN*.3pm*
#%{_mandir}/man3/*Git*.3pm*
%{_mandir}/man3/*Git*
#%{_libdir}/perl5/%{perl_version}/*
%{_libdir64}/perl5/%{perl_version}/*

%files svn
%defattr(-,root,system)
%doc 32bit/Documentation/*svn*.txt
%doc 32bit/Documentation/*svn*.html
%{_mandir}/man1/*svn*.1*
%{_libexecdir}/git-core/*svn*
#%{_libexecdir}64/git-core/*svn*

%files all
# No files for you!


%changelog
* Wed Apr 24 2019 Clément Chigot <clement.chigot@atos.net> - 2.21.0-6
- Correct previous fix to work correctly under a user too

* Fri Apr 19 2019 Clément Chigot <clement.chigot@atos.net> - 2.21.0-5
- Fix hooks failures when git is launched under root

* Tue Mar 26 2019 Tony Reix <tony.reix@atos.net> - 2.21.0-4
- find ... -type f OR l . Not both !

* Wed Mar 20 2019 Tony Reix <tony.reix@atos.net> - 2.21.0-3
- Fix missing symlinks

* Fri Mar 15 2019 Tony Reix <tony.reix@atos.net> - 2.21.0-2
- Fix issue with t9300-fast-import.patch : file6_data='#!bin/sh   !!!!!
- Use GCC again

* Wed Feb 27 2019 Tony Reix <tony.reix@atos.net> - 2.21.0-1
- Updated to version 2.21.0

* Wed Aug 22 2018 Tony Reix <tony.reix@atos.net> - 2.15.1-2
- Fix git-remote-https missing and some other issues

* Fri Jan 12 2018 Daniele Silvestre <daniele.silvestre@atos.net> - 2.15.1-1
- Updated to version 2.15.1
- Add gcc - and gcc is the default compiler -
- Add 64 bits - and both 32 and 64 bit binaries are delivered, 64 bit is the default for command
- Adapt .spec to git.spec delivered with the sources 

* Tue May 10 2016 Michael Wilson <michael.wilson@bull.net> 2.8.2-1
- Updated to version 2.8.2

* Mon May 19 2014 Gerard Visiedo <gerard.visiedo@bull.net> 1.8.3.1-3
- Re-Build with openssl.10.0.1-g due to symbole lost into new library libcrypto.so.1.0.1

* Thu Jul 18 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.8.3.1-2
- Build on Aix6.1

* Mon Jun 24 2013 Michael Perzl <michael@perzl.org> - 1.8.3.1-1
- updated to version 1.8.3.1

* Wed May 29 2013 Michael Perzl <michael@perzl.org> - 1.8.3-1
- updated to version 1.8.3

* Wed May 29 2013 Michael Perzl <michael@perzl.org> - 1.8.2.3-1
- updated to version 1.8.2.3

* Wed Mar 20 2013 Michael Perzl <michael@perzl.org> - 1.8.2-1
- updated to version 1.8.2

* Wed Mar 20 2013 Michael Perzl <michael@perzl.org> - 1.8.1.5-1
- updated to version 1.8.1.5

* Wed Feb 20 2013 Michael Perzl <michael@perzl.org> - 1.8.1.4-1
- updated to version 1.8.1.4

* Thu Jan 17 2013 Michael Perzl <michael@perzl.org> - 1.8.1.1-1
- updated to version 1.8.1.1

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.8.1-1
- updated to version 1.8.1

* Tue Jan 08 2013 Michael Perzl <michael@perzl.org> - 1.8.0.3-1
- updated to version 1.8.0.3

* Mon Dec 17 2012 Michael Perzl <michael@perzl.org> - 1.8.0.2-1
- updated to version 1.8.0.2

* Wed Dec 05 2012 Michael Perzl <michael@perzl.org> - 1.8.0.1-1
- updated to version 1.8.0.1

* Thu Oct 25 2012 Michael Perzl <michael@perzl.org> - 1.8.0-1
- updated to version 1.8.0

* Thu Oct 25 2012 Michael Perzl <michael@perzl.org> - 1.7.12.4-1
- updated to version 1.7.12.4

* Tue Oct 09 2012 Michael Perzl <michael@perzl.org> - 1.7.12.3-1
- updated to version 1.7.12.3

* Tue Oct 09 2012 Michael Perzl <michael@perzl.org> - 1.7.11.7-1
- updated to version 1.7.11.7

* Thu Aug 09 2012 Michael Perzl <michael@perzl.org> - 1.7.11.4-1
- updated to version 1.7.11.4

* Fri Jul 27 2012 Michael Perzl <michael@perzl.org> - 1.7.11.3-1
- updated to version 1.7.11.3

* Wed Jul 18 2012 Michael Perzl <michael@perzl.org> - 1.7.11.2-1
- updated to version 1.7.11.2

* Fri Jun 22 2012 Michael Perzl <michael@perzl.org> - 1.7.11.1-1
- updated to version 1.7.11.1

* Tue Jun 19 2012 Michael Perzl <michael@perzl.org> - 1.7.11-1
- updated to version 1.7.11

* Tue Jun 19 2012 Michael Perzl <michael@perzl.org> - 1.7.10.5-1
- updated to version 1.7.10.5

* Mon Jun 04 2012 Michael Perzl <michael@perzl.org> - 1.7.10.4-1
- updated to version 1.7.10.4

* Mon Jun 04 2012 Michael Perzl <michael@perzl.org> - 1.7.10.2-2
- rebuilt against correct version of openssl

* Tue May 15 2012 Michael Perzl <michael@perzl.org> - 1.7.10.2-1
- updated to version 1.7.10.2

* Thu May 03 2012 Michael Perzl <michael@perzl.org> - 1.7.10.1-1
- updated to version 1.7.10.1

* Sun Apr 15 2012 Michael Perzl <michael@perzl.org> - 1.7.10-1
- updated to version 1.7.10

* Mon Apr 02 2012 Michael Perzl <michael@perzl.org> - 1.7.9.5-1
- updated to version 1.7.9.5

* Tue Mar 13 2012 Michael Perzl <michael@perzl.org> - 1.7.9.4-1
- updated to version 1.7.9.4

* Mon Mar 05 2012 Michael Perzl <michael@perzl.org> - 1.7.9.2-1
- updated to version 1.7.9.2

* Fri Feb 17 2012 Michael Perzl <michael@perzl.org> - 1.7.9.1-1
- updated to version 1.7.9.1

* Wed Feb 08 2012 Michael Perzl <michael@perzl.org> - 1.7.9-2
- fixed compile against wrong openssl version

* Tue Jan 31 2012 Michael Perzl <michael@perzl.org> - 1.7.9-1
- updated to version 1.7.9

* Tue Jan 31 2012 Michael Perzl <michael@perzl.org> - 1.7.8.4-1
- updated to version 1.7.8.4

* Thu Jan 05 2012 Michael Perzl <michael@perzl.org> - 1.7.8.2-1
- updated to version 1.7.8.2

* Fri Dec 23 2011 Michael Perzl <michael@perzl.org> - 1.7.8.1-1
- updated to version 1.7.8.1

* Thu Dec 15 2011 Michael Perzl <michael@perzl.org> - 1.7.8-1
- updated to version 1.7.8

* Thu Dec 15 2011 Michael Perzl <michael@perzl.org> - 1.7.7.4-1
- updated to version 1.7.7.4

* Thu Nov 17 2011 Michael Perzl <michael@perzl.org> - 1.7.7.3-1
- updated to version 1.7.7.3
- added man pages
- added 'git-daemon' package

* Thu Nov 03 2011 Michael Perzl <michael@perzl.org> - 1.7.7.2-1
- updated to version 1.7.7.2

* Tue Sep 27 2011 Michael Perzl <michael@perzl.org> - 1.7.6.4-1
- updated to version 1.7.6.4

* Wed Sep 07 2011 Michael Perzl <michael@perzl.org> - 1.7.6.1-1
- updated to version 1.7.6.1

* Mon Jul 25 2011 Michael Perzl <michael@perzl.org> - 1.7.6-2
- fixed a spec file typo

* Fri Jul 01 2011 Michael Perzl <michael@perzl.org> - 1.7.6-1
- updated to version 1.7.6

* Mon Jun 13 2011 Michael Perzl <michael@perzl.org> - 1.7.5.4-1
- updated to version 1.7.5.4

* Mon May 23 2011 Michael Perzl <michael@perzl.org> - 1.7.5.2-1
- updated to version 1.7.5.2

* Thu May 05 2011 Michael Perzl <michael@perzl.org> - 1.7.5.1-1
- updated to version 1.7.5.1

* Tue Apr 26 2011 Michael Perzl <michael@perzl.org> - 1.7.5-1
- updated to version 1.7.5

* Tue Apr 26 2011 Michael Perzl <michael@perzl.org> - 1.7.4.5-1
- updated to version 1.7.4.5

* Wed Apr 13 2011 Michael Perzl <michael@perzl.org> - 1.7.4.4-1
- updated to version 1.7.4.4

* Fri Apr 01 2011 Michael Perzl <michael@perzl.org> - 1.7.4.2-1
- updated to version 1.7.4.2

* Tue Mar 22 2011 Michael Perzl <michael@perzl.org> - 1.7.4.1-1
- updated to version 1.7.4.1

* Fri Feb 18 2011 Michael Perzl <michael@perzl.org> - 1.7.4-2
- fixed configure script for XLC so no profiling version is compiled

* Thu Feb 03 2011 Michael Perzl <michael@perzl.org> - 1.7.4-1
- updated to version 1.7.4

* Tue Jan 11 2011 Michael Perzl <michael@perzl.org> - 1.7.3.5-1
- updated to version 1.7.3.5

* Tue Dec 21 2010 Michael Perzl <michael@perzl.org> - 1.7.3.4-1
- updated to version 1.7.3.4

* Mon Dec 06 2010 Michael Perzl <michael@perzl.org> - 1.7.3.3-1
- updated to version 1.7.3.3

* Mon Oct 25 2010 Michael Perzl <michael@perzl.org> - 1.7.3.2-1
- updated to version 1.7.3.2

* Thu Oct 07 2010 Michael Perzl <michael@perzl.org> - 1.7.3.1-1
- updated to version 1.7.3.1

* Thu Oct 07 2010 Michael Perzl <michael@perzl.org> - 1.7.2.3-1
- updated to version 1.7.2.3

* Thu Aug 26 2010 Michael Perzl <michael@perzl.org> - 1.7.2.2-1
- updated to version 1.7.2.2

* Fri Jul 30 2010 Michael Perzl <michael@perzl.org> - 1.7.2.1-1
- updated to version 1.7.2.1

* Fri Jul 23 2010 Michael Perzl <michael@perzl.org> - 1.7.1.1-1
- updated to version 1.7.1.1

* Fri Jul 23 2010 Michael Perzl <michael@perzl.org> - 1.7.0.6-1
- updated to version 1.7.0.6

* Fri Jul 23 2010 Michael Perzl <michael@perzl.org> - 1.6.6.2-1
- updated to version 1.6.6.2

* Fri Jul 23 2010 Michael Perzl <michael@perzl.org> - 1.6.0.6-1
- updated to version 1.6.0.6

* Thu Nov 05 2009 Michael Perzl <michael@perzl.org> - 1.6.0.1-1
- first version for AIX V5.1 and higher
