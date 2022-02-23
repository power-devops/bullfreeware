Summary: A tool for creating scanners (text pattern recognizers).
Name: flex
Version: 2.5.4a
Release: 6
License: IBM_ILA
URL: http://www.gnu.org/software/flex/flex.html
Group: Development/Tools
Source: ftp://ftp.gnu.org/gnu/findutils/flex-2.5.4a.tar.gz
Source1: IBM_ILA
Prefix: %{_prefix}
BuildRoot: /var/tmp/%{name}-root

%define DEFCC cc

%description
The flex program generates scanners.  Scanners are programs which can
recognize lexical patterns in text.  Flex takes pairs of regular
expressions and C code as input and generates a C source file as
output.  The output file is compiled and linked with a library to
produce an executable.  The executable searches through its input for
occurrences of the regular expressions.  When a match is found, it
executes the corresponding C code.  Flex was designed to work with
both Yacc and Bison, and is used by many programs as part of their
build process.

You should install flex if you are going to use your system for
application development.

%prep
%setup -q -n flex-2.5.4

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat COPYING >> LICENSE

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

CFLAGS="$CFLAGS" ./configure --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=${RPM_BUILD_ROOT}%{_prefix} install

( cd ${RPM_BUILD_ROOT}
  /usr/bin/strip .%{_prefix}/bin/flex 2>/dev/null || :
  ln -sf flex .%{_prefix}/bin/lex
  ln -s flex.1 .%{_prefix}/man/man1/lex.1
  ln -s flex.1 .%{_prefix}/man/man1/flex++.1
  ln -s libfl.a .%{_prefix}/lib/libl.a
)

(cd $RPM_BUILD_ROOT
 for dir in usr/bin usr/lib usr/linux/bin usr/linux/lib usr/include
 do
    mkdir -p $dir
 done


 cd usr/linux/bin
 ln -sf ../../..%{_prefix}/bin/flex lex
 cd ../lib
 ln -sf ../../..%{_prefix}/lib/libfl.a libl.a
 cd ../../bin
 ln -sf ../..%{_prefix}/bin/flex .
 ln -sf ../..%{_prefix}/bin/flex++ .
 cd ../include
 ln -sf ../..%{_prefix}/include/FlexLexer.h .
 cd ../lib
 ln -sf ../..%{_prefix}/lib/libfl.a .
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc COPYING NEWS README LICENSE
%{_prefix}/bin/lex
%{_prefix}/bin/flex
%{_prefix}/bin/flex++
/usr/linux/bin/lex
/usr/bin/flex
/usr/bin/flex++
%{_prefix}/man/man1/*
%{_prefix}/lib/libl.a
/usr/linux/lib/libl.a
%{_prefix}/lib/libfl.a
%{_prefix}/include/FlexLexer.h
/usr/lib/libfl.a
/usr/include/FlexLexer.h

%changelog
* Thu Jul 10 2003 David Clissold <cliss@austin.ibm.com>
- Build with IBM VAC compiler for better size and performance.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Mar 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Add logic for default compiler

* Wed Feb 28 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Fix minor error in install section of previous patch

* Thu Feb 15 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- add a libl.a link to libfl.a

* Wed Aug 25 1999 Jeff Johnson <jbj@redhat.com>
- avoid uninitialized variable warning (Erez Zadok).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.5.4 to 2.5.4a

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 20 1997 Michael Fulbright <msf@redhat.com>
- Updated to v. 2.5.4
