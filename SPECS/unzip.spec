%define _prefix /opt/freeware
%define _defaultdocdir %{_prefix}/doc

Summary: A utility for unpacking zip files.
Name: unzip
Version: 5.50
Release: 3
License: BSD
URL: http://www.ctan.org/tex-archive/tools/zip/info-zip/UnZip.html
Group: Applications/Archiving
Source: ftp://ftp.uu.net/pub/archiving/zip/src/unzip-%{version}.tar.bz2

Patch0:		unzip-5.50-aix.patch

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%define DEFCC cc

%description
The unzip utility is used to list, test, or extract files from a zip
archive.  Zip archives are commonly found on MS-DOS systems.  The zip
utility, included in the zip package, creates zip archives.  Zip and
unzip are both compatible with archives created by PKWARE(R)'s PKZIP
for MS-DOS, but the programs' options and default behaviors do differ
in some respects.

Install the unzip package if you need to list, test or extract files from
a zip archive.

%prep
%setup -q 

if test x$PATCH = x ; then
  PATCH=patch ;
fi
$PATCH -p2 -s < %{_sourcedir}/unzip-5.50-aix.patch


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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

LOCAL_UNZIP="-D_LARGE_FILES" make -f unix/Makefile CC=$CC aix

%install
if test "%{buildroot}" != "/"; then
	rm -rf %{buildroot}
fi

make prefix=$RPM_BUILD_ROOT%{_prefix} install

strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

(cd $RPM_BUILD_ROOT
 mkdir -p usr/bin
 cd usr/bin
 ln -sf ../..%{_prefix}/bin/* .
 cd -
)

%files
%defattr(-,root,root)
%doc README BUGS COPYING.OLD LICENSE INSTALL ToDo WHERE
%{_bindir}/unzip
%{_bindir}/funzip
%{_bindir}/unzipsfx
%{_bindir}/zipgrep
%{_bindir}/zipinfo
/usr/bin/unzip
/usr/bin/funzip
/usr/bin/unzipsfx
/usr/bin/zipgrep
/usr/bin/zipinfo
%{_mandir}/man1/*
%changelog
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
*  Wed May 25 2005  BULL
 - Release  1
 - New version  version: 5.50
