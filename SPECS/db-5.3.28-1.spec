%bcond_without dotests
Summary: The Berkeley Database, the Open Source embedded database system
Name: db
%define major_version 5.3
%define minor_version 28
Version: %{major_version}.%{minor_version}
Release: 1
License: BSD and Sleepycat
Group: System Environment/Libraries
# Local tar.gz
Source: db-%{version}.tar.gz

Patch1: db-4.8.24-inst.patch
Patch2: db-6.2.23-compilerflag.patch

Source1: libdb-4.8.so-aix32
Source2: libdb-4.8.so-aix64
Source100: %{name}-%{version}-%{release}.build.log 
URL: https://www.oracle.com/database/technologies/related/berkeleydb.html

BuildRequires: libgcc >= 8.4.0-1
Requires: libgcc >= 8.4.0-1

%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif

%define _libdir64 %{_prefix}/lib64

%description
Berekley DB is a programmatic toolkit that provides high-performance built-in 
database support for desktop and server applications and for information 
appliances.

The Berkeley DB access methods include B+tree, Extended Linear Hashing, Fixed 
and Variable-length records, and Queues.  Berkeley DB provides full 
transactional support, database recovery, online backups, and separate
access to locking, logging and shared memory caching subsystems.

Berkeley DB supports C, C++, Java, Tcl, Perl, and Python APIs.

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%prep
%setup -q
%patch1 -p1 -b .db-inst
%patch2 -p0 -b .compilerflag
# Prep 64-bit build in 64bit subdirectory
##########################################
# Test whether we can run a 64bit command so we don't waste our time
# /usr/bin/locale64 >/dev/null 2>&1
mkdir 64bit
cd 64bit
gunzip -c %{SOURCE0} |tar -xf -
cd %{name}-%{version}
cp ../../dist/configure ./dist/

%build
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32 -D_LARGE_FILES -O2"
export CFLAGS="`echo $CFLAGS | sed 's:-O2::'` -Wall"
cd build_unix
# If we don't set LIBSO_LIBS, we get unresolved pthread symbols
#  when linking the db library.
LIBSO_LIBS=-lpthread ../dist/configure --prefix=%{_prefix} \
	--libdir=%{_libdir} --enable-compat185 --enable-shared --disable-static \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
gmake


#Patch on-the-fly  (DB185 is only used internally; not available for
# the packaged db_185.h file).
 perl -pi -e "s|^DB185|DB|" db_185.h
cd ..
/usr/bin/ar -qv build_unix/.libs/libdb-5.3.a \
        build_unix/.libs/libdb-5.3.so
(
cd build_unix/.libs
#db 32bits
cp %{SOURCE1}                      libdb-4.8.so
/usr/bin/strip -X32 -e             libdb-4.8.so
/usr/bin/ar    -X32 -q libdb-6.2.a libdb-4.8.so

#db 64bits
cp %{SOURCE2}                      libdb-4.8.so
/usr/bin/strip -X64 -e             libdb-4.8.so
/usr/bin/ar    -X64 -q libdb-6.2.a libdb-4.8.so
)


# Now build again as 64bit
###########################
cd 64bit/%{name}-%{version}
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64 -O2 "
cd build_unix
# If we don't set LIBSO_LIBS, as of 3.3.11, we get unresolved pthread symbols
#  when linking the db library.
LIBSO_LIBS=-lpthread ../dist/configure --prefix=%{_prefix} \
	--libdir=%{_libdir64} --enable-compat185 --enable-shared --disable-static \
	--host=%{buildhost} --target=%{buildhost} --build=%{buildhost}
gmake

#Patch on-the-fly  (DB185 is only used internally; not available for
# the packaged db_185.h file).
perl -pi -e "s|^DB185|DB|" db_185.h

# Go back to 32-bit library and add our 64bit shared object
#  into same archive
cd ../../..
/usr/bin/ar -qv build_unix/.libs/libdb-5.3.a \
    64bit/%{name}-%{version}/build_unix/.libs/libdb-5.3.so


%install
rm -rf $RPM_BUILD_ROOT
export OBJECT_MODE=64
cd 64bit/db-%{version}/build_unix
make DESTDIR=$RPM_BUILD_ROOT install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)

(
    cd  ${RPM_BUILD_ROOT}/%{_libdir64}
    cp %{SOURCE2} libdb-4.8.so
    ln -sf libdb-4.8.so libdb-4.so
)

export OBJECT_MODE=32
cd ../../../build_unix
make DESTDIR=$RPM_BUILD_ROOT install
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

