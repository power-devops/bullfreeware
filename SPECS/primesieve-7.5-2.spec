# Create a test package in ANY case, but test only if with dotests.
%bcond_without dotests

%global _libdir64 %{_prefix}/lib64

Name:     primesieve
%global   so_version 9
Version:  7.5
Release:  2
Summary:  Fast prime number generator
License:  BSD
URL:      https://github.com/kimwalisch/primesieve
Source0:  https://github.com/kimwalisch/primesieve/archive/v%{version}.tar.gz
Source1000:       %{name}-%{version}-%{release}.build.log


Requires: primesieve-libs%{?_isa} = %{version}-%{release}

Patch0: primesieve-7.5-class-thread.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.7
# Doc/Man:
#	BuildRequires:  doxygen
#	BuildRequires:  graphviz
#	BuildRequires:  asciidoc

%description
primesieve is a program that generates primes using a highly optimized
sieve of Eratosthenes implementation. primesieve can generate primes
and prime k-tuplets up to 2^64.

%package -n primesieve-libs
Summary: C/C++ library for generating prime numbers

%description -n primesieve-libs
This package contains the shared runtime library for primesieve.

%package -n primesieve-devel
Summary: Development files for the primesieve library
Requires: primesieve-libs%{?_isa} = %{version}-%{release}

%description -n primesieve-devel
This package contains the C/C++ header files and the configuration
files for developing applications that use the primesieve library.
It also contains the API documentation of the library.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .class-thread

# Duplicate source for 32 & 64 bits
rm -rf   ../%{name}-%{version}-32bit
mkdir    ../%{name}-%{version}-32bit
mv     * ../%{name}-%{version}-32bit
mv       ../%{name}-%{version}-32bit 32bit
cp -pr                               32bit 64bit


%build

build_all()
{
set -x

export OBJECT_MODE=$1
export LIBDIR=$2

export CC="/opt/freeware/bin/gcc -maix$OBJECT_MODE"
export CXX="/opt/freeware/bin/g++ -maix$OBJECT_MODE"

if [ $OBJECT_MODE -eq 64 ]
then
        export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
else
        export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
fi

#	export CFLAGS="-O0 -g -gdwarf"
export CXXFLAGS="-pthread"

cmake . \
	-DBUILD_STATIC_LIBS=OFF \
	-DOBJECT_MODE=$OBJECT_MODE \
%if %{with dotests}
	-DBUILD_TESTS=ON \
%endif
	-DBUILD_MANPAGE=OFF -DBUILD_DOC=OFF \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
	-DCMAKE_INSTALL_LIBDIR="${LIBDIR}" \
	-DCMAKE_INSTALL_MANDIR=share/man \

#            -DCMAKE_INSTALL_DOCDIR="%{_pkgdocdir}" \
#            -DCMAKE_INSTALL_DOCREADMEDIR="%{_pkgdocdir}" \
#            -DCMAKE_INSTALL_INCLUDEDIR=include \
#            -DCMAKE_INSTALL_INFODIR=share \

# add the following for debug
#	-DCMAKE_CXX_FLAGS_RELEASE="-O0 -g -gdwarf -DDEBUG" \
#	-DCMAKE_C_FLAGS_RELEASE:STRING="-O0 -g -gdwarf -DDEBUG"

#	%make_build
gmake --trace VERBOSE=1
##	%make_build doc
##	find doc/html -name '*.md5' -exec rm {} +

}

cd 64bit
build_all 64 %{_lib}64

cd ../32bit
build_all 32 %{_lib}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%install
##	%make_install
##	%ldconfig_scriptlets -n primesieve-libs

(
  cd 64bit
  export OBJECT_MODE=64
  export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
  gmake DESTDIR=%{buildroot} install
  mv ${RPM_BUILD_ROOT}%{_bindir}/primesieve ${RPM_BUILD_ROOT}%{_bindir}/primesieve_64
)

(
  cd 32bit
  export OBJECT_MODE=32
  export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
  gmake DESTDIR=%{buildroot} install
  mv ${RPM_BUILD_ROOT}%{_bindir}/primesieve ${RPM_BUILD_ROOT}%{_bindir}/primesieve_32
)

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  ln -s primesieve_64 primesieve
)

