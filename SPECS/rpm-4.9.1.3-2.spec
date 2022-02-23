# To make this package relocateable, change the Prefix: line
Summary: The RPM package management system
Name: rpm
%define version 4.9.1.3
Version: %{version}
Release: 2
Group: System Environment/Base
Source: http://rpm.org/releases/rpm-4.9.x/rpm-%{version}.tar.bz2
Source1: rpm-wrapper
Source2: rpm-find-provides-aix.c
Source3: rpm-4.9.1.3.macros.aix
Source4: mkvirtpkg.rpm-4.9.1.3
Patch0: rpm-%{version}-aix.patch
Patch1: rpm-%{version}-rpmrc.patch
Patch2: rpm-%{version}-aixdef.patch
Patch3: rpm-%{version}-header.patch
Patch4: rpm-%{version}-rpmbuild.patch
Patch5: rpm-%{version}-test.patch
Patch6: rpm-%{version}-glob_pattern.patch
Patch7: rpm-%{version}-ramfs.patch
Patch8: rpm-%{version}-macros_aix.patch
#Patch1: rpm-%{version}-payload.patch
#Patch2: rpm-%{version}-typechk.patch
#Patch3: rpm-%{version}-ramfs.patch
#Patch4: rpm-%{version}-mode.patch
#Patch5: rpm-%{version}-unsetenv.patch
#Patch6: rpm-%{version}-pyhack.patch
#Patch7: rpm-%{version}-freespace.patch
#Patch8: rpm-%{version}-dbpath.patch
#Patch9: rpm-%{version}-glob.patch
#Patch10: rpm-%{version}-stat64.patch
#Patch11: rpm-%{version}-open64.patch
#Patch12: rpm-%{version}-reloc.patch
#Patch13: rpm-%{version}-nonrpm.patch
#Patch14: rpm-%{version}-CVE20102059.patch
License: GPL
Conflicts: patch < 2.5
BuildRoot: /var/tmp/%{name}-%{version}-root
BuildRequires: db, make, zlib-devel
#The following should probably be removed for later versions of rpm.
Requires: db =< 4.8.24
Requires: popt =< 1.16
Requires: libiconv =< 1.13.1
Requires: gettext =< 0.17
Requires: file-libs =< 5.12
Requires: nss =< 3.13.2
Requires: nspr =< 4.9
Requires: bash =< 4.2
Requires: info =< 4.13
Requires: readline =< 6.2
Requires: lua =< 5.1.5
Requires: rpm-README-AIX =< 4.9.1.3

Prefix: %{_prefix}
%define DEFCC cc

%description
The RPM Package Manager (RPM) is a powerful command-line driven package
management system capable of installing, uninstalling, verifying, querying, and
updating software packages.  Each software package consists of an archive of
files along with information about the package like its version, a description,
etc.

%package devel
Summary: Development files for applications which will manipulate RPM packages.
Group: Development/Libraries
Requires: rpm = %{version}, popt

%description devel
This package contains the RPM C library and header files.  These development
files will simplify the process of writing programs which manipulate RPM
packages and databases. These files are intended to simplify the process of
creating graphical package managers or any other tools that need an intimate
knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that will
manipulate RPM packages and databases.

%package devel-python
Summary: This package contains files to be added on top of rpm-devel for python developements.
Group: Development/Tools
Requires: rpm-devel = %{version}

%description devel-python
This package contains scripts and executable programs that are used to build with python
packages using RPM.



%prep
%setup -q 
%patch0 -p1 -b .aix
%patch1 -p1 -b .rpmrc
%patch2 -p1 -b .aixdef
%patch3 -p1 -b .header
%patch4 -p1 -b .rpmbuild
%patch5 -p1 -b .test
%patch6 -p1 -b .glob_pattern
%patch7 -p1 -b .ramfs
%patch8 -p1 -b .macros_aix
#%patch1 -p1 -b .payload
#%patch2 -p1 -b .typechk
#%patch3 -p1 -b .ramfs
#%patch4 -p1 -b .mode
#%patch5 -p1 -b .unsetenv
#%patch6 -p1 -b .hack
#%patch7 -p0 -b .freespace
#%patch8 -p0 -b .dbpath
#%patch9 -p0 -b .glob
#%patch10 -p0 -b .stat64
#%patch11 -p0 -b .open64
#%patch12 -p0 -b .reloc
#%patch13 -p0 -b .nonrpm
#%patch14 -p0 -b .CVE20102059

