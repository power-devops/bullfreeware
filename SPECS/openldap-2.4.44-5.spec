# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# compiler defauft gcc
# To use xlc : --define 'gcc_compiler=0'

%{!?gcc_compiler:%define gcc_compiler 1}

Summary: The configuration files, libraries, and documentation for OpenLDAP
Name: openldap
Version: 2.4.44
Release: 5
License: OpenLDAP
Group: System Environment/Daemons
Source: ftp://ftp.OpenLDAP.org/pub/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source2: %{name}-%{version}-%{release}.build.log

# Patches for 2.4
Patch0: openldap-2.4.44-config.patch
Patch1: openldap-2.0.11-ldaprc.patch
Patch2: openldap-2.4.11-aix-conf.patch

URL: http://www.openldap.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libtool >= 1.5.6-2, openssl-devel >= 1.0.2g, db >= 4.8, unixODBC-devel >= 2.3.1
Obsoletes: compat-openldap < 2.4
Requires: openssl >= 1.0.2g, unixODBC >= 2.3.1, db >= 4.8

%define _libdir64 %{_prefix}/lib64

%define ldbm_backend berkeley

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

%if %{gcc_compiler} == 1
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


%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"

%setup -q 
%patch0 -p1 -b .config
%patch1 -p1 -b .ldaprc
%patch2 -p1 -b .aix-conf

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
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
CPPFLAGS="$OPENSSL_CPPFLAGS" ; export CPPFLAGS
OPENSSL_LDFLAGS="-L/opt/freeware/lib"
LDFLAGS="$OPENSSL_LDFLAGS" ; export LDFLAGS


# Choose XLC or GCC
%if %{gcc_compiler} == 1
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



# build on 64bit mode
export OBJECT_MODE=64
export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

libtool='%{_builddir}/openldap-%{version}/64bit/libtool'

cd 64bit

CPPFLAGS="-I%{_prefix}/include $OPENSSL_CPPFLAGS" 
LDFLAGS="-L%{_libdir64} -L%{_prefix}/lib -L/usr/lib64 -L/usr/lib $OPENSSL_LDFLAGS" 

# Trouble with make if MAKE not set as below:
export MAKE=/opt/freeware/bin/gmake
echo "MAKE: " $MAKE

LIBS=-lpthread \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --libexecdir=%{_libdir64} \
    --enable-local --enable-rlookups \
    --enable-passwd \
    --enable-cleartext \
    --enable-lmpasswd \
    --enable-dynamic \
    --enable-shared \
    --disable-static \
    --disable-sql \
    --enable-slapd \
    --without-keberos \
    --enable-plugins \
    --enable-multimaster \
    --enable-bdb \
    --enable-hdb \
    --enable-ldap \
    --enable-ldbm \
    --with-ldbm-api=%{ldbm_backend} \
    --enable-meta \
    --enable-monitor \
    --enable-null \
    --enable-shell \
    --enable-relay \
    --enable-sql \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --libexecdir=%{_libdir}

gmake depend

gmake LIBTOOL="$libtool"

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
fi


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
export OBJECT_MODE=32
export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

libtool='%{_builddir}/openldap-%{version}/32bit/libtool'

cd ../32bit

CPPFLAGS="-I%{_prefix}/include $OPENSSL_CPPFLAGS" 
LDFLAGS="-L%{_prefix}/lib -L/usr/lib $OPENSSL_LDFLAGS" 

LIBS=-lpthread \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir} \
    --enable-local --enable-rlookups \
    --enable-passwd \
    --enable-cleartext \
    --enable-lmpasswd \
    --enable-dynamic \
    --enable-shared \
    --disable-static \
    --disable-sql \
    --enable-slapd \
    --without-keberos \
    --enable-plugins \
    --enable-multimaster \
    --enable-bdb \
    --enable-hdb \
    --enable-ldap \
    --enable-ldbm \
    --with-ldbm-api=%{ldbm_backend} \
    --enable-meta \
    --enable-monitor \
    --enable-null \
    --enable-shell \
    --enable-relay \
    --enable-sql \
    --host=%{buildhost} --target=%{buildhost} --build=%{buildhost} \
    --libexecdir=%{_libdir} 

gmake depend

gmake LIBTOOL="$libtool"

if [ "%{dotests}" == 1 ]
then
    ( gmake -k check || true )
fi

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
export INSTALL=/opt/freeware/bin/install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIGURE_ENV_ARGS=/opt/freeware/bin/bash

[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

[ -e /opt/freeware/lib64/liblber.a ] || ln -s /opt/freeware/lib/liblber.a /opt/freeware/lib64/liblber.a

# building in 64bit mode
cd 64bit

export OBJECT_MODE=64

libtool='%{_builddir}/openldap-%{version}/64bit/libtool'

# Create symling from lib64 to: 64bit/libraries/${dirlib}/.libs/${lib}

mkdir -p $RPM_BUILD_ROOT/%{_libdir64}
for lib in liblber.a liblber.la libldap.la 
do
   dirlib="`echo  ${lib} | cut -d"." -f1`"
   if [ ! -e $RPM_BUILD_ROOT/%{_libdir64}/${lib} ]; then
       ln -s %{_builddir}/openldap-%{version}/64bit/libraries/${dirlib}/.libs/${lib} $RPM_BUILD_ROOT/%{_libdir64}/${lib}
   fi
done

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
      [ -L "$f" ] && continue;
      [ -f "$f" ] || continue;
      mv -f ${f} ${f}_64
  done
  ln -s ldapmodify_64 ldapadd_64
)

