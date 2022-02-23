# avec test : /usr/bin/rpm -ba   --define dotests=1  $SPECS/xz....spec   2>&1  | tee   $SPECS/xz....spec.res
# sans tests: /usr/bin/rpm -ba                       $SPECS/xz....spec   2>&1  | tee   $SPECS/xz....spec.res

%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}

Summary:LZMA compression utilities
Name:xz
Version:5.2.2
Release:2
License:LGPLv2+
Group:Applications/File
Source0:%{name}/%{name}-%{version}.tar.gz
Source2:liblzma.so.0-aix32
Source3:liblzma.so.0-aix64
Source4: %{name}-%{version}-%{release}.build.log

Patch0:%{name}-5.0.3-aix.patch
Patch1:%{name}-5.0.3-aix_rpath.patch
URL:http://tukaani.org/%{name}/

BuildRoot:/var/tmp/%{name}-%{version}-%{release}-root
BuildRequires:make, gettext, pkg-config, bash
Requires:%{name}-libs = %{version}-%{release}
Requires:bash, gettext

%define _libdir64 %{_prefix}/lib64


%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package libs
Summary:Libraries for decoding LZMA compression
Group:System Environment/Libraries
License:LGPLv2+

%description libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package devel
Summary:Devel libraries & headers for liblzma
Group:Development/Libraries
License:LGPLv2+
Requires:%{name}-libs = %{version}-%{release}
Requires:pkg-config

%description  devel
Devel libraries and headers for liblzma.


%package lzma-compat
Summary:Older LZMA format compatibility binaries
Group:Development/Libraries
# lz{grep,diff,more} are GPLv2+. Other binaries are LGPLv2+
License:GPLv2+ and LGPLv2+
Requires:%{name} = %{version}-%{release}
Requires:gettext
Obsoletes:lzma < 5
Provides:lzma = 5

%description  lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.


%prep
echo "DO_TESTS=%{DO_TESTS}"
%setup -q
# %patch0
# %patch1 -p1 -b .aix_rpath

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
export CONFIG_SHELL=/usr/bin/ksh
export CONFIG_ENV_ARGS=/usr/bin/ksh
export RM="/usr/bin/rm -f"

export CC="/usr/vac/bin/xlc_r -qlanglvl=extc99 -qcpluscmt"

export CFLAGS__="$CFLAGS -O2 -D_FILE_OFFSET_BITS=64"
export CXXFLAGS__="$CXXFLAGS -O2 -D_FILE_OFFSET_BITS=64"


# first build the 64-bit version
cd 64bit

export CFLAGS="$CFLAGS__ -q64"
export OBJECT_MODE=64

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
fi
/usr/sbin/slibclean


# now build the 32-bit version
cd ../32bit

export CFLAGS="$CFLAGS__ -q32"
export OBJECT_MODE="32"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --enable-shared --disable-static

gmake


if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd 64bit
export OBJECT_MODE="64"
gmake install DESTDIR=${RPM_BUILD_ROOT}

cd ../32bit
export OBJECT_MODE="32"
gmake install DESTDIR=${RPM_BUILD_ROOT}


# add the 64-bit shared objects to the shared library containing already the
# 32-bit shared objects
/usr/bin/ar -X64 -x ${RPM_BUILD_ROOT}%{_libdir64}/liblzma.a
/usr/bin/ar -X64 -q ${RPM_BUILD_ROOT}%{_libdir}/liblzma.a  liblzma.so.5
(
  rm -f     ${RPM_BUILD_ROOT}%{_libdir64}/liblzma.a
  cd        ${RPM_BUILD_ROOT}%{_libdir64}
  ln -s                      %{_libdir}/liblzma.a .
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


(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
  [ -L usr/include/lzma ] && rm -f usr/include/lzma
  mkdir -p usr/include/lzma
  cd usr/include/lzma
  ln -sf ../../..%{_prefix}/include/lzma/* .
  cd -
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system,-)
%doc 32bit/AUTHORS 32bit/README 32bit/THANKS 32bit/COPYING.* 32bit/ChangeLog 
%{_bindir}/*xz*
%{_mandir}/man1/*xz*
/usr/bin/*xz*


%files libs
%defattr(-,root,system,-)
%doc 32bit/COPYING.*
%{_libdir}/*.a
/usr/lib/*.a


%files devel
%defattr(-,root,system,-)
%doc 32bit/doc/faq.txt 32bit/doc/lzma-file-format.txt
%doc 32bit/doc/xz-file-format.txt 32bit/doc/history.txt
%{_includedir}/lzma*
%{_libdir}/*.la
%{_libdir64}/*.la
%{_libdir}/pkgconfig/liblzma.pc
%{_libdir64}/pkgconfig/liblzma.pc
/usr/include/lzma.h
/usr/include/lzma/*
/usr/lib/*.la
/usr/lib64/*.la


%files lzma-compat
%defattr(-,root,system,-)
%{_bindir}/*lz*
%{_mandir}/man1/*lz*
/usr/bin/*lz*


%changelog
* Mon Aug 22 2016 Jean Girardet <jean.girardet@atos.net> - 5.2.2-2
- Manage 32/64 bits.

* Fri Aug 05 2016 Jean Girardet <jean.girardet@atos.net> - 5.2.2-1
- Initial port on AIX 6.1

* Thu Sep 06 2012 Gerard Visiedo <gerard.visiedo@bull.net> - 5.0.4-1
- Initial port on Aix6.1