%build
# Use the default compiler for this platform - gcc otherwise
if [ -z "$CC" ]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if test "X$CC" != 'Xgcc'; then
    export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
if test "X$CC" = 'Xcc'; then
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -ma"
fi

%ifarch ppc rs6000
LDFLAGS="-Wl,-brtl"
%else
LDFLAGS=
%endif

sed -e "s;defined(hpux);defined(hpux) \|\| defined(_AIX);" misc/fts.h >misc/fts.h.tmp
mv misc/fts.h.tmp misc/fts.h


export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS" MKDIR=/usr/bin/mkdir \
CPPFLAGS='-I/usr/include/nspr4 -I/usr/include/nss3' \
 ./configure --disable-static --enable-shared --prefix=%{_prefix} --mandir=%{_mandir} --with-external-db --enable-python

gmake CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS"



# Workaround optimzation problem
rm ./rpmio/.libs/rpmio.o ./rpmio/rpmio.lo lib/librpm.la
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-O2::'`
gmake CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS"


${CC} -o find-provides-aix %{SOURCE2} -lld
ln -sf find-provides-aix find-provides


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export RM="/usr/bin/rm -f"

gmake DESTDIR="$RPM_BUILD_ROOT" install
#gmake DESTDIR="$RPM_BUILD_ROOT" install -C python
mkdir -p $RPM_BUILD_ROOT%{_prefix}/etc/rpm
mkdir -p $RPM_BUILD_ROOT/tmp/bin
mkdir -p $RPM_BUILD_ROOT/tmp/lib/rpm
mkdir -p $RPM_BUILD_ROOT/tmp/lib/rpm/fileattrs


