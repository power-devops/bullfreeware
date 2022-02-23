# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

%define _libdir64 %{_prefix}/lib64

Summary: The GNU binutils development utilities
Name: binutils
Version: 2.37
Release: 4
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/binutils/
Source0: http://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.gz

Source1: binutils-2.37-copycsect.c
Source2: binutils-2.37-copycsect.make

Source1000:     %{name}-%{version}-%{release}.build.log

# Not mandatory with gcc8 but will be with futures gcc versions
Patch1: binutils-2.37-bfd-add-cast-to-avoid-gcc-errors.patch

# Adjust ld tests.
Patch2: binutils-2.37-ld-invert-exported-and-unexported-symbols-in-ld-test.patch
Patch3: binutils-2.37-ld-set-correct-flags-for-AIX-shared-tests.patch

# Backported patches
Patch4: binutils-2.37-bfd-avoid-a-crash-when-debug_section-isn-t-created-i.patch
Patch5: binutils-2.37-bfd-ensure-that-symbols-targeted-by-DWARF-relocation.patch
Patch6: binutils-2.37-gas-always-add-dummy-symbols-when-creating-XCOFF-sec.patch
Patch7: binutils-2.37-gas-correctly-output-XCOFF-tbss-symbols-with-XTY_CM-.patch
Patch8: binutils-2.37-gas-ensure-XCOFF-DWARF-subsection-are-initialized-to.patch
Patch9: binutils-2.37-gas-improve-C_BSTAT-and-C_STSYM-symbols-handling-on-.patch
Patch10: binutils-2.37-objdump-add-DWARF-support-for-AIX.patch

BuildRequires: flex >= 2.6.4
Requires: flex >= 2.6.4

# For tests
BuildRequires: dejagnu

%description
GNU binutils package contains utilities useful for development during
compilation.  Utilities such as nm, elfdump, size, and others are included.

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Requires: zlib-devel
Requires: binutils = %{version}-%{release}

%description devel
This package contains BFD and opcodes static libraries.

Unlike Fedora, dynamic libraries aren't provided.
Binutils documentation doesn't recommend to use libbfd
dynamically anyway, as its API is too unstable.

%package gccgov1
Summary:    Contains copycsect for GCCGo
Group:      Development/Languages
Requires:	gettext
Requires:	zlib
Requires:	libiconv

%description gccgov1
Contains copycsect ($OBJCOPY) for GCC Go.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# Add copycsect sources
mkdir copycsect
cp %{SOURCE1} copycsect/copycsect.c
cp %{SOURCE2} copycsect/copycsect.make

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

%build

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

export CFLAGS_COMMON="$RPM_OPT_FLAGS -O2"
export LIBINTL="-L/opt/freeware/lib -lintl"

# There is a problem when generating archives when nls is enabled.
# libintl.a will be added directly inside the static archives, blocking
# further compilations
# TODO: fix it and remove --disable-nls.

build_binutils() {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--disable-nls \
	--enable-pthread \
	--enable-threads \
	--disable-gdb \
	--enable-aix64a

    gmake

}

cd 64bit
# first build the 64-bit version
export CC="gcc -maix64"
export CFLAGS="$CFLAGS_COMMON"
export OBJECT_MODE=64

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib "

build_binutils %{_libdir64}

# Build copycsect for GCC Go.
# Only in 64bit as 32bit binaries aren't distributed anyway.
sh -x `pwd`/copycsect/copycsect.make 64 `pwd`

cd ../32bit
# now build the 32-bit version
export CC="gcc -maix32"
export CFLAGS="$CFLAGS_COMMON -D_LARGE_FILES"
export OBJECT_MODE=32

export LDFLAGS="-Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"

build_binutils %{_libdir}

# # remove the "-print-multi-os-directory" flag
# sed -e "s/MULTIOSDIR = \`\$(CC) \$(CFLAGS) -print-multi-os-directory\`/MULTIOSDIR = ./" libiberty/Makefile > Makefile.tmp
# mv -f Makefile.tmp libiberty/Makefile



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


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
cd ..

# Only provide 64bit version of binutils commands.
(
    # Replace 32bit command by 64bit version
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in $(ls | grep -v -e _64)
    do
	mv ${f}_64 ${f}
    done
)
# Retrieve copycsect
cp 64bit/copycsect/copycsect $RPM_BUILD_ROOT%{_bindir}/copycsect


(
    # Strip all of the executables
    cd $RPM_BUILD_ROOT%{_bindir}
    /usr/bin/strip * 2>/dev/null || :
)

# Do not create links between /lib64 libraries
# and /lib ones, because there are static ones for now.

