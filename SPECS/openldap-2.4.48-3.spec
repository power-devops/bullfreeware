# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

# By default, OpenSSL LPP is used
# To choose OpenSSL RPM: rpmbuild --without ibm_SSL *.spec
%bcond_without ibm_SSL

%define base_release 3
%define release %{base_release}%{?without_ibm_SSL:opensourcessl}

Summary: The configuration files, libraries, and documentation for OpenLDAP
Name: openldap
Version: 2.4.48
Release: %{release}
License: OpenLDAP
Group: System Environment/Daemons
URL: http://www.openldap.org/
Source: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz

Source1000: %{name}-%{version}-%{base_release}.build.log

# Patches for 2.4
Patch0: openldap-2.4.48-config.patch
# Patch1: openldap-2.0.11-ldaprc.patch
Patch2: openldap-2.4.11-aix-conf.patch

Patch3: %{name}-%{version}-libtool-add-hardcode-direct-absolute.patch

BuildRequires: libtool >= 1.5.6-2, db >= 4.8
BuildRequires: cyrus-sasl-devel >= 2.1.27-1, unixODBC-devel
Requires: cyrus-sasl >= 2.1.27-1
Obsoletes: compat-openldap < 2.4

%if %{with ibm_SSL}
# Workaround to use AIX libssl.a and libcrypto.a needs OpenSource sed
# BuildRequires: sed
%else
BuildRequires: openssl-devel >= 1.0.2g
Requires: openssl >= 1.0.2g
%endif


%define _libdir64 %{_prefix}/lib64

%ifos aix5.3
%define buildhost powerpc-ibm-aix5.3.0.0
%endif
%ifos aix6.1
%define buildhost powerpc-ibm-aix6.1.0.0
%endif
%ifos aix7.1
%define buildhost powerpc-ibm-aix7.1.0.0
%endif
%ifos aix7.2
%define buildhost powerpc-ibm-aix7.2.0.0
%endif

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%if %{with gcc_compiler}
This version has been compiled with GCC.
%else
This version has been compiled with XLC.
%endif


%package devel
Summary: OpenLDAP development libraries and header files
Group: Development/Libraries
Requires: openldap = %{version}-%{release}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.


%package servers
Summary: LDAP server
License: OpenLDAP
Requires: openldap = %{version}-%{release}, libdb-utils

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.

%package clients
Summary: LDAP client utilities
Requires: openldap = %{version}-%{release}

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.



%prep

# Check that ICU4C.adt is installed for "unicode/utypes.h"
if ! lslpp -L | grep -q "ICU4C.adt" ; then
	echo "Error: lpp ICU4C.adt must be installed to provide \"unicode/utypes.h\""
	echo "Aborting..."
	exit 1
fi

%setup -q
%patch0 -p1 -b .config
#%patch1 -p1 -b .ldaprc
%patch2 -p1 -b .aix-conf
%patch3 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export INSTALL=/opt/freeware/bin/install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export RM="/usr/bin/rm -f"
export M4=/opt/freeware/bin/m4
GLOBAL_CC_OPTIONS="-O2 -DMDB_USE_ROBUST=0 "

export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# OpenSSL's header and library dependencies.
OPENSSL_CPPFLAGS="-I/opt/freeware/include/openssl"
# CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
# OPENSSL_LDFLAGS="-L/opt/freeware/lib"
# LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS


# Choose XLC or GCC
%if %{with gcc_compiler}
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
# export LDFLAGS=""
export FLAG32="-maix32"
export FLAG64="-maix64"

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"
export CXX__="/usr/vacpp/bin/xlC"
# export LDFLAGS=""
export FLAG32="-q32"
export FLAG64="-q64"

echo "CC Version:"
$CC__ -qversion

%endif

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

