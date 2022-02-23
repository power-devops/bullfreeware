Name: pcre
Version: 8.34
Release: 1
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz
Source1: ftp://ftp.csx.cam.ac.uk/pub/software/programming/%{name}/%{name}-%{version}.tar.gz.sig
License: BSD
Group: System Environment/Libraries
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
BuildPrereq: sed
BuildRequires: bzip2 >= 1.0.2, zlib-devel >= 1.2.3, readline-devel >= 5.2
Requires: bzip2 >= 1.0.2, zlib >= 1.2.3, readline >= 5.2

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for static linking, etc) for %{name}.


%prep
%setup -q


%build
export CONFIG_SHELL=/usr/bin/sh
export CONFIG_ENV_ARGS=/usr/bin/sh

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
export CC="/usr/vac/bin/xlc_r -q64"
export CXX="/usr/vacpp/bin/xlC_r -q64"
LIBPATH="%{_libdir}:%{_prefix}/lib64:/usr/lib64:/usr/lib" \
./configure \
  --prefix=%{_prefix} \
  --mandir=%{_mandir} \
  --enable-utf8 \
  --enable-unicode-properties \
  --enable-pcregrep-libz \
  --enable-pcregrep-libbz2 \
  --enable-pcretest-libreadline

make

cp .libs/libpcre.so.1 .
cp .libs/libpcrecpp.so.0 .
cp .libs/libpcreposix.so.0 .
make distclean

# now build the 32-bit version
export CC="/usr/vac/bin/xlc_r"
export CXX="/usr/vacpp/bin/xlC_r"
LIBPATH="%{_libdir}:/usr/lib" \
./configure \
  --prefix=%{_prefix} \
  --mandir=%{_mandir} \
  --enable-utf8 \
  --enable-unicode-properties \
  --enable-pcregrep-libz \
  --enable-pcregrep-libbz \
  --enable-pcretest-libreadline
make %{?_smp_mflags}

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q .libs/libpcre.a ./libpcre.so.1
${AR} -q .libs/libpcrecpp.a ./libpcrecpp.so.0
${AR} -q .libs/libpcreposix.a ./libpcreposix.so.0


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export RM="/usr/bin/rm -f"
export AR="ar -X32_64"

make DESTDIR=${RPM_BUILD_ROOT} install

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpcrecpp.a ./libpcrecpp.so.0
${AR} -q ${RPM_BUILD_ROOT}%{_libdir}/libpcreposix.a ./libpcreposix.so.0

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
%doc AUTHORS LICENCE README
%{_bindir}/pcregrep
%{_bindir}/pcretest
%{_libdir}/*.a
%{_mandir}/man1/pcregrep.1
%{_mandir}/man1/pcretest.1
/usr/bin/pcregrep
/usr/bin/pcretest
/usr/lib/*.a


%files devel
%defattr(-,root,system)
%{_bindir}/pcre-config
%{_includedir}/*.h
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_mandir}/man1/pcre-config.1
%{_mandir}/man3/*
/usr/bin/pcre-config
/usr/include/*
/usr/lib/*.la


%changelog
* Fri Mar 14 2014  Gerard Visiedo <gerard.visiedo@bull.net> -8.34-1
- Update to version 8.34

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> -8.12-3
- Initial port on Aix6.1

* Fri Oct 14 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 8.12-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Mar 17 2011 Gerard Visiedo <gerard.visiedo@bull.net> 8.12-1
- Update to version 8.12

* Thu Oct 14 2010 Jean Noel Cordenner <jean-noel.cordenner@bull.net> 8.10-1
- Update to version 8.10.

* Thu Feb 16 2006 Reza Arbab <arbab@austin.ibm.com>
- Add patch for CAN-2005-2491.

* Fri Nov 22 2002 David Clissold <cliss@austin.ibm.com>
- Add IBM ILA license.


