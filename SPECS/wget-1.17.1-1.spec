Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.17.1
Release: 1
License: GPLv3+
Group: Appl/var/tions/Internet
Url: http://www.gnu.org/software/%{name}/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz.sig
Patch0: %{name}-%{version}-aix.patch
Provides: webclient
Requires: /sbin/install-info, info
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: openssl-devel >= 1.0.0d, gettext, libidn-devel >= 1.24-1
BuildRequires: libiconv >= 1.13.1
BuildRequires: pcre-devel >= 8.12-3
BuildRequires: zlib-devel >= 1.2.5-4
Requires: openssl >= 1.0.0d, gettext, libidn >= 1.24-1
Requires: libiconv >= 1.13-1
Requires: pcre >= 8.12-3
Requires: zlib >= 1.2.5-4

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

Install wget if you need to retrieve large numbers of files with HTTP or FTP,
or if you need a utility for mirroring web sites or FTP directories.

Note: This version is compiled with SSL support.


%prep
%setup -q
%patch0 -p1 -b .aix


%build
# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"
export AR="/usr/bin/ar -X32_64"
export CC="/usr/vac/bin/xlc_r"

export CFLAGS=" -D_LARGE_FILES"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --with-ssl=openssl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-nls \
    --disable-ipv6 \
    --disable-rpath \
    --with-libidn=%{_prefix} \
    --with-libiconv-prefix=%{_prefix}

make 


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info

cd ${RPM_BUILD_ROOT}
mkdir -p usr/bin
cd usr/bin
ln -sf ../..%{_bindir}/* .


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*
#%{_datadir}/locale/*/*/*
/usr/bin/*


%changelog
* Wed Jan 13 2016 Michael Wilson michael.a.wilson@atos.net> 1.17.1-1
- Update to version 1.17.1 for 2016Q1 priority list

* Thu Nov 06 2014 Gerard Visiedo gerard.visiedo@bull.net> 1.16-1
- Update to version 1.16 including  critical flaw security fix

* Tue Oct 23 2012 Gerard Visiedo gerard.visiedo@bull.net> 1.14-1
-  Update to version 1.14-1

* Thu Feb 9 2011 Patricia Cugny <patricia.cugny@bull.net> 1.13.4-2
- Update to version 1.13.4-2.
- Build for AIX 6.1
- Build using system-provided OpenSSL.

* Mon Jan 21 2008 Reza Arbab <arbab@austin.ibm.com> 1.9.1-2
- Rebuild using system-provided OpenSSL.

* Fri May 13 2005 David Clissold <cliss@austin.ibm.com> 1.9.1-1
- Update to version 1.9.1

* Wed Jun 09 2004 David Clissold <cliss@austin.ibm.com> 1.9-2
- Add ability to build with SSL mode.

* Tue Nov 25 2003 David Clissold <cliss@austin.ibm.com> 1.9-1
- Version 1.9; add patch so it builds with vac compiler

* Mon Jan 28 2002 David Clissold <cliss@austin.ibm.com>
- Version 1.8.1

* Tue Nov 27 2001 David Clissold <cliss@austin.ibm.com>
- Version 1.7.1

* Thu Jul 05 2001 Marc Stephenson <marc@austin.ibm.com>
- Version 1.7

* Tue Apr 03 2001 David Clissold <cliss@austin.ibm.com>
- Build with -D_LARGE_FILES enabled (for >2BG files)

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- don't permit chmod 777 on symlinks (#4725).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
