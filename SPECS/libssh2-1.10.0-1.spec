# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

%define		_libdir64 %{_prefix}/lib64

Name:           libssh2
Version: 1.10.0
Release: 1
Summary:        A library implementing the SSH2 protocol

Group:          System Environment/Libraries
License:        BSD
URL:            https://www.libssh2.org/
Source0:        https://www.libssh2.org/download/%{name}-%{version}.tar.gz

Source100: %{name}-%{version}-%{release}.build.log

# Patch1:         0001-scp-do-not-NUL-terminate-the-command-for-remote-exec.patch

BuildRequires:  zlib-devel
BuildRequires:  pkg-config, make
BuildRequires:  libgcc >= 6.3.0-1
Requires: zlib
Requires: libgcc >= 6.3.0-1

%if %{with ibm_SSL}
# Workaround to use AIX libssl.a and libcrypto.a needs OpenSource sed
# BuildRequires: sed
%else
BuildRequires: openssl-devel >= 1.0.2g
Requires: openssl >= 1.0.2g
%endif

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

# The null terminated command for scp remote execution breaks some
# SCP/SSH server implementations
# https://bugzilla.redhat.com/show_bug.cgi?id=1489736
# %patch1 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export RM="/usr/bin/rm -f"

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

build_libssh2(){
	./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=$1\
		--enable-shared --disable-static \

# # # Deactivate Workaround
# # %if %{with ibm_SSL}
# # # Workaround to use AIX OpenSSL
# # 	for f in `find . -name "Makefile"`; do
# # 		/opt/freeware/bin/sed -i "s|LTLIBSSL = .*|LTLIBSSL = /usr/lib/libssl.a /usr/lib/libcrypto.a|g" $f 
# # 		/opt/freeware/bin/sed -i "s|LIBSSL = .*|LIBSSL = /usr/lib/libssl.a /usr/lib/libcrypto.a|g" $f 
# # 	done
# # %endif

	gmake
}




# first build the 64-bit version
cd 64bit
export CC="/opt/freeware/bin/gcc -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
build_libssh2 %{_libdir64}


cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"
build_libssh2 %{_libdir}



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
cd ..

(
	# Extract .so from 64bit .a libraries and create links from /lib64 to /lib
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x libssh2.a
	rm -f libssh2.a
	ln -sf ../lib/libssh2.a libssh2.a
)

(
	# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libssh2.a		libssh2.so.1
	rm libssh2.so.1
)


# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in lib include
#   do
#     mkdir -p usr/${dir}
#     cd usr/${dir}
#     ln -sf ../..%{_prefix}/${dir}/* .
#     cd -
#   done
# )

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/COPYING 32bit/README 32bit/NEWS
%{_libdir}/*.a
# /usr/lib/*.a


%files docs
%defattr(-,root,system,-)
%doc 32bit/COPYING 32bit/example/
%{_mandir}/man?/*


%files devel
%defattr(-,root,system,-)
%doc 32bit/COPYING
%{_includedir}/*
# %{_libdir}/*.la
# /usr/include/*
# /usr/lib/*.la


%changelog
* Fri Sep 03 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 1.10.0-1
- Update to 1.10.0

* Thu Oct 08 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 1.9.0-4
- Update to 1.9.0

* Wed Oct 07 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.9.0-3
- Simplfy release numberiong

* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 1.9.0-2
- Bullfreeware OpenSSL removal

* Wed Dec 18 2019 Clément Chigot <clement.chigot@atos.net> - 1.9.0-1
- BullFreeware Compatibility Improvements
- Switch to OpenSSL LPP
- Update to 1.9.0
- Remove .la files
- Remove /usr links
- Build both 32 and 64 bits versions

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
