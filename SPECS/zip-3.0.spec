Summary: A file compression and packaging utility compatible with PKZIP
Name: 		zip
Version: 	3.0
Release: 	1
License: 	BSD-like
Group: 		Archiving/Compression
URL: 		http://www.info-zip.org/pub/infozip/
Source0: 	http://dfn.dl.sourceforge.net/sourceforge/infozip/%{name}30.tar.gz
Prefix: 	%{_prefix}
BuildRequires: 	bzip2
BuildRoot: 	%{_tmppath}/%{name}-root

%description
The zip program is a compression and file packaging utility. Zip is analogous
to a combination of the UNIX tar and compress commands and is compatible with
PKZIP (a compression and file packaging utility for MS-DOS systems).

Install the zip package if you need to compress files using the zip program.

This version support crypto encryption.

%prep

%setup -q -n %{name}30

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

export TARGET=generic_gcc

if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
       export TARGET=generic
fi

make -f unix/Makefile prefix=%{_prefix} "RPM_OPT_FLAGS=$RPM_OPT_FLAGS" $TARGET

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/man/man1

make -f unix/Makefile prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{prefix}/man \
	infodir=${RPM_BUILD_ROOT}%{prefix}/info \
	install

(
    cd $RPM_BUILD_ROOT
    for n in zipnote zipsplit zip zipcloak ; do
        /usr/bin/strip .%{_prefix}/bin/$n 2>/dev/null || :
        chmod 755 .%{_prefix}/bin/$n
    done

    mkdir -p usr/bin
    cd usr/bin
    ln -sf ../..%{_prefix}/bin/* .
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE README BUGS CHANGES TODO WHATSNEW WHERE
%{_prefix}/bin/zipnote
%{_prefix}/bin/zipsplit
%{_prefix}/bin/zip
%{_prefix}/bin/zipcloak
/usr/bin/zipnote
/usr/bin/zipsplit
/usr/bin/zip
/usr/bin/zipcloak
%{_prefix}/man/man1/zip*.1*

%changelog
* Fri Jun 4 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net>
- Update to version 3.0

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Fri Aug 31 2001 David Clissold <cliss@austin.ibm.com>
- Build with _LARGE_FILES

* Wed Mar 21 2001 David Clissold <cliss@austin.ibm.com>
- Change to allow build with non-gcc compiler

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- fix some perms

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan 11 2000 Bill Nottingham <notting@redhat.com>
- update to 2.3

* Fri Jul 30 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- updated text in the spec file

* Fri Jan 15 1999 Cristian Gafton <gafton@redhat.com>
- patch top build on the arm

* Mon Dec 21 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Mon Aug 10 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
