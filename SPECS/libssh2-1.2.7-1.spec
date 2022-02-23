Name:           libssh2
Version:        1.2.7
Release:        1
Summary:        A library implementing the SSH2 protocol

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.libssh2.org/
Source0:        http://www.libssh2.org/download/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:  zlib-devel
Requires: openssl >= 0.9.8
Requires: zlib

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        docs 
Summary:        Documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    docs
The %{name}-docs package contains man pages and examples for
developing applications that use %{name}.


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}
  for dir in lib include
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.a
/usr/lib/*.a


%files docs
%defattr(-,root,system,-)
%doc COPYING HACKING example/
%{_mandir}/man?/*


%files devel
%defattr(-,root,system,-)
%doc COPYING 
%{_includedir}/*
%{_libdir}/*.la
/usr/include/*
/usr/lib/*.la

%changelog
* Fri Mar 04 2011 Patricia Cugny <patricia.cugnt@bull.net> - 1.2.7-1
- first version for AIX V5.3 and higher
