# Optional tests
%bcond_without dotests


Name:		fio
Version:	3.20
Release:	1
Summary:	Multithreaded IO generation tool
Group:		Applications/System
License:	GPLv2
URL:		http://git.kernel.dk/?p=fio.git;a=summary
Source0:	http://brick.kernel.dk/snaps/%{name}-%{version}.tar.gz
Source100:      %{name}-%{version}-%{release}.build.log

Patch0:		%{name}-3.20-aix.patch
Patch1:         %{name}-3.20-statx.patch
Patch2:         %{name}-3.20-ppc.patch


BuildRequires:	zlib-devel, make, gcc >= 8.3, coreutils
BuildRequires:	patch, tar, sed
BuildRequires:	python3 >= 3.8.0
Requires:	zlib, bash
Requires:	python3 >= 3.8.0

%description
fio is an I/O tool that will spawn a number of threads or processes doing
a particular type of io action as specified by the user.  fio takes a
number of global parameters, each inherited by the thread unless
otherwise parameters given to them overriding that setting is given.
The typical use of fio is to write a job file matching the io load
one wants to simulate.


%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q
%patch0 -p1 -b .makefile
%patch1 -p1 -b .statx
%patch2 -p1 -b .ppc64

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/opt/freeware/bin:$PATH
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 32bit
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=32
export CC="gcc -pthread -maix32 $RPM_OPT_FLAGS"
./configure --disable-shm
gmake --trace

cd ../64bit
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64
export CC="gcc -pthread -maix64 $RPM_OPT_FLAGS"
./configure
# Assembler generated for gettime file is wrong if optimized.
gcc -pthread -maix64 -O0  -DFIO_VERSION='"fio-%{version}"' -DBITS_PER_LONG=64  -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -std=gnu99 -Wwrite-strings -Wall -Wdeclaration-after-statement -D_GNU_SOURCE -include config-host.h  -Wimplicit-fallthrough -I. -I. -D_GNU_SOURCE -include config-host.h  -Wimplicit-fallthrough -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFIO_INTERNAL -DFIO_INC_DEBUG -D_LARGE_FILES -D__ppc__ -c gettime.c
gmake --trace


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/opt/freeware/bin:$PATH

install_fio () {
  set -x
  export OBJECT_MODE=$1
  gmake install prefix=%{_prefix} mandir=%{_mandir} DESTDIR=${RPM_BUILD_ROOT}
  
  /usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

  (
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for fic in fio fio-dedupe fio-genzipf fio-verify-state
    do
        mv ${fic} ${fic}_$1
    done
  )
}

cd 32bit
install_fio 32

cd ../64bit
install_fio 64

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for fic in fio fio-dedupe fio-genzipf fio-verify-state
  do
    ln -sf ${fic}_64 ${fic}
  done
  
  /opt/freeware/bin/sed -i 's|#!/usr/bin/python2.7|#! /usr/bin/env python3|' *.py fio_jsonplus_clat2csv fio2gnuplot
)


%check
%if %{with dotests}
export PATH=/opt/freeware/bin:$PATH

check_fio () {
  set -x
  export OBJECT_MODE=$1

#  ulimit -m unlimited
#  ulimit -d unlimited
#  ulimit -n unlimited
#  ulimit -a

  ( gmake test || true )
}

cd 32bit
# Beware:
# fio: cache invalidation of fiotestfile.tmp failed: Invalid argument
check_fio 32

cd ../64bit
check_fio 64
%endif


%post
echo ""
echo "Please note that POSIX aio may not be enabled by default on AIX."
echo "If you get messages like:"
echo ""
echo "    Symbol resolution failed for /usr/lib/libc.a(posix_aio.o) because:"
echo "        Symbol _posix_kaio_rdwr (number 2) is not exported from dependent module /unix."
echo ""
echo "you need to enable POSIX aio. Run the following commands as root:"
echo ""
echo "    # lsdev -C -l posix_aio0"
echo "        posix_aio0 Defined  Posix Asynchronous I/O"
echo "    # cfgmgr -l posix_aio0"
echo "    # lsdev -C -l posix_aio0"
echo "        posix_aio0 Available  Posix Asynchronous I/O"
echo ""
echo "POSIX aio should work now. To make the change permanent (reboot required):"
echo ""
echo "    # chdev -l posix_aio0 -P -a autoconfig='available'"
echo "        posix_aio0 changed"
echo ""


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 64bit/README 64bit/REPORTING-BUGS 64bit/COPYING 64bit/HOWTO 64bit/examples
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}


