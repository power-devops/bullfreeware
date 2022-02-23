Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.8.5
Release: 1
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/automake
Source: ftp://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.bz2
Prefix: %{_prefix}
Prereq: /sbin/install-info
BuildArchitectures: noarch
BuildRequires: autoconf >= 2.54
Buildroot: %{_tmppath}/%{name}-root

%description
Automake is a tool for automatically generating "Makefile.in" files from
Makefile.am files.  Makefile.am is a series of make macro definitions (with
rules occasionally thrown in).  The generated Makefile.in files are compatible
with the GNU Makefile standards.

%prep
%setup -q

%build

%configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/info/automake*

cd $RPM_BUILD_ROOT
mkdir -p usr/bin || true 
mkdir -p usr/share || true 
for file in automake aclocal
do
   ln -sf ../..%{_prefix}/bin/$file usr/bin/$file
done
ln -sf ../..%{_prefix}/share/automake usr/share/automake

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/info/automake.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_prefix}/info/automake.info.gz %{_prefix}/info/dir
fi

%files
%defattr(-,root,system)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
/usr/bin/aclocal
/usr/bin/automake
/usr/share/automake
%{_prefix}/bin/*
%{_prefix}/info/automake*
%{_prefix}/share/*

%changelog
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
