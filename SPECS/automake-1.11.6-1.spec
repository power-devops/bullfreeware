Summary: A GNU tool for automatically creating Makefiles.
Name: automake
Version: 1.11.6
Release: 1
License: GPL
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/automake/%{name}-%{version}.tar.xz
URL: http://www.gnu.org/software/automake
BuildRoot: /var/tmp/%{name}-root

BuildRequires: autoconf >= 2.60
Requires: /sbin/install-info
Requires:   autoconf >= 2.60

BuildArchitectures: noarch

%define DEFCC cc

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles. If you install Automake, you will also need to install
GNU's Autoconf package.


%prep
export PATH=/opt/freeware/bin:$PATH
rm -rf $RPM_BUILD_ROOT
%setup -q

%build
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS=$RPM_OPT_FLAGS


%configure --prefix=%{_prefix}
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/*.info

cd $RPM_BUILD_ROOT
mkdir -p usr/bin || true 
for file in automake aclocal
do
	ln -sf ../..%{_bindir}/$file usr/bin/$file
done


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
/sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,system)
%doc AUTHORS COPYING INSTALL NEWS README THANKS TODO
%{_bindir}/*
%{_infodir}/*.info*
%{_mandir}/man1/*
%{_prefix}/share/*
/usr/bin/*

%changelog
* Thu Oct 06 2016 Tony Reix <tony.reix@bull.net> 1.11.6-1
- Update to version 1.11.6

* Tue Mar 01 2011 Patricia Cugny <patricia.cugny@bull.net> 1.11.1-1
- modify spec file

* Fri Apr 23 2010 Jean Noel Cordenner <Jean-noel.cordenner@bull.net> 1.11.1
- Update to version 1.11.1

* Fri Apr 06 2007 Christophe Belle <christophe.belle@bull.net> 1.10-1
- Update to version 1.10

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
