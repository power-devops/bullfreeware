# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define		_libdir64 %{_prefix}/lib64
%global     _plugindir2 %{_libdir}/sasl2
%global     _plugindir2_64 %{_libdir64}/sasl2

%define  name		cyrus-sasl
%define release		1
%define version 	2.1.27

%define API_VERSION 3

Summary: 	Simple Authentication and Security Layer (SASL).
License: 	GPL
Name: 		%{name}
Release: 	%{release}
Version:	%{version}
Group: 		Development/Tools

Source0: 	%{name}-%{version}.tar.gz
Source1000:	%{name}-%{version}-%{release}.build.log


BuildRequires: libgcc >= 6.3.0-1
Requires: libgcc >= 6.3.0-1
Requires:	db >= 4.8.24


# # %ifos aix6.1
# # Requires: AIX-rpm >= 6.1.0.0
# # Requires: AIX-rpm < 6.2.0.0
# # %endif
# # %ifos aix7.1
# # Requires: AIX-rpm >= 7.1.0.0
# # Requires: AIX-rpm < 7.2.0.0
# # %endif
# # %ifos aix7.2
# # Requires: AIX-rpm >= 7.2.0.0
# # Requires: AIX-rpm < 7.3.0.0
# # %endif

%description
Simple Authentication and Security Layer (SASL) is a framework for authentication
and data security in Internet protocols.
It decouples authentication mechanisms from application protocols, in theory allowing
any authentication mechanism supported by SASL to be used in any application protocol
that uses SASL.

%package devel
Group: Development/Tools
Summary: Development package for the cyrus-sasl
Requires: cyrus-sasl = %{version}-%{release}

%description devel
Development package for the cyrus-sasl.

%package plain
Requires: cyrus-sasl = %{version}-%{release}
Summary: PLAIN and LOGIN authentication support for Cyrus SASL

%description plain
The %{name}-plain package contains the Cyrus SASL plugins which support
PLAIN and LOGIN authentication schemes.

%package md5
Requires: cyrus-sasl = %{version}-%{release}
Summary: CRAM-MD5 and DIGEST-MD5 authentication support for Cyrus SASL

%description md5
The %{name}-md5 package contains the Cyrus SASL plugins which support
CRAM-MD5 and DIGEST-MD5 authentication schemes.

%package scram
Requires: cyrus-sasl = %{version}-%{release}
Summary: SCRAM auxprop support for Cyrus SASL

%description scram
The %{name}-scram package contains the Cyrus SASL plugin which supports
the SCRAM authentication scheme.

%prep
%setup -q
# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64 -B"

build_cyrus() {
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--sbindir=%{_sbindir} \
		--infodir=%{_infodir} \
		--mandir=%{_mandir} \
		--enable-login \
		--enable-shared \
		--disable-gssapi \
		--with-plugindir=$1/sasl2

	make
}

#Build on 64bit mode
export OBJECT_MODE=64
cd 64bit
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export CC="gcc -maix64"
export CC_FOR_BUILD=$CC

build_cyrus %{_libdir64}


#Build on 32bit mode
export OBJECT_MODE=32
cd ../32bit
export CC="gcc -maix32"
export CC_FOR_BUILD=$CC
export CFLAGS="-D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_cyrus %{_libdir}



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -X32_64"

# install on 64bit mode
export OBJECT_MODE=64
cd 64bit
make install DESTDIR=${RPM_BUILD_ROOT}

# (
# 	cd utils/.libs
# 	cp ./* ${RPM_BUILD_ROOT}%{_sbindir}
# )


