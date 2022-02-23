# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

Summary: A garbage collector for C and C++
Name:    gc
Version: 8.0.4
Release: 1
Group:   System Environment/Libraries
License: BSD
Url:     http://www.hboehm.info/gc/
Source0: https://www.hboehm.info/gc/gc_source/gc-%{version}.tar.gz

# Source1: libatomic_ops-7.4.4.tar.gz
Source100: %{name}-%{version}-%{release}.build.log

# Patch0:  %{name}-%{version}-3_powerpc_h.patch

# https://github.com/ivmai/bdwgc/issues/285
Patch0: gc-8.0.4-Fix-mmap-PROT_NONE-failure-on-AIX.patch

# https://github.com/ivmai/bdwgc/issues/348
Patch1: gc-8.0.4-Fix-ulong-undefined-compilation-error-on-AIX.patch

# Avoid undefined alloca
Patch2: gc-8.0.4-Include-alloca.h-when-using-alloca-on-AIX.patch

# _data and _end are already imported by libgc. There is 
# no need to import them again for every programs/libraries
# built with libgc
Patch3: gc-8.0.4-include-remove-import-of-_end-_data-for-AIX.patch

BuildRequires: automake libtool
BuildRequires: gcc-c++

%define _libdir64 %{_prefix}/lib64


%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

When using libgc.a in order to build a shared library, _end and _data
symbols must be imported. This two symbols are needed by libgc.a but
are only defined by the linker when creating an executable, not a shared
library.
Thus, make sure "-Wl,-bI:libgc.imp" is added with "libgc.imp" being:
"#! .
_data
_end
"


%package devel
Summary: Libraries and header files for %{name} development
Group:   Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# libgc needs _end and _data symbols which are created by
# ld only when creating an executable. When created a shared
# libraries this symbol must be imported.
%if %{with gcc_compiler}
cat <<EOF > libgc.imp
#! .
_data
_end
EOF
%endif

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf ..?* .[!.]* *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
# see https://bugzilla.redhat.com/689877
CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN"; export CPPFLAGS

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"


%if %{with gcc_compiler}
export __CC="gcc"
export __CXX="g++"
export FLAG32="-maix32"
export FLAG64="-maix64"
%else
export __CC="xlc_r"
export __CXX="xlC_r"
export FLAG32="-q32"
export FLAG64="-q64"

%endif

build_gc() {
    ./configure \
	--prefix=%{_prefix} \
	--libdir=$1 \
	--enable-shared --disable-static 
	# --with-libatomic-ops=no

    gmake %{?_smp_mflags}

}

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64

export CC="$__CC $FLAG64"
export CXX="$__CXX $FLAG64"
export CFLAGS="-O2"
export CXXFLAGS="$CFLAGS"
%if %{with gcc_compiler}
export LDFLAGS="-Wl,-bI:libgc.imp"
%endif

build_gc %{_libdir64}

# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32

export CC="$__CC $FLAG32"
export CXX="$__CXX $FLAG32"
export CFLAGS="-O2"
export CXXFLAGS="$CFLAGS"
%if %{with gcc_compiler}
export LDFLAGS="-Wl,-bI:libgc.imp"
%endif
export LDFLAGS="-Wl,-bmaxdata:0x80000000 $LDFLAGS"

build_gc %{_libdir}



%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

cd 64bit
export OBJECT_MODE=64
gmake install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE=32
gmake install DESTDIR=${RPM_BUILD_ROOT}

(
    # Extract .so from 64bit .a libraries and create links from /lib64 to /lib
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for f in lib*.a ; do
	${AR} -x ${f}
	rm -f ${f}
	ln -sf ../lib/${f} ${f}
    done

    # Create 32 bits libraries with 32/64bit members
    cd ${RPM_BUILD_ROOT}%{_libdir}
    for f in lib*.a ; do
	${AR} -q ${f} ${RPM_BUILD_ROOT}%{_libdir64}/`basename ${f} .a`.so.1
	rm ${RPM_BUILD_ROOT}%{_libdir64}/`basename ${f} .a`.so.1
    done

    # Create links for 64 bits libraries
    cd ${RPM_BUILD_ROOT}%{_libdir64}
    for f in lib*.a ; do
	rm -f ${f}
	ln -sf ../lib/${f} ${f}
    done
)

# # add the 64-bit shared objects to the shared libraries containing already the
# # 32-bit shared objects
# echo "%{name}   1   "   > input.lib.$$.tmp
# echo "cord      1   "  >> input.lib.$$.tmp

# cat input.lib.$$.tmp | while read lib number pad;
# do
#     SEP=".";
#      [ $number == "NULL" ] && { number="";SEP=""; }
#     # add the 64-bit shared object to the shared library containing already the
#     # 32-bit shared object
#     $AR -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
#     $AR -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/lib"$lib".a lib"$lib".so"$SEP$number"
#     (
# 	# Make the 64bits version of lib"$lib".a as a symbolic link to the 32bits version
# 	$RM ${RPM_BUILD_ROOT}%{_libdir64}/lib"$lib".a
# 	cd  ${RPM_BUILD_ROOT}%{_libdir64}
# 	ln -s ../lib/lib"$lib".a lib"$lib".a
#     )
# done
# rm -f input.lib.$$.tmp

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
cp doc/gc.man ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3
chmod 0644 ${RPM_BUILD_ROOT}%{_mandir}/man3/gc.3

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
%{_libdir}/*.a
%{_libdir64}/*.a

%files devel
%defattr(-,root,system,-)
%doc 32bit/README.md
%doc 32bit/README.QUICK
%doc 32bit/doc/*.md
%{_includedir}/*
%{_mandir}/*/*
%{_libdir}/pkgconfig/*.pc
%{_libdir64}/pkgconfig/*.pc


%changelog
* Wed May 26 2021 Clement Chigot <clement.chigot@atos.net> 8.0.4-1
- Update to version 8.0.4

- BullFreeware Compatibility Improvements
* Fri Sep 02 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-4
- Improve .spec file

* Fri Sep 02 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-3
- Improve .spec file

* Thu Aug 25 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-2
- Add gcc/xlc.

* Tue Aug 23 2016 Jean Girardet <Jean.Girardet@atos.net> - 7.6.0-1
- Update to version 7.6.0

* Fri Aug 05 2016 Tony Reix <tony.reix@atos.net> - 7.4.4-1
- Update to version 7.4.4

* Fri Aug 05 2016 Tony Reix <tony.reix@atos.net> - 7.4.2-2
- Add .pc files
- Fix issues with README files

* Fri Sep 18 2015 Pascal Oliva <pascal.oliva@atos.net> - 7.4.2-1
- Update to version 7.4.2

* Thu Nov 04 2014 Gerard Visiedo <gerard.visiedo@bull.net> - 6.8-1
- First port on Aix6.1
