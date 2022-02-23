%define version 1.4.2

Summary: A front end for testing other programs.
Name: dejagnu
Version: %{version}
Release: 1
Copyright: GPL
Source: ftp://ftp.gnu.org/gnu/dejagnu/snapshots/dejagnu-%{version}.tar.gz
Prefix: %{_prefix}
Group: Development/Tools
Requires: tcl >= 8.0, expect >= 5.21
BuildRoot: /tmp/%{name}-root
%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
# Until the dependency on -Md gets fixed
%define DEFCC gcc
%endif

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q -n dejagnu-%{version}

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
./configure -v
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{prefix}
mkdir -p $RPM_BUILD_ROOT%{prefix}/include
mkdir -p $RPM_BUILD_ROOT%{prefix}/share/dejagnu
mkdir -p $RPM_BUILD_ROOT%{prefix}/doc/dejagnu-%{version}
make prefix=$RPM_BUILD_ROOT%{prefix} install
#make prefix=$RPM_BUILD_ROOT%{prefix} install-doc

(cd $RPM_BUILD_ROOT
 for dir in bin share doc include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING NEWS README AUTHORS INSTALL ChangeLog doc/overview.sgml
%{prefix}/bin/runtest
%{prefix}/include/dejagnu.h
%{prefix}/share/dejagnu/*
/usr/bin/runtest
/usr/include/dejagnu.h
/usr/share/dejagnu/*

%changelog
* Thu Oct 04 2001 David Clissold <cliss@austin.ibm.com>
-  Update to version 1.4.2

* Fri Jun 22 2001 Marc Stephenson <marc@austin.ibm.com>
-  Adapted for AIX Toolbox

* Wed Apr 11 2001 Rob Savoye <rob@welcomehome.org>
- Added installing dejagnu.h.
- Install the ps and pdf formatted docs too

* Wed Feb 21 2001 Rob Savoye <rob@welcomehome.org>
- Fixed Requires line, and changed the URL to the new ftp site.

* Sun Oct 31 1999 Rob Savoye <rob@welcomehome.org>
- updated to the latest snapshot
- added doc files
- added the site.exp config file

* Mon Jul 12 1999 Tim Powers <timp@redhat.com>
- updated to 19990628
- updated patches as needed
- added %defattr in files section

* Wed Mar 10 1999 Jeff Johnson <jbj@redhat.com>
- add alpha expect patch (#989)
- use %configure

* Thu Dec 17 1998 Jeff Johnson <jbj@redhat.com>
- Update to 19981215.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-10-29.

* Wed Jul  8 1998 Jeff Johnson <jbj@redhat.com>
- Update to 1998-05-28.

* Sun Feb  1 1998 Jeff Johnson <jbj@jbj.org>
- Create.
 