%changelog
* Thu Jul 16 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 3.20-1
- Add 64 bits support
- Erase link to /usr
- Correct wrong dependency to python
- Use python3 as a default

* Tue Sep 18 2018 Tony Reix <tony.reix@atos.net> - 3.2-1
- Port on AIX 6.1

* Wed Nov 08 2017 Michael Perzl <michael@perzl.org> - 3.2-1
- updated to version 3.2

* Mon Oct 09 2017 Michael Perzl <michael@perzl.org> - 3.1-1
- updated to version 3.1

* Tue Sep 05 2017 Michael Perzl <michael@perzl.org> - 3.0-1
- updated to version 3.0

* Tue Sep 05 2017 Michael Perzl <michael@perzl.org> - 2.99-1
- updated to version 2.99

* Thu Jun 22 2017 Michael Perzl <michael@perzl.org> - 2.21-1
- updated to version 2.21

* Thu Jun 22 2017 Michael Perzl <michael@perzl.org> - 2.20-1
- updated to version 2.20

* Thu Jun 22 2017 Michael Perzl <michael@perzl.org> - 2.19-1
- updated to version 2.19

* Tue Feb 28 2017 Michael Perzl <michael@perzl.org> - 2.18-1
- updated to version 2.18

* Mon Jan 23 2017 Michael Perzl <michael@perzl.org> - 2.17-1
- updated to version 2.17

* Tue Jan 10 2017 Michael Perzl <michael@perzl.org> - 2.16-1
- updated to version 2.16

* Tue Nov 01 2016 Michael Perzl <michael@perzl.org> - 2.15-1
- updated to version 2.15

* Tue Sep 20 2016 Michael Perzl <michael@perzl.org> - 2.14-1
- updated to version 2.14

* Wed Aug 24 2016 Michael Perzl <michael@perzl.org> - 2.13-1
- updated to version 2.13

* Tue Jul 12 2016 Michael Perzl <michael@perzl.org> - 2.12-1
- updated to version 2.12

* Tue Jul 12 2016 Michael Perzl <michael@perzl.org> - 2.11-1
- updated to version 2.11

* Mon May 02 2016 Michael Perzl <michael@perzl.org> - 2.9-1
- updated to version 2.9

* Wed Apr 20 2016 Michael Perzl <michael@perzl.org> - 2.8-1
- updated to version 2.8

* Wed Apr 20 2016 Michael Perzl <michael@perzl.org> - 2.7-1
- updated to version 2.7

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.6-1
- updated to version 2.6

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.5-1
- updated to version 2.5

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.3-1
- updated to version 2.3

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.13-1
- updated to version 2.2.13

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.12-1
- updated to version 2.2.12

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.11-1
- updated to version 2.2.11

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.10-1
- updated to version 2.2.10

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.9-1
- updated to version 2.2.9

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.8-1
- updated to version 2.2.8

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.7-1
- updated to version 2.2.7

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.6-1
- updated to version 2.2.6

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.5-1
- updated to version 2.2.5

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.4-1
- updated to version 2.2.4

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.3-1
- updated to version 2.2.3

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.2-1
- updated to version 2.2.2

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.1-1
- updated to version 2.2.1

* Thu Mar 03 2016 Michael Perzl <michael@perzl.org> - 2.2.0-1
- updated to version 2.2.0

* Wed Nov 19 2014 Michael Perzl <michael@perzl.org> - 2.1.14-1
- updated to version 2.1.14

* Mon Oct 13 2014 Michael Perzl <michael@perzl.org> - 2.1.13-1
- updated to version 2.1.13

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 2.1.12-1
- updated to version 2.1.12

* Fri Aug 15 2014 Michael Perzl <michael@perzl.org> - 2.1.11-1
- updated to version 2.1.11

* Wed Jun 11 2014 Michael Perzl <michael@perzl.org> - 2.1.10-1
- updated to version 2.1.10

* Wed May 28 2014 Michael Perzl <michael@perzl.org> - 2.1.9-1
- updated to version 2.1.9

* Wed May 28 2014 Michael Perzl <michael@perzl.org> - 2.1.8-1
- updated to version 2.1.8

* Tue Apr 01 2014 Michael Perzl <michael@perzl.org> - 2.1.7-1
- updated to version 2.1.7

