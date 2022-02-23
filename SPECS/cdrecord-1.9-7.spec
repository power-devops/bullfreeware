%define CDVERSION 1.9
Summary: A command line CD/DVD recording program.
Name:		cdrecord
Version:	%{CDVERSION}
Release:	7
Serial:		3
Prefix:		%{_prefix}
License:	GPL
Group: Applications/Archiving
URL: http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/cdrecord.html
Source: ftp://ftp.fokus.gmd.de/pub/unix/cdrecord/%{name}-%{version}.tar.gz
Patch0: %{name}-libm.patch
Patch1: %{name}-ide.patch
BuildRoot:	/var/tmp/%{name}-%{version}


%description
Cdrecord is an application for creating audio and data CDs. Cdrecord
works with many different brands of CD recorders, fully supports
multi-sessions and provides human-readable error messages.

%package	devel
Summary: The libschily SCSI user level transport library.
Group: Development/Libraries
Requires:	%{name} = %{serial}:%{version}

%description	devel
The cdrecord-devel package contains a SCSI user level transport
library which can talk to any SCSI device without a special driver for
the device. Cdrecord can easily be ported to any system with a SCSI
device driver similar to the scg driver.

%package -n mkisofs
Version: 1.13
Summary: Creates an image of an ISO9660 filesystem.
Group: Applications/System
Obsoletes: cdrecord-mkisofs

%description -n mkisofs
The mkisofs program is used as a pre-mastering program; i.e., it
generates the ISO9660 filesystem.  Mkisofs takes a snapshot of
a given directory tree and generates a binary image of the tree
which will correspond to an ISO9660 filesystem when written to
a block device.  Mkisofs is used for writing CD-ROMs, and includes
support for creating bootable El Torito CD-ROMs.

Install the mkisofs package if you need a program for writing
CD-ROMs.

%package -n cdda2wav
Group: Applications/Multimedia
Summary: A utility for sampling/copying .wav files from digital audio CDs.
Obsoletes: cdrecord-cdda2wav

%description -n cdda2wav
Cdda2wav is a sampling utility for CD-ROM drives that are capable of
providing a CD's audio data in digital form to your host. Audio data
read from the CD can be saved as .wav or .sun format sound files.
Recording formats include stereo/mono, 8/12/16 bits and different
rates.  Cdda2wav can also be used as a CD player.

%prep
%setup -q
%ifnos aix5.1
# Add the libm & ide patches for aix5.2 (and up); exclude 5.1
%patch0
%patch1 -b .ide
%endif

%build
if [[ -z "$CC" ]]
then
    if test "X`type cc 2>/dev/null`" != 'X'; then
       CC=cc
    else 
       CC=gcc
    fi
fi
./Gmake CCOM=$CC CPPOPTX="-D_LARGE_FILES"

%install
rm -rf $RPM_BUILD_ROOT
if [[ -z "$CC" ]]
then
    if test "X`type cc 2>/dev/null`" != 'X'; then
       CC=cc
    else 
       CC=gcc
    fi
fi
./Gmake CCOM=$CC "INS_BASE=$RPM_BUILD_ROOT%{prefix}" install

# Installing Header files for use with devel package
[ -e  include/scg ] && rm include/scg

