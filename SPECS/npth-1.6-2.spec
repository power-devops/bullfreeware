# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary:        The New GNU Portable Threads library
Name:           npth
Version:        1.6
Release:        2
# software uses dual licensing (or both in parallel)
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            https://git.gnupg.org/cgi-bin/gitweb.cgi?p=npth.git
Source:         https://gnupg.org/ftp/gcrypt/npth/%{name}-%{version}.tar.bz2
# Manual page is re-used and changed pth-config.1 from pth-devel package
Source2:        npth-config.1
Source100: %{name}-%{version}-%{release}.build.log

BuildRequires:  gcc
Requires: libgcc >= 8

%description
nPth is a non-preemptive threads implementation using an API very similar
to the one known from GNU Pth.  It has been designed as a replacement of
GNU Pth for non-ancient operating systems.  In contrast to GNU Pth is is
based on the system's standard threads implementation.  Thus nPth allows
the use of libraries which are not compatible to GNU Pth.


%package devel
Summary:        Development headers and libraries for GNU nPth
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for GNU Pth.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export RM="/usr/bin/rm -f"
export AR="/usr/bin/ar -X32_64"

build_npth() {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--enable-shared --disable-static

    gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export OBJECT_MODE=64
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_npth %{_libdir64}

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="-D_LARGE_FILES"
export OBJECT_MODE=32
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_npth %{_libdir}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export AR="/usr/bin/ar -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
  cd ${RPM_BUILD_ROOT}%{_bindir}
  for f in * ; do
    mv -f ${f} ${f}_64
  done
)

cd ../32bit
export OBJECT_MODE=32
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 32bit binaries' name and make default link towards 64bit
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _32 -e _64)
    do
	mv ${f} ${f}_32
	ln -sf ${f}_64 ${f}
    done
)

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    %define libsoversion 0

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x lib%{name}.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -x lib%{name}.a
    ${AR} -q lib%{name}.a ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.%{libsoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/lib%{name}.so.%{libsoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f lib%{name}.a
    ln -sf ../lib/lib%{name}.a lib%{name}.a
)

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_mandir}/man1/
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man1/*


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
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/COPYING.LIB 32bit/ChangeLog
%doc 32bit/NEWS 32bit/README
%{_libdir}/*.a
#	%{_libdir}/*.so*
#	%{_libdir64}/*.so*


%files devel
%defattr(-,root,system,-)
%{_bindir}/*
%{_includedir}/*
%{_mandir}/*/*
%{_datadir}/aclocal/*


%changelog
* Tue Jun 08 2021 Tony Reix <tony.reix@atos.net> - 1.6-2
- No more deliver .so files
- Nothing new in Fedora .spec file

* Tue May 25 2021 Clement Chigot <clement.chigot@atos.net> - 1.6-1
- Update to version 1.6
- Rebuilt in 64bit
- Rebuilt with RPMv4

* Thu Nov 17 2017 Tony Reix <tony.reix@atos.net> - 1.5-1
- Port on AIX 6.1

* Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.5-1
- updated to version 1.5

* Thu Jul 13 2017 Michael Perzl <michael@perzl.org> - 1.4-1
- updated to version 1.4

* Thu Nov 24 2016 Michael Perzl <michael@perzl.org> - 1.3-1
- updated to version 1.3

* Wed Dec 23 2015 Michael Perzl <michael@perzl.org> - 1.2-1
- updated to version 1.2

* Fri Nov 07 2014 Michael Perzl <michael@perzl.org> - 1.1-1
- updated to version 1.1

* Thu Sep 18 2014 Michael Perzl <michael@perzl.org> - 1.0-1
- updated to version 1.0

* Mon Jan 27 2014 Michael Perzl <michael@perzl.org> - 0.91-1
- first version for AIX V5.1 and higher
