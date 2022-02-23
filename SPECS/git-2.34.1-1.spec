# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without dotests

# CVS haven't been updated for a long time.
# By default, don't built its support.
%bcond_with cvs

%define _libdir64 %{_libdir}64

# %%define path_settings prefix=%%{_prefix} mandir=%%{_mandir} htmldir=%%{_docdir}/%%{name}-%%{version}

# - Include prebuilt documentation - pbs xmlto/asciidoc & access to network URLs
%global use_prebuilt_docs   1


Name: 		git
Version: 2.34.1
Release: 1
Summary:  	Core git tools
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://mirrors.edge.kernel.org/pub/software/scm/git/
Source0: 	http://mirrors.edge.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.xz
Source2: 	gitweb-httpd.conf
Source3: 	gitweb.conf.in
Source4: 	https://mirrors.edge.kernel.org/pub/software/scm/git/%{name}-htmldocs-%{version}.tar.xz
Source6: 	https://mirrors.edge.kernel.org/pub/software/scm/git/%{name}-manpages-%{version}.tar.xz
Source8:	%{name}-%{version}-%{release}.build.log

Source99:	git-print-failed-test-output.sh

Patch5:		%{name}-2.25.0-config-SHELL-and-AR-v3.patch

# Don't merged
Patch7:		%{name}-2.31.1-SIGCHLD-handler-v2.patch

%if ! %{use_prebuilt_docs}
BuildRequires:	asciidoc >= 8.6.3
BuildRequires:	xmlto >= 0.0.24-1
%endif

BuildRequires:	coreutils
BuildRequires:	curl-devel >= 7.73
BuildRequires:	expat-devel >= 2.2.10
BuildRequires:	gettext-devel => 0.20
BuildRequires:	sed
BuildRequires:	perl(perl) >= 5.30.0
BuildRequires:	zlib-devel >= 1.2.11-3
BuildRequires:	grep

Requires:   git-core = %{version}-%{release}
Requires:   git-core-doc = %{version}-%{release}
Requires:   bash
Requires:   expat >= 2.0.1
Requires:   gettext >= 0.20
Requires:   less
# Perl with correct path
Requires:   perl(perl) >= 5.30.0
Requires:   python3 >= 3.8

Requires:   vim vim-enhanced


%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.


%package all
Summary:        Meta-package to pull in all git tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with cvs}
Requires:       git-cvs = %{version}-%{release}
%endif
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
Requires:	zlib >= 1.2.11-3
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


%if %{with cvs}
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

%endif

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
Requires:	perl(perl) >= 5.30.0
#Requires: 	perl-Net-SMTP-SSL
#Requires: 	perl-Authen-SASL
%description email
Git tools for sending email.


%package gui
Summary:        Git GUI tool
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

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
Requires:       perl(perl) >= 5.30.0
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
Requires:       perl(perl) >= 5.30.0

%description -n gitweb
Simple web interface to track changes in git repositories


%package -n perl%{perl_version}-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       %perl_compat

%description -n perl%{perl_version}-Git
Perl interface to Git.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       perl%{perl_version}-Git = %{version}-%{release}
Requires:       perl(perl) >= 5.30.0

%description -n perl-Git
Perl interface to Git.

%package subtree
Summary:        Git tools to merge and split repositories
Requires:       git-core = %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.


%prep
# to use /opt/freeware/bin/tar
export PATH=/opt/freeware/bin:$PATH

%setup -q

%patch5 -p1
%patch7

# AIX sed doesn't have the -i flag
export SED=/opt/freeware/bin/sed

# Change "/usr/bin/perl" to "/usr/bin/env perl" in contrib scripts's shebangs.
for f in `find contrib -type f`; do
	$SED -i "s|#!/usr/bin/perl|#!/usr/bin/env perl|g" $f
done

# git-remove-mediawiki.perl have a space in its shebang.
f=contrib/mw-to-git/git-remote-mediawiki.perl
$SED -i "s|#! /usr/bin/perl|#! /usr/bin/env perl|g" $f

# hooks--fsmonitor-watchman.sample is another problematic shell under /template
f=templates/hooks--fsmonitor-watchman.sample
$SED -i "s|#!/usr/bin/perl|#!/usr/bin/env perl|g" $f