# move slapd out of %{_libdir64}
mv ${RPM_BUILD_ROOT}%{_libdir}/slapd ${RPM_BUILD_ROOT}%{_sbindir}/slapd_64
for i in acl add auth cat dn index passwd schema test ; do
    rm -f ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}
done

# set up tools as symlinks to slapd
for i in acl add auth cat dn index passwd schema test ; do
    ln -s slapd_64 ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}_64
done


# building in 32bit mode
cd ../32bit

rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libldap.la

export OBJECT_MODE=32

libtool='%{_builddir}/openldap-%{version}/32bit/libtool'

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
for lib in liblber.a liblber.la libldap.la 
do
   dirlib="`echo  ${lib} | cut -d"." -f1`"
   if [ ! -e $RPM_BUILD_ROOT/%{_libdir}/${lib} ]; then
       ln -sf %{_builddir}/openldap-%{version}/32bit/libraries/${dirlib}/.libs/${lib} $RPM_BUILD_ROOT/%{_libdir}/${lib}
   fi
done

cd %{_builddir}/openldap-%{version}/32bit/build
sed "s;strip \$dsttmp || shtool_exit;strip -X32_64 \$dsttmp || shtool_exit;" shtool >shtool.tmp
mv -f shtool.tmp shtool
chmod +x shtool
cd -

gmake install DESTDIR=$RPM_BUILD_ROOT

# move slapd out of %{_libdir}
mv ${RPM_BUILD_ROOT}%{_libdir}/slapd ${RPM_BUILD_ROOT}%{_sbindir}/slapd
for i in acl add auth cat dn index passwd schema test ; do
    rm -f ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}
done

# bin : Create the *_32
(
    for bin in %{_bindir} %{_sbindir}
    do
	cd ${RPM_BUILD_ROOT}$bin
	for fic in * ; do
            [ -L "$f" ] && continue;
	    [ -f "$f" ] || continue;
	    grep _64 $f && continue
	    mv -f ${f}    ${f}_32
	    ln -s ${f}_64 ${f}     # By default, binaries link to 64bit
	done
    done
)

# set up tools as symlinks to slapd
for i in acl add auth cat dn index passwd schema test ; do
    ln -s slapd ${RPM_BUILD_ROOT}%{_sbindir}/slap${i}
done

#rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.a
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/liblber.la
#rm -f ${RPM_BUILD_ROOT}%{_libdir}/libldap.la

(
  cd ${RPM_BUILD_ROOT}%{_libdir}
  for f in *.a ; do
      /usr/bin/ar -X32 -x ${f}
  done
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  for f in *.a ; do
      /usr/bin/ar -X64 -x ${f}
  done
)


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
for i in lber-2.4 ldap-2.4 ldap_r-2.4 ; do
    /usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib${i}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib${i}.so*
    /usr/bin/strip -e -X64 ${RPM_BUILD_ROOT}%{_libdir64}/lib${i}.so*
    /usr/bin/strip -e -X32 ${RPM_BUILD_ROOT}%{_libdir}/lib${i}.so*
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ln -sf ../lib/lib"$i".a lib"$i".a
done

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin sbin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean 
rm -rf $RPM_BUILD_ROOT


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
%doc 32bit/contrib/slapd-modules/smbk5pwd/README
%attr(0755,root,system) %dir %{_sysconfdir}/openldap
%attr(0640,root,ldap) %config(noreplace) %{_sysconfdir}/openldap/slapd.conf*
%attr(0644,root,system) %config(noreplace) %{_sysconfdir}/openldap/schema*/*.schema*
%attr(0644,root,system) %config(noreplace) %{_sysconfdir}/openldap/schema*/*.ldif
%attr(0644,root,system) %config(noreplace) %{_sysconfdir}/openldap/ldap*.conf*

# %attr(0755,root,system) %{_libdir}/liblber.a
# %attr(0755,root,system) %{_libdir}/liblber-2.4.*
# %attr(0755,root,system) %{_libdir}/libldap.a
# %attr(0755,root,system) %{_libdir}/libldap-2.4.*
# %attr(0755,root,system) %{_libdir}/libldap_r.a
# %attr(0755,root,system) %{_libdir}/libldap_r-2.4.*
# 
# %attr(0755,root,system) %{_libdir64}/liblber.a
# %attr(0755,root,system) %{_libdir64}/liblber-2.4.*
# %attr(0755,root,system) %{_libdir64}/libldap.a
# %attr(0755,root,system) %{_libdir64}/libldap-2.4.*
# %attr(0755,root,system) %{_libdir64}/libldap_r.a
# %attr(0755,root,system) %{_libdir64}/libldap_r-2.4.*

%attr(0755,root,system) %{_bindir}/*
%attr(0755,root,system) /usr/bin/*
%attr(0755,root,system) %{_sbindir}/*
%attr(0755,root,system) /usr/sbin/*
%attr(0755,root,system) %{_libdir}/*
%attr(0755,root,system) /usr/lib/*
%attr(0755,root,system) %{_libdir64}/*
%attr(0755,root,system) /usr/lib64/*
%attr(0644,root,system) %{_prefix}/share/man/man1/*
%attr(0644,root,system) %{_prefix}/share/man/man3/*
%attr(0644,root,system) %{_prefix}/share/man/man5/*
%attr(0644,root,system) %{_prefix}/share/man/man8/*


%files devel
%defattr(-,root,system) 
%attr(0755,root,system) %{_libdir}/libl*.la
%attr(0755,root,system) %{_libdir64}/libl*.la
%attr(0755,root,system) /usr/lib/libl*.la
%attr(0644,root,system) %{_includedir}/* 
%attr(0644,root,system) /usr/include/* 
%attr(0644,root,system) %{_prefix}/share/man/man3/* 


%changelog
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
