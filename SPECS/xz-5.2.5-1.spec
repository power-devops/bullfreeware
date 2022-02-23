# By default, dotests are run.
# No tests: rpmbuild -ba --without dotests *.spec
%bcond_without dotests

# By default, gcc is used.
# Choose XLC: rpmbuild -ba --without gcc_compiler *.spec
%bcond_without gcc_compiler

Summary:	LZMA compression utilities
Name:		xz
Version: 5.2.5
Release: 1
License:	LGPLv2+
Group:		Applications/File

Source0:	https://sourceforge.net/projects/lzmautils/files/%{name}-%{version}.tar.gz
URL:		http://tukaani.org/xz
Source2:	liblzma.so.0-aix32
Source3:	liblzma.so.0-aix64
Source1000:	%{name}-%{version}-%{release}.build.log

BuildRequires:	make
BuildRequires:	gettext-devel
BuildRequires:	pkg-config
BuildRequires:	bash

Requires:	%{name}-libs = %{version}-%{release}
Requires:	bash
Requires:	gettext

%define _libdir64 %{_prefix}/lib64

%global _smp_mflags -j4


%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package libs
Summary: Libraries for decoding LZMA compression
Group: System Environment/Libraries
License: LGPLv2+

%description libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package devel
Summary: Devel libraries & headers for liblzma
Group: Development/Libraries
License: LGPLv2+
Requires: %{name}-libs = %{version}-%{release}
Requires: pkg-config

%description  devel
Devel libraries and headers for liblzma.


%package lzma-compat
Summary: Older LZMA format compatibility binaries
Group: Development/Libraries
# lz{grep,diff,more} are GPLv2+. Other binaries are LGPLv2+
License: GPLv2+ and LGPLv2+
Requires: %{name} = %{version}-%{release}
Requires: gettext
Obsoletes: lzma < 5
Provides: lzma = 5

%description  lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.


%prep
echo "dotests=%{dotests}"
%setup -q

# fake a <stdbool.h> as AIX5L V5.1 and XLC/C++ V7 doesn't have one
cat > stdbool.h <<EOF
// EOF
#ifndef stdbool_h_wrapper
#define stdbool_h_wrapper

typedef enum {false = 0, true = 1} bool;

#endif
EOF

# Duplicate source for 32 & 64 bits
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -rf *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
export PATH=/opt/freeware/bin:$PATH
export CONFIG_SHELL=/opt/freeware/bin/bash
export CONFIG_ENV_ARGS=/opt/freeware/bin/bash
export RM="/usr/bin/rm -f"

# XLC
#	export CC="/usr/vac/bin/xlc_r -qlanglvl=extc99 -qcpluscmt"
#	export CFLAGS__="$CFLAGS -O2 -D_FILE_OFFSET_BITS=64"
#	export CXXFLAGS__="$CXXFLAGS -O2 -D_FILE_OFFSET_BITS=64"

# first build the 64-bit version
cd 64bit

# XLC
#	export CFLAGS="$CFLAGS__ -q64"

export CC="gcc -maix64 -O2 -D_FILE_OFFSET_BITS=64"
export CXX="g++ -maix64 -O2 -D_FILE_OFFSET_BITS=64"
export LDFLAGS="-L/opt/freeware/lib64 -L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib64:/opt/freeware/lib:/usr/lib:/lib"
export OBJECT_MODE=64

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake %{_smp_mflags}

# now build the 32-bit version
cd ../32bit

# XLC
#	export CFLAGS="$CFLAGS__ -q32"

export CC="gcc -maix32 -O2 -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export CXX="g++ -maix32 -O2 -D_LARGE_FILES -D_FILE_OFFSET_BITS=64"
export LDFLAGS="-L/opt/freeware/lib -Wl,-blibpath:/opt/freeware/lib:/usr/lib:/lib -Wl,-bmaxdata:0x80000000"
export OBJECT_MODE=32

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake %{_smp_mflags}


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE=64
gmake install DESTDIR=${RPM_BUILD_ROOT}
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_64
    done
)
(
    cd ${RPM_BUILD_ROOT}/%{_prefix}/bin
    ln -sf xz_64     lzcat_64
    ln -sf xzdiff_64 lzcmp_64
    ln -sf xzdiff_64 lzdiff_64
    ln -sf xzgrep_64 lzegrep_64
    ln -sf xzgrep_64 lzfgrep_64
    ln -sf xzgrep_64 lzgrep_64
    ln -sf xzless_64 lzless_64
    ln -sf xz_64     lzma_64
    ln -sf xzmore_64 lzmore_64
    ln -sf xz_64     unlzma_64
    ln -sf xz_64     unxz_64
    ln -sf xz_64     xzcat_64
    ln -sf xzdiff_64 xzcmp_64
    ln -sf xzgrep_64 xzegrep_64
    ln -sf xzgrep_64 xzfgrep_64
)

