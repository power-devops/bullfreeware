Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name:    curl 
Version: 7.47.1
Release: 1
License: MIT
Group:   Applications/Internet
Source0: http://curl.haxx.se/download/%{name}-%{version}.tar.gz
Source1: http://curl.haxx.se/download/%{name}-%{version}.tar.gz.asc
Source2: curlbuild.h
Patch0:  %{name}-%{version}-events.patch
URL: http://curl.haxx.se/
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel >= 1.0.2g, pkg-config, libidn-devel >= 1.24
BuildRequires: libssh2-devel >= 1.2.7, zlib-devel
BuildRequires: openldap-devel >= 2.4.24
Requires: libidn >= 1.24, openssl >= 1.0.0d, zlib, libssh2 >= 1.2.7

%define DEFCC cc

%description
CURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

The library is available as 32-bit and 64-bit.

%package devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libidn-devel, openssl-devel >= 1.0.0d, pkg-config, zlib-devel, libssh2-devel


%description devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The curl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.



%prep
%setup -q 
%patch0 -p1


%build
PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
CONFIG_SHELL=/usr/bin/ksh
CONFIGURE_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar"

# first build the 64-bit version
export OBJECT_MODE=64
export CC="/usr/vac/bin/xlc_r -q64"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --enable-static
gmake 

# To be done after after having built/installed the RPMs
(gmake -k check ; /usr/sbin/slibclean ; echo "For not breaking %build phase if any test error")

cp lib/.libs/libcurl.so.4 .
cp include/curl/curlbuild.h curlbuild-ppc64.h

make distclean

# now build the 32-bit version
export OBJECT_MODE=32
export CC="/usr/vac/bin/xlc_r"

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --enable-static
gmake

# To be done after after having built/installed the RPMs
(gmake -k check ; /usr/sbin/slibclean ; echo "For not breaking %build phase if any test error")

# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
$AR -X64 -q lib/.libs/libcurl.a ./libcurl.so.4


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

mv ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild-ppc32.h
mv curlbuild-ppc64.h ${RPM_BUILD_ROOT}%{_includedir}/curl
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_includedir}/curl/curlbuild.h


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/$dir
    cd usr/$dir
    ln -sf ../..%{_prefix}/$dir/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc CHANGES README* COPYING
%doc docs/BUGS docs/FAQ docs/FEATURES
%doc docs/MANUAL docs/RESOURCES
%doc docs/TheArtOfHttpScripting docs/TODO
%{_bindir}/curl
%{_libdir}/*.a
%{_mandir}/man1/curl.1
/usr/bin/curl
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS
%{_bindir}/curl-config*
%{_includedir}/%{name}
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1
%{_mandir}/man3/*
/usr/bin/curl-config*
/usr/include/*
/usr/lib/*.la


%changelog
* Mon Mar 21 2016 Tony Reix <tony.reix@atos.net> - 7.47.1-1
- Update version to 7.47.1 on 32 and 64 bit

* Wed Jul 01 2015 Tony Reix <tony.reix@atos.net> - 7.43.0-1
- Update version to 7.43.0 on 32 and 64 bit

* Mon Oct 22 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.28.0-1
- update version to 7.28.0 on 32 and 64 bit

* Thu Mar 29 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 7.21.4-2
- Port on Aix6.1

* Fri Mar 04 2011 Patricia Cugny <patricia.cugny@bull.net> - 7.21.4-1
- updated to version 7.21.4
- remove option to flip on/off compile with SSL.

* Mon Oct 27 2003 David Clissold <cliss@austin.ibm.com>
- Add option to flip on/off compile with SSL.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Apr 30 2002 David Clissold <cliss@austin.ibm.com>
- First version for AIX Toolbox.