build_openldap() {
	LIBS=-lpthread \
		./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=$1 \
		--libexecdir=$1 \
		--enable-local --enable-rlookups \
		--enable-passwd \
		--enable-cleartext \
		--enable-lmpasswd \
		--enable-dynamic \
		--enable-shared \
		--disable-static \
		--disable-sql \
		--enable-slapd \
		--enable-bdb \
		--enable-hdb \
		--enable-ldap \
		--enable-meta \
		--enable-monitor \
		--enable-null \
		--enable-shell \
		--enable-relay \
		--enable-sql \
		--host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \

# # # Deactivate Workaround
# # %if %{with ibm_SSL}
# # 	# Workaround to use AIX OpenSSL
# # 	find . -name "Makefile" | xargs /opt/freeware/bin/sed -i "s|-lssl -lcrypto|/usr/lib/libssl.a /usr/lib/libcrypto.a|g"
# # %endif


	gmake depend

	# # This patches libtool so that it makes use of -llber instead of :
	# #	/opt/freeware/lib*/liblber.a which generates a hard libpath
	# /opt/freeware/bin/patch -p1 -b --suffix .llber64 < %{SOURCE1064}

	gmake # LIBTOOL="$libtool"
}


# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CC="${CC64}"
export CXX="${CXX64}"
export CFLAGS="$GLOBAL_CC_OPTIONS"
export CXXFLAGS="$GLOBAL_CC_OPTIONS"

# libtool='%{_builddir}/openldap-%{version}/64bit/libtool'


export CPPFLAGS="$OPENSSL_CPPFLAGS"
export LDFLAGS="$OPENSSL_LDFLAGS -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

# Trouble with make if MAKE not set as below:
# export MAKE="/opt/freeware/bin/gmake --trace -j8"
# echo "MAKE: " $MAKE

build_openldap %{_libdir64}


# Patch the libdir= in the .la file with the path to the built libraries.
#cat libraries/liblber/liblber.la | awk -F= \
#       '{
#	if($1=="libdir")
#        	print "libdir=$RPM_BUILD_ROOT/opt/freeware/lib64";
#	else
#        	print $0
#	}' > /tmp/LIBLBER
#cp /tmp/LIBLBER libraries/liblber/liblber.la


#now build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"
export CFLAGS="$GLOBAL_CC_OPTIONS"
export CXXFLAGS="$GLOBAL_CC_OPTIONS"

# libtool='%{_builddir}/openldap-%{version}/32bit/libtool'


export CPPFLAGS="$OPENSSL_CPPFLAGS"
export LDFLAGS="$OPENSSL_LDFLAGS -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_openldap %{_libdir}

# LIBS=-lpthread \
# ./configure \
#     --prefix=%{_prefix} \
#     --libdir=%{_libdir} \
#     --libexecdir=%{_libdir} \
#     --enable-local --enable-rlookups \
#     --enable-passwd \
#     --enable-cleartext \
#     --enable-lmpasswd \
#     --enable-dynamic \
#     --enable-shared \
#     --disable-static \
#     --disable-sql \
#     --enable-slapd \
#     --without-keberos \
#     --enable-plugins \
#     --enable-multimaster \
#     --enable-bdb \
#     --enable-hdb \
#     --enable-ldap \
#     --enable-ldbm \
#     --with-ldbm-api=%{ldbm_backend} \
#     --enable-meta \
#     --enable-monitor \
#     --enable-null \
#     --enable-shell \
#     --enable-relay \
#     --enable-sql \
#     --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
#     --libexecdir=%{_libdir} 

# ${MAKE} depend

# # This patches libtool so that it makes use of -llber instead of :
# #	/opt/freeware/lib*/liblber.a which generates a hard libpath
# /opt/freeware/bin/patch -p1 -b --suffix .llber32 < %{SOURCE1032}

# ${MAKE} # LIBTOOL="$libtool"


# Patch the libdir= in the .la file with the path to the built libraries.
#cat libraries/liblber/liblber.la | awk -F= \
#       '{
#	if($1=="libdir")
#        	print "libdir=$RPM_BUILD_ROOT/opt/freeware/lib";
#	else
#        	print $0
#	}' > /tmp/LIBLBER
#cp /tmp/LIBLBER libraries/liblber/liblber.la
#rm -f /tmp/LIBLBER


%install
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

[ -e /opt/freeware/lib64/liblber.a ] || ln -s /opt/freeware/lib/liblber.a /opt/freeware/lib64/liblber.a

# Installing in 64bit mode
cd 64bit

export OBJECT_MODE=64

# libtool='%{_builddir}/openldap-%{version}/64bit/libtool'

# Create symlink from lib64 to: 64bit/libraries/${dirlib}/.libs/${lib}

