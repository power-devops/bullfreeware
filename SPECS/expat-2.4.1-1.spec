# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

Summary: An XML parser library
Name: expat
Version: 2.4.1
Release: 1
Group: System Environment/Libraries
Source0: https://sourceforge.net/projects/expat/files/expat/%{version}/expat-%{version}.tar.bz2
Source1: libexpat.so.0-aix64
Source2: libexpat.so.0-aix32
URL: https://libexpat.github.io/
License: MIT

Source10: %{name}-%{version}-%{release}.build.log

# TODO
# BuildRequires: xmlto
Requires: libgcc >= 6.3.0-1

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


# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
# setup environment for 32-bit and 64-bit builds
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
CONFIG_ENV_ARGS=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_BASE="-O2"

%if %{with gcc_compiler}
export __CC="gcc"
export __CXX="g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="xlc_r"
export __CXX="xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"
%endif

# libm is needed for isnanf.
export LIBS=-lm

build_expat() {
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--enable-shared --disable-static

	gmake %{?_smp_mflags}
}

# first build the 64-bit version

cd 64bit
export OBJECT_MODE=64
export CC="$__CC $FLAG64"
export CXX="$__CXX $FLAG64"
export CFLAGS="$CFLAGS_BASE"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_expat %{_libdir64}


# now build the 32-bit version

cd ../32bit
export OBJECT_MODE=32
export CC="$__CC $FLAG32"
export CXX="$__CXX $FLAG32"
export CFLAGS="$CFLAGS_BASE -D_LARGE_FILES"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_expat %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"



# install 64-bit version

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

# Save 64bits version of xmlwf
mv ${RPM_BUILD_ROOT}%{_bindir}/xmlwf ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64
# Strip 64bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64 || :


# install 32-bit version

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/xmlwf ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_32
cd ${RPM_BUILD_ROOT}%{_bindir}
ln -sf xmlwf_64 xmlwf
cd -

# Strip 32bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf || :


rm -f examples/*.dsp
chmod 644 COPYING Changes doc/* examples/*


# add the 64-bit shared objects to the shared library containing already the 32-bit shared objects
# and create link.
(
    cd                  ${RPM_BUILD_ROOT}%{_libdir64}
    /usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/libexpat.a    libexpat.so.1
	/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a      libexpat.so.1
	rm libexpat.a libexpat.so.1
	ln -sf ../lib/libexpat.a libexpat.a
)


# Add the older libexpat.so.0 shared members for compatibility with older apps
# (make sure they're set for LOADONLY)
dump -X64 -ov %{SOURCE1} | grep -q "LOADONLY" || /usr/bin/strip -X64 -e %{SOURCE1}
dump -X32 -ov %{SOURCE2} | grep -q "LOADONLY" || /usr/bin/strip -X32 -e %{SOURCE2}
cp %{SOURCE1} libexpat.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a libexpat.so.0
cp %{SOURCE2} libexpat.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a libexpat.so.0



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
%defattr(-,root,system)
%doc 32bit/AUTHORS 32bit/COPYING 32bit/Changes
%{_bindir}/*
%{_libdir}/*.a
%{_libdir64}/*.a
#%{_datadir}/man/man?/*


%files devel
%defattr(-,root,system)
%doc 32bit/Changes 32bit/doc 32bit/examples
%{_includedir}/*.h


%changelog
* Mon Aug 02 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.4.1-1
- Update to 2.4.1

* Fri Mar 26 2021 Bullfreeware Continous Integration <bullfreeware@atos.net> - 2.3.0-1
- Update to 2.3.0

* Thu Oct 29 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 2.2.10-1
- Update to 2.2.10

* Tue Oct 26 2020 Étienne Guesnet <etienne.guesnet@atos.net> 2.2.9-2
- Update specfile for automated build

* Mon Mar 30 2020 Clement Chigot <clement.chigot@atos.net> 2.2.9-1
- BullFreeware Compatibility Improvements
- Build with gcc
- Move tests to %check section

* Mon Sep 17 2018 Michael Wilson <michael.a.wilson@atos.net> 2.2.6-1
- Update to version 2.2.6
- W/A libtool issue wanting runtests/runtestspp prefixed with lt-
- Have to install the new libexpat.a with possible new symbols for runtests

* Wed Aug 08 2018 Tony Reix <tony.reix@bull.net> 2.2.5-1
- Update and Initial port on AIX 6.1

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

* Mon Mar 21 2011  Patricia Cugny <patricia.cugny@bull.net> - 2.0.1-1
- update to version 2.0.1

*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