(cd $RPM_BUILD_ROOT
mkdir -p .%{_prefix}/src/packages
mkdir -p .%{_prefix}/src/packages/BUILD
mkdir -p .%{_prefix}/src/packages/RPMS
mkdir -p .%{_prefix}/src/packages/RPMS/noarch
mkdir -p .%{_prefix}/src/packages/RPMS/ppc
mkdir -p .%{_prefix}/src/packages/RPMS/powerpc
mkdir -p .%{_prefix}/src/packages/SOURCES
mkdir -p .%{_prefix}/src/packages/SPECS
mkdir -p .%{_prefix}/src/packages/SRPMS


 for dir in bin include src
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done

mkdir -p usr/lib
cd usr/lib
ln -sf ../..%{_prefix}/lib/* .
)

sed "s#/usr/linux/bin#/usr/bin#"  $RPM_BUILD_ROOT/opt/freeware/lib/rpm/macros | sed "s#%._var./tmp#/var/tmp#" >macros.tmp
mv macros.tmp  $RPM_BUILD_ROOT/opt/freeware/lib/rpm/macros

cp $RPM_BUILD_ROOT/opt/freeware/bin/* $RPM_BUILD_ROOT/tmp/bin
cp $RPM_BUILD_ROOT/opt/freeware/lib/librpm* $RPM_BUILD_ROOT/tmp/lib
cp -r $RPM_BUILD_ROOT/opt/freeware/lib/rpm/* $RPM_BUILD_ROOT/tmp/lib/rpm

cp %{_sourcedir}/rpm-4.9.1.3.macros.aix $RPM_BUILD_ROOT%{_prefix}/etc/rpm/macros

cp $RPM_BUILD_ROOT/tmp/lib/librpm*.la $RPM_BUILD_ROOT%{_libdir}


#Install the wrapper script in /usr/bin.
rm -f $RPM_BUILD_ROOT/usr/bin/rpm
cp %{SOURCE1} ${RPM_BUILD_ROOT}/usr/bin/rpm

mkdir -p ${RPM_BUILD_ROOT}/tmp
cp %{SOURCE4} ${RPM_BUILD_ROOT}/tmp

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%pre
echo "\n#####################################################
	Creating virtual packages already installed in your system
	It will be take few minutes ...\n"
# Saving information on existing packages and what they provide before installing new rpm manager
export LIBPATH=%{_libdir}:/usr/lib:${LIBPATH}
export TMPDIR=/tmp/tmprpm
export RPMDIR=${TMPDIR}/rpmdir
[ -e ${RPMDIR} ] || mkdir -p ${RPMDIR}
[ -e ${RPMDIR}/RPMS ] && rm -rf  ${RPMDIR}/RPMS/* || mkdir -p ${RPMDIR}/RPMS
[ -e ${RPMDIR}/SRPMS ] && rm -rf  ${RPMDIR}/SRPMS/* || mkdir -p ${RPMDIR}/SRPMS
export VIRTUALSDIR=${TMPDIR}/virtuals
[ -e ${VIRTUALSDIR} ] && rm -rf ${VIRTUALSDIR}/* || mkdir -p ${VIRTUALSDIR}
export OLDRPMROOTDIR=%{_libdir}/saveoldrpm/oldrpm
[ -e ${OLDRPMROOTDIR} ] && rm -rf ${OLDRPMROOTDIR}/* || mkdir -p ${OLDRPMROOTDIR}
# Before intalling the new rpm package, we save the old rpm files
mkdir -p ${OLDRPMROOTDIR}/bin
mkdir -p ${OLDRPMROOTDIR}/lib
mkdir -p ${OLDRPMROOTDIR}/lib/rpm
mkdir ${OLDRPMROOTDIR}/rpmdb
cp -p %{_prefix}/packages/* ${OLDRPMROOTDIR}/rpmdb
cp -pf %{_bindir}/rpm*  ${OLDRPMROOTDIR}/bin
cp -pf %{_bindir}/gendiff  ${OLDRPMROOTDIR}/bin
#To preserve symbolic links to the libraries, we use find and cpio commands 
cd %{_libdir}
find . -name "librpm*" -print | grep -v saveoldrpm | cpio -pdmu ${OLDRPMROOTDIR}/lib
cp -prf %{_libdir}/rpm/*  ${OLDRPMROOTDIR}/lib/rpm

# We will need to transfer information from the old rpm database to the new one
# To do that we create virtual packages containing information from the old existing rpm packages 
# and we will install them in the new database. 
# So only the information will be transfered; binaries and files will not be modified.
for pac in `/usr/bin/rpm -qa --dbpath ${OLDRPMROOTDIR}/rpmdb`
do

   # Saving rpm info from old rpmdb
   /usr/bin/rpm -q ${pac} --info --dbpath ${OLDRPMROOTDIR}/rpmdb | \
	grep -v "^Install " | \
	sed "/Description/,\$d" | \
	sed "s/Relocations:.*$//;s/Vendor:.*$//;s/Build Date:.*$//;s/Source RPM:.*$//;s/^Size.*License.*:/License:/" \
		> ${VIRTUALSDIR}/mkvirtpkg.${pac}
   # Saving rpm requires from old rpmdb
   /usr/bin/rpm -q ${pac} --requires --dbpath ${OLDRPMROOTDIR}/rpmdb | \
	sed "s/^/Requires: /" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Saving rpm provides from old rpmdb
   /usr/bin/rpm -q ${pac} --provides --dbpath ${OLDRPMROOTDIR}/rpmdb | \
	grep -v "(contains no files)" | \
	sed "s/^/Provides: /" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Saving rpm description from old rpmdb 
   echo "%description" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}
   /usr/bin/rpm -q ${pac} --info --dbpath ${OLDRPMROOTDIR}/rpmdb |  \
	sed "1,/Description/d" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Addig some fake commands block into the spec file
   echo '
#%prep
#%build
#%install
#%clean' | sed "s/#//" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Saving scripts block command from old rpmdb
   rpm -q --scripts --dbpath ${OLDRPMROOTDIR}/rpmdb ${pac} | \
   sed "s;^\(.*\)install script (through /bin/sh):;%\1;" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Creating %files block command into the spec file
   # We do not want to mix our new packages with the client packages
   # so we change _rpmdir and _srcrpmdir location into %file block command
   echo 'files
define _rpmdir /tmp/tmprpm/rpmdir/RPMS
define _srcrpmdir /tmp/tmprpm/rpmdir/SRPMS' | sed "s/^/%/" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}

   # Adding the list of files of the package
   rpm -ql --dbpath ${OLDRPMROOTDIR}/rpmdb ${pac} | grep -v "(contains no files)" | while read item
   do
       if [ -d ${item} ]
       then
           echo ${item} | grep -q "/doc/" ; status=$?
           [ $status -eq 0 ] \
              && echo ${item} | sed "s!^\(.*/doc/.*$\)!%docdir \1!" \
                   >> ${VIRTUALSDIR}/mkvirtpkg.${pac} \
              || echo ${item} | sed "s!^\(.*$\)!%dir \1!" >> ${VIRTUALSDIR}/mkvirtpkg.${pac}
       else
           echo ${item} | grep -q "/doc/" ; status=$?
           [ $status -eq 0 ] \
              && echo ${item} | sed "s!^\(.*/doc/.*$\)!%doc \1!" >> ${VIRTUALSDIR}/mkvirtpkg.${pac} \
              || echo ${item} >> ${VIRTUALSDIR}/mkvirtpkg.${pac}
       fi
   done
