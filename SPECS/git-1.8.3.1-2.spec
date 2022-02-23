%define perl_version %(eval "`perl -V:version`"; echo $version)
%define perl_installlib %{_libdir}/perl5/%{perl_version}

Name: 		git
Version: 	1.8.3.1
Release: 	2
Summary:  	Core git tools
License: 	GPLv2
Group: 		Development/Tools
URL: 		http://kernel.org/pub/software/scm/git/
Source0: 	http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz
Source2: 	%{name}.conf.httpd
Source3: 	gitweb.conf.in
Patch0: 	%{name}-%{version}-aix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	asciidoc >= 8.6.3
BuildRequires:	coreutils
BuildRequires:	curl-devel >= 7.19.7-1
BuildRequires:	expat-devel >= 2.0.1
BuildRequires:	gettext
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	perl >= 5.8.8
BuildRequires:	xmlto >= 0.0.24-1
BuildRequires:	zlib-devel >= 1.2.3

Requires:	bash
Requires:	curl >= 7.19.7-1
Requires:	expat >= 2.0.1
Requires:	gettext
Requires:	less
Requires:	openssl >= 1.0.1
Requires:	perl >= 5.8.8
Requires:	python >= 2.6.2
Requires:	rsync
Requires:	zlib >= 1.2.3

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.


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
Requires:       perl(Net::SMTP::SSL), perl(Authen::SASL)

%description email
Git tools for sending email.


%package gui
Summary:        Git GUI tool
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       tcl >= 8.4
Requires:       tk >= 8.4

%description gui
Git GUI tool.


%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5.8.8
Requires:       subversion
# Requires:     perl(Term::Readkey)

%description svn
Git tools for importing Subversion repositories.


%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       tcl >= 8.4
Requires:       tk >= 8.4

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
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl >= 5.8.8
Requires:       perl(Error)

%description -n perl-Git
Perl interface to Git.


%prep
%setup -q
%patch0


%build
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
export CFLAGS="-D_LARGE_FILES"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --with-perl=/usr/bin/perl \
    --with-openssl=%{_prefix}

PATH=/opt/freeware/bin:$PATH gmake %{?_smp_mflags}


%install
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
LIBPATH="/opt/freeware/lib:/usr/lib" \
gmake install install-doc DESTDIR=${RPM_BUILD_ROOT} INSTALLDIRS=vendor

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
/usr/bin/strip ${RPM_BUILD_ROOT}%{_libexecdir}/git-core/* || :

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
mv ${RPM_BUILD_ROOT}/Error.pm ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version}
mv ${RPM_BUILD_ROOT}/Git ${RPM_BUILD_ROOT}%{_libdir}/perl5/%{perl_version}
mv ${RPM_BUILD_ROOT}/Git* ${RPM_BUILD_ROOT}%{_mandir}/man3
mv ${RPM_BUILD_ROOT}/private-Error.3 ${RPM_BUILD_ROOT}%{_mandir}/man3


find ${RPM_BUILD_ROOT} -type f -name .packlist -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name '*.bs' -empty -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -exec rm -f {} ';'

(find ${RPM_BUILD_ROOT}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) > bin-man-doc-files
(find ${RPM_BUILD_ROOT}%{_libexecdir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files

(find ${RPM_BUILD_ROOT}%{perl_installlib} -type f | sed -e s@^${RPM_BUILD_ROOT}@@) > perl-files

(find ${RPM_BUILD_ROOT}%{_mandir} -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool|git-daemon|Git" | sed -e s@^${RPM_BUILD_ROOT}@@ -e 's/$/*/' ) >> bin-man-doc-files

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .

(find ${RPM_BUILD_ROOT}/usr/bin -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^${RPM_BUILD_ROOT}@@) >> bin-man-doc-files


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files -f bin-man-doc-files
%defattr(-,root,system)
%doc README COPYING Documentation/*.txt contrib/
%doc Documentation/howto Documentation/technical
%{_datadir}/git-core/
%dir %{_libexecdir}/git-core/
/usr/bin/git
/usr/bin/git-receive-pack
/usr/bin/git-shell
/usr/bin/git-upload-archive
/usr/bin/git-upload-pack


%files arch
%defattr(-,root,system)
%doc Documentation/git-archimport.txt
%{_libexecdir}/git-core/git-archimport


%files cvs
%defattr(-,root,system)
%doc Documentation/*git-cvs*.txt
%{_bindir}/*cvsserver
%{_libexecdir}/git-core/*cvs*
/usr/bin/*cvsserver
%{_mandir}/man1/*cvs*.1*


%files daemon
%defattr(-,root,system)
%doc Documentation/*daemon*.txt
%{_libexecdir}/git-core/*daemon*
%{_mandir}/man1/*daemon*.1*
/var/lib/git


%files email
%defattr(-,root,system)
%doc Documentation/*email*.txt
%{_libexecdir}/git-core/*email*
%{_mandir}/man1/*email*.1*


%files gui
%defattr(-,root,system)
%{_libexecdir}/git-core/git-gui*
%{_libexecdir}/git-core/git-citool
%{_datadir}/git-gui
%{_mandir}/man1/git-citool.1*
%{_mandir}/man1/git-gui.1*


%files svn
%defattr(-,root,system)
%doc Documentation/*svn*.txt
%{_libexecdir}/git-core/*svn*
%{_mandir}/man1/*svn*.1*


%files -n gitk
%defattr(-,root,system)
%doc Documentation/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk
/usr/bin/*gitk*


%files -n perl-Git -f perl-files
%defattr(-,root,system)
%{_mandir}/man3/*Git*3
%{_mandir}/man3/private-Error.3


%files -n gitweb
%defattr(-,root,system)
%doc gitweb/INSTALL gitweb/README
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
/var/www/git/


%changelog
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
