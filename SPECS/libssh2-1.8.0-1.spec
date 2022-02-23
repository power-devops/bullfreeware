Name:           libssh2
Version:        1.8.0
Release:        1
Summary:        A library implementing the SSH2 protocol

Group:          System Environment/Libraries
License:        BSD
URL:            https://www.libssh2.org/
Source0:        https://www.libssh2.org/download/%{name}-%{version}.tar.gz
Source1:        https://www.libssh2.org/download/%{name}-%{version}.tar.gz.asc
BuildRoot:      /var/tmp/%{name}-%{version}-%{release}-root

Source100: %{name}-%{version}-%{release}.build.log

Patch1:         0001-scp-do-not-NUL-terminate-the-command-for-remote-exec.patch

BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:  zlib-devel
BuildRequires:  pkg-config, make
Requires: openssl >= 0.9.8
Requires: zlib

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

The library is available as 32-bit and 64-bit.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%package        docs 
Summary:        Documentation for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    docs
The %{name}-docs package contains man pages and examples for
developing applications that use %{name}.


%prep
%setup -q

# The null terminated command for scp remote execution breaks some
# SCP/SSH server implementations
# https://bugzilla.redhat.com/show_bug.cgi?id=1489736
%patch1 -p1

%build
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"
export GREP="/usr/bin/grep"
export PATH="/usr/bin:$PATH"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
#export CC="/usr/vac/bin/xlc_r -q64"
export CC="gcc -maix64"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
gmake

(gmake -C tests check || true )

slibclean


mv ./src/.libs/%{name}.so.1 .
gmake distclean

# now build the 32-bit version
#export CC="/usr/vac/bin/xlc_r"
export CC="gcc -maix32"
./configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static
gmake

(gmake -C tests check || true )

slibclean


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ./src/.libs/%{name}.a ./%{name}.so.1


%install
export GREP="/usr/bin/grep "

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
gmake DESTDIR=${RPM_BUILD_ROOT} install

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
%doc AUTHORS COPYING README RELEASE-NOTES NEWS
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
* Tue Mar 12 2019 Michael Wilson <michael.a.wilson@atos.net> - 1.8.0-1
- Complete the port to 1.8.0 based on Fedora 30
-  scp: Do not NUL-terminate the command for remote exec
-  diffie_hellman_sha256: Convert bytes to bits (CVE-2016-0787) 1.7.0

* Wed Jun 21 2017 Tony Reix <tony.reix@bull.net> - 1.8.0-1
- Fix issue with libssl.so and libcrypto.so

* Fri Oct 19 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.4.2-1
- Update to version 1.4.2 and build on 32 and 64 bit

* Thu Mar 29 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 1.2.7-2
- Port on Aix6.1

* Fri Mar 04 2011 Patricia Cugny <patricia.cugnt@bull.net> - 1.2.7-1
- first version for AIX V5.3 and higher