# Gzip info
rm ${RPM_BUILD_ROOT}%{_infodir}/dir
gzip -9 ${RPM_BUILD_ROOT}%{_infodir}/*info*

# Rename commands already available on AIX with "gnu-" prefix.
# Binutils commands are still not fully compatible with AIX natives.
# Thus, it's better to not use them by default.
(
    cd ${RPM_BUILD_ROOT}%{_bindir}
    for f in ld ld.bfd as strip ranlib ar size nm; do
	mv $f gnu-$f
    done

    # However, in order to provide compatilibility, add links between
    # the previous and new names.
    for f in ld as strip ranlib; do
	ln -s gnu-$f g$f
    done

    # nm and size are working fine so they can be used as is.
    for f in nm size; do
	ln -s gnu-$f $f
    done
)

# Remove .la files
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm ${RPM_BUILD_ROOT}%{_libdir64}/*.la


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

# They are a lot of errors in ld tests because
# the current default gcc (gcc-8) doesn't allow to
# specify a different ld, as.
# Thus, ld tests are made with AIX one and not GNU one.

cd 64bit
(gmake -k check || true)
cd ../32bit
(gmake -k check || true)

%post
/sbin/install-info %{_prefix}/info/as.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/bfd.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/binutils.info.gz %{_prefix}/info/dir
echo "Commands also available on AIX are now prefixed with 'gnu-',"
echo "instead of just 'g'. 'gas' becomes 'gnu-as'."
echo "For now, in order to ensure a smooth transition, links between"
echo "the old and the new names are made."


%preun
if [ $1 = 0 ] ; then
    /sbin/install-info --delete %{_prefix}/info/as.info.gz %{_prefix}/info/dir || :
    /sbin/install-info --delete %{_prefix}/info/bfd.info.gz %{_prefix}/info/dir || :
    /sbin/install-info --delete %{_prefix}/info/binutils.info.gz %{_prefix}/info/dir || :
fi

%files
%defattr(-,root,system,-)
%doc 64bit/COPYING 64bit/COPYING.LIB 64bit/COPYING3 64bit/COPYING3.LIB 64bit/binutils/README 64bit/binutils/NEWS
%doc %{_prefix}/man/man1/*
# Avoid adding copycsect
%{_bindir}/*
%exclude %{_bindir}/copycsect
# %{_datadir}/locale/*/*/*
%{_infodir}/*

%files devel
%defattr(-,root,system,-)
%{_libdir64}/*
%{_libdir}/*
%{_includedir}/*


%files gccgov1
%defattr(-,root,system,-)
%{_bindir}/copycsect


%changelog
* Tue Sep 14 2021 Clément Chigot <clement.chigot@atos.net> - 2.37-4
- Backport patches improving P10, DWARF, etc

* Mon Aug 02 2021 Clément Chigot <clement.chigot@atos.net> - 2.37-3
- Add links towards new names for nm and size binaries.

* Thu Jul 29 2021 Clément Chigot <clement.chigot@atos.net> - 2.37-2
- Correctly launch tests in %check

* Tue Jul 20 2021 Clément Chigot <clement.chigot@atos.net> - 2.37-1
- Update to version 2.37
- Rename common commands with AIX: 'gnu-cmd'

* Thu Mar 09 2017 Tony Reix <tony.reix@atos.net > 2.25.1-4
- Improve BinUtils-2.25.1.GccGo-1.8.copycsect.make
- Add Requires: for binutils-gccv7go
- Add build.log
- Removing configure.info.gz : missing

* Mon Mar 06 2017 Tony Reix <tony.reix@atos.net > 2.25.1-3
- Add copycsect fo GCC Go.
- Add package binutils-gccv7go

* Tue Oct 11 2016 Tony Reix <tony.reix@atos.net > 2.25.1-2
- Add tests

* Thu Aug 06 2015 Hamza Sellami <hamza.sellami@atos.net > 2.25.1-1
- update to version 2.25.1 

* Fri Jun 29 2012 Patricia Cugny <patricia.cugny@bull.net> 2.22-1
- update to 2.22 and rename as to gas

* Thu Sep 22 2011 Patricia Cugny <patricia.cugny@bull.net> 2.21-2
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Fri May 27 2011 Gerard Visiedo <gerard.visiedo@bull.net> 2.21-1
- Update to 2.21

* Tue Oct 26 2004 David Clissold <cliss@austin.ibm.com> 2.14-3
- Ranlib has problems; rename to granlib and make nonexecutable.
- Users should use native AIX ranlib, but granlib will be present if
- anyone really wants it for whatever reason.

* Tue Jun 22 2004 David Clissold <cliss@austin.ibm.com> 2.14-2
- Fix "prereq" of install-info to be /sbin/install-info.

* Wed Jan 21 2004 David Clissold <cliss@austin.ibm.com> 2.14-1
- Initial version, adapted from old GNUPro.spec.