# mkdir -p $RPM_BUILD_ROOT/%{_libdir64}
# (
# 	for lib in liblber.a liblber.la libldap.la
# 	do
# 		dirlib="`echo  ${lib} | cut -d"." -f1`"
# 		if [ ! -e $RPM_BUILD_ROOT/%{_libdir64}/${lib} ]; then
# 			ln -s %{_builddir}/openldap-%{version}/64bit/libraries/${dirlib}/.libs/${lib} $RPM_BUILD_ROOT/%{_libdir64}/${lib}
# 		fi
# 	done
# )

# Directory build: change shtool (+-X32_64)
cd %{_builddir}/openldap-%{version}/64bit/build
sed "s;strip \$dsttmp || shtool_exit;strip -X32_64 \$dsttmp || shtool_exit;" shtool >shtool.tmp
mv -f shtool.tmp shtool
chmod +x shtool
cd -

gmake install DESTDIR=$RPM_BUILD_ROOT

# bin : create the *_64
(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  rm -f ldapadd
  for f in * ; do
      mv -f ${f} ${f}_64
  done
  ln -s ldapmodify_64 ldapadd_64
)

# move slapd out of %{_libdir64}
mv ${RPM_BUILD_ROOT}%{_libdir64}/slapd ${RPM_BUILD_ROOT}%{_sbindir}/slapd_64
for i in acl add auth cat dn index passwd schema test ; do
    rm -f ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}
done

# set up tools as symlinks to slapd
for i in acl add auth cat dn index passwd schema test ; do
    ln -s slapd_64 ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}_64
done


# building in 32bit mode
cd ../32bit

# rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.a
# rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.la
# rm -f ${RPM_BUILD_ROOT}%{_libdir}/libldap.la

export OBJECT_MODE=32

# libtool='%{_builddir}/openldap-%{version}/32bit/libtool'

# mkdir -p $RPM_BUILD_ROOT/%{_libdir}
# for lib in liblber.a liblber.la libldap.la 
# do
#    dirlib="`echo  ${lib} | cut -d"." -f1`"
#    if [ ! -e $RPM_BUILD_ROOT/%{_libdir}/${lib} ]; then
#        ln -s %{_builddir}/openldap-%{version}/32bit/libraries/${dirlib}/.libs/${lib} $RPM_BUILD_ROOT/%{_libdir}/${lib}
#    fi
# done

cd %{_builddir}/openldap-%{version}/32bit/build
sed "s;strip \$dsttmp || shtool_exit;strip -X32_64 \$dsttmp || shtool_exit;" shtool >shtool.tmp
mv -f shtool.tmp shtool
chmod +x shtool
cd -

gmake install DESTDIR=$RPM_BUILD_ROOT
(
	cd ${RPM_BUILD_ROOT}%{_bindir}
	rm -f ldapadd
	for f in $(ls -1| grep -v -e _32 -e _64) ; do
		mv -f ${f} ${f}_32
		ln -sf "$f"_64 $f
	done
	ln -s ldapmodify_32 ldapadd_32
	ln -sf ldapadd_64 ldapadd
)

# setup directories for TLS certificates
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/openldap/certs

# move slapd out of %{_libdir}
mv ${RPM_BUILD_ROOT}%{_libdir}/slapd ${RPM_BUILD_ROOT}%{_sbindir}/slapd_32
for i in acl add auth cat dn index passwd schema test ; do
    rm -f ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}
done

# set up tools as symlinks to slapd
for i in acl add auth cat dn index passwd schema test ; do
    ln -s slapd_32 ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}_32
done

#rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.a
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.la
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/libldap.la

# (
#   cd ${RPM_BUILD_ROOT}%{_libdir}
#   for f in *.a ; do
#       /usr/bin/ar -X32 -x ${f}
#   done
#   cd ${RPM_BUILD_ROOT}%{_libdir64}
#   for f in *.a ; do
#       /usr/bin/ar -X64 -x ${f}
#   done
# )

(
	# Extract .so from 64bit .a libraries and create links from /lib64 to /lib
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	for f in liblber-2.4.a libldap-2.4.a libldap_r-2.4.a; do
		${AR} -x ${f}
		rm -f ${f}
		ln -sf ../lib/${f} ${f}
	done
)