done

if [ -s ${VIRTUALSDIR} ]
then
   cd  ${VIRTUALSDIR}
   for f in `ls mkvirtpkg*`
   do
      /usr/bin/rpm -ba ${f} > ${TMPDIR}/${f}.$$.out 2>&1
   done
else
	echo "Error: directory ${VIRTUALSDIR} not found"
	exit 1
fi

if [ "`grep _rpmlock_path /usr/lib/rpm/macros`" = "" ]
then
    echo "%_rpmlock_path  %{_dbpath}/.rpm.lock" >> /usr/lib/rpm/macros
fi

%post
export TMPDIR=/tmp/tmprpm

echo '
export TMPDIR=/tmp/tmprpm
export LIBPATH=%{_libdir}:${LIBPATH}
export RPMDIR=${TMPDIR}/rpmdir

# We do not want to mix our new packages with the users packages
# so we change _rpmdir and _srcrpmdir location into %file block command
export _rpmdir=${RPMDIR}/RPMS
export _srcrpmdir=${RPMDIR}/SRPMS
export VIRTUALSDIR=${TMPDIR}/virtuals
sleep 1
cp /tmp/mkvirtpkg.rpm-4.9.1.3 ${VIRTUALSDIR}
/usr/bin/rpm -ba /tmp/mkvirtpkg.rpm-4.9.1.3 >${TMPDIR}/mkvirtpkg.rpm-4.9.1.3.$$.out 2>&1
slibclean

# The new rpm files have been copied into /tmp/bin and /tmp/lib directories.
# cleaning obsoletes files and copying new rpm files
rm -f %{_libdir}/librpm*
rm -f /usr/lib/librpm*
ListLibRpmOldFiles="brp-redhat
convertrpmrc.sh
cpanflute
find-prov.pl
find-provides.perl
find-req.pl
find-requires.perl
get_magic.pl
getpo.sh
http.req
magic.prov
magic.req
rpmdiff
rpmdiff.cgi
rpmgettext
rpmpopt
rpmputtext
u_pkg.sh
vpkg-provides.sh
vpkg-provides2.sh
"
for file in ${ListLibRpmOldFiles}
do
   rm -f %{_libdir}/rpm/${file}
