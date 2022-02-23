Summary: The GNU line editor
Name: ed
Version: 1.14.2
Release: 1
License: GPL3+
Group: Applications/Text
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.lz.sig
URL: http://www.gnu.org/software/ed/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: /sbin/install-info, info

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.


%prep
%setup -q
rm -f stamp-h.in


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    CC=xlc_r CXX=xlC_r CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS"
make %{?_smp_mflags} all

gmake check


%install
export PATH=/opt/freeware/bin:$PATH

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir*
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
install -p -m 0644 doc/ed.1 ${RPM_BUILD_ROOT}%{_mandir}/man1

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
cd usr/linux/bin
ln -sf ../../..%{_bindir}/* .


%post
/sbin/install-info %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :


%preun
if [ $1 = 0 ] ; then
    /sbin/install-info --delete %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc ChangeLog NEWS README TODO AUTHORS COPYING
%{_bindir}/*
%{_infodir}/ed.info.gz
%{_mandir}/man?/*
/usr/linux/bin/*


%changelog
* Fri Aug 24 2018 Tony Reix <tony.reix@atos.net> - 1.14.2-1
- RePort on AIX 6.1

* Wed Feb 22 2017 Michael Perzl <michael@perzl.org> - 1.14.2-1
- updated to version 1.14.2

* Wed Jan 18 2017 Michael Perzl <michael@perzl.org> - 1.14.1-1
- updated to version 1.14.1

* Sat Jan 07 2017 Michael Perzl <michael@perzl.org> - 1.14-1
- updated to version 1.14

* Fri Feb 12 2016 Michael Perzl <michael@perzl.org> - 1.13-1
- updated to version 1.13

* Wed Jul 08 2015 Michael Perzl <michael@perzl.org> - 1.12-1
- updated to version 1.12

* Wed Apr 01 2014 Michael Perzl <michael@perzl.org> - 1.11-1
- updated to version 1.11

* Wed Feb 19 2014 Michael Perzl <michael@perzl.org> - 1.10-1
- updated to version 1.10

* Fri Jun 21 2013 Michael Perzl <michael@perzl.org> - 1.9-1
- updated to version 1.9

* Tue Apr 23 2013 Michael Perzl <michael@perzl.org> - 1.8-1
- updated to version 1.8

* Sat Nov 24 2012 Michael Perzl <michael@perzl.org> - 1.7-1
- updated to version 1.7

* Tue Jan 03 2012 Michael Perzl <michael@perzl.org> - 1.6-1
- updated to version 1.6

* Sat Sep 04 2010 Michael Perzl <michael@perzl.org> - 1.5-1
- updated to version 1.5

* Tue Jul 14 2009 Michael Perzl <michael@perzl.org> - 1.4-1
- updated to version 1.4

* Tue Jun 16 2009 Michael Perzl <michael@perzl.org> - 1.3-1
- updated to version 1.3

* Mon Feb 09 2009 Michael Perzl <michael@perzl.org> - 1.2-1
- updated to version 1.2

* Thu Oct 16 2008 Michael Perzl <michael@perzl.org> - 1.1-1
- updated to version 1.1

* Mon Aug 25 2008 Michael Perzl <michael@perzl.org> - 1.0-1
- updated to version 1.0

* Fri May 09 2008 Michael Perzl <michael@perzl.org> - 0.9-1
- first version for AIX V5.1 and higher
