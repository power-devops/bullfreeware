# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define		_libdir64 %{_prefix}/lib64

Summary:   Character set conversion library, portable iconv implementation
Name:      libiconv
Version:   1.16
Release:   3
Group:     System Environment/Libraries
License:   LGPL
URL:       http://www.gnu.org/software/libiconv/
Source0:   http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Source1000:	%{name}-%{version}-%{release}.build.log

%define _libdir64 %{_prefix}/lib64

# Makefile is directly adding objects from /lib/libiconv.a (ie shr4.o, shr.o, shr4_64.o).
# However, these need to be stripped before being added.
Patch2:   %{name}-%{version}-lib-makefile-strip-AIX-libiconv-objects.patch

# Fix linking with shared libraries
Patch3:   %{name}-%{version}-configure-fix-shrext-for-AIX-without-brtl.patch
Patch4:   %{name}-%{version}-configure-fix-disable-rpath.patch


# there is a circular dependency between gettext and libiconv
# first build and install libiconv, then build and install gettext then build and install again libiconv
# comment the following lines if gettext not installed
# see also %files section
BuildRequires: gettext
BuildRequires: gettext-devel

%description
GNU libiconv provides an iconv() implementation for use on systems
which do not have one or whose implementation cannot convert from/to Unicode.

The library is available as 32-bit and 64-bit.


%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# work around strange configure error on AIX6.1, see details at:
# https://www.ibm.com/developerworks/forums/thread.jspa?messageID=14145662
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.

# setup environment for 32-bit and 64-bit builds
export RM="rm -f"
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export STRIP="/usr/bin/strip -X32_64"
export CC="gcc"
export CFLAGS_BASE="-D_GNU_SOURCE"


build_libiconv() {
	./configure \
		--prefix=%{_prefix} \
		--libdir=$1 \
		--infodir=%{_infodir} \
		--mandir=%{_mandir} \
		--enable-shared --disable-static \
		--enable-extra-encodings \
		--disable-rpath

	gmake %{?_smp_mflags}

}

# first build the 64-bit version
cd 64bit

export OBJECT_MODE=64
export CFLAGS="$CFLAGS_BASE -maix64"
export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"

build_libiconv %{_libdir64}

cd ../32bit
# now build the 32-bit version
export OBJECT_MODE=32
export CFLAGS="$CFLAGS_BASE -maix32"
export LDFLAGS="-Wl,-bmaxdata:0x80000000 -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib"

build_libiconv %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# install 64-bit version
export OBJECT_MODE=64
cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install

(
	# Change 64bit binaries' name
	cd ${RPM_BUILD_ROOT}%{_bindir}
	for f in *
	do
		mv ${f} ${f}_64
	done
)
cd ..

# install 32-bit version
cd 32bit
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

(
	# Extract 64bit members
	cd ${RPM_BUILD_ROOT}%{_libdir64}
	${AR} -x libiconv.a
	${AR} -x libcharset.a

	# Include 64bit members in 32bit archives
	cd ${RPM_BUILD_ROOT}%{_libdir}
	${AR} -q libiconv.a ${RPM_BUILD_ROOT}%{_libdir64}/libiconv.so.2
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libiconv.so.2
	${AR} -q libcharset.a ${RPM_BUILD_ROOT}%{_libdir64}/libcharset.so.1
	rm ${RPM_BUILD_ROOT}%{_libdir64}/libcharset.so.1

	# Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
	rm -f libiconv.a
	ln -sf ../lib/libiconv.a libiconv.a
	rm -f libcharset.a
	ln -sf ../lib/libcharset.a libcharset.a

)


/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
gmake -k check

cd ../32bit
gmake -k check


%post
# we need to include all shared members of the system wide /usr/lib/libiconv.a
# at rpm installation time to avoid core dump of system binaries

export AR="/usr/bin/ar -X32_64"

/usr/bin/mkdir -p /tmp/libiconv.tmp
cd  /tmp/libiconv.tmp
LIST=`${AR} -t /usr/lib/libiconv.a`
${AR} -x /usr/lib/libiconv.a
/usr/bin/strip -X32_64 -e *
cp %{_libdir}/libiconv.a %{_libdir}/libiconv.a.tmp
for i in ${LIST}
do
   if [ "$i" != "libiconv.so.2" ]; then
     echo "add $i shared members from /usr/lib/libiconv.a to %{_libdir}/libiconv.a.tmp"
    ${AR} -r %{_libdir}/libiconv.a.tmp ${i}
   fi
done
echo "Replacing %{_libdir}/libiconv.a by %{_libdir}/libiconv.a.tmp"
mv %{_libdir}/libiconv.a.tmp %{_libdir}/libiconv.a
cd -
/usr/bin/rm -rf /tmp/libiconv.tmp

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS* 32bit/COPYING.LIB* 32bit/ChangeLog* 32bit/DESIGN*
%doc 32bit/INSTALL.generic* 32bit/NEWS* 32bit/NOTES* 32bit/README* 32bit/THANKS*
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.a
%{_libdir64}/*.a
%{_mandir}/man?/*
# comment the following line if gettext not installed
%{_datadir}/locale/*/*/*

%changelog
* Fri Dec 06 2019 Clément Chigot <clement.chigot@atos.net - 1.16-3
- BullFreeware Compatibility Improvements
- Move tests to %check section
- Remove /usr links
- Correctly build/install 32bit and 64bit version
- Fix configure for AIX shared libraries
- Remove .la
- Fix %defattr inf %files sections

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
