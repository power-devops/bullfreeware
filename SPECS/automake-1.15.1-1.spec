# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.15.1
Release: 1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/automake
Source0: ftp://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.gz
Source1: %{name}-%{version}-%{release}.build.log
Prefix: %{_prefix}

BuildArchitectures: noarch
BuildRequires: autoconf >= 2.65

# From automake-1.15-4.fc23.spec :
Requires:   autoconf >= 2.65
# This is needed to allow 'help2man' to run 'automake --help' during build.
BuildRequires:   perl(Thread::Queue)
# requirements not detected automatically (#919810)
Requires:   perl(Thread::Queue)
Requires:   perl(threads)
# for better tests coverage:
%if %{with dotests}
BuildRequires: libtool gettext-devel flex bison
BuildRequires: make
#BuildRequires: texinfo-tex texlive-dvips
#BuildRequires: dejagnu expect emacs imake python-docutils vala
#BuildRequires: cscope ncompress sharutils help2man
# GCC/Linux world: to be adapted
#BuildRequires: java-devel-openjdk gcc-gfortran
#BuildRequires: gcc-objc gcc-objc++
%endif
# The filtering macros are currently in /etc/rpm/macros.perl:
#BuildRequires: perl-macros


%description
Automake is a tool for automatically generating "Makefile.in" files from
Makefile.am files.  Makefile.am is a series of make macro definitions (with
rules occasionally thrown in).  The generated Makefile.in files are compatible
with the GNU Makefile standards.

%prep
%setup -q

%build

export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.

export CC="/usr/bin/gcc"
export CXX="/usr/bin/g++"
export CFLAGS="-O2"
export AR="/usr/bin/ar -X32_64"

%configure --prefix=%{_prefix}
gmake



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/info/automake*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

(gmake -k check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_prefix}/info/automake.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_prefix}/info/automake.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS
# /usr/bin/aclocal
# /usr/bin/automake
# /usr/share/automake
%{_prefix}/bin/*
%{_prefix}/info/automake*
%{_prefix}/share/*

%changelog
* Wed Mar 25 2020 Cl??ment Chigot <clement.chigot@atos.net> 1.15.1-1
- BullFreeware Mass Rebuild for clean builds
- Move tests to %check section
- Remove /usr links
- Remove BuildRoot

* Wed Mar 09 2016 Tony Reix <tony.reix@atos.net> 1.15-2
- BuildRequires: autoconf >= 2.65

* Wed Aug 05 2015 Hamza Sellami <hamza.sellami@atos.net>
- Update to version 1.15

* Fri Apr 22 2005 David Clissold <cliss@austin.ibm.com> 1.8.5-1
- Update to version 1.8.5

* Tue Feb 17 2004 David Clissold <cliss@austin.ibm.com> 1.7.9-1
- Update to version 1.7.9

* Fri Jun 14 2002 David Clissold <cliss@austin.ibm.com>
- Update to version 1.6.2.  Just announced as I was building 1.6.1!

* Fri Jun 14 2002 David Clissold <cliss@austin.ibm.com>
- Update to version 1.6.1

* Tue Oct 02 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 1.5

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
