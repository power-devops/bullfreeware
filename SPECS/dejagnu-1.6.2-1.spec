# By default, tests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

Summary: A front end for testing other programs.
Name: dejagnu
Version: 1.6.2
Release: 1
Epoch: 1
License: GPLv3+
Source: ftp://ftp.gnu.org/gnu/dejagnu/dejagnu-%{version}.tar.gz
Source10: %{name}-%{version}-%{release}.build.log

URL: http://www.gnu.org/software/dejagnu/
Group: Development/Tools
BuildArch: noarch

BuildRequires: tcl-devel >= 8.6.10-3
BuildRequires: expect >= 5.45

Requires: tcl >= 8.6.10-3
Requires: expect >= 5.45

# Until the dependency on -Md gets fixed
%define DEFCC gcc

%description
DejaGnu is an Expect/Tcl based framework for testing other programs.
DejaGnu has several purposes: to make it easy to write tests for any
program; to allow you to write tests which will be portable to any
host or target where a program must be tested; and to standardize the
output format of all tests (making it easier to integrate the testing
into software development).

%prep
%setup -q -n dejagnu-%{version}

#Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

%build
#First build the 64bit version

cd 64bit
export PATH="/opt/freeware/bin:$PATH"
export CC="gcc -maix64"
export CXX="g++ -maix64"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
./configure -v \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}64 
	
gmake


#Now build 32-bit version
cd ../32bit
export CC="gcc -maix32 -D_LARGE_FILES"
export CXX="g++ -maix32 -D_LARGE_FILES"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
./configure -v \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#mkdir -p $RPM_BUILD_ROOT%{_prefix}
#mkdir -p $RPM_BUILD_ROOT%{_prefix}/include
#mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/dejagnu
#mkdir -p $RPM_BUILD_ROOT%{_prefix}/doc/dejagnu-%{version}

cd 64bit
export AR="/usr/bin/ar -X64"
export OBJECT_MODE=64
gmake DESTDIR=$RPM_BUILD_ROOT install

# /usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in *
  do
    mv ${f} ${f}_64
  done
)

cd ../32bit
export AR="/usr/bin/ar -X32"
export OBJECT_MODE=32
gmake DESTDIR=$RPM_BUILD_ROOT install

# /usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in runtest 
  do
    mv ${f} ${f}_32
  done
)

# Make 64bit executable as default
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in runtest
  do
    ln -sf ${f}_64 ${f}
  done
)


%check
%if %{with dotests}
cd 64bit
export CC="gcc -maix64"
export CXX="g++ -maix64"
export OBJECT_MODE=64
(gmake -k check || true)
cd ../32bit
export CC="gcc -maix32"
export CXX="g++ -maix32"
export OBJECT_MODE=32
(gmake -k check || true)
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/COPYING 32bit/NEWS 32bit/README 32bit/AUTHORS 32bit/INSTALL 32bit/ChangeLog
%{_bindir}/runtest*
%{_includedir}/dejagnu.h
%{_datadir}/dejagnu/*
#%{_mandir}/*/*
#%{_infodir}/dejagnu*


%changelog
* Mon Nov 09 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.6.2-1
- Update to 1.6.2

* Mon Nov 09 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 1.6.1-3
- Update specfile for automated build

* Tue Sep 15 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.6.1-2
- Merge Toolbox and Bullfreeware Specfiles
- Correct "too many open file" bug

* Wed Nov 07 2018 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.6.1-1
- Updated to 1.6.1

* Thu May 12 2016 Tony Reix <tony.reix@bull.net> 1.6-1
- Initial port of 1.6 on AIX 6.1

* Mon Feb 16 2015 Hamza Sellami <hamza.sellami@bull.net>
- Build with the new GCC of version 1.5.3

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
 