install -d $RPM_BUILD_ROOT%{prefix}/include/schily/scg
install -m 644 include/* $RPM_BUILD_ROOT%{prefix}/include/schily
install -m 644 incs/*/xconfig.h $RPM_BUILD_ROOT%{prefix}/include/schily
install -m 644 libscg/scg/* $RPM_BUILD_ROOT%{prefix}/include/schily/scg

mkdir -p $RPM_BUILD_ROOT/etc
install -m 644 cdrecord/cdrecord.dfl $RPM_BUILD_ROOT/etc/cdrecord.conf

/usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/* || :

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
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,system)
%doc AN-%{CDVERSION} doc/cdrecord.ps Changelog README* Linux.scsi-patch
%doc cdrecord/cdrecord.dfl
%config /etc/cdrecord.conf
%{prefix}/bin/cdrecord
%{prefix}/bin/readcd
%{prefix}/bin/devdump
%{prefix}/bin/isoinfo
%{prefix}/bin/isodump
%{prefix}/bin/isovfy
/usr/bin/cdrecord
/usr/bin/readcd
/usr/bin/devdump
/usr/bin/isoinfo
/usr/bin/isodump
/usr/bin/isovfy
%{prefix}/man/man1/cdrecord.1*
%{prefix}/man/man1/readcd.1*
%{prefix}/man/man8/isoinfo.8*

%files	devel
%defattr(-,root,system)
%{prefix}/lib/libdeflt.a
%{prefix}/lib/libscg.a
%{prefix}/lib/libschily.a
/usr/lib/libdeflt.a
/usr/lib/libscg.a
/usr/lib/libschily.a
%{prefix}/include/schily

%files -n mkisofs
%defattr(-,root,system)
%doc AN-%{CDVERSION} mkisofs/COPYING mkisofs/ChangeLog
%doc mkisofs/README*
%{prefix}/bin/mkisofs
/usr/bin/mkisofs
%{prefix}/man/man8/mkisofs.8*

%files -n cdda2wav
%defattr(-,root,system)
%doc AN-%{CDVERSION} cdda2wav/GPL cdda2wav/FAQ cdda2wav/OtherProgs
%doc cdda2wav/README* cdda2wav/Frontends cdda2wav/HOWTOUSE
%{prefix}/bin/cdda2wav
/usr/bin/cdda2wav
%{prefix}/man/man1/cdda2wav.1*

%changelog
* Mon Mar 20 2006 Reza Arbab <arbab@austin.ibm.com> 1.9-7
- Fix an errno handling bug when the media is unwritable.

* Fri Jun 24 2005 Reza Arbab <arbab@austin.ibm.com> 1.9-6
- Add support for DK_PASSTHRU. 

* Fri Feb 18 2005 David Clissold <cliss@austin.ibm.com> 1.9-5
- Try to get working correctly w/ IDE.  Seems to work now.
   (Code assistance from Nick Ham made this possible.)

* Mon May 14 2001 Marc Stephenson <marc@austin.ibm.com>
- Build with large files enabled

* Fri Mar 02 2001 Marc Stephenson <marc@austin.ibm.com>
- Observe IA64 32-bit ABI changes

* Wed Jan 10 2001 Marc Stephenson <aixtoolbox-l@austin.ibm.com>
- Added links for AIX Toolbox distribution

* Wed Feb 23 2000 Bill Nottingham <notting@redhat.com>
- fix cdda2wav on sparc, and probably other IDE drives...

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- version 1.8 final
- man pages are compressed

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
- get rid of useless defines at the top of the spec file

* Fri Jan 28 2000 Cristian Gafton <gafton@redhat.com>
- version 1.8a40
- according to the author, cdda2wav and mkisofs are more recent in this
  package, so build them out of this tree too
- add sparc patch from jakub

* Sun Dec 12 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.8a34

* Mon Sep 20 1999 Matt Wilson <msw@redhat.com>
- require serial:version

* Mon Sep 20 1999 Preston Brown <pbrown@redhat.com>
- a29

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Mon Sep 06 1999 Cristian Gafton <gafton@redhat.com>
- move config file to a sane place (/etc/cdrecord.conf)

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- 1.8a25

* Mon Aug 23 1999 Cristian Gafton <gafton@redhat.com>
- removed the mkisofs subpackage - we have mkisofs provided by 
  a'nother package (doh!)
- moved former mkisofs diagnostic binaries to the main package
- get rod of the cdda2wav too; cdparanoia is now in the distribution and
  it is a whole lot better too

* Fri Aug 20 1999 Preston Brown <pbrown@redhat.com>
- adopted for Red Hat Linux 6.1 from Ryan Weaver.
