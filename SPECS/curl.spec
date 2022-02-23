# Use --define 'nossl 1' on the command line to disable SSL detection
%{!?nossl:%define SSL 1}
%{?nossl:%define SSL 0}

%define name curl
%define version 7.9.3
%define release 2%{!?nossl:ssl}
%define curlroot %{_builddir}/%{name}-%{version}

Summary: get a file from a FTP, GOPHER or HTTP server.
Name: %{name}
Version: %{version}
Release: %{release}
License: IBM_ILA
Group: Applications/Internet
Source: %{name}-%{version}.tar.bz2
Source1: IBM_ILA
Provides: curl
URL: http://curl.haxx.se/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}
%if %{SSL} == 1
Prereq: openssl
%endif

%description
curl is a client to get documents/files from servers, using any of the
supported protocols.  The command is designed to work without user
interaction or any kind of interactivity.

curl offers many useful tricks like proxy support, user authentication,
ftp upload, HTTP post, file transfer resume and more.

%if %{SSL} == 0
Note: this version is compiled with SSL support.
%else
Note: this version is compiled without SSL support.
%endif

%package	devel
Summary:	The includes, libs, and man pages to develop with libcurl
Group:		Development/Libraries
Requires:	curl = %{version}

%description devel
libcurl is the core engine of curl; this packages contains all the libs,
headers, and manual pages to develop applications using libcurl.

%define DEFCC cc

%prep
rm -rf %{curlroot}
%setup -q

# Add license info
cat $RPM_SOURCE_DIR/IBM_ILA > LICENSE
cat LEGAL >> LICENSE


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
if [[ "$CC" != "gcc" ]]
then
       export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
fi
export CFLAGS="$RPM_OPT_FLAGS -I/opt/freeware/include"
export CPPFLAGS="-I/opt/freeware/include"
export LDFLAGS=-L/opt/freeware/lib

./configure --prefix=%{prefix} \
%if %{SSL} == 1
        --with-ssl
%else
        --without-ssl
%endif

make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-strip

( cd $RPM_BUILD_ROOT   # same as %{buildroot}

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
 cd -
)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/*
%{_libdir}/libcurl.a
%doc CHANGES LEGAL MITX.txt MPL-1.1.txt README docs/BUGS LICENSE
%doc docs/CONTRIBUTE docs/FAQ docs/FEATURES docs/INSTALL docs/INTERNALS
%doc docs/MANUAL docs/RESOURCES docs/TODO
%doc docs/TheArtOfHttpScripting
/usr/bin/curl
/usr/lib/libcurl.a

%files devel
%defattr(-,root,root)
%doc LICENSE
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/curl/*
%{_libdir}/libcurl.la
/usr/include/curl

%changelog
* Mon Oct 27 2003 David Clissold <cliss@austin.ibm.com>
- Add option to flip on/off compile with SSL.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.

* Tue Apr 30 2002 David Clissold <cliss@austin.ibm.com>
- First version for AIX Toolbox.
