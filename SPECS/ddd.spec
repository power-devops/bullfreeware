Summary: A GUI for several command-line debuggers.
Name: ddd
Version: 3.3.1
Release: 2
Copyright: GPL or BSD
Group: Development/Debuggers
Source0: ftp://ftp.gnu.org/pub/gnu/ddd/ddd-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/pub/gnu/ddd/ddd-%{version}-pics.tar.gz
Source2: ddd.desktop
Patch0: ddd-%{version}-XawInit.patch
URL: http://www.gnu.org/software/ddd/
BuildRoot: %{_tmppath}/%{name}-root
Prereq: /sbin/install-info
Prefix: %{_prefix}
%ifos linux
BuildPreReq: openmotif-devel
Requires: openmotif
%endif

%description
The Data Display Debugger (DDD) is a popular GUI for command-line
debuggers like GDB, DBX, JDB, WDB, XDB, the Perl debugger, and the
Python debugger.  DDD allows you to view source texts and provides an
interactive graphical data display, in which data structures are
displayed as graphs.  You can use your mouse to dereference pointers
or view structure contents, which are updated every time the program
stops.  DDD can debug programs written in Ada, C, C++, Chill, Fortran,
Java, Modula, Pascal, Perl, and Python.  DDD provides machine-level
debugging; hypertext source navigation and lookup; breakpoint,
watchpoint, backtrace, and history editors; array plots; undo and
redo; preferences and settings editors; program execution in the
terminal emulation window, debugging on a remote host, an on-line
manual, extensive help on the Motif user interface, and a command-line
interface with full editing, history and completion capabilities.

%prep
%setup -q -b 1 
%patch -p1 -b .aixhdr

%build
#cp -f /usr/share/libtool/config.* .
export CXXFLAGS="-O"
%configure
make CXXOPT="-DNDEBUG" LDFLAGS="-Wl,-bbigtoc"

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
%makeinstall

mkdir -p $RPM_BUILD_ROOT/etc/X11/applnk/Development
install -m 644 %{SOURCE2} \
	$RPM_BUILD_ROOT/etc/X11/applnk/Development/ddd.desktop 

install -m 755 pydb/pydb.py $RPM_BUILD_ROOT/%{_bindir}
install -m 755 pydb/pydbcmd.py $RPM_BUILD_ROOT/%{_bindir}
install -m 755 pydb/pydbsupt.py $RPM_BUILD_ROOT/%{_bindir}

gzip -9nfq $RPM_BUILD_ROOT/%{_infodir}/*

cd $RPM_BUILD_ROOT%{_bindir}
ln -sf pydb.py pydb

( cd $RPM_BUILD_ROOT

 /usr/bin/strip .%{prefix}/bin/* || :

 for dir in bin share
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{prefix}/$dir/* .
    cd -
 done
)


%post
/sbin/install-info %{_infodir}/ddd.info.gz %{_infodir}/dir
 
%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/ddd.info.gz %{_infodir}/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/README doc/ddd.pdf doc/ddd-paper.ps doc/sample.dddinit
%doc ANNOUNCE BUGS COPYING INSTALL NEWS OPENBUGS PROBLEMS README TIPS TODO
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/ddd*
/usr/bin/*
/usr/share/ddd*
%config /etc/X11/applnk/Development/ddd.desktop 
%dir %{_datadir}/%{name}-%{version}
%{_datadir}/%{name}-%{version}/ddd
%{_datadir}/%{name}-%{version}/themes
%{_datadir}/%{name}-%{version}/vsllib

%changelog
* Wed Apr 24 2002 David Clissold <cliss@austin.ibm.com>
- No functional change.  Remove minor politically-sensitive
- designation from the original gzipped tarball.

* Wed Feb 06 2002 David Clissold <cliss@austin.ibm.com>
- strip binaries; create links

* Thu Nov 15 2001 Marc Stephenson <marc@austin.ibm.com>
- build for AIX Toolbox

* Sat Feb 03 2001 Than Ngo <than@redhat.com>
- updated to 3.3

* Tue Jan 23 2001 Than Ngo <than@redhat.com>
- updated to 3.2.98, a release candidate for DDD 3.3

* Mon Dec 04 2000 Than Ngo <than@redhat.com>
- updated to 2.3.92 (Bug #16254)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Sat Jul 22 2000 Tim Powers <timp@redhat.com>
- fixed missing BuildPreReq

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- added defattr

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Mon Jun 12 2000 Than Ngo <than@redhat.de>
- rebuild with openmotif-2.1.30 for 7.0
- clean up specfile
- FHS fixes

* Mon May 8 2000 Tim Powers <timp@redhat.com>
- updated to 3.2.1
- use applnk 

* Fri Feb 11 2000 Tim Powers <timp@redhat.com>
- applied patch for ddd for use with lesstif 0.89 which caused the "view news"
	etc. help items not to uncompress the news and manual properly, resulting in
	an error message. Patch was from Andreas Zeller
	<andreas.zeller@fmi.uni-passau.de>
	
* Tue Feb 01 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space
- built for 6.2

* Tue Feb 01 2000 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- includes pdf doc instead of postscript
- upgraded to 3.2
- changed source locations and URLs to point at the new GNU sites
- now does a make strip
- added GNOME desktop entry


* Fri Jan 07 2000 Trond Eivind Glomsrød <teg@pvv.ntnu.no>
- removed ptrace patch
- now installs pydb
- upgraded to 3.1.99
- removed lots of old log entries

* Thu Aug 19 1999 Tim Powers <timp@redhat.com>
- reapplied patch for ptrace problems with sparc

* Thu Aug 19 1999 Dale Lovelace <dale@redhat.com>
- added ddd.wmconfig

* Thu Jul 1 1999 Tim Powers <timp@redhat.com>
- added the --with-motif-includes= and --with-motif-libraries= lines
  so that it would build
- rebuilt package for Powertools

* Sat Jun 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 3.1.5.

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated package
