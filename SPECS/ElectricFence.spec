Summary: A debugger which detects memory allocation violations.
Name: ElectricFence
Version: 2.2.2
Release: 1
Copyright: GPL
Group: Development/Tools
# NOTE that this version comes from the perens 'beta' subdirectory.
#  however, the so-called 'beta' has been current for over 2 years and
#  is the version packaged for most Linux distributions.
Source: ftp://ftp.perens.com/pub/ElectricFence/beta/%{name}-%{version}.tar.gz
Patch1: %{name}-2.0.5-longjmp.patch
Patch2: %{name}-2.1-vaarg.patch
Patch3: %{name}-2.2.2-aix.patch
BuildRoot: %{_tmppath}/%{name}-root
Prefix: %{_prefix}
%ifos linux
Requires: /sbin/ldconfig
%endif

%description
ElectricFence is a utility for C programming and
debugging. ElectricFence uses the virtual memory hardware of your
system to detect when software overruns malloc() buffer boundaries,
and/or to detect any accesses of memory released by
free(). ElectricFence will then stop the program on the first
instruction that caused a bounds violation and you can use your
favorite debugger to display the offending statement.

Install ElectricFence if you need a debugger to find malloc()
violations.

%prep
%setup -q
%patch1 -p1 -b .longjmp
%patch2 -p1 -b .vaarg
%patch3 -p1 -b .aix

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man3

make	BIN_INSTALL_DIR=%{buildroot}%{_bindir} \
	LIB_INSTALL_DIR=%{buildroot}%{_libdir} \
	MAN_INSTALL_DIR=%{buildroot}%{_mandir}/man3 \
	install

( cd $RPM_BUILD_ROOT
 mkdir -p usr/lib
 cd usr/lib
 ln -sf ../..%{prefix}/lib/* .
 cd -
)

%ifos linux
echo ".so man3/efence.3" > %{buildroot}%{_mandir}/man3/libefence.3
%endif

%clean
rm -rf %{buildroot}

%ifos linux
%post
/sbin/ldconfig
%postun
/sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%ifos linux
%{_bindir}/*
%endif
%{_libdir}/*
%{_mandir}/*/*
/usr/lib/*

%changelog
* Mon Jul 02 2001 David Clissold <cliss@austin.ibm.com>
- Initial build for AIX Toolbox
- Note that 'ef' is not shipped, as it is N/A to AIX.

* Thu Nov 16 2000 Tim Powers <timp@redhat.com>
- use -fPIC, not -fpic, also -DUSE_SEMAPHORE to make it thread safe,
  as per bug #20935

* Tue Sep 19 2000 Bill Nottingham <notting@redhat.com>
- use -fpic

* Fri Aug 18 2000 Tim Waugh <twaugh@redhat.com>
- fix efence.3/libefence.3 confusion (#16412).

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- added ldconfig stuff to ;post and postun
- added Requires /sbin/ldconfig
* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 05 2000 Preston Brown <pbrown@redhat.com>
- back in main distro
- 2.2.2 version - claimed beta, but no releases in over a year.
- FHS macros

* Fri May 26 2000 Tim Powers <timp@redhat.com>
- moved to Powertools
- fix map page location to be in /usr/share/man

* Tue May 16 2000 Jakub Jelinek <jakub@redhat.com>
- fix build on ia64

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan  4 2000 Jeff Johnson <jbj@redhat.com>
- remove ExcludeArch: alpha (#6683).

* Sat Apr 10 1999 Matt Wilson <msw@redhat.com>
- version 2.1

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 13)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Fri Aug 21 1998 Jeff Johnson <jbj@redhat.com>
- create efence.3 (problem #830)

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- need to use sigsetjmp() and siglongjmp() for proper testing

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use ExcludeArch instead of Exclude

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
