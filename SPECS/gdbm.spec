Summary: A GNU set of database routines which use extensible hashing.
Name: gdbm
Version: 1.8.3
Release: 2
Source: ftp://ftp.gnu.org/gnu/gdbm/gdbm-%{version}.tar.gz
Source1: libgdbm.so.2
URL: http://www.gnu.org/software/gdbm
License: GPL
Group: System Environment/Libraries
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root
BuildRequires: libtool >= 1.3.5
%define DEFCC cc

# Use --define 'no64 1' on the command line to disable 64bit build
%{!?no64:%define BUILD64 1}
%{?no64:%define BUILD64 0}
%define prefix64 %{prefix}/64

%description
Gdbm is a GNU database indexing library, including routines which use
extensible hashing.  Gdbm works in a similar way to standard UNIX dbm
routines.  Gdbm is useful for developers who write C applications and
need access to a simple and efficient database or who are building C
applications which will use such a database.


%package devel
Summary: Development libraries and header files for the gdbm library.
Group: Development/Libraries
Requires: gdbm
Prereq: /sbin/install-info

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

Install gdbm-devel if you are developing C programs which will use the
gdbm database library.  You'll also need to install the gdbm package.

%prep
%setup -q

%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
/usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gunzip -c %{SOURCE0} |tar -xf -
cd %{name}-%{version}
%endif

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
       export CFLAGS="$RPM_OPT_FLAGS"
fi

export SED=/usr/bin/sed
libtoolize --force
%configure --disable-static
make includedir=%{_prefix}/include/gdbm

# We need to add libgdbm.so.2 for older apps that linked dynamically with
#  libgdbm.a(libgdbm.so.2).  This binary was pre-built from gdbm 1.8.0.
cd .libs
cp %{SOURCE1} .
# make it load-only (new links should only be against libgdbm.so.3).
/usr/bin/strip -e libgdbm.so.2
ar -crv libgdbm.a libgdbm.so.2
cd ..

%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64

libtoolize --force
%configure --disable-static
make includedir=%{_prefix}/include/gdbm

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../..
/usr/bin/ar -q .libs/libgdbm.a \
   64bit/%{name}-%{version}/.libs/libgdbm.so.3

%endif #BUILD64

%install
rm -rf $RPM_BUILD_ROOT

export SED=/usr/bin/sed
make INSTALL_ROOT=$RPM_BUILD_ROOT install install-compat \
    prefix=%{_prefix} \
    includedir=%{_prefix}/include/gdbm

( cd $RPM_BUILD_ROOT
  ln -sf gdbm/gdbm.h .%{_prefix}/include/gdbm.h
  gzip -9nf .%{_prefix}/info/gdbm*info*

  mkdir -p usr/include || :
  mkdir -p usr/lib || :

  cd usr/include
  ln -sf ../..%{_prefix}/include/* .
  cd -

  cd usr/lib
  ln -sf ../..%{_prefix}/lib/* .
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
 mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
 cd $RPM_BUILD_ROOT/%{prefix64}/lib
 ln -s ../../lib/*.a .
)
%endif

%post devel
/sbin/install-info %{_prefix}/info/gdbm.info.gz %{_prefix}/info/dir --entry="* gdbm: (gdbm).                   The GNU Database."

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/gdbm.info.gz %{_prefix}/info/dir --entry="* gdbm: (gdbm).                   The GNU Database."
fi

%files
%defattr(-,root,system)
%doc COPYING NEWS README
%{_prefix}/lib/libgdbm.a
/usr/lib/libgdbm.a
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif

%files devel
%defattr(-,root,system)
/usr/include/*
/usr/lib/libgdbm.la
%{_prefix}/lib/libgdbm.la
%{_prefix}/include/*
%{_prefix}/info/gdbm*gz
%{_prefix}/man/man3/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Dec 14 2004 David Clissold <cliss@austin.ibm.com> 1.8.3-2
- Build 64-bit library version.

* Tue Apr 13 2004 David Clissold <cliss@austin.ibm.com> 1.8.3-1
- Update to 1.8.3.

* Thu Mar 22 2001 Marc Stephenson <marc@austin.ibm.com>
- Build both 32- and 64-bit libraries

* Fri Mar 09 2001 Marc Stephenson <marc@austin.ibm.com>
- Use libtool 1.3.5a
- Rebuild against new shared objects
- Build with default compiler
- Add Bull freeware compatibility member

* Thu Feb 22 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- make sure created database header is initialized (#4457).

* Tue Jun  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.8.0.
- repackage to include /usr/include/gdbm/*dbm.h compatibility includes.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 19)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- gdbm-devel moved to Development/Libraries

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- buildroot and built for Manhattan

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc
