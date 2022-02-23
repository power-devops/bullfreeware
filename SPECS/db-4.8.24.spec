Summary: The Berkeley Database, the Open Source embedded database system
Name: db
Version: 4.8.24
Release: 1
License: Sleepycat
Group: System Environment/Libraries
Source: http://www.sleepycat.com/update/%{version}/db-%{version}.tar.gz
Patch1: db-4.8.24-inst.patch
URL: http://www.sleepycat.com/index.html
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root
%define DEFCC cc

Buildroot: /var/tmp/%{name}-root
%ifos aix5.1
%define buildhost powerpc-ibm-aix5.1.0.0
%endif
%ifos aix5.2
%define buildhost powerpc-ibm-aix5.2.0.0
%endif
%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

# Use --define 'no64 1' on the command line to disable 64bit build
%{!?no64:%define BUILD64 1}
%{?no64:%define BUILD64 0}
%define prefix64 %{prefix}/64

%description
Berekley DB is a programmatic toolkit that provides high-performance built-in 
database support for desktop and server applications and for information 
appliances.

The Berkeley DB access methods include B+tree, Extended Linear Hashing, Fixed 
and Variable-length records, and Queues.  Berkeley DB provides full 
transactional support, database recovery, online backups, and separate
access to locking, logging and shared memory caching subsystems.

Berkeley DB supports C, C++, Java, Tcl, Perl, and Python APIs.

%prep
%setup -q
%patch1 -p1 -b .db-inst

%if %{BUILD64} == 1
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
# /usr/bin/locale64 >/dev/null 2>&1
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
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    else 
       export CC=gcc
    fi
fi
cd build_unix
# If we don't set LIBSO_LIBS, we get unresolved pthread symbols
#  when linking the db library.
LIBSO_LIBS=-lpthread ../dist/configure --prefix=%{_prefix} \
	--enable-compat185 --enable-shared --disable-static \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
make

#Patch on-the-fly  (DB185 is only used internally; not available for
# the packaged db_185.h file).
 perl -pi -e "s|^DB185|DB|" db_185.h
cd ..
/usr/bin/ar -qv build_unix/.libs/libdb-4.8.a \
        build_unix/.libs/libdb-4.8.so


%if %{BUILD64} == 1
# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64
cd build_unix
# If we don't set LIBSO_LIBS, as of 3.3.11, we get unresolved pthread symbols
#  when linking the db library.
LIBSO_LIBS=-lpthread ../dist/configure --prefix=%{_prefix} \
	--enable-compat185 --enable-shared --disable-static \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
make

#Patch on-the-fly  (DB185 is only used internally; not available for
# the packaged db_185.h file).
perl -pi -e "s|^DB185|DB|" db_185.h

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../../..
/usr/bin/ar -qv build_unix/.libs/libdb-4.8.a \
    64bit/%{name}-%{version}/build_unix/.libs/libdb-4.8.so
%endif #BUILD64

%install
rm -rf $RPM_BUILD_ROOT
cd build_unix
make prefix=$RPM_BUILD_ROOT%{_prefix} install

cd $RPM_BUILD_ROOT%{_prefix}/lib
ln -sf libdb-4.8.a libdb.a
ln -sf libdb-4.8.a libdb-4.a
ln -sf libdb-4.8.a libdb4.a
cd -

( cd $RPM_BUILD_ROOT

 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
)

%if %{BUILD64} == 1
#Add links for 64-bit library members
(
mkdir -p $RPM_BUILD_ROOT/%{prefix64}/lib
cd $RPM_BUILD_ROOT/%{prefix64}/lib
ln -s ../../lib/*.a .
)
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%docdir %{_prefix}/docs
%doc LICENSE README 
%{_prefix}/bin/db_*
%{_prefix}/lib/*
%{_prefix}/include/*
/usr/bin/*
/usr/lib/*
/usr/include/*
%if %{BUILD64} == 1
%attr(755,bin,bin) %dir %{prefix64}
%attr(755,bin,bin) %dir %{prefix64}/lib
%{prefix64}/lib/lib*.a
%endif


%changelog
* Mon Jan 18 2010 Cordenner Jean Noel <jean-noel.cordenner@bull.net> 4.8.24
- New release 4.8.24

* Wed Oct 15 2008 Cordenner Jean Noel <jean-noel.cordenner@bull.net> 4.4.20-1 
- Fix library build

* Wed Apr 2 2008 Cordenner Jean Noel <jean-noel.cordenner@bull.net> 4.4.20 
- New release 4.4.20

* Tue Dec 14 2004 David Clissold <cliss@austin.ibm.com> 3.3.11-4
- Build 64-bit library version.

* Thu Feb 27 2003 David Clissold <cliss@austin.ibm.com>
- Fix the __db185_open prototype for the db_185.h header.
- Also, legal change; this should be left as sleepycat license.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license

* Wed Aug 15 2001 David Clissold <cliss@austin.ibm.com>
- Update to version 3.3.11

* Thu Jun 07 2001 David Clissold <cliss@austin.ibm.com>
- Package was inadvertently shipping a bogus core and temp file.

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Tue Feb 20 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Thu Feb 24 2000 Cristian Gafton <gafton@redhat.com>
- add patch from Andreas Jaeger to fix dtype lookups (for glibc 2.1.3
  builds)

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man page.

* Fri Jan 21 2000 Cristian Gafton <gafton@redhat.com>
- apply patch to fix a /tmp race condition from Thomas Biege
- simplify %install

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.78.1.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- added a serial tag so it upgrades right

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Sep 16 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for large file support in glob
 
* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.77

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- udpated from 3.75 to 3.76
- various spec file cleanups
- added install-info support

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