%if %{use_prebuilt_docs}
mkdir -p prebuilt_docs/html
mkdir -p prebuilt_docs/man
xz -dc %{SOURCE4} | tar xf - -C prebuilt_docs/html
xz -dc %{SOURCE6} | tar xf - -C prebuilt_docs/man
# Remove non-html files
find prebuilt_docs/html -type f ! -name '*.html' | xargs rm
find prebuilt_docs/html -type d | xargs rmdir --ignore-fail-on-non-empty
%endif

%if %{without cvs}
# Remove git-cvs* from command list
sed -i '/^git-cvs/d' command-list.txt
%endif

# Move docs to Documentation
mv contrib/subtree/git-*.txt Documentation/

# Install print-failed-test-output script
install -p -m 755 %{SOURCE99} git-print-failed-test-output.sh

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
prefix = %{_prefix}
mandir = %{_mandir}
CC_LD_DYNPATH = "-L"
ETC_GITCONFIG = %{_sysconfdir}/gitconfig

PERL_PATH = %{__perl}
PYTHON_PATH = %{_bindir}/python3
SHELL_PATH = %{_bindir}/bash

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
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build

export NM="/usr/bin/nm -X32_64"
export SED="/opt/freeware/bin/sed"

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

# Needed both for 32 and 64 bit
export CFLAGS="-mcmodel=large"

