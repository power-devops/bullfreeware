# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: Library for processing UTF-8 encoded Unicode strings
Name:    utf8proc
Version: 2.4.0
Release: 1
License: Unicode and MIT
URL:     http://julialang.org/utf8proc/
Source:  https://github.com/JuliaLang/utf8proc/archive/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz

Source1000: %{name}-%{version}-%{release}.build.log

Patch0:  utf8proc-2.4.0-AIX.patch


BuildRequires: gcc
BuildRequires: perl(perl)
BuildRequires: sed

%description
utf8proc is a library for processing UTF-8 encoded Unicode strings.
Some features are Unicode normalization, stripping of default ignorable
characters, case folding and detection of grapheme cluster boundaries.
A special character mapping is available, which converts for example
the characters “Hyphen” (U+2010), “Minus” (U+2212) and “Hyphen-Minus
(U+002D, ASCII Minus) all into the ASCII minus sign, to make them
equal for comparisons.

This package only contains the C library.


%package devel
Summary:  Header files, libraries and development documentation for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Contains header files for developing applications that use the %{name}
library.

The documentation for the C library is found in the utf8proc.h header file.
"utf8proc_map" is most likely the function you will be using for mapping UTF-8
strings, unless you want to allocate memory yourself.


%prep
%setup -qn %{name}-%{version}

%patch0 -p1 -b .AIX

# Disable slow tests and tests which require network access
/opt/freeware/bin/sed -i '/-C bench/d;/\ttest.* data/d' Makefile
touch data/NormalizationTest.txt data/GraphemeBreakTest.txt

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build

export AR=/usr/bin/ar

export __CFLAGS="-O2 -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fasynchronous-unwind-tables -fstack-clash-protection "
export __CXXFLAGS=$__CFLAGS
export __LDFLAGS="-Wl,-z -Wl,-z "
export CC=gcc
export CXX=g++

cd 64bit
export MAJOR=`grep "set(SO_MAJOR" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`
export MINOR=`grep "set(SO_MINOR" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`
export PATCH=`grep "set(SO_PATCH" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`
echo "MAJOUR.MINOR.PATCH = ${MAJOR}.${MINOR}.${PATCH}"

export OBJECT_MODE=64
export CFLAGS="-maix64 $__CFLAGS"
export CXXFLAGS="-maix64 $__CXXFLAGS"
export LDFLAGS="-maix64 $__LDFLAGS -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib64:/usr/lib:/lib "

gmake %{?_smp_mflags}

rm -f %{name}.exp lib%{name}.a
${AR} -X64 -rv lib%{name}.a lib%{name}.so.${MAJOR}.${MINOR}.${PATCH}
dump -X64 -Hv lib%{name}.so.${MAJOR}.${MINOR}.${PATCH}

cd ..

cd 32bit
export OBJECT_MODE=32
export CFLAGS="-maix32 $__CFLAGS"
export CXXFLAGS="-maix32 $__CXXFLAGS"
export LDFLAGS="-maix32 $__LDFLAGS -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

gmake %{?_smp_mflags}

rm -f %{name}.exp lib%{name}.a
${AR} -X32 -rv lib%{name}.a lib%{name}.so.${MAJOR}.${MINOR}.${PATCH}
dump -X32 -Hv lib%{name}.so.${MAJOR}.${MINOR}.${PATCH}


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

export AR=/usr/bin/ar

export __CFLAGS="-O2 -fexceptions -g -grecord-gcc-switches -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fasynchronous-unwind-tables -fstack-clash-protection "
export __CXXFLAGS=$__CFLAGS
export CC=gcc
export CXX=g++

cd 64bit
export OBJECT_MODE=64
export CFLAGS="-maix64 $__CFLAGS"
export CXXFLAGS="-maix64 $__CXXFLAGS"
export LDFLAGS="-maix64 "

gmake %{?_smp_mflags} check

cd ..