done
cp -pf /tmp/bin/*  %{_bindir}
#To preserve symbolic links to the libraries, we use find and cpio commands utilities
cd /tmp/lib
find . -name "librpm*" -print | cpio -dpmu %{_libdir}
cd /tmp/lib/rpm
cp * %{_libdir}/rpm
mkdir -p %{_libdir}/rpm/fileattrs
cd /tmp/lib/rpm/fileattrs
cp * %{_libdir}/rpm/fileattrs
cd /usr/lib
ln -s ../..%{_libdir}/librpm* .
/bin/rpm --initdb
[ -e /var/lib ] || mkdir -p /var/lib 2>/dev/null
chmod 755 /var/lib
ln -sf %{_prefix}/packages /var/lib/rpm
rpmdir=`/usr/bin/rpm --eval "%{_rpmdir}"`
# Re-creating the information of the previous package in the new rpm data base without copying files
if [ -s ${VIRTUALSDIR} ]
then
   cd  ${VIRTUALSDIR}
   arch=`LANG=C /usr/bin/rpm --showrc | /usr/bin/grep "^build arch"  | /usr/bin/awk "{print \\\$NF}"`
   os=`LANG=C /usr/bin/rpm --showrc | /usr/bin/grep "^build os"  | /usr/bin/awk "{print \\\$NF}"`
   for f in `ls mkvirtpkg*`
   do
       name=`/usr/bin/grep "^Name" ${f} | /usr/bin/awk "{print \\\$NF}"`
       version=`/usr/bin/grep "^Version" ${f} | /usr/bin/awk "{print \\\$NF}"`
       release=`/usr/bin/grep "^Release" ${f} | /usr/bin/awk "{print \\\$NF}"`
       /usr/bin/rpm -U --justdb --ignoresize --nodeps ${RPMDIR}/RPMS/$arch/$name-$version-$release.$os.$arch.rpm
       if [ $? -ne 0 ]
       then
            /usr/bin/cat ${TMPDIR}/${f}.$$.out
       fi
   done
fi
' > ${TMPDIR}/rpm_install.sh
echo "\n#####################################################
	Rebuilding RPM Data Base ...
	Please wait for rpm_install background job termination
	It will be take few minutes\n"
chmod +x ${TMPDIR}/rpm_install.sh
nohup ${TMPDIR}/rpm_install.sh  2>&1 > /tmp/nohup.log &

%files
# commented files are put under /tmp in order to avoid conflict
# when installing new rpm manager with previous version
%defattr(-,root,system)
%doc COPYING CHANGES GROUPS doc/manual/*
#%{_prefix}/bin/rpm
#%{_prefix}/bin/rpm2cpio
#%{_prefix}/bin/gendiff
#%{_bindir}/rpmquery
#%{_bindir}/rpmverify
#%{_bindir}/rpmbuild
#%{_bindir}/rpmdb
#%{_bindir}/rpmkeys
#%{_bindir}/rpmsign
#%{_bindir}/rpmspec
/tmp/bin/rpm
/tmp/bin/rpm2cpio
/tmp/bin/gendiff
/tmp/bin/rpmquery
/tmp/bin/rpmverify
/tmp/bin/rpmbuild
/tmp/bin/rpmdb
/tmp/bin/rpmkeys
/tmp/mkvirtpkg.rpm-4.9.1.3
/usr/bin/rpm
#/tmp/bin/rpm
/usr/bin/rpm2cpio
/usr/bin/gendiff
/usr/bin/rpmquery
/usr/bin/rpmverify
/usr/bin/rpmbuild
/usr/bin/rpmdb
/usr/bin/rpmkeys
/usr/bin/rpmsign
/usr/bin/rpmspec

%{_mandir}/man1/gendiff.1*
%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpmdb.8*
%{_mandir}/man8/rpmkeys.8*
%{_mandir}/man8/rpm2cpio.8*
%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmsign.8*
%{_mandir}/man8/rpmspec.8*

%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

#%{_libdir}/rpm/*
/tmp/lib/rpm/brp-*
/tmp/lib/rpm/check-*
/tmp/lib/rpm/find-lang.sh
/tmp/lib/rpm/*provides*
/tmp/lib/rpm/*requires*
/tmp/lib/rpm/*deps*
/tmp/lib/rpm/*.prov
/tmp/lib/rpm/*.req
/tmp/lib/rpm/config.*
/tmp/lib/rpm/mkinstalldirs
/tmp/lib/rpm/macros*
/tmp/lib/rpm/fileattrs
/tmp/lib/rpm/rpmpopt*
/tmp/lib/rpm/rpmrc
/tmp/lib/rpm/rpm2cpio.sh
/tmp/lib/rpm/rpm.daily
/tmp/lib/rpm/rpm.log
/tmp/lib/rpm/tgpg
%{_prefix}/etc/rpm/macros*
/usr/lib/rpm


%dir %{_prefix}/src/packages
%dir %{_prefix}/src/packages/BUILD
%dir %{_prefix}/src/packages/SPECS
%dir %{_prefix}/src/packages/SOURCES
%dir %{_prefix}/src/packages/SRPMS
%dir %{_prefix}/src/packages/RPMS
%{_prefix}/src/packages/RPMS/*
%dir /usr/src
%{_prefix}/share/locale/*/LC_MESSAGES/rpm.mo

/tmp/lib/librpm.so*
/tmp/lib/librpmio.so*
/tmp/lib/librpmbuild.so*
/tmp/lib/librpmsign.so*
#%{_prefix}/lib/librpm.so*
#%{_prefix}/lib/librpmio.so*
#%{_prefix}/lib/librpmbuild.so*
#%{_prefix}/lib/librpmsign.so*
/usr/lib/librpm.so*
/usr/lib/librpmio.so*
/usr/lib/librpmbuild.so*
/usr/lib/librpmsign.so*

