Name: ftpcopy
Version: 0.3.9
Release: 1
Copyright: Free, no warranties.
Group: Applications/Internet
Source: http://www.ohse.de/uwe/ftpcopy/ftpcopy-%{version}.tar.bz2
URL: http://www.ohse.de/uwe/ftpcopy.html
BuildRoot: %{_tmppath}/%{name}-root
Summary: A mirroring tool.
%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
%define DEFCC cc
%endif

%description
ftpcopy is a simply FTP client written to copy files or directories
(recursively) from a FTP server. It's primary purpose is to mirror
FTP sites which support the EPLF directory listing format, but it
may be used to mirror other sites, too.

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
if test "X$CC" != "Xgcc"
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
       export CFLAGS="$RPM_OPT_FLAGS"
fi

make CFLAGS="$CFLAGS" CC="$CC"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 ftpls ftpcp ftpcopy $RPM_BUILD_ROOT%{_bindir}
install -m 644 ftpls.1 ftpcp.1 ftpcopy.1 $RPM_BUILD_ROOT%{_mandir}/man1

(cd $RPM_BUILD_ROOT
 for dir in bin
 do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
 done
)

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%{_bindir}/*
/usr/bin/*
%{_mandir}/*/*

%changelog
* Tue Sep 04 2001 Marc Stephenson <marc@austin.ibm.com>
- Adapt for AIX Toolbox

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.3.9-1
- 0.3.9

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.3.7-1
- 0.3.7

* Fri Jan 19 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.3.4 - fixes date mismatches in a couple of cases

* Tue Dec  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to 0.3.3 - fixes security bugs. A ftp server being mirrored could
  overwrite any files on the mirroring system by sending filenames containing
  "../"

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.3.0 to get man pages

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat May 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- initial package
