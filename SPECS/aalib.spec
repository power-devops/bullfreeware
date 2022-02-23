Summary: An ASCII art library.
Name: aalib
Version: 1.2
Release: 2
Group: System Environment/Libraries
Copyright: LGPL
Url: http://www.ta.jcu.cz/aa
Source0: %{name}-%{version}.tar.gz
Buildroot: /var/tmp/%{name}-%{version}-%{release}-root
Prereq: /sbin/install-info
Prefix: %{_prefix}

%ifarch ia64
%define stdlib lib/ia64l32
%define stdlib64 lib/ia64l64
%define liblink ../../..
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
%define stdlib lib
%define liblink ../..
%define DEFCC cc
%endif

%description
AA-lib is a low level graphics library that doesn't require a graphics
device and has no graphics output.  Instead AA-lib replaces those
old-fashioned output methods with a powerful ASCII-art renderer.  The
AA-Project is working on porting important software like DOOM and Quake
to work with AA-lib. If you'd like to help them with their efforts,
you'll also need to install the aalib-devel package.

%package devel
Summary: The static libraries and header files for AA-lib.
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The aalib-devel package contains the static libraries and header files
for the AA-lib ASCII art library.  If you'd like to develop programs
using AA-lib, you'll need to install aalib-devel.

%prep
%setup -q 

%ifarch sparc
%patch0 -p1
%endif

%build
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
fi
export CFLAGS="$RPM_OPT_FLAGS"

./configure --prefix=%{prefix} --with-x
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -r $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT/usr
%makeinstall 

strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

( cd $RPM_BUILD_ROOT
 for dir in bin include
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done

 mkdir -p usr/%{stdlib}
 cd usr/%{stdlib}
 ln -sf %{liblink}%{prefix}/lib/* .
)

%files
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS COPYING ChangeLog NEWS
%attr(755,root,root) %{_bindir}/aafire
%attr(755,root,root) %{_bindir}/aainfo
%attr(755,root,root) %{_bindir}/aasavefont
%attr(755,root,root) %{_bindir}/aatest
%attr(755,root,root) %{_libdir}/libaa.*
%attr(644,root,root) %{_infodir}/*.info*
/usr/bin/*
/usr/%{stdlib}/libaa.*

%files devel
%attr(644,root,root) %{_includedir}/*.h
/usr/include/*.h

%clean
rm -r $RPM_BUILD_ROOT

%post
if [ -e %{_infodir}/libaa.info.gz ]; then
	/sbin/install-info %{_infodir}/libaa.info.gz %{_infodir}/dir
fi

%ifos linux
/sbin/ldconfig
%endif


%preun
if [ -e %{_infodir}/libaa.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/libaa.info.gz %{_infodir}/dir
fi

%ifos linux
%postun
/sbin/ldconfig
%endif

%changelog
* Mon Oct 22 2001 David Clissold <cliss@austin.ibm.com>
- No functional change.  Modify SPEC b/c of incompat w/ newer libtool.

* Wed May 23 2001 David Clissold <cliss@austin.ibm.com>
- First build for AIX.

* Mon Aug 7 2000 Tim Powers <timp@redhat.com>
- use patch submitted in bug #15193 by bob@ccl.kuleuven.ac.be for sparc only.

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jun 2 2000 Tim Powers <timp@redhat.com>
- fix man page location to be FHS compliant
- spec file cleanups for RPM 4.0 macros

* Tue Apr 25 2000 Tim Powers <timp@redhat.com>
- general spec file cleanups. No more useless defines
- use percent configure instead of ./configure
* Thu Dec 23 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.2

* Tue Jul 6 1999 Tim Powers <timp@redhat.com>
- built package for 6.1

* Wed Apr 21 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