cd ../32bit
export OBJECT_MODE=32
gmake install DESTDIR=${RPM_BUILD_ROOT}
(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
	mv $fic "$fic"_32
	ln -sf "$fic"_64 $fic
    done
)
(
    cd ${RPM_BUILD_ROOT}/%{_prefix}/bin
    ln -sf xz_32     lzcat_32
    ln -sf xzdiff_32 lzcmp_32
    ln -sf xzdiff_32 lzdiff_32
    ln -sf xzgrep_32 lzegrep_32
    ln -sf xzgrep_32 lzfgrep_32
    ln -sf xzgrep_32 lzgrep_32
    ln -sf xzless_32 lzless_32
    ln -sf xz_32     lzma_32
    ln -sf xzmore_32 lzmore_32
    ln -sf xz_32     unlzma_32
    ln -sf xz_32     unxz_32
    ln -sf xz_32     xzcat_32
    ln -sf xzdiff_32 xzcmp_32
    ln -sf xzgrep_32 xzegrep_32
    ln -sf xzgrep_32 xzfgrep_32
)

# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/liblzma.a
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/liblzma.a  liblzma.so.5
(
  rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/liblzma.a
  cd        ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s     ../lib/liblzma.a .
)


# Add the older 4.999.9 shared members for compatibility with older apps
# (make sure they're set for LOADONLY with 'strip -e')
cp %{SOURCE2} liblzma.so.0
/usr/bin/strip -X32 -e liblzma.so.0
/usr/bin/ar -X32 -q ${RPM_BUILD_ROOT}%{_libdir}/liblzma.a liblzma.so.0

cp %{SOURCE3} liblzma.so.0
/usr/bin/strip -X64 -e liblzma.so.0
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/liblzma.a liblzma.so.0


/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/* || :

rm -rf ${RPM_BUILD_ROOT}%{_docdir}/%{name}


#(
#  cd ${RPM_BUILD_ROOT}
#  for dir in bin include lib lib64
#  do
#    mkdir -p usr/${dir}
#    cd usr/${dir}
#    ln -sf ../..%{_prefix}/${dir}/* .
#    cd -
#  done
#  [ -L usr/include/lzma ] && rm -f usr/include/lzma
#  mkdir -p usr/include/lzma
#  cd usr/include/lzma
#  ln -sf ../../..%{_prefix}/include/lzma/* .
#  cd -
#)


%check
%if %{without dotests}
echo "*** Skipping tests"
exit 0
%endif # without dotests

cd 64bit
    ( gmake -k check || true )
    /usr/sbin/slibclean

cd ../32bit
    ( gmake -k check || true )
    /usr/sbin/slibclean


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/README 32bit/THANKS 32bit/COPYING.* 32bit/ChangeLog 
%{_bindir}/*xz*
%{_mandir}/man1/*xz*


%files libs
%defattr(-,root,system,-)
%doc 32bit/COPYING.*
%{_libdir}/*.a
%{_libdir64}/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/faq.txt 32bit/doc/lzma-file-format.txt
%doc 32bit/doc/xz-file-format.txt 32bit/doc/history.txt
%{_includedir}/lzma*
%{_libdir}/pkgconfig/liblzma.pc
%{_libdir64}/pkgconfig/liblzma.pc


%files lzma-compat
%defattr(-,root,system,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*


%changelog
* Tue Oct 27 2020 Bullfreeware Continuous Integration <bullfreeware@atos.net> - 5.2.5-1
- Update to 5.2.5

* Wed Oct 27 2020 Étienne Guesnet <etienne.guesnet@atos.net> - 5.2.4-2
- Clean URL
- Update specfile for automated build 

* Wed Jan 08 2020 Tony Reix <tony.reix@atos.net> - 5.2.4-1
- Update to 5.2.4
- Update to new brpm rules

* Mon Aug 22 2016 Jean Girardet <jean.girardet@atos.net> - 5.2.2-2
- Manage 32/64 bits.

* Fri Aug 05 2016 Jean Girardet <jean.girardet@atos.net> - 5.2.2-1
- Initial port on AIX 6.1

* Thu Sep 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.0.4-1
- Initial port on Aix6.1
