Summary:   Character set conversion library, portable iconv implementation
Name:      libiconv
Version:   1.16
Release:   2
Group:     System Environment/Libraries
License:   LGPL
URL:       http://www.gnu.org/software/libiconv/
Source0:   http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
# No More useful
#	Patch0:    libiconv-1.13.1-aixconf.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _libdir64 %{_prefix}/lib64

# there is a circular dependency between gettext and libiconv
# first build and install libiconv, then build and install gettext then build and install again libiconv
# comment the following lines if gettext not installed
# see also %files section
BuildRequires: gettext 
BuildRequires: gettext-devel

%description
GNU libiconv provides an iconv() implementation for use on systems
which don't have one or whose implementation cannot convert from/to Unicode.

The library is available as 32-bit and 64-bit.


%prep
# In order to find the BullFreeware patch command !
export PATH=/opt/freeware/bin:$PATH
%setup -q
#	%patch0 -p1 -b .aixconf


%build
# work around strange configure error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export RM="rm -f"
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export OBJECT_MODE=64

# XLC
#CC=cc \
#CFLAGS="-q64 -D_GNU_SOURCE -I/opt/freeware/include/" \
#CXXFLAGS="-q64" \

# GCC
CC=gcc \
CFLAGS="-maix64 -D_GNU_SOURCE -I/opt/freeware/include/" \
CXXFLAGS="-maix64" \
AR="/usr/bin/ar -X32_64" \
LIBS=" -L/opt/freeware/lib" \
CPPFLAGS="-I/opt/freeware/include" \
LDFLAGS=" -L/opt/freeware/lib" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-extra-encodings

gmake %{?_smp_mflags}

#( gmake check || true )
gmake check

cp lib/.libs/libiconv.so.2 .
cp libcharset/lib/.libs/libcharset.so.1 .
# Build at install phase... nuts !   cp ./src/iconv iconv_64

gmake distclean
slibclean


# now build the 32-bit version
export OBJECT_MODE=32

CC=gcc \
AR="/usr/bin/ar -X32_64" \
CFLAGS=" -D_GNU_SOURCE -I/opt/freeware/include/" \
LIBS=" -L/opt/freeware/lib" \
CPPFLAGS="-I/opt/freeware/include" \
LDFLAGS=" -L/opt/freeware/lib" \
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static \
    --enable-extra-encodings

gmake %{?_smp_mflags}

#( gmake check || true )
gmake check


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install

# The libiconv Makefile process only the 32 bits library for newly
# created libiconv.so.2 and system lib shared objects (/usr/lib/libiconv.a)
# recreate libs correctly
export AR="/usr/bin/ar -X32_64"

/usr/bin/rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

# add 32 then 64 bits shared objects
${AR} -rv ${RPM_BUILD_ROOT}%{_libdir}/libcharset.a libcharset/lib/.libs/libcharset.so.1
${AR} -q  ${RPM_BUILD_ROOT}%{_libdir}/libcharset.a ./libcharset.so.1
${AR} -rv ${RPM_BUILD_ROOT}%{_libdir}/libiconv.a   lib/.libs/libiconv.so.2
${AR} -q  ${RPM_BUILD_ROOT}%{_libdir}/libiconv.a   ./libiconv.so.2

# Add a symlink between libiconv.a 32 and 64bit
# This helps to fix issues when:
#    64bit code is looking for 64bit libiconv.so from libiconv.a in /opt/freeware/lib64 where it is not
mkdir -p                                     ${RPM_BUILD_ROOT}%{_libdir64}
ln -s ${RPM_BUILD_ROOT}%{_libdir}/libiconv.a ${RPM_BUILD_ROOT}%{_libdir64}/libiconv.a


# Manage 64bit version of iconv some time in the future...
#	cp iconv_64 ${RPM_BUILD_ROOT}%{_bindir}
#	mv ${RPM_BUILD_ROOT}%{_bindir}/iconv ${RPM_BUILD_ROOT}%{_bindir}/iconv_32
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
#	ln -s ${RPM_BUILD_ROOT}%{_bindir}/iconv_32 ${RPM_BUILD_ROOT}%{_bindir}/iconv

# create symbolic links
(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/linux/${dir}
    cd usr/linux/${dir}
    ln -sf ../../..%{_prefix}/${dir}/* .
    cd -
  done
)


%post
# we need to include all shared members of the system wide /usr/lib/libiconv.a
# at rpm installation time to avoid core dump of system binaries

export AR="/usr/bin/ar -X32_64"

/usr/bin/mkdir -p /tmp/libiconv.tmp
cd  /tmp/libiconv.tmp
LIST=`${AR} -t /usr/lib/libiconv.a`
${AR} -x /usr/lib/libiconv.a
/usr/bin/strip -X32_64 -e *
for i in ${LIST}
do
   if [ "$i" != "libiconv.so.2" ]; then
     echo "add $i shared members from /usr/lib/libiconv.a to  %{_libdir}/libiconv.a"
    ${AR} -r %{_libdir}/libiconv.a ${i}
   fi
done
cd -
/usr/bin/rm -rf /tmp/libiconv.tmp

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc AUTHORS* COPYING.LIB* ChangeLog* DESIGN*
%doc INSTALL.generic* NEWS* NOTES* PORTS* README* THANKS*
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.*a
%{_mandir}/man?/*
# comment the following line if gettext not installed
%{_datadir}/locale/*/*/*
/usr/linux/bin/*
/usr/linux/include/*
/usr/linux/lib/*.a*

%changelog
* Tue Jun 18 2019 Tony Reix <tony.reix@atos.net> 1.16-2
- Add: /usr/bin/strip -X32_64 -e *  in the %post stage

* Fri May 24 2019 Tony Reix <tony.reix@atos.net> 1.16-1
- New version

* Thu Aug 24 2017 Tony Reix <tony.reix@atos.net> 1.14-23
- Move to release 23 since release 1.14-2 was wrongly name 1.14.22
- Fix needed symlink between 32bit and 64bit libiconv.a versions

* Fri Aug 07 2015 Hamza Sellmai <hamza.sellami@atos.net> 1.14-2
- Compoling with new GCC 

* Wed Aug 28 2013 Gerard Visiedo <gerard.visiedo@bull.net> 1.14-1
- Update to version 1.14

* Mon Feb 6 2012 Patricia Cugny <patricia.cugny@bull.net> 1.13.1-3
- Add patch for building on aix 6.1

* Thu Jun 30 2011 Patricia Cugny ,patricia.cugnybull.net>  1.13.1-2
- add 64 bits library 
- include also system wide /usr/lib/libiconv.a shared members 

* Thu Sep 30 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 1.13.1
- Initial port for AIX
