# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, curl is built with SSL support
# To disable SSL, rpmbuild --without SSL *.spec
%bcond_without SSL

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

%define	_libdir64 %{_prefix}/lib64


Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.21.2
Release: 1
License: GPLv3+
Group: Applications/Internet
Url: https://www.gnu.org/software/%{name}/
Source0: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

# Patch0: %{name}-1.20.3-aix.patch

Provides: webclient
Requires: /sbin/install-info, info

BuildRequires: gettext
BuildRequires: libiconv >= 1.13.1
BuildRequires: pcre-devel >= 8.43
BuildRequires: zlib-devel >= 1.2.5-4
# To create info.gz
BuildRequires: gzip

Requires: gettext
Requires: libiconv >= 1.13-1
Requires: pcre >= 8.43
Requires: zlib >= 1.2.5-4

%if %{without ibm_SSL}
BuildRequires: openssl-devel >= 1.0.2g
Requires: openssl >= 1.0.2g
%endif


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
# %patch0 -p1 -b .aix

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# work around strange libtool error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export AR="/usr/bin/ar -X32_64"

export CFLAGS=" -D_LARGE_FILES -O2"

%if %{with SSL} && %{with ibm_SSL}
export OPENSSL_LIBS="-lssl -lcrypto"
export OPENSSL_CFLAGS="-lssl -lcrypto"
%endif

build_wget() {
    # Set --with-included-libunistring to avoid having hardcoded path for
    # libunistring in wget binary.
    ./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--libdir=$1 \
	--enable-largefile \
	--enable-opie \
	--enable-digest \
	--enable-nls \
	--disable-ipv6 \
	--with-ssl=openssl \
	--with-libiconv-prefix=%{_prefix} \
	--with-included-libunistring \
%if %{without SSL}
    --without-ssl
%endif


    gmake

    # make check
}

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="/opt/freeware/bin/gcc -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_wget %{_libdir64}


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="/opt/freeware/bin/gcc -maix32"

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_wget %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
	# Change 64bit binaries' name
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)
cd ..

# install 32-bit version
cd 32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
(
	# Change 32bit binaries' name and make default link towards 64bit
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in $(ls | grep -v -e _32 -e _64)
	do
		mv ${f} ${f}_32
		ln -sf ${f}_64 ${f}
	done
)


rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip --best ${RPM_BUILD_ROOT}%{_infodir}/*.info

# cd ${RPM_BUILD_ROOT}
# mkdir -p usr/bin
# cd usr/bin
# ln -sf ../..%{_bindir}/* .

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


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
%doc 32bit/AUTHORS 32bit/MAILING-LIST 32bit/NEWS 32bit/README 32bit/COPYING 32bit/doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*
#%{_datadir}/locale/*/*/*
# /usr/bin/*


%changelog
* Mon Apr 19 2021 Clément Chigot <clement.chigot@atos.net> 1.21.2-1
- Update to 1.21.2
- Remove --disable-rpath patchs

* Thu Oct 08 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.20.3-5
- Update to 1.20.3

* Wed Oct 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.20.3-4
- Simplfy release numberiong

* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.20.3-3
- Bullfreeware OpenSSL removal

* Thu Dec 19 2019 Clément Chigot <clement.chigot@atos.net> - 1.20.3-2
- BullFreeware Compatibility Improvements
- Switch to OpenSSL LPP
- Move tests to %check section
- Remove /usr links
- Remove libidn dependency
   Only libidn2 is supported now, but we do not have at the moment.

* Thu Feb 21 2019 Ravi Hirekurabar <rhirekur@in.ibm.com> - 1.20.3-1
- Updated to version 1.20.3
- This version fixes following CVE's
- CVE-2019-5953 CVE-2018-20483  

* Mon Jan 07 2019 Michael Wilson <michael.a.wilson@atos.net> 1.20.1-1
- Update to version 1.20.1 for CVE-2018-20483 fix

* Tue Feb 07 2017 Tony Reix <tony.reix@atos.net> 1.19-1
- Update to version 1.19

* Wed Jan 13 2016 Michael Wilson <michael.a.wilson@atos.net> 1.17.1-1
- Update to version 1.17.1 for 2016Q1 priority list

* Thu Nov 06 2014 Gerard Visiedo <gerard.visiedo@bull.net> 1.16-1
- Update to version 1.16 including  critical flaw security fix

* Tue Oct 23 2012 Gerard Visiedo gerard.visiedo@bull.net> 1.14-1
-  Update to version 1.14-1

* Thu Feb 10 2011 Patricia Cugny <patricia.cugny@bull.net> 1.13.4-2
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