* Sun Mar 09 2014 Michael Perzl <michael@perzl.org> - 2.1.6.1-1
- updated to version 2.1.6.1

* Sun Mar 09 2014 Michael Perzl <michael@perzl.org> - 2.1.5-1
- updated to version 2.1.5

* Tue Nov 19 2013 Michael Perzl <michael@perzl.org> - 2.1.4-1
- updated to version 2.1.4

* Tue Nov 19 2013 Michael Perzl <michael@perzl.org> - 2.1.3-1
- updated to version 2.1.3

* Thu Aug 08 2013 Michael Perzl <michael@perzl.org> - 2.1.2-1
- updated to version 2.1.2

* Wed Jun 12 2013 Michael Perzl <michael@perzl.org> - 2.1.1-1
- updated to version 2.1.1

* Thu May 16 2013 Michael Perzl <michael@perzl.org> - 2.1-1
- updated to version 2.1

* Tue Apr 09 2013 Michael Perzl <michael@perzl.org> - 2.0.15-1
- updated to version 2.0.15

* Sat Feb 23 2013 Michael Perzl <michael@perzl.org> - 2.0.14-1
- updated to version 2.0.14

* Thu Jan 10 2013 Michael Perzl <michael@perzl.org> - 2.0.13-1
- updated to version 2.0.13

* Thu Dec 20 2012 Michael Perzl <michael@perzl.org> - 2.0.12.2-1
- updated to version 2.0.12.2

* Thu Oct 11 2012 Michael Perzl <michael@perzl.org> - 2.0.10-1
- updated to version 2.0.10

* Thu Aug 23 2012 Michael Perzl <michael@perzl.org> - 2.0.9-1
- updated to version 2.0.9

* Tue Jun 12 2012 Michael Perzl <michael@perzl.org> - 2.0.8-1
- updated to version 2.0.8

* Fri Apr 13 2012 Michael Perzl <michael@perzl.org> - 2.0.7-1
- updated to version 2.0.7

* Fri Mar 23 2012 Michael Perzl <michael@perzl.org> - 2.0.6-1
- updated to version 2.0.6

* Tue Mar 13 2012 Michael Perzl <michael@perzl.org> - 2.0.5-1
- updated to version 2.0.5

* Fri Feb 24 2012 Michael Perzl <michael@perzl.org> - 2.0.4-1
- updated to version 2.0.4

* Tue Feb 07 2012 Michael Perzl <michael@perzl.org> - 2.0.3-1
- updated to version 2.0.3

* Mon Feb 06 2012 Michael Perzl <michael@perzl.org> - 2.0.2-1
- updated to version 2.0.2

* Sun Dec 18 2011 Michael Perzl <michael@perzl.org> - 2.0-1
- updated to version 2.0

* Thu Nov 17 2011 Michael Perzl <michael@perzl.org> - 1.99.12-1
- updated to version 1.99.12

* Thu Nov 17 2011 Michael Perzl <michael@perzl.org> - 1.60.2-1
- updated to version 1.60.2

* Fri Sep 16 2011 Michael Perzl <michael@perzl.org> - 1.58-1
- updated to version 1.58

* Tue Aug 02 2011 Michael Perzl <michael@perzl.org> - 1.57-1
- updated to version 1.57

* Wed Jul 13 2011 Michael Perzl <michael@perzl.org> - 1.56-1
- updated to version 1.56

* Mon May 30 2011 Michael Perzl <michael@perzl.org> - 1.55-1
- updated to version 1.55

* Fri May 13 2011 Michael Perzl <michael@perzl.org> - 1.54-1
- updated to version 1.54

* Thu May 05 2011 Michael Perzl <michael@perzl.org> - 1.53-1
- updated to version 1.53

* Fri Apr 29 2011 Michael Perzl <michael@perzl.org> - 1.52-1
- updated to version 1.52

* Wed Jan 26 2011 Michael Perzl <michael@perzl.org> - 1.50-1
- updated to version 1.50

* Tue Dec 21 2010 Michael Perzl <michael@perzl.org> - 1.44.3-1
- updated to version 1.44.3

* Mon Dec 06 2010 Michael Perzl <michael@perzl.org> - 1.44.2-1
- updated to version 1.44.2

* Fri Nov 05 2010 Michael Perzl <michael@perzl.org> - 1.44.1-1
- first version for AIX V5.3 and higher
