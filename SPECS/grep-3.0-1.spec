# By default, test are runned. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}
# By default, compiler is gcc. To compile with xlc : --define 'gcc_compiler=0'
#%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler:%define gcc_compiler 1}
#By default, 64bit mode
%{!?default_bits: %define default_bits 64}

%{!?optimize:%define optimize 2}

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 3.0
Release: 1
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep//grep-%{version}.tar.xz
Source1: %{name}-%{version}-%{release}.build.log
#useless in 3.0 Patch0: %{name}-3.0-en_US.UTF-8_tests.patch
#useless in 3.0 Patch1: %{name}-3.0-en_US.UTF-8_others.patch
URL: http://www.gnu.org/software/grep

BuildRequires: texinfo
BuildRequires: pkg-config
Prereq: /sbin/install-info

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix: %{_prefix}

#%define _libdir64 %{_prefix}/lib64

%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU s grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.

%if %{gcc_compiler} == 1
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
echo "optimize=%{optimize}"
echo "default_bits=%{default_bits}"

%setup -q
# These 2 patches are designed for handling en_US.UTF8 which is EN_US.UTF8 on AIX
# Patches are not applied since it makes (only) 1 test fail (surrogate-pair) in tests directory
#  (same result for gnulib-tests directory)
# Without patches:
## TOTAL: 143
## PASS:  122
## SKIP:  20
## XFAIL: 0
## FAIL:  1
## XPASS: 0
## ERROR: 0
# With patches: unknow for 3.0
 # TOTAL: 95
 # PASS:  70
 # SKIP:  22
 # XFAIL: 2
 # FAIL:  1 surrogate-pair
#%patch0 -p1 -b .en_US.UTF-8_tests
#%patch1 -p1 -b .en_US.UTF-8_others

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

echo "BUILD ENVIRONMENT:"
/usr/bin/env | /usr/bin/sort

# save script for debugging
cp $0 %{name}-%{version}_script_build.ksh

export AR="/usr/bin/ar "
export NM="/usr/bin/nm -X32_64"
export MAKE="/opt/freeware/bin/gmake --trace"
#export MAKE="/opt/freeware/bin/gmake"
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
export GLOBAL_CC_OPTIONS="$RPM_OPT_FLAGS -O%{optimize} -D_LARGE_FILES"

# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"
export CXX__="/usr/vacpp/bin/xlC"
export FLAG32="-q32"
export FLAG64="-q64"
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"


# build on 32bit mode
cd 32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"\
      ./configure \
      --prefix=%{_prefix} \
      --libdir=%{_libdir} \
      --libexecdir=%{_libdir}

$MAKE

if [ "%{dotests}" == 1 ]
then
    $MAKE -k check || true
fi

cd ..


# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" \
 ./configure \
      --prefix=%{_prefix} \
      --libdir=%{_libdir} \
      --libexecdir=%{_libdir}
      
#$MAKE  CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"  LDFLAGS=-s
$MAKE  CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES"

if [ "%{dotests}" == 1 ]
then
    $MAKE -k check || true
fi

cd ..


%install
export AR="/usr/bin/ar "

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#export MAKE="gmake --trace"
export MAKE="gmake"


# install on 64bit mode
cd 64bit

# Files grep.info.gz and man1 are built at:
#	 $RPM_BUILD_ROOT%{prefix}/share
# though our grep-2.6.3-4.spec file expects them at:
#	 $RPM_BUILD_ROOT%{prefix}/
# Don't know why.
# Anyway, IBM grep-2.20-1.spec expects them at .../share .
# So do I now. Adding /share before /info and /man here below.

$MAKE DESTDIR=${RPM_BUILD_ROOT} \
	prefix=%{_prefix} \
	exec_prefix=%{prefix} \
	infodir=%{prefix}/info \
	mandir=%{prefix}/man \
	install

#echo $RPM_BUILD_ROOT%{prefix}/info/grep*
gzip -9f $RPM_BUILD_ROOT%{prefix}/info/grep*
mv  $RPM_BUILD_ROOT%{prefix}/info  $RPM_BUILD_ROOT%{prefix}/info64



(
    cd  ${RPM_BUILD_ROOT}/%{prefix}/bin
    /usr/bin/strip -X64 grep
    for fic in $(ls -1| /usr/bin/grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)
cd -
# Fin install on 64bit mode



# install on 32bit mode
cd 32bit

# Files grep.info.gz and man1 are built at:
#	 $RPM_BUILD_ROOT%{prefix}/share
# though our grep-2.6.3-4.spec file expects them at:
#	 $RPM_BUILD_ROOT%{prefix}/
# Don't know why.
# Anyway, IBM grep-2.20-1.spec expects them at .../share .
# So do I now. Adding /share before /info and /man here below.

$MAKE DESTDIR=${RPM_BUILD_ROOT} \
	prefix=%{_prefix} \
	exec_prefix=%{prefix} \
	infodir=%{prefix}/info \
	mandir=%{prefix}/man \
	install

#echo $RPM_BUILD_ROOT%{prefix}/info/grep*
gzip -9f $RPM_BUILD_ROOT%{prefix}/info/grep*


(
    cd  ${RPM_BUILD_ROOT}/%{prefix}/bin
    /usr/bin/strip -X32 grep
    for fic in $(ls -1| /usr/bin/grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)
cd -
# Fin install on 32bit mode



(
    mkdir -p $RPM_BUILD_ROOT/usr/linux/bin
    cd $RPM_BUILD_ROOT/usr/linux/bin
    ln -sf ../../..%{_prefix}/bin/* .
)



%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info --quiet --info-dir=%{_prefix}/info %{_prefix}/info/grep.info.gz

%preun
if [ $1 = 0 ]; then
        /sbin/install-info --quiet --info-dir=%{_prefix}/info --delete %{_prefix}/info/grep.info.gz
fi

%files
%defattr(-,root,root)
%doc 32bit/ABOUT-NLS 32bit/AUTHORS 32bit/THANKS 32bit/TODO 32bit/NEWS 32bit/README 32bit/COPYING 32bit/ChangeLog

%{_prefix}/bin/*
/usr/linux/bin/*
%{_prefix}/info/*.info.gz
%{_prefix}/man/*/*
%{_prefix}/share/locale/*/*/grep.*

%changelog
* Wed Jun 28 2017 Daniele Silvestre <daniele.silvestre@atos.net> 3.0-1
- Update to 3.0
- Add texinfo BuildRequires
- Add pkg-config BuildRequires
- remove useless --disable-perl-regexp option in configure => 9 additional succesful PCRE tests

* Tue Nov 22 2016 Jean Girardet <jean.girardet@atos.net> 2.26-2
- Correction of links for binary files

* Tue Nov 15 2016 Jean Girardet <jean.girardet@atos.net> 2.26-1
- Third port on AIX 6.1 , add the 64 bits version

* Fri Jan 08 2016 Tony Reix <tony.reix@bull.net> 2.22-2
- Second port on AIX 6.1

* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.3-4
- Initial port on Aix6.1

* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 2.6.3-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 08 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.6.3-2
- Compile on toolbox3

* Fri May 28 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.6.3
- Update to 2.6.3

* Wed May 07 2003 David Clissold <cliss@austin.ibm.com>
- Update to 2.5.1.
- Patch from last entry now in main code, so not needed.

* Fri Jul 06 2001 David Clissold <cliss@austin.ibm.com>
- Add patch to fix problem with "grep -r" not working.

* Tue Apr 10 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix path to install-info in preun

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb 03 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- gzip info pages (Bug #9035)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.4.

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- prereq install-info

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %post/%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
