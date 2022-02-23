%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: The GNU version of the awk text processing utility.
Name: gawk
Version: 5.0.1
Release: 1
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/gawk
Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz.sig
Source100: %{name}-%{version}-%{release}.build.log

BuildRequires: gettext-devel
BuildRequires: libsigsegv-devel >= 2.7-1
BuildRequires: readline-devel >= 5.2-3
Requires: gettext
Requires: libsigsegv >= 2.7-1
Requires: readline >= 5.2-3
Requires: /sbin/install-info

%define DEFCC gcc

%description
The gawk package contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard tool for processing text.


%prep
%setup -q
#%patch0 -p1 -b .aixconf

rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


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

# An issue appeared with version 4.1.4 vs version 4.0.0 :
#   When using /usr/vac/bin/xlc_r or xlc , now all tests are : (core dumped)
#   When using /usr/bin/cc               , tests works !
# The issue started to appear within version 4.1.0 or 4.1.1 .
# The issue is related to gawk code being now not 100% ANSI.
# Thus, since xlc adds -qansi by default, -O2 tries optimizations based on the fact that the code is ANSI.
# Temporary solution: say to xlc to NOT expect the code to be ANSI when doing optimizations
# export CC="/usr/vac/bin/xlc -qalias=noansi"

if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi


export PATH=/opt/freeware/bin:/usr/bin
export AR="/usr/bin/ar -X32_64"

build_gawk () {
set -ex
./configure --prefix=%{_prefix} \
--mandir=%{_mandir} \
--infodir=%{_infodir} \
--libdir=$1

gmake
}

cd 64bit
export OBJECT_MODE=64
export CFLAGS="-O2 -D_LARGE_FILES -maix64"
export LDFLAGS="-Wl,-bnoipath -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
build_gawk %{_libdir64}

cd ../32bit
export OBJECT_MODE=32
export CFLAGS="-O2 -D_LARGE_FILES -maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-bnoipath -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
build_gawk %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:/usr/bin
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  for loc in %{_bindir} %{_prefix}/libexec/awk
  do
    cd ${RPM_BUILD_ROOT}"$loc"
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
      mv $fic "$fic"_64
    done
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  for loc in %{_bindir} %{_prefix}/libexec/awk
    do
    cd ${RPM_BUILD_ROOT}"$loc"
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
      mv $fic "$fic"_32
      ln -sf "$fic"_64 $fic
    done
  done
)


ln -sf gawk.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/awk.1

(
  cd ${RPM_BUILD_ROOT}
  gzip -9nf .%{_infodir}/gawk.info*
  gzip -9nf .%{_infodir}/gawkinet.info*
)

(
  cd ${RPM_BUILD_ROOT}%{_libdir}/gawk
  for fic in `ls *.a`
    do
    $AR -x ../../lib64/gawk/"$fic"
    $AR -qc $fic `basename $fic .a`.so
  done
  cd ${RPM_BUILD_ROOT}%{_libdir64}/gawk
  ln -sf ../../lib/gawk/*.a .
)


%check
# Some tests fail with a non UTF-8 locale.
# Some others fail with a non C locale.
# Test both, and check results.
%if %{with dotests}
cd 64bit
export OBJECT_MODE=64
export LIBPATH=`pwd`/extension/.libs:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib
(GAWKLOCALE=C           gmake -k check || true)
(GAWKLOCALE=EN_US.UTF-8 gmake -k check || true)

cd ../32bit
export OBJECT_MODE=32
export LIBPATH=`pwd`/extension/.libs:/opt/freeware/lib:/usr/lib
(GAWKLOCALE=C           gmake -k check || true)
(GAWKLOCALE=EN_US.UTF-8 gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_infodir}/gawk.info.gz %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gawkinet.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/gawk.info.gz %{_infodir}/dir || :
   /sbin/install-info --delete %{_infodir}/gawkinet.info.gz %{_infodir}/dir || :
fi


%files
%defattr(-,root,system)
%doc 64bit/ABOUT-NLS 64bit/AUTHORS
%doc 64bit/README 64bit/COPYING 64bit/INSTALL 64bit/NEWS
%doc 64bit/README_d 64bit/POSIX.STD
%dir %{_prefix}/share/awk
%dir %{_prefix}/libexec/awk
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/gawk*info*
%{_prefix}/libexec/awk/*
%{_datadir}/awk/*
%{_datadir}/locale/*/LC_MESSAGES/*
%{_libdir}/gawk/*.a
%{_libdir64}/gawk/*.a


%changelog
* Fri Apr 10 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 5.0.1-1
- New version 5.0.1

* Thu Apr 09 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 4.1.4-3
- Add 64 bit support
- Add check section
- No more provide link to /usr
- Provides librairies

* Tue Oct 25 2016 Tony Reix <tony.reix@bull.net> 4.1.4-2
- Use -qalias=noansi in order to have correct optimizations.

* Thu Oct 20 2016 Tony Reix <tony.reix@bull.net> 4.1.4-1
- Initial port on AIX 6.1
- Need to use /usr/bin/cc !!!

* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> 4.0.0-2
- Initial port on Aix6.1

* Mon Oct 3 2011 Patricia Cugny <patricia.cugny@bull.net> 4.0.0-1
- Update to version 4.0.0

* Thu May 27 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 3.1.8
- Update to version 3.1.8

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 3.1.3-1
- Update to version 3.1.3

* Thu Aug 15 2002 David Clissold <cliss@austin.ibm.com>
- packaging bug with libexec dir; symlinking to nowhere. Rel 2

* Wed Jun 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 3.1.0

* Thu Apr 19 2001 David Clissold <cliss@austin.ibm.com>
- Binaries weren't being stripped correctly

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Rebuild against new shared objects
- Use default compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix man page symlinks
- Fix description
- Fix download URL

* Wed Jun 30 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.0.4.

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

