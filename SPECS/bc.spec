Summary: GNU's bc (a numeric processing language) and dc (a calculator).
Name: bc
Version: 1.06
Release: 2
Copyright: GPL
Group: Applications/Engineering
Source: ftp://prep.ai.mit.edu/pug/gnu/bc-%{version}.tar.gz
Prereq: /sbin/install-info
Prefix: %{_prefix}
Buildroot: /var/tmp/%{name}-root

%ifarch ia64
%define DEFCCIA cc
%define DEFCC %{DEFCCIA}
%else
%define DEFCC cc
%endif

%description
The bc package includes bc and dc.  Bc is an arbitrary precision
numeric processing arithmetic language.  Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%prep
%setup -q -n bc-1.06


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
       # If not using gcc, get rid of undesirable hard-coded flags
       for dir in bc dc lib ; do
          sed -e 's/-Wall -funsigned-char//' $dir/Makefile.in > Mf.in \
            && mv Mf.in $dir/Makefile.in
       done
fi


%configure --with-readline
make

%install
rm -rf $RPM_BUILD_ROOT

#make prefix=$RPM_BUILD_ROOT%{_prefix} install
make DESTDIR=$RPM_BUILD_ROOT install
gzip -n -9f $RPM_BUILD_ROOT%{_prefix}/info/dc.info

/usr/bin/strip $RPM_BUILD_ROOT%{prefix}/bin/dc $RPM_BUILD_ROOT%{prefix}/bin/bc

(cd $RPM_BUILD_ROOT
 mkdir -p usr/linux/bin
 cd usr/linux/bin
 ln -sf ../../..%{prefix}/bin/* .
)

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ifos linux
# previous versions of bc put an improper entry into /usr/info/dir -- remove
# it
if grep 'dc: (bc)' %{prefix}/info/dir > /dev/null; then
    grep -v 'The GNU RPN calculator' < %{prefix}/info/dir > %{prefix}/info/dir.$$
    mv -f %{prefix}/info/dir.$$ %{prefix}/info/dir
fi
%endif

/sbin/install-info %{prefix}/info/dc.info.gz %{prefix}/info/dir --entry="* dc: (dc).                      The GNU RPN calculator."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{prefix}/info/dc.info.gz %{prefix}/info/dir --entry="* dc: (dc).                      The GNU RPN calculator."
fi

%files
%defattr(-,root,root)
%{prefix}/bin/dc
%{prefix}/bin/bc
/usr/linux/bin/dc
/usr/linux/bin/bc
%{prefix}/man/man1/*
%{prefix}/info/dc.info.gz

%changelog
* Thu Mar 21 2001 David Clissold <cliss@austin.ibm.com>
- Pull undesired hardcoded CFLAGS out of Makefile.in (via sed)

* Thu Mar  1 2001 Marc Stephenson <marc@austin.ibm.com>
- Add links for AIX Toolbox

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Jan 21 1999 Jeff Johnson <jbj@redhat.com>
- use %configure

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.05a.

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Thu Jun 04 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.05 with build root.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Erik Troan <ewt@redhat.com>
- got upgrades of info entry working (I hope)

* Sun Apr 05 1998 Erik Troan <ewt@redhat.com>
- fixed incorrect info entry

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- added install-info support

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- upgraded from 1.03 to 1.04

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