cp %{SOURCE1} $RPM_BUILD_ROOT/%{_libdir}
(
    cd  ${RPM_BUILD_ROOT}/%{_bindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)
(
    cd  ${RPM_BUILD_ROOT}/%{_libdir}
    cp %{SOURCE1} libdb-4.8.so
    ln -sf libdb-4.8.so libdb-4.so
    mv libdb-%{major_version}.a libdb.a
    ln -sf libdb.a libdb-4.8.a

    /usr/bin/strip -X32_64 -e          libdb-4.8.so
    /usr/bin/strip -X32_64 -e ../lib64/libdb-4.8.so
    /usr/bin/ar -X32_64 -qc libdb.a          libdb-4.8.so
    /usr/bin/ar -X32_64 -qc libdb.a ../lib64/libdb-4.8.so
)

#Add links for 64-bit library members
(
    cd $RPM_BUILD_ROOT/%{_libdir64}
    ln -s ../lib/*.a .
    cd $RPM_BUILD_ROOT
)


%clean 
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%check
%if %{with dotests}
echo "Not test for db!"
%endif


%pre
rel=`rpm -qi db|grep Release|awk '{print $3}'` 
db_ver=`rpm -qi db|grep Version|awk '{print $3}'`
rpm_ver=`ODMDIR=/usr/lib/objrepos /usr/bin/odmget -q lpp_name=rpm.rte product | grep ver | awk '{print $3}'`
if [[ $rel -eq 3 && $db_ver == "4.8.24" && $rpm_ver -eq 4 ]];then
	cd /opt/freeware/lib
	for lib in libdb4.a libdb.so libdb.a libdb-4.so libdb-4.a libdb-4.8.so libdb-4.8.a
	do
        	/usr/bin/cp -h $lib $lib.orig
	done
fi

%triggerpostun -- db = 4.8.24-3
rpm_ver=`ODMDIR=/usr/lib/objrepos /usr/bin/odmget -q lpp_name=rpm.rte product | grep ver | awk '{print $3}'`
if [[ $rpm_ver -eq 4 ]];then
	cd /opt/freeware/lib
	for lib in libdb4.a libdb.so libdb.a libdb-4.so libdb-4.a libdb-4.8.so libdb-4.8.a
	do
        	mv $lib.orig $lib
	done
fi


%posttrans
# Reinstate the LPP rpm.rte symlinks, they have probably been replaced/removed
if ! test -e /usr/lib/libdb.a && ! test -h /usr/lib/libdb.a
then
  ln -sf /usr/opt/rpm/lib/libdb.a /usr/lib/libdb.a
fi
if ! test -e /usr/lib/libdb.so && ! test -h /usr/lib/libdb.so
then
  ln -sf /usr/opt/rpm/lib/libdb.so /usr/lib/libdb.so
fi
 

%files
%defattr(-,root,system)
%docdir %{_prefix}/docs
%doc LICENSE README 
%{_bindir}/db_*

%{_libdir}/libdb.a
%{_libdir}/libdb-%{major_version}.so
# Compatibility
%{_libdir}/libdb-4.8.a
%{_libdir}/libdb-4.8.so
%{_libdir}/libdb-4.so


%{_includedir}/*
#%attr(755,bin,bin) %dir %{_libdir64}
%{_libdir64}/libdb.a
%{_libdir64}/libdb-%{major_version}.so
%{_libdir64}/libdb-4.8.a
%{_libdir64}/libdb-4.8.so
%{_libdir64}/libdb-4.so

%files devel
%defattr(-,root,system)
%doc docs/*
%{_includedir}/db.h
%{_includedir}/db_185.h
%{_includedir}/db_cxx.h


%changelog
* Wed Oct 21 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 5.3.28-1
- Create 5.3.28 specfile using 6.2.38-25 specfile.
- Stop providing link to /usr
- Increase compatibility with version 4
 
* Fri Apr 17 2020 Reshma V Kumar <reskumar@in.ibm.com> - 6.2.38-2
- Rebuild to ship libdb.a

* Fri Aug 30 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 6.2.38
- Updated to 6.2.38 to fix security vulnerability 

* Mon Aug 20 2018 Reshma V Kumar <reskumar@in.ibm.com> 6.2.32-2
- Rebuild to add libgcc dependency and include libdb-4.8.so with the rpm

* Thu Nov 30 2017 Reshma V Kumar <reskumar@in.ibm.com> 6.2.32-1
- Update to latest version

* Thu Jan 29 2015 Sangamesh Mallayya <smallayy@in.ibm.com> 4.8.24-3
- Rebuild for distribution in AIX toolbox.

* Wed Oct 05 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 4.8.24-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 24 2011 Gerard Visiedo <gerard.visiedo@bull.net> 4.8.24-2
- Add devel module

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