(
	# Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
	for i in lber-2.4 ldap-2.4 ldap_r-2.4 ; do
		${AR} -X64 -q lib${i}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib${i}.so*
		# rm ${RPM_BUILD_ROOT}%{_libdir64}/lib${i}.so*
	done
)

# (
#   cd ${RPM_BUILD_ROOT}
#   for dir in bin sbin include lib lib64
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

ulimit -m unlimited

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%pre
# add the "ldap" group only if it does not yet exist
result=`/usr/sbin/lsgroup ldap | /usr/bin/awk '{ print $1 }' 2>/dev/null`
if [ "${result}" != "ldap" ] ; then
    /usr/bin/mkgroup ldap 2> /dev/null || :
fi


%preun 
if [ "$1" = "0" ] ; then
  /sbin/service ldap stop > /dev/null 2>&1 || :
fi
# remove "ldap" group
/usr/sbin/rmgroup ldap || :


%files
%defattr(-,root,system)
%doc 32bit/ANNOUNCEMENT
%doc 32bit/CHANGES
%doc 32bit/COPYRIGHT
%doc 32bit/LICENSE
%doc 32bit/README
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/certs
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%{_libdir}/liblber*.a
%{_libdir}/libldap*.a
%{_libdir64}/liblber*.a
%{_libdir64}/libldap*.a
%{_mandir}/man5/ldif.5*
%{_mandir}/man5/ldap.conf.5*


%files servers
%defattr(-,root,system)
%doc 32bit/contrib/slapd-modules/smbk5pwd/README
%doc 32bit/doc/guide/admin/*.html
%doc 32bit/doc/guide/admin/*.png
%doc 32bit/servers/slapd/back-perl/SampleLDAP.pm
%doc 32bit/servers/slapd/back-perl/README
# %{_libdir}/openldap/*
# %{_libdir64}/openldap/*
%{_sbindir}/sl*
%{_mandir}/man8/*
%{_mandir}/man5/slapd*.5*
%{_mandir}/man5/slapo-*.5*
# obsolete configuration
%ghost %config(noreplace,missingok) %attr(0640,ldap,ldap) %{_sysconfdir}/openldap/slapd.conf

%files clients
%defattr(-,root,system)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,system)
%doc 32bit/doc/drafts 32bit/doc/rfc
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Wed Jan 29 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 2.4.48-3
- Bullfreeware OpenSSL removal
- Add cyrus-sasl require. It is needed to work

* Tue Nov 19 2019 Clément Chigot <clement.chigot@atos.net - 2.4.48-2
- BullFreeware Compatibility Improvements
- Built with IBM SSL by default
- Move tests to %check section
- Remove Requires: cyrus-sasl. It is only needed when building.
- Remove old configure options not available anymore
- Remove .so files
- Add servers and clients packages
- Add BuildRequires: unixODBC-devel

* Wed Sep 25 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.48-1
- Update to fix CVE-2019-13565

* Tue May 21 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.4.46-2
- Rebuild with cyrus-sasl 2.1.26-4 and mdb support


* Mon May 20 2019 Tony Reix <tony.reix@atos.net> - 2.4.44-6
- Use harcoded_link=no in libtool (no hard-coded LIBPATH for liblber.a)

* Tue Feb 07 2017 Tony Reix <tony.reix@atos.net> - 2.4.44-5
- Strip -e isolated .so files.

* Thu Oct 20 2016 Jean Girardet <Jean.girardet@atos.net> - 2.4.44-4
- Add links in /usr and modify link in bin sbin

* Thu Oct 13 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 2.4.44-3
- Fixed bad reference to liblber.a

* Mon Sep 26 2016 Jean Girardet <jean.girardet@atos.net> - 2.4.44-2
- Update to 2.4.44 Build on 32 and 64bit

* Thu Jun 20 2013 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.35-1
- Update to 2.4.35 Build on 32 and 64bit

* Tue Feb 07 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 2.4.24-1
- Inital port on Aix 6.1

* Wed Mar 2 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.4.24-0
- Update to 2.4.24

* Mon Dec 1 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.11-2
- Bug fix during rpm installation + adding devel package

* Thu Sep 25 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.11
- Update to 2.4.11

* Wed Jul 9 2008 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 2.4.8
- Port on AIX plateform
