# Tests by default. No tests: rpm -ba --define 'dotests 0' *.spec
%{!?dotests: %define dotests 1}

# compiler defauft gcc
# To use xlc : --define 'gcc_compiler=0'

%{?gcc_compiler:%define gcc_compiler 0}
%{!?gcc_compiler:%define gcc_compiler 1}

Name:    libatomic_ops
Summary: Atomic memory update operations
Version: 7.4.4
Release: 8%{?dist}

# libatomic_ops MIT, libatomic_ops_gpl GPLv2
License: GPLv2 and MIT
#URL:    http://www.hpl.hp.com/research/linux/atomic_ops/
URL:     https://github.com/ivmai/libatomic_ops/
Source0: http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-%{version}.tar.gz
# updated GPLv2 license text
Source1: http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Source2: %{name}-%{version}-%{release}.build.log

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

%define _libdir64 %{_prefix}/lib64

Patch0: %{name}-%{version}-8_ppc64_powerpc_h.patch
Patch1:   %{name}-%{version}-8_aix_powerpc_h.patch

Patch3: %{name}-%{version}_AO_HAVE_load.patch

## upstream patches
# 7.4 branch
Patch2: 0002-Fix-makefile-preventing-AO_pause-undefined-in-libato.patch
Patch5: 0005-Fix-missing-casts-to-match-printf-format-specifier-i.patch
Patch6: 0006-Eliminate-variable-set-but-not-used-Cppcheck-warning.patch
Patch7: 0007-Fix-missing-output-folder-on-making-auto-generated-h.patch
Patch9: 0009-Fix-missing-output-folder-on-making-auto-generated-t.patch
Patch15: 0015-Eliminate-signed-to-unsigned-value-extension-compile.patch
Patch17: 0017-Fix-GCC-5.x-compatibility-for-AArch64-double-wide-pr.patch

# master branch
Patch116: 0016-Use-LLD-and-SCD-instructions-on-mips64.patch
Patch117: 0017-Remove-inclusion-of-acquire_release_volatile.h-on-mi.patch
Patch118: 0018-Minor-fix-of-code-alignment-in-mips-AO_compare_and_s.patch

## upstreamable patches
# https://bugzilla.redhat.com/show_bug.cgi?id=1096574
Patch500: gc_ppc64le_force_AO_load.patch

# re-autofoo for patch2 (and others)
BuildRequires: automake libtool
Group:          Development/Languages

%description
Provides implementations for atomic memory update operations on a
number of architectures. This allows direct use of these in reasonably
portable code. Unlike earlier similar packages, this one explicitly
considers memory barrier semantics, and allows the construction of code
that involves minimum overhead across a variety of architectures.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Group:          Development/Languages

%description devel
Files for developing with %{name}.


#%package static
#Summary: Static library files for %{name}
#Requires: %{name}-devel%{?_isa} = %{version}-%{release}
#Group:          Development/Languages
#
#%description static
#Files for developing with %{name} and linking statically.

%prep
echo "dotests=%{dotests}"
echo "gcc_compiler=%{gcc_compiler}"
#%autosetup -p1
%setup -q

cp -p  ./src/atomic_ops/sysdeps/gcc/powerpc.h ./src/atomic_ops/sysdeps/gcc/powerpc.h.origine
%patch0
cp -p  ./src/atomic_ops/sysdeps/gcc/powerpc.h ./src/atomic_ops/sysdeps/gcc/powerpc.h.patch0
%patch1
cp -p  ./src/atomic_ops/sysdeps/gcc/powerpc.h ./src/atomic_ops/sysdeps/gcc/powerpc.h.patch1
%patch3

# To be worked later
# Patchs KO are: (all !)
#%patch2
#%patch5
#%patch6
#%patch7
#%patch9
#%patch15
#%patch17
#%patch116
#%patch117
#%patch118
#%patch500



# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit

export M4=/opt/freeware/bin/m4
export INSTALL=/opt/freeware/bin/install
export INSTALL=/usr/bin/install

cd 64bit
# patch50 introduces rpath (probably due to older libtool), refresh stuff here
autoreconf -fi
/opt/freeware/bin/install -m644 -p %{SOURCE1} ./COPYING
cd ..

cd 32bit
# patch50 introduces rpath (probably due to older libtool), refresh stuff here
autoreconf -fi
/opt/freeware/bin/install -m644 -p %{SOURCE1} ./COPYING
cd -


%build
export INSTALL=/opt/freeware/bin/install
export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export RM="/usr/bin/rm -f"
export M4=/opt/freeware/bin/m4

