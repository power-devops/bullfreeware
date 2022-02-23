# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define major_version 6
%define minor_version 2

Summary: A terminal handling library
Name: ncurses
Version: %{major_version}.%{minor_version}
Release: 2
License: MIT
Group: System Environment/Libraries
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://ftp.invisible-island.net/ncurses/%{name}-%{version}.tar.gz
Source1: %{name}-%{version}-%{release}.build.log
Source4: %{name}-6.1-librairies.tar.gz

Requires: libgcc >= 6.3.0-1
Requires: libstdc++ >= 6.3.0-1

BuildRequires: make, sed, findutils
BuildRequires: libtool >= 2.4.6-5
BuildRequires: libgcc >= 6.3.0-1
BuildRequires: libstdc++ >= 6.3.0-1


%define _libdir64 %{_prefix}/lib64

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.


%package devel
Summary: Development files for the ncurses library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.


%prep
%setup -q

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -rp 32bit/* 64bit/

# Extract old shared objects, to be added to new archive
mkdir lib_so_5
cd lib_so_5
cp %SOURCE4 .
gzip -d *.tar.gz
tar -xf $(basename *.tar)
/usr/bin/strip -X32 -e *.so.5.aix32
/usr/bin/strip -X64 -e *.so.5.aix64
cd -

%build
export PATH=/opt/freeware/bin:/usr/bin:/usr/linux/bin:/usr/local/bin:/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:.
# hack to get shared libraries working on AIX
find . -name Makefile.in -exec /opt/freeware/bin/sed -i 's/@OBJEXT@/lo/' {} \;

# setup environment for 32-bit and 64-bit builds
export CONFIG_SHELL=/bin/sh
export CONFIGURE_ENV_ARGS=/bin/sh

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CC="/opt/freeware/bin/gcc"
export CXX="/opt/freeware/bin/g++"

# shell function to configure ncurses
build_ncurses() {
	./configure \
		--prefix=%{_prefix} \
		--mandir=%{_mandir} \
		--libdir=$1 \
		--without-ada \
		--without-normal \
		--without-debug \
		--with-shared \
		--with-libtool \
		--enable-hard-tabs \
		--enable-xmc-glitch \
		--enable-colorfgbg \
		--disable-static \
		--with-shared


	make %{?_smp_mflags}
}

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CFLAGS="-O2 -maix64"
export CXXFLAGS=${CFLAGS}

export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_ncurses %{_libdir64}
cd ..

# now build the 32-bit version
cd 32bit
export OBJECT_MODE=32
export CFLAGS="-O2 -maix32"
export CXXFLAGS=${CFLAGS}

export LDFLAGS="-L/opt/freeware/lib -L/usr/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_ncurses %{_libdir}
cd ..

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export AR="/usr/bin/ar -X32_64"

# Install the 64 bit version
cd 64bit
export OBJECT_MODE=64
make DESTDIR=$RPM_BUILD_ROOT install

(
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)



# Install the 32 bits version
cd ../32bit
export OBJECT_MODE=32
make DESTDIR=$RPM_BUILD_ROOT install

cd ..

(
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in $(ls | grep -v -e _32 -e _64)
	do
		mv ${f} ${f}_32
		ln -sf ${f}_64 ${f}
	done
)


(
	for library in libncurses libpanel libmenu libform libncurses++
	do
		(
			# Extract .so.X
			cd ${RPM_BUILD_ROOT}%{_libdir}
			${AR} -x ${library}.a
			cd ${RPM_BUILD_ROOT}%{_libdir64}
			${AR} -x ${library}.a
		)


		# Create 32 bits libraries with 32/64bit members
		(
			cd ${RPM_BUILD_ROOT}%{_libdir}
			${AR} -rv ${library}.a ${library}.so.%{major_version}
			${AR} -q ${library}.a ${RPM_BUILD_ROOT}%{_libdir64}/${library}.so.%{major_version}
		)

		# Add old versions for compatibility
		cp lib_so_5/${library}.so.5.aix64 ${library}.so.5
		/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/${library}.a                 ${library}.so.5
		cp lib_so_5/${library}.so.5.aix32 ${library}.so.5
		/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/${library}.a                 ${library}.so.5

		# Create links for libpanel and libncurses which are requires by python
		# Remove the others
		(
			case ${library} in
				libncurses|libpanel)
					cd ${RPM_BUILD_ROOT}%{_libdir}
					ln -sf ${library}.so.%{major_version} ${library}.so
					cd ${RPM_BUILD_ROOT}%{_libdir64}
					ln -sf ${library}.so.%{major_version} ${library}.so
					;;
				*)
					rm ${RPM_BUILD_ROOT}%{_libdir}/${library}.so.%{major_version}
					rm ${RPM_BUILD_ROOT}%{_libdir64}/${library}.so.%{major_version}
					;;
			esac

		)
	done
)

(
	for library in libncurses libpanel libmenu libform libncurses++
	do
		# Create links for 64 bits libraries
        cd ${RPM_BUILD_ROOT}%{_libdir64}
		rm -f ${library}.a
		ln -sf ../lib/${library}.a ${library}.a
	done
)


# strip binaries
/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || true

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

echo "Tests are to be run manually in tests directory"


%files
%defattr(-,root,system,-)
%doc 32bit/ANNOUNCE 32bit/AUTHORS 32bit/README 32bit/TO-DO
%{_bindir}/[cirt]*
%{_libdir}/*.a
%{_libdir}/*.so*
%{_libdir64}/*.a
%{_libdir64}/*.so*
%{_libdir}/terminfo
%{_datadir}/terminfo
%{_datadir}/tabset
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/html/hackguide.html 32bit/doc/html/ncurses-intro.html 32bit/c++/README*
%{_bindir}/ncurses*-config*
%dir %{_includedir}/ncurses
%{_includedir}/ncurses/*.h
%{_mandir}/man3/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%changelog
* Thu Oct 08 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 6.2-2
- Update to 6.2

* Mon Oct 05 2020 Étienne Guesnet <etienne.guesnet.external@atos.net> - 6.2-1
- New version 6.2

* Mon Jul 20 2020 Clément Chigot <clement.chigot@atos.net> - 6.1-4
- Correctly distribute ncurses-config binaries

* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net> - 6.1-3
- BullFreeware Compatibility Improvements
- Add tests to %check section
- Remove /usr links
- Remove BuildRoot
- Add -Wl,-bmaxdata during 32bit build
- Remove .la files
- Fix %defattr inf %files sections

* Tue Jan 08 2019 Ayappan P <ayappap2@in.ibm.com> - 6.1-2
- Fix library issues

* Mon May 28 2018 Tony Reix <tony.reix@atos.net> -6.1-1
- Updated to latest version

* Mon Aug 01 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> -6.0p2016O730-1
- updated with all patches until 20160730

* Wed Jun 01 2016 Reshma V Kumar <reskumar@in.ibm.com> -6.0-1
- updated to latest version

* Fri Feb 03 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-3
- Initial port on Aix6.1

* Tue Oct 04 2011 Gerard Visiedo <gerard.visiedo@bull.net> - 5.9-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Wed Jul 13 2011 Gerard Visiedo <gerard.visiedo@bull.net - 5.9-1
- Initial port on Aix 5.3

