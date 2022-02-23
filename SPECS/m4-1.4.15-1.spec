Summary: The GNU macro processor.
Name: m4
Version: 1.4.15
Release: 1
Copyright: GPLv3+
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
URL: http://www.gnu.org/software/m4
Buildroot: /var/tmp/%{name}-root

%define DEFCC cc
%define _infodir %{_prefix}/share/info
%define _mandir %{_prefix}/share/man

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

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

./configure --prefix=%{_prefix}
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

rm -f  $RPM_BUILD_ROOT%{_infodir}/dir
gzip -9fn $RPM_BUILD_ROOT%{_infodir}/%{name}*

[[ ! -d $RPM_BUILD_ROOT/usr/linux/bin ]] && mkdir -p $RPM_BUILD_ROOT/usr/linux/bin
cd ${RPM_BUILD_ROOT}/usr/linux/bin
ln -sf ../../..%{_bindir}/%{name} .


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
%doc AUTHORS NEWS README COPYING THANKS INSTALL TODO
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/*
/usr/linux/bin/*

%changelog
* Mon Feb 28 2011 Patricia Cugny <patricia.cugny@bull.net> 1.4.15-1
- Update to version  1.4.15

* Fri Apr 23 2010 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.4.14-1
- Update to version  1.4.14

* Mon Jun 22 2009 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.4.13-1
- Update to version  1.4.13

* Wed Mar 26 2003 David Clissold <cliss@austin.ibm.com>
- Rebuild using IBM VAC compiler.

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

