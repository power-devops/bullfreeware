%bcond_without dotests

%global tarver 2.1-3
%define _libdir64 %{_libdir}64

Name:           CUnit
Version:        2.1.3
Release:        2
Summary:        Unit testing framework for C

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://cunit.sourceforge.net/
Source0:        http://downloads.sourceforge.net/cunit/%{name}-%{tarver}.tar.bz2
Source1000:     %{name}-%{version}-%{release}.build.log

BuildRequires:  automake,autoconf
BuildRequires:  coreutils >= 8.25
BuildRequires:  libtool
BuildRequires:  findutils
Requires:       libgcc >= 6.3.0

%description 
CUnit is a lightweight system for writing, administering,
and running unit tests in C.  It provides C programmers a basic
testing functionality with a flexible variety of user interfaces.

%package devel
Summary:        Header files and libraries for CUnit development
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel 
The %{name}-devel package contains the header files
and libraries for use with CUnit package.

%prep
%setup -q -n %{name}-%{tarver}
/opt/freeware/bin/find -name *.c -exec chmod -x {} \;
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build
export CC=/opt/freeware/bin/gcc

# build on 64bit mode
cd 64bit
export OBJECT_MODE=64
export CFLAGS="-O2 -maix64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
autoreconf -f -i
%configure --disable-static --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --includedir=%{_includedir} \
    --docdir=%{_docdir}/%{name} 

gmake %{?_smp_mflags}

# build on 32bit mode
cd ../32bit
export OBJECT_MODE=32
export CFLAGS="-O2 -maix32 -D_LARGE_FILES"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
autoreconf -f -i
%configure --disable-static --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --docdir=%{_docdir}/%{name} 

gmake %{?_smp_mflags}

/usr/bin/ar -X64 -q CUnit/Sources/.libs/libcunit.a ../64bit/CUnit/Sources/.libs/libcunit.so.1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export FIND=/opt/freeware/find

# install on 64bit mode
cd 64bit
export OBJECT_MODE=64
gmake install DESTDIR=${RPM_BUILD_ROOT}
rm -f `$FIND ${RPM_BUILD_ROOT} -name *.la`

# install on 32bit mode
cd ../32bit
export OBJECT_MODE=32
gmake install DESTDIR=${RPM_BUILD_ROOT}
rm -f `$FIND ${RPM_BUILD_ROOT} -name *.la`

# work around bad docdir= in doc/Makefile*
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/%{name}/html
(
cd ${RPM_BUILD_ROOT}%{_prefix}/doc/%{name}
mv -f CUnit_doc.css error_handling.html fdl.html headers index.html introduction.html managing_tests.html running_tests.html test_registry.html writing_tests.html html
)

# add some doc files into the buildroot manually (#1001276)
for f in AUTHORS ChangeLog COPYING NEWS README TODO VERSION ; do
    /opt/freeware/bin/install -p -m0644 -D $f ${RPM_BUILD_ROOT}%{_docdir}/%{name}/${f}
done

# lib64 libraries are link of lib librairies
(
  cd ${RPM_BUILD_ROOT}%{_libdir64}
  ln -sf ../lib/libcunit.a .
)


%check
%if %{with dotests}
# No test. gmake check does nothings.
# You can tests manually in Examples folder.
# However, Makefiles are not OK.
# To compile examples, go to a specific example folder,
# use gmake "exampleName". From commandline, add to the bad compile line
# -I.., ../../CUnit/Sources/.libs/libcunit.a ../../CUnit/Sources/Automated/.libs/libcunitautomated.a ../../CUnit/Sources/Basic/.libs/libcunitbasic.a  ../../CUnit/Sources/Console/.libs/libcunitconsole.a ../../CUnit/Sources/Framework/.libs/libcunitfmk.a ../ExampleTests.c "exampleName".c

# cd 64bit
# export OBJECT_MODE=64
# ( gmake -k check || true )
# cd ../32bit
# export OBJECT_MODE=32
# ( gmake -k check || true )
%endif


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%{_datadir}/%{name}/
%{_libdir}/libcunit.a
%{_libdir64}/libcunit.a
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/NEWS
%{_docdir}/%{name}/README
%{_docdir}/%{name}/TODO
%{_docdir}/%{name}/VERSION

%files devel
%defattr(-,root,system)
%{_docdir}/%{name}/html/
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/cunit.pc
%{_libdir64}/pkgconfig/cunit.pc
%{_mandir}/man3/CUnit.3*

%changelog
* Wed Feb 12 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> 2.1.3-2
- Port on Bullfreeware

* Mon May 27 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.1.3-1
- Initial port of CUnit to AIX toolbox
