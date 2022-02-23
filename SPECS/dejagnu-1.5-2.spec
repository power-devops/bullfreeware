Summary: A front end for testing other programs.
Name: dejagnu
Version: 1.5
Release: 2
Copyright:  GPLv3+
Source: ftp://ftp.gnu.org/gnu/dejagnu/%{name}-%{version}.tar.gz
Patch0: dejagnu-1.5-remote.patch
URL: http://www.gnu.org/software/dejagnu/
Group: Development/Tools
Requires: tcl >= 8.0, expect >= 5.21
Requires: /sbin/install-info
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q -n dejagnu-%{version}
%patch0 -p1 -b .remote

%build
./configure -v \
    --prefix=%{_prefix} \
    --infodir=%{_infodir} \
    --mandir=%{_mandir} \
    CC="/opt/hamza/build.gcc.4.8.3/bin/gcc"\
    CXX="/opt/hamza/build.gcc.4.8.3/bin/g++"

gmake 

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p $RPM_BUILD_ROOT%{_prefix}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/%{name}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/doc/%{name}-%{version}

make prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/man \
	infodir=${RPM_BUILD_ROOT}%{_prefix}/info \
	install

# Strip all of the executables
/usr/bin/strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* 2>/dev/null || :

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/*info*

(cd $RPM_BUILD_ROOT
 for dir in bin share doc include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf ../../..%{_prefix}/bin/* .
 cd -
)

%post
/sbin/install-info %{_prefix}/info/dejagnu.info.gz %{_prefix}/info/dir || :

%preun
if [ $1 = 0 ] ; then
   /sbin/install-info --delete %{_prefix}/info/dejagnu.info.gz %{_prefix}/info/d
ir || :
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc COPYING NEWS README AUTHORS INSTALL TODO ChangeLog doc/dejagnu.texi
%{_prefix}/bin/*
%{_prefix}/include/dejagnu.h
%{_prefix}/share/dejagnu/*
%{_prefix}/man/man1/runtest.1*
%{_prefix}/info/dejagnu.info*

/usr/bin/*
/usr/include/dejagnu.h
/usr/share/dejagnu/*
/usr/linux/bin/*

%changelog
* Mon Feb 16 2015 Hamza Sellami <hamza.sellami@bull.net>
- Build with the new GCC

* Mon Aug 29 2011 Patricia Cugny <patricia.cugny@bull.net> 
- modifs spec file 1.5-1

* Fri Jun 3 2011 Gerard Visiedo <gerard.visiedo@bull.net>
- Porting 1.5 on aix5.3

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
 
