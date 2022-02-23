# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without dotests

# 64-bit version by default
%define default_bits 64

%define _libdir64 %{_libdir}64

%define path_settings prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version}

# For Perl-Git
%define perl  %{_bindir}/perl_32
%define perl_version  %(eval "`%{perl} -V:version`" ; echo $version | sed "s|\.[0-9]*$||")
%define perl_vendorlib %(eval "`%{perl} -V:installvendorlib`"; echo $installvendorlib)

# - Include prebuilt documentation - pbs xmlto/asciidoc & access to network URLs
%global use_prebuilt_docs   1

Name: 		git
Version: 	2.22.0
Release: 	2
Summary:  	Core git tools
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source0: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source2: 	gitweb-httpd.conf
Source3: 	gitweb.conf.in
Source4: 	https://www.kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.xz
Source5: 	https://www.kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.sign
Source6: 	https://www.kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.xz
Source7: 	https://www.kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.sign
Source8:	%{name}-%{version}-%{release}.build.log

Source99:	git-print-failed-test-output.sh

# Patch1:		%{name}-2.22.0-Makefile-aix.patch
Patch2:		%{name}-2.22.0-Makefile-aix-64bit.patch
Patch3:		%{name}-2.22.0-64bit-libexec.patch
Patch4:		%{name}-2.22.0-Makefile-aix-32bit.patch
Patch5:		%{name}-2.22.0-config-SHELL-and-AR.patch

# Patch6 not enough. Requires also: export TAR=...........
Patch6:		%{name}-2.21.0-TAR.patch

# Don't merged
Patch7:		%{name}-2.21.0-SIGCHLD-handler-v2.patch

# Remove requirement on /usr/bin/python
Patch8:     %{name}-2.22.0-fix-svnrdump_sim-py-script-shebang.patch


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
BuildRequires:	perl >= 5.30.0
BuildRequires:	zlib-devel >= 1.2.3
BuildRequires:  curl-devel

Requires:   git-core = %{version}-%{release}
Requires:   git-core-doc = %{version}-%{release}
Requires:	bash
Requires:	expat >= 2.0.1
Requires:	gettext
Requires:	less
#Requires:	openssl >= 1.0.1-g
# Perl with correct path
Requires:	perl >= 5.30.0
Requires:	python >= 2.6.2

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
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       git-subtree = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-instaweb = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.


%package core
Summary:        Core package of git with minimal functionality
Requires:       less
Requires:	    zlib >= 1.2.3
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%package core-doc
Summary:        Documentation files for git-core
BuildArch:      noarch
Requires:       git-core = %{version}-%{release}
%description core-doc
Documentation files for git-core package including man pages.


%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       cvs
Requires:       cvsps
Requires:       perl >= 5.30.0
Requires:       perl(DBD::SQLite)

%description cvs
Git tools for importing CVS repositories.


%package daemon
Summary:        Git protocol daemon
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


%package instaweb
Summary:        Repository browser in gitweb
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}
Requires:       lighttpd

%description instaweb
A simple script to set up gitweb and a web server for browsing the local
repository.

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
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5.30.0
%description -n perl-Git
Perl interface to Git.




%prep
# to use /opt/freeware/bin/tar
export PATH=/opt/freeware/bin:$PATH

%setup -q

# %patch1
%patch5
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

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
prefix = %{_prefix}
mandir = %{_mandir}
CC_LD_DYNPATH = "-L"
ETC_GITCONFIG = %{_sysconfdir}/gitconfig

# gitweb
GITWEB_PROJECTROOT = %{_localstatedir}/lib/git
gitwebdir = %{_localstatedir}/www/git

# Perl
perllibdir = %{perl_vendorlib}


EOF
# Print config.mak to aid confirmation/verification of settings
cat config.mak


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


cd 64bit
%patch2 -p2
%patch3 -p2

cd ../32bit
%patch4 -p2


%build

export NM="/usr/bin/nm -X32_64"
export SED="/opt/freeware/bin/sed"
export MAKE="/opt/freeware/bin/gmake --trace"

# to use /opt/freeware/bin/grep
export PATH=/opt/freeware/bin:$PATH

export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

# Default:
export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"


build_git() {
	set -x

	# Export for Makefile
	export AR="/usr/bin/ar -X32_64"
	export NM="/usr/bin/nm -X32_64"
	export TAR=/opt/freeware/bin/tar

	chmod +x ./configure
	./configure \
		--libdir=$1 \
		--with-perl=%{_prefix}/bin/perl \
		--with-openssl=%{_prefix}


	$MAKE --print-directory \
		  %{path_settings} \
		  NO_REGEX=NeedsStartEnd	-j8


	# No doc !
	#$MAKE --trace --print-directory \
		#       %{path_settings} \
		#       doc

	# Make man for perl Modules
	# It's not provided by git-manpages tar
	$MAKE  --print-directory \
		   man-perl



}


#Build on 64bit mode
cd 64bit
export OBJECT_MODE=64

export CC="${CC64}"
export CXX="${CXX64}"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64  -Wl,-blibpath:$LIBPATH"

build_git \
    %{_libdir64}
cd ..


#Build on 32bit mode
cd 32bit
export OBJECT_MODE=32

export CC="${CC32}"
export CXX="${CXX32}"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:$LIBPATH -Wl,-bmaxdata:0x8000000"

build_git \
    %{_libdir}
cd ..

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export MAKE="/opt/freeware/bin/gmake --trace"

make_tests(){
	($MAKE %{path_settings} \
		   NO_REGEX=NeedsStartEnd \
		   -i test ||  ./print-failed-test-output )

	pwd
	(gmake -C contrib/credential/netrc/ test || \
		 gmake -C contrib/credential/netrc/ testverbose || \
		 true)

}

