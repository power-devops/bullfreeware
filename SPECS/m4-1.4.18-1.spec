%bcond_without dotests

Summary: The GNU macro processor.
Name: m4
Version: 1.4.18
Release: 1
License: GPLv3+
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source100: %{name}-%{version}-%{release}.build.log
URL: http://www.gnu.org/software/m4

Patch1: m4-1.4.18-Werror.patch

BuildRequires: help2man
Requires: help2man

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q

%patch1 -p1 -b .werror

#Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/


%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/ar -X32_64"

build_m4 () {
# For Wabi error
export CFLAGS=" -fabi-version=10 "
./configure	--prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-largefile

gmake %{?_smp_mflags}
}

#First build 64bit version
cd 64bit
export CC="gcc -maix64 -D_LARGE_FILES"
export LDFLAGS=" -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=64
build_m4

#Now build 32bit version
cd ../32bit

export CC="gcc -maix32 -D_LARGE_FILES"
export LDFLAGS=" -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib"
export OBJECT_MODE=32
build_m4


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"

install_m4 () {
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  mv m4 m4_$1
)
}

#install the 64bit version
cd 64bit
export OBJECT_MODE=64
install_m4 64

#install the 32bit version
cd ../32bit
export OBJECT_MODE=32
install_m4 32

# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  ln -sf m4_64 m4
)

gzip -9fn $RPM_BUILD_ROOT%{_infodir}/%{name}*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%check
%if %{with dotests}
cd 64bit
(gmake -k check || true)
cd ../32bit
(gmake -k check || true)
%endif


%post
    if [ -s /etc/info-dir ] && [ ! -L /opt/freeware/info/dir ]; then
    ln -sf /etc/info-dir /opt/freeware/info/dir
    fi 
    /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/NEWS 32bit/README 32bit/COPYING 32bit/THANKS 32bit/INSTALL 32bit/TODO
%{_bindir}/*
%{_infodir}/*
%{_mandir}/man1/*


%changelog
* Tue Feb 25 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 1.4.18-1
- New version 1.4.18
- Adapt to RPM v4.

* Tue Jan 31 2017 M Sushma Bhat <susmbhat@in.ibm.com> 1.4.17-1
- Update to version 1.4.17.$
- Built both 32bit and 64bit version.64bit binary made default executable.

* Tue Oct 22 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.4.17-1
- Update to version  1.4.17

* Fri Jul 26 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.4.16-2
- Fix conflit %{_infodir}/dir with package "info" 

* Thu Jan 26 2012 Patricia Cugny <patricia.cugny@bull.net> 1.4.16-1
- Update to version  1.4.16

* Mon Feb 28 2011 Patricia Cugny <patricia.cugny@bull.net> 1.4.15-1
- Update to version  1.4.15

* Fri Apr 23 2010 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.4.14-1
- Update to version  1.4.14

* Mon Jun 22 2009 Jean noel Cordenner <jean-noel.cordenner@bull.net> 1.4.13-1
- Update to version  1.4.13

* Wed Mar 26 2003 David Clissold <cliss@austin.ibm.com>
- Rebuild using IBM VAC compiler.

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