ar -X64 -x  ${RPM_BUILD_ROOT}%{_libdir64}/libprimesieve.a
ar -X64 -qc ${RPM_BUILD_ROOT}%{_libdir}/libprimesieve.a libprimesieve.so.%{so_version}
rm          ${RPM_BUILD_ROOT}%{_libdir64}/libprimesieve.a
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s ../lib/libprimesieve.a .
)


%check
#	export CFLAGS="-O0 -g -gdwarf"
#	export CXXFLAGS="-pthread"

%if %{with dotests}
cd 64bit
export LDFLAGS=-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
export LIBPATH=/opt/freeware/lib/pthread/ppc64:/opt/freeware/src/packages/BUILD/primesieve-7.5:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib
gmake test

cd ../32bit
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LIBPATH=/opt/freeware/lib/pthread:/opt/freeware/src/packages/BUILD/primesieve-7.5:/opt/freeware/lib:/usr/lib:/lib
gmake test

#	gmake --trace VERBOSE=1 generate_n_primes2
#	gmake --trace VERBOSE=1 generate_primes2
#	gmake --trace VERBOSE=1 next_prime2
#	gmake --trace VERBOSE=1 prev_prime2
%endif


%files -n primesieve
%defattr(-,root,system,-)
%doc 32bit/README.md 32bit/ChangeLog
%{_bindir}/primesieve*
#	%{_mandir}/man1/primesieve.1*


%files -n primesieve-libs
%defattr(-,root,system,-)
%license 32bit/COPYING
%{_libdir}/libprimesieve.a
%{_libdir64}/libprimesieve.a


%files -n primesieve-devel
%defattr(-,root,system,-)
#	%doc doc/html examples
%{_libdir}/libprimesieve.a
%{_libdir64}/libprimesieve.a
%{_includedir}/primesieve.h
%{_includedir}/primesieve.hpp
%dir %{_includedir}/primesieve
%{_includedir}/primesieve/StorePrimes.hpp
%{_includedir}/primesieve/iterator.h
%{_includedir}/primesieve/iterator.hpp
%{_includedir}/primesieve/primesieve_error.hpp
%dir %{_libdir}/cmake/primesieve
%{_libdir}/cmake/primesieve/*.cmake
%{_libdir}/pkgconfig/primesieve.pc
%dir %{_libdir64}/cmake/primesieve
%{_libdir64}/cmake/primesieve/*.cmake
%{_libdir64}/pkgconfig/primesieve.pc


%changelog
* Thu Jun 04 2020 Tony Reix <tony.reix@atos.net> - 7.5-2
- Port to AIX

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Kim Walisch <walki@fedoraproject.org> - 7.5-1
- Update to primesieve-7.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Kim Walisch <walki@fedoraproject.org> - 7.4-2
- Rename libprimesieve to primesieve-libs
- Rename libprimesieve-devel to primesieve-devel
- Increase CMake version to >= 3.7

* Mon Apr 08 2019 Kim Walisch <walki@fedoraproject.org> - 7.4-1
- Update to primesieve-7.4
- Move Requires before description
- Drop libprimesieve-static package

* Sun Jul 08 2018 Kim Walisch <walki@fedoraproject.org> - 7.0-1
- Update to primesieve-7.0
- Fix erroneous date in changelog

* Sat Mar 24 2018 Kim Walisch <walki@fedoraproject.org> - 6.4-5
- Update to primesieve-6.4

* Fri Feb 16 2018 Kim Walisch <walki@fedoraproject.org> - 6.4-4
- Add libprimesieve package
- Improve summaries and descriptions
- Update to primesieve-6.4-rc2

* Tue Feb 06 2018 Kim Walisch <walki@fedoraproject.org> - 6.4-3
- Fix new issues from package review

* Wed Jan 31 2018 Kim Walisch <walki@fedoraproject.org> - 6.4-2
- Fix issues from package review

* Tue Jan 30 2018 Kim Walisch <walki@fedoraproject.org> - 6.4-1
- Initial package
