%bcond_without dotests

Summary: A GNU general-purpose parser generator.
Name: bison
Version: 3.5.2
Release: 1
License: GPLv3+
Group: Development/Tools
Source0: ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.xz
Source100: %{name}-%{version}-%{release}.build.log

Patch0: bison-3.0.5-aix.patch
URL: http://www.gnu.org/software/bison/

# We must use the same version during build and use.
BuildRequires: m4 = 1.4.18
Requires: m4 = 1.4.18

Requires: /sbin/install-info
Requires: gettext >= 0.19.8


%description
Bison is a general purpose parser generator that converts a grammar
description for an LALR(1) context-free grammar into a C program to
parse that grammar. Bison can be used to develop a wide range of
language parsers, from ones used in simple desk calculators to complex
programming languages. Bison is upwardly compatible with Yacc, so any
correctly written Yacc grammar should work with Bison without any
changes. If you know Yacc, you shouldn't have any trouble using
Bison. You do need to be very proficient in C programming to be able
to use Bison. Bison is only needed on systems that are used for
development.

If your system will be used for C development, you should install
Bison.

%prep
%setup -q
%patch0 -p1 -b .aix

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

## # setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

## # first build the 64-bit version
cd 64bit
export CC="gcc -maix64 "
export LDFLAGS=" -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=64

export CFLAGS=$RPM_OPT_FLAGS

./configure \
     --prefix=%{_prefix} \
     --mandir=%{_mandir} \
     --infodir=%{_infodir} \

make %{?_smp_mflags}

## # now build the 32-bit version
cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=32

CFLAG="$RPM_OPT_FLAGS -D_LARGE_FILES -D_LARGEFILE_SOURCE" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \

make %{?_smp_mflags}


%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in *
  do
    mv ${f} ${f}_64
  done
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in bison yacc
  do
    mv ${f} ${f}_32
    ln -sf ${f}_64 ${f}
  done
)

# To be done by hand after, since very long
# Tested on 3.5.2: do nothing
# make syntax-check
# make distcheck

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/%{name}*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%check
%if %{with dotests}
cd 64bit
export CC="gcc -maix64 "
export CXX="g++ -maix64 "
export LDFLAGS=" -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=64
(gmake -k check || true)

cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export CXX="g++ -maix32 -D_LARGE_FILES"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=32
(gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/bison.info.gz %{_infodir}/dir --entry="* bison: (bison).                        The GNU parser generator." || :

# A bug in 1.875-1 packaging caused the system's /usr/bin/yacc to be
# relinked to point to the Toolbox version of yacc (bison).
# After updating, that link will now be gone, so check and see if that
# that situation exists, and if so, put the link back as it should be.
#
# Unfortunately, the bad link will still be there when this runs, because
# the old file isn't removed until after this %post script runs.
# So even if we created the link, the removal of 1.875 will then remove it
# again.  Still, let's leave this here so that future updates after 1.875-2
# will automatically correct the link if it is missing.
if [ -f /usr/ccs/bin/yacc ] && [ ! -L /usr/bin/yacc ] ; then
     /usr/bin/ln -sf /usr/ccs/bin/yacc /usr/bin/yacc
fi


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/bison.info.gz %{_infodir}/dir --entry="* bison: (bison).                        The GNU parser generator." || :
fi


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/AUTHORS 32bit/COPYING 32bit/ChangeLog 32bit/INSTALL 32bit/NEWS 32bit/README 32bit/THANKS
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/bison*
%{_datadir}/bison
%{_datadir}/aclocal/*
# %{_datadir}/locale/*/LC_MESSAGES/*.mo
#%{_libdir}/*.a


%changelog
* Tue Feb 25 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 3.5.2
- New version 3.5.2
- Add a requires to m4
- Create a check section
- No more porvides lib (static only)

* Mon Jul 30 2018 Harshita Jain<harjain9@in.ibm.com> 3.0.5-1
- Update to 3.0.5

* Mon Sep 21 2015 Tony Reix <tony.reix@bull.net> 3.0.4-1
- Update to 3.0.4

* Thu Jul 05 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.5-1
- Initial port on Aix6.1

* Fri May 6 2011 Patricia Cugny <patricia.cugny@bull.net> 2.4.3-1
- Update to 2.4.3

* Tue Jun 1 2010 Jean Noel Cordenner <jean-noel.cordenner> 2.4.2
- Update to 2.4.2

* Thu Jun 23 2005 Reza Arbab <arbab@austin.ibm.com> 1.875-3
- Link uses "-L/opt/freeware/lib -lintl" instead of "/opt/freeware/lib/libintl.a".

* Mon Mar 29 2004 David Clissold <cliss@austin.ibm.com> 1.875-2
- Fix the /usr/bin/yacc link; that one should belong to the AIX system yacc.
- Put a link to the toolbox one in /usr/linux/bin instead.

* Mon Nov 24 2003 David Clissold <cliss@austin.ibm.com> 1.875-1
- Update to version 1.875

* Mon Jan 06 2003 David Clissold <cliss@austin.ibm.com>
- Set prefix explicitly.  Was defaulting bison.simple to /usr/local.

* Fri Jun 14 2002 David Clissold <cliss@austin.ibm.com>
- Update to bison version 1.34

* Wed Jan 30 2002 David Clissold <cliss@austin.ibm.com>
- Update to bison version 1.30

* Wed Mar 07 2001 Marc Stephenson <marc@austin.ibm.com>
- Update to libtool 1.3.5a
- Add logic for default compiler

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man page.

* Fri Jul 16 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.28.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)

* Mon Mar  8 1999 Jeff Johnson <jbj@redhat.com>
- configure with datadir=/usr/lib (#1386).

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.
- update to 1.27

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- built for Manhattan
- added build root

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- various spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

