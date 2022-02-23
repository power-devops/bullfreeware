Summary: The GNU libtool, which simplifies the use of shared libraries.
Name: libtool
Version: 1.5.22
Release: 1
License: GPL
Group: Development/Tools
Source: ftp://alpha.gnu.org/gnu/libtool-%{version}.tar.gz
# Source1: libtool.libltdl.so.0
URL: http://www.gnu.org/software/libtool
Prefix: %{_prefix}
PreReq: /sbin/install-info autoconf automake m4
BuildRoot: /var/tmp/%{name}-root
# avoid unnecessary dependency on the GNU sed
#  (can just deinstall sed and reinstall after build)
BuildConflicts: sed
%define DEFCC cc

%description
The libtool package contains the GNU libtool, a set of shell scripts which
automatically configure UNIX and UNIX-like architectures to generically build
shared libraries.  Libtool provides a consistent, portable interface which
simplifies the process of using shared libraries.

If you are developing programs which will use shared libraries, you should
install libtool.

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
export NM=/usr/bin/nm
export ECHO=/usr/bin/echo

./configure --prefix=%{_prefix}
make

# Add the old version of libltdl.so.0 for compatability with
# older apps that depend on libltdl.a(libltdl.so.0)
#
# if [[ -e "%{SOURCE1}" ]]
# then
#     cd ./libltdl/.libs
#     cp %{SOURCE1} ./libltdl.so.0
#     /usr/bin/strip -e libltdl.so.0
#     ar -r libltdl.a libltdl.so.0
# fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

cp install-sh missing demo

cd $RPM_BUILD_ROOT
gzip -9nf .%{_prefix}/share/info/*.info*

(cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
 cd -

 mkdir -p usr/share/aclocal
 cd usr/share
 ln -sf ../..%{_prefix}/share/libtool .
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/libtool.info.gz %{_prefix}/share/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/share/info/libtool.info.gz %{_prefix}/share/info/dir
fi

%files
%defattr(-,root,system)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog demo
%{_prefix}/bin/*
/usr/bin/*
%{_prefix}/share/info/libtool.info*
%{_prefix}/include/ltdl.h
%{_prefix}/lib/libltdl.*
/usr/include/ltdl.h
/usr/lib/libltdl.*
%{_prefix}/share/libtool
%{_prefix}/share/aclocal/libtool.m4

%changelog
* Thu Apr 12 2007 Christophe Belle <christophe.belle@bull.net> 1.5.22-1
- Update to version 1.5.22

* Thu Aug 19 2004 David Clissold <cliss@austin.ibm.com>  1.5.8-1
- Update to 1.5.8

* Thu May 27 2004 David Clissold <cliss@austin.ibm.com>  1.5-2
- Avoid forced dependency on GNU sed; ok to use AIX sed.

* Wed Apr 30 2003 David Clissold <cliss@austin.ibm.com>
- Update to level 1.5

* Thu Sep 27 2001 David Clissold <cliss@austin.ibm.com>
- Update to level 1.4.2

* Fri May 25 2001 David Clissold <cliss@austin.ibm.com>
- Fix to patch for ia64 -- add no_undefined_flag="-zdefs"

* Sun Mar 25 2001 Marc Stephenson <marc@austin.ibm.com>
- Fix library dependency code for ia64

* Wed Mar 21 2001 Marc Stephenson <marc@austin.ibm.com>
- Hardcode noentry flag

* Tue Mar 06 2001 Marc Stephenson <marc@austin.ibm.com>
- Add code to handle non-gcc compilers

* Sun Mar 04 2001 Marc Stephenson <marc@austin.ibm.com>
- Update to 1.3.5a

* Thu Mar 01 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Update needed for the the IA64 aix patch

* Fri Feb 16 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Account for different standard lib location in IA64 32-bit ABI

* Fri Oct 27 2000 pkgmgr <pkgmgr@austin.ibm.com>
- Modify for AIX Freeware distribution

* Fri Mar  3 2000 Jeff Johnson <jbj@redhat.com>
- add prereqs for m4 and perl inorder to run autoconf/automake.

* Mon Feb 28 2000 Jeff Johnson <jbj@redhat.com>
- functional /usr/doc/libtool-*/demo by end-user %post procedure (#9719).

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.4.

* Mon Dec  6 1999 Jeff Johnson <jbj@redhat.com>
- change from noarch to per-arch in order to package libltdl.a (#7493).

* Thu Jul 15 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.3.

* Mon Jun 14 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.2.

* Tue May 11 1999 Jeff Johnson <jbj@redhat.com>
- explicitly disable per-arch libraries (#2210)
- undo hard links and remove zero length file (#2689)

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- disable the --cache-file passing to ltconfig; this breaks the older
  ltconfig scripts found around.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 2)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.2f

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- completed arm patch
- added patch to make it more arm-friendly
- upgrade to version 1.2d

* Thu May 07 1998 Donnie Barnes <djb@redhat.com>
- fixed busted group

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- Update to 1.0h
- added install-info support

* Tue Nov 25 1997 Elliot Lee <sopwith@redhat.com>
- Update to 1.0f
- BuildRoot it
- Make it a noarch package