cd 32bit
export OBJECT_MODE=32
export CFLAGS="-maix32 $__CFLAGS"
export CXXFLAGS="-maix32 $__CXXFLAGS"
export LDFLAGS="-maix32 "

gmake %{?_smp_mflags} check


%install

export AR=/usr/bin/ar

cd 64bit
export MAJOR=`grep "set(SO_MAJOR" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`
export MINOR=`grep "set(SO_MINOR" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`
export PATCH=`grep "set(SO_PATCH" CMakeLists.txt | awk '{print $2}' | sed "s/)//"`

gmake install DESTDIR=%{buildroot} prefix=%{_prefix} includedir=%{_includedir} libdir=%{_libdir64}

cd ..

cd 32bit
gmake install DESTDIR=%{buildroot} prefix=%{_prefix} includedir=%{_includedir} libdir=%{_libdir}
rm %{buildroot}%{_libdir}/lib%{name}.so*

rm ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.a
${AR} -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a %{buildroot}%{_libdir64}/lib%{name}.so.${MAJOR}.${MINOR}.${PATCH}
rm %{buildroot}%{_libdir64}/lib%{name}.so*
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s ../lib/lib%{name}.a .
)
dump -X64 -Hv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a
dump -X32 -Hv ${RPM_BUILD_ROOT}%{_libdir}/lib%{name}.a


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/LICENSE.md 32bit/NEWS.md 32bit/README.md
%{_libdir}/lib%{name}.a
%{_libdir64}/lib%{name}.a

%files devel
%defattr(-,root,system,-)
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir64}/pkgconfig/lib%{name}.pc


%changelog
* Mon Nov 16 2020 Tony Reix <tony.reix@atos.net> - 2.4.0-1
- First port to AIX

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Milan Bouchet-Valat <nalimilan@club.fr> - 2.4.0-1
- New upstream release.

* Sun Apr 21 2019  Milan Bouchet-Valat <nalimilan@club.fr> - 2.3.0-1
- New upstream release.

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Joe Orton <jorton@redhat.com> - 2.1.1-4
- update License tag to Unicode and MIT
- BR gcc (#1606627)
- run minimal tests

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018  Milan Bouchet-Valat <nalimilan@club.fr> - 2.1.1-2
- Fix missing build flags (RHBZ #1573115).

* Fri Apr 27 2018  Milan Bouchet-Valat <nalimilan@club.fr> - 2.1.1-1
- New upstream release.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 7 2017  Milan Bouchet-Valat <nalimilan@club.fr> - 2.1.0
- New upstream release.

* Thu Sep 15 2016  Milan Bouchet-Valat <nalimilan@club.fr> - 2.0.2-1
- New upstream release.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015  Milan Bouchet-Valat <nalimilan@club.fr> - 1.3.1-1
- New upstream release.

* Tue Aug 11 2015 Milan Bouchet-Valat <nalimilan@club.fr> - 1.3-1
- New upstream release.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Mar 28 2015 Milan Bouchet-Valat <nalimilan@club.fr> - 1.2-1
- New upstream release.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 4 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 1.1.6-3
- Add downstream SONAME version 0.1 since upstream does not set one.

* Fri Feb 14 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 1.1.6-2
- Fix package Group.
- Do not remove build root on install phase.

* Sun Jan 26 2014 Milan Bouchet-Valat <nalimilan@club.fr> - 1.1.6-1
- Adapt package to Fedora.
- Updated to release 1.1.6.

* Sat Aug 29 2009 Dries Verachtert <dries@ulyssis.org> - 1.1.4-1 - 7981/dag
- Updated to release 1.1.4.

* Sun Jul 29 2007 Dries Verachtert <dries@ulyssis.org> - 1.1.2-1
- Updated to release 1.1.2.

* Mon Jul 23 2007 Dries Verachtert <dries@ulyssis.org> - 1.1.1-1
- Updated to release 1.1.1.

* Tue Apr 17 2007 Dries Verachtert <dries@ulyssis.org> - 1.0.3-1
- Initial package.
