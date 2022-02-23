Summary: A GNU stream text editor.
Name: sed
Version: 4.2.1
Release: 1
Copyright: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/sed
Source0: ftp://ftp.gnu.org/gnu/sed/sed-%{version}.tar.bz2
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root
%define DEFCC cc

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive) editor.
Sed takes text as input, performs an operation or set of operations on the text
and outputs the modified text.  The operations that sed performs
(substitutions, deletions, insertions, etc.) can be specified in a script file
or from the command line.

%prep
%setup -q

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
fi
export CFLAGS=$RPM_OPT_FLAGS

%configure --exec-prefix=%{_prefix}
./configure --exec-prefix=%{_prefix} --prefix=$RPM_BUILD_ROOT
make LDFLAGS=-s CFLAGS=-D_LARGE_FILES

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/%{_prefix} \
     exec_prefix=$RPM_BUILD_ROOT/%{_prefix} \
     infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
     mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
     install

( cd $RPM_BUILD_ROOT
  mkdir -p usr/linux/bin
  ln -sf ../../..%{_prefix}/bin/sed usr/linux/bin/sed
  gzip -9nf .%{_prefix}/info/sed.info*
  rm -f .%{_prefix}/info/dir
)

%post
/sbin/install-info %{_prefix}/info/sed.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/sed.info.gz %{_prefix}/info/dir
fi

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc AUTHORS BUGS COPYING NEWS README THANKS
%{_prefix}/bin/sed
/usr/linux/bin/sed 
%{_prefix}/info/sed.info*
%{_prefix}/man/man1/*

%changelog
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