%files devel
%defattr(-,root,system)
%{_prefix}/lib/rpm-plugins/*
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/include/rpm
%{_prefix}/lib/librpm*.la
/usr/include/rpm

%files devel-python
%defattr(-,root,system)
%{_prefix}/lib/python2.*/*


%changelog
* Tue Jun 4 2013 Bernard Cahen <bernard.cahen@bull.net> 4.9.1.3-2
- Creation of devel-python package
- Modify %post scripts and %files list to make rpm 4.9.1.3 appear in rpm -qa
 
* Thu Jan 31 2013 Bernard Cahen <bernard.cahen@bull.net> 4.9.1.3-1
- Update to version 4.9.1.3

* Mon Nov 15 2010 Sangamesh Mallayya <smallayy@in.ibm.com> 3.0.5-52
- Add security fix CVE-2010-2059

* Thu Jan 21 2010 Reza Arbab <arbab@austin.ibm.com> 3.0.5-50
- Update to accomodate possible future version numbers of AIX.

* Fri Jul 10 2009 Reza Arbab <arbab@austin.ibm.com> 3.0.5-49
- Fix bug where `rpm -i [non-rpm package file]` still returns 0.

* Wed Oct 22 2008 Reza Arbab <arbab@austin.ibm.com> 3.0.5-46
- Fix a bug reported with the --prefix flag.

* Tue Apr 15 2008 Reza Arbab <arbab@austin.ibm.com> 3.0.5-44
- Change the debug variable for find-provides from $DEBUG to $FIND_PROVIDES_DEBUG.
- Use open64/stat64 instead of open/stat.

* Fri Mar 14 2008 Reza Arbab <arbab@austin.ibm.com> 3.0.5-43
- Change %%{_dbpath} from a symlink to the actual directory.
- Tweak source to enable AIX 5.2 build environment.

* Tue Jan  8 2008 Reza Arbab <arbab@austin.ibm.com> 3.0.5-42
- New optimizations for find-provides.
- Add AIX 6.1 support in config.guess.

* Wed Jun  6 2006 Reza Arbab <arbab@austin.ibm.com> 3.0.5-41
- Add "os_compat" lines to rpmrc for possible future AIX releases.
- /usr/bin/rpm is now a wrapper script rather than a symlink.
- find-provides is now fast native code instead of a script

* Mon Apr 17 2006 Reza Arbab <arbab@austin.ibm.com> 3.0.5-38
- Attempt to fix a "space needed" calculation bug on systems with huge filesystems.

* Thu Nov 04 2004 David Clissold <cliss@austin.ibm.com> 3.0.5-37
- Rebuild with a find-provides fix (OBJECT_MODE)
-   While I'm at it, clean up some unused ia64 stuff.

* Mon Jul 02 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix locale references

* Fri Mar 30 2001 Marc Stephenson <marc@austin.ibm.com>
- Disable mntent()-related calls

* Tue Mar 27 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix mode verification comparison

* Sat Mar 24 2001 Marc Stephenson <marc@austin.ibm.com>
- Work in AIX RAM filesystem

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Tue Feb 20 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Fri Oct 27 2000 rpmpkg <rpmpkg@austin.ibm.com>
- Modify for build and installation on AIX 4.3 and 5.1

* Wed Mar  1 2000 Jeff Johnson <jbj@redhat.com>
- fix rpmmodule.so python bindings.

* Sun Feb 27 2000 Jeff Johnson <jbj@redhat.com>
- rpm-3.0.4 release candidate.

* Fri Feb 25 2000 Jeff Johnson <jbj@redhat.com>
- fix: filter excluded paths before adding install prefixes (#8709).
- add i18n lookaside to PO catalogue(s) for i18n strings.
- try for /etc/rpm/macros.specspo so that specspo autoconfigures rpm.
- per-platform configuration factored into /usr/lib/rpm subdir.

* Tue Feb 15 2000 Jeff Johnson <jbj@redhat.com>
- new rpm-build package to isolate rpm dependencies on perl/bash2.
- always remove duplicate identical package entries on --rebuilddb.
- add scripts for autogenerating CPAN dependencies.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- brp-compress deals with hard links correctly.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- brp-compress deals with symlinks correctly.

* Mon Jan 24 2000 Jeff Johnson <jbj@redhat.com>
- explicitly expand file lists in writeRPM for rpmputtext.
