Summary: An XML parser library
Name: expat
Version: 2.0.1
Release: 4
Group: System Environment/Libraries
Source0: http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: libexpat.so.0-aix32
Source2: libexpat.so.0-aix64
Patch2: expat-2.0.1-CVE-2009-3560-revised.patch
Patch3: expat-1.95.8-CVE-2009-3720.patch
Patch4: expat-%{version}-aixconf.patch
URL: http://www.libexpat.org/
License: MIT
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildRequires: patch

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
%patch2 -p1 -b .newcve3560
%patch3 -p1 -b .cve3720
%patch4 -p1 -b .aixconf


%build
# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"
export NM="nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

cp .libs/libexpat.so.1 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
./configure \
    --prefix=%{_prefix} \
    --enable-shared --enable-static
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libexpat.a ./libexpat.so.1

# Add the older libexpat.so.0 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
/usr/bin/strip -X32 -e %{SOURCE1}
/usr/bin/strip -X64 -e %{SOURCE2}
cp %{SOURCE1} libexpat.so.0
/usr/bin/ar -X32 -q .libs/libexpat.a libexpat.so.0
cp %{SOURCE2} libexpat.so.0
/usr/bin/ar -X64 -q .libs/libexpat.a libexpat.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export RM="/usr/bin/rm -f"
rm -f examples/*.dsp
chmod 644 README COPYING Changes doc/* examples/*

make DESTDIR=${RPM_BUILD_ROOT} install

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

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


%files
%defattr(-,root,system)
%doc README COPYING
%{_bindir}/*
%{_libdir}/*.a
%{_mandir}/man?/*
/usr/bin/*
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%doc Changes doc examples
%{_libdir}/*.la
%{_includedir}/*.h
/usr/include/*
/usr/lib/*.la


%changelog
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