build_git() {
	set -x

	# Export for Makefile
	export AR="/usr/bin/ar -X32_64"
	export NM="/usr/bin/nm -X32_64"
	# export TAR=/opt/freeware/bin/tar

	chmod +x ./configure
	./configure \
		--libdir=$1 \
		--with-perl=%{__perl} \
		--with-python=%{_bindir}/python \
		--with-shell=%{_bindir}/bash

	make -j8

	# Make man for perl Modules
	# It's not provided by git-manpages tar
	make man-perl

	# Build subtree
	make -C contrib/subtree
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
export LDFLAGS="-L/opt/freeware/lib  -Wl,-blibpath:$LIBPATH -Wl,-bmaxdata:0x80000000"
export CFLAGS="$CFLAGS -D_LARGE_FILES"

build_git \
    %{_libdir}
cd ..

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests


make_tests(){
    make -i test ||  ./print-failed-test-output

    make -C contrib/credential/netrc/ test || true
    make -C contrib/subtree/ test || true
}

cd 64bit
make_tests

cd ../32bit
make_tests


%install
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# Install on 64bit mode
cd 64bit
export OBJECT_MODE=64
LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib" \
make install DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor NO_REGEX=NeedsStartEnd 

make install DESTDIR=${RPM_BUILD_ROOT} -C contrib/subtree

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
make install DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor NO_REGEX=NeedsStartEnd 

make install DESTDIR=${RPM_BUILD_ROOT} -C contrib/subtree

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
make install-doc DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor
%else
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}
cp -a prebuilt_docs/man/* ${RPM_BUILD_ROOT}%{_mandir}
cp -a prebuilt_docs/html/* Documentation/
%endif

# Install man of perl Modules
make install-man-perl DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor


mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d
install -m 0644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/httpd/conf.d/git.conf
sed -e "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
    %{SOURCE3} > ${RPM_BUILD_ROOT}%{_sysconfdir}/gitweb.conf


mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/git

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3

find ${RPM_BUILD_ROOT} -type f -name .packlist     -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name '*.bs'        -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -exec rm -f {} ';'

%if %{without cvs}
# Remove git-cvs* and gitcvs*
find $RPM_BUILD_ROOT Documentation \( -type f -o -type l \) \
     \( -name 'git-cvs*' -o -name 'gitcvs*' \) -exec rm -f {} ';'
%endif
# endif without cvs

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

# # Create /usr/bin links
# mkdir -p ${RPM_BUILD_ROOT}/usr/bin
# cd ${RPM_BUILD_ROOT}/usr/bin
# ln -sf ../..%{_bindir}/* .
# cd -

# (find ${RPM_BUILD_ROOT}/usr/bin -type f | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files
# (find ${RPM_BUILD_ROOT}/usr/bin -type l | grep -vE "$exclude_re" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files

# Split core files
not_core_re="git-(add--interactive|contacts|credential-(libsecret|netrc)|difftool|filter-branch|instaweb|request-pull|send-mail)|gitweb"
grep -vE "$not_core_re|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
grep -vE "$not_core_re" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core.tmp
grep -E  "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

# Remove git-credential-cache--daemon.1 duplicates
grep -v "git-credential-cache--daemon.1" man-doc-files-core.tmp > man-doc-files-core

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files -f 32bit/bin-man-doc-git-files
%defattr(-,root,system)
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
%defattr(-,root,system)
%doc 32bit/README.md 32bit/COPYING 32bit/contrib/
%doc 32bit/Documentation/RelNotes
%doc 32bit/Documentation/howto 32bit/Documentation/technical
%doc 32bit/Documentation/*.txt 32bit/Documentation/*.html

%if %{with cvs}
%files cvs
%defattr(-,root,system)
%doc 32bit/Documentation/*git-cvs*.txt
%doc 32bit/Documentation/*git-cvs*.html
%{_mandir}/man1/*cvs*.1*
%{_bindir}/git-cvsserver*
%{_libexecdir}/git-core/*cvs*
%endif

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
#%%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui


%files -n gitk
%defattr(-,root,system)
%doc 32bit/Documentation/*gitk*.txt
%doc 32bit/Documentation/*gitk*.html
%{_mandir}/man1/*gitk*.1*
%{_bindir}/*gitk*
%{_datadir}/gitk
# /usr/bin/*gitk*


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
%defattr(-,root,system)
%{_libexecdir}/git-core/git-instaweb*
%{_mandir}/man1/git-instaweb.1*
%doc 32bit/Documentation/git-instaweb.txt
%doc 32bit/Documentation/git-instaweb.html

%files -n perl%{perl_version}-Git -f 32bit/perl-git-files
%defattr(-,root,system)
%{_mandir}/man3/*Git*.3pm*

%files -n perl-Git
%defattr(-,root,system)

%files subtree
%defattr(-,root,system)
%doc 32bit/Documentation/git-subtree.txt
# This doc aren't provided in prebuilt docs.
# %doc 32bit/Documentation/git-subtree.html
# %%{_mandir}/man1/git-subtree.1*

%{_libexecdir}/git-core/git-subtree*

%files svn
%defattr(-,root,system)
%doc 32bit/Documentation/*svn*.txt
%doc 32bit/Documentation/*svn*.html
%{_mandir}/man1/*svn*.1*
%{_libexecdir}/git-core/*svn*

%files all
# No files for you!


%changelog
* Sat Dec 04 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.34.1-1
- Update to 2.34.1

* Sat Nov 20 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.34.0-1
- Update to 2.34.0

* Mon Oct 18 2021 Etienne Guesnet <etienne.guesnet@atos.net> - 2.33.1-2
- Mass rebuild for new version of perl.
- Update for new perl.

* Sat Oct 16 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.33.1-1
- Update to 2.33.1

* Sat Aug 21 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.33.0-1
- Update to 2.33.0

* Mon Jun 21 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.32.0-1
- Update to 2.32.0

* Mon Jun 14 2021 Clément Chigot <clement.chigot@atos.net> - 2.31.1-2
- Remove .sign from sources

* Mon Mar 29 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.31.1-1
- Update to 2.31.1

* Tue Mar 16 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.31.0-1
- Update to 2.31.0

* Thu Feb 11 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.30.1-1
- Update to 2.30.1

* Fri Feb 05 2021 Clément Chigot <clement.chigot@atos.net> - 2.25.0-2
- Fix Source URL
- Remove without ibm_ssl condition
- Update minimal version for dependencies
- Clean up specfiles
- Add correct perl requirement
- Add grep requirement
- Add git-subtree and disable git-cvs by default

* Tue Feb 04 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.25.0-1
- New version 2.25.0
- Bullfreeware OpenSSL removal

* Fri Dec 20 2019 Clément Chigot <clement.chigot@atos.net> - 2.24.1-1
- Updated to version 2.24.1
- Built with IBM SSL by default

* Wed Nov 27 2019 Clément Chigot <clement.chigot@atos.net> - 2.22.0-3
- Fix %defattr
- Add -Wl,-bmaxdata for 32bit build
- Fix git-credential-cache--daemon.1 file conflict
- Remove /usr links
- Force python, perl, bash paths to be OpenSources version (ie /opt/freeware/bin)

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
