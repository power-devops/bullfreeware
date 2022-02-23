# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary:	Automated text file generator
Name:		autogen
Version:	5.18.16
Release:	1
# Some files are licensed under GPLv2+.
# We redistribute them under GPLv3+.
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/autogen/
Source0:	ftp://ftp.gnu.org/gnu/autogen/rel%{version}/%{name}-%{version}.tar.xz

Patch1:	%{name}-5.18.7-pkgconfig.patch
Patch2:	%{name}-5.18.7-lintl.patch
# Fix gcc error on overlapping strings
Patch3:		autogen-overlap.patch

# Change getdate_r for getdate
Patch4:	%{name}-5.18.16-remove-getdate_r.patch

# Add stat time convertion to struct timespec
Patch5:	%{name}-5.18.16-agen5-convert-stat.st_mtime-to-struct-timespec-on-AI.patch

Source100:	%{name}-%{version}-%{release}.build.log


BuildRequires:	guile-devel >= 2.0.14
BuildRequires:	libtool
BuildRequires:	libxml2-devel

%description
AutoGen is a tool designed to simplify the creation and maintenance of
programs that contain large amounts of repetitious text. It is especially
valuable in programs that have several blocks of text that must be kept
synchronised.

This package is available in 32bit and 64bit.


%package libopts
Summary:	Automated option processing library based on %{name}
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		System Environment/Libraries

%description libopts
Libopts is very powerful command line option parser consisting of a set of
AutoGen templates and a run time library that nearly eliminates the hassle of
parsing and documenting command line options.


%package libopts-devel
Summary:	Development files for libopts
# Although sources are dual licensed with BSD, some autogen generated files
# are only under LGPLv3+. We drop BSD to avoid multiple licensing scenario.
License:	LGPLv3+
Group:		Development/Libraries

Requires:	automake
Requires:	%{name}-libopts = %{version}-%{release}
Requires:	pkgconfig

%description libopts-devel
This package contains development files for libopts.


%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build

# # Due to a bug, the build breaks with this message:   columns program is not findable
# # A work-around is to add a symlink to columns installed with previous version of autogen
# # I'm not sure the columns built by this version works fine...
# # ln -s /opt/freeware/bin/columns /columns
# #
# # Tests need the 64bit/32bit version... so 2 symlink are executed when testing.
# # So: 1) Build 2) Install 3) Build&Test
# #
# if test -L /columns; then
# echo "/columns is there !"
# else
# echo "/columns is missing !"
# echo "Do: ln -s /opt/freeware/bin/columns /columns"
# exit
# fi
#
# The issue deals with:
# autoopts/tpl/agtexi-cmd.tpl :
#    (shell "CLexe=${AGexe%/agen5/*}/columns/columns
# where AGexe is empty.
# Code thus looks for: /columns/columns and then /columns .

# The code is using -Werror but there are some warnings triggered for
# small things. Fedora do the same.
export CFLAGS_COMMON="-O2 -Wno-implicit-fallthrough -Wno-format-overflow \
		-Wno-format-truncation"

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


build_autogen() {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--disable-dependency-tracking

    gmake %{?_smp_mflags}
}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

build_autogen %{_libdir64}

cd ..

cd 32bit
cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000 "

build_autogen %{_libdir}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
make DESTDIR=${RPM_BUILD_ROOT} install

(
    # Change 64bit binaries' name
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in *
    do
	mv ${f} ${f}_64
    done
)

cd ../32bit
export OBJECT_MODE=32
make DESTDIR=${RPM_BUILD_ROOT} install

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
    %define liboptssoversion 25

    # Extract .so from 64bit .a libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    ${AR} -x libopts.a

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    ${AR} -q libopts.a ${RPM_BUILD_ROOT}%{_libdir64}/libopts.so.%{liboptssoversion}
    rm ${RPM_BUILD_ROOT}%{_libdir64}/libopts.so.%{liboptssoversion}

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    rm -f libopts.a
    ln -sf ../lib/libopts.a libopts.a
)

# Gzip info
rm   -f ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
(gmake -k check || true)

cd ../32bit
(gmake -k check || true)

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS
%doc 32bit/ChangeLog
%doc 32bit/COPYING
%doc 32bit/NEWS
%doc 32bit/README
%doc 32bit/THANKS
%doc 32bit/pkg/libopts/COPYING.gplv3

%{_bindir}/columns*
%{_bindir}/getdefs*
%{_bindir}/%{name}*
%{_bindir}/xml2ag*
%{_infodir}/*info*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%files libopts
%defattr(-,root,system,-)
%doc 32bit/pkg/libopts/COPYING.mbsd
%doc 32bit/pkg/libopts/COPYING.lgplv3
%{_libdir}/*.a
%{_libdir64}/*.a


%files libopts-devel
%defattr(-,root,system,-)
%{_bindir}/autoopts-config*
%{_datadir}/aclocal/autoopts.m4
#%{_datadir}/aclocal/liboptschk.m4
%{_libdir}/*.a
%{_libdir64}/*.a
%{_libdir}/pkgconfig/autoopts.pc
%{_libdir64}/pkgconfig/autoopts.pc

%dir %{_includedir}/autoopts
%{_includedir}/autoopts/options.h
%{_includedir}/autoopts/usage-txt.h


%changelog
* Wed May 26 2021 Clement Chigot <clement.chigot@atos.net> 5.18.16-1
- Update to version 5.18.16
- BullFreeware Compatibility Improvements
- Rebuild with RPMv4

* Tue Aug 23 2016 Tony Reix <tony.reix@atos.net> - 5.18.7-1
- Initial port on AIX 6.1
- Work-around /columns issue
- Work-around defs & library -lintl issue
- Fix all 32/64 issues

* Tue Sep 29 2015 Pascal OLIVA <pascal.oliva@atos.net> - 5.12-1
- Porting for AIX