(
	# Change 64bit binaries' name
    cd  ${RPM_BUILD_ROOT}%{_sbindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)
# mkdir -p ${RPM_BUILD_ROOT}%{_libdir}64/sasl2
# mv ${RPM_BUILD_ROOT}%{_libdir}/sasl2/* ${RPM_BUILD_ROOT}%{_libdir}64/sasl2/

export OBJECT_MODE=32
cd ../32bit

make install DESTDIR=${RPM_BUILD_ROOT}


mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sasl2
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/saslauthd
mkdir -p ${RPM_BUILD_ROOT}/var/state/saslauthd

#cp %{SOURCE1} ${RPM_BUILD_ROOT}/etc/sendmail.cf
#cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_sbindir}     
#chmod +x ${RPM_BUILD_ROOT}%{_sbindir}/sendmail 

# (
# 	cd utils/.libs
# 	cp ./* ${RPM_BUILD_ROOT}%{_sbindir}
# )


(
	# Change 32bit binaries' name and make default link towards 64bit
    cd  ${RPM_BUILD_ROOT}/%{_sbindir}
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
		mv $fic "$fic"_32
		ln -sf "$fic"_64 $fic
    done
)


(
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	for f in libsasl2 ; do
		# Extract .so from 64bit .a libraries and add them to the 32bit .a libraries.
		${AR} -x ${f}.a
		${AR} -q -X64 ${RPM_BUILD_ROOT}%{_libdir}/${f}.a ${f}.so.%{API_VERSION}

		# Create links from /lib64 to /lib
		rm -f ${f}.a
		ln -sf ../lib/${f}.a ${f}.a
	done
)

(
	# By default, make install will create plugins inside .a files.
	# However, dlopen inside the software doesn't know how to open .a files
	# Instead, just extract .so files and let the code as is.
	# Note: there is no tests on this part, so I don't know if it does really
	# work, anyway...
	cd ${RPM_BUILD_ROOT}%{_plugindir2}
	for f in lib*.a; do
		${AR} -x ${f}
		rm ${f}
	done

	cd ${RPM_BUILD_ROOT}%{_plugindir2_64}
	for f in lib*.a; do
		${AR} -x ${f}
		rm ${f}
	done
)

# (
# cd ${RPM_BUILD_ROOT}
# for dir in sbin
# do
#    mkdir -p usr/$dir
#    cd usr/$dir
#    ln -sf ../..%{_prefix}/$dir/* .
#    cd -
# done
# )



# cd ${RPM_BUILD_ROOT}
# for dir in lib/sasl2 include/sasl lib/pkgconfig lib64/sasl2 lib64/pkgconfig
# do
#    mkdir -p usr/$dir
#    cd usr/$dir
#    ln -sf ../../..%{_prefix}/$dir/* .
#    cd -
# done

# cd ${RPM_BUILD_ROOT}/usr/lib
# for f in libsasl2.a libsasl2.la libsasl2.so.3 libsasl2.so.3.0.0
# do
#    ln -sf ../../..%{_prefix}/lib/$f .
# done

# cd ${RPM_BUILD_ROOT}/usr/lib64
# for f in libsasl2.a libsasl2.la libsasl2.so.3 libsasl2.so.3.0.0
# do
#    ln -sf ../../..%{_prefix}/lib64/$f .
# done

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
%doc 32bit/AUTHORS 32bit/doc/html/*.html
%{_sbindir}/pluginviewer*
%{_sbindir}/saslauthd*
%{_sbindir}/testsaslauthd*
%{_sbindir}/saslpasswd2*
%{_sbindir}/sasldblistusers2*
%config(noreplace) %{_sysconfdir}/sysconfig/saslauthd
%{_libdir}/lib*.a
%{_libdir64}/lib*.a

%dir %{_sysconfdir}/sasl2
%dir %{_plugindir2}/
%dir %{_plugindir2_64}/
%{_plugindir2}/*anonymous*.so*
%{_plugindir2}/*sasldb*.so*
%{_plugindir2}/*otp*.so*
%{_plugindir2_64}/*anonymous*.so*
%{_plugindir2_64}/*sasldb*.so*
%{_plugindir2_64}/*otp*.so*

%dir /var/state/saslauthd

%{_mandir}/man8/*

%files plain
%defattr(-,root,system,-)
%{_plugindir2}/*plain*.so*
%{_plugindir2}/*login*.so*
%{_plugindir2_64}/*plain*.so*
%{_plugindir2_64}/*login*.so*

%files md5
%defattr(-,root,system,-)
%{_plugindir2}/*crammd5*.so*
%{_plugindir2}/*digestmd5*.so*
%{_plugindir2_64}/*crammd5*.so*
%{_plugindir2_64}/*digestmd5*.so*

%files scram
%defattr(-,root,system,-)
%{_plugindir2}/libscram.so*
%{_plugindir2_64}/libscram.so*


%files devel
%defattr(-,root,system,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir64}/pkgconfig/*
%{_mandir}/man3/*
# /usr/include/sasl/*.h

%changelog
* Tue Nov 19 2019 Clément Chigot <clement.chigot@atos.net> - 2.1.27-1
- BullFreeware Mass Rebuild for clean builds
- Move tests to %check section
- Remove /usr links
- Add scram, md5 and plain RPMS

* Wed Aug 1 2018 Reshma V Kumar<reskumar@in.ibm.com> - 2.1.26-3
- Rebuild adding Requires: libgcc >= 6.3.0

* Wed Jul 18 2018 Reshma V Kumar<reskumar@in.ibm.com> - 2.1.26-2
- Update to version 2.1.26 for AIX toolbox

* Fri Dec 16 2016 Juan P Villamizer <jpvillam@us.ibm.com> 2.1.26-1.
- Update to version 2.1.26.
- Include sendmail binary & configuration files. Sendmail included with this rpm is
- compiled to use sasl authentication. So sendmail depends on libsasl.a.


