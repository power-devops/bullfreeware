Summary: A plain ASCII to PostScript converter.
Name: enscript
Version: 1.6.1
Release: 3
Copyright: GNU
Group: Applications/Publishing
Source0: ftp://ftp.gnu.org/pub/gnu/enscript-1.6.1.tar.gz
Patch: enscript-1.6.1-destdir.patch
Prefix: %{_prefix}
BuildRoot: /var/tmp/%{name}-root
Obsoletes: nenscript
%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
%define DEFCC cc
%endif

%description
GNU enscript is a free replacement for Adobe's Enscript
program. Enscript converts ASCII files to PostScript(TM) and spools
generated PostScript output to the specified printer or saves it to a
file.  Enscript can be extended to handle different output media and
includes many options for customizing printouts.

%prep
%setup -q
%patch -p1

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

%define optflags "$RPM_OPT_FLAGS"
%configure --with-media=Letter --sysconfdir=%{prefix}/etc
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# XXX note doubled %% in sed script below.
(cd $RPM_BUILD_ROOT;find .%{_prefix}/share/enscript/*) | \
	sed -e 's,^\.,,' | sed -e 's,*font.map,%%config &,' > share.list

{ cd $RPM_BUILD_ROOT
  /usr/bin/strip .%{_prefix}/bin/* || :
  ln .%{_prefix}/bin/enscript .%{_prefix}/bin/nenscript
  mkdir -p usr/bin usr/linux/bin
  cd usr/bin
  ln -sf ../..%{prefix}/bin/* .
  rm -f enscript
  cd -
  cd usr/linux/bin
  ln -sf ../../..%{prefix}/bin/enscript .
}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f share.list
%defattr(-,root,root)
%{_prefix}/bin/diffpp
%{_prefix}/bin/sliceprint
%{_prefix}/bin/enscript
%{_prefix}/bin/nenscript
%{_prefix}/bin/mkafmmap
%{_prefix}/bin/states
%{_prefix}/bin/over
/usr/bin/*
/usr/linux/bin/enscript

%{_prefix}/man/man1/*
%config %{_prefix}/etc/enscript.cfg

%doc AUTHORS ChangeLog FAQ.html NEWS README README.ESCAPES THANKS TODO 

%changelog
* Thu Mar 29 2001 Marc Stephenson <marc@austin.ibm.com>
- Build with default compiler

* Thu Mar 01 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Add links from /usr/bin and /usr/linux/bin as appropriate

* Mon Feb 26 2001 aixtoolbox <aixtoollbox-l@austin.ibm.com>
- Update for AIX.

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Wed Mar 24 1999 Erik Troan <ewt@redhat.com>
- marked /usr/share/enscript/font.map as a config file

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- added documentation to the RPM

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.
- include i18n locales.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Wed Nov 11 1998 Preston Brown <pbrown@redhat.com>
- translations ripped out, slight cleanup to build section.

* Mon Nov 09 1998 Preston Brown <pbrown@redhat.com>
- initial build of GNU enscript to replace nenscript.
