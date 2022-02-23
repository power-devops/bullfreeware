# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A GNU stream text editor.
Name: sed
Version: 4.8
Release: 1
License: GPLv3+
Group: Applications/Text
URL: http://www.gnu.org/software/sed
Source0: https://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.xz
Source1: %{name}-%{version}-%{release}.build.log

Patch0: sed-4.7-sed-dont_close_twice.patch
Prefix: %{_prefix}
# Buildroot: /var/tmp/%{name}-root

BuildRequires: gettext-devel

%define DEFCC cc

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive) editor.
Sed takes text as input, performs an operation or set of operations on the text
and outputs the modified text.  The operations that sed performs
(substitutions, deletions, insertions, etc.) can be specified in a script file
or from the command line.

%prep

# Does not work
#export TAR=/opt/freeware/bin/tar
export PATH=/opt/freeware/bin:$PATH
%setup -q

%patch0

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


#first build the 64bit version
cd 64bit

export CC="gcc -maix64 -D_LARGE_FILES"
export OBJECT_MODE=64
export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-s -lpthreads -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


%configure --without-libintl-prefix

# %%configure  --prefix=$RPM_BUILD_ROOT  --exec-prefix=%{_prefix}
# Why run configure twice ?
# ./configure --exec-prefix=%{_prefix} --prefix=$RPM_BUILD_ROOT

gmake

# ( gmake -k check || true )


#Now build the 32bit version
cd ../32bit

export CC="gcc -maix32 -D_LARGE_FILES"
export OBJECT_MODE=32
export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-s -lpthreads -Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"


%configure --without-libintl-prefix

# %%configure  --prefix=$RPM_BUILD_ROOT  --exec-prefix=%{_prefix}
# Why run configure twice ?
# ./configure --exec-prefix=%{_prefix} --prefix=$RPM_BUILD_ROOT

gmake

# ( gmake -k check || true )


%install

rm -rf $RPM_BUILD_ROOT

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64

# Not sure why all this, but sed gets installed to /opt/freeware/bin on laurel2
# because no DESTDIR - strange
# gmake prefix=$RPM_BUILD_ROOT/%{_prefix} \
#      exec_prefix=$RPM_BUILD_ROOT/%{_prefix} \
#      infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
#      mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
#      install

gmake DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in *
  do
    mv ${f} ${f}_64
  done
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32

# Not sure why all this, but sed gets installed to /opt/freeware/bin on laurel2
# because no DESTDIR - strange
# make prefix=$RPM_BUILD_ROOT/%{_prefix} \
#      exec_prefix=$RPM_BUILD_ROOT/%{_prefix} \
#      infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
#      mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
#      install

gmake DESTDIR=$RPM_BUILD_ROOT install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in sed
  do
    mv ${f} ${f}_32
  done
)

# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in sed
  do
    ln -sf ${f}_64 ${f}
  done
)

( cd $RPM_BUILD_ROOT
  mkdir -p usr/linux/bin
  ln -sf ../../..%{_prefix}/bin/sed usr/linux/bin/sed
  gzip -9nf .%{_prefix}/info/sed.info*
  rm -f .%{_prefix}/info/dir
)


%check

%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)



%post
/sbin/install-info %{_prefix}/info/sed.info.gz %{_prefix}/info/dir


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/sed.info.gz %{_prefix}/info/dir
fi


%clean 

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/BUGS 32bit/COPYING 32bit/NEWS 32bit/README 32bit/THANKS
%{_prefix}/bin/sed*
# /usr/linux/bin/sed*
%{_prefix}/info/sed.info*
%{_prefix}/man/man1/*


%changelog
* Thu Jun 25 2020 Michael Wilson  <michael.a.wilsont@atos.net> 4.8-1
- Update to version 4.8
- Corrects to strange configure commands and include --without-libintl-prefix
- Make install missing DESTDIR
- Add BuildRequires: gettext-devel for autobuild
- Move tests to %check section, remove /usr links, remove BuildRoot, ...

* Mon Mar 04 2019 Tony Reix <tony.reix@atos.net> 4.7-2
- Add 64 & 32bit build

* Mon Mar 04 2019 Tony Reix <tony.reix@atos.net> 4.7-1
- Initial port on AIX 6.1

* Wed Feb 01 2012 Gerard Visiedo <gerard.visiedo@bull.net> 4.2.1-4
- Initial port on Aix6.1

* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 4.2.1-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jun 8 2011 Gerard Visiedo <gerard.visiedo@bull.net> 4.2.1-2
- Compil on toolbox3

* Wed Jun 2 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 4.2.1
- Update to 4.2.1

* Fri May 20 2005 David Clissold <cliss@austin.ibm.com> 4.1.1-1
- Update to 4.1.1

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 4.0.7-1
- Update to 4.0.7

* Wed Mar 26 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM VAC compiler.

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Tue Jan 18 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild with glibc 2.1.3 to fix an mmap64 bug in sys/mman.h

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Tue Aug 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.02

* Sun Jul 26 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.01

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- removed references to the -g option from the man page that we add

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
