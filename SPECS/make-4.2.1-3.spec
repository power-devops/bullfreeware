%{!?gcc_compiler: %define gcc_compiler 1}
%{!?default_bits: %define default_bits 32}
%{!?dotests: %define dotests 1}

Summary: A GNU tool which simplifies the build process for users
Name: make
Epoch: 1
Version: 4.2.1
%global LastVersion 4.2.1
Release: 3
License: GPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/make/
Source0: ftp://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnu.org/gnu/make/%{name}-%{version}.tar.bz2.sig
Source2: %{name}-%{version}-%{release}.build.log
Patch0: make-4.1-aixrealpath.patch
Patch1: make-4.1-aixSyncAndDashl.patch
Patch2: make-4.1-aixfopen-fail.patch
Patch3: make-4.1-aixREADME.patch
Patch4: make-4.1-aixOptionDisabled.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# make check on anything below AIX 5.3 produces tons of errors :-(
BuildRequires: AIX-rpm >= 5.3.0.0
Requires: AIX-rpm >= 5.3.0.0

BuildRequires: /sbin/install-info, info
BuildRequires: gettext-devel
BuildRequires: guile-devel
Requires: /sbin/install-info, info
Requires: gettext
Requires: guile

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files. Make
allows users to build and install packages without any significant
knowledge about the details of the build process. The details about
how the program should be built are provided for make in the program's
makefile.


%prep
echo "dotests=%{dotests}"
echo "default_bits=%{default_bits}"
echo "gcc_compiler=%{gcc_compiler}"
%if %{gcc_compiler} == 1
echo "GCC version=`/opt/freeware/bin/gcc --version | head -1`"
%endif
%setup -q
%patch0 -p1 -b %{name}-%{LastVersion}-aixrealpath.patch
%patch1 -p1 -b .aixSyncAndDashl
cd tests
%patch2 -p1 -b .aixfopen-fail
%patch3 -p1 -b .aixREADME
cd ..
%patch4 -p1 -b .aixOptionDisabled

cd tests
sed -e 's/\-O/\--output-sync=/' ./scripts/features/output-sync >  ./scripts/features/output-sync.tmp1.$$
mv  ./scripts/features/output-sync.tmp1.$$ ./scripts/features/output-sync
cd ..

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
cp -rp . /tmp/%{name}-%{version}-32bit
rm -rf *
mv /tmp/%{name}-%{version}-32bit 32bit
cp -rp 32bit 64bit

%build
%if %{gcc_compiler} == 1
export FLAG32="-maix32"
export FLAG64="-maix64"
export CC=/opt/freeware/bin/gcc
%else
export FLAG32="-q32"
export FLAG64="-q64"
export CC=/usr/vac/bin/xcl_r
%endif
export CC32="${CC}  ${FLAG32}"
export CC64="${CC}  ${FLAG64}"

export PATH=/usr/bin:/usr/linux/bin:/usr/local/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:/usr/samples/kernel:.
export LIBPATH=/opt/freeware/lib:/usr/lib
export CFLAGS=
export AR=/usr/bin/ar

build_make() {
    echo "Building ${OBJECT_MODE}-bit version"
    cd ${OBJECT_MODE}bit
    ./configure \
        --prefix=%{_prefix} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir}
    gmake %{?_smp_mflags}

    if [ "%{dotests}" == 1 ]
    then
        echo "Testing ${OBJECT_MODE}-bit version"
        ( gmake -k check || true )
        /usr/sbin/slibclean
    fi
    cd ..
}

export OBJECT_MODE=64
export CC=${CC64}
build_make

export OBJECT_MODE=32
export CC=${CC32}
build_make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
gmake DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/make ${RPM_BUILD_ROOT}%{_bindir}/make_64
cd ..

cd 32bit
gmake DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/make ${RPM_BUILD_ROOT}%{_bindir}/make_32
cd ..

/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :
#*/

DEFAULT_BITS=64
if [ "%{default_bits}" == 32 ]; then
    DEFAULT_BITS=32
fi

ln -sf make_${DEFAULT_BITS} ${RPM_BUILD_ROOT}%{_bindir}/make
ln -sf make ${RPM_BUILD_ROOT}%{_bindir}/gmake
ln -sf make.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/gmake.1

chmod 0755 ${RPM_BUILD_ROOT}%{_bindir}/*

gzip --best ${RPM_BUILD_ROOT}%{_infodir}/make.info*
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

cd ${RPM_BUILD_ROOT}
mkdir -p usr/linux/bin
ln -sf ../../..%{_bindir}/make usr/linux/bin

mkdir -p usr/bin
ln -sf ../..%{_bindir}/make usr/bin/gmake


%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :


%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir --entry="* Make: (make).                 The GNU make utility." || :
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/NEWS 32bit/README 32bit/COPYING 32bit/AUTHORS
%{_bindir}/*
%{_mandir}/man?/*
%{_infodir}/*.info*
%{_datadir}/locale/*/*/*
/usr/bin/*
/usr/linux/bin/*


%changelog
* Mon Sep 26 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 4.2.1-3
- fixed bad rpath in binaries

* Tue Sep 06 2016 Matthieu Sarter <matthieu.sarter.external@atos.net> - 4.2.1-1
- switched to GCC compiler
- added 64 bit build
- updated to version 4.2.1

* Mon Oct 06 2014 Michael Perzl <michael@perzl.org> - 4.1-1
- updated to version 4.1

* Wed Oct 09 2013 Michael Perzl <michael@perzl.org> - 4.0-1
- updated to version 4.0

* Wed Jul 28 2010 Michael Perzl <michael@perzl.org> - 3.82-1
- updated to version 3.82

* Wed Jul 28 2010 Michael Perzl <michael@perzl.org> - 3.81-1
- updated to version 3.81

* Thu Jul 01 2010 Michael Perzl <michael@perzl.org> - 3.80-3
- removed dependency on gettext

* Mon Sep 15 2008 Michael Perzl <michael@perzl.org> - 3.80-2
- first version for AIX V5.1 and higher
