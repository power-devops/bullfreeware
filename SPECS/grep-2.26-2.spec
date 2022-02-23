# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}
# compiler defauft gcc
# To use xlc : --define 'gcc_compiler=0'

%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler:%define gcc_compiler 1}

%{!?optimize:%define optimize 2}


# RAF : versions 64 bits  %files %doc, liens, binaires, include, libraires fuxion libraires dybamiques ...


Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: 2.26
Release: 2
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.gnu.org/gnu/grep//grep-%{version}.tar.xz
Source1: %{name}-%{version}-%{release}.build.log
Patch0: %{name}-2.26-en_US.UTF-8_tests.patch
Patch1: %{name}-2.26-en_US.UTF-8_others.patch
URL: http://www.gnu.org/software/grep
Prefix: %{_prefix}
Prereq: /sbin/install-info
Buildroot: /var/tmp/grep-root

%define DEFCC cc
%define _libdir64 %{_prefix}/lib64

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

%setup -q
# These 2 patches are designed for handling en_US.UTF8 which is EN_US.UTF8 on AIX
# Patches are not applied since it makes (only) 1 test fail (surrogate-pair) in tests directory
#  (same result for gnulib-tests directory)
# Without patches:
 # TOTAL: 95
 # PASS:  53
 # SKIP:  41
 # XFAIL: 1
 # FAIL:  0
# With patches:
 # TOTAL: 95
 # PASS:  70
 # SKIP:  22
 # XFAIL: 2
 # FAIL:  1 surrogate-pair
%patch0 -p1 -b .en_US.UTF-8_tests
%patch1 -p1 -b .en_US.UTF-8_others

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit



%build
export MAKE="gmake --trace"

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

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"


# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"
export LIBPATH="/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib64:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib64"

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

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s \
      ./configure --prefix=%{_prefix} --disable-perl-regexp \
      --libdir=%{_libdir64} \
      --libexecdir=%{_libdir64}
      
$MAKE  CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s

if [ "%{dotests}" == 1 ]
then
    $MAKE -k check || true
fi

cd ..

# build on 32bit mode
cd 32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export LIBPATH="/opt/freeware/lib:/usr/lib:/lib"
export LD_LIBRARY_PATH="/opt/freeware/lib:/usr/lib:/lib"
export LDFLAGS="-L/opt/freeware/lib"

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

CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s \
      ./configure --prefix=%{_prefix} --disable-perl-regexp \
      --libdir=%{_libdir} \
      --libexecdir=%{_libdir}

$MAKE  CFLAGS="$RPM_OPT_FLAGS -D_LARGE_FILES" LDFLAGS=-s

if [ "%{dotests}" == 1 ]
then
    $MAKE -k check || true
fi

cd ..



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export MAKE="gmake --trace"


# install on 64bit mode
cd 64bit

# Files grep.info.gz and man1 are built at:
#	 $RPM_BUILD_ROOT%{prefix}/share
# though our grep-2.6.3-4.spec file expects them at:
#	 $RPM_BUILD_ROOT%{prefix}/
# Don't know why.
# Anyway, IBM grep-2.20-1.spec expects them at .../share .
# So do I now. Adding /share before /info and /man here below.

$MAKE LDFLAGS=-s DESTDIR=${RPM_BUILD_ROOT} \
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
    for fic in $(ls -1| grep -v -e _32 -e _64)
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

$MAKE LDFLAGS=-s DESTDIR=${RPM_BUILD_ROOT} \
	prefix=%{_prefix} \
	exec_prefix=%{prefix} \
	infodir=%{prefix}/info \
	mandir=%{prefix}/man \
	install

#echo $RPM_BUILD_ROOT%{prefix}/info/grep*
gzip -9f $RPM_BUILD_ROOT%{prefix}/info/grep*


(
    cd  ${RPM_BUILD_ROOT}/%{prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
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
