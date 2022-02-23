Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl 
Version: 7.21.4
Release: 2
License: MIT
Group: Applications/Internet
Source0: http://curl.haxx.se/download/%{name}-%{version}.tar.gz
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel >= 0.9.8, pkg-config, libidn-devel >= 1.15
BuildRequires: libssh2-devel >= 1.2.2, zlib-devel
Requires: libidn >= 1.15, openssl >= 0.9.8, zlib, libssh2 >= 1.2.2

%define DEFCC cc

%description
CURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.


%package devel
Summary: Files needed for building applications with libcurl
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libidn-devel, openssl-devel >= 0.9.8, pkg-config, zlib-devel, libssh2-devel

%description devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The curl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.


%prep
%setup -q 


%build
export CC="/usr/vac/bin/xlc_r"
export RM="/usr/bin/rm -f"
# Use the default compiler for this platform - gcc otherwise
if [[ -z "$CC" ]]
then
    if test "X`type %{DEFCC} 2>/dev/null`" != 'X'; then
       export CC=%{DEFCC}
    else
       export CC=gcc
    fi
fi
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS=$RPM_OPT_FLAGS

./configure \
    --prefix=%{_prefix} \
    --mandir=%{_prefix}/man \
    --enable-shared --enable-static
make 

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :


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