# ??? GLOBAL_CC_OPTIONS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGE_FILES "
GLOBAL_CC_OPTIONS=" "


# Choose XLC or GCC
%if %{gcc_compiler} == 1
export CC__="/opt/freeware/bin/gcc"
export CXX__="/opt/freeware/bin/g++"
export LDFLAGS=""
export FLAG32="-maix32"
export FLAG64="-maix64"
export CFLAGS=""

echo "CC Version:"
$CC__ --version

%else

# XLC specific (do NOT compile yet...)
export CC__="/usr/vac/bin/xlc"
export CXX__="/usr/vacpp/bin/xlC"
#export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"
export FLAG32="-q32"
export FLAG64="-q64"

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's:-fsigned-char::'`
export CFLAGS=`echo $CFLAGS | sed 's:-fsigned-char::'`

echo "CC Version:"
$CC__ -qversion

%endif


type $CC__
type $CXX__

export CC32=" ${CC__}  ${FLAG32}"
export CXX32="${CXX__} ${FLAG32}"
export CC64=" ${CC__}  ${FLAG64}"
export CXX64="${CXX__} ${FLAG64}"

export CFLAGS="$CFLAGS -O2"


cd 64bit

export CC="${CC64}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX64} $GLOBAL_CC_OPTIONS"

export OBJECT_MODE=64

export AR="/usr/bin/ar -X64"
export NM="/usr/bin/nm -X64"
export STRIP="/usr/bin/strip -X64"

echo "compiler="$CC

./configure \
    --enable-shared \
    --includedir=%{_includedir} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --bindir=%{_bindir} \
  --disable-silent-rules

gmake %{?_smp_mflags}


if [ "%{dotests}" == 1 ]
then
    ( gmake check %{?arch_ignore} || true )
fi


cd ../32bit

export CC="${CC32}   $GLOBAL_CC_OPTIONS"
export CXX="${CXX32} $GLOBAL_CC_OPTIONS"

export OBJECT_MODE=32

export AR="/usr/bin/ar -X32"
export NM="/usr/bin/nm -X32"
export STRIP="/usr/bin/strip -X32"

echo "compiler="$CC

./configure \
  --enable-shared \
  --prefix=%{_prefix} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --bindir=%{_bindir} \
  --disable-silent-rules

gmake %{?_smp_mflags}


if [ "%{dotests}" == 1 ]
then
    ( gmake check %{?arch_ignore} || true )
fi

cd ..


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export INSTALL=/opt/freeware/bin/install

export PATH=/usr/bin:/etc:/usr/sbin:/usr/ucb:/usr/bin/X11:/sbin:.
export LIBPATH=
export RM="/usr/bin/rm -f"

cd 64bit
export OBJECT_MODE=64
export AR="/usr/bin/ar -X64"

gmake install DESTDIR=%{buildroot}


cd ../32bit
export OBJECT_MODE=32
export AR="/usr/bin/ar -X32"

gmake install DESTDIR=%{buildroot}

cd ..

# Extraction des .so 64 puis 32
(
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for f in *.a ; do
	/usr/bin/ar -X64 -x ${f}
    done

    cd ${RPM_BUILD_ROOT}%{_libdir}
    for f in *.a ; do
	/usr/bin/ar -X32 -x ${f}
    done
)


# add the 64-bit shared objects to the shared libraries containing already the
# 32-bit shared objects
echo "atomic_ops      1   "  > input.lib.$$.tmp
echo "atomic_ops_gpl  1   " >> input.lib.$$.tmp

cat input.lib.$$.tmp | while read lib number pad;
do
    SEP=".";
    [ $number == "NULL" ] && { number="";SEP=""; }
    # add the 64-bit shared object to the shared library containing already the
    # 32-bit shared object
    $AR -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
    $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a lib"$lib".so"$SEP$number"
    (
	# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
	$RM ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
	cd  ${RPM_BUILD_ROOT}%{_libdir64}
	ln -s ../lib/lib"$lib".a lib"$lib".a
    )
done
rm -f input.lib.$$.tmp


(
    cd ${RPM_BUILD_ROOT}
    for dir in include lib lib64
    do
	mkdir -p usr/${dir}
	cd usr/${dir}
	ln -sf ../..%{_prefix}/${dir}/* .
	cd -
    done
)



## unpackaged files
#rm -f 64bit/%{buildroot}%{_libdir}/lib*.la
#rm -f 32bit/%{buildroot}%{_libdir}/lib*.la
# omit dup'd docs
rm -f 64bit/%{buildroot}%{_datadir}/libatomic_ops/{COPYING,README*,*.txt}
rm -f 32bit/%{buildroot}%{_datadir}/libatomic_ops/{COPYING,README*,*.txt}


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# %post -p /sbin/ldconfig
# %postun -p /sbin/ldconfig


%files
# %license COPYING
%doc 32bit/doc/LICENSING.txt
%doc 32bit/AUTHORS 32bit/ChangeLog 32bit/README.md

%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a
%{_libdir}/libatomic_ops.so.1*
%{_libdir}/libatomic_ops_gpl.so.1*

%{_libdir64}/libatomic_ops.a
%{_libdir64}/libatomic_ops_gpl.a
%{_libdir64}/libatomic_ops.so.1*
%{_libdir64}/libatomic_ops_gpl.so.1*

/usr/lib/*.a
/usr/lib/*.so*
/usr/lib64/*.a
/usr/lib64/*.so*


%files devel
%doc 32bit/doc/README*

%{_includedir}/atomic_ops.h
%{_includedir}/atomic_ops_malloc.h
%{_includedir}/atomic_ops_stack.h
%{_includedir}/atomic_ops/

%{_libdir}/lib*.la
%{_libdir}/pkgconfig/atomic_ops.pc
%{_libdir64}/lib*.la
%{_libdir64}/pkgconfig/atomic_ops.pc

/usr/include/*
/usr/lib/*.la
/usr/lib64/*.la


#%files static
#%{_libdir}/libatomic_ops.a
#%{_libdir}/libatomic_ops_gpl.a
#%{_libdir64}/libatomic_ops.a
#%{_libdir64}/libatomic_ops_gpl.a


%changelog
* Wed Oct 19 2016 jean Girardet <Jean.Girardet@atos.net> 7.4.4-8
- 7.4.4 : Finalize patch power pc

* Mon Oct 03 2016 jean Girardet <Jean.Girardet@atos.net> 7.4.4
- 7.4.4-6 : Correct missing file in devel rpm

* Mon Sep 26 2016 jean Girardet <Jean.Girardet@atos.net> 7.4.4-5
- removes the dependency has : /sbin/ldconfig, modify patch powerpc

* Wed Sep 21 2016 jean Girardet <Jean.Girardet@atos.net> 7.4.4-4
- Patch libatomic_ops-7.4.4_AO_HAVE_load.patch (src/atomic_ops/sysdeps/loadstore/atomic_load.h)

* Fri Sep 19 2016 jean Girardet <Jean.Girardet@atos.net> 7.4.4-3
 - Some improvements

* Fri Sep 16 2016 Jean Girardet <Jean.Girardet@atos.net> 7.4.4-2
- Modify patch powerpc : to resolve : test_stack failed

* Fri Sep 02 2016 Tony Reix <tony.reix@atos.net> 7.4.4-1
- Initial port on AIX 6.1

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-9
- make check fails on test_stack for ppc64le arch (#1096574), drop reference to 0032.patch

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.4.2-8
- pull in upstream (7.4 branch) fixes
- Add support for 64-bit MIPS (#1317509)
- use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul  7 2015 Peter Robinson <pbrobinson@fedoraproject.org> 7.4.2-6
- Don't fail check on aarch64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-2
- link libatomic_ops_gpl against libatomic_ops for missing symbol(s)

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-1
- libatomic_opts-7.4.2
- new upstream/source URLs
- %%check: skip ppc64le too
- License: MIT and GPLv2
- update/longer %%description
- updated GPLv2 license text (with correct address)

* Wed Dec 04 2013 Rex Dieter <rdieter@fedoraproject.org>  7.4.0-1
- separate libatomic_ops lives again!

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-8.gc
- use gc tarball, tag gc release

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2-7
- devel: Provides: %%name-static ...
- consolidate %%doc's
- %%files: track libs

* Wed May 20 2009 Dan Horak <dan[t]danny.cz> - 1.2-6
- added fix for s390

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 22 2008 Jon Stanley <jonstanley@gmail.com> - 1.2-4
- Fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2-3
- Autorebuild for GCC 4.3

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 1.2-2
- Added fix for PPC AO_load_acquire.

* Fri Nov 10 2006 Pierre Ossman <drzeus@drzeus.cx> 1.2-1
- Update to 1.2.

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-2
- Fix naming of package.
- General cleanup of spec file.

* Wed Aug 30 2006 Pierre Ossman <drzeus@drzeus.cx> 1.1-1
- Initial package for Fedora Extras.
