Summary: The GNU patch command, for modifying/upgrading files.
Name: patch
Version: 2.6.1
Release: 1
Copyright: GPL
Url: http://www.gnu.org/software/patch/
Group: Development/Tools
Source: http://ftp.gnu.org/gnu/patch/%{name}-%{version}.tar.gz
Buildroot: /var/tmp/%{name}-root
Prefix: %{_prefix}

%ifarch ia64
  %define DEFCCIA xlc
  %define DEFCC %{DEFCCIA}
%else
  %define DEFCC xlc
%endif

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q

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
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS=$RPM_OPT_FLAGS

./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
make "CFLAGS=$RPM_OPT_FLAGS" LDFLAGS=-s



%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/%{_prefix} \
	mandir=$RPM_BUILD_ROOT/%{_prefix}/man \
	install 

(cd $RPM_BUILD_ROOT
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf ../../..%{_prefix}/bin/* .
)

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS README
%{_prefix}/bin/*
/usr/linux/bin/*
%{_prefix}/man/*/*

%changelog
* Wed May 26 2010 Jean Noel Cordenner <jean-noel.cordenner>
- update to version 2.6.1

* Fri Mar 23 2001 David Clissold <cliss@austin.ibm.com>
- STDC needed -- default compiler to xlc, not cc

* Thu Mar 08 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler
- Rebuild against new shared objects

* Fri Oct 27 2000 rpmpkg <rpmpkg@austin.ibm.com>
- Adapted for AIX Freeware delivery

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Jun 06 1999 Alan Cox <alan@redhat.com> 
- Fix the case where stderr isnt flushed for ask(). Now the 'no such file'
  appears before the skip patch question, not at the very end, Doh!

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- (ultra?) sparc was getting large file system support.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 7)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- bump release to preserve newer than back-ported 4.2.

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- Fix for problem #682 segfault.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- added buildroot

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 2.5

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
