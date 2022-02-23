#
# lsof_4.89 spec file
#
# Built incrementally to debug

Name: lsof
Summary: A tool that lists open files and sockets
Version: 4.89
Release: 2
License: IBM_ILA
Group: Development/Debuggers
Source0: ftp://vic.cc.purdue.edu/pub/tools/unix/lsof/lsof_%{version}.tar.bz2
Source1: %{name}_%{version}.IBM_ILA

Patch0: %{name}_%{version}-test.patch

# Not used. Kept if needed in future.
Patch1: %{name}_%{version}-check64kern.patch


Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}
%define DEFAULT_COMPILER cc


%description
Lsof stands for LiSt Open Files, and it does just that: it lists
information about files that are open by the processes running on a
UNIX system.

%prep
%setup -q -n lsof_%{version}

[ -f lsof_%{version}_src.tar ] && tar xf lsof_%{version}_src.tar
[ -d lsof_%{version}_src.linux -a ! -d lsof_%{version_src} ] && \
        mv lsof_%{version}_src.linux lsof_%{version}_src
[ -d lsof_%{version}_src ] && cd lsof_%{version}_src

%patch0 -p1 -b .test

# Put License into place
cat %{SOURCE1} > LICENSE
echo "See file 00DIST for more information." >> LICENSE


%build
#export PATH=/usr/bin:/opt/freeware/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export PATH=/usr/bin:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export AR="/usr/bin/ar -X32_64"

# if CC undefined set to default compiler - %DEFCC

if [[ -z "$CC" ]]
then
    export CC=%{DEFAULT_COMPILER}
fi

# Ensure that we have a compiler
compiler_path=$(which ${CC} 2>/dev/null)

if [[ ! -x "$compiler_path" ]]
then
    echo "Can't find compiler: ${CC}. Set CC and retry"
    exit -1
fi


# Set the appropriate compiler options

echo "Compiler: $CC"

if  [[ "$CC" == "gcc" ]]
then
    export bld_target=aixgcc
    export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
    export CFLAGS="$RPM_OPT_FLAGS"
else
    export bld_target=aix
    xlc -qversion
fi

# Run the configure command in the source directory
[ -d lsof_%{version}_src ] && cd lsof_%{version}_src
# -DLT_BIGF : see: 00TEST :
#	G.2. LTbigf, Test Sizes and Offsets for Large (> 32 bit) Files
# 	Requires ulimit file block "unlimited"
#	cd tests ; ./LTbigf -p /tmp/HH
ulimit -f unlimited
./Configure -n $bld_target

gmake

cd tests
(make all || true)
(make opt || true)


%install

# Clean build dir
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# The Makefile doesn't provide an "install" target - got to roll our own

[ -d lsof_%{version}_src ] && cd lsof_%{version}_src

# Install and strip binary (strip seperately because of -X64)
# See Makefile for other installation options
#
install -d ${RPM_BUILD_ROOT}%{prefix}/sbin
install lsof ${RPM_BUILD_ROOT}%{prefix}/sbin
strip -X64 ${RPM_BUILD_ROOT}%{prefix}/sbin/lsof

# Install man pages
install -d ${RPM_BUILD_ROOT}%{prefix}/man/man8
install lsof.8 ${RPM_BUILD_ROOT}%{prefix}/man/man8/

# link to RPM_BUILD_ROOT (why all this jumping through hoops?)
# Binary
mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
cd ${RPM_BUILD_ROOT}/usr/sbin
ln -sf ../..%{prefix}/sbin/lsof .

# Manpages
mkdir -p ${RPM_BUILD_ROOT}/usr/man/man8
cd ${RPM_BUILD_ROOT}/usr/man/man8
ln -sf ../../..%{prefix}/man/man8/* .


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,system,755)
%doc lsof_%{version}_src/00* lsof_%{version}_src/LICENSE
%attr(2755,root,system) %{prefix}/sbin/lsof
%{prefix}/man/man8/lsof.8*
/usr/man/man8/lsof.8*
/usr/sbin/lsof



%changelog
* Mon Apr 11 2016 Tony Reix <tony.reix@atos.net> - 4.89-2
- Improve .spec file for better portability

* Wed Mar 30 2016 Jez Wain <jezwain@us.ibm.com> - 4.89-1
- Build only 64-bit kernel version 
- Tidied up the compiler checking code
- Update to version 4.89

* Tue Feb 11 2003 David Clissold <cliss@austin.ibm.com>
- On AIX5, Make lsof check the kernel size at startup to ensure
- we are running a 32-bit kernel; if not, exec the lsof64
- binary.  That way, user can just run 'lsof' for either case.

* Mon Sep 09 2002 David Clissold <cliss@austin.ibm.com>
- For AIX 5, add lsof64 (build from the same source on a 5.1
- system with a 64-bit kernel).  Added as a source.
- Ideally, the source is built on the system where it will be run.
- Adding the 64bit version as a source and then building the rpm
- on a 32-bit system allows us to make one package with both versions.
- Run "lsof" if on a 32-bit system, or "lsof64" if on a 64-bit system.

* Wed May 29 2002 David Clissold <cliss@austin.ibm.com>
- Update to Version 4.61

* Tue Aug 14 2001 David Clissold <cliss@austin.ibm.com>
- Update to Version 4.57

* Wed May 23 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 4.56

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Use default compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution
- Adapted from RedHat lsof-4.47-2
- Contributors: Christian Gafton <gafton@redhat.com>
-               Jeff Johnson <jbj@redhat.com>
-               Preston Brown <pbrown@redhat.com>
-               Maciej Lesniewski <nimir@kis.p.lodz.pl>