cd 64bit
make_tests

cd ../32bit
make_tests


%install
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace"
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Install on 64bit mode
cd 64bit
export OBJECT_MODE=64
LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib" \
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


#Install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
LIBPATH="/opt/freeware/lib:/usr/lib:/lib" \
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
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}
cp -a prebuilt_docs/man/* ${RPM_BUILD_ROOT}%{_mandir}
cp -a prebuilt_docs/html/* Documentation/
%endif

# Install man of perl Modules
$MAKE install-man-perl DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor


mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d/git.conf
sed -e "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
    %{SOURCE3} > ${RPM_BUILD_ROOT}%{_sysconfdir}/gitweb.conf


mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/git

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3

find ${RPM_BUILD_ROOT} -type f -name .packlist     -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name '*.bs'        -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -exec rm -f {} ';'

exclude_re="archimport|email|git-(citool|cvs|daemon|gui|instaweb|p4|subtree|svn)|gitk|gitweb|p4merge"

(find ${RPM_BUILD_ROOT}%{_bindir} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) > bin-man-doc-files
cat bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_bindir} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e "s@^${RPM_BUILD_ROOT}@%dir @") >> bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_libexecdir} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_libexecdir} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e "s@^${RPM_BUILD_ROOT}@%dir @") >> bin-man-doc-files

(find ${RPM_BUILD_ROOT}%{perl_vendorlib} -type f | sed -e s@^${RPM_BUILD_ROOT}@@) > perl-git-files
(find ${RPM_BUILD_ROOT}%{perl_vendorlib} -mindepth 1 -type d | sed -e "s@^${RPM_BUILD_ROOT}@%dir @") >> perl-git-files

(find ${RPM_BUILD_ROOT}%{_mandir}     -type f | grep -vE "$exclude_re|Git" | sed -e s@^${RPM_BUILD_ROOT}@@ -e 's/$/*/' ) >> bin-man-doc-files

# Setup bash completion
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/bash-completion/
install -Dpm 644 contrib/completion/git-completion.bash ${RPM_BUILD_ROOT}%{_prefix}/share/bash-completion/git

# Install git-prompt.sh
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
		${RPM_BUILD_ROOT}%{_datadir}/git-core/contrib/completion/


# Install contrib/hooks
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/git-core/contrib
cp -r contrib/hooks ${RPM_BUILD_ROOT}%{_datadir}/git-core/contrib

# Create /usr/bin links
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
cd ${RPM_BUILD_ROOT}/usr/bin
ln -sf ../..%{_bindir}/* .
cd -

(find ${RPM_BUILD_ROOT}/usr/bin -type f | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files
(find ${RPM_BUILD_ROOT}/usr/bin -type l | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files

# Split core files
not_core_re="git-(add--interactive|contacts|credential-(libsecret|netrc)|difftool|filter-branch|instaweb|request-pull|send-mail)|gitweb"
grep -vE "$not_core_re|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
grep -vE "$not_core_re" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core
grep -E  "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files -f 32bit/bin-man-doc-git-files
%{_datadir}/git-core/contrib/hooks/multimail
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample



%files core -f 32bit/bin-files-core
%defattr(-,root,system)
# exclude is best way here because of troubles with symlinks inside git-core/
%exclude %{_datadir}/git-core/contrib/hooks/multimail
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%{_datadir}/git-core/

%files core-doc -f 32bit/man-doc-files-core
%doc 32bit/README.md 32bit/COPYING 32bit/contrib/
%doc 32bit/Documentation/RelNotes
%doc 32bit/Documentation/howto 32bit/Documentation/technical
%doc 32bit/Documentation/*.txt 32bit/Documentation/*.html

%files cvs
%defattr(-,root,system)
%doc 32bit/Documentation/*git-cvs*.txt
%doc 32bit/Documentation/*git-cvs*.html
%{_mandir}/man1/*cvs*.1*
%{_bindir}/git-cvsserver*
%{_libexecdir}/git-core/*cvs*
/usr/bin/*cvsserver*

%files daemon
%defattr(-,root,system)
%doc 32bit/Documentation/*daemon*.txt
%doc 32bit/Documentation/*daemon*.html
%{_mandir}/man1/*daemon*.1*
%{_libexecdir}/git-core/*daemon*
%{_localstatedir}/lib/git

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
%doc 32bit/Documentation/gitweb*.txt
%doc 32bit/Documentation/gitweb*.html
%{_mandir}/man1/*gitweb*.1*
%{_mandir}/man5/*gitweb*.5*
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
%{_localstatedir}/www/git/

%files instaweb
%defattr(-,root,root)
%{_libexecdir}/git-core/git-instaweb*
%{_mandir}/man1/git-instaweb.1*
%doc 32bit/Documentation/git-instaweb.txt
%doc 32bit/Documentation/git-instaweb.html

%files -n perl-Git -f 32bit/perl-git-files
%defattr(-,root,system)
%{_mandir}/man3/*Git*.3pm*

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
* Tue Sep 17 2019 Clément Chigot <clement.chigot@atos.net> - 2.22.0-2
- Remove /usr/bin/python requirement

* Thu Jun 20 2019 Clément Chigot <clement.chigot@atos.net> - 2.22.0-1
- Updated to version 2.22.0
- Clean up spec file and move to RPM v4
- Remove requirements of curl, rsync
- Install git-completion.bash correctly
- Correctly install perl-git in perl_vendorlib
- Correctly install gitweb with its correct name

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
