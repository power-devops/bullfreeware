# rpm -ba --define 'dotests 0' expat-2.1.1-1.spec ...
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}


Summary: An XML parser library
Name: expat
Version: 2.1.1
Release: 1
Group: System Environment/Libraries
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: libexpat.so.0-aix64
Source2: libexpat.so.0-aix32
#Patch2: expat-2.0.1-CVE-2009-3560-revised.patch
#Patch3: expat-1.95.8-CVE-2009-3720.patch
#Patch4: expat-%{version}-aixconf.patch
URL: http://www.libexpat.org/
License: MIT
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

BuildRequires: patch

%define _libdir64 %{_prefix}/lib64

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

The library is available as 32-bit and 64-bit.


%package devel
Summary: Libraries and header files to develop applications using expat
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "cc -q64" or "gcc -maix64".


%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH
#%patch2 -p1 -b .newcve3560
#%patch3 -p1 -b .cve3720
#%patch4 -p1 -b .aixconf

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/


%build
# setup environment for 32-bit and 64-bit builds
export PATH=/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/usr/bin/sh
CONFIG_ENV_ARGS=/usr/bin/sh
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC=" /usr/vacpp/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC=" /usr/vacpp/bin/xlc_r -q32"
export CXX="/usr/vacpp/bin/xlC_r -q32"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared --enable-static

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


# install 64-bit version

export OBJECT_MODE=64
cd 64bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install

# Save 64bits version of xmlwf
mv ${RPM_BUILD_ROOT}%{_bindir}/xmlwf ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64
# Strip 64bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64 || :


# install 32-bit version

export OBJECT_MODE=32
cd ../32bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install
# Strip 32bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf || :


rm -f examples/*.dsp
chmod 644 README COPYING Changes doc/* examples/*


# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
(
    cd                  ${RPM_BUILD_ROOT}%{_libdir64}
    /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libexpat.a              libexpat.so.1
)
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a  ${RPM_BUILD_ROOT}%{_libdir64}/libexpat.so.1

#ls -l ${RPM_BUILD_ROOT}%{_bindir}


# Add the older libexpat.so.0 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
/usr/bin/strip -X64 -e %{SOURCE1}
/usr/bin/strip -X32 -e %{SOURCE2}
cp %{SOURCE1} libexpat.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a libexpat.so.0
cp %{SOURCE2} libexpat.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a libexpat.so.0


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#echo ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/README 32bit/COPYING
%{_bindir}/*
%{_libdir}/*.a
%{_datadir}/man/man?/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc 32bit/Changes 32bit/doc 32bit/examples
%{_libdir}/*.la
%{_includedir}/*.h
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Apr 29 2016 Tony Reix <tony.reix@bull.net> 2.1.1-1
- Update and Initial port on AIX 6.1

* Thu Jul 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.1.0-2
- Building on Aix5.3

* Wed Mar 06 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.1.0-1
- update to version 2.1.0

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.0.1-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.0.1-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jun 23 2011 Gerard Visiedo <gerard.visiedo@bull.net> -2.0.1-2
- Insert libexpat missing

* Mon Mar 20 2011  Patricia Cugny <patricia.cugny@bull.net> - 2.0.1-1
- update to version 2.0.1

*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
