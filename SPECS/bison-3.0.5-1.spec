Summary: A GNU general-purpose parser generator.
Name: bison
Version: 3.0.5
Release: 1
License: GPLv2+
Group: Development/Tools
Source0: ftp://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.xz
Patch0: bison-%{version}-aix.patch
URL: http://www.gnu.org/software/bison/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: m4 >= 1.4
Requires: /sbin/install-info
%define DEFCC cc

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
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .aix

%build

export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

########################################################################
### ATTENTION seulement en 32bit. Les libs generees sont statiques ??
### si 64bit $AR ne passe pas dans make ??
########################################################################

## # setup environment for 32-bit and 64-bit builds
## export AR="/usr/bin/ar -X32_64"
## export NM="/usr/bin/nm -X32_64"

## # first build the 64-bit version
## export CC="/usr/vac/bin/xlc_r -q64"
## export CXX="/usr/vacpp/bin/xlC_r -q64"

export CC=gcc
export CXX=g++

# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS=$RPM_OPT_FLAGS

## AR="/usr/bin/ar -X32_64" \
## ./configure \
##     --prefix=%{_prefix} \
##     --mandir=%{_mandir} \
##     --infodir=%{_infodir}

## make %{?_smp_mflags}

## cp lib/libbison.a .
## cp lib/liby.a .

## make dsiestclean

## # now build the 32-bit version
## export CC="/usr/vac/bin/xlc_r"
## export CXX="/usr/vacpp/bin/xlC_r"

export CC=gcc
export CXX=g++

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES -D_LARGEFILE_SOURCE" \
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

gmake %{?_smp_mflags}

(gmake check || true )

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# To be done by hand after, since very long
#make check syntax-check
#make distcheck

## # add the 64-bit shared objects to the shared library containing already the
## # 32-bit shared objects
## ${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/liby.a ./????

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/%{name}*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

(
  cd $RPM_BUILD_ROOT
  mkdir -p usr/bin
  cd usr/bin
  ln -sf ../..%{_bindir}/bison .
  cd -

  mkdir -p usr/linux/bin
  cd usr/linux/bin
  ln -sf ../../..%{_bindir}/* .
  cd -

  mkdir -p usr/share
  cd usr/share
  ln -sf ../..%{_datadir}/bison .
)


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


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,system)
%doc AUTHORS AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/bison*
%{_datadir}/bison
%{_datadir}/aclocal/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
/usr/bin/*
/usr/linux/bin/*
/usr/share/*
%{_libdir}/*.a

%changelog
* Tue Apr 30 2019 Tony Reix <tony.reix@bull.net> 3.0.5-1
- Update to 3.0.5

* Tue Sep 21 2015 Tony Reix <tony.reix@bull.net> 3.0.4-1
- Update to 3.0.4

* Thu Jul 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.5-1
- Initial port on Aix6.1

* Fri May 6 2011 Patricia Cugny <patricia.cugny@bull.net> 2.4.3-1
- Update to 2.4.3

* Mon Jun 1 2010 Jean Noel Cordenner <jean-noel.cordenner> 2.4.2
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

