Summary: The GNU macro processor.
Name: m4
Version: 1.4.1
Release: 1
License: GPL
Group: Applications/Text
URL: http://www.gnu.org/software/m4
Source: ftp://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Buildroot: /var/tmp/m4-root
Prefix: %{_prefix}
%define DEFCC xlc

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is useful for
writing text files which can be logically parsed, and is used by many programs
as part of their build process.  M4 has built-in functions for including files,
running shell commands, doing arithmetic, etc.  The autoconf program needs m4
for generating configure scripts, but not for running configure scripts.

%prep
rm -rf $RPM_BUILD_ROOT

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

./configure
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}
make install
gzip -9fn $RPM_BUILD_ROOT%{_prefix}/info/*
[[ ! -d $RPM_BUILD_ROOT/usr/linux/bin ]] && mkdir -p $RPM_BUILD_ROOT/usr/linux/bin
ln -sf ../../..%{_prefix}/bin/m4 $RPM_BUILD_ROOT/usr/linux/bin/m4

%files
%defattr(-,root,root)
%doc NEWS README COPYING THANKS INSTALL TODO
%{_prefix}/bin/m4
%{_prefix}/info/*
/usr/linux/bin/m4

%post
/sbin/install-info %{_prefix}/info/m4.info.gz %{_prefix}/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/m4.info.gz %{_prefix}/info/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 10 2004 David Clissold <cliss@austin.ibm.com> 1.4.1-1
- Update to version 1.4.1

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

